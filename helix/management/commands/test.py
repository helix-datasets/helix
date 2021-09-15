import unittest

from ... import utils
from ... import tests
from ... import exceptions

from .. import utils as management_utils


class Command(management_utils.CommandBase):
    """Run tests.

    .. code-block:: none

        usage: helix test [-h] {unit,system,integration} ...

        positional arguments:
          {unit,system,integration}
            unit                unit tests for blueprints, components, or transforms
            system              unit tests for core helix functionality
            integration         integration tests for combinations of blueprints,
                                components, and transforms

        optional arguments:
          -h, --help            show this help message and exit
    """

    name = "test"
    help = "run any of the supported test types"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="subcommand")
        subparsers.required = True

        unit_parser = subparsers.add_parser(
            "unit",
            help="unit tests for blueprints, components, or transforms",
        )

        system_parser = subparsers.add_parser(
            "system", help="unit tests for core helix functionality"
        )

        integration_parser = subparsers.add_parser(
            "integration",
            help="integration tests for combinations of blueprints, components, and transforms",
        )

        verbosity = {
            "type": int,
            "choices": {0, 1, 2},
            "default": 1,
            "help": "test verbosity level (default: 1)",
        }
        runner = {
            "type": str,
            "choices": {"text", "junit"},
            "default": "text",
            "help": "test runner (default: 'text')",
        }
        output = {
            "type": str,
            "default": ".",
            "help": "output directory - used by some runners (default: '.')",
        }

        unit_parser.add_argument(
            "unit",
            help="the name of a specific blueprint, component, or transform to test",
            nargs="?",
        )
        unit_parser.add_argument("-v", "--verbosity", **verbosity)
        unit_parser.add_argument("-r", "--runner", **runner)
        unit_parser.add_argument("-o", "--output", **output)

        system_parser.add_argument("-v", "--verbosity", **verbosity)
        system_parser.add_argument("-r", "--runner", **runner)
        system_parser.add_argument("-o", "--output", **output)

        integration_parser.add_argument("-v", "--verbosity", **verbosity)
        integration_parser.add_argument("-r", "--runner", **runner)
        integration_parser.add_argument("-o", "--output", **output)

    def handle(self, *args, **options):
        group = options.get("subcommand")

        if group == "unit":
            try:
                testcases = utils.load("helix.tests", options.get("testcase", None))
            except exceptions.EntrypointNotFound:
                testcases = []
        elif group == "system":
            testcases = tests.SYSTEM_TESTS
        elif group == "integration":
            testcases = tests.INTEGRATION_TESTS
        else:
            raise ValueError("invalid test type: {}".format(group))

        loader = unittest.TestLoader()
        testsuite = unittest.TestSuite(
            [loader.loadTestsFromTestCase(c) for c in testcases]
        )

        if options["runner"] == "text":
            runner = unittest.TextTestRunner(verbosity=options["verbosity"])
        elif options["runner"] == "junit":
            try:
                import xmlrunner
            except ImportError:
                print(
                    "xmlrunner is not installed (hint: did you install with testing extension enabled?)"
                )
                exit(1)

            runner = xmlrunner.XMLTestRunner(
                output=options["output"], verbosity=options["verbosity"]
            )

        result = runner.run(testsuite)

        if not result.wasSuccessful():
            exit(1)
