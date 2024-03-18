"""Utility functions for adding CLI Options."""

# ruff: noqa: ANN001, ANN002, ANN003, ANN201, ANN202
import functools
from inspect import Parameter, signature
from typing import Type

import typer
from pydantic import BaseModel


def add_options_from_model(model: Type[BaseModel], option_prefix: str = ""):
    """Add options to a function from a pydantic model.

    :param model: The pydantic model to add options from.
    :param option_prefix: A prefix to add to the option names.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            model_instance = model(**kwargs)
            return func(model_instance)

        sig = signature(func)
        new_parameters = list(sig.parameters.values())

        for field_name, field in model.__fields__.items():
            option_help = field.field_info.description or field_name
            option_name = (
                f"{option_prefix}_{field_name}" if option_prefix else field_name
            )
            new_param = Parameter(
                option_name,
                Parameter.KEYWORD_ONLY,
                default=typer.Option(..., help=option_help),
            )
            new_parameters.append(new_param)

        wrapper.__signature__ = sig.replace(parameters=new_parameters)
        return wrapper

    return decorator
