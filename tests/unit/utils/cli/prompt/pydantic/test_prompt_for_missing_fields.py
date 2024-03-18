"""Test the prompt_for_missing_fields function."""

from unittest.mock import Mock

import pytest
from geneweaver.client.utils.cli.prompt.pydantic import prompt_for_missing_fields

from tests.unit.utils.cli.prompt.pydantic.conftest import (
    MOCK_EXISTING_COMBINATIONS,
    MOCK_MODEL_FIELD_COMBINATIONS,
    MOCK_MODEL_FIELDS,
    MockModel,
)


# We can't use every combination of fields because the number of combinations
# grows much too large to be practical.
# Instead, we use the first 25 and last 25 combinations.
@pytest.mark.parametrize(
    "existing", MOCK_EXISTING_COMBINATIONS[:25] + MOCK_EXISTING_COMBINATIONS[-25:]
)
@pytest.mark.parametrize(
    "exclude", MOCK_MODEL_FIELD_COMBINATIONS[:25] + MOCK_MODEL_FIELD_COMBINATIONS[-25:]
)
@pytest.mark.parametrize("prompt_to_keep_existing", [True, False])
def test_prompt_for_missing(existing, exclude, prompt_to_keep_existing, monkeypatch):
    """Test the prompt_for_missing_fields function."""
    mock_prompt_to_keep = Mock()
    mock_prompt_for_field_by_type = Mock()
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.pydantic.prompt_to_keep_field",
        mock_prompt_to_keep,
    )
    monkeypatch.setattr(
        "geneweaver.client.utils.cli.prompt.pydantic.prompt_for_field_by_type",
        mock_prompt_for_field_by_type,
    )
    prompt_for_missing_fields(MockModel, existing, exclude, prompt_to_keep_existing)

    # We should prompt for every field in `existing` that is not in `exclude`.
    if prompt_to_keep_existing and len(existing) > 0:
        assert mock_prompt_to_keep.call_count == len(set(existing.keys()) - exclude)

    # We should prompt for every field in `MockModel` that is not in
    # `existing` or `exclude`.
    assert mock_prompt_for_field_by_type.call_count == len(
        set(MOCK_MODEL_FIELDS) - set(existing.keys()) - exclude
    )
