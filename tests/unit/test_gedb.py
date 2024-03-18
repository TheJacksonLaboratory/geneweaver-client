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
    real_server: boolean = True # Should be false for CICD which then mocks
    
    if real_server:
        # The auth here needs a cookie to connect to geneweaver-dev.jax.org when trying to 
        # run these tests against a real server. To do this use:
        # 1. Connect to swagger at https://geneweaver-dev.jax.org/gedb/
        # 2. Make a call, for instance to distinct tissues
        # 3. Press F12 and open developer tools, go to network
        # 4. Copy value of "_oauth2_proxy" and use here
        auth_proxy = "1nKmq1WwyMfrZsg9an5fRZrl7Tq6p8spGHsFRhCPEyMIZuQarOKZiXkg8tV1LRgXwgoQNDEKD2DvAp_xDk1XKoSoERJo-8kEeG2d3VVbqOU89HHaFqsWf9cVTXjsGkUYiNKZpNG6SmAPhumvVTOwwisk-2jGaTru-YeqNjKecjG-iNNdUa7JhWsBjGl6pExLmipBeDbvULyNYMGqxbG15gCyOPU2Bvbsc2NyjCwWuTJJcEpspblQ4v4_hydwROct-EV5dGlInnpzqjXxnzaqnSjf0S35CgXX2uVY_9H4vViJrsgv0dpfC3m2xgCBd1wx32wHbpAnbN7rdKavpAnNPbREeaVmv_cGQTqmgvWgjCZnMTStUG8Efh_oolFVBlt0e6w7NYNyAmKOzBCdDLA_lT4hfrsV48wngaJ9KaGocSmLXIgTL31wHCPBaVfwYC9Quh-4zKlRpMbM_lD9NLaFzua_Ct30ZLx1AAG4bv4TvjXqNvFK-WPcegTRUlzMXYxaFnMYN4GC4F1GLKq7yTIWmm6153HLWJocqpYHDacBhNFcvnJ5JZgzaXRuKY10-Mn6xn2lK6KesW86u5oVCRt8jScS4lRSrtkRp4ICf2cmFmsDjOZyf-tEqT44smlQVtSWn2Phhoj1SS-gJ1r11FlHUnDfFFlWKV2nY_DSRJwEfWKiAwqHYALDe2iszBjDifEetwBEPW-KYNuDihS5XY6BKwYGXOdmN-fjtXIrKKAMvvcEMa88Hylz0_NqZwZOgEa75oQEf02yRebaAGH4tN4rF8VwmOdfi7AcE5JAgqtkyONrz9u7NK8s3Rhik6xBIeVqdUp2FVNMtRxnXgehvXZi2uvTcFV9h12usgcim7k7XIDqoEPq0CVfusJgllunstVmLH-wkXuPe-eggyNwk4dcXSu4XJ-jmVmV8GMeJz7ME7fAU46I22j2ZeK7jdx5O8AgPatG7GDczXCXUbWEOmGbHLbn8PQqIykuWjo4fq7gIiWglqtvFEAa4qVX7eKNU7NFoBwHtqZGXIrteOhs9NzxxShK_hNv_SyTRM3lILXkwp4jtj-rQAg6YvfLU823SX7iiuxJ23Ff11s3uULv2S7t7vGjdZipP0uZ9iw5XsfOb5Nn-lDBn7FEA2lTkAG_tm-dqy2gMDIJZ_u3aPc-wQIhlVuZpQ_I1SsTjnm4zL71HTTY6EfhRAtqpfZN8KS0v74zQEf5HfHTiT1qh-BzkChwWzXUfLgwhRcSoRC3rJcdDqW8QXYW5vNi5aI2O73N5ticS94kCs_63RC3ZpXCvszClVIaR4W5MeXtf9oQWtRdqm1BDnHEVPTk6mRWCv8SKgtVBVRIXFS4AW0CXvdMQthLJQe0BKeuYI3oZUGTOImDDGJIzX8OC9kM5R4_b-Twp11KzByCNrMQaHGZvEjAJB-9ddafOu8EyBF5078QLiIQ-yXZ_wluauecBLcwa4qM7k94g7lpyfR5MoaAS50V8kY2AhtiN9cUO44be9TJUd1lPpYUy2ZqhEcpGkdWEG1TxqibXbwCzDcjQFc9yYzPBxRrT47NKCleVSh46xYd0G37_AZW_iU9_nSyV2IlUisjNwNsP_YZ-OZ969XnYhulrJlAvEbSK6OoVVyeX8yuKSBadojvvk_5Stm5Jtbjhwk1sbFkBphw1Xmi0FXZ8EB88xgknDy4WuL9SBTXtprQuUkX69dBJX2PUT83fQkVKgZ9ZwY8dMTPlPB02-TeTovWuOBu48dS49JZ95aDp3oKv0Ht6Qv1oupNvV849woNj6EksK1ePfelLgXuVFKhiXHwTni7TQ6-agzMCVSTyAUaL4Zci2l0V2guMp8Fu1eFhSSWYfcuLi4wWkQA0sreRn1sNNMXot01Yp4JUmczmqM9NsjDmtz-uUX695IoQP2xvUl8IyE3OcUhpmRDIOxCMalRVo5Kz9kGmifN9c94MTcESldAAcRccZ-Y8X1PVNJKEgDXevFZn4tiLhA0R4lBxyO6LWDRy00oUFnZ3HRLLLHTp8HEiKaB1TyhfdtVgw-T_C7-cMItHnyEbgN7C2lA_BFWXMfOYTCYqJPmMmVUJRGKgag-OK5PZnfdtyF8NhGfU5nXrJ_S-1yfdUwFGCJc_uVyM6LziYGVwbD8-yFJ7jbb-WAZh-Bvpo_LHyAPW56_e5RhrAOp5IyODUPDt_jxDSUvLY0bEAAvwl0TTn7z2Di6wXQ96jCVwGQ3Qww458rQOyUkcMR2VMziZDqLQxjeIt8B8HjLIUkJmUHpg0FXuawun8jEA_ILXhilia6-NP4WTApKk9mLvzBRYGXCbz6GK8U-FSWeuw0Fv1945OjdT3Rh_hKE1GASU4BhsIrfTVAQ5V9txU--Xh0bIe37WGVcOkygYIJtwTYLUIavZMUC2ASc_iDhPCSNj7IJ0ma0JGKuuY2AWBrMFdGl2cK3fEmlIntoJCPrtAYJWaAOUtYjdkIUZpRHZ5pK9iNRIRtVVIRu1MKd-lIsciNjTTc5uTvUMsfhsd5CVItlIYH_F5BaHmfFEsuEnoqq45lgHfEg|1710437090|f9oHFkdfgJXlhx1kbSgz5Lst_klm5RK49A8-cozuJN8="
        test_client = GeneExpressionDatabaseClient(url="https://geneweaver-dev.jax.org/gedb", auth_proxy=auth_proxy)
    else:
        test_client = MockGeneExpressionDatabaseClient()
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
        
    def test_get_strains(self, test_client):
        tissues: Set[str] = test_client.distinct("strain")
        assert "B6" in tissues, "Strains set must contain B6"
        assert "CAST" in tissues, "Strains set must contain CAST"

    def test_get_not_there(self, test_client):
        with pytest.raises(Exception):
            empty: Set[str] = test_client.distinct("NOT-THERE")

    def test_search_expressions(self, test_client):
        
        genes = self.get_genes("tests/unit/connective_tissue_disorder_log2fc_test.csv")
        
        drequest = DataRequest(geneIds     = list(genes.keys()), 
                               strains     = ["*"],   # All strains if not searching on limited set.
                               sourceType  = SourceType.IMPUTED.name)
        
        js: str = json.dumps(drequest.__dict__)
        print(js)
        imputations = test_client.search(drequest)    
    
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


class MockGeneExpressionDatabaseClient(GeneExpressionDatabaseClient):
    """
    We mock out some of the methods used in the test, badly.
    TODO Find better way of doing this.
    The strings returned here are copied from calling endpoints on the
    dev server.
    
    """
    
    
    def search(self, drequest: DataRequest):
        
        raise Exception("Not mocked!")    
    
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
        
        raise Exception("Not mocked!")
