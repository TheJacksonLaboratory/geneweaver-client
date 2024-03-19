"""Test to get things from gedb similar to getting them from file."""

from tests.unit import test_client
from geneweaver.client.gedb import (
    DataRequest,
    DataResult,
    GeneExpressionDatabaseClient,
    SourceType,
)

class TestRecommenderDataStructures:
    # noqa: D102
    """Test recommender (recommender_py) connection.

    A very basic test class which should be improved to
    include more error conditions.
    """

    def test_fixture_works(self, test_client: GeneExpressionDatabaseClient) -> None:
        assert test_client is not None, "Unexpectedly cannot make a test_client using fixture"
