"""Test functions of the graph client."""

from contextlib import contextmanager

import pytest

# What we are testing
from geneweaver.client.api.graph import Position, SearchRequest, VariantGraphClient
from neomodel import config
from requests import HTTPError

# All the stuff needed to test it
from testcontainers.neo4j import Neo4jContainer

from .dao import Gene, GraphManager
from .graph_server import GraphServer


@contextmanager
def start_neo4j():
    """Start neo4j indocker using test containers."""
    neo4j = Neo4jContainer("neo4j:5.9.0-community")
    neo4j.start()
    yield neo4j
    neo4j.stop()


@pytest.fixture(scope="session", autouse=True)
def neo4j():
    """Start neo4j indocker using test containers."""
    with start_neo4j() as neo4j:
        yield neo4j

        # Clean neo4j database


@pytest.fixture(scope="session", autouse=True)
def bolt_url(neo4j):
    """Create the bolt url and configure OGM to use.

    for the object creation steps
    """
    url = neo4j.get_connection_url()
    # Replace bolt:// with bolt://neo4j:password@
    url = "bolt://neo4j:password@" + url[7:]
    config.DATABASE_URL = url
    return url


@pytest.fixture(scope="session", autouse=True)
def server(neo4j):
    """Start the Java graph server which talks to the graph database.

    NOTE: This means that the automated build must either have a JDK
    on it or we put this graph server in a docker container and use
    that.
    """
    url = neo4j.get_connection_url()
    server = GraphServer("neo4j", "password", url)
    server.start_test_server()
    yield server
    server.stop_test_server()


@pytest.fixture()
def vgc(server):
    """Make the variant graph client.

    - to be used in the test to ask questions about the graph.

    IMPORTANT: This is the class which we are actually testing!
    Where you see: 'vgc' that's what's being tested!
    """
    url = server.url()
    vgc = VariantGraphClient(url)
    return vgc


@pytest.fixture()
def manager(server):
    """Create graph manager helper object."""
    manager = GraphManager()
    yield manager
    manager.clear()


@pytest.mark.skip(reason="We do not want java on the build server")
class TestOrthologs:
    """The tests."""

    def test_client_started_ok(self, vgc):
        """Test."""
        if vgc is None:
            raise Exception("Client not injected!")

        status: dict = vgc.heartbeat()
        if status["connected"] is not True:
            raise Exception("Client not connected to server!")

    def test_save_one_gene(self, vgc):
        """Test."""
        gene = Gene(geneId="test", geneName="TEST")
        gene.save()

    def test_one_ortholog(self, vgc, manager):
        """Test."""
        _ = manager.create_orthologs(1)
        geneset = ["ENSGTEST0"]
        homs = vgc.get_orthologs(geneset)
        assert len(homs) == 1

    def test_ten_orthologs(self, vgc, manager):
        """Test."""
        _ = manager.create_orthologs(10)
        geneset = ["ENSGTEST{}".format(i) for i in range(10)]
        homs = vgc.get_orthologs(geneset)
        assert len(homs) == 10

        expected = ["ENSMUSGTEST{}".format(i) for i in range(10)]
        for hid, mid in zip(geneset, expected):
            assert homs[hid] == mid

    def test_no_orthologs(self, vgc, manager):
        """Test."""
        _ = manager.create_a_graph(10, connect=False)
        geneset = ["ENSGTEST{}".format(i) for i in range(10)]
        homs = vgc.get_orthologs(geneset)
        assert len(homs) == 0

    def test_ten_orthologs_larger_graph(self, vgc, manager):
        """Test."""
        _ = manager.create_a_graph(10)
        geneset = ["ENSGTEST{}".format(i) for i in range(10)]
        homs = vgc.get_orthologs(geneset)
        assert len(homs) == 10

        expected = ["ENSMUSGTEST{}".format(i) for i in range(10)]
        for hid, mid in zip(geneset, expected):
            assert homs[hid] == mid


@pytest.mark.skip(reason="We do not want java on the build server")
class TestSearch:
    """Simple search tests."""

    def test_wrong_json(self, vgc, manager):
        """Test."""
        _ = manager.create_a_graph(10)
        req = {}
        req["queryKey"] = {"TEST BUCKET": "TEST INPUT"}
        req["output"] = {"TEST BUCKET": "TEST INPUT"}

        with pytest.raises(HTTPError):
            _ = vgc.search(req)  # This is an invalid search!

    def test_eqtl_bp_less_than_0(self, vgc, manager):
        """Test."""
        _ = manager.create_a_graph(10)

        r: SearchRequest = SearchRequest()
        p: Position = Position(-232, "1")
        r.eqtls = [p]
        r.rsId = "TESTRS0"

        with pytest.raises(TypeError):
            _ = vgc.search(r)  # Your bp must not be -ve!

    # def test_simple_bp38_gene_search(self, vgc, manager):
