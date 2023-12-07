"""Test the is_bool function."""
import pytest
from geneweaver.client.utils.cli.prompt.bool import is_bool


@pytest.mark.parametrize(
    ("value", "expected_output"),
    [
        (bool, True),
        (True, False),
        (False, False),
        ("True", False),
        ("False", False),
        ([], False),
        (int, False),
    ],
)
def test_is_bool(value, expected_output):
    """Test the is_bool function."""
    assert is_bool(value) == expected_output
