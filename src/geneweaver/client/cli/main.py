"""The main entrypoint to the GeneWeaver CLI client."""
# ruff: noqa: B008
import pkg_resources
import typer

from geneweaver.client.cli import parser
from geneweaver.client.cli import auth
from geneweaver.client.cli import batch

cli = typer.Typer(no_args_is_help=True)
cli.add_typer(parser.cli, name="parse")
cli.add_typer(auth.cli, name="auth")
cli.add_typer(batch.cli, name="batch")


def version_callback(version: bool) -> None:
    """Print the version of the GeneWeaver CLI client."""
    if version:
        version = pkg_resources.get_distribution("geneweaver-client").version
        typer.echo(f"GeneWeaver CLI client (gweave) version: {version}")
        raise typer.Exit(code=0)


@cli.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),
) -> None:
    """GeneWeaver CLI client."""
    pass
