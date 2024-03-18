"""Test the tables.print_tabular_data function."""

from unittest.mock import MagicMock, Mock, patch

import pytest
from geneweaver.client.utils.cli.print.tables import print_tabular_data
from rich.table import Table


@pytest.fixture()
def mock_console():
    """Mock the console object."""
    with patch("geneweaver.client.utils.cli.print.tables.Console") as mock:
        yield mock


@pytest.mark.parametrize(
    ("headers", "rows"),
    [
        (["Name", "Age"], [{"Name": "Alice", "Age": 30}, {"Name": "Bob", "Age": 25}]),
        (["ID", "Score"], [{"ID": 1, "Score": 85}, {"ID": 2, "Score": 90}]),
        # Testing with empty headers
        ([], [{"ID": 1, "Score": 85}, {"ID": 2, "Score": 90}]),
        # Testing with empty rows
        (["ID", "Score"], []),
        # Testing with empty headers and rows
        ([], []),
    ],
)
def test_print_tabular_data(headers, rows, monkeypatch, mock_console):
    """Test the print_tabular_data function."""
    # Mocking the console.print method
    mock_print = Mock()
    mock_table = MagicMock(spec=Table)
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.print.tables.console.print", mock_print
    )
    monkeypatch.setattr("geneweaver.client.utils.cli.print.tables.Table", mock_table)

    # Calling the function with mock
    print_tabular_data(headers, rows)

    assert mock_table.call_count == 1
    assert mock_table.call_args[0] == tuple(headers)
    assert mock_table.return_value.add_row.call_count == len(rows)

    # Asserting that the console.print method was called
    assert mock_print.call_count == 1
    assert isinstance(mock_print.call_args[0][0], MagicMock)
