"""Test to get things from gedb similar to getting them from file."""

from typing import List

import pytest
from geneweaver.client.gedb import (
    GeneExpressionDatabaseClient,
    Metadata,
)
from pandas import DataFrame


class TestRecommenderDataStructures:
    # noqa: D102
    """Test recommender (recommender_py) connection.

    A very basic test class which should be improved to
    include more error conditions.
    """

    @pytest.mark.usefixtures("test_client")
    def test_fixture_works(self, test_client: GeneExpressionDatabaseClient) -> None:
        """Test fixture works."""
        assert (
            test_client is not None
        ), "Unexpectedly cannot make a test_client using fixture"

    @pytest.mark.usefixtures("test_client")
    def test_get_meta_for_tissue(
        self, test_client: GeneExpressionDatabaseClient
    ) -> None:
        """Test meta mocked."""
        meta: List[Metadata] = test_client.get_meta("maxilla")
        assert meta is not None, "No metadata found for maxilla tissue!"

    def disabled_test_get_bulks_as_csv(
        self, test_client: GeneExpressionDatabaseClient
    ) -> None:
        """Test bulks."""
        meta: List[Metadata] = test_client.get_meta("maxilla")
        ingest_id = meta[0].get("ingestid")
        assert ingest_id is not None, "No ingest id found for maxilla tissue!"
        # TODO What happens if multiple ingests for maxilla?

        # Get all bulks as CSV and read into table.
        expr_data: DataFrame = test_client.read_expression_data(ingest_id)
        assert len(expr_data.index) == 14767, "The data frame size is {}".format(
            len(expr_data.index)
        )
