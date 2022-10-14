import json
import magic
import os
import shutil

from json.decoder import JSONDecodeError

from ... import utils
from ... import transform


class TigressError(Exception):
    """Raised when Tigress fails."""


class TigressDependency(utils.ManualPATHDependency):
    """Checks if Tigress is installed and both (PATH and TIGRESS_HOME) environment
    variables are set."""

    def installed(self):
        return super().installed() and os.getenv("TIGRESS_HOME") is not None


class TigressTransform(transform.Transform):
    """Transform for the Tigress C Diversifier/Obfuscator."""

    name = "tigress"
    verbose_name = "Tigress"
    description = "The Tigress Diversifier/Obfuscator (v3.3.2)."
    version = "1.0.0"
    type = transform.Transform.TYPE_SOURCE

    dependencies = [
        TigressDependency(
            name="tigress",
            help="[remember to set the TIGRESS_HOME and PATH environment variables]",
        )
    ]

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

        tigress = utils.find("tigress")

        with open(source, "r") as f:
            source_code = f.read()

        source = os.path.abspath(source)
        destination = os.path.abspath(destination)
        cwd, _ = os.path.split(source)
        fnames = utils.extract_fnames(source_code)

        recipe = self.parse_json(self.configuration["Recipe"], fnames)

        if recipe:
            cmd = "{}{} --out=result.c {}".format(tigress, recipe, source)

            utils.run(
                cmd,
                cwd,
                TigressError("Tigress failed to run with command:\n{}".format(cmd)),
            )

            obfuscated = cwd + "/result.c"
            os.remove(source)
            os.rename(obfuscated, source)

        else:
            print("> Resulting artifact is not obfuscated by Tigress.\n")

        shutil.copy(source, destination)
