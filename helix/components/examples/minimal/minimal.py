from .... import component
from .... import utils
from .... import tests


class MinimalExampleComponent(component.Component):
    """A minimal example component.

    This is a very simple example component with no configuration parameters
    and a very simple template.
    """

    name = "minimal-example"
    verbose_name = "Minimal Example"
    description = "A minimal example component."
    version = "1.0.0"
    type = "example"
    date = "2019-10-01 17:15:00.000000"
    tags = (("family", "example"), ("sample", "minimal-example"))

    blueprints = ["cmake-cpp"]

    def generate(self):
        source = utils.source(__name__, "minimal-example.cpp")

        self.functions = [source]
        self.calls = {"main": ["${minimal_example}(argc, argv);"]}
        self.globals = ["minimal_example"]


class MinimalExampleComponentTests(tests.UnitTestCase, tests.ComponentTestCaseMixin):
    blueprint = "cmake-cpp"
    component = "minimal-example"
