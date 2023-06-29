"""Utility functions to parse CSV documents."""
import csv
import itertools
from typing import Dict, List, TextIO, Tuple, Union

from geneweaver.client.exceptions import EmptyFileError
from geneweaver.client.types import StringOrPath


def find_header(
    file_path: StringOrPath, max_rows_to_check: int = 5
) -> Tuple[bool, int]:
    """Determine if a CSV (.csv) file has a header row.

    This function will check up to 'max_rows_to_check' rows from the top to find a
    header row.

    This function assumes that a row can be interpreted as a header if none of its
    values are numeric, if it has more than one column, and if the following row has the
    same number of columns that it does.

    :param file_path: Path to the CSV file.
    :param max_rows_to_check: The number of rows to check from the top to find a header
    row.

    Returns
    -------
    Tuple[bool, int]: First index - True if a header row is found, False otherwise.
                      Second index - The index of the header row if found, otherwise -1.
    """
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i >= max_rows_to_check:
                break
            if (
                len(row) > 1
                and all(len(item) > 0 for item in row)
                and all(not item.replace(".", "", 1).isdigit() for item in row)
            ):
                next_row = next(reader, None)
                if next_row and len(row) == len(next_row):
                    return True, i
    return False, -1


def has_header(file_path: StringOrPath, max_rows_to_check: int = 5) -> bool:
    """Summary function to return true/false for if a header is found by `find_header`.

    :param file_path: Path to the CSV file.
    max_rows_to_check (int): The number of rows to check from the top to find a header
    row.

    Returns
    -------
    bool:  True if a header row is found, False otherwise.
    """
    return find_header(file_path, max_rows_to_check)[0]


def get_headers(file_path: StringOrPath) -> Tuple[List[str], int]:
    """Read the first row from a CSV file and return it as a list of strings.

    Assumes that the first row of the CSV file is the header row.

    :param file_path: Path to the CSV file.

    Returns
    -------
    Tuple[List[str], int]: List of column names from the CSV file, and the index of the
    header row.
    """
    headers = []
    file_has_header, header_idx = find_header(file_path)
    if file_has_header:
        headers = read_row(file_path, header_idx)
    return headers, header_idx


def read_row(file_path: StringOrPath, row_idx: int = 0) -> List[str]:
    """Get the contents of a row from a CSV file.

    :param file_path: The file path to the CSV file.
    :param row_idx: The index of the row from which to read the headers. Defaults to 0.

    Returns
    -------
    List[str]: The contents of a row

    Raises
    ------
    ValueError: If the file is empty or does not contain enough rows.
    """
    row = []
    with open(file_path, newline="") as f:
        reader = csv.reader(f)
        for i, r in enumerate(reader):
            if i == row_idx:
                row = r
                break
        else:
            raise ValueError(f"File does not contain a row at index {row_idx}")
        return row


def get_csv_dict_reader(file: TextIO, start_row: int) -> csv.DictReader:
    """Get a csv.DictReader for the given file, starting from the specified row.

    :param file: The opened file object.
    :param start_row: The row number to start reading from (0-indexed). This row will be
    used as the header.

    Returns
    -------
    csv.DictReader: A DictReader instance for the remaining rows in the file, using the
    specified row as the header.
    """
    reader = csv.reader(file)
    header = None
    for _ in range(start_row + 1):  # read up to and including the start_row
        header = next(reader, None)
    if header is None:
        raise ValueError("start_row was larger than the number of rows in the file")

    return csv.DictReader(file, fieldnames=header)


def read_to_dict(
    file_path: StringOrPath, start_row: int = 0
) -> List[Dict[str, Union[str, int]]]:
    """Read a CSV file and return its contents as a list of dictionaries.

    Each dictionary in the list corresponds to a row in the CSV file, and the keys
    are the column names from the CSV file.

    :param file_path: Path to the CSV file.
    :param start_row: The row number to start reading from (0-indexed).
                               This row will be used as the header.
                               Defaults to 0.

    Returns
    -------
    List[Dict[str, str]]: List of dictionaries representing the CSV file.
    """
    with open(file_path, mode="r") as infile:
        dict_reader = get_csv_dict_reader(infile, start_row)
        data = [dict(row) for row in dict_reader]
    return data


def read_to_dict_n_rows(
    file_path: StringOrPath, n: int, start_row: int = 0
) -> List[Dict[str, str]]:
    """Parse n lines of a CSV file into a dictionary.

    Parse a CSV file into a dictionary, with keys as column names and values as column
    values. This function will only return the first n rows of data.

    :param file_path: The file path to the CSV file.
    :param n: The number of rows of data to return.
    :param start_row: The row number to start reading from (0-indexed).
                               This row will be used as the header.
                               Defaults to 0.

    Returns
    -------
    List[Dict[str, str]]: A list of dictionaries, where each dictionary represents
    a row from the CSV file.
    """
    with open(file_path, mode="r") as infile:
        dict_reader = get_csv_dict_reader(infile, start_row)
        data = list(itertools.islice(dict_reader, n))
        if len(data) == 0:
            raise EmptyFileError(
                file_path,
                f"Selected start row ({start_row}) and " f"n ({n}) yielded no results.",
            )
    return data
