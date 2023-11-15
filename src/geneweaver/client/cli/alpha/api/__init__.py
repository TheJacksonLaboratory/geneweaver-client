"""Root of the alpha api subcommand."""
import typer

HELP_MESSAGE = """
Tools and utilities for interacting with the Geneweaver API.
"""

cli = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")
