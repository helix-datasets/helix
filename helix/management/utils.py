"""Common command utilities.

Like an abstract base class for commands note: this is a rough implementation
of Django's custom management commands:
https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/
"""

import abc
import sys
import enum
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


class Style(enum.Enum):
    """Terminal style storage Enum."""

    none = ""

    bold = "\033[1m"
    dim = "\033[2m"


class Color(enum.Enum):
    """Terminal color storage Enum."""

    none = ""

    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    blue = "\033[94m"
    pink = "\033[95m"
    cyan = "\033[96m"
    white = "\033[97m"


END = "\033[0m"


def format(message, style=None, color=None):
    """Format a message with terminal colors.

    This is intelligent enough to not apply color formatting when the output
    file descriptor would not support it.

    Args:
        message (str): A string message to format.
        style (str): The sttyle to print - select from the Style Enum.
            Optional.
        color (str): The color to print - select from the Color Enum. Optional.

    Returns:
        A formatted message in the given color. You can pass this directly to
        ``print``.
    """

    if not sys.stdout.isatty():
        return message

    if style is None:
        style = Style.none
    elif not isinstance(style, Style):
        raise ValueError("unknown style: {}".format(style))

    if color is None:
        color = Color.none
    elif not isinstance(color, Color):
        raise ValueError("unknown color: {}".format(color))

    return "{}{}{}{}".format(style.value, color.value, message, END)


_print = print


def print(*args, style=None, color=None, **kwargs):
    """An augmented version of print that supports terminal colors.

    All args/kwargs to the default python ``print()`` function are supported.

    Arguments:
        color(str): The color to apply.
        style(str): The style to apply.
    """

    modified = []

    for arg in args:
        modified.append(format(arg, color=color, style=style))

    _print(*modified, **kwargs)


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
