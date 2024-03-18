"""Root of the beta cli subcommand."""

import typer
from geneweaver.client.cli.beta import auth

HELP_MESSAGE = """
These commands are in beta testing.

They are subject to future change and/or removal. Beta commands are
[italic]intended[/italic] to be released beyond beta testing, but may have bugs or other
issues. There is also [bold]no guarantee[/bold] that beta commands will be released
beyond beta testing.

:warning: [bold red]Use at your own risk.[/bold red] :warning:
"""

cli = typer.Typer(no_args_is_help=True)

cli.add_typer(auth.cli, name="auth", help=auth.HELP_MESSAGE)
