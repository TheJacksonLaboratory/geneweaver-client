"""Base class for all datasets."""

import io
import zipfile
from pathlib import Path

import pandas as pd
import requests


class BaseDataset:
    """Base class for all datasets."""

    URL = None
    DS_FOLDER = None
    UNZIPPED_LOC = None

    def __init__(self, base_folder: str = "data") -> None:
        """Initialize the BaseDataset."""
        self.base_folder = Path(base_folder)
        self.dataset_skip_rows = 0
        self._pandas_df = None
        self._pandas_read_f = pd.read_excel

    @property
    def dataset_path(self) -> Path:
        """Return the dataset's path."""
        return self.base_folder / self.DS_FOLDER / self.UNZIPPED_LOC

    def download_zip_file(self, redownload: bool = False) -> None:
        """Download the zip file from the dataset's URL."""
        if not redownload and self.dataset_path.is_file():
            return None

        response = requests.get(self.URL)
        response.raise_for_status()

        z = zipfile.ZipFile(io.BytesIO(response.content))

        z.extractall(self.base_folder / self.DS_FOLDER)

    def as_pandas(self) -> pd.DataFrame:
        """Return the dataset as a Pandas DataFrame."""
        if self._pandas_df is None:
            self.read_pandas()
        return self._pandas_df

    def read_pandas(self) -> None:
        """Read the dataset into a Pandas DataFrame."""
        self._pandas_df = self._pandas_read_f(
            self.dataset_path, skiprows=self.dataset_skip_rows
        )
