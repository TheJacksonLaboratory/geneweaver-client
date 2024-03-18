"""Root of the alpha datasets subcommand."""

import typer

HELP_MESSAGE = """
Tools and utilities for interacting with the Geneweaver Client datasets.

These datasets are available to help you get started with Geneweaver, and do not reflect
 the full collection of available datasets.
"""

cli = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")
