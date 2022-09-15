from ... import component
from ... import utils
from ... import tests


class FibonacciComponent(component.Component):
    """Tigress Test Fibonacci component."""

    name = "fibonacci"
    verbose_name = "Fibonacci Component"
    description = "Evaluate the Fibonacci of a number."
    version = "1.0.0"
    type = "example"
    date = "2022-08-26 15:06:00.000000"
    tags = (("family", "example"), ("sample", "fibonacci"))
    options = {"number": {"default": "5"}}
    function = "fib"

    blueprints = ["cmake-c"]

    def generate(self):
        source = utils.source(__name__, "fibonacci.c")
        self.functions = [source]
        self.calls = {
            "main": ["${}({});".format(self.function, self.configuration["number"])]
        }
        self.globals = [self.function]


class FibonacciComponentTests(tests.UnitTestCase, tests.ComponentTestCaseMixin):
    blueprint = "cmake-c"
    component = "fibonacci"
