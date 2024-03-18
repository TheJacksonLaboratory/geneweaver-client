# noqa: D100

import gzip
import json
from typing import List, Set

import pytest
from geneweaver.client.gedb import (
    DataRequest,
    DataResult,
    GeneExpressionDatabaseClient,
    SourceType,
)
from requests.exceptions import HTTPError
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(scope="session", autouse=True)
def test_client():
    """Yield a test client."""
    local_server: bool = False  # Should be false for CICD which then mocks
    cs_server: bool = False  # Should be false for CICD which then mocks

    if local_server:
        # You will need to start the gene-expr-service pointing to BigQuery
        # in order to get this to work. Your creds will need to allow you to
        # contact to this service. application.yml will need to provide a
        # google project and BQ dataset which has been prefilled with data.
        test_client = GeneExpressionDatabaseClient(url="http://localhost:2289")

    elif cs_server:
        # The auth here needs a cookie to connect to
        # geneweaver-dev.jax.org when trying to
        # run these tests against a real server. To do this use:
        # 1. Connect to swagger at https://geneweaver-dev.jax.org/gedb/
        # 2. Make a call, for instance to distinct tissues
        # 3. Press F12 and open developer tools, go to network
        # 4. Copy value of "_oauth2_proxy" and use here
        auth_proxy = "YOUR_TOKEN"
        test_client = GeneExpressionDatabaseClient(
            url="https://geneweaver-dev.jax.org/gedb", auth_proxy=auth_proxy
        )

    else:
        test_client = MockGeneExpressionDatabaseClient()

    return test_client


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

    def test_get_tissues(self, test_client):
        """Test get tissues."""
        tissues: Set[str] = test_client.distinct("tissue")
        assert "heart" in tissues, "Tissue set must contain heart"
        assert "striatum" in tissues, "Tissue set must contain striatum"

    def test_get_strains(self, test_client):
        """Test get strains."""
        tissues: Set[str] = test_client.distinct("strain")
        assert "B6" in tissues, "Strains set must contain B6"
        assert "CAST" in tissues, "Strains set must contain CAST"

    def test_get_not_there(self, test_client):
        """Test not there."""
        with pytest.raises(HTTPError):
            test_client.distinct("NOT-THERE")

    def test_search_expressions(self, test_client):
        """Test get tissues."""
        imputations = self._connective_tissue_disorder(test_client)
        assert (
            len(imputations) == 122859
        ), "The length of the imputations array is {}".format(len(imputations))

    def test_sort_results(self, test_client):
        """Test sort results."""
        imputations = self._connective_tissue_disorder(test_client)
        srtd = test_client.sort("strain", imputations)
        # There are 657 strains in this list of results.
        assert len(srtd) == 657, "The size of the strains map is {}".format(len(srtd))

    def _connective_tissue_disorder(self, test_client) -> List[DataResult]:
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


class MockGeneExpressionDatabaseClient(GeneExpressionDatabaseClient):
    """Mock Client.

    We mock out some of the methods used in the test, badly.
    TODO Find better way of doing this.
    The strings returned here are copied from calling endpoints on the
    dev server.

    """

    def search(self, drequest: DataRequest):
        """Mock search."""
        if drequest.sourceType is SourceType.IMPUTED.name:
            # Read file and return json
            with gzip.open("tests/unit/imputations.json.gz", "rb") as f:
                file_content = f.read()
                return json.loads(file_content)

        raise HTTPError("Not mocked!")

    def distinct(self, field: str) -> Set[str]:
        """Mock distinct."""
        # Override for test.
        if field == "tissue":
            return json.loads(
                '["ovary","testis","bone","Striatum","hippocampus", \
            "Islet","striatum","liver", \
            "skeletalmuscle","maxilla","adipose","mESC","islet","heart", \
            "kidney","skeletal muscle", \
            "dorsal vagal complex","hypothalamus","HFD"]'
            )

        if field == "strain":
            return json.loads(
                '["B6","CAST","NZO","PWK","129","NOD","WSB","Cast","AJ","C57BL/6J", \
            "129P2/OlaHsd","129S1/SvImJ","129S5SvEv<Brd>","A/J","AKR/J","B10.RIII","BALB/cByJ",\
            "BALB/cJ","BTBR T<+> Itpr3<tf>/J","BUB/BnJ","C3H/HeH","C3H/HeJ",\
            "C57BL/10J",\
            "C57BL/10SnJ","C57BL/6NJ","C57BR/cdJ","C57L/J","C58/J","CAST/EiJ","CBA/J","CE/J",\
            "CZECHII/EiJ","DBA/1J","DBA/2J","FVB/NJ","I/LnJ","JF1/MsJ","KK/HlJ","LEWES/EiJ",\
            "LG/J","LP/J","MA/MyJ","MOLF/EiJ","NOD/ShiLtJ","NON/ShiLtJ","NZB/BlNJ","NZO/HlLtJ",\
            "NZW/LacJ","PL/J","PWK/PhJ","QSi3/Ianm","QSi5/Ianm","RF/J","RIIIS/J","SEA/GnJ","SJL/J",\
            "SM/J","SPRET/EiJ","ST/bJ","SWR/J","WSB/EiJ","ZALENDE/EiJ","BXD224","BXD85/RwwJ",\
            "BXD67/RwwJ","BXD50/RwwJ","BXD199/RwwJ","BXD87/RwwJ","BXD89/RwwJ","BXD111/RwwJ",\
            "BXD124/RwwJ","BXD114","BXD20/TyJ","BXD8/TyJ","BXD216/RwwJ","BXD1/TyJ","BXD128/RwwJ",\
            "BXD48a/RwwJ","BXD15/TyJ","BXD123/RwwJ","BXD171/RwwJ","BXD71/RwwJ","BXD147","BXD31/TyJ",\
            "BXD33/TyJ","BXD209","BXD194/RwwJ","BXD53/2RwwJ","BXD73b/RwwJ","BXD131","BXD161/RwwJ",\
            "BXD101/RwwJ","BXD38/TyJ","BXD173","BXD168/RwwJ","BXD226","BXD65b/RwwJ","BXD16/TyJ",\
            "BXD74/RwwJ","BXD202/RwwJ"]'
            )

        raise HTTPError("Not mocked!")
