"""Print information about a file."""

from pathlib import Path
from typing import List


def print_metadata_xlsx(
    file_path: Path,
    sheet_names: List[str],
    sheet_metadata: List[List[str]],
    n_sheets: int,
) -> None:
    """Print metadata from an Excel file.

    :param file_path: The file path to the Excel file.
    :param sheet_names: A list of sheet names in the Excel file.
    :param sheet_metadata: A list of metadata for each sheet in the Excel file.
    :param n_sheets: The number of sheets in the Excel file.
    """
    print(f"{file_path} contains {n_sheets} sheets:")

    for name, metadata in zip(sheet_names, sheet_metadata):  # noqa: B905
        print(f" - {name} - {metadata}")


def print_metadata_csv(file_path: Path, metadata: List[str]) -> None:
    """Print the metadata from a CSV file.

    :param file_path: The file path to the CSV file.
    :param metadata: A list of metadata for the CSV file.
    """
    print(f"{file_path} contains:")
    for metadata_line in metadata:
        print(f" - {metadata_line}")
