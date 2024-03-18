"""Authentication CLI commands."""

import typer
from geneweaver.client import auth
from geneweaver.client.auth import get_access_token, get_id_token
from geneweaver.client.exceptions import AuthenticationError

cli = typer.Typer()

HELP_MESSAGE = """
The auth commands allow you to authenticate with the GeneWeaver API.
"""


@cli.command(name="login")
def _login(reauth: bool = typer.Option(False, "--reauth")) -> None:  # noqa: B008
    """Run the device authorization flow.

    :param reauth: Force a re-authentication
    """
    if not reauth and get_access_token():
        print("You are already logged in")
        raise typer.Exit(code=1)

    try:
        auth.login()
    except AuthenticationError as e:
        print(e)
        raise typer.Exit(code=1) from e


@cli.command()
def print_access_token() -> None:
    """Print the current user's access token."""
    print(get_access_token())


@cli.command()
def print_identity_token() -> None:
    """Print the current user's identity token."""
    print(get_id_token())
