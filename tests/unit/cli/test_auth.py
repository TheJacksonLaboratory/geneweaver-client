"""Tests for the auth CLI command."""

from unittest.mock import patch

import pytest
from geneweaver.client.cli.beta.auth import AuthenticationError, cli
from typer.testing import CliRunner

runner = CliRunner()


@pytest.mark.parametrize(
    ("reauth", "auth_token_exists", "raises_auth_error"),
    [
        (False, True, False),  # Already logged in, no reauth
        (False, False, False),  # Not logged in, no reauth, successful login
        (True, False, False),  # Not logged in, reauth, successful login
        (True, True, False),  # Already logged in, reauth, successful login
        (False, False, True),  # Not logged in, no reauth, login error
    ],
)
def test_login(reauth, auth_token_exists, raises_auth_error):
    """Test the login CLI command under various scenarios."""
    with patch("geneweaver.client.auth.login") as mock_login, patch(
        "geneweaver.client.cli.beta.auth.get_access_token",
        return_value=auth_token_exists,
    ), patch("builtins.print") as mock_print:
        auth_error = AuthenticationError("Login error")
        if raises_auth_error:
            mock_login.side_effect = auth_error

        inputs = ["login"]
        if reauth:
            inputs.append("--reauth")

        result = runner.invoke(cli, inputs)

        if not reauth and auth_token_exists:
            assert result.exit_code == 1, result.output
            mock_print.assert_called_once()
        elif raises_auth_error:
            assert result.exit_code == 1, result.output
            mock_print.assert_called_once_with(auth_error)
        else:
            assert result.exit_code == 0, result.output
            mock_login.assert_called_once()


def test_print_identity_token():
    """Test the print_identity_token CLI command."""
    with patch("geneweaver.client.cli.beta.auth.get_id_token") as mock_get_id_token:
        mock_get_id_token.return_value = "id_token"
        result = runner.invoke(cli, ["print-identity-token"])
        assert result.exit_code == 0, result.output
        mock_get_id_token.assert_called_once()
        assert result.output == "id_token\n"


def test_print_access_token():
    """Test the print_access_token CLI command."""
    with patch(
        "geneweaver.client.cli.beta.auth.get_access_token"
    ) as mock_get_access_token:
        mock_get_access_token.return_value = "access_token"
        result = runner.invoke(cli, ["print-access-token"])
        assert result.exit_code == 0, result.output
        mock_get_access_token.assert_called_once()
        assert result.output == "access_token\n"
