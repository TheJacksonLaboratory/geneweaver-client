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
def get_headers(file_path: Path, sheet: str = None):
    headers = []
    try:
        headers = general.get_headers(file_path, sheet_name=sheet)
    except (EmptyFileError, ValueError) as e:
        print(e)
        raise typer.Exit(code=1)

    for header in headers:
        print(header)


@cli.command()
def preview(file_path: Path, rows_to_read: int = 5, sheet: str = None):
    rows = []
    try:
        headers, headers_idx = general.get_headers(file_path, sheet_name=sheet)
        rows = general.data_file_to_dict_n_rows(
            file_path, rows_to_read, headers_idx, sheet_name=sheet
        )
    except (EmptyFileError, ValueError) as e:
        print(e)
        raise typer.Exit(code=1)

    table = Table(*headers)
    for row in rows:
        table.add_row(*(str(r) for r in row.values()))
    console.print(table)


@cli.command()
def get_sheet_names(file_path: Path):
    try:
        names = xlsx.get_sheet_names(file_path)
        print(names)
    except ValueError as e:
        print(e)
        raise typer.Exit(code=1)
