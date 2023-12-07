"""Test the format_enum_name function."""
from enum import Enum

import pytest
from geneweaver.client.utils.cli.prompt.enum import format_enum_name

from tests.unit.utils.cli.prompt.enum.conftest import MockEnum, MockIntEnum


class GenesetSpeciesEnum(Enum):
    """Mock enum for testing."""


class GenesetScoreTypeEnum(Enum):
    """Mock enum for testing."""


@pytest.mark.parametrize(
    ("enum_input", "expected"),
    [
        (MockEnum, "Mock"),
        (MockIntEnum, "MockInt"),
        (GenesetSpeciesEnum, "Species"),
        (GenesetScoreTypeEnum, "Score"),
    ],
)
def test_format_enum_name(enum_input, expected):
    """Test the format_enum_name function with valid input."""
    assert format_enum_name(enum_input) == expected
