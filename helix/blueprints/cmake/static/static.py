from .. import cmake


class StaticCMakeBlueprint(cmake.CMakeBlueprint):
    """A statically linked CMake Blueprint."""

    version = "1.0.0"

    @property
    def libraries(self):
        libraries = super().libraries

        lines = []
        for name in libraries:
            lines.append("find_static_library({} {})".format(name, name.upper()))

        lines.append(
            "target_link_libraries({} {})".format(
                self.build_name,
                " ".join("${{{}}}".format(library.upper()) for library in libraries),
            )
        )

        return ["\n".join(lines)]


class StaticCMakeCBlueprint(StaticCMakeBlueprint):
    name = "static-cmake-c"
    verbose_name = "Static CMake C Project"
    description = "A statically linked CMake C Blueprint"
    type = "c"


class StaticCMakeCppBlueprint(StaticCMakeBlueprint):
    name = "static-cmake-cpp"
    verbose_name = "Static CMake C++ Project"
    description = "A statically linked CMake C++ Blueprint"
    type = "cpp"


__all__ = [
    "StaticCMakeCBlueprint",
    "StaticCMakeCppBlueprint",
]
