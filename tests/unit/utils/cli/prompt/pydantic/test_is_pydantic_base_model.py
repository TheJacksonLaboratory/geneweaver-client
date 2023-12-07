"""Test the is_pydantic_base_model function."""
import pytest
from geneweaver.client.utils.cli.prompt.pydantic import is_pydantic_base_model
from geneweaver.core.schema.batch import BatchUploadGeneset
from geneweaver.core.schema.score import GenesetScoreType
from pydantic import BaseModel


@pytest.mark.parametrize(
    "model_class", [BaseModel, GenesetScoreType, BatchUploadGeneset]
)
def test_is_pydantic_base_model_with_pydantic_base_model(model_class):
    """Test the is_pydantic_base_model function with a pydantic base model."""
    assert is_pydantic_base_model(model_class)


@pytest.mark.parametrize(
    "model_class", [str, int, float, bool, list, tuple, dict, 1, ""]
)
def test_is_pydantic_base_model_with_non_pydantic_base_model(model_class):
    """Test the is_pydantic_base_model function with a non-pydantic base model."""
    assert not is_pydantic_base_model(model_class)
