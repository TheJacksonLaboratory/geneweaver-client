"""Test the format_enum_name function."""
import pytest
from geneweaver.client.utils.cli.prompt.enum import format_enum_name

from tests.unit.utils.cli.prompt.enum.conftest import MockEnum, MockIntEnum


@pytest.mark.parametrize(
    ("enum_input", "expected"),
    [
        (MockEnum, "Mock Enum"),
        (MockIntEnum, "Mock Int Enum"),
    ],
)
def test_format_enum_name_with_enum(enum_input, expected):
    """Test the format_enum_name function with valid input."""
    assert format_enum_name(enum_input) == expected
