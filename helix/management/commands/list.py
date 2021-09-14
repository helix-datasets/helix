from ... import utils
from .. import utils as management_utils


class Command(management_utils.CommandBase):
    """List components and transforms.

    .. code-block:: none

        usage: helix list [-h] [-v]

        optional arguments:
          -h, --help     show this help message and exit
          -v, --verbose  verbose output
    """

    name = "list"
    help = "list components and transforms"

    def add_arguments(self, parser):
        parser.add_argument(
            "-v", "--verbose", help="verbose output", action="store_true", default=False
        )

    def __list_entrypoint(self, entrypoint, verbose_entrypoint_name, verbose=False):
        classes = utils.load(entrypoint)
        classes = sorted(classes, key=lambda c: c.name)

        print(
            management_utils.color(
                "Available {}:".format(verbose_entrypoint_name),
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

    def handle(self, *args, **options):
        self.__list_entrypoint(
            "helix.blueprints", "Blueprints", verbose=options["verbose"]
        )
        self.__list_entrypoint(
            "helix.components", "Components", verbose=options["verbose"]
        )
        self.__list_entrypoint(
            "helix.transforms", "Transforms", verbose=options["verbose"]
        )
