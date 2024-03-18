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
@patch("geneweaver.client.auth._get_token_data_value_or_none")
@patch("geneweaver.client.auth.access_token_expired")
@patch("geneweaver.client.auth.refresh_token")
def test_get_access_token(mock_refresh, mock_expired, mock_get_token, token_data):
    """Test the get_access_token function with mock data."""
    mock_expired.return_value = False
    mock_get_token.side_effect = [token_data, token_data]
    mock_refresh.return_value = None

    # Call get_access_token and assert its return value
    result = get_access_token()
    assert result == token_data

    # Assert _get_token_data_value_or_none was called correctly
    assert mock_get_token.call_count == 1
    # Assert access_token_expired was called correctly
    assert mock_expired.call_count == 1
    # Refresh token should not be called
    assert mock_refresh.call_count == 0


@pytest.mark.parametrize(
    "token_data",
    [
        {"access_token": "mock_access_token"},
        {"access_token": "mock_access_token", "other_key": "other_value"},
        {"other_key": "other_value"},
        None,
    ],
)
@patch("geneweaver.client.auth._get_token_data_value_or_none")
@patch("geneweaver.client.auth.access_token_expired")
@patch("geneweaver.client.auth.refresh_token")
def test_get_access_token_expired(
    mock_refresh, mock_expired, mock_get_token, token_data
):
    """Test the get_access_token function with mock data."""
    mock_expired.return_value = True
    mock_get_token.side_effect = [token_data, token_data]
    mock_refresh.return_value = None

    # Mock return value for _get_token_data_value_or_none
    mock_expired.return_value = True
    mock_get_token.side_effect = [token_data, token_data]

    # Call get_access_token and assert its return value
    result = get_access_token()
    assert result == token_data

    # Assert _get_token_data_value_or_none was called correctly
    assert mock_get_token.call_count == 2
    # Assert access_token_expired was called correctly
    assert mock_expired.call_count == 1
    # Refresh token should be called
    assert mock_refresh.call_count == 1
