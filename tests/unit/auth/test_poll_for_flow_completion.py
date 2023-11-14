"""Test the auth._poll_for_flow_completion function."""
from unittest.mock import MagicMock, patch

import pytest
from geneweaver.client.auth import AuthenticationError, _poll_for_flow_completion


@pytest.mark.parametrize(
    (
        "token_response_data",
        "status_code",
        "error_key",
        "expected_result",
        "raises_exception",
    ),
    [
        ({"id_token": "id_token_123"}, 200, None, {"id_token": "id_token_123"}, False),
        (
            {"error_description": "Error occurred", "error": "invalid_request"},
            400,
            "invalid_request",
            None,
            True,
        ),
        (
            {"error_description": "Error occurred", "error": "invalid_request"},
            500,
            "invalid_request",
            None,
            True,
        ),
        (
            {"error_description": "Error occurred", "error": "other_error"},
            401,
            "other_error",
            None,
            True,
        ),
    ],
)
def test_poll_for_flow_completion(
    token_response_data, status_code, error_key, expected_result, raises_exception
):
    """Test the _poll_for_flow_completion function using mocks."""
    device_code_data = {"device_code": "device_code_123", "interval": 5}

    with patch("geneweaver.client.auth.requests.post") as mock_post, patch(
        "geneweaver.client.auth._token_payload", return_value={}
    ), patch("geneweaver.client.auth.print"), patch(
        "geneweaver.client.auth.validate_token"
    ), patch(
        "geneweaver.client.auth.time.sleep"
    ):
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.json.return_value = token_response_data
        mock_post.return_value = mock_response

        # Check for exception or return value
        if raises_exception:
            with pytest.raises(AuthenticationError):
                _poll_for_flow_completion(device_code_data)
        else:
            result = _poll_for_flow_completion(device_code_data)
            assert result == expected_result


@pytest.mark.parametrize(
    (
        "token_response_data",
        "status_code",
        "sleep_calls",
        "expected_sleep_arg",
    ),
    [
        # Case for authorization pending or slow down
        (
            {"error": "authorization_pending", "error_description": "pending"},
            400,
            1,
            5,
        ),
        ({"error": "slow_down", "error_description": "pending"}, 400, 1, 5),
        # Case for invalid request
        (
            {"error": "invalid_request", "error_description": "invalid"},
            400,
            0,
            None,
        ),
        # Case for other errors
        ({"error": "other_error", "error_description": "other"}, 400, 0, None),
    ],
)
def test_poll_for_flow_completion_sleep(
    token_response_data, status_code, sleep_calls, expected_sleep_arg
):
    """Test the _poll_for_flow_completion function using mocks."""
    device_code_data = {
        "device_code": "device_code_123",
        "interval": expected_sleep_arg,
    }

    with patch("geneweaver.client.auth.requests.post") as mock_post, patch(
        "geneweaver.client.auth._token_payload", return_value={}
    ), patch("geneweaver.client.auth.print"), patch(
        "geneweaver.client.auth.validate_token"
    ), patch(
        "geneweaver.client.auth.time.sleep"
    ) as mock_sleep:
        # Configure mock response for the first and second call
        first_response = MagicMock()
        first_response.status_code = status_code
        first_response.json.return_value = token_response_data
        second_response = MagicMock()
        second_response.status_code = 200
        second_expected_result = {"id_token": "123"}
        second_response.json.return_value = second_expected_result

        mock_post.side_effect = [first_response, second_response]

        # Call the function
        if token_response_data["error"] not in ("authorization_pending", "slow_down"):
            with pytest.raises(AuthenticationError):
                _poll_for_flow_completion(device_code_data)
        else:
            result = _poll_for_flow_completion(device_code_data)

            # Assert time.sleep was called with the correct interval
            assert mock_sleep.call_count == sleep_calls
            mock_sleep.assert_called_with(expected_sleep_arg)

            # Assert the final result
            assert result == second_expected_result
