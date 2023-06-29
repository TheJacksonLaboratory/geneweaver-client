"""CLI for parsing data files."""
from pathlib import Path

import typer
from geneweaver.client.exceptions import EmptyFileError
from geneweaver.client.parser import general, xlsx
from rich import print
from rich.console import Console
from rich.table import Table

cli = typer.Typer()
console = Console()


@cli.command()
def get_headers(file_path: Path, sheet: str = None) -> None:
    """Get the headers from a data file."""
    headers = []
    try:
        headers = general.get_headers(file_path, sheet_name=sheet)
    except (EmptyFileError, ValueError) as e:
        print(e)
        raise typer.Exit(code=1) from e

    for header in headers:
        print(header)


@cli.command()
def preview(file_path: Path, rows_to_read: int = 5, sheet: str = None) -> None:
    """Preview the data in a data file."""
    rows = []
    try:
        headers, headers_idx = general.get_headers(file_path, sheet_name=sheet)
        rows = general.data_file_to_dict_n_rows(
            file_path, rows_to_read, headers_idx, sheet_name=sheet
        )
    except (EmptyFileError, ValueError) as e:
        print(e)
        raise typer.Exit(code=1) from e

    table = Table(*headers)
    for row in rows:
        table.add_row(*(str(r) for r in row.values()))
    console.print(table)


@cli.command()
def get_sheet_names(file_path: Path) -> None:
    """Get the sheet names from an Excel file."""
    try:
        names = xlsx.get_sheet_names(file_path)
        print(names)
    except ValueError as e:
        print(e)
        raise typer.Exit(code=1) from e
