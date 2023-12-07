"""Test the allow_none_str function."""
import pytest
from geneweaver.client.utils.cli.prompt.generic import allow_none_str


@pytest.mark.parametrize(
    "none_repr",
    [
        ["None"],
        ["--"],
        ["N/A"],
        ["N/A", "None"],
        ["N/A", "--"],
    ],
)
def test_allow_none_str(none_repr, monkeypatch):
    """Test the allow_none_str function generates string with NONE_REPRS in it."""
    monkeypatch.setattr("geneweaver.client.utils.cli.prompt.none.NONE_REPRS", none_repr)
    result = allow_none_str()
    for none_str in none_repr:
        assert none_str in result

    # The result should be consistent
    assert result == allow_none_str()
