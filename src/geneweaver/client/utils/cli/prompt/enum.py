"""Utility functions for prompting the user related to enums."""

from enum import Enum
from typing import Any, Iterable, Type, TypeVar, Union, get_args

import typer

E = TypeVar("E", bound=Enum)


def is_enum_or_enum_union(field_type: Type[Any]) -> bool:
    """Check if the field_type is an enum or a union of enums."""
    # Check if the field_type is an enum
    try:
        if issubclass(field_type, Enum):
            return True
    except TypeError:
        return is_enum_union(field_type)


def is_enum_union(field_type: Any) -> bool:  # noqa: ANN401
    """Check if the field_type is a union of enums.

    :param field_type: The type to check.
    :return: True if field_type is a union of enum subclasses, False otherwise.
    """
    if hasattr(field_type, "__origin__") and field_type.__origin__ is Union:
        try:
            return all((issubclass(arg, Enum) for arg in get_args(field_type)))
        except TypeError:
            pass
    return False


def select_enum_from_enum_union(union_enum_type: Union[Enum]) -> Type[Enum]:
    """Select an enum from a union of enums.

    :param union_enum_type: The union of enums to select from.
    """
    # Check if the field_type is a union of enums
    # Prompt the user to select an enum from the union
    enum_type_options = get_args(union_enum_type)
    selection_string = _format_enum_type_selection(enum_type_options)
    print(selection_string)
    selected_value = typer.prompt(
        f"Please enter a value between 0 and {len(enum_type_options) - 1}: ", type=int
    )
    # Return the selected enum type
    return enum_type_options[selected_value]


def prompt_for_enum_selection(
    enum_class: Union[Enum, Union[Enum]],
    allow_none: bool = False,
) -> Enum:
    """Prompt the user to select an enum member from an enum.

    If provided with a union of enums, prompt the user to select an enum from the union.

    :param enum_class: The enum to select from.
    """
    # Determine the type of enum (int or str) and generate the appropriate prompt
    if is_enum_union(enum_class):
        enum_class = select_enum_from_enum_union(enum_class)

    enum_type = int if issubclass(enum_class, int) else str

    # Prompt the user for a selection
    selection_string = _format_enum_selection(enum_class, enum_type)
    print(selection_string)

    selected_value = typer.prompt(
        f"Please enter a value between 0 and {len(enum_class) - 1}: ", type=int
    )

    return _enum_member_by_index(enum_class, selected_value)


def _format_enum_selection(enum_class: Type[Enum], enum_type: Union[str, int]) -> str:
    """Format the enum selection prompt string."""
    enum_name = format_enum_name(enum_class)
    strs = [f"\nAvailable Geneset {enum_name} Types:"]
    for index, member in enumerate(enum_class):
        display_name = member.name.capitalize() + " "
        display_value = f"{member.value} -- {index}" if enum_type is str else index
        strs.append(f"    {display_name.ljust(30, '-')} {display_value}")
    return "\n".join(strs)


def _format_enum_type_selection(enums: Iterable[Type[Enum]]) -> str:
    """Format the enum type selection prompt string.

    :param enums: The enum types to select from.
    :return: The formatted enum type selection prompt string.
    """
    strs = ["\nPlease Select one of: "]
    for index, enum_class in enumerate(enums):
        enum_name = format_enum_name(enum_class)
        strs.append(f"    {enum_name.ljust(30, '-')} {index}")
    return "\n".join(strs)


def format_enum_name(enum_class: Type[Enum]) -> str:
    """Return the name of the enum class without the 'Geneset' or 'Type' suffix.

    :param enum_class (Type[Enum]): The class of the enumeration.
    :return (str): The name of the enum class without the 'Geneset' or 'Type' suffix.
    """
    return (
        enum_class.__name__.replace("Geneset", "")
        .replace("Type", "")
        .replace("Enum", "")
        .strip()
    )


def _enum_member_by_index(enum_class: Type[E], index: int) -> E:
    """Get the enum member at the specified index from the given enum class.

    :param enum_class (Type[E]): The class of the enumeration.
    :param index (int): The index of the enum member to return.
    :return (E): The enum member at the specified index.
    :raises IndexError: If the index is out of range.
    """
    return list(enum_class)[index]
