"""Utility functions for use with the CLI."""

import functools
from typing import Callable

import typer


def print_value_errors(func: Callable) -> Callable:
    """Print any value errors that occur in the decorated function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):  # noqa: ANN002, ANN003, ANN202
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"An error occurred: {e}")
            typer.Exit(code=1)

    return wrapper
