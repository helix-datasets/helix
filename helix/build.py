from . import utils
from . import exceptions


def sane(configuration):
    """Checks configuration sanity, raising exceptions if there are problems."""

    def assert_key(dictionary, *keys):
        found = False

        for key in keys:
            if key in dictionary:
                found = True

        if not found:
            raise exceptions.ConfigurationError(
                "missing configuration key(s): {}".format(" | ".join(keys))
            )

    assert_key(configuration, "name")
    assert_key(configuration, "blueprint")
    assert_key(configuration, "components")
    assert_key(configuration, "transforms")

    assert_key(configuration["blueprint"], "name", "class")

    for component in configuration["components"]:
        assert_key(component, "name", "class")

    for transform in configuration["transforms"]:
        assert_key(transform, "name", "class")


def load(entrypoint, specification):
    """Loads the class specified by a given specification.

    This function allows Blueprints, Components, and Transforms to be specified
    either by name or directly by class using different keys. If ``name`` is
    given in ``specification``, the target class will be loaded from the given
    ``entrypoint`` by name. If ``class`` instead is given, the class specified
    will be returned directly. If both are given, ``class`` is given priority.

    Args:
        entrypoint: The entrypoint from which a class should be loaded if given
            by name.
        specification: A dictionary specification of a Blueprint, Component, or
            Transform.

    Returns:
        The target class of the given specification.
    """

    if "class" in specification:
        return specification["class"]
    elif "name" in specification:
        return utils.load(entrypoint, specification["name"])
    else:
        raise exceptions.ConfigurationError(
            "{}: must specify a target by class or name".format(specification)
        )


def build(configuration, output, options=None):
    """Build a given configuration.

    Builds the given ``configuration`` dictionary using ``output`` as a
    working directory.

    Args:
        configuration: A dictionary describing blueprint, components, and
            transforms to use for this build.
        output (str): The path to the output directory.
        options (dict): An optional dictionary of additional options to be
            passed to the build command.

    Returns:
        A list of build artifact paths.

    Example:
        Example configuration dictionary::

            {
                "name": "test",
                "blueprint": {"name": "cmake-cpp"},
                "components": [
                    {"name": "minimal-example"},
                    {
                        "name": "configuration-example",
                        "configuration": { "second_word": "world" }
                    }
                    {"class": components.MinimalExampleComponent}
                ],
                "transforms": [
                    ...
                ]
            }

        Configuration parameters are passed via the ``configuration`` key. Note
        that Blueprints, Components and Transforms may be specified by either
        ``name`` or directly by ``class``.
    """

    options = options or {}

    sane(configuration)

    blueprint = load("helix.blueprints", configuration["blueprint"])

    components = []
    for specification in configuration["components"]:
        component = load("helix.components", specification)()
        component.configure(**specification.get("configuration", {}))
        component.generate()
        component.finalize()

        components.append(component)

    transforms = []
    for specification in configuration["transforms"]:
        transform = load("helix.transforms", specification)()
        transform.configure(**specification.get("configuration", {}))

        transforms.append(transform)

    blueprint = blueprint(configuration["name"], components, transforms)
    artifacts = blueprint.build(output, options=options)

    return artifacts, blueprint.tags
