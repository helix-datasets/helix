import os
import abc

from ... import blueprint
from ... import utils
from ... import exceptions


class CMakeBlueprint(blueprint.Blueprint, metaclass=abc.ABCMeta):
    """A simple CMake project Blueprint."""

    version = "1.0.0"

    if os.name == "posix":
        dependencies = [utils.LinuxAPTDependency("cmake")]
    elif os.name == "nt":
        import winreg

        dependencies = [
            utils.WindowsChocolateyDependency("cmake"),
            utils.WindowsChocolateyDependency("visualstudio2017-workload-vctools"),
        ]

    CALLSITE_MAIN = "main"
    """A callsite in the main function.

    Both ``argc`` and ``argv`` are available at this callsite and may be used
    in calls here. Return values are ignored.
    """

    callsites = [CALLSITE_MAIN]

    def _aggregate(self, key):
        """Aggregate a list of component properties of a given name.

        Args:
            key (str): The name of the property to be aggregated.

        Returns:
            A deduplicated list combining the named property for all Components
            of this Blueprint.
        """

        values = []

        for component in self.components:
            values += getattr(component, key, [])

        return list(set(values))

    @property
    def libraries(self):
        """Aggregate required libraries from included components.

        The ``libraries`` property may optionally be specified on Components
        that support this Blueprint in order to specify the names of installed
        system libraries to link against.
        """

        return self._aggregate("libraries")

    @property
    def include_directories(self):
        """Aggregate required include directories from included components.

        The ``include_directories`` property may optionally be specified on
        Components that support this Blueprint in order to specify paths to be
        added to the preprocessor search path.
        """

        return self._aggregate("include_directories")

    def generate(self, directory):
        """:meta private:"""

        functions = "\n".join(self.functions)
        main = self.calls.pop(self.CALLSITE_MAIN, [])
        main = "\n    ".join(main)

        try:
            source = utils.source(self.__class__.__module__, "main.c")
        except FileNotFoundError:
            source = utils.source(__name__, "main.c")

        source = utils.substitute(source, functions=functions, main=main)

        libraries = " ".join(self.libraries)
        include_directories = " ".join(self.include_directories)

        try:
            cmakelists = utils.source(self.__class__.__module__, "CMakeLists.txt")
        except FileNotFoundError:
            cmakelists = utils.source(__name__, "CMakeLists.txt")

        cmakelists = utils.substitute(
            cmakelists,
            name=self.build_name,
            include_directories=include_directories,
            extension=self.type,
            libraries=libraries,
        )

        sourcefile = os.path.join(directory, "main.{}".format(self.type))

        with open(sourcefile, "w") as f:
            f.write(source)

        with open(os.path.join(directory, "CMakeLists.txt"), "w") as f:
            f.write(cmakelists)

        return [sourcefile]

    def __binary(self, build_directory):
        """Find the built binary.

        Because CMake works transparently with a bunch of different compilers,
        we have to try a few possible locations for the final built binary.
        """

        locations = (
            os.path.join(build_directory, self.build_name),  # gcc
            os.path.join(
                build_directory, "Debug", "{}.exe".format(self.build_name)
            ),  # MSVC
        )

        for location in locations:
            if os.path.isfile(location):
                return location

        raise exceptions.BuildFailure(
            "unsupported compiler - could not find the final binary"
        )

    def compile(self, directory, options):
        """:meta private:"""

        cmake = utils.find("cmake")

        build_directory = os.path.join(directory, "build")

        if not os.path.exists(build_directory):
            os.makedirs(build_directory)

        cmd = "{} ..".format(cmake)
        utils.run(
            cmd,
            build_directory,
            exceptions.BuildFailure("cmake invocation failed"),
            propagate=options.get("propagate"),
            stdout=options.get("stdout"),
            stderr=options.get("stderr"),
        )

        cmd = "{} --build .".format(cmake)
        utils.run(
            cmd,
            build_directory,
            exceptions.BuildFailure("make invocation failed"),
            propagate=options.get("propagate"),
            stdout=options.get("stdout"),
            stderr=options.get("stderr"),
        )

        binary = self.__binary(build_directory)

        return [binary]


class CMakeCBlueprint(CMakeBlueprint):
    """A simple CMake C project Blueprint."""

    name = "cmake-c"
    verbose_name = "CMake C Project"
    description = "A simple CMake C project Blueprint"
    type = "c"

    CALLSITE_MAIN = "main"
    """A callsite in the main function.

    Both ``argc`` and ``argv`` are available at this callsite and may be used
    in calls here. Return values are ignored.
    """

    callsites = [CALLSITE_MAIN]


class CMakeCppBlueprint(CMakeBlueprint):
    """A simple CMake C++ project Blueprint."""

    name = "cmake-cpp"
    verbose_name = "CMake C++ Project"
    description = "A simple CMake C++ project Blueprint"
    type = "cpp"

    CALLSITE_MAIN = "main"
    """A callsite in the main function.

    Both ``argc`` and ``argv`` are available at this callsite and may be used
    in calls here. Return values are ignored.
    """

    callsites = [CALLSITE_MAIN]
