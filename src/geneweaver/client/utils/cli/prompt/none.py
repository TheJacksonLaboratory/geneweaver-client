"""Utility functions for prompting when allowing None values."""

from typing import Any, Optional, TypeVar

import typer

NONE_REPRS = ["--", "NONE"]

T = TypeVar("T")


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


def prompt_if_none(field_name: str, value: Optional[T] = None) -> Optional[T]:
    """Prompt the user to enter a value if the value is None.

    :param value: The value to check.
    :param field_name: The name of the field to prompt for.
    :return: The value entered by the user.
    """
    if value is None:
        value = typer.prompt(
            f"Please enter a value for {field_name.capitalize()}"
        ).strip()
    return value
