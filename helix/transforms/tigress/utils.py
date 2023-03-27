import os
import re
from zipfile import ZipFile, ZipInfo

from ... import utils
from .configurations import argument_specification
from .configurations import configurations as valid_configs
from .configurations import top_level_transform_specific


class CustomZipFile(ZipFile):
    """Overriding ``_extract_member`` method to handle file permissions.

    This allows to take advantage of ZipInfo.external_attr that returns external
    file information in the form of 4 bytes. The high order two bytes represent
    file type bits and UNIX permission.

    Source: https://stackoverflow.com/questions/39296101/python-zipfile-removes-execute-permissions-from-binaries
    """

    def _extract_member(self, member, targetpath, pwd):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)

        targetpath = super()._extract_member(member, targetpath, pwd)
        mode = member.external_attr >> 16

        if mode != 0:
            os.chmod(targetpath, mode)

        return targetpath


def validate(transform: str, configs: dict):
    """Validates configurations based on the valid option/choices hardcoded in `configurations.py`.

    This function uses the following formats to validate configurations:
        * regex     configs should match any of the combined regex representing valid configurations
        * list      configs in the form of "-" separated lists should have valid and non-repeated elements
        * tuple     configs should be part of the list of valid configurations in the tuple
        * float     configs should be able to be transformed into a float literal with the float() casting
        * flag      validates that the flag name is valid
        * None      validates that the option is valid; and takes as choice any string

    Args:
        transform (str): transform to whom the configurations belong
        configs (dict): holds the desired configurations as key, value pairs

    Returns:
        invalid_options (list): list of tuples representing invalid options
            e.g. [(<transform>, <option>)]
        invalid_choices: (list): list of tuples representing invalid choices
            e.g. [(<transform>, <option>, <choice>)]
    """
    invalid_options = []
    invalid_choices = []

    # Validates configurations (option/choice) parsed from user input.
    for option, choice in configs.items():
        valid_options = valid_configs[transform]

        # Verifies that option is valid.
        if option in valid_options.keys():

            # Determines the format that will be used to validate the user choice.
            format = valid_configs[transform][option]

            # Handles formats different than the ones hardcoded in the `utils.argument_specification` dict.
            if isinstance(format, list):
                valid_values = format
                format = "list"
            elif isinstance(format, tuple):
                valid_values = list(format)
                format = "tuple"
            elif isinstance(format, bool):
                format = "flag"
            else:
                valid_values, format = argument_specification[format]

            # Validates the choices based on the determined format.
            if format == "regex":
                combined = "(" + ")|(".join(valid_values) + ")"
                if re.fullmatch(combined, choice):
                    continue
            elif format == "list":
                choice_lst = choice.split("-")
                not_repeated = len(choice_lst) == len(set(choice_lst))
                valid = all(x in valid_values for x in choice_lst)
                if not_repeated and valid:
                    continue
            elif format == "tuple":
                if choice in valid_values:
                    continue
            elif format == "float":
                try:
                    float(choice)
                    continue
                except ValueError:
                    pass
            elif format == "flag" or format == None:
                continue

            # Handles invalid choice.
            invalid_choices.append((transform, option, choice))

        # Handles invalid option.
        else:
            invalid_options.append((transform, option))

    return invalid_options, invalid_choices


def to_dict(transforms: str):
    """Takes the user input (str) and parses it into a format (dict) that will be used to validate the provided
    configurations.

    Args:
        transforms (str): a string representing a tigress configuration
            e.g. 'split:kinds=block-level-recursive,name=first;split;split:kinds=level-recursive-block,name=third

    Returns:
        parsed (dict): a dictionary representing the user's configurations
            e.g. parsed = {
                    'transform-1': {
                        'transform_name': 'split',
                        'kinds': 'block-level-recursive',
                        'name': 'first'
                    },
                    'transform-2': {
                        'transform_name': 'split'
                    },
                    'transform-3': {
                        'transform_name': 'split',
                        'kinds': 'level-recursive-block',
                        'name': 'third'
                    },
                    transforms_lst = ['split', 'split', 'split']
                }
    """
    transforms = transforms.split(";")
    transforms_lst = list()
    parsed = dict()

    for i, transform in enumerate(transforms):
        # The `try`` block will succeed if a transform has configurations.
        try:
            tf, configs = transform.split(":")

            parsed_configs = {}
            parsed_configs["transform_name"] = tf
            transforms_lst.append(tf)

            configs_kv = re.findall("([^=,]+)(=[^,=]+)?", configs)
            for option, choice in configs_kv:
                parsed_configs[option] = choice[1:]

            parsed["transform-" + str(i + 1)] = parsed_configs

        # The `except` block handles transforms without specific configurations.
        except:
            transforms_lst.append(transform)
            parsed["transform-" + str(i + 1)] = {"transform_name": transform}

    parsed["transforms_lst"] = transforms_lst
    return parsed


def tigress_format(option: str):
    return option.title().replace("_", "")


def build_command(configs: dict, source: str):
    """Function used to build the actual Tigress command to run.

    This function is also in charge of modifying configurations to match the Tigress syntax.

    Args:
        configs (dict): dictionary holding the desired configurations
        source (str): path to source code

    Returns:
        cmd (str): a string representing the Tigress command to run
    """
    # Adds Tigress binary path to `cmd`.
    tigress = utils.find(
        "tigress", guess=[os.path.expanduser("~/bin/tigress/3.1/tigress")]
    )
    cmd = "{} ".format(tigress)

    # Separates global top-level configs from the transform specific configurations.
    transforms = configs.pop("transforms")
    del transforms["transforms_lst"]
    top_level = configs

    # Adds global top-level configurations to `cmd`.
    for option, choice in top_level.items():
        cmd += "--{}={} ".format(tigress_format(option), choice)

    # Adds parsed transform configurations into `cmd`.
    for config in transforms.values():
        transform = config.pop("transform_name")
        tf = tigress_format(transform)
        cmd += "--Transform={} ".format(tf)

        for option, choice in config.items():
            # Considers flag options that don't require a choice.
            if isinstance(valid_configs[transform][option], bool):
                cmd += "--{} ".format(tf + tigress_format(option))
            else:
                # Modifies list-like options to use "," (Tigress syntax) instead of "-"
                # (Helix syntax).
                if isinstance(valid_configs[transform][option], list):
                    choice = choice.replace("-", ",")

                # Transform specific top-level configs don't require the transform name as prefix.
                if option in top_level_transform_specific.keys():
                    option = tigress_format(option)
                else:
                    option = tf + tigress_format(option)

                cmd += "--{}={} ".format(option, choice)

        # Deafults to obfuscating all functions in source.
        cmd += "--Functions=* "

    cmd += "{} --out=result.c".format(source)
    return cmd
