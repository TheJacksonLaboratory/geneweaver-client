"""Utility functions for the parser module."""
from pathlib import Path
from typing import Dict, List

from geneweaver.client.types import StringOrPath


def get_file_type(file_path: StringOrPath) -> str:
    """Determine if a file at a given path is a csv or xlsx file.

    :param file_path: Path to the file.

    Returns
    -------
    str: The file type. 'csv' if the file is a CSV file, 'xlsx' if the file is an Excel
         file.

    Raises
    ------
    ValueError: If the file type is not supported.
    """
    file_path = Path(file_path)  # convert to Path object if not already
    extension = file_path.suffix.lower()

    if extension == ".csv":
        return "csv"
    elif extension == ".xlsx":
        return "xlsx"
    else:
        raise ValueError(f"Unsupported file type {extension}.")


def replace_keys(
    data: List[Dict[str, str]], new_keys: List[str]
) -> List[Dict[str, str]]:
    """Replace keys in a list of dictionaries.

    :param data: Original list of dictionaries.
    :param new_keys: List of new keys. The order should correspond to the order of
    original keys.

    Returns
    -------
    List[Dict[str, str]]: A new list of dictionaries with replaced keys.
    """
    new_data = []
    for row in data:
        new_row = dict(zip(new_keys, row.values(), strict=True))
        new_data.append(new_row)
    return new_data
