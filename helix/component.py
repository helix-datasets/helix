import abc
import uuid

from . import utils
from . import exceptions


class Component(
    utils.Metadata, utils.Configurable, utils.Dependable, metaclass=abc.ABCMeta
):
    """A common base class for all components.

    A component represents a single, configurable unit of functionality. This
    may be as simple as a single function or as complex as an entire command
    and control library.
    """

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    @property
    @abc.abstractmethod
    def date(self):
        """A relevant date.

        Possibly the initial publication date of this sample or compile
        timestamp. This does not need to be exact but may be useful for some
        applications of the final dataset and will be included.

        Note:
            The date should be in a string format parsable with ``DATE_FORMAT``
        """

        return ""

    @property
    @abc.abstractmethod
    def blueprints(self):
        """A list of the Blueprints supported by this component.

        This should be a list of the string names of supported Blueprint and
        must match the corresponding ``Blueprint.name`` property.
        """

        return []

    functions = []
    """A list of functions included in this Component.

    This list of functions may be defined either in the Component class
    (for relatively simple components) or may be populated by the
    implementation of the ``generate()`` method.
    """

    calls = {}
    """A dictionary of callsites (defined by Blueprints) to call strings.

    This dictionary of calls may be defined either in the Component class (for
    relatively simple components) or may be populated by the implementation of
    the ``generate()`` method.
    """

    globals = []
    """A list of template parameter names that must be globally unique.

    These template parameters are present in the ``functions`` and ``calls``
    parameters and will be substituted for a globally unique value when this
    Component is finalized. This list should encompass all of the parts of this
    Component that must be globally unique (e.g., function names, global
    variable names). A good test to ensure that all of the globally unique
    parameters have been templated is to try to build a Blueprint with two
    instances of this component.
    """

    @property
    def generated(self):
        """Indicates if this Component has been generated yet.

        Note:
            This assumes that the Component has been generated if functions or
            calls have been set. This means that components which define a
            generate method should leave these parameters empty and set them
            inside of the ``generate()`` method only. A hybrid aproach of
            partially setting these parameters and then updating them inside of
            the ``generate()`` method is not advised.
        """

        return self.functions or self.calls

    def generate(self):
        """Generate configured source code for this component.

        This function is responsible for any necessary code generation.
        ``configure`` will be called before generate so this function may draw
        from any instance attributes (set by ``configure``) for configuration
        parameters. This function may be used to populate/modify the
        ``functions`` and ``calls`` properties of this Component.

        Note:
            Defining this method is optional - relatively simple components may
            find it easy enough to simply define all of the data they may need
            directly on the class.
        """

    finalized = False

    def finalize(self):
        """Make this Component unique.

        Uses the ``globals`` list to generate and insert globally unique values
        into the ``functions`` and ``calls`` properties to prepare this
        Component to be used by a Blueprint.
        """

        if not self.configured:
            raise exceptions.NotConfigured("cannot finalize an unconfigured component")

        if not self.generated:
            raise exceptions.NotGenerated("cannot finalize an ungenerated component")

        globals = {g: "{}_{}".format(g, uuid.uuid4().hex) for g in self.globals}

        try:
            self.functions = [
                utils.substitute(f, safe=False, **globals) for f in self.functions
            ]

            for site in self.calls:
                self.calls[site] = [
                    utils.substitute(c, safe=False, **globals) for c in self.calls[site]
                ]
        except KeyError as e:
            raise KeyError(
                "unresolved parameter {} (hint: double check your globals list and options parameters)".format(
                    e
                )
            )

        self.finalized = True
