"""Unit tests for the auth._get_device_code_data function."""

from unittest.mock import MagicMock, patch

import pytest
from geneweaver.client.auth import (
    AuthenticationError,
    _get_device_code_data,
)


@pytest.mark.parametrize(
    ("status_code", "response_data", "expected_output", "raises_exception"),
    [
        (
            200,
            {"device_code": "123", "user_code": "abc"},
            {"device_code": "123", "user_code": "abc"},
            False,
        ),
        (
            200,
            {
                "device_code": "123",
                "user_code": "abc",
                "verification_uri": "https://example.com",
            },
            {
                "device_code": "123",
                "user_code": "abc",
                "verification_uri": "https://example.com",
            },
            False,
        ),
        (400, None, None, True),
        (400, {"error": "Error!"}, {"error": "Error!"}, True),
        (401, None, None, True),
        (401, {"error": "Other Error!"}, {"error": "Other Error!"}, True),
        (500, None, None, True),
        (500, {"error": "Another Error!"}, {"error": "Another Error!"}, True),
    ],
)
def test_get_device_code_data(
    status_code, response_data, expected_output, raises_exception
):
    with patch("geneweaver.client.auth.requests.post") as mock_post, patch(
        "geneweaver.client.auth._device_code_payload", return_value={"mock": "payload"}
    ):
        # Configure the mock response
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.json.return_value = response_data
        mock_post.return_value = mock_response

        # Execute the test
        if raises_exception:
            with pytest.raises(AuthenticationError):
                _get_device_code_data()
        else:
            result = _get_device_code_data()
            assert result == expected_output
