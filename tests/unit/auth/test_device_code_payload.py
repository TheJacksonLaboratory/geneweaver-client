"""Test the auth._device_code_payload function."""

from unittest.mock import patch

from geneweaver.client.auth import (
    _device_code_payload,
)


def test_device_code_payload():
    """Test the _device_code_payload function with mock data."""
    # Mock settings
    with patch(
        "geneweaver.client.auth.settings.AUTH_CLIENT_ID", "mock_client_id"
    ), patch("geneweaver.client.auth.settings.AUTH_SCOPES", ["scope1", "scope2"]):
        expected_payload = {"client_id": "mock_client_id", "scope": "scope1 scope2"}
        # Call the function and assert its return value
        assert _device_code_payload() == expected_payload
