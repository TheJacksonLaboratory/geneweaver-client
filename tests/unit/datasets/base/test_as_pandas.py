"""Test the BaseDataset as_pandas method."""

from unittest.mock import patch

import pandas as pd
import pytest
from geneweaver.client.datasets.base import BaseDataset


@pytest.mark.parametrize("initial_df_exists", [True, False])
def test_as_pandas(initial_df_exists):
    """Test the as_pandas method in BaseDataset with patch/mock."""
    with patch.object(BaseDataset, "read_pandas") as mock_read_pandas:
        # Create an instance of BaseDataset
        base_dataset = BaseDataset("test_data")

        # Set _pandas_df based on the parametrization
        if initial_df_exists:
            mock_df = pd.DataFrame({"col1": [1, 2, 3]})
            base_dataset._pandas_df = mock_df
        else:
            mock_df = None
            base_dataset._pandas_df = mock_df

        # Call as_pandas method
        result_df = base_dataset.as_pandas()

        # Check if read_pandas was called
        if not initial_df_exists:
            mock_read_pandas.assert_called_once()
        else:
            mock_read_pandas.assert_not_called()

        # Assert the returned DataFrame
        if initial_df_exists:
            assert result_df.equals(mock_df)
