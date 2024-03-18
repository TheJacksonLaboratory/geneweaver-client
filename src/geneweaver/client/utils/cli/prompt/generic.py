"""Utility functions for prompting for generic values."""

from typing import Optional, Type, TypeVar

import typer
from geneweaver.client.utils.cli.prompt.none import (
    allow_none_str,
    prompt_if_none,
    value_represents_none,
)

T = TypeVar("T")


def prompt_generic(field_name: str, field_type: Type[T], allow_none: bool = False) -> T:
    """Prompt the user for a value for a field."""
    text_prompt = f"{field_name.replace('_', ' ').capitalize()} ({field_type.__name__})"
    if allow_none:
        text_prompt += allow_none_str()

    while True:
        result = typer.prompt(text_prompt)

        if allow_none and value_represents_none(result):
            return None
        else:
            try:
                return field_type(result)
            except (TypeError, ValueError):
                print(f"Invalid value for {field_name}. Please try again.")
                continue


def prompt_to_keep_dict_field(
    field_name: str, existing_kwargs: dict, default: bool = True
) -> bool:
    """Prompt the user to keep an existing field value.

    :param field_name: The name of the field to prompt for.
    :param existing_kwargs: The existing kwargs to use as defaults.
    :param default: What to set the default value to.
    :return: True if the user wants to keep the field value, False otherwise.
    """
    if field_name in existing_kwargs:
        selection = prompt_to_keep_field(
            field_name, existing_kwargs[field_name], default=default
        )
        if not selection:
            existing_kwargs.pop(field_name)
        return selection
    return False


def prompt_to_keep_field(
    field_name: str, field_value: str, default: bool = True
) -> bool:
    """Prompt the user to keep a field value.

    :param field_name: The name of the field to prompt for.
    :param field_value: The value of the field to prompt for.
    :param default: What to set the default value to.
    :return: True if the user wants to keep the field value, False otherwise.
    """
    field_name = field_name.replace("_", " ").capitalize()
    return typer.confirm(f"{field_name} = {field_value}, OK?", default=default)


def prompt_if_none_or_ask_to_keep(
    field_name: str, value: Optional[T] = None, default: bool = True
) -> Optional[T]:
    """Prompt the user to enter a value if the value is None or to keep the value.

    :param field_name: The name of the field to prompt for.
    :param value: The value to check.
    :param default: The default value for the prompt.
    :return: The value entered by the user.
    """
    if value is None:
        value = prompt_if_none(field_name, value)
    elif not prompt_to_keep_field(field_name, value, default=default):
        value = prompt_if_none(field_name, None)
    return value
