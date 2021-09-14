"""Module call handler."""

import argparse

from . import management

from . import __title__
from . import __description__


def main():
    parser = argparse.ArgumentParser(
        description="{}: {}".format(__title__, __description__)
    )

    management.build_parser(parser, management.commands)

    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
