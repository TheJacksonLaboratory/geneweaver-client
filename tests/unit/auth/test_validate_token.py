"""Test the auth.validate_token function."""

from unittest.mock import MagicMock, patch

import pytest
from auth0.authentication.token_verifier import (
    TokenValidationError,
)
from geneweaver.client.auth import validate_token


@pytest.mark.parametrize(
    "example_token",
    [
        "valid_token",
        "invalid_token",
        "",
        None,
        MagicMock(),
        123,
        {"token": "valid_token"},
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikpva"
        "G4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
    ],
)
@pytest.mark.parametrize("valid_token", [True, False])
def test_validate_token(example_token, valid_token):
    """Test token validation using mocks."""
    with patch(
        "geneweaver.client.auth.settings.AUTH_DOMAIN", "mock_auth_domain"
    ), patch("geneweaver.client.auth.AsymmetricSignatureVerifier"), patch(
        "geneweaver.client.auth.TokenVerifier"
    ) as mock_tv_class:
        # Mock instances of AsymmetricSignatureVerifier and TokenVerifier
        mock_tv = mock_tv_class.return_value

        # Configure TokenVerifier's verify method to raise an exception for invalid
        # tokens
        if not valid_token:
            mock_tv.verify.side_effect = TokenValidationError("Invalid token")

        # Test the validate_token function
        if valid_token:
            validate_token(example_token)  # Should not raise an exception
        else:
            with pytest.raises(TokenValidationError):
                validate_token(example_token)
