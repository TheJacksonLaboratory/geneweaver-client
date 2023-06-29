"""Tests for the parser utility functions."""
# ruff: noqa: ANN001, ANN201
import pytest
from geneweaver.client.parser.utils import get_file_type, replace_keys


def test_get_file_type():
    """Test the get file type utility function."""
    # Test with a csv file
    assert get_file_type("/path/to/file.csv") == "csv"

    # Test with an Excel file
    assert get_file_type("/path/to/file.xlsx") == "xlsx"

    # Test with an unsupported file type
    with pytest.raises(ValueError, match="Unsupported") as exc_info:
        get_file_type("/path/to/file.txt")
    assert str(exc_info.value) == "Unsupported file type .txt."


def test_replace_keys():
    """Test the replace keys utility function."""
    data = [{"key1": "value1", "key2": "value2"}, {"key1": "value3", "key2": "value4"}]
    new_keys = ["new_key1", "new_key2"]
    expected_data = [
        {"new_key1": "value1", "new_key2": "value2"},
        {"new_key1": "value3", "new_key2": "value4"},
    ]

    assert replace_keys(data, new_keys) == expected_data
