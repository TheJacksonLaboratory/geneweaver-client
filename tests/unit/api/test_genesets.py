"""Tests for the Geneset API."""
# ruff: noqa: ANN001, ANN201
import datetime

import pytest
from geneweaver.client.api import genesets
from geneweaver.client.api.exc import GeneweaverAPIError
from geneweaver.core.enum import GenesetAccess, ScoreType
from geneweaver.core.schema.geneset import BatchUpload, GenesetUpload

from .test_api_utils import CLIENT_ERROR, SERVER_ERROR

VALID_GENESET_RESPONSES = [
    {
        "name": "test",
        "abbreviation": "test",
        "description": "test",
        "count": 1,
        "threshold_type": 0,
        "threshold": "0",
        "gene_id_type": 0,
        "created": str(datetime.date.today()),
        "admin_flag": "test",
        "updated": str(datetime.datetime.now()),
        "status": "test",
        "gsv_qual": "test",
        "attribution": 0,
        "is_edgelist": False,
    }
]

VALID_GENESET_UPLOADS = [
    GenesetUpload(
        **{
            "score_type": ScoreType.BINARY,
            "pubmed-id": "12345678",
            "access": GenesetAccess.PUBLIC,
            "groups": ["test"],
            "name": "test",
            "label": "test",
            "species": "test",
            "description": "test",
            "gene_identifier": "test",
            "gene_list": [{"symbol": "test", "value": 1}],
        }
    ),
]

VALID_GENESET_BATCH_UPLOADS = [
    BatchUpload(**{"batch_file": "test", "curation_group": ["test"]}),
]


@pytest.mark.parametrize("geneset", VALID_GENESET_UPLOADS)
@pytest.mark.parametrize("response", VALID_GENESET_RESPONSES)
def test_post_geneset(config_sessionmanager_patch, geneset, response):
    """Test that the geneset upload API works."""
    config_sessionmanager_patch(status_code=200, resp_json=response)
    result = genesets.post("token", geneset)
    assert result is not None


@pytest.mark.parametrize("geneset", VALID_GENESET_UPLOADS)
@pytest.mark.parametrize("error_status", CLIENT_ERROR + SERVER_ERROR)
def test_post_geneset_fails(config_sessionmanager_patch, error_status, geneset):
    """Test that the geneset upload API fails when the server returns an error."""
    config_sessionmanager_patch(status_code=error_status, resp_json={"error": "test"})
    with pytest.raises(GeneweaverAPIError):
        _ = genesets.post("token", geneset)


@pytest.mark.parametrize("geneset", VALID_GENESET_BATCH_UPLOADS)
@pytest.mark.parametrize("response", VALID_GENESET_RESPONSES)
def test_post_geneset_batch(config_sessionmanager_patch, geneset, response):
    """Test that the geneset batch upload API works."""
    config_sessionmanager_patch(status_code=200, resp_json=response)
    result = genesets.post_batch("token", geneset)
    assert result is not None
