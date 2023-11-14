"""Test the dataset_path property of the BaseDataset class."""
from pathlib import Path

from geneweaver.client.datasets.base import BaseDataset


def test_base_dataset_path():
    """Test the dataset_path property."""
    base_dataset = BaseDataset("test_data")
    base_dataset.DS_FOLDER = "ds_folder"
    base_dataset.UNZIPPED_LOC = "unzipped_loc"
    expected_path = Path("test_data/ds_folder/unzipped_loc")
    assert base_dataset.dataset_path == expected_path
