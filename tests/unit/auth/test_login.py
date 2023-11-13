"""Test the auth.login function."""

from unittest.mock import MagicMock, patch

from geneweaver.client.auth import login


def test_login():
    with patch(
        "geneweaver.client.auth._get_device_code_data"
    ) as mock_get_device_code_data, patch(
        "geneweaver.client.auth._print_device_code_instructions"
    ) as mock_print_device_code_instructions, patch(
        "geneweaver.client.auth._poll_for_flow_completion"
    ) as mock_poll_for_flow_completion, patch(
        "geneweaver.client.auth.app_dir.save_auth_token"
    ) as mock_save_auth_token:
        # Setup mock return values
        mock_device_code_data = MagicMock(name="device_code_data")
        mock_token_data = MagicMock(name="token_data")

        mock_get_device_code_data.return_value = mock_device_code_data
        mock_poll_for_flow_completion.return_value = mock_token_data

        # Call the login function
        login()

        # Assert that each function is called with the correct arguments
        mock_get_device_code_data.assert_called_once()
        mock_print_device_code_instructions.assert_called_once_with(
            mock_device_code_data
        )
        mock_poll_for_flow_completion.assert_called_once_with(mock_device_code_data)
        mock_save_auth_token.assert_called_once_with(mock_token_data)
