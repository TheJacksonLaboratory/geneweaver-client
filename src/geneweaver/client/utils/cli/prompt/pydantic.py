"""Utility functions for use with the CLI."""

from typing import Any, Optional, Type

import typer
from geneweaver.client.utils.cli.prompt.bool import is_bool, prompt_for_bool
from geneweaver.client.utils.cli.prompt.enum import (
    is_enum_or_enum_union,
    prompt_for_enum_selection,
)
from geneweaver.client.utils.cli.prompt.generic import prompt_generic
from geneweaver.client.utils.cli.prompt.list import (
    is_list_of_str_or_int,
    prompt_for_list_selection,
)
from pydantic import BaseModel, Field


def is_pydantic_base_model(arg: Type[Any]) -> bool:
    """Check if an argument is a pydantic base model.

    :param arg: The argument to check.
    :return: True if the argument is a pydantic base model, False otherwise.
    """
    try:
        return issubclass(arg, BaseModel)
    except TypeError:
        return False


def format_field_name(field_name: str) -> str:
    """Format a field name for display to the user.

    :param field_name: The field name to format.
    :return: The formatted field name.
    """
    return field_name.replace("_", " ").capitalize()


def prompt_to_keep_field(existing_kwargs: dict, field_name: str) -> dict:
    """Prompt the user to keep an existing field value.

    :param existing_kwargs: The existing kwargs to use as defaults.
    :param field_name: The name of the field to prompt for.
    """
    if field_name in existing_kwargs and not typer.confirm(
        f"{format_field_name(field_name)} =" f" {existing_kwargs[field_name]}, OK?",
        default=True,
    ):
        existing_kwargs.pop(field_name)
    return existing_kwargs


def prompt_for_field_by_type(
    field: Field, field_name: str, existing_kwargs: dict
) -> dict:
    """Prompt the user to enter a value for a field based on its type.

    :param field: The field to prompt for.
    :param field_name: The name of the field to prompt for.
    :param existing_kwargs: The existing kwargs to use as defaults.
    """
    field_type = field.outer_type_ if field.outer_type_ else str
    if is_pydantic_base_model(field_type):
        existing_kwargs[field_name] = prompt_for_missing_fields(
            field_type, existing_kwargs
        )
    elif is_enum_or_enum_union(field_type):
        existing_kwargs[field_name] = prompt_for_enum_selection(
            field_type, field.allow_none
        )
    elif is_list_of_str_or_int(field_type):
        existing_kwargs[field_name] = prompt_for_list_selection(
            field_type, field.allow_none
        )
    elif is_bool(field_type):
        existing_kwargs[field_name] = prompt_for_bool(field_name, field.allow_none)
    else:
        existing_kwargs[field_name] = prompt_generic(
            field_name, field_type, field.allow_none
        )
    return existing_kwargs


def prompt_for_missing_fields(
    model: Type[BaseModel],
    existing_kwargs: dict,
    exclude: Optional[set] = None,
    prompt_to_keep_existing: bool = True,
) -> dict:
    """Prompt the user to enter values for any missing fields in a pydantic model.

    :param model: The pydantic model to prompt for.
    :param existing_kwargs: The existing kwargs to use as defaults.
    :param exclude: A set of field names to exclude from prompting.
    :param prompt_to_keep_existing: Whether to prompt the user to keep existing
    :return: A dictionary of kwargs for the model.
    """
    for field_name, field in model.__fields__.items():
        if exclude and field_name in exclude:
            continue

        if prompt_to_keep_existing and field_name in existing_kwargs:
            prompt_to_keep_field(existing_kwargs, field_name)

        if field_name not in existing_kwargs:
            prompt_for_field_by_type(field, field_name, existing_kwargs)

    return existing_kwargs
