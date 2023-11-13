"""Unit tests for the get_access_token function in the auth module."""
from unittest.mock import patch

import pytest
from geneweaver.client.auth import get_access_token


@pytest.mark.parametrize(
    "token_data",
    [
        {"access_token": "mock_access_token"},
        {"access_token": "mock_access_token", "other_key": "other_value"},
        {"other_key": "other_value"},
        None,
    ],
)
def test_get_access_token(token_data):
    """Test the get_access_token function with mock data."""
    with patch(
        "geneweaver.client.auth._get_token_data_value_or_none"
    ) as mock_get_token_data:
        # Mock return value for _get_token_data_value_or_none
        mock_get_token_data.return_value = token_data

        # Call get_access_token and assert its return value
        result = get_access_token()
        assert result == token_data

        # Assert _get_token_data_value_or_none was called correctly
        mock_get_token_data.assert_called_once_with("access_token")
