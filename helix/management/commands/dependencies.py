import textwrap

from ... import utils
from ... import exceptions

from .. import utils as management_utils


class Command(management_utils.CommandBase):
    """Install external dependencies.

    .. code-block:: none

        usage: helix dependencies [-h] {blueprint,component,transform,all} ...

        positional arguments:
          {blueprint,component,transform,all}
            blueprint           install blueprint dependencies
            component           install component dependencies
            transform           install transform dependencies
            all                 install all dependencies

        optional arguments:
          -h, --help            show this help message and exit
    """

    name = "dependencies"
    help = "install external dependencies"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="subcommand")
        subparsers.required = True

        blueprint_parser = subparsers.add_parser(
            "blueprint", help="install blueprint dependencies"
        )
        blueprint_parser.add_argument(
            "name",
            type=str,
            help="name to install dependencies for",
            nargs="?",
            default=None,
        )
        blueprint_parser.add_argument(
            "-v", "--verbose", default=False, action="store_true", help="verbose mode"
        )

        component_parser = subparsers.add_parser(
            "component", help="install component dependencies"
        )
        component_parser.add_argument(
            "name",
            type=str,
            help="name to install dependencies for",
            nargs="?",
            default=None,
        )
        component_parser.add_argument(
            "-v", "--verbose", default=False, action="store_true", help="verbose mode"
        )

        transform_parser = subparsers.add_parser(
            "transform", help="install transform dependencies"
        )
        transform_parser.add_argument(
            "name",
            type=str,
            help="name to install dependencies for",
            nargs="?",
            default=None,
        )
        transform_parser.add_argument(
            "-v", "--verbose", default=False, action="store_true", help="verbose mode"
        )

        all_parser = subparsers.add_parser("all", help="install all dependencies")
        all_parser.add_argument(
            "-v", "--verbose", default=False, action="store_true", help="verbose mode"
        )

    def handle(self, *args, **options):
        part = options.get("subcommand")
        name = options.get("name")

        if part == "all":
            parts = ["blueprint", "component", "transform"]
        else:
            parts = [part]

        for part in parts:
            try:
                classes = utils.load("helix.{}s".format(part), name)
            except exceptions.EntrypointNotFound as e:
                print(management_utils.color(e, management_utils.COLOR_RED))
                exit(1)

            if name is not None:
                classes = [classes]
            else:
                classes = sorted(classes, key=lambda c: c.name)

            for c in classes:
                print(c.string())

                if c.dependencies:
                    if c.installed():
                        print(
                            management_utils.color(
                                "  already installed", management_utils.COLOR_GREEN
                            )
                        )

                        continue

                    try:
                        c.install(verbose=options.get("verbose"))
                    except exceptions.DependencyInstallationFailure as e:
                        print(
                            management_utils.color(
                                "  {}".format(e), management_utils.COLOR_RED
                            )
                        )

                        if e.help:
                            help = textwrap.wrap(
                                e.help, initial_indent="  ", subsequent_indent="  "
                            )
                            print(
                                management_utils.color(
                                    "\n".join(help), management_utils.COLOR_YELLOW
                                )
                            )
                        continue

                    print(
                        management_utils.color(
                            "  installed successfully", management_utils.COLOR_GREEN
                        )
                    )
                else:
                    print("  no dependencies found")
