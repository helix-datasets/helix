import os
import json
import magic
import shutil

from helix import utils
from helix import transform

# from functiondefextractor import core_extractor


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
    description = "The Tigress Diversifier/Obfuscator."
    version = "1.0.0"
    type = transform.Transform.TYPE_SOURCE

    dependencies = [
        TigressDependency(
            name="tigress",
            help="[remember to set the TIGRESS_HOME and PATH environment variables]",
        )
    ]

    options = {
        "Environment": {"default": "x86_64:Linux:Gcc:4.6"},
        "Seed": {"default": "42"},
        "Recipe": {"default": "recipe.json"},
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

    def parse_json(self, recipe):
        f = open(recipe)
        data = json.load(f)

        recipe = ""

        for transform in data.keys():
            recipe += " --Transform=" + transform
            for option in data[transform].keys():
                recipe += " --" + option + "=" + data[transform][option]

        return recipe

    def transform(self, source, destination):
        """Obfuscate functions on a target source code."""

        tigress = utils.find("tigress")

        source = os.path.abspath(source)

        destination = os.path.abspath(destination)

        cwd, _ = os.path.split(source)

        try:
            recipe = self.parse_json(self.configuration["Recipe"])
        except:
            print("Failed to open recipe; using default transform (Flatten).")
            recipe = " --Transform=Flatten --Functions=main"  # supposes there's a main function

        cmd = "{} --Environment={} --Seed={}{} --out=result.c {}".format(
            tigress,
            self.configuration["Environment"],
            self.configuration["Seed"],
            recipe,
            source,
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


# OLD CODE
# options = {
#     "Environment": {"default": "x86_64:Linux:Gcc:4.6"},
#     "Seed": {"default": "42"},
#     "Configuration": {
#         "default": "Transform:Flatten_FlattenDispatch:goto_Functions:main"
#     },
# }

# options = {s
#     "Environment": {"default": "x86_64:Linux:Gcc:4.6"},
#     "Seed": {"default": "42"},
#     "Configuration": {
#         "default": "Transform:InitEntropy_Functions:main_InitEntropyKinds:vars_Transform:InitOpaque_Functions:main_InitOpaqueStructs:list,array,env_Transform:InitBranchFuns_InitBranchFunsCount:1_Transform:AddOpaque_Functions:main_AddOpaqueStructs:list_AddOpaqueKinds=true_Transform:AntiBranchAnalysis_Functions:main_Transform:EncodeArithmetic_Functions:main"
#     },
# }

# Checks if functions were provided, if not it defaults to all the functions in the src.
# if self.configuration["functions"] != "-":
#     functions = self.configuration["functions"].replace("/", ",")
# else:
#     extract_f = core_extractor.extractor(
#         os.path.split(source)[0], exclude=r"*.cpp*"
#     )
#     f_names = [
#         name.replace(source + "_", "") for name in extract_f["Uniq ID"].values
#     ]
#     functions = ",".join(f_names)
