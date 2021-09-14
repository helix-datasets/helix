"""Common command utilities.

Like an abstract base class for commands note: this is a rough implementation
of Django's custom management commands:
https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/
"""

import abc
import pkgutil

from . import exceptions


def confirm(message=None):
    if message is not None:
        print(message)
    try:
        response = input("Do you want to continue? [y/N] ")
    except KeyboardInterrupt:
        return False

    response = response.lower()

    if response not in ("y", "yes"):
        return False

    return True


COLOR_BOLD = "\033[1m"
COLOR_DIM = "\033[2m"
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_PINK = "\033[95m"
COLOR_CYAN = "\033[96m"
COLOR_WHITE = "\033[97m"
COLOR_END = "\033[0m"


def color(message, color=None):
    """Format a message with terminal colors.

    Args:
        message (str): A string message to format.
        color (str): The color to print - select from COLOR_* constants in this
            module. If this is not provided, this function does nothing.

    Returns:
        A formatted message in the given color. You can pass this directoy to
        ``print``.
    """

    if color is None:
        return message

    return "{}{}{}".format(color, message, COLOR_END)


class CommandBase(object, metaclass=abc.ABCMeta):
    """A common base class for custom module call commands."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def name(self):
        """The name of this command."""

        return

    @abc.abstractproperty
    def help(self):
        """Help content."""

        return

    def add_arguments(self, parser):
        """Add arguments to this command."""

        return

    @abc.abstractmethod
    def handle(self, *args, **options):
        """Execute the command.

        Parsed arguments will be available in the options kwarg dict.
        """

        return

    def execute(self, args):
        """Internal execute method."""

        options = {k: v for (k, v) in vars(args).items() if v is not None}

        try:
            self.handle(**options)
        except exceptions.CommandError as e:
            print(e)
            exit(1)


def build_parser(parser, module):
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    for _, modname, _ in pkgutil.iter_modules(module.__path__, module.__name__ + "."):
        command_module = __import__(modname, fromlist="dummy")

        try:
            command = command_module.Command()
        except AttributeError:
            continue

        command_parser = subparsers.add_parser(command.name, help=command.help)
        command.add_arguments(command_parser)
        command_parser.set_defaults(func=command.execute)
