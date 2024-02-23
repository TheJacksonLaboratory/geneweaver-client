"""Test the auth._token_payload function."""
from unittest.mock import patch

import pytest
from geneweaver.client.auth import _token_payload


# Parametrize test cases with different device codes
@pytest.mark.parametrize(
    "device_code",
    [
        "code123",
        "abc456",
        "def789",
        "ghi012",
        "jkl345",
        "mno678",
        "pqr901",
        "Do-re-mi" "abc-123",
        "you-and-me",
    ],
)
def test_token_payload(device_code):
    """Test the private _token_payload function using mocks."""
    with patch("geneweaver.client.auth.settings.AUTH_CLIENT_ID", "mock_client_id"):
        # Expected output based on the device_code and mocked settings
        expected_payload = {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code,
            "client_id": "mock_client_id",
            "scope": "offline_access",
        }

        # Call the function and assert its return value
        assert _token_payload(device_code) == expected_payload
