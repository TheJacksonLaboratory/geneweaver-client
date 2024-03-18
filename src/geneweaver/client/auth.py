"""Authentication code for the GeneWeaver client."""

import time
from typing import Any, Dict, Optional

import jwt
import requests
from auth0.authentication.token_verifier import (
    AsymmetricSignatureVerifier,
    TokenVerifier,
)
from geneweaver.client.core import app_dir
from geneweaver.client.core.config import settings
from geneweaver.client.exceptions import AuthenticationError


def login() -> None:
    """Run the device authorization flow."""
    device_code_data = _get_device_code_data()
    _print_device_code_instructions(device_code_data)
    token_data = _poll_for_flow_completion(device_code_data)
    app_dir.save_auth_token(token_data)


def get_id_token() -> Optional[str]:
    """Get the ID token from the authentication token file.

    :returns: The ID token.
    """
    return _get_token_data_value_or_none("id_token")


def get_access_token() -> Optional[str]:
    """Get the Access token from the authentication token file.

    :returns: The ID token.
    """
    token = _get_token_data_value_or_none("access_token")
    if access_token_expired(token):
        refresh_token()
        token = _get_token_data_value_or_none("access_token")
    return token


def _get_token_data_value_or_none(token_data_key: str) -> Optional[str]:
    token_data = app_dir.get_auth_token()

    if token_data is None:
        return None

    return token_data.get(token_data_key)


def validate_token(token: str) -> None:
    """Verify the token and its precedence.

    :param token:
    """
    jwks_url = "https://{}/.well-known/jwks.json".format(settings.AUTH_DOMAIN)
    issuer = "https://{}/".format(settings.AUTH_DOMAIN)
    sv = AsymmetricSignatureVerifier(jwks_url)
    tv = TokenVerifier(
        signature_verifier=sv, issuer=issuer, audience=settings.AUTH_CLIENT_ID
    )
    tv.verify(token)


def access_token_expired(access_token: str) -> bool:
    """Check if the access token is unexpired."""
    token_data = app_dir.get_auth_token()
    try:
        jwt.decode(
            token_data["access_token"],
            algorithms=settings.AUTH_ALGORITHMS,
            options={"verify_signature": False},
        )
        return False
    except jwt.ExpiredSignatureError:
        return True


def refresh_token() -> None:
    """Refresh the access token."""
    token_data = app_dir.get_auth_token()
    refresh_token = token_data["refresh_token"]
    payload = {
        "grant_type": "refresh_token",
        "client_id": settings.AUTH_CLIENT_ID,
        "refresh_token": refresh_token,
    }
    response = requests.post(
        "https://{}/oauth/token".format(settings.AUTH_DOMAIN), data=payload
    )
    token_data = response.json()
    token_data["refresh_token"] = app_dir.get_auth_token()["refresh_token"]
    app_dir.save_auth_token(token_data)


def current_user(id_token: str) -> Dict[str, str]:
    """Get the current user from the ID token."""
    return jwt.decode(
        id_token,
        algorithms=settings.AUTH_ALGORITHMS,
        options={"verify_signature": False},
    )


def _device_code_payload() -> Dict[str, str]:
    return {
        "client_id": settings.AUTH_CLIENT_ID,
        "scope": " ".join(settings.AUTH_SCOPES),
    }


def _get_device_code_data() -> dict:
    device_code_response = requests.post(
        "https://{}/oauth/device/code".format(settings.AUTH_DOMAIN),
        data=_device_code_payload(),
    )

    if device_code_response.status_code != 200:
        raise AuthenticationError("Error generating the device code")

    return device_code_response.json()


def _print_device_code_instructions(device_code_data: Dict[str, Any]) -> None:
    print(
        "1. On your computer or mobile device navigate to: ",
        device_code_data["verification_uri_complete"],
    )
    print("2. Enter the following code: ", device_code_data["user_code"])


def _token_payload(device_code: str) -> Dict[str, str]:
    return {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": device_code,
        "scope": "offline_access",
        "client_id": settings.AUTH_CLIENT_ID,
    }


def _poll_for_flow_completion(
    device_code_data: Dict[str, Any]
) -> Optional[Dict[str, any]]:
    authenticated = False
    token_data = None
    while not authenticated:
        token_response = requests.post(
            "https://{}/oauth/token".format(settings.AUTH_DOMAIN),
            data=_token_payload(device_code_data["device_code"]),
        )

        token_data = token_response.json()
        if token_response.status_code == 200:
            print("Authenticated!")
            print("- Id Token: {}...".format(token_data["id_token"][:10]))
            validate_token(token_data["id_token"])
            authenticated = True
        elif token_data["error"] not in ("authorization_pending", "slow_down"):
            raise AuthenticationError(token_data["error_description"])
        else:
            time.sleep(device_code_data["interval"])

    return token_data
