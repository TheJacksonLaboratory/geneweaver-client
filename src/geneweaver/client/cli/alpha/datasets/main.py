"""Module containing the CLI for the datasets subcommand."""

import typer

cli = typer.Typer()


@cli.command(name="list")
def _list() -> None:
    """List all available datasets."""
    print("- DNACombinedaCGHGeneSummary")


@cli.command()
def downloaded() -> None:
    """List downloaded datasets."""
    print("- DNACombinedaCGHGeneSummary")
