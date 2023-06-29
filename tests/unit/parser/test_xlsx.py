"""Tests for the XLSX parser module."""
# ruff: noqa: B905, ANN001, ANN201
from unittest.mock import patch

import pytest
from geneweaver.client.parser import xlsx


def test_get_sheet_names(multi_sheet_excel_file):
    """Test that the get_sheet_names function returns the correct sheet names."""
    temp_excel_file_path, expected_result = multi_sheet_excel_file

    # Call the function and get the result
    result = xlsx.get_sheet_names(temp_excel_file_path)

    # Check if the result matches the expected result
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_get_sheet_names_nonexistent_file():
    """Test that the get_sheet_names raises an error when the file does not exist."""
    with pytest.raises(FileNotFoundError):
        xlsx.get_sheet_names("nonexistent_file.xlsx")


def test_get_sheet_names_invalid_file(not_an_xlsx_file):
    """Test that the get_sheet_names raises an error when file not an Excel file."""
    # Test the function
    with pytest.raises(ValueError, match="File is not a zip file"):
        xlsx.get_sheet_names(not_an_xlsx_file)


def test_get_sheet_basic(multi_sheet_excel_file):
    """Test that the get_sheet function returns the correct sheet."""
    file_path, sheets = multi_sheet_excel_file

    # Test the function with default sheet
    sheet = xlsx.get_sheet(file_path)
    assert sheet.title == sheets[0]

    for sheet_name in sheets:
        # Test the function with specified sheet
        sheet = xlsx.get_sheet(file_path, sheet_name)
        assert sheet.title == sheet_name


def test_get_sheet_nonexistent(multi_sheet_excel_file):
    """Test that the get_sheet raises an error when the sheet does not exist."""
    file_path, _ = multi_sheet_excel_file
    # Test the function with a non-existing sheet
    with pytest.raises(KeyError):
        xlsx.get_sheet(file_path, "NonexistentSheet")


def test_get_sheet_invalid_file():
    """Test that the get_sheet raises an error when the file is not an Excel file."""
    with pytest.raises(FileNotFoundError):
        xlsx.get_sheet("nonexistent_file.xlsx")


def test_has_header_true():
    """Test that the has_header returns True when the header exists."""
    with patch(
        "geneweaver.client.parser.xlsx.find_header", return_value=(True, 0)
    ) as mock:
        assert xlsx.has_header("fake_path") is True
        mock.assert_called_once_with("fake_path", 5, None)


def test_has_header_false():
    """Test that the has_header returns False when the header does not exist."""
    with patch(
        "geneweaver.client.parser.xlsx.find_header", return_value=(False, -1)
    ) as mock:
        assert xlsx.has_header("fake_path") is False
        mock.assert_called_once_with("fake_path", 5, None)


def test_has_header_custom_args():
    """Test that the has_header returns the correct value arguments are passed."""
    with patch(
        "geneweaver.client.parser.xlsx.find_header", return_value=(True, 0)
    ) as mock:
        assert xlsx.has_header("fake_path", 7, "Sheet2") is True
        mock.assert_called_once_with("fake_path", 7, "Sheet2")


def test_find_header(multi_sheet_excel_file_w_data):
    """Test that the find_header returns correct header index and has_header value."""
    excel_file, _, data = multi_sheet_excel_file_w_data
    has_header, index = xlsx.find_header(excel_file)
    assert index == data[1]
    assert has_header is data[2]


def test_get_headers(multi_sheet_excel_file_w_data):
    """Test that the get_headers returns the correct headers."""
    excel_file, _, data = multi_sheet_excel_file_w_data
    data, index, has_header = data
    headers, header_idx = xlsx.get_headers(excel_file)
    if has_header:
        assert headers == data[index]
        assert header_idx == index
    else:
        assert headers == []


def test_read_row(multi_sheet_excel_file_w_data):
    """Test that the read_row returns the correct row."""
    excel_file, _, data = multi_sheet_excel_file_w_data
    data, _, _ = data
    for idx, d in enumerate(data):
        row = xlsx.read_row(excel_file, idx)
        if len(row) == len(d):
            assert row == d
        elif len(d) == 0:
            assert all([cell is None for cell in row])
        else:
            for item in d:
                assert item in row


def test_read_row_invalid_index(multi_sheet_excel_file_w_data):
    """Test that the read_row raises an error when the index is out of bounds."""
    excel_file, _, data = multi_sheet_excel_file_w_data
    data, _, _ = data
    with pytest.raises(ValueError, match="does not contain a row"):
        xlsx.read_row(excel_file, len(data) + 1)


def test_read_row_no_data(multi_sheet_excel_file):
    """Test that the read_row raises an error when the sheet does not contain data."""
    excel_file, _ = multi_sheet_excel_file
    with pytest.raises(ValueError, match="does not contain a row"):
        xlsx.read_row(excel_file, 1)


def test_read_row_invalid_file():
    """Test that the read_row raises an error when the file is not an Excel file."""
    with pytest.raises(FileNotFoundError):
        xlsx.read_row("nonexistent_file.xlsx", 0)


def test_read_row_invalid_sheet(multi_sheet_excel_file_w_data):
    """Test that the read_row raises an error when the sheet does not exist."""
    excel_file, _, data = multi_sheet_excel_file_w_data
    data, _, _ = data
    with pytest.raises(KeyError):
        xlsx.read_row(excel_file, 0, "NonexistentSheet")


def test_read_to_dict(multi_sheet_excel_file_w_data_as_dict):
    """Test that the read_to_dict returns the correct dictionary."""
    excel_file, sheets, header_index, data = multi_sheet_excel_file_w_data_as_dict
    if header_index >= 0:
        for sheet in sheets:
            result = xlsx.read_to_dict(
                excel_file, start_row=header_index, sheet_name=sheet
            )
            assert result == data
    else:
        for sheet in sheets:
            result = xlsx.read_to_dict(excel_file, sheet_name=sheet)
            assert result == data


def test_read_to_dict_invalid_file():
    """Test that the read_to_dict raises an error when the file is not an Excel file."""
    with pytest.raises(FileNotFoundError):
        xlsx.read_to_dict("nonexistent_file.xlsx")


def test_read_to_dict_n_rows(multi_sheet_excel_file_w_data_as_dict):
    """Test that the read_to_dict returns the correct dictionary with n_rows."""
    excel_file, sheets, header_index, data = multi_sheet_excel_file_w_data_as_dict
    if header_index >= 0:
        for sheet in sheets:
            result = xlsx.read_to_dict_n_rows(
                excel_file, n=1, start_row=header_index, sheet_name=sheet
            )
            assert result == [data[0]]
    else:
        for sheet in sheets:
            result = xlsx.read_to_dict_n_rows(excel_file, n=1, sheet_name=sheet)
            assert result == [data[0]]


def test_read_to_dict_no_data(multi_sheet_excel_file):
    """Test that it raises an error when the file contains no data."""
    file_path, _ = multi_sheet_excel_file
    with pytest.raises(ValueError, match="does not contain a row"):
        xlsx.read_to_dict_n_rows(file_path, 1)


def test_read_to_dict_n_rows_no_data(multi_sheet_excel_file):
    """Test that it raises an error when the file does not contain a row."""
    file_path, _ = multi_sheet_excel_file
    with pytest.raises(ValueError, match="does not contain a row"):
        xlsx.read_to_dict_n_rows(file_path, 1)
