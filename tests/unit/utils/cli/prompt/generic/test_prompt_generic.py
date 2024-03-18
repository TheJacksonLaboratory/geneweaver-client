"""Test the prompt_generic function."""

from unittest.mock import Mock

import pytest
from geneweaver.client.utils.cli.prompt.generic import prompt_generic


@pytest.mark.parametrize("field_name", ["field_name", "field_name_2", "field_name_3"])
@pytest.mark.parametrize(
    ("field_type", "example_input"),
    [(str, "test"), (int, 1), (float, 1.0), (bool, False)],
)
@pytest.mark.parametrize("allow_none", [True, False])
def test_prompt_generic(field_name, field_type, example_input, allow_none, monkeypatch):
    """Test the prompt_generic function."""
    mock_prompt = Mock(return_value=example_input)
    mock_allow_none_str = Mock(return_value=" (Optional)")
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.generic.typer.prompt", mock_prompt
    )
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.generic.allow_none_str", mock_allow_none_str
    )
    assert mock_prompt.call_count == 0

    result = prompt_generic(field_name, field_type, allow_none)

    assert mock_prompt.call_count == 1
    assert result == field_type(example_input)
    assert (
        f"{field_name.replace('_', ' ').capitalize()} ({field_type.__name__})"
        in mock_prompt.call_args_list[0][0][0]
    )
    if allow_none:
        assert mock_prompt.call_args_list[0][0][0].endswith("(Optional)")
    else:
        assert not mock_prompt.call_args_list[0][0][0].endswith("(Optional)")


def test_prompt_generic_with_none_input(monkeypatch):
    """Test the prompt_generic function with None input."""
    mock_prompt = Mock(return_value=None)
    mock_allow_none_str = Mock(return_value=" (Optional)")
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.generic.typer.prompt", mock_prompt
    )
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.generic.allow_none_str", mock_allow_none_str
    )
    assert mock_prompt.call_count == 0

    result = prompt_generic("field_name", str, True)

    assert mock_prompt.call_count == 1
    assert result is None
    assert "Field name (str) (Optional)" in mock_prompt.call_args_list[0][0][0]
    assert mock_prompt.call_args_list[0][0][0].endswith("(Optional)")


def test_prompt_generic_with_invalid_input(monkeypatch):
    """Test the prompt_generic function with invalid input."""
    mock_prompt = Mock(side_effect=[None, 1])
    mock_print = Mock()
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.generic.typer.prompt", mock_prompt
    )
    monkeypatch.setattr("builtins.print", mock_print)
    assert mock_prompt.call_count == 0

    result = prompt_generic("field_name", int)

    assert mock_prompt.call_count == 2
    assert result == 1
    assert "Field name (int)" in mock_prompt.call_args_list[0][0][0]
    assert (
        "Invalid value for field_name. Please try again."
        in mock_print.call_args_list[0][0][0]
    )
