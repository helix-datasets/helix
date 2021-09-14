import os
import shutil
import base64

from helix import transform


class ExampleTransform(transform.Transform):
    """A simple example transform."""

    name = "example-transform"
    verbose_name = "Example Transform"
    type = transform.Transform.TYPE_ARTIFACT
    version = "1.0.0"
    description = "A simple example transform"
    tags = (("group", "example"),)

    def transform(self, source, destination):
        """Print the contents of the binary.

        This transform doesn't actually do anything, it is just a simple
        example that prints the contents of the input file, base64 encoded.
        """

        source = os.path.abspath(source)
        destination = os.path.abspath(destination)

        with open(source, "rb") as f:
            print(base64.b64encode(f.read()))

        shutil.copy(source, destination)
