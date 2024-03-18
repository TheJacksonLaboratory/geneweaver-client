"""Root of the alpha api subcommand."""

import typer
from geneweaver.client.cli.alpha.api import genes, genesets

HELP_MESSAGE = """
Tools and utilities for interacting with the Geneweaver API.
"""

cli = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")
cli.add_typer(genesets.cli, name="genesets", help=genesets.HELP_MESSAGE)
cli.add_typer(genes.cli, name="genes", help=genes.HELP_MESSAGE)
