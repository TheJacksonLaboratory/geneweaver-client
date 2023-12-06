"""Test the file_info.print_metadata_csv function."""
from pathlib import Path
from unittest.mock import Mock

import pytest
from geneweaver.client.utils.cli.print.file_info import print_metadata_xlsx


@pytest.mark.parametrize("extension", [".csv", ".xlsx", ".xls", ".txt", ".tsv"])
@pytest.mark.parametrize(
    "filename",
    [
        "something",
        "something_else",
        "-",
        "file",
        "a_very_long_filename_with_way_too_many_characters_to_be_reasonable",
    ],
)
@pytest.mark.parametrize(
    "sheet_names",
    [
        ["sheet1"],
        ["sheet1", "sheet2"],
        [f"test{i}" for i in range(10)],
        [f"test{i}" for i in range(100)],
        [],
    ],
)
@pytest.mark.parametrize(
    "metadata",
    [
        ["metadata"],
        ["metadata1", "metadata2"],
        [f"test{i}" for i in range(10)],
        [f"test{i}" for i in range(100)],
        [],
    ],
)
def test_print_metadata_xlsx(extension, filename, sheet_names, metadata, monkeypatch):
    """Test the file_info.print_metadata_csv function."""
    filename = filename + extension
    mock_print = Mock()
    monkeypatch.setattr("builtins.print", mock_print)
    assert mock_print.call_count == 0

    print_metadata_xlsx(
        Path(filename),
        sheet_names,
        [metadata for _ in range(len(sheet_names))],
        len(sheet_names),
    )

    assert mock_print.call_count == len(sheet_names) + 1
    assert filename in mock_print.call_args_list[0][0][0]
    assert str(len(sheet_names)) in mock_print.call_args_list[0][0][0]

    for i, line in enumerate(sheet_names):
        assert line in mock_print.call_args_list[i + 1][0][0]
