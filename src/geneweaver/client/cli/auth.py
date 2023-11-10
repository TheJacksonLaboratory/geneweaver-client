"""Authentication CLI commands."""
import typer
from geneweaver.client import auth
from geneweaver.client.exceptions import AuthenticationError
from geneweaver.client.user_config import get_auth_token

cli = typer.Typer()


@cli.command()
def login(reauth: bool = typer.Option(False, "--reauth")) -> None:
    """Runs the device authorization flow.

    :param reauth: Force a re-authentication
    """
    if not reauth and get_auth_token():
        print("You are already logged in")
        raise typer.Exit(code=1)

    try:
        auth.login()
    except AuthenticationError as e:
        print(e)
        raise typer.Exit(code=1)
