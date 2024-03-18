"""Root command for the parse cli subcommand."""

import typer
from geneweaver.client.cli.alpha.parse import utils

from .convert import convert

HELP_MESSAGE = """
Tools and utilities to parse data files for use in Geneweaver.

The parse commands help to transform data files in various formats into data files that
can be uploaded to Geneweaver.
"""

cli = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")

cli.add_typer(utils.cli, name="utils")

cli.command()(convert)
cli.command(name="cn", help="Alias for `convert` command.")(convert)
