"""Wrap a simple version of the graph server for testing."""

import os
import subprocess
import time

import wget


class GraphServer:
    """A *TEST* server which starts a known version of the graph server.

    In order to test against newer versions, one should update the
    server jar file in this repo. This is as simple as going to the
    graph service reop and doing 'mvn package' to get the jar depending
    on unit tests running.
    """

    def __init__(self, user_name, password, bolt_url) -> None:
        """Set up the server ready to start it.

        @param bolt_url: The url to which to attach to the test neo4j database.
                         Of the form: bolt://neo4j:password@ip:port
        """
        self.user_name = user_name
        self.password = password
        self.bolt_url = bolt_url
        self.server_exec = "graph-service-0.4.5.jar"
        self.process = None
        self.server_url = None

    def url(self) -> str:
        """Url used."""
        return self.server_url

    def is_running(self) -> bool:
        """If we are running."""
        if self.process is None:
            return False
        return self.process.poll() is not None

    def start_test_server(self) -> None:
        """Start it."""
        user = "-DNEO4J_USER={}".format("neo4j")
        password = "-DNEO4J_PASS={}".format("password")
        bolt = "-DBOLT_URI={}".format(self.bolt_url)

        if not os.path.exists("./{}".format(self.server_exec)):
            url: str = (
                "https://repo1.maven.org/maven2/org/geneweaver/graph-service/0.4.5/{}".format(
                    self.server_exec
                )
            )
            wget.download(url, out=".")

        # Start test server in disconnected storage mode. This means that large queries
        # will not store back to google storage. It is just for testing.
        cmd = [
            "java",
            "-Dserver.port=8080",
            user,
            password,
            bolt,
            "-DDISCONNECTED_STORAGE=true",
            "-jar",
            self.server_exec,
        ]

        # This process normally needs google credentials in order to
        self.process = subprocess.Popen(
            cmd,
            stdout=open("./test_graph_server_out.log", "w"),
            stderr=open("./test_graph_server_err.log", "w"),
            preexec_fn=os.setpgrp,
        )

        while True:
            if ":: Spring Boot ::" in open("./test_graph_server_out.log").read():
                break
            time.sleep(1)

        self.server_url = "http://localhost:8080/"
        time.sleep(5)

    def stop_test_server(self) -> None:
        """Stop it."""
        try:
            self.process.terminate()
        except Exception:
            # Make sure dead
            self.process.kill()
