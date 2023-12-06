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
from pydantic import BaseModel


def is_pydantic_base_model(arg: Type[Any]) -> bool:
    """Check if an argument is a pydantic base model.

    :param arg: The argument to check.
    :return: True if the argument is a pydantic base model, False otherwise.
    """
    try:
        return issubclass(arg, BaseModel)
    except TypeError:
        return False


def prompt_for_missing_fields(
    model: Type[BaseModel], existing_kwargs: dict, exclude: Optional[set] = None
) -> dict:
    """Prompt the user to enter values for any missing fields in a pydantic model.

    :param model: The pydantic model to prompt for.
    :param existing_kwargs: The existing kwargs to use as defaults.
    :param exclude: A set of field names to exclude from prompting.
    :return: A dictionary of kwargs for the model.
    """
    for field_name, field in model.__fields__.items():
        if exclude and field_name in exclude:
            continue

        if field_name in existing_kwargs:
            keep = typer.confirm(
                f"{field_name.replace('_', ' ').capitalize()} ="
                f" {existing_kwargs[field_name]}, OK?",
                default=True,
            )
            if not keep:
                existing_kwargs.pop(field_name)

        if field_name not in existing_kwargs:
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
                existing_kwargs[field_name] = prompt_for_bool(
                    field_name, field.allow_none
                )
            else:
                existing_kwargs[field_name] = prompt_generic(
                    field_name, field_type, field.allow_none
                )

    return existing_kwargs
