"""Test the value_represents_none function."""

# ruff: noqa: ANN101
import pytest
from geneweaver.client.utils.cli.prompt.none import value_represents_none


@pytest.mark.parametrize("value", [None, "None", "none", "nOnE", "--"])
def test_value_represents_none(value):
    """Test the value_represents_none function."""
    assert value_represents_none(value)


@pytest.mark.parametrize("value", ["n/a", "N/A", "N", " ", "-"])
def test_value_does_not_represent_none(value):
    """Test the value_represents_none function."""
    assert not value_represents_none(value)


class MockInvalidClass:
    """Mock class to test invalid input."""

    def __init__(self, invalid_response) -> None:
        """Initialize the class."""
        self.invalid_response = invalid_response

    def __str__(self) -> str:
        """Return the invalid response."""
        return self.invalid_response


@pytest.mark.parametrize("value", [True, False, 1, 0, None])
def test_value_represents_none_with_invalid_input(value):
    """Test the value_represents_none function with invalid input."""
    result = value_represents_none(MockInvalidClass(value))
    assert result is False
