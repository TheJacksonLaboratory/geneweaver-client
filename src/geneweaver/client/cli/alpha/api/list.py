"""Module containing the CLI for the API subcommand."""

import typer

cli = typer.Typer()


@cli.command()
def geneset() -> None:
    """Get a geneset by ID."""
    print("Test")
