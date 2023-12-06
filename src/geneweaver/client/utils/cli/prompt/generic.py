"""Utility functions for prompting for generic values."""
from typing import Type, TypeVar

import typer
from geneweaver.client.utils.cli.prompt.none import (
    allow_none_str,
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
