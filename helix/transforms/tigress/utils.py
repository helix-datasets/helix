import os
import re

from zipfile import ZipFile, ZipInfo
from .configurations import argument_specification, configurations, tigress_transforms
from ... import utils


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


def _validate(transform: str, configs: dict):
    """Validates configurations based on the valid choices hardcoded in `configurations.py`.

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

    for option, choice in configs.items():
        # Validates options parsed from user input.
        valid_options = configurations[transform]
        if option in valid_options.keys():
            # Determines the format that will be used to validate the choices.
            format = configurations[transform][option]

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

            # Validates the choices over the corresponding valid format.
            if format == "regex":
                combined = "(" + ")|(".join(valid_values) + ")"
                if re.fullmatch(combined, choice):
                    continue
            elif format == "list":
                choice_lst = choice.split("-")
                if len(choice_lst) == len(set(choice_lst)) and all(
                    x in valid_values for x in choice_lst
                ):
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
            elif format == "flag" or format == "":
                continue

            invalid_choices.append((transform, option, choice))
        else:
            invalid_options.append((transform, option))

    return invalid_options, invalid_choices


def _to_dict(transforms: str):
    """Takes a string representing the user's desired configurations and parses it into a
    format (dict) that can be used to validate the provided configurations.

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
    transforms_lst = []
    parsed = {}

    for i, transform in enumerate(transforms):
        try:
            name, configs = transform.split(":")

            parsed_configs = {}
            parsed_configs["transform_name"] = name
            transforms_lst.append(name)

            configs_kv = re.findall("([^=,]*)=([^,]*)", configs)
            for option, choice in configs_kv:
                parsed_configs[option] = choice

            parsed["transform-" + str(i + 1)] = parsed_configs
        except:
            parsed["transform-" + str(i + 1)] = {"transform_name": transform}
            transforms_lst.append(transform)

    parsed["transforms_lst"] = transforms_lst
    return parsed


def extract_fnames(src):
    """Extracts function names out of function definitions on C source code.

    Args:
        src (str): C source code as a string.

    Returns:
        List of function names.

    RegEx patterns explained:
        //.*\n?                     : matches code formatted as single-line comments
        /*.*?*//n?                  : matches code formatted as multi-line comments
        char|signed char|...        : matches return types
        ( |\n)(*)( |\n)             : considers functions returning pointers
        [a-zA-Z_]+[a-zA-Z0-9_]*     : matches the function name
         ?                          : matches 0 or 1 whitespace
        ([^;]*?)                    : matches parameters inside parentheses
         ?                          : matches 0 or 1 whitespace
        ?:{|\n{                     : matches the start of the body of the function definition
    """

    singleline_pattern = r"\/\/.*\n?"
    multiline_pattern = r"\/\*.*?\*\/\n?"

    regex_singleline = re.compile(singleline_pattern)
    regex_multiline = re.compile(multiline_pattern, re.DOTALL)

    src = re.sub(regex_singleline, "", src)
    src = re.sub(regex_multiline, "", src)

    pattern = r"""(?:char|signed char|unsigned char|short|short int|signed short|signed short int|
    unsigned short|unsigned short int|int|signed|signed int|unsigned|unsigned int|long|long int|
    signed long|signed long int|unsigned long|unsigned long int|long long|long long int|
    signed long long|signed long long int|unsigned long long|unsigned long long int|float|double|
    long double|void|bool)(?: |\n)(?:\*)?(?: |\n)?([a-zA-Z_]+\w*) ?(?:\([^;]*?\)) ?(?:\{|\n\{)"""
    return re.findall(pattern, src)


def _build_command(configs: dict, source=""):
    """ """
    tigress = utils.find(
        "tigress", guess=[os.path.expanduser("~/bin/tigress/3.1/tigress")]
    )
    cmd = "{} ".format(tigress)

    transforms = configs.pop("transforms")
    del transforms["transforms_lst"]
    top_level = configs

    for option, choice in top_level.items():
        option = option.title().replace("_", "")
        cmd += "--{}={} ".format(option, choice)

    for _, config in transforms.items():
        transform = config.pop("transform_name")
        cmd += "--Transform={} ".format(transform.title())

        for option, choice in config.items():
            if isinstance(configurations[transform][option], list):
                choice = choice.replace("-", ",")

            option = transform.title() + option.title().replace("_", "")
            cmd += "--{}={} ".format(option, choice)

        cmd += "--Functions=* "

    cmd += "{} --out=result.c".format(source)
    return cmd
