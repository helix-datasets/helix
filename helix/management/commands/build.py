import os
import json

from ... import build
from ... import utils
from ... import exceptions

from .. import utils as mutils


class Command(mutils.CommandBase):
    """Build a blueprint with a set of components and transforms.

    .. code-block:: none

        usage: helix build [-h] {blueprint,json} ...

        positional arguments:
          {blueprint,json}
            blueprint       manually specify blueprint, components, and transforms
            json            build from a json configuration file

        optional arguments:
          -h, --help        show this help message and exit
    """

    name = "build"
    help = "build a blueprint with a set of components and transforms"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="subcommand")
        subparsers.required = True

        blueprint_parser = subparsers.add_parser(
            "blueprint", help="manually specify blueprint, components, and transforms"
        )
        blueprint_parser.add_argument("blueprint", help="blueprint (by name)")
        blueprint_parser.add_argument(
            "-c", "--components", help="component(s) (by name)", nargs="*", default=[]
        )
        blueprint_parser.add_argument(
            "-t", "--transforms", help="transform(s) (by name)", nargs="*", default=[]
        )
        blueprint_parser.add_argument("output", help="output file or directory")
        blueprint_parser.add_argument(
            "-v",
            "--verbose",
            help="build in verbose mode",
            action="store_true",
            default=False,
        )

        json_parser = subparsers.add_parser(
            "json", help="build from a json configuration file"
        )
        json_parser.add_argument("input", help="input json file")
        json_parser.add_argument("output", help="output file or directory")
        json_parser.add_argument(
            "-v",
            "--verbose",
            help="build in verbose mode",
            action="store_true",
            default=False,
        )

    def handle(self, *args, **options):
        if options["subcommand"] == "blueprint":
            configuration = {
                "name": os.path.basename(options["output"]),
                "blueprint": {"name": options["blueprint"]},
            }

            configuration["components"] = [
                utils.parse(c) for c in options["components"]
            ]
            configuration["transforms"] = [
                utils.parse(t) for t in options["transforms"]
            ]
        elif options["subcommand"] == "json":
            with open(options["input"], "r") as f:
                configuration = json.load(f)
        else:
            raise Exception("unknown command: {}".format(options["subcommand"]))

        try:
            artifacts, tags = build.build(
                configuration,
                options["output"],
                options={"propagate": options["verbose"]},
            )
        except (
            exceptions.ConfigurationError,
            exceptions.EntrypointNotFound,
            exceptions.BlueprintNotSane,
            exceptions.NotInstalled,
            exceptions.MissingDependency,
            exceptions.BuildFailure,
        ) as e:
            mutils.print(e, color=mutils.Color.red)
            exit(1)

        print("Tags: ")
        for tag in tags:
            print("  {}".format(tag))

        print("Artifacts: ")
        for artifact in artifacts:
            print("  {}".format(artifact))
