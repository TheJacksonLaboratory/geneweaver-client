"""A module that marshals access to specific file type parsing."""
from typing import List, Optional

from geneweaver.core.parse import csv, utils, xlsx
from geneweaver.core.parse.exceptions import UnsupportedFileTypeError
from geneweaver.core.types import DictRow, StringOrPath


def get_headers(file_path: StringOrPath, sheet_name: Optional[str] = None) -> List[str]:
    """Retrieve the header row from a CSV or Excel file.

    This function first determines the file type (CSV or Excel) and then uses
    the appropriate helper function to get the headers.

    :param file_path: The path to the file.
    :param sheet_name: Name of the sheet to read from (for Excel files).
                       If not provided, the function will read from the active sheet.
                       This argument is ignored for CSV files.

    :returns: A list of strings representing the header row of the file.

    :raises ValueError: If the file type is neither CSV nor Excel (.xlsx).
    """
    file_type = utils.get_file_type(file_path)

    if file_type == "csv":
        data, _ = csv.get_headers(file_path)

    elif file_type == "xlsx":
        data, _ = xlsx.get_headers(file_path, sheet_name)

    else:
        raise UnsupportedFileTypeError(f"Unsupported file type: {file_type}")

    return data


def data_file_to_dict(
    file_path: StringOrPath, sheet_name: Optional[str] = None
) -> List[DictRow]:
    """Parse a CSV or Excel file into a list of dictionaries.

    Parse a CSV or Excel file into a list of dictionaries, with keys as column names and
     values as column values.

    :param file_path: The file path to the CSV or Excel file.
    :param sheet_name: Name of the sheet to read from (for Excel files). If not
    provided, the function will read from the active sheet. Ignored for CSV files.

    :returns: A list of dictionaries, where each dictionary represents a row from the
    CSV or Excel file.
    """
    file_type = utils.get_file_type(file_path)

    if file_type == "csv":
        data = csv.read_to_dict(file_path)

    elif file_type == "xlsx":
        data = xlsx.read_to_dict(file_path, sheet_name)

    else:
        raise UnsupportedFileTypeError(f"Unsupported file type: {file_type}")

    return data


def data_file_to_dict_n_rows(
    file_path: StringOrPath,
    n: int,
    start_row: int = 0,
    sheet_name: Optional[str] = None,
) -> List[DictRow]:
    """Parse n lines of a CSV or Excel file into a list of dictionaries.

    Parse a CSV or Excel file into a list of dictionaries, with keys as column names and
    values as column values.

    :param file_path: The file path to the CSV or Excel file.
    :param n: The number of rows of data to return.
    :param start_row: The row to start reading from. Defaults to 0.
    :param sheet_name: Name of the sheet to read from (for Excel files). If not
    provided, the function will read from the active sheet. Ignored for CSV files.

    :returns: A list of dictionaries, where each dictionary represents a row from the
    CSV or Excel file.
    """
    file_type = utils.get_file_type(file_path)

    if file_type == "csv":
        data = csv.read_to_dict_n_rows(file_path, n, start_row)

    elif file_type == "xlsx":
        data = xlsx.read_to_dict_n_rows(file_path, n, start_row, sheet_name)

    else:
        raise UnsupportedFileTypeError(f"Unsupported file type: {file_type}")

    return data
