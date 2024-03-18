"""Utility functions for printing tables."""

from typing import List

from geneweaver.core.types import DictRow
from rich.console import Console
from rich.table import Table

console = Console()


def print_tabular_data(headers: List[str], rows: List[DictRow]) -> None:
    """Print the data in a formatted table.

    :param headers: The headers for the table.
    :param rows: The rows for the table.
    """
    table = Table(*headers)
    for row in rows:
        table.add_row(*(str(r) for r in row.values()))
    console.print(table)
