"""Utilities for AON interaction."""

from collections.abc import Hashable
from typing import Dict, List, Tuple, TypeVar, Union

Number = TypeVar("Number", bound=Union[int, float])
T = TypeVar("T", bound=Hashable)


def map_symbols(
    original: Dict[T, Number], mappings: List[Tuple[T, T]]
) -> Dict[T, Number]:
    """Map gene symbols using a list of mappings.

    When a human gene maps to multiple mouse genes, there should be a row for each
    of those mouse ids to be included, and therefore the score will be the same
    for all of those.

    When multiple human genes map to the same mouse gene, we want to keep the
    gene that has the highest abs(score).

    :param original: The original gene symbols and values.
                     With the key as the identifier and the value as the value.
    :param mappings: The mappings to use.
                     With the source as the first item and the target as the second.

    :return: The mapped gene symbols and values.
    """
    mapped_values = {}
    for mapping in mappings:
        source, target = mapping

        try:
            value = original[source]
        except KeyError:
            continue

        if target not in mapped_values or abs(value) > abs(mapped_values[target]):
            mapped_values[target] = value

    return mapped_values
