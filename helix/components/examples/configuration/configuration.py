from .... import component
from .... import utils


class ConfigurationExampleComponent(component.Component):
    """A minimal example component with configuration.

    This is a very simple example component with simple configuration
    parameters and a very simple template.
    """

    name = "configuration-example"
    verbose_name = "Configuration Example"
    description = "A minimal example component with configuration."
    version = "1.0.0"
    type = "example"
    date = "2019-10-01 17:15:00.000000"
    tags = (("family", "example"), ("sample", "configuration-example"))

    blueprints = ["cmake-cpp"]

    options = {"first_word": {"default": "hello"}, "second_word": {}}

    def generate(self):
        """Generate configured source code for this component

        This is a very simple component with no configuration - this simply
        loads the template files.
        """

        configuration = {k: '"{}"'.format(v) for k, v in self.configuration.items()}

        source = utils.source(__name__, "configuration-example.cpp")
        source = utils.substitute(source, **configuration)

        self.functions = [source]
        self.calls = {"main": ["${configuration_example}(argc, argv);"]}
        self.globals = ["configuration_example"]
