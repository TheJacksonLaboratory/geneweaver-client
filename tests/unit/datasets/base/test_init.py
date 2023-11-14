"""Tests for the BaseDataset class init method."""
from pathlib import Path

import pandas as pd
from geneweaver.client.datasets.base import BaseDataset


def test_base_dataset_init():
    """Test the BaseDataset class init method."""
    base_dataset = BaseDataset("test_data")
    assert base_dataset.base_folder == Path("test_data")
    assert base_dataset.dataset_skip_rows == 0
    assert base_dataset._pandas_df is None
    assert base_dataset._pandas_read_f == pd.read_excel
