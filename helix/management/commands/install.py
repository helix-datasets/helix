import textwrap

from ... import utils
from ... import exceptions

from .. import utils as mutils


class Command(mutils.CommandBase):
    """Install external dependencies.

    .. code-block:: none

        usage: helix install [-h] [-c] [-f] [-v] {blueprints,components,transforms} ...

        positional arguments:
          {blueprints,components,transforms}
            blueprints          install dependencies for blueprints
            components          install dependencies for components
            transforms          install dependencies for transforms

        optional arguments:
          -h, --help            show this help message and exit
          -c, --check           check the installation status without installing anything
          -f, --fail-fast       stop installing if there are any failures
          -v, --verbose         verbose mode
    """

    name = "install"
    help = "install external dependencies"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="subcommand")

        def common(subparser):
            subparser.add_argument(
                "-c",
                "--check",
                default=False,
                action="store_true",
                help="check the installation status without installing anything",
            )
            subparser.add_argument(
                "-f",
                "--fail-fast",
                default=False,
                action="store_true",
                help="stop installing if there are any failures",
            )
            subparser.add_argument(
                "-v",
                "--verbose",
                default=False,
                action="store_true",
                help="verbose mode",
            )

        def category(subparser, name):
            subparser.add_argument(
                "names",
                metavar="name",
                type=str,
                help="{}(s) for which to install dependencies".format(name),
                nargs="*",
                default=None,
            )

        common(parser)

        blueprint_parser = subparsers.add_parser(
            "blueprints", help="install dependencies for blueprints"
        )
        category(blueprint_parser, "blueprint")
        common(blueprint_parser)

        component_parser = subparsers.add_parser(
            "components", help="install dependencies for components"
        )
        category(component_parser, "component")
        common(component_parser)

        transform_parser = subparsers.add_parser(
            "transforms", help="install dependencies for transforms"
        )
        category(transform_parser, "transform")
        common(transform_parser)

    def handle(self, *args, **options):
        fast = options.get("fail_fast")
        verbose = options.get("verbose")
        part = options.get("subcommand")
        names = options.get("names")

        if part is None:
            parts = ["blueprints", "components", "transforms"]
        else:
            parts = [part]

        for part in parts:
            try:
                if names:
                    classes = []
                    for name in names:
                        classes.append(utils.load("helix.{}".format(part), name))
                else:
                    classes = utils.load("helix.{}".format(part))
            except exceptions.EntrypointNotFound as e:
                mutils.print(e, color=mutils.Color.red)
                exit(1)

            classes = sorted(classes, key=lambda c: c.name)

            failed = False

            for c in classes:
                mutils.print(c.string(), style=mutils.Style.bold)

                if c.dependencies:
                    if c.installed():
                        mutils.print("  already installed", color=mutils.Color.green)

                        continue

                    if options.get("check"):
                        mutils.print("  not installed", color=mutils.Color.yellow)

                        failed = True
                        if fast:
                            break

                        continue

                    if verbose:
                        print("-" * 80)

                    try:
                        c.install(verbose=verbose)
                    except exceptions.DependencyInstallationFailure as e:
                        if verbose:
                            print("-" * 80)

                        mutils.print("  {}".format(e), color=mutils.Color.red)

                        if e.help:
                            help = textwrap.wrap(
                                e.help, initial_indent="  ", subsequent_indent="  "
                            )
                            mutils.print("\n".join(help), color=mutils.Color.yellow)

                        failed = True
                        if fast:
                            break
                    else:
                        if verbose:
                            print("-" * 80)

                        mutils.print(
                            "  installed successfully", color=mutils.Color.green
                        )
                else:
                    mutils.print("  no dependencies found", style=mutils.Style.dim)

        if failed:
            exit(1)
