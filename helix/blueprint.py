import os
import abc

from . import transform
from . import utils
from . import exceptions


class Blueprint(utils.Metadata, utils.Dependable, metaclass=abc.ABCMeta):
    """A common base class for all blueprints."""

    @property
    @abc.abstractmethod
    def callsites(self):
        """A list of valid callsites which Components may use.

        A good practice is to define these as constants on the Blueprint class
        as well so they may be referenced directly by components and don't rely
        on matched strings.
        """

        return []

    def __init__(self, build_name, components=None, transforms=None, *args, **kwargs):
        """Initialize the Blueprint.

        Complete a number of sanity checks, raising ``BlueprintNotSane`` if
        there are errors.

        Args:
            build_name (str): A name for this particular build
            components: An iterable of components to include.
            transforms: An iterable of transforms to include.
        """

        super().__init__(*args, **kwargs)

        if not components:
            components = []

        if not transforms:
            transforms = []

        self.build_name = build_name

        if any([not c.finalized for c in components]):
            raise exceptions.BlueprintNotSane(
                "components must be finalized before incorporating them in a Blueprint"
            )

        for component in components:
            if self.name not in component.blueprints:
                raise exceptions.BlueprintNotSane(
                    "{} does not support {} - supported Blueprint list: {}".format(
                        self, component, ", ".join(component.blueprints)
                    )
                )

            for site in component.calls:
                if site not in self.callsites:
                    raise exceptions.BlueprintNotSane(
                        "{} includes an invalid callsite for {}: {}".format(
                            component, self, site
                        )
                    )

        if any([not t.configured for t in transforms]):
            raise exceptions.BlueprintNotSane(
                "transforms must be configured before incorporating them in a Blueprint"
            )

        if len(set(components)) != len(components):
            raise exceptions.BlueprintNotSane(
                "duplicated components are supported but must be uniquely finalized"
            )

        self.components = components
        self.transforms = transforms

        self.sane()

    def sane(self):
        """Ensure the current list of components is sane.

        This method is optional and allows the developer to define additional
        constraints on the components supported by this Blueprint. This method
        should raise exceptions if the build is not sane.
        """

        return

    @property
    def tags(self):
        """Returns the union of all tags involved in this blueprint.

        Simply aggregates and dedups all tags on Components and Transforms.
        """

        grouped = [c.tags for c in self.components]
        grouped += [t.tags for t in self.transforms]

        return tuple(set([t for sublist in grouped for t in sublist]))

    @property
    def functions(self):
        """Aggregate all functions from included Components."""

        functions = []

        for component in self.components:
            functions += component.functions

        return functions

    @property
    def calls(self):
        """Aggregate all calls from included Components."""

        calls = {}

        for component in self.components:
            for site, c in component.calls.items():
                if site not in calls:
                    calls[site] = []
                calls[site] += c

        return calls

    @abc.abstractmethod
    def generate(self, directory):
        """Generates a source directory from an iterable of components.

        The components passed to this class will be finalized prior to calling
        this so that their source code is readily available. This function is
        responsible for writing configured components to the target output
        directory.

        Args:
            directory (str): A directory to write the resulting generated source
                code - you may assume that this directory already exists and is
                writable.

        Returns:
            A list of generated source files.

        Note:
            Component order matters here - this is the order in which calls and
            includes will be inserted into the generated source so if this is
            important you should make sure the order of components passed to this
            function is what you want.
        """

        return []

    def transform(self, type, targets):
        """Applies all Transforms of a given type.

        Args:
            type (str): The type of transform to apply.
            targets (str): A list of targets to transform.
        """

        transforms = [t for t in self.transforms if t.type == type]

        for transform in transforms:
            transformed = False

            if not targets:
                transformed = True

            for target in targets:
                transformed_target = "{}.transformed".format(target)
                if transform.supported(target):
                    transform.transform(target, transformed_target)

                    os.remove(target)
                    os.rename(transformed_target, target)

                    transformed = True

            if not transformed:
                raise exceptions.BuildFailure(
                    "unsupported {} transform: {}".format(transform.type, transform)
                )

    @abc.abstractmethod
    def compile(self, directory, options):
        """Compiles the target directory.

        Compiles a directory generated with ``generate``, applies any artifact
        transformations, and returns a list of build artifacts.

        Args:
            directory (str): A directory with generated source code.
            options (dict): An optional dictionary of additional build options
                that should be respected by this function. This will contain
                things like ``stdout``, ``stderr`` and ``propagate`` for
                display options.

        Returns:
            A list of built artifacts.

        Note:
            In practice this may frequently just be a bunch of calls to
            ``os.system`` to invoke the target build system of this Blueprint.
        """

        return []

    def build(self, directory, options=None):
        """Fully builds this Blueprint.

        Generates code from Components, applies source Transforms, compiles
        code, and applies artifact Transforms.

        Args:
            directory (str): A directory to write the resulting generated source
                code.
            options (dict): An optional dictionary of additional build options
                that should be used by ``compile``.

        Returns:
            A list of built and transformed artifacts.
        """

        options = options or {}

        if not os.path.isdir(directory):
            os.makedirs(directory)

        sources = self.generate(directory)
        self.transform(transform.Transform.TYPE_SOURCE, sources)
        artifacts = self.compile(directory, options=options)
        self.transform(transform.Transform.TYPE_ARTIFACT, artifacts)

        return artifacts
