"""Top level fixtures for unit tests."""

import gzip
import json
import os
import random
from typing import List, Set

import numpy
import pytest
from geneweaver.client.gedb import (
    Bulk,
    DataRequest,
    DataResult,
    GeneExpressionDatabaseClient,
    Metadata,
    SourceType,
)
from geneweaver.testing.fixtures import *  # noqa: F403
from numpy.random import Generator
from pandas import DataFrame
from requests.exceptions import HTTPError


@pytest.fixture(scope="session", autouse=True)
def test_client():
    """Yield a test client for the GEDB."""
    local_server: bool = False  # Should be false for CICD which then mocks

    # IMPORTANT IT IS A GOOD IDEA TO SET THIS TO TRUE and set AUTH_PROXY
    # in order to check your changes vs. the real expression database.
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
        auth_proxy = os.environ.get("AUTH_PROXY", None)
        test_client = GeneExpressionDatabaseClient(
            url="https://geneweaver-dev.jax.org/gedb", auth_proxy=auth_proxy
        )

    else:
        test_client = MockGeneExpressionDatabaseClient()

    return test_client


class MockGeneExpressionDatabaseClient(GeneExpressionDatabaseClient):
    """Mock Client.

    We mock out some of the methods used in the test, badly.
    TODO Find better way of doing this.
    The strings returned here are copied from calling endpoints on the
    dev server.

    """

    def search(self, drequest: DataRequest):
        """Mock search."""
        if (
            drequest.sourceType is SourceType.IMPUTED.name
            and drequest.tissue == "maxilla"
        ):

            # Read file and return json
            with gzip.open("tests/unit/imputations.json.gz", "rb") as f:
                file_content = f.read()
                return [
                    self._class_from_args(DataResult, item)
                    for item in json.loads(file_content)
                ]

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

    def get_meta(self, tissue: str) -> List[Metadata]:
        """Mock get metadata."""
        if "maxilla" == tissue:
            jsons: List = json.loads(
                '[{"ingestid": "95c8aa44-5d5a-42d9-9f10-33a20904ad1e", \
            "modelversion": "ridge_v1_2_1", "population": "GenomeMUSter_v2", \
            "tissue": "maxilla", "sourcetype": "IMPUTED", "species": "Mus musculus", \
            "uberon": "0002397"}]'
            )
            return [self._class_from_args(Metadata, item) for item in jsons]

        raise HTTPError("Not mocked!")

    def random(self, ingest_id: str, size: int, count: int = 1) -> List[DataFrame]:
        """Get a random gene expression frame."""
        randoms: List[str] = []

        for _ in range(count):
            name: str = "s{}".format(round(random.random() * 1000))
            for _ in range(size):
                r: str = "{},{}".format(name, (random.random() * 2) - 1)
                randoms.append(r)

        ret: List[List[str]] = self._split_list(randoms, size)
        return [self._frame(list(r)) for r in ret]

    def random_spearmanrho(
        self, ingest_id: str, scores: [float], r_size: int = 1
    ) -> List[float]:
        """Mock."""
        gen: Generator = numpy.random.default_rng()
        rhos: List[float] = list(gen.random(r_size))
        return rhos

    def _random_data_result(self, name: str) -> Bulk:
        r: Bulk = Bulk()
        r.exprnames = [name]
        r.exprvalues = [(random.random() * 2) - 1]
        r.geneid = "ESNMUSTEST{}".format(round(random.random() * 1000))
        return r
