# noqa: D100

from typing import List, Set

import pytest
from geneweaver.client.gedb import (
    DataRequest,
    DataResult,
    GeneExpressionDatabaseClient,
    SourceType,
)
from requests.exceptions import HTTPError

from tests.unit import test_client

class TestOrthologs:
    # noqa: D102
    """Test Orthologs.

    A very basic test class which should be improved to
    include more error conditions.
    """

    def test_init_client_no_args(self) -> None:
        """Test client no args."""
        client = GeneExpressionDatabaseClient()
        assert client is not None, "Unexpectedly cannot make a client with no args"

    def test_init_client_on_dev(self):
        """Test client on dev."""
        client = GeneExpressionDatabaseClient("https://geneweaver-dev.jax.org/gedb")
        assert client is not None, "Unexpectedly cannot make a client with dev uri"

    def test_get_tissues(self, test_client: GeneExpressionDatabaseClient):
        """Test get tissues."""
        tissues: Set[str] = test_client.distinct("tissue")
        assert "heart" in tissues, "Tissue set must contain heart"
        assert "striatum" in tissues, "Tissue set must contain striatum"

    def test_get_strains(self, test_client: GeneExpressionDatabaseClient):
        """Test get strains."""
        tissues: Set[str] = test_client.distinct("strain")
        assert "B6" in tissues, "Strains set must contain B6"
        assert "CAST" in tissues, "Strains set must contain CAST"

    def test_get_not_there(self, test_client: GeneExpressionDatabaseClient):
        """Test not there."""
        with pytest.raises(HTTPError):
            test_client.distinct("NOT-THERE")

    def test_search_expressions(self, test_client: GeneExpressionDatabaseClient):
        """Test get tissues."""
        imputations = self._connective_tissue_disorder(test_client)
        assert (
            len(imputations) == 122859
        ), "The length of the imputations array is {}".format(len(imputations))

    def test_sort_results(self, test_client: GeneExpressionDatabaseClient):
        """Test sort results."""
        imputations = self._connective_tissue_disorder(test_client)
        srtd = test_client.sort("strain", imputations)
        # There are 657 strains in this list of results.
        assert len(srtd) == 657, "The size of the strains map is {}".format(len(srtd))

    def _connective_tissue_disorder(self, test_client: GeneExpressionDatabaseClient) -> List[DataResult]:
        genes = test_client.get_genes(
            "tests/unit/connective_tissue_disorder_log2fc_test.csv"
        )
        drequest = DataRequest(
            geneIds=list(genes.keys()),
            strains=["*"],  # All strains if not searching on limited set.
            sourceType=SourceType.IMPUTED.name,
        )

        # This is a larger search size. When connected to a real database
        # it takes about 1.5-2 minutes. This is acceptable performance we think.
        return test_client.search(drequest)
