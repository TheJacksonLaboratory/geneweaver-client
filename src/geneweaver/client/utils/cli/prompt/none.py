"""Utility functions for prompting when allowing None values."""
from typing import Any

NONE_REPRS = ["--", "NONE"]


def value_represents_none(value: Any) -> bool:  # noqa: ANN401
    """Check if the value represents None.

    A value is considered to represent None if the upper case version of its string
    representation is in the NONE_REPRS list.

    :param value: The value to check.
    :return: True if the value represents None, False otherwise.
    """
    try:
        return str(value).upper() in NONE_REPRS
    except (TypeError, AttributeError):
        return False


def allow_none_str() -> str:
    """Format the string prompt when a field allows None values.

    :return: A string describing the allowed None values.
    """
    return f" (or {'/'.join(NONE_REPRS)} to leave blank)"
