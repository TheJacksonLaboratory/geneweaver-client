"""Test the auth._print_device_code_instructions function."""
from unittest.mock import patch

import pytest
from geneweaver.client.auth import _print_device_code_instructions


@pytest.mark.parametrize(
    "device_code_data",
    [
        {
            "verification_uri_complete": "https://example.com/verify",
            "user_code": "123456",
        },
        {
            "verification_uri_complete": "https://example.org/activate",
            "user_code": "ABCDEF",
        },
        {
            "verification_uri_complete": "https://example.net/confirm",
            "user_code": "abcdef",
        },
        {
            "verification_uri_complete": "https://jacksonlaboratory.auth0.com/verify",
            "user_code": "1a2b3c4d5e6f",
        },
    ],
)
def test_print_device_code_instructions(device_code_data):
    with patch("builtins.print") as mock_print:
        # Call the function with mock data
        _print_device_code_instructions(device_code_data)

        # Assert print was called correctly
        expected_calls = [
            (
                (
                    "1. On your computer or mobile device navigate to: ",
                    device_code_data["verification_uri_complete"],
                ),
            ),
            (("2. Enter the following code: ", device_code_data["user_code"]),),
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)
