"""Unit tests for the read_pandas method of the BaseDataset class."""

from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest
from geneweaver.client.datasets.base import BaseDataset


# Parametrize test cases
@pytest.mark.parametrize(
    ("skiprows", "file_extension"),
    [
        (0, "csv"),
        (1, "json"),
        # You can add more combinations of skiprows and file extensions
    ],
)
def test_read_pandas(skiprows, file_extension):
    """Test the read_pandas method in BaseDataset with mocks."""
    with patch(
        "geneweaver.client.datasets.base.pd.read_excel"
    ) as mock_read_excel, patch(
        "geneweaver.client.datasets.base.pd.read_csv"
    ) as mock_read_csv, patch(
        "geneweaver.client.datasets.base.pd.read_json"
    ) as mock_read_json:
        # Set up a mock DataFrame to be returned by the read functions
        mock_df = pd.DataFrame({"col1": [1, 2, 3]})
        if file_extension == "xlsx":
            mock_read_function = mock_read_excel
        elif file_extension == "csv":
            mock_read_function = mock_read_csv
        elif file_extension == "json":
            mock_read_function = mock_read_json
        mock_read_function.return_value = mock_df

        # Instantiate BaseDataset and configure it
        base_dataset = BaseDataset("test_data")
        base_dataset.DS_FOLDER = "ds_folder"
        base_dataset.UNZIPPED_LOC = f"file.{file_extension}"
        base_dataset.dataset_skip_rows = skiprows

        # Depending on file_extension, set the appropriate read function
        base_dataset._pandas_read_f = getattr(pd, f"read_{file_extension}")

        # Call read_pandas method
        base_dataset.read_pandas()

        # Check if the read function was called correctly
        dataset_path = Path("test_data/ds_folder") / f"file.{file_extension}"
        mock_read_function.assert_called_once_with(dataset_path, skiprows=skiprows)

        # Assert the DataFrame is set correctly
        assert base_dataset._pandas_df.equals(mock_df)
