"""Code to interact with user configuration and state."""

import json
from pathlib import Path
from typing import Optional

import typer


def get_config_dir() -> Path:
    """Get the path to the configuration directory.

    :returns: The path to the configuration directory.
    """
    return Path(typer.get_app_dir("gweave"))


def get_config_file() -> Path:
    """Get the path to the configuration file.

    :returns: The path to the configuration file.
    """
    return get_config_dir() / "config.json"


def get_auth_token_file() -> Path:
    """Get the path to the authentication token file.

    :returns: The path to the authentication token file.
    """
    return get_config_dir() / "auth_token.json"


def get_auth_token() -> Optional[dict]:
    """Get the authentication token data from the authentication token file.

    :returns: The authentication token.
    """
    auth_token_file = get_auth_token_file()

    if not auth_token_file.is_file():
        return None

    with open(auth_token_file, "r") as f:
        token = json.load(f)

    return token


def save_auth_token(token: dict) -> None:
    """Save the authentication token to the authentication token file.

    :param token: The authentication token.
    """
    auth_token_file = get_auth_token_file()
    auth_token_file.parent.mkdir(parents=True, exist_ok=True)

    with open(auth_token_file, "w") as f:
        json.dump(token, f)
