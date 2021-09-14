import os
import shutil

from ... import transform
from ... import utils


class MPRESSError(Exception):
    """Raised when UPX fails."""


class MPRESSTransform(transform.Transform):
    """The MPRESS packer."""

    name = "mpress"
    verbose_name = "MPRESS"
    type = transform.Transform.TYPE_ARTIFACT
    version = "1.0.0"
    description = "The MPRESS packer"

    dependencies = [utils.WindowsChocolateyDependency("mpress")]

    def transform(self, source, destination):
        """Apply MPRESS to the target binary."""

        source = os.path.abspath(source)
        destination = os.path.abspath(destination)

        cwd, _ = os.path.split(source)

        shutil.copy(source, destination)

        cmd = "{} {}".format(self.mpress, destination)

        utils.run(cmd, cwd, MPRESSError("MPRESS failed to run."))
