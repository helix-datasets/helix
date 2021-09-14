"""Custom command exceptions."""


class CommandError(Exception):
    """An expected command error.

    Handled by printing the error message to the console rather than giving a
    full stacktrace.
    """
