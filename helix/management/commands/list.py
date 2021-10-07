import textwrap

from ... import utils
from ... import exceptions

from .. import utils as management_utils


class Command(management_utils.CommandBase):
    """Print details about blueprints, components, and transforms.

    .. code-block:: none

                usage: helix list [-h] [-s SEARCH] [-d] [-y] [-t] [-c] [-r] [-v] [-vv] [-vvv] {blueprints,components,transforms} ...

                positional arguments:
                  {blueprints,components,transforms}
                        blueprints          list blueprints
                        components          list components
                        transforms          list transforms

                optional arguments:
                  -h, --help            show this help message and exit
                  -s SEARCH, --search SEARCH
                                                                search with a given string
                  -d, --description     include description
                  -y, --type            include type
                  -t, --tags            include tags
                  -c, --configuration   include configuration parameters
                  -r, --dependencies    include dependencies
                  -v, --verbose         include description and tags
                  -vv, --very-verbose   verbose plus configuration
                  -vvv, --very-very-verbose
                                                                very verbose plus type and dependencies
    """

    name = "list"
    help = "print details about blueprints, components, and transforms"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="subcommand")

        def common(subparser):
            subparser.add_argument("-s", "--search", help="search with a given string")

            subparser.add_argument(
                "-d",
                "--description",
                default=False,
                action="store_true",
                help="include description",
            )
            subparser.add_argument(
                "-y",
                "--type",
                default=False,
                action="store_true",
                help="include type",
            )
            subparser.add_argument(
                "-t",
                "--tags",
                default=False,
                action="store_true",
                help="include tags",
            )
            subparser.add_argument(
                "-c",
                "--configuration",
                default=False,
                action="store_true",
                help="include configuration parameters",
            )
            subparser.add_argument(
                "-r",
                "--dependencies",
                default=False,
                action="store_true",
                help="include dependencies",
            )

            subparser.add_argument(
                "-v",
                "--verbose",
                default=False,
                action="store_true",
                help="include description and tags",
            )
            subparser.add_argument(
                "-vv",
                "--very-verbose",
                default=False,
                action="store_true",
                help="verbose plus configuration",
            )
            subparser.add_argument(
                "-vvv",
                "--very-very-verbose",
                default=False,
                action="store_true",
                help="very verbose plus type and dependencies",
            )

        def category(subparser, name):
            subparser.add_argument(
                "names",
                metavar="name",
                type=str,
                help="{}(s) to list".format(name),
                nargs="*",
                default=None,
            )

        common(parser)

        blueprint_parser = subparsers.add_parser("blueprints", help="list blueprints")
        category(blueprint_parser, "blueprint")
        common(blueprint_parser)

        component_parser = subparsers.add_parser("components", help="list components")
        category(component_parser, "component")
        common(component_parser)

        transform_parser = subparsers.add_parser("transforms", help="list transforms")
        category(transform_parser, "transform")
        common(transform_parser)

    def __list_entrypoint(self, entrypoint, verbose_entrypoint_name, verbose=False):
        classes = utils.load(entrypoint)
        classes = sorted(classes, key=lambda c: c.name)

        print(
            management_utils.color(
                "{}:".format(verbose_entrypoint_name),
                management_utils.COLOR_BOLD,
            )
        )

        for c in classes:
            print("  {}".format(c.string()))

            if verbose:
                print(
                    management_utils.color(
                        "    Type: {}".format(c.type), management_utils.COLOR_DIM
                    )
                )
                print(
                    management_utils.color(
                        "    Description: {}".format(c.description),
                        management_utils.COLOR_DIM,
                    )
                )

        if not classes:
            print("  None")

    @staticmethod
    def search(classes, search):
        """Filter classes by some search parameter.

        Arguments:
            classes (list): A list of classes to filter.
            search (str): A string search parameter.

        Returns:
            A truncated list of classes that match the search parameter.
        """

        search = search.lower()

        results = []
        for c in classes:
            match = False

            match |= search in c.name
            match |= search in c.description
            match |= search in c.type

            if hasattr(c, "blueprints"):
                match |= search in " ".join(c.blueprints)

            if hasattr(c, "tags") and isinstance(c.tags, (tuple, list)):
                match |= search in " ".join(["{}:{}".format(k, v) for k, v in c.tags])

            match |= search in " ".join(
                ["{}".format(d.string()) for d in c.dependencies]
            )

            if match:
                results.append(c)

        return results

    def handle(self, *args, **options):
        part = options.get("subcommand")
        names = options.get("names")
        search = options.get("search")
        vvverbose = options.get("very_very_verbose")
        vverbose = options.get("very_verbose") or vvverbose
        verbose = options.get("verbose") or vverbose

        if part is None:
            parts = ["blueprints", "components", "transforms"]
        else:
            parts = [part]

        for part in parts:
            print("{}:".format(part.title()))

            try:
                if names:
                    classes = []
                    for name in names:
                        classes.append(utils.load("helix.{}".format(part), name))
                else:
                    classes = utils.load("helix.{}".format(part))
            except exceptions.EntrypointNotFound as e:
                print(management_utils.color(e, management_utils.COLOR_RED))
                exit(1)

            if search:
                classes = self.search(classes, search)

            classes = sorted(classes, key=lambda c: c.name)

            for c in classes:

                print(
                    management_utils.color(
                        "  {}".format(c.string()), management_utils.COLOR_BOLD
                    )
                )

                if options.get("description") or verbose:
                    print(
                        "    Description: {}".format(
                            management_utils.color(
                                c.description,
                                management_utils.COLOR_DIM,
                            )
                        )
                    )

                if options.get("type") or vvverbose:
                    print(
                        "    Type: {}".format(
                            management_utils.color(c.type, management_utils.COLOR_DIM)
                        )
                    )

                    if hasattr(c, "blueprints"):
                        print(
                            "    Blueprints: {}".format(
                                management_utils.color(
                                    ", ".join(c.blueprints), management_utils.COLOR_DIM
                                )
                            )
                        )

                if options.get("tags") or verbose:
                    if isinstance(c.tags, (tuple, list)):
                        output = "Tags:"

                        for key, value in sorted(c.tags, key=lambda t: t[0]):
                            output += management_utils.color(
                                " ({}:{})".format(key, value),
                                management_utils.COLOR_DIM,
                            )

                        output = textwrap.wrap(
                            output,
                            initial_indent="    ",
                            subsequent_indent="      ",
                            break_on_hyphens=False,
                        )

                        for line in output:
                            print(line)

                if options.get("configuration") or vverbose:
                    if hasattr(c, "options") and c.options:
                        output = "    Configuration Parameters: "

                        parameters = []
                        for option, settings in c.options.items():
                            parameters.append(
                                "{}{}".format(
                                    option,
                                    " (default: {})".format(settings["default"])
                                    if "default" in settings
                                    else "",
                                )
                            )

                        output += management_utils.color(
                            ", ".join(parameters), management_utils.COLOR_DIM
                        )

                        print(output)

                if options.get("dependencies") or vvverbose:
                    if hasattr(c, "dependencies") and c.dependencies:
                        output = "Dependencies: "

                        deps = []
                        for dependency in c.dependencies:
                            deps.append(dependency.string())

                        output += management_utils.color(
                            ", ".join(deps), management_utils.COLOR_DIM
                        )

                        output = textwrap.wrap(
                            output,
                            initial_indent="    ",
                            subsequent_indent="      ",
                            break_on_hyphens=False,
                        )

                        for line in output:
                            print(line)

            if not classes:
                print("  None")
