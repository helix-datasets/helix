import os

from ... import transform
from ... import utils


class UPXError(Exception):
    """Raised when UPX fails."""


class UPXTransform(transform.Transform):
    """The UPX packer."""

    name = "upx"
    verbose_name = "UPX"
    type = transform.Transform.TYPE_ARTIFACT
    version = "1.0.0"
    description = "The UPX packer"

    if os.name == "posix":
        dependencies = [utils.LinuxAPTDependency("upx-ucl")]
    elif os.name == "nt":
        dependencies = [utils.WindowsChocolateyDependency("upx")]

    def supported(self, source):
        """Check if UPX supports the given file.

        UPX's file constraints are somewhat opaque - the most accurate (though
        slightly inefficient) thing to do here is to just attempt to transform
        the given file and, if successful, then we know that the file is
        supported.
        """

        try:
            self.transform(source, os.devnull)
        except UPXError:
            return False

        return True

    def transform(self, source, destination):
        """Apply UPX to the target binary."""

        upx = utils.find("upx")

        source = os.path.abspath(source)
        destination = os.path.abspath(destination)

        cwd, _ = os.path.split(source)

        cmd = "{} {} -o {} -f".format(upx, source, destination)

        utils.run(cmd, cwd, UPXError("UPX failed to run."))
