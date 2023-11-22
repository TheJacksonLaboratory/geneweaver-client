"""CLI for parsing utility functions."""
from pathlib import Path
from typing import List, Optional, Tuple

import typer
from geneweaver.client.cli.utils import print_value_errors
from geneweaver.client.parser import general
from geneweaver.core.parse import csv, xlsx
from geneweaver.core.parse.exceptions import EmptyFileError, UnsupportedFileTypeError
from geneweaver.core.parse.utils import get_file_type
from geneweaver.core.types import DictRow
from rich import print
from rich.console import Console
from rich.table import Table

cli = typer.Typer()
console = Console()


@cli.command()
@print_value_errors
def infer_file_format(file_path: Path) -> None:
    """Infer the file format of a data file."""
    file_type = get_file_type(file_path)
    print(f"{file_type.name} - {file_type.value}")


@cli.command()
@print_value_errors
def get_headers(file_path: Path, sheet: str = None) -> None:
    """Get the headers from a data file."""
    try:
        headers, _ = general.get_headers(file_path, sheet_name=sheet)
    except (EmptyFileError, ValueError, UnsupportedFileTypeError) as e:
        print(e)
        raise typer.Exit(code=1) from e

    for idx, header in enumerate(headers):
        print(f"{idx} - {header}")


@cli.command()
@print_value_errors
def get_sheet_names(file_path: Path) -> None:
    """Get the sheet names from an Excel file."""
    try:
        names = xlsx.get_sheet_names(file_path)
    except ValueError as e:
        print(e)
        raise typer.Exit(code=1) from e

    for idx, name in enumerate(names):
        print(f"{idx} - {name}")


@cli.command()
@print_value_errors
def get_metadata(file_path: Path, sheet: Optional[str] = None) -> None:
    """Get the metadata from a data file."""
    file_type = get_file_type(file_path)

    if file_type == "csv":
        header, header_idx = csv.get_headers(file_path)
        _print_metadata_csv(file_path, header_idx)
    elif file_type == "xlsx":
        sheet_names, sheet_metadata, _, _, n_sheets = _get_metadata_xlsx(
            file_path, sheet
        )
        _print_metadata_xlsx(file_path, sheet_names, sheet_metadata, n_sheets)


@cli.command()
@print_value_errors
def preview(
    file_path: Path, rows_to_read: int = 5, sheet: str = None, prompt: bool = True
) -> None:
    """Preview the data in a data file."""
    file_type = get_file_type(file_path)
    if file_type == "csv":
        _preview_csv(file_path, rows_to_read, prompt)
    elif file_type == "xlsx":
        _preview_xlsx(file_path, rows_to_read, sheet, prompt)


def _preview_csv(file_path: Path, rows_to_read: int = 5, prompt: bool = True) -> None:
    """Preview the data in a CSV file."""
    header, header_idx = csv.get_headers(file_path)
    _print_metadata_csv(file_path, header_idx)

    if prompt:
        typer.confirm("Do you want to preview data?", default=True, abort=True)

    rows = csv.read_to_dict_n_rows(file_path, rows_to_read, header_idx)
    _print_format_data(header, rows)


def _print_metadata_csv(file_path: Path, header_idx: int) -> None:
    """Print the metadata from a CSV file."""
    try:
        metadata = general.read_metadata(file_path, header_idx)
    except (EmptyFileError, ValueError, UnsupportedFileTypeError) as e:
        print(e)
        raise typer.Exit(code=1) from e

    print(f"{file_path} contains:")
    for metadata_line in metadata:
        print(f" - {metadata_line}")


def _get_metadata_xlsx(
    file_path: Path, sheet: Optional[str] = None
) -> Tuple[List[str], List[List[str]], List[List[str]], List[int], int]:
    if sheet:
        sheet_names = [sheet]
        headers, headers_idx = xlsx.get_headers(file_path, sheet_name=sheet)
        sheet_metadata = [
            general.read_metadata(file_path, headers_idx, sheet_name=sheet)
        ]
        headers, headers_idx = [headers], [headers_idx]
        n_sheets = 1
    else:
        sheet_names = xlsx.get_sheet_names(file_path)
        headers, headers_idx = [], []
        for s in sheet_names:
            h, h_idx = xlsx.get_headers(file_path, sheet_name=s)
            headers.append(h)
            headers_idx.append(h_idx)

        sheet_metadata = [
            general.read_metadata(file_path, h, sheet_name=s)
            for s, h in zip(sheet_names, headers_idx)  # noqa: B905
        ]
        n_sheets = len(sheet_names)

    return sheet_names, sheet_metadata, headers, headers_idx, n_sheets


def _print_metadata_xlsx(
    file_path: Path,
    sheet_names: List[str],
    sheet_metadata: List[List[str]],
    n_sheets: int,
) -> None:
    print(f"{file_path} contains {n_sheets} sheets:")

    for name, metadata in zip(sheet_names, sheet_metadata):  # noqa: B905
        print(f" - {name} - {metadata}")


def _preview_xlsx(
    file_path: Path, rows_to_read: int = 5, sheet: str = None, prompt: bool = True
) -> None:
    sheet_names, sheet_metadata, headers, headers_idx, n_sheets = _get_metadata_xlsx(
        file_path, sheet
    )

    if not sheet:
        _print_metadata_xlsx(file_path, sheet_names, sheet_metadata, n_sheets)

        if prompt:
            typer.confirm("Do you want to preview data?", default=True, abort=True)

    zipped_data = zip(sheet_names, sheet_metadata, headers, headers_idx)  # noqa: B905

    for idx, (sheet_name, metadata, header, header_idx) in enumerate(zipped_data):
        print(f"Data for sheet - {sheet_name} - {metadata}")
        rows = xlsx.read_to_dict_n_rows(
            str(file_path), rows_to_read, header_idx, sheet_name
        )
        _print_format_data(header, rows)

        if prompt and idx < n_sheets - 1:
            typer.confirm("Next sheet?", default=True, abort=True)


def _preview_data(file_path: Path, rows_to_read: int = 5, sheet: str = None) -> None:
    try:
        headers, headers_idx = general.get_headers(file_path, sheet_name=sheet)
        rows = general.data_file_to_dict_n_rows(
            file_path, rows_to_read, headers_idx, sheet_name=sheet
        )
    except ValueError as e:
        print("Something went wrong, the file is probably empty.\n" + str(e))
        raise typer.Exit(code=1) from e
    except (EmptyFileError, UnsupportedFileTypeError) as e:
        print(e)
        raise typer.Exit(code=1) from e

    _print_format_data(headers, rows)


def _print_format_data(headers: List[str], rows: List[DictRow]) -> None:
    """Print the data in a formatted table."""
    table = Table(*headers)
    for row in rows:
        table.add_row(*(str(r) for r in row.values()))
    console.print(table)
