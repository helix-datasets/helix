import json
import magic
import os
import shutil
from urllib import parse, request as req

from json.decoder import JSONDecodeError

from ... import utils
from ... import transform
from ... import exceptions


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
        print("  By installing, you accept the Tigress End-User License Agreement.")
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

        temp = os.path.expanduser("~/Downloads/tigress-3.1-bin.zip")
        destination = os.path.expanduser("~/Downloads")

        open(temp, "wb").write(response.read())
        shutil.unpack_archive(temp, destination)
        os.remove(temp)

        exec_permission = "chmod -R u+x " + destination + "/tigress"
        utils.run(exec_permission)

    def installed(self):
        """Checks if Tigress is installed by guessing the path to the binary."""
        binary = utils.find(
            "tigress", guess=[os.path.expanduser("~/Downloads/tigress/3.1/tigress")]
        )

        return binary is not None


class TigressTransform(transform.Transform):
    """Transform for the Tigress C Diversifier/Obfuscator."""

    name = "tigress"
    verbose_name = "Tigress"
    description = "The Tigress Diversifier/Obfuscator (v3.1)."
    version = "1.0.0"
    type = transform.Transform.TYPE_SOURCE

    dependencies = [TigressDependency("tigress")]

    options = {
        "Recipe": {"default": "simple-recipe.json"},
    }

    def supported(self, source):
        """Checks if Tigress supports the given file.

        Verifies that the target file has a .c file extension.
        """

        m = magic.Magic()
        filetype = m.id_filename(source)

        if "C source" in filetype:
            return True
        else:
            return False

    def parse_json(self, recipe, fnames):
        try:
            f = open(recipe, "r")
            print("> Found JSON file.")
            try:
                data = json.load(f)
                print("> Loaded JSON file data.")
            except JSONDecodeError:
                f.close()
                print("> Could not load JSON file.")
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
            print("> JSON file not found.")
            return False

    def transform(self, source, destination):
        """Obfuscate functions on a target source code."""

        tigress = utils.find(
            "tigress", guess=[os.path.expanduser("~/Downloads/tigress/3.1/tigress")]
        )

        with open(source, "r") as f:
            source_code = f.read()

        source = os.path.abspath(source)
        destination = os.path.abspath(destination)
        cwd, _ = os.path.split(source)
        fnames = utils.extract_fnames(source_code)

        recipe = self.parse_json(self.configuration["Recipe"], fnames)

        if recipe:
            env = os.environ
            env["TIGRESS_HOME"] = os.path.expanduser("~/Downloads/tigress/3.1")
            env["PATH"] = os.path.expanduser("~/Downloads/tigress/3.1:") + env["PATH"]

            cmd = "{}{} --out=result.c {}".format(tigress, recipe, source)

            utils.run(
                cmd,
                cwd,
                TigressError("Tigress failed to run with command:\n{}".format(cmd)),
                env=env,
            )

            obfuscated = cwd + "/result.c"
            os.remove(source)
            os.rename(obfuscated, source)

        else:
            print("> Resulting artifact is not obfuscated by Tigress.\n")

        shutil.copy(source, destination)
