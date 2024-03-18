"""Root of the alpha cli subcommand."""

import typer
from geneweaver.client.cli.alpha import api, datasets, parse

HELP_MESSAGE = """
These commands are in alpha testing and are considered [bold]experimental[/bold].

They may be removed or changed in the future [italic bold]without warning[/italic bold],
and have a higher risk of bugs.

Alpha commands do not have the same level of testing requirements
as the rest of the CLI, and [bold underline magenta]may break or change in unexpected \
ways[/bold underline magenta].

:warning: [bold red]Use at your own risk.[/bold red] :warning:
"""

cli = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")

cli.add_typer(parse.cli, name="parse", help=parse.HELP_MESSAGE)
cli.add_typer(api.cli, name="api", help=api.HELP_MESSAGE)
cli.add_typer(datasets.cli, name="datasets", help=datasets.HELP_MESSAGE)
