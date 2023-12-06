"""Utility functions for prompting the user to enter a list of values."""
from typing import List, TypeVar, get_args, get_origin

import typer

T = TypeVar("T")


def prompt_for_list_selection(field_type: T, allow_none: bool = False) -> List[T]:
    """Prompt the user to enter a list of values.

    :param field_type: A list of strings or integers, treated as strings if not
                       integers.
    :return: The list of values entered by the user.
    """
    origin_type = get_origin(field_type)
    if origin_type != list:
        raise ValueError("Expected a typing.List type")

    # Extract the type of the list's elements
    element_type = get_args(field_type)[0]

    # Determine if the elements are integers or strings
    is_int_type = element_type is int

    items = []
    while True:
        item = typer.prompt(
            f"Enter a {'number' if is_int_type else 'string'} "
            "(or just enter to finish): ",
            type=element_type,
            default="",
        )
        if not item:
            break
        items.append(item)
    print(items)
    return items


def is_list_of_str_or_int(field_type: T) -> bool:
    """Check if the field_type is a list of strings or integers.

    :param field_type: The field type to check.
    :return: True if the field type is a list of strings or integers, False otherwise.
    """
    # Check if the field_type is a list
    if get_origin(field_type) is list:
        # Get the type of elements in the list
        element_type = get_args(field_type)[0]
        # Check if the element type is str or int
        return element_type in [str, int]
    return False
