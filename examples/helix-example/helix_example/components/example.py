from helix import component
from helix import tests
from helix import utils


class ExampleComponent(component.Component):
    """A simple example component."""

    name = "example-component"
    verbose_name = "Example Component"
    type = "example"
    version = "1.0.0"
    description = "A simple example component"
    date = "2020-10-20 12:00:00.000000"
    tags = (("group", "example"),)

    blueprints = ["cmake-c", "cmake-cpp"]

    options = {"message": {"default": "hello world"}}

    dependencies = [utils.LinuxAPTDependency("cowsay")]

    def generate(self):
        template = utils.source(__name__, "example.c")

        cowsay = utils.find("cowsay")
        output, _ = utils.run(
            "{} {}".format(cowsay, self.configuration["message"]), cwd="./"
        )
        formatted = repr(output.decode("utf-8")).replace("'", "")

        function = utils.substitute(template, message=formatted)

        self.functions = [function]
        self.calls = {"main": [r"${example}();"]}
        self.globals = ["example"]


class ExampleComponentTests(tests.UnitTestCase, tests.ComponentTestCaseMixin):
    blueprint = "cmake-cpp"
    component = "example-component"
