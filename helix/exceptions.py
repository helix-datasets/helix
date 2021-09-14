"""Custom named exceptions."""


class EntrypointNotFound(Exception):
    """Raised when an entrypoint cannot be found."""


class ConfigurationError(Exception):
    """Raised when there are configuration problems."""


class NotConfigured(Exception):
    """Raised when a component should have been configured."""


class NotGenerated(Exception):
    """Raised when a component should have been generated."""


class NotInstalled(Exception):
    """Raised when a component's dependencies are not installed."""


class BlueprintNotSane(Exception):
    """Raised when a Blueprint is not sane."""


class BuildFailure(Exception):
    """Raised when a Blueprint build fails."""


class MissingDependency(Exception):
    """Raised when a dependency cannot be found."""


class DependencyInstallationFailure(Exception):
    """Raised when dependency installation fails."""

    def __init__(self, *args, help=None, **kwargs):
        self.help = help
