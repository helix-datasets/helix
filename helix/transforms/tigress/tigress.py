import os
import magic
import shutil

from helix import utils
from helix import transform
from functiondefextractor import core_extractor


class TigressError(Exception):
    """Raised when Tigress fails."""


class TigressDependency(utils.ManualPATHDependency):
    """Checks if Tigress is installed and both (PATH and TIGRESS_HOME) environment
    variables are set."""

    def installed(self):
        binary = utils.find(self.name)
        return super().installed() and os.getenv("TIGRESS_HOME") is not None


class TigressTransform(transform.Transform):
    """Transform for the Tigress C Diversifier/Obfuscator."""

    name = "tigress"
    verbose_name = "Tigress"
    type = transform.Transform.TYPE_SOURCE
    version = "1.0.0"
    description = "The Tigress Diversifier/Obfuscator."

    dependencies = [
        TigressDependency(
            name="tigress",
            help="[remember to set the TIGRESS_HOME and PATH environment variables]",
        )
    ]

    """Configuration options."""
    options = {
        "env": {"default": "x86_64:Linux:Gcc:4.6"},
        "transform": {"default": "Flatten"},
        "functions": {"default": "-"},
        "flags": {"default": ""},
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

    def transform(self, source, destination):
        """Obfuscate functions on a target source code."""

        tigress = utils.find("tigress")

        source = os.path.abspath(source)

        destination = os.path.abspath(destination)

        cwd, _ = os.path.split(source)

        # Checks if functions were provided, if not it defaults to all the functions in the src.
        if self.configuration["functions"] != "-":
            functions = self.configuration["functions"].replace("/", ",")
        else:
            extract_f = core_extractor.extractor(
                os.path.split(source)[0], exclude=r"*.cpp*"
            )
            f_names = [
                name.replace(source + "_", "") for name in extract_f["Uniq ID"].values
            ]
            functions = ",".join(f_names)

        cmd = "{} --Environment={} --Transform={} --Functions={} --out=result.c {}".format(
            tigress,
            self.configuration["env"],
            self.configuration["transform"],
            functions,
            source,
        )

        # transforms = ""
        # if "/" in self.configuration["transforms"]:
        #     config = self.configuration["transforms"].split("/")
        #     for c in config:
        #         transforms += " --Transform=" + c
        # else:
        #     transforms += " --Transform=" + self.configuration["transforms"]

        # cmd = "{} --Environment={} {} --Functions={} --out=result.c {}".format(
        #     tigress,
        #     self.configuration["env"],
        #     transforms,
        #     functions,
        #     source,
        # )

        if "/" in self.configuration["flags"]:
            config = self.configuration["flags"].split("/")
            for c in config:
                cmd += " --" + c.split(":")[0] + "=" + c.split(":")[1]
        elif self.configuration["flags"]:
            cmd += (
                " --"
                + self.configuration["flags"].split(":")[0]
                + "="
                + self.configuration["flags"].split(":")[1]
            )

        print("COMMAND: {}".format(cmd))

        utils.run(cmd, cwd, TigressError("tigress failed to run."))

        obfuscated = os.path.split(source)[0] + "/result.c"

        os.rename(obfuscated, source)
        shutil.copy(source, destination)

        # DEBUG: Prints the full command being run.
        # print("COMMAND: {}".format(cmd))

        # DEBUG: Prints the current working directory.
        # print("CWD: {}".format(cwd))

        # DEBUG: Prints the source path.
        # print("SOURCE: {}".format(source))

        # DEBUG: Prints the path of the obfuscated code.
        # print("OBFUSCATED PATH: {}".format(obfuscated))

        # DEBUG: Prints the path where the obfuscated code is being copied to.
        # print("DESTINATION: {}".format(destination))

        # DRAFT: Command wihout much configuration.
        # cmd = "{} --Environment=x86_64:Linux:Gcc:4.6 --Transform=Flatten
        # --Functions=fac,fib --out=result.c {}".format(tigress1, source)
