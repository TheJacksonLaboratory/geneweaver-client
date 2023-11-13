"""Test the auth.current_user function."""

from unittest.mock import patch

import pytest
from geneweaver.client.auth import (
    current_user,
)


@pytest.mark.parametrize(
    "mock_id_token",
    [
        "mock_id_token",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikpva"
        "G4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikpva"
        "G4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.cThIIoDvwdueQB468K5xDc5633seEFoqwxjF_xSJyQQ",
    ],
)
@pytest.mark.parametrize("auth_algorithms", [["HS256"], ["RS256"], ["HS256", "RS256"]])
@pytest.mark.parametrize(
    "expected_user",
    [
        ({"username": "user1", "email": "user1@example.com"}),
        (
            {
                "username": "user2",
                "email": "user2@example.com",
                "additional_field": "extra_data",
            }
        ),
        ({"username": "user3", "email": "user3@jax.org"}),
        ({"username": "user.dot", "email": "user.dot@jax.org"}),
        ({"username": "user.dot", "email": "user.dot@example.com"}),
    ],
)
def test_current_user_mock(expected_user, auth_algorithms, mock_id_token):
    # Mock jwt.decode and settings.AUTH_ALGORITHMS
    with patch("geneweaver.client.auth.jwt.decode") as mock_jwt_decode, patch(
        "geneweaver.client.auth.settings.AUTH_ALGORITHMS", auth_algorithms
    ):
        # Set the return value of jwt.decode to the expected user for this test
        # iteration
        mock_jwt_decode.return_value = expected_user

        # Call current_user with a mock token
        result = current_user(mock_id_token)

        # Assertions
        mock_jwt_decode.assert_called_once_with(
            mock_id_token,
            algorithms=auth_algorithms,
            options={"verify_signature": False},
        )
        assert result == expected_user


@pytest.mark.parametrize(
    ("mock_id_token", "example_user"),
    [
        (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6I"
            "kpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.cThIIoDvwdueQB468K5xDc5633seEFoqwxjF"
            "_xSJyQQ",
            {"sub": "1234567890", "name": "John Doe", "iat": 1516239022},
        ),
        (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6I"
            "kphbmUgRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.cMErWtEf7DxCXJl8C9q0L7ttkm-Ex54UWHsO"
            "CMGbtUc",
            {"sub": "1234567890", "name": "Jane Doe", "iat": 1516239022},
        ),
        (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6I"
            "kphbmUgRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.HI_rCMev2MLeWKzMa1reAEjNqMeaRjVG_vF6"
            "ViHXBg0",
            {"sub": "1234567890", "name": "Jane Doe", "iat": 1516239022},
        ),
        (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6I"
            "kV1Y2xpZGVzIFJ1cGVydG8iLCJpYXQiOjE1MTYyMzkxNDV9.GC_-79SIvKDsEnZLs6jTSBipZr"
            "ADQbWmOtPS7c_AvSI",
            {"sub": "1234567890", "name": "Euclides Ruperto", "iat": 1516239145},
        ),
        (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdXRoMHw5ODc1NzM4IiwibmFtZ"
            "SI6IkNhc2UgVmFyc2hhIiwiaWF0IjoxNTE2MjQ5MTQ1fQ.lnW_2-Dy36_XV8lpVekYb8YPbRMf"
            "NBFhMk0p5InHEcg",
            {"sub": "auth0|9875738", "name": "Case Varsha", "iat": 1516249145},
        ),
    ],
)
def test_current_user_decode(mock_id_token, example_user):
    # Call current_user with the example token
    result = current_user(mock_id_token)

    assert result == example_user
