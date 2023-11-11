"""Test the main entrypoint to the GeneWeaver CLI client."""
# ruff: noqa: ANN001, ANN201
from geneweaver.client.cli.main import cli
from typer.testing import CliRunner

runner = CliRunner()


def test_version_callback():
    """Test the version callback."""
    # Simulate the CLI execution
    result = runner.invoke(cli, ["--version"])

    # Check the output message
    assert "GeneWeaver CLI client (gweave) version:" in result.output
    # Check the exit code
    assert result.exit_code == 0


def test_common():
    """Test the common callback."""
    # Simulate the CLI execution without any arguments
    result = runner.invoke(cli)

    # There should be no output in this case
    assert "GeneWeaver CLI client." in result.output
    # Check the exit code
    assert result.exit_code == 0


def test_common_w_arg():
    """Test the common callback with an argument."""
    # Now check when you pass an argument
    result_with_args = runner.invoke(cli, ["alpha", "parse", "--help"])

    # Check the exit code
    assert result_with_args.exit_code == 0
