import os

from helix import blueprint
from helix import utils


class ExamplePythonBlueprint(blueprint.Blueprint):
    """An example Python blueprint."""

    name = "example-python"
    verbose_name = "Example Python Blueprint"
    type = "python"
    version = "1.0.0"
    description = "A simple Python blueprint"

    CALLSITE_STARTUP = "startup"
    """Called at program startup.

    Calls at this callsite are called once and expected to return.
    """

    CALLSITE_LOOP = "loop"
    """Called every five seconds, indefinitely.

    Calls this callsite repeatedly, inside of a loop, until the program is
    terminated.
    """

    callsites = [CALLSITE_STARTUP, CALLSITE_LOOP]

    TEMPLATE = """import time

${functions}

if __name__ == "__main__":
    ${startup}

    while True:
        ${loop}

        time.sleep(5)
"""

    def filename(self, directory):
        """Generate a build file name in the given directory.

        Args:
            directory (str): The path to the build directory.

        Returns:
            The file path of the build file.
        """

        return os.path.join(directory, "{}.py".format(self.build_name))

    def generate(self, directory):
        functions = "\n".join(self.functions)

        startup = self.calls.pop(self.CALLSITE_STARTUP, [])
        startup = "\n    ".join(startup) or "pass"

        loop = self.calls.pop(self.CALLSITE_LOOP, [])
        loop = "\n        ".join(loop) or "break"

        source = utils.substitute(
            self.TEMPLATE, functions=functions, startup=startup, loop=loop
        )

        with open(self.filename(directory), "w") as f:
            f.write(source)

    def compile(self, directory, options):
        """Nothing to do here.

        Python is an interpreted language, so we don't really need to do
        anything in the ``compile()`` step. We still need to pass the build
        artifacts to the output, however.
        """

        return [self.filename(directory)]
