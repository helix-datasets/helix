import os
import magic

from ... import transform
from ... import utils


class StripError(Exception):
    """Raised when strip fails."""


class StripTransform(transform.Transform):
    """The linux strip binutil."""

    name = "strip"
    verbose_name = "Strip"
    type = transform.Transform.TYPE_ARTIFACT
    version = "1.0.0"
    description = "The linux strip binutil"

    dependencies = [utils.LinuxAPTDependency("binutils")]

    def supported(self, source):
        """Check if strip supports the given file."""

        source = os.path.abspath(source)

        with magic.Magic() as m:
            filetype = m.id_filename(source)

        if "ELF" not in filetype:
            return False

        return True

    def transform(self, source, destination):
        """Strip the target binary."""

        strip = utils.find("strip")

        source = os.path.abspath(source)
        destination = os.path.abspath(destination)

        cwd, _ = os.path.split(source)

        cmd = "{} {} -o {}".format(strip, source, destination)

        utils.run(cmd, cwd, StripError("strip failed to run."))
