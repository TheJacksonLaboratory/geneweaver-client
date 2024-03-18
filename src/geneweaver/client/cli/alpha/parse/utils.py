"""CLI for parsing utility functions."""

from pathlib import Path
from typing import Optional

import typer
from geneweaver.client.parser import general
from geneweaver.client.utils.cli.decorators.errors import print_value_errors
from geneweaver.client.utils.cli.print.file_info import (
    print_metadata_csv,
    print_metadata_xlsx,
)
from geneweaver.client.utils.cli.print.tables import print_tabular_data
from geneweaver.core.parse import csv, xlsx
from geneweaver.core.parse.exceptions import EmptyFileError, UnsupportedFileTypeError
from geneweaver.core.parse.utils import get_file_type
from rich import print
from rich.console import Console

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
        try:
            metadata = general.read_metadata(file_path, header_idx)
        except (EmptyFileError, ValueError, UnsupportedFileTypeError) as e:
            print(e)
            raise typer.Exit(code=1) from e

        print_metadata_csv(file_path, metadata)
    elif file_type == "xlsx":
        sheet_names, sheet_metadata, _, _, n_sheets = xlsx.get_metadata(
            file_path, sheet
        )
        print_metadata_xlsx(file_path, sheet_names, sheet_metadata, n_sheets)


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
    try:
        metadata = general.read_metadata(file_path, header_idx)
    except (EmptyFileError, ValueError, UnsupportedFileTypeError) as e:
        print(e)
        raise typer.Exit(code=1) from e

    print_metadata_csv(file_path, metadata)

    if prompt:
        typer.confirm("Do you want to preview data?", default=True, abort=True)

    rows = csv.read_to_dict_n_rows(file_path, rows_to_read, header_idx)
    print_tabular_data(header, rows)


def _preview_xlsx(
    file_path: Path, rows_to_read: int = 5, sheet: str = None, prompt: bool = True
) -> None:
    sheet_names, sheet_metadata, headers, headers_idx, n_sheets = xlsx.get_metadata(
        file_path, sheet
    )

    if not sheet:
        print_metadata_xlsx(file_path, sheet_names, sheet_metadata, n_sheets)

        if prompt:
            typer.confirm("Do you want to preview data?", default=True, abort=True)

    zipped_data = zip(sheet_names, sheet_metadata, headers, headers_idx)  # noqa: B905

    for idx, (sheet_name, metadata, header, header_idx) in enumerate(zipped_data):
        print(f"Data for sheet - {sheet_name} - {metadata}")
        rows = xlsx.read_to_dict_n_rows(
            str(file_path), rows_to_read, header_idx, sheet_name
        )
        print_tabular_data(header, rows)

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

    print_tabular_data(headers, rows)
