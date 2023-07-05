"""Test the general entrypoint to parser functions."""
# ruff: noqa: ANN001, ANN201
from unittest.mock import patch

import pytest
from geneweaver.client.parser import general


@pytest.mark.parametrize(
    ("file_type", "expected_result"),
    [
        ("csv", ["csv_header1", "csv_header2"]),
        ("xlsx", ["xlsx_header1", "xlsx_header2"]),
    ],
)
@patch("geneweaver.client.parser.utils.get_file_type")
@patch(
    "geneweaver.client.parser.csv.get_headers",
    return_value=(["csv_header1", "csv_header2"], []),
)
@patch(
    "geneweaver.client.parser.xlsx.get_headers",
    return_value=(["xlsx_header1", "xlsx_header2"], []),
)
def test_get_headers(
    mock_xlsx_get_headers,
    mock_csv_get_headers,
    mock_get_file_type,
    file_type,
    expected_result,
):
    """Test the get_headers function."""
    mock_get_file_type.return_value = file_type
    result = general.get_headers("dummy_path")
    assert result == expected_result

    if file_type == "csv":
        mock_csv_get_headers.assert_called_once()
        mock_xlsx_get_headers.assert_not_called()
    elif file_type == "xlsx":
        mock_xlsx_get_headers.assert_called_once()
        mock_csv_get_headers.assert_not_called()


@pytest.mark.parametrize(
    "file_type",
    ["tsv", "txt", "tiff"],
)
@patch("geneweaver.client.parser.utils.get_file_type")
def test_get_headers_raises(mock_get_file_type, file_type):
    """Test the get_headers function raises an error for unsupported file types."""
    mock_get_file_type.return_value = file_type
    with pytest.raises(ValueError, match="Unsupported") as e:
        general.get_headers("dummy_path.txt")

    assert file_type in str(e.value)


EXPECTED_CSV_RESULT_DICT = [
    {"csv_header1": "value1", "csv_header2": "value2"},
    {"csv_header1": "value3", "csv_header2": "value4"},
]

EXPECTED_XLSX_RESULT_DICT = [
    {"xlsx_header1": "value1", "xlsx_header2": "value2"},
    {"xlsx_header1": "value3", "xlsx_header2": "value4"},
]


@pytest.mark.parametrize(
    ("file_type", "expected_result"),
    [
        ("csv", EXPECTED_CSV_RESULT_DICT),
        ("xlsx", EXPECTED_XLSX_RESULT_DICT),
    ],
)
@patch("geneweaver.client.parser.utils.get_file_type")
@patch(
    "geneweaver.client.parser.csv.read_to_dict",
    return_value=EXPECTED_CSV_RESULT_DICT,
)
@patch(
    "geneweaver.client.parser.xlsx.read_to_dict",
    return_value=EXPECTED_XLSX_RESULT_DICT,
)
def test_data_file_to_dict(
    mock_xlsx_read_to_dict,
    mock_csv_read_to_dict,
    mock_get_file_type,
    file_type,
    expected_result,
):
    """Test the data_file_to_dict function."""
    mock_get_file_type.return_value = file_type
    result = general.data_file_to_dict("dummy_path")
    assert result == expected_result

    if file_type == "csv":
        mock_csv_read_to_dict.assert_called_once()
        mock_xlsx_read_to_dict.assert_not_called()
    elif file_type == "xlsx":
        mock_xlsx_read_to_dict.assert_called_once()
        mock_csv_read_to_dict.assert_not_called()


@pytest.mark.parametrize(
    "file_type",
    ["tsv", "txt", "tiff"],
)
@patch("geneweaver.client.parser.utils.get_file_type")
def test_data_file_to_dict_wrong_file_type(mock_get_file_type, file_type):
    """Test that data_file_to_dict raises an error for unsupported file types."""
    mock_get_file_type.return_value = file_type
    with pytest.raises(ValueError, match="Unsupported") as e:
        general.data_file_to_dict("dummy_path.txt")

    assert file_type in str(e.value)


@pytest.mark.parametrize(
    ("file_type", "expected_result"),
    [
        ("csv", EXPECTED_CSV_RESULT_DICT),
        ("xlsx", EXPECTED_XLSX_RESULT_DICT),
    ],
)
@patch("geneweaver.client.parser.utils.get_file_type")
@patch(
    "geneweaver.client.parser.csv.read_to_dict_n_rows",
    return_value=EXPECTED_CSV_RESULT_DICT,
)
@patch(
    "geneweaver.client.parser.xlsx.read_to_dict_n_rows",
    return_value=EXPECTED_XLSX_RESULT_DICT,
)
def test_data_file_to_dict_n_rows(
    mock_xlsx_read_to_dict,
    mock_csv_read_to_dict,
    mock_get_file_type,
    file_type,
    expected_result,
):
    """Test the data_file_to_dict_n_rows function."""
    mock_get_file_type.return_value = file_type
    result = general.data_file_to_dict_n_rows("dummy_path", 2)
    assert result == expected_result

    if file_type == "csv":
        mock_csv_read_to_dict.assert_called_once()
        mock_xlsx_read_to_dict.assert_not_called()
    elif file_type == "xlsx":
        mock_xlsx_read_to_dict.assert_called_once()
        mock_csv_read_to_dict.assert_not_called()


@pytest.mark.parametrize(
    "file_type",
    ["tsv", "txt", "tiff"],
)
@patch("geneweaver.client.parser.utils.get_file_type")
def test_data_file_to_dict_n_rows_wrong_file_type(mock_get_file_type, file_type):
    """Test that data_file_to_dict_n_rows raises an error for unsupported file types."""
    mock_get_file_type.return_value = file_type
    with pytest.raises(ValueError, match="Unsupported") as e:
        general.data_file_to_dict_n_rows("dummy_path.txt", 2)

    assert file_type in str(e.value)
