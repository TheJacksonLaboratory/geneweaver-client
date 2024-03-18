"""Utility functions for prompting boolean values."""

from typing import Optional, TypeVar

import typer

T = TypeVar("T")


def is_bool(field_type: T) -> bool:
    """Check if the field_type is a bool.

    :param field_type: The type to check.
    """
    return field_type is bool


def prompt_for_bool(field_name: Optional[str] = None, allow_none: bool = False) -> bool:
    """Prompt the user to enter a boolean value.

    :return: The boolean value entered by the user.
    """
    prompt_str = "Please enter a boolean value"
    if field_name is not None:
        prompt_str = f"{field_name.capitalize()}?"
    return typer.confirm(f"{prompt_str} ")
