"""Unit tests for the auth.get_id_token function."""

from unittest.mock import patch

import pytest
from geneweaver.client.auth import get_id_token


@pytest.mark.parametrize(
    "token_data",
    [
        {"access_token": "mock_access_token"},
        {"access_token": "mock_access_token", "other_key": "other_value"},
        {"other_key": "other_value"},
        None,
    ],
)
def test_get_id_token(token_data):
    """Test the auth.get_id_token function using mocks."""
    with patch(
        "geneweaver.client.auth._get_token_data_value_or_none"
    ) as mock_get_token_data:
        # Mock return value for _get_token_data_value_or_none
        mock_get_token_data.return_value = token_data

        # Call get_id_token and assert its return value
        result = get_id_token()
        assert result == token_data

        # Assert _get_token_data_value_or_none was called correctly
        mock_get_token_data.assert_called_once_with("id_token")
