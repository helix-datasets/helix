import abc

from ... import component
from ... import utils


class SimpleTemplatedComponent(component.Component, metaclass=abc.ABCMeta):
    """A simple templated component base class.

    For components consisting of a single source file with a single call to a
    single function. This base class implements a ``generate`` method that uses
    the source files as templates for the component's configuration.
    """

    blueprints = ["cmake-cpp", "cmake-c"]
    """Supported Blueprints.

    This is specifically geared toward the CMake Blueprints and as such functions with
    both C and C++. Components that only function with one or the other should
    limit this further.
    """

    @property
    @abc.abstractmethod
    def source(self):
        """The path to the source template file."""

        return ""

    @property
    @abc.abstractmethod
    def function(self):
        """The function name to be called.

        This assumes that the function should be called with ``argc`` and
        ``argv`` as the only arguments so functions should be written
        accordingly.
        """

        return ""

    extras = []
    """Extra values to add to the globals list.

    These are included along with the ``function`` attribute when generating
    the list of Component globals.
    """

    def generate(self):
        """Generate configured source code for this component.

        This assumes that configuration parameters are intended to be strings,
        and wraps them in double quotes accordingly.
        """

        configuration = {}
        for k, v in self.configuration.items():
            if self.options[k].get("literal", False):
                configuration[k] = v
            else:
                configuration[k] = '"{}"'.format(v)

        source = utils.source(self.__class__.__module__, self.source)
        source = utils.substitute(source, **configuration)

        self.functions = [source]
        self.calls = {"main": ["${{{}}}(argc, argv);".format(self.function)]}
        self.globals = [self.function] + self.extras
