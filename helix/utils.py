import os
import re
import abc
import string
import subprocess
import pkg_resources

from . import exceptions


class Metadata(object, metaclass=abc.ABCMeta):
    """A common metadata storage mixin."""

    @property
    @abc.abstractmethod
    def name(self):
        """A simple name.

        Names should consist of `[a-z-]`. Make use of the optional
        ``verbose_name`` property if you would like a pretty-printable version
        of this name.
        """

        return ""

    @property
    @abc.abstractmethod
    def verbose_name(self):
        """Optional verbose name for pretty printing.

        By default this will just return ``name``.
        """

        return self.name

    @property
    @abc.abstractmethod
    def description(self):
        return ""

    @property
    @abc.abstractmethod
    def version(self):
        """A version number.

        This should be a string using `Semantic Versioning`_.

        .. _Semantic Versioning:
            https://semver.org/
        """

        return ""

    @property
    @abc.abstractmethod
    def type(self):
        """A short type descriptor.

        This should be set to some constant (a short string) defined in some
        common location.
        """

        return ""

    tags = ()
    """An optional iterable of human-readable tag tuples.

    Tags may represent family or component groupings and are fairly loosely
    defined.

    Example:
        An ``APT29``/``SEDINT`` sample may be defined as
        ``(("family", "APT29"), ("sample", "SEDINT"))``
    """

    @classmethod
    def string(cls):
        return "{} ({}) [{}]".format(cls.verbose_name, cls.version, cls.name)

    def __str__(self):
        return self.__class__.string()


class Configurable(object, metaclass=abc.ABCMeta):
    """A common configuration parsing mixin."""

    options = {}
    """A dictionary of configurable options and default values.

    This defines which options which may be edited with a call to
    ``configure``.

    Example:

        A subclass with both required and default parameters may be defined
        as::

            options = {
                "server": {},
                "port": {"default": 1337}
            }
    """

    def validate_configuration(self):
        """Custom option validation code.

        This optional method may be implemented on subclasses to provide custom
        configuration validation and is called by the ``configure`` method. If
        invalid configuration is detected, this method should raise
        ``ConfigurationError``. Parsed configuration values are stored in
        ``configuration`` by the time this is called.
        """

        return

    _configuration = {}

    @property
    def configuration(self):
        """Parsed configuration parameters.

        This is populated by the ``configure`` method, controlled by the
        ``options`` parameter. If this has not yet been configured, this raises
        a ``NotConfigured`` exception.
        """

        if not self.configured:
            raise exceptions.NotConfigured(
                "{} has not been configured yet".format(self)
            )

        return self._configuration

    _configured = False

    @property
    def configured(self):
        """Indicates if this has been configured.

        This attribute is set ``True`` by the ``configure`` method. Components are
        reconfigurable, so ``configure`` may still be called if ``configured`` is
        ``True``.

        A Configurable with no configuration options is considered to be
        already configured.
        """

        return not self.options or self._configured

    def configure(self, **kwargs):
        """Parse configuration data passed as kwargs.

        Configuration values taken from ``options`` will be passed to this
        function as kwargs. This function is responsible for parsing and
        storing those configuration options and storing them in
        ``configuration``.

        Args:
            **kwargs: Arbitrary keyword arguments corresponding to fields in
                ``options``

        Note:
            Although it is possible to pass values of varying types to this
            method, it is recommended that code which makes use of
            configuration parameters assumed that they are a string, since
            configuration parameters parsed from command line arguments and
            configuration files will be passed as strings.
        """

        configuration = {}

        for option, config in self.options.items():
            if option in kwargs:
                configuration[option] = kwargs.pop(option)
            elif "default" in config:
                configuration[option] = config["default"]
            else:
                raise exceptions.ConfigurationError(
                    "{}: missing required configuration parameter: {}".format(
                        self.__class__.__name__, option
                    )
                )

        if kwargs:
            raise exceptions.ConfigurationError(
                "{}: invalid configuration parameter: {}".format(
                    self.name, list(kwargs.keys())[0]
                )
            )

        self._configuration = configuration

        self._configured = True

        try:
            self.validate_configuration()
        except:
            self._configured = False
            raise


class Dependency(object, metaclass=abc.ABCMeta):
    """A base class for dependency definitions.

    This defines the interface for all dependency installers.
    """

    @abc.abstractmethod
    def install(self, verbose=False):
        """Install this dependency.

        Raise a ``DependencyInstallationFailure`` on error.

        Args:
            verbose (boolean): Verbosity.
        """

    @abc.abstractmethod
    def installed(self):
        """Check if this dependency is installed.

        Returns:
            ``True`` if this has already been installed, and ``False``
            otherwise.
        """

    def string(self):
        """The string representation of this dependency.

        Example:
            The name of the package to install or the path to a script to run.
        """

        return ""

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self.string())

    def __repr__(self):
        return str(self)


class ManualDependency(Dependency):
    """A dependency that must be manually installed.

    This dependency always fails installation with the given name and
    optional help message and is intended to indicate to the user that they
    must manually install something theirselves.

    Args:
        name (str): The name of this dependency.
        help (str): A short description of how to install this dependency
            manually. Optional, but recommended.
    """

    def __init__(self, name, help=None):
        self.name = name
        self.help = help

    def install(self, verbose=False):
        raise exceptions.DependencyInstallationFailure(
            "{} must be installed manually".format(self.name), help=self.help
        )

    def string(self):
        return self.name


class ManualPATHDependency(ManualDependency):
    """A manually installed dependency that resides in the PATH.

    This is a minor extension of ``ManualDependency`` which adds additional
    functionality to check if target dependency has been installed and
    resides in the PATH.

    Note:
        ``name`` must match the target binary to find in the PATH or this will
        not work.
    """

    def installed(self):
        """Check the PATH for the existence of ``name``."""

        binary = find(self.name)
        return binary is not None


class ManualWindowsRegistryDependency(ManualDependency):
    """A manually installed dependency that sets a Windows registry key.

    This checks for the existence of a Windows registry key to verify the
    installation status of a dependency.

    Args:
        name (str): The name of this dependency.
        help (str): A short description of how to install this dependency
            manually. Optional, but recommended.
        key (str): The full path to the key to check.
    """

    def __init__(self, *args, registry, key, **kwargs):
        if os.name != "nt":
            raise exceptions.ConfigurationError(
                "unsupported platform for this dependency type: {}".format(os.name)
            )

        super().__init__(*args, **kwargs)

        self.registry = registry
        self.key = key

    def installed(self):
        """Check the registry for the existence of ``key``.

        This uses the built-in ``winreg`` API to check for the existence of the
        key.
        """

        import winreg

        try:
            registry = winreg.ConnectRegistry(None, self.registry)
        except TypeError:
            raise exceptions.ConfigurationError(
                "{} is not a valid regitry - constants from `winreg` should be used (e.g., `winreg.HKEY_LOCAL_MACHINE`)".format(
                    self.registry
                )
            )

        try:
            winreg.OpenKey(registry, self.key)
        except FileNotFoundError:
            return False

        return True


class WindowsChocolateyDependency(Dependency):
    """A dependency that may be installed via the Chocolatey package manager.

    Args:
        package (str): The package name.

    Note:
        These sorts of dependencies require that the plaform under which this
        Blueprint/Component/Transform is run includes Chocolatey and assume
        that it is already installed (i.e., this will not work on Linux).

    Note:
        These dependencies require Administrator permissions to install
        successfully.
    """

    def __init__(self, package):
        if os.name != "nt":
            raise exceptions.ConfigurationError(
                "unsupported platform for this dependency type: {}".format(os.name)
            )

        self.package = package

    def install(self, verbose=False):
        """Install the package with Chocolatey."""

        choco = find("choco")

        if not choco:
            raise exceptions.MissingDependency(
                "Chocolatey is not installed on this platform"
            )

        run(
            "{} install -y {}".format(choco, self.package),
            ".",
            exceptions.DependencyInstallationFailure(
                "failed to install {}".format(self.package)
            ),
            propagate=verbose,
        )

    def installed(self):
        """Check if the package is installed with Chocolately."""

        choco = find("choco")

        if not choco:
            raise exceptions.MissingDependency(
                "Chocolatey is not installed on this platform"
            )

        output, _ = run(
            "{} list -l -e {}".format(choco, self.package),
            ".",
        )

        output = output.decode("utf-8")

        return "1 packages installed" in output and self.package in output

    def string(self):
        return self.package


class LinuxAPTDependency(Dependency):
    """A dependency that may be installed via the Advanced Package Tool (APT).

    Args:
        package (str): The package name.

    Note:
        These sorts of dependencies require that the plaform under which this
        Blueprint/Component/Transform is run includes APT and assume that it is
        already installed (i.e., this will not work on Windows).

    Note:
        These dependencies require root permissions to install successfully.
    """

    def __init__(self, package):
        if os.name != "posix":
            raise exceptions.ConfigurationError(
                "unsupported platform for this dependency type: {}".format(os.name)
            )

        self.package = package

    def install(self, verbose=False):
        """Install the package with APT."""

        apt = find("apt")

        if not apt:
            raise exceptions.MissingDependency("APT is not installed on this platform")

        def command(cmd, sudo=False, error=None):
            sudo = "sudo" if sudo else ""

            run(
                "{} {} {}".format(sudo, apt, cmd),
                ".",
                error,
                propagate=verbose,
            )

        sudo = False
        permissions = exceptions.DependencyInstallationFailure(
            "`apt update` failed (hint: do you have permission to install packages?)"
        )

        try:
            command("update", sudo=sudo, error=permissions)
        except exceptions.DependencyInstallationFailure:
            if verbose:
                print("\nfailed to install: attempting to elevate\n")

            sudo = True
            command("update", sudo=sudo, error=permissions)

        command(
            "install -y {}".format(self.package),
            sudo=sudo,
            error=exceptions.DependencyInstallationFailure(
                "failed to install {}".format(self.package)
            ),
        )

    def installed(self):
        """Check if the package is installed with dpkg."""

        dpkg = find("dpkg")

        if not dpkg:
            raise exceptions.MissingDependency("dpkg is not installed on this platform")

        try:
            run(
                "{} -s {}".format(dpkg, self.package),
                ".",
            )
        except subprocess.CalledProcessError:
            return False

        return True

    def string(self):
        return self.package


class ScriptDependency(Dependency):
    """A dependency that can be run as a script on the local system.

    This allows including dependency installation scripts alongside your
    code. This is not a final class - the ``installed`` method remains abstract
    so this must be subclassed with an implementation for that method in order
    to be used.

    Args:
        path (str): The path to the script to run.
        relative (str): A module for relative to which the ``path`` exists.

    Note:
        These dependencys are agnostic of the operating system that they are
        run on - if you want to support multiple operating systems, add a
        conditional to the class definition.

    Note:
        This (and its descendents) are not unit tested - in most cases this is
        likely not the best way to implement dependency checking/installation
        and should only be used as a last resort. Developing a more
        specific (while still reusable) ``Dependency`` subclass is likely a
        better approach.
    """

    def __init__(self, path, relative=None):
        if relative:
            self.path = pkg_resources.resource_filename(relative, path)
        else:
            self.path = os.path.abspath(path)

    def install(self, verbose=False):
        """Install by running the script."""

        if verbose:
            print(
                "---------------------------------- Installing ----------------------------------"
            )

        exception = None
        try:
            run(
                self.path,
                ".",
                exceptions.DependencyInstallationFailure(
                    "dependency installation failed"
                ),
                propagate=verbose,
            )
        except Exception as e:
            exception = e

        if verbose:
            print("-" * 80)

        if exception:
            raise exception

    def string(self):
        return self.path


class ScriptPATHDependency(ScriptDependency):
    """A script-installed dependency that resides in the PATH.

    Args:
        path (str): The relative path to the script to run.
        names (list): A list of binaries in the PATH that should be installed
            by this script.

    This is a minor extension of ``ScriptDependency`` which adds additional
    functionality to check if target dependency has been installed and
    resides in the PATH.
    """

    def __init__(self, *args, names=None, **kwargs):
        super().__init__(*args, **kwargs)

        if names:
            self.names = names

    def installed(self):
        """Check the PATH for the existence of each ``name`` in ``names``."""

        status = True

        for name in self.names:
            binary = find(name)
            status = status and binary is not None

        return status


class Dependable(object, metaclass=abc.ABCMeta):
    """A class interface for introducing dependencies."""

    dependencies = []

    """A list of external dependencies which must be installed.

    This list is optional, but must consist of zero or more instances of
    ``Dependency`` (or subclasses) which may be installed by users.
    """

    @classmethod
    def install(cls, verbose=False):
        """Install all dependencies.

        This reruns dependency installation regardless of if it has been
        installed already. This should be safe because of the requirement that
        dependency installation methods be repeatable but can be inefficient.
        Users can check the ``installed()`` method to determine if the
        installation should be rerun.

        Args:
            verbose (bool): Verbosity.
        """

        for dependency in cls.dependencies:
            dependency.install(verbose=verbose)

    @classmethod
    def installed(cls):
        """Check if all dependencies have been installed.

        Returns:
            ``True`` if all dependencies have been installed already, and
            ``False`` otherwise.
        """

        status = True

        for dependency in cls.dependencies:
            status &= dependency.installed()

        return status

    def __init__(self, *args, **kwargs):
        """Check that dependencies have been installed.

        Throws an error if dependencies have not been installed.
        """
        super().__init__(*args, **kwargs)

        if not self.installed():
            raise exceptions.NotInstalled(
                "dependencies have not been installed for {} (hint: use the `install` command to install them)".format(
                    self.__class__.__name__
                )
            )


def source(package, resource):
    """Fetch the content of a specific file in this package.

    Args:
        package (str): The package path relative to which the resource exists.
            In most cases you probably want to supply ``__name__`` to search
            relative to the current code.
        resource (str): The resource filename to load.

    Returns:
        The content of the package resource as a string.
    """

    filename = pkg_resources.resource_filename(package, resource)

    with open(filename, "r") as f:
        content = f.read()

    return content


def substitute(template, safe=True, **kwargs):
    """Substitute parameters in a template string.

    Template substitution makes use of Python string templates (described in
    `PEP 292 <https://www.python.org/dev/peps/pep-0292/>`_).

    Args:
        template (str): The template string.
        safe (bool): If ``True``, missing parameters will be ignored and some
            template parameters may remain in the return value.
        **kwargs: Template parameters.

    Returns:
        The substituted template string.
    """

    template = string.Template(template)

    if safe:
        # Raise errors on invalid template even when ``safe == True``.
        try:
            template.substitute()
        except KeyError:
            pass

        return template.safe_substitute(kwargs)
    else:
        return template.substitute(kwargs)


def find(name, environment=None, guess=None):
    """Finds a particular binary on this system.

    Attempts to find the binary given by ``name``, first checking the value of
    the environment variable named ``environment`` (if provided), then by
    checking the system path, then finally checking hardcoded paths in
    ``guess`` (if provided). This function is cross-platform compatible - it
    works on Windows, Linux, and Mac. If there are spaces in the path found,
    this function will wrap its return value in double quotes.

    Args:
        name (str): Binary name.
        environment (str): An optional environment variable to check.
        guess (iterable): An optional list of hardcoded paths to check.

    Returns:
        A string with the absolute path to the binary if found, otherwise
        ``None``.
    """

    def sanitize(path):
        quotes = ("'", "'")
        if " " in path and path[0] not in quotes and path[-1] not in quotes:
            path = '"{}"'.format(path)

        return path

    if environment:
        path = os.environ.get(environment)
        if path is not None:
            path = os.path.abspath(os.path.expanduser(path))
            if os.path.isfile(path):
                return sanitize(path)

    if os.name == "posix":
        search = "which"
    elif os.name == "nt":
        search = "where.exe"
    else:
        raise EnvironmentError("unknown platform: {}".format(os.name))

    try:
        with open(os.devnull, "w") as output:
            path = subprocess.check_output([search, name], stderr=output).decode(
                "utf-8"
            )

        return sanitize(os.path.abspath(path.strip()))
    except subprocess.CalledProcessError:
        pass

    if guess:
        for path in guess:
            if os.path.isfile(path):
                return sanitize(path)

    return None


def run(cmd, cwd=None, exception=None, propagate=False, stdout=None, stderr=None):
    """Run the given command as a subprocess.

    This function caputres ``stdout`` and ``stderr`` by default and returns
    them, and raises the given exception if the process fails.

    Args:
        cmd (str): The command to run.
        cwd (str): The working directory in which to run the command.
        exception: An exception to raise if the command fails.
        propagate (bool): If ``True``, command output will be written to stdout
            and stderr of the current process, otherwise command output is
            captured and returned (and written to ``stdout`` and ``stderr`` if
            provided). Default: ``False``.
        stdout (file): An open file-like object or fileno where stdout should
            be written or ``None``.
        stderr (file): An open file-like object or fileno where stderr should
            be written or ``None``.

    Returns:
        Output to stdout and stderr as binary strings.

    Note:
        Without adding sufficient complexity (additional threads) output cannot
        be both captured and printed stdout/stderr of the current process in
        real time. If this is called with ``propagate=True``, then no output
        will be returned or written to the provided ``stdout``/``stderr``
        arguments.
    """

    cwd = cwd or os.path.abspath(".")

    process = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        stdout=None if propagate else subprocess.PIPE,
        stderr=None if propagate else subprocess.PIPE,
    )

    if stdout and process.stdout:
        stdout.write(process.stdout)
        stdout.flush()
    if stderr and process.stderr:
        stderr.write(process.stderr)
        stderr.flush()

    if process.returncode != 0:
        if exception:
            raise exception
        raise subprocess.CalledProcessError(cmd=cmd, returncode=process.returncode)

    return process.stdout, process.stderr


def parse(specification):
    """Parse optional configuration values.

    This function parses the given ``specification`` value into a name and
    a dictionary of key/value configuration pairs if specified.

    Args:
        specification (str): The specification to parse.

    Returns:
        A tuple of the parse name and configuration if provided, otherwise
        ``None``.

    Example:
        The following configuration specification::

        configuration-example:first=something,second="another thing"

        Will be parsed as::

        (
            'configuration-example',
            {
                'first': 'something',
                'second': 'another thing'
            }
        )
    """

    result = specification.split(":", 1)

    if len(result) == 1:
        return {"name": result[0], "configuration": {}}

    name, configuration = result

    name = name.strip('"')

    configuration = dict(re.findall(r'([^,]+)=(["\'].*?["\']|[^,]+)', configuration))
    configuration = {k: v.strip("\"'") for k, v in configuration.items()}

    return {"name": name, "configuration": configuration}


def load(entrypoint, name=None):
    """Loads part(s) of helix from a given entrypoint.

    Args:
        entrypoint (str): The entrypoint namespace to load.
        name (str): Optional entrypoint name for exact match.

    Returns:
        A list of classes exposed in the entrypoint namespace ``entrypoint``
        or, if ``name`` is provided, a single class matching ``name``.
    """

    entrypoints = pkg_resources.iter_entry_points(entrypoint, name)

    classes = []
    for e in entrypoints:
        try:
            classes.append(e.load())
        # ignore entrypoints with missing, optional dependencies
        except pkg_resources.DistributionNotFound:
            pass

    if not classes:
        raise exceptions.EntrypointNotFound(
            "could not find a matching entrypoint in namespace {}{}".format(
                entrypoint, ": {}".format(name) if name else ""
            )
        )

    if name:
        return classes[0]

    return classes
