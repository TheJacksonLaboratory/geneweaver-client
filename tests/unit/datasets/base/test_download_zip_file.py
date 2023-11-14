"""Test the download_zip_file method in BaseDataset."""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from geneweaver.client.datasets.base import BaseDataset
from requests.exceptions import HTTPError


@pytest.mark.parametrize(
    ("file_exists", "redownload", "http_status", "raises_exception"),
    [
        (True, False, 200, False),  # File exists, no redownload
        (False, False, 200, False),  # File does not exist, download it
        (False, True, 200, False),  # Redownload even if file exists
        (False, False, 404, True),  # File does not exist, HTTP request fails
        (False, False, 500, True),  # File does not exist, HTTP request fails
    ],
)
def test_download_zip_file(file_exists, redownload, http_status, raises_exception):
    """Test the download_zip_file method in BaseDataset with mocks."""
    with patch("geneweaver.client.datasets.base.requests.get") as mock_get, patch(
        "geneweaver.client.datasets.base.zipfile.ZipFile"
    ), patch.object(Path, "is_file", return_value=file_exists):
        # Configure the mock response for requests.get
        mock_response = MagicMock()
        mock_response.status_code = http_status
        if http_status == 200:
            mock_response.content = b"Mock content"
        else:
            mock_response.raise_for_status.side_effect = HTTPError("Mock exception")
        mock_get.return_value = mock_response

        # Instantiate BaseDataset
        base_dataset = BaseDataset("test_data")
        base_dataset.URL = "http://example.com/data.zip"
        base_dataset.DS_FOLDER = "ds_folder"
        base_dataset.UNZIPPED_LOC = "unzipped_loc"

        # Test download_zip_file
        if raises_exception:
            with pytest.raises(
                HTTPError
            ):  # Replace with specific exception if applicable
                base_dataset.download_zip_file(redownload=redownload)
        else:
            base_dataset.download_zip_file(redownload=redownload)
