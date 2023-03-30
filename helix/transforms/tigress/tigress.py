import copy
import logging
import os
import shutil
from urllib import parse
from urllib import request as req

import magic

from ... import exceptions, transform, utils
from . import utils as tigress_utils
from .configurations import tigress_transforms

logger = logging.getLogger("transform.tigress")


class TigressError(Exception):
    """Raised when Tigress fails."""

    pass


class TigressDependency(utils.Dependency):
    """Using the Tigress Transform."""

    def __init__(self, name):
        if os.name != "posix":
            raise exceptions.ConfigurationError(
                "unsupported platform for this dependency type: {}".format(os.name)
            )

        self.name = name

    def install(self, verbose):
        """Downloading Tigress binaries and adding execution permission."""
        logger.info("By installing, you accept the Tigress End-User License Agreement.")

        url = "http://tigress.cs.arizona.edu/cgi-bin/projects/tigress/download.cgi"
        data = {
            "accept": "Accept and Download",
            "mode": "download",
            "buffer": "address:----email:----file:tigress-3.1-bin.zip----name:----remote_addr=----timestamp:----",
            "file": "tigress-3.1-bin.zip",
            "destfile": "tigress-3.1-bin.zip",
        }
        data = parse.urlencode(data).encode()
        request = req.Request(url=url, data=data)
        response = req.urlopen(request)

        destination = os.path.expanduser("~/bin")
        if not os.path.exists(destination):
            os.makedirs(destination)

        temp = destination + "/tigress-3.1-bin.zip"

        open(temp, "wb").write(response.read())
        with tigress_utils.CustomZipFile(temp, "r") as z:
            z.extractall(destination)

        os.remove(temp)

    def installed(self):
        """Checks if Tigress is installed by guessing the path to the binary."""
        binary = utils.find(
            "tigress", guess=[os.path.expanduser("~/bin/tigress/3.1/tigress")]
        )

        return binary is not None


class TigressTransform(transform.Transform):
    """Transform for the Tigress C Diversifier/Obfuscator."""

    name = "tigress"
    verbose_name = "Tigress"
    description = "The Tigress Diversifier/Obfuscator (v3.1)"
    version = "1.0.0"
    type = transform.Transform.TYPE_SOURCE

    dependencies = [TigressDependency("tigress")]

    options = {
        "environment": {"default": "x86_64:Linux:Gcc:4.6"},
        "seed": {"default": "0"},
        "file_prefix": {"default": "NONE"},
        "transforms": "",
    }

    def supported(self, source):
        """Checks if Tigress supports the given file.

        Verifies that the source code file is written in C programming language.
        """

        m = magic.Magic()
        filetype = m.id_filename(source)

        return "C source" in filetype

    def validate_configuration(self):
        """
        Provides custom configuration validation.

        This method checks that at least one valid transform was provided and that both options &
        choices provided are valid. By parsing the user input, it creates a dictionary that will
        be validated by a call to the ``tigress_utils.validate()`` method. Raises a ConfigurationError
        if any user input is invalid and raises an Exception.
        """
        invalid_transforms = list()
        invalid_options = list()
        invalid_choices = list()

        # Validates global top_level configurations.
        configs = {
            k: self.configuration[k] for k in self.configuration.keys() - {"transforms"}
        }
        _, ic = tigress_utils.validate("top_level", configs)
        invalid_choices.extend(ic)

        # Parses ``transforms`` option into dict for validation.
        parsed = tigress_utils.to_dict(self.configuration["transforms"])
        self.configuration["transforms"] = copy.deepcopy(parsed)

        # Validates user provided transforms.
        usr_transforms = parsed.pop("transforms_lst")
        usr_transforms.sort()

        invalid_transforms = [t for t in usr_transforms if t not in tigress_transforms]
        invalid_transforms.sort()

        if usr_transforms == invalid_transforms:
            raise exceptions.ConfigurationError("no valid transform was provided")

        # Validates user provided option/choice; excluding those from the invalid transforms.
        for obj in parsed.values():
            transform = obj.pop("transform_name")
            if transform not in invalid_transforms:
                configs = {option: obj[option] for option in obj.keys()}
                if configs:
                    io, ic = tigress_utils.validate(transform, configs)
                    invalid_options.extend(io)
                    invalid_choices.extend(ic)

        # If any invalid configuration was provided raises a configuration error with a log message.
        if invalid_transforms or invalid_options or invalid_choices:
            tigress_utils.raise_config_error(
                invalid_transforms, invalid_options, invalid_choices
            )

    def transform(self, source, destination):
        """Obfuscate functions on a target source code."""
        source = os.path.abspath(source)
        with open(source, "r+") as s:
            src_code = s.read()
            s.seek(0, 0)
            s.write(
                '#include "'
                + os.path.expanduser("~/bin/tigress/3.1/tigress.h")
                + '"\n'
                + src_code
            )

        destination = os.path.abspath(destination)
        cwd, _ = os.path.split(source)

        cmd = tigress_utils.build_command(self.configuration, source)

        env = os.environ
        env["TIGRESS_HOME"] = os.path.expanduser("~/bin/tigress/3.1")
        env["PATH"] = os.path.expanduser("~/bin/tigress/3.1:") + env["PATH"]

        utils.run(
            cmd,
            cwd,
            TigressError("Tigress failed to run with command:\n{}".format(cmd)),
            env=env,
        )

        obfuscated = cwd + "/result.c"
        os.rename(source, cwd + "/source.c")
        os.rename(obfuscated, source)

        shutil.copy(source, destination)
