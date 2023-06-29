"""Tests for the CSV parser module."""
# ruff: noqa: B905, ANN001, ANN201
import tempfile
from pathlib import Path

import pytest
from geneweaver.client.exceptions import EmptyFileError
from geneweaver.client.parser.csv import (
    find_header,
    get_headers,
    has_header,
    read_row,
    read_to_dict,
    read_to_dict_n_rows,
)

EXAMPLE_CSV_FILES_WITH_HEADER = [
    "name,age\nAlice,20\nBob,30",
    (
        "ID,geneSymbol,geneName,illID.Search_Key,illID.ILMN_Gene,illID.Accession,"
        "illID.Symbol,illID.Probe_Id,illID.Array_Address_Id,illID.nuID,Fold Change,"
        "logFC,AveExpr,t,P.Value,adj.P.Val,B\n"
        "6hA0gLWXgj2oJI6dYo,March2,membrane-associated ring finger (C3HC4) 2,"
        "ILMN_211667,MARCH2,NM_145486.2,March2,ILMN_1236993,2490630,6hA0gLWXgj2oJI6dYo,"
        "0.973740363,-0.03839095,9.386122676,-0.644865251,0.525578157,0.870814186,"
        "-5.896065537"
    ),
    (
        "geneSymbol,geneName,Fold Change,P.Value,adj.P.Val,B\n"
        "March2,membrane-associated ring finger (C3HC4) 2,0.973740363,"
        "0.525578157,0.870814186,-5.896065537"
    ),
    (
        "Table 1\n"
        "geneSymbol,geneName,Fold Change,P.Value,adj.P.Val,B\n"
        "March2,membrane-associated ring finger (C3HC4) 2,0.973740363,"
        "0.525578157,0.870814186,-5.896065537"
    ),
    (
        "Differentially expressed genes in astrocytes after EOD (p < 0.05) ,,,,,\n"
        "Gene,baseMean,Log2FoldChange,lfcSE,stat,p-value\n"
        "Amotl2,241.5118269,0.426986377,0.079435004,5.375292477,7.65E-08"
    ),
    (
        ",,,,,\n,,,,,\n"
        "Differentially expressed genes in astrocytes after EOD (p < 0.05) ,,,,,\n"
        "Gene,baseMean,Log2FoldChange,lfcSE,stat,p-value\n"
        "Amotl2,241.5118269,0.426986377,0.079435004,5.375292477,7.65E-08"
    ),
    (
        "Differentially expressed ,,,,,\n"
        "genes in astrocytes after EOD (p < 0.05) ,,,,,\n"
        "Gene,baseMean,Log2FoldChange,lfcSE,stat,p-value\n"
        "Amotl2,241.5118269,0.426986377,0.079435004,5.375292477,7.65E-08"
    ),
    (
        "Differentially expressed ,,,,,\n"
        "genes in astrocytes after EOD (p < 0.05) ,,,,,\n"
        "Gene,baseMean,Log2FoldChange,lfcSE,stat,p-value\n"
        "Amotl2,241.5118269,0.426986377,0.079435004,5.375292477,7.65E-08\n"
        "Amotl2,241.5118269,0.426986377,0.079435004,5.375292477,7.65E-08"
    ),
]

EXAMPLE_HEADERS = [
    ["name", "age"],
    [
        "ID",
        "geneSymbol",
        "geneName",
        "illID.Search_Key",
        "illID.ILMN_Gene",
        "illID.Accession",
        "illID.Symbol",
        "illID.Probe_Id",
        "illID.Array_Address_Id",
        "illID.nuID",
        "Fold Change",
        "logFC",
        "AveExpr",
        "t",
        "P.Value",
        "adj.P.Val",
        "B",
    ],
    ["geneSymbol", "geneName", "Fold Change", "P.Value", "adj.P.Val", "B"],
    ["geneSymbol", "geneName", "Fold Change", "P.Value", "adj.P.Val", "B"],
    ["Gene", "baseMean", "Log2FoldChange", "lfcSE", "stat", "p-value"],
    ["Gene", "baseMean", "Log2FoldChange", "lfcSE", "stat", "p-value"],
]

EXAMPLE_HEADER_IDX = [
    0,
    0,
    0,
    1,
    1,
    3,
    2,
]


@pytest.fixture()
def csv_file() -> Path:
    """Create a temporary CSV file."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".csv") as temp:
        yield temp.name
    Path(temp.name).unlink()  # Clean up temporary file


@pytest.mark.parametrize(
    ("csv_content", "expected_header_idx"),
    zip(EXAMPLE_CSV_FILES_WITH_HEADER, EXAMPLE_HEADER_IDX),
)
def test_find_header_with_header(csv_file, csv_content, expected_header_idx):
    """Test finding the header in a CSV file with a header."""
    # Write to the temporary CSV file
    with open(csv_file, "w") as f:
        f.write(csv_content)
    header_found, header_idx = find_header(csv_file)
    assert header_found
    assert header_idx == expected_header_idx


def test_find_header_beyond_max_row(csv_file):
    """Test finding the header in a CSV file with a header beyond the max row."""
    csv_content = (
        ",,,,,\n,,,,,\n,,,,,\n,,,,,\n"
        "Differentially expressed genes in astrocytes after EOD (p < 0.05) ,,,,,\n"
        "Gene,baseMean,Log2FoldChange,lfcSE,stat,p-value\n"
        "Amotl2,241.5118269,0.426986377,0.079435004,5.375292477,7.65E-08"
    )
    # Write to the temporary CSV file
    with open(csv_file, "w") as f:
        f.write(csv_content)
    header_found, header_idx = find_header(csv_file)
    assert header_found is False
    assert header_idx == -1


@pytest.mark.parametrize("csv_content", EXAMPLE_CSV_FILES_WITH_HEADER)
def test_has_header_with_header(csv_file, csv_content):
    """Test checking if a CSV file has a header."""
    # Write to the temporary CSV file
    with open(csv_file, "w") as f:
        f.write(csv_content)
    assert has_header(csv_file)


def test_has_header_without_header(csv_file):
    """Test checking if a CSV file has a header (when there isn't one)."""
    # Write to the temporary CSV file
    with open(csv_file, "w") as f:
        f.write("Alice,20\nBob,30\n")
    assert not has_header(csv_file)


def test_has_header_empty_file(csv_file):
    """Test checking if a CSV file has a header (when it's empty)."""
    assert has_header(csv_file) is False


@pytest.mark.parametrize(
    ("csv_content", "expected_headers"),
    zip(EXAMPLE_CSV_FILES_WITH_HEADER, EXAMPLE_HEADERS),
)
def test_get_headers_with_header(csv_file, csv_content, expected_headers):
    """Test getting the headers from a CSV file with a header."""
    # Write to the temporary CSV file
    with open(csv_file, "w") as f:
        f.write(csv_content)
    assert get_headers(csv_file)[0] == expected_headers


def test_get_headers_without_header(csv_file):
    """Test getting the headers from a CSV file without a header."""
    # Write to the temporary CSV file
    with open(csv_file, "w") as f:
        f.write("Alice,20\nBob,30\n")
    assert get_headers(csv_file)[0] == []


def test_get_headers_empty_file(csv_file):
    """Test getting the headers from an empty CSV file."""
    assert get_headers(csv_file)[0] == []


@pytest.mark.parametrize("csv_content", EXAMPLE_CSV_FILES_WITH_HEADER)
def test_read_row(csv_file, csv_content):
    """Test reading a row from a CSV file."""
    with open(csv_file, "w") as f:
        f.write(csv_content)
    rows = csv_content.split("\n")
    for idx, expected_row in enumerate(rows):
        row = read_row(csv_file, idx)
        assert row == expected_row.split(",")


@pytest.mark.parametrize("csv_content", EXAMPLE_CSV_FILES_WITH_HEADER)
def test_read_row_not_found(csv_file, csv_content):
    """Test reading a row from a CSV file for row that does not exist."""
    with open(csv_file, "w") as f:
        f.write(csv_content)

    rows = csv_content.split("\n")
    idx = len(rows)

    with pytest.raises(ValueError, match="does not contain a row") as e:
        _ = read_row(csv_file, idx)

    assert str(idx) in str(e)


@pytest.mark.parametrize(
    ("csv_content", "expected_header_idx", "expected_header"),
    zip(EXAMPLE_CSV_FILES_WITH_HEADER, EXAMPLE_HEADER_IDX, EXAMPLE_HEADERS),
)
def test_read_to_dict(csv_file, csv_content, expected_header_idx, expected_header):
    """Test reading a CSV file into a list of dictionaries."""
    # Write to the temporary CSV file
    with open(csv_file, "w") as f:
        f.write(csv_content)
    result = read_to_dict(csv_file, expected_header_idx)
    for row in result:
        assert expected_header == list(row.keys())


@pytest.mark.parametrize(
    ("csv_content", "expected_header_idx", "expected_header"),
    zip(EXAMPLE_CSV_FILES_WITH_HEADER, EXAMPLE_HEADER_IDX, EXAMPLE_HEADERS),
)
def test_read_to_dict_out_of_range(
    csv_file, csv_content, expected_header_idx, expected_header
):
    """Test reading a CSV file into a list of dictionaries, when out of range."""
    # Write to the temporary CSV file
    with open(csv_file, "w") as f:
        f.write(csv_content)
    idx = len(csv_content.split("\n"))

    with pytest.raises(ValueError, match="number of rows in the file") as e:
        _ = read_to_dict(csv_file, idx)

    assert "start_row" in str(e)


@pytest.mark.parametrize(
    ("csv_content", "expected_header_idx", "expected_header"),
    zip(EXAMPLE_CSV_FILES_WITH_HEADER, EXAMPLE_HEADER_IDX, EXAMPLE_HEADERS),
)
def test_read_to_dict_n_rows(
    csv_file, csv_content, expected_header_idx, expected_header
):
    """Test reading a CSV file into a list of dictionaries."""
    # Write to the temporary CSV file
    with open(csv_file, "w") as f:
        f.write(csv_content)

    result = read_to_dict_n_rows(csv_file, 1, expected_header_idx)

    assert len(result) == 1

    for row in result:
        assert expected_header == list(row.keys())


@pytest.mark.parametrize(
    ("csv_content", "expected_header_idx", "expected_header"),
    zip(EXAMPLE_CSV_FILES_WITH_HEADER, EXAMPLE_HEADER_IDX, EXAMPLE_HEADERS),
)
def test_read_to_dict_n_rows_no_data(
    csv_file, csv_content, expected_header_idx, expected_header
):
    """Test that an error is raised when no data is found in the CSV file."""
    # Write to the temporary CSV file
    with open(csv_file, "w") as f:
        f.write(csv_content)

    with pytest.raises(EmptyFileError) as e:
        _ = read_to_dict_n_rows(csv_file, 0, expected_header_idx)

    assert "no results" in str(e.value)
    assert csv_file in str(e.value)
