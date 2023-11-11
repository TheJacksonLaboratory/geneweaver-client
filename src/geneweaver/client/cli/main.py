"""The main entrypoint to the GeneWeaver CLI client."""
# ruff: noqa: B008
import pkg_resources
import typer
from geneweaver.client.cli import auth, batch, parser

cli = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")
alpha = typer.Typer(no_args_is_help=True)
beta = typer.Typer(no_args_is_help=True)

ALPHA_HELP_MESSAGE = """
These commands are in alpha testing and are considered [bold]experimental[/bold].

They may be removed or changed in the future [italic bold]without warning[/italic bold],
and have a higher risk of bugs.

:warning: [bold red]Use at your own risk.[/bold red] :warning:
"""

BETA_HELP_MESSAGE = """
These commands are in beta testing.

They are subject to future change and/or removal. Beta commands are
[italic]intended[/italic] to be released beyond beta testing, but may have bugs or other
issues. There is also [bold]no guarantee[/bold] that beta commands will be released
beyond beta testing.

:warning: [bold red]Use at your own risk.[/bold red] :warning:
"""

cli.add_typer(alpha, name="alpha", help=ALPHA_HELP_MESSAGE)
cli.add_typer(beta, name="beta", help=BETA_HELP_MESSAGE)

alpha.add_typer(parser.cli, name="parse")
alpha.add_typer(batch.cli, name="batch")
beta.add_typer(auth.cli, name="auth")


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
