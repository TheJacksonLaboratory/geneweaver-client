"""Test the auth._get_token_data_value_or_none function."""

from unittest.mock import patch

import pytest
from geneweaver.client.auth import _get_token_data_value_or_none


@pytest.mark.parametrize(
    ("token_data", "token_data_key", "expected_result"),
    [
        ({"key1": "value1", "key2": "value2"}, "key1", "value1"),
        ({"key1": "value1", "key2": "value2"}, "key3", None),
        (None, "key1", None),
    ],
)
def test_get_token_data_value_or_none(token_data, token_data_key, expected_result):
    """Test the _get_token_data_value_or_none function."""
    with patch(
        "geneweaver.client.auth.app_dir.get_auth_token", return_value=token_data
    ):
        # Call the function and assert its return value
        result = _get_token_data_value_or_none(token_data_key)
        assert result == expected_result
