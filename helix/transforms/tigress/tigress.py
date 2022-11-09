import json
import logging
import magic
import os
import shutil

from json.decoder import JSONDecodeError
from urllib import parse, request as req
from .utils import CustomZipFile, extract_fnames

from ... import exceptions
from ... import transform
from ... import utils


logger = logging.getLogger("transform.tigress")


class TigressError(Exception):
    """Raised when Tigress fails."""

    pass


class TigressDependency(utils.Dependency):
    """Using the Tigress Transform"""

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
        with CustomZipFile(temp, "r") as z:
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
        "recipe": {"default": "simple-recipe.json"},
    }

    def supported(self, source):
        """Checks if Tigress supports the given file.

        Verifies that the source code file is written in C programming language.
        """

        m = magic.Magic()
        filetype = m.id_filename(source)

        return "C source" in filetype

    def parse_json(self, recipe, fnames):
        try:
            f = open(recipe, "r")
            logger.info("Found JSON file.")
            try:
                data = json.load(f)
                logger.info("Loaded JSON file data.")
            except JSONDecodeError:
                f.close()
                logger.error("Could not load JSON file.")
                return False

            recipe = ""

            for key in data.keys():
                if key == "Transform":
                    for t in data[key]:
                        recipe += " --Transform=" + t
                        for option in data[key][t]:
                            recipe += " --" + option + "=" + data[key][t][option]
                        recipe += " --Functions=" + ",".join(fnames)
                else:
                    recipe += " --" + key + "=" + data[key]
            f.close()
            return recipe

        except FileNotFoundError:
            logger.error("JSON file not found.")
            return False

    def transform(self, source, destination):
        """Obfuscate functions on a target source code."""

        tigress = utils.find(
            "tigress", guess=[os.path.expanduser("~/bin/tigress/3.1/tigress")]
        )

        with open(source, "r") as f:
            source_code = f.read()

        source = os.path.abspath(source)
        destination = os.path.abspath(destination)
        cwd, _ = os.path.split(source)
        fnames = extract_fnames(source_code)

        recipe = self.parse_json(self.configuration["recipe"], fnames)

        if recipe:
            env = os.environ
            env["TIGRESS_HOME"] = os.path.expanduser("~/bin/tigress/3.1")
            env["PATH"] = os.path.expanduser("~/bin/tigress/3.1:") + env["PATH"]

            cmd = "{}{} --out=result.c {}".format(tigress, recipe, source)

            utils.run(
                cmd,
                cwd,
                TigressError("Tigress failed to run with command:\n{}".format(cmd)),
                env=env,
                propagate=True,
            )

            obfuscated = cwd + "/result.c"
            os.remove(source)
            os.rename(obfuscated, source)

        else:
            logger.warning("Resulting artifact is not obfuscated by Tigress.\n")

        shutil.copy(source, destination)
