import typer

from . import parser

cli = typer.Typer()
cli.add_typer(parser.cli, name="parse")


@cli.command()
def test():
    print("test")
