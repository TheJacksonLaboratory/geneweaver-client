"""The main entrypoint to the GeneWeaver CLI client."""

# ruff: noqa: B008
import pkg_resources
import typer
from geneweaver.client.cli import alpha, beta

cli = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")

cli.add_typer(alpha.cli, name="alpha", help=alpha.HELP_MESSAGE)
cli.add_typer(beta.cli, name="beta", help=beta.HELP_MESSAGE)


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
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress all output."),
    pretty: bool = typer.Option(
        False, "--pretty", "-p", help="Pretty print data output."
    ),
) -> None:
    """GeneWeaver CLI client."""
    ctx.obj = {"quiet": quiet, "pretty": pretty}
