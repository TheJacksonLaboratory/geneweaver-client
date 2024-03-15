from unittest.mock import patch

import pytest
import os
import json

from typer.testing import CliRunner
from geneweaver.client.gedb import *
from typing import List
from typing import Set
from pathlib import Path
from collections import OrderedDict

runner = CliRunner()


@pytest.fixture(scope="session", autouse=True)
def test_client():
    """
    Yield a test client
    """
    test_client = TestGeneExpressionDatabaseClient()
    yield test_client
        
    
class TestOrthologs():

    def test_init_client_no_args(self):
        client = GeneExpressionDatabaseClient()
        assert client is not None, "Unexpectedly cannot make a client with no args"
        
    def test_init_client_on_dev(self):
        client = GeneExpressionDatabaseClient("https://geneweaver-dev.jax.org/gedb")
        assert client is not None, "Unexpectedly cannot make a client with dev uri"
        
    def test_get_tissues(self, test_client):
        tissues:  Set[str] = test_client.distinct("tissue")
        assert "heart" in tissues, "Tissue set must contain heart"
        assert "striatum" in tissues, "Tissue set must contain striatum"
        
    def test_get_stains(self, test_client):
        all_strains: Set[str] = test_client.distinct("strain")
        assert "B6" in tissues, "Strains set must contain B6"
        assert "CAST" in tissues, "Strains set must contain CAST"

    def test_search_expressions(self, test_client):
        
        genes = self.get_genes("tests/unit/connective_tissue_disorder_log2fc_test.csv")
        
        drequest = DataRequest(geneIds     = list(genes.keys()), 
                               strains     = ["*"],   # All strains if not searching on limited set.
                               sourceType  = SourceType.IMPUTED.name)
        
        js: str = json.dumps(drequest.__dict__)
        print(js)
        imputations: List[DataResult] = test_client.search(drequest, test=True)    
    
        print(imputations)
        # TODO Test result
    
    
    def get_genes(self, path: str) -> OrderedDict:
        
        # We keep the keys in order here as
        # it is easier to use the debugger and
        # check the dict
        gene_values = OrderedDict()
        with open(path,'r') as file:
     
            # reading each line from original text file
            for line in file.readlines():
                
                line = line.strip()
                if not (line.startswith('#')):
                    sa = line.split(',')
                    # Ingore other columns, just use first two.
                    gene_values[sa[0]] = sa[1]
                    
        return gene_values


class TestGeneExpressionDatabaseClient(GeneExpressionDatabaseClient):
    """
    We mock out some of the methods used in the test, badly.
    TODO Find better way of doing this.
    The strings returned here are copied from calling endpoints on the
    dev server.
    
    """
    
    def search(self, drequest: DataRequest, test=False):
        
        # Likely to fail with auth.
        return GeneExpressionDatabaseClient.search(self, drequest)
    
    def distinct(self, field: str) -> Set[str]:
        
        # Override for test.
        if field == "tissue":
            return json.loads('["ovary","testis","bone","Striatum","hippocampus","Islet","striatum","liver", \
            "skeletalmuscle","maxilla","adipose","mESC","islet","heart","kidney","skeletal muscle", \
            "dorsal vagal complex","hypothalamus","HFD"]')
        
        if field == "strain":
            return json.loads('["B6","CAST","NZO","PWK","129","NOD","WSB","Cast","AJ","C57BL/6J", \
            "129P2/OlaHsd","129S1/SvImJ","129S5SvEv<Brd>","A/J","AKR/J","B10.RIII","BALB/cByJ",\
            "BALB/cJ","BTBR T<+> Itpr3<tf>/J","BUB/BnJ","C3H/HeH","C3H/HeJ","C57BL/10J",\
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
            "BXD74/RwwJ","BXD202/RwwJ"]')
        
        # Likely to fail with auth.
        return GeneExpressionDatabaseClient.distinct(self, field)
    
# Example data request
'''
# Get using curl
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"geneIds": ["ENSMUSG00000000782", "ENSMUSG00000003279", "ENSMUSG00000005373", "ENSMUSG00000006014", "ENSMUSG00000006522", "ENSMUSG00000006800", "ENSMUSG00000018819", "ENSMUSG00000019838", "ENSMUSG00000020053", "ENSMUSG00000020218", "ENSMUSG00000020388", "ENSMUSG00000020866", "ENSMUSG00000021057", "ENSMUSG00000021136", "ENSMUSG00000021200", "ENSMUSG00000022440", "ENSMUSG00000022899", "ENSMUSG00000023034", "ENSMUSG00000024190", "ENSMUSG00000024697", "ENSMUSG00000024812", "ENSMUSG00000024968", "ENSMUSG00000024990", "ENSMUSG00000025027", "ENSMUSG00000026304", "ENSMUSG00000026360", "ENSMUSG00000026414", "ENSMUSG00000027204", "ENSMUSG00000027254"], "strains": ["*"], "sourceType": "IMPUTED"}' \
  https://geneweaver-dev.jax.org/gedb/gene/expression/search

'''