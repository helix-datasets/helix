import abc

from . import utils


class Transform(
    utils.Metadata, utils.Configurable, utils.Dependable, metaclass=abc.ABCMeta
):
    """A common base class for all transforms."""

    TYPE_SOURCE = "source"
    """A source-to-source transformation.

    Setting ``Transform.type`` to ``TYPE_SOURCE`` indicates to Blueprints that
    this Transform should be fed source files and should produce modified
    source files.
    """

    TYPE_ARTIFACT = "artifact"
    """An artifact-to-artifact transformation.

    Setting ``Transform.type`` to ``TYPE_ARTIFACT`` indicates to Blueprints
    that this Transform should be fed built artifacts and should produce
    modified built artifacts.
    """

    def supported(self, source):
        """Check if the given source is supported.

        This method is optional - the default behavior is to assume all sources
        are suppored.

        Args:
            source (str): The source material for this tranformation.

        Returns:
            ``True`` if the target is supported by this transform, ``False``
            otherwise.
        """

        return True

    @abc.abstractmethod
    def transform(self, source, destination):
        """Apply this transform.

        Applies this transform to the given ``source`` and writes the output to
        ``destination``. If this transform expects configuration, this method
        should raise exceptions if ``configured`` is ``False`` when this is
        called.

        Args:
            source (str): The source material for this tranformation.
            destination (str): The destination to write the output of this
                transformation.
        """

        return None
