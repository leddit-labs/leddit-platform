import os
from pathlib import Path
import sys

import pytest
from neo4j import GraphDatabase
from fastapi.testclient import TestClient
from testcontainers.neo4j import Neo4jContainer

from app.database import get_db
from app.main import app


SERVICE_ROOT = Path(__file__).resolve().parents[2]
if str(SERVICE_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVICE_ROOT))

class DockerFriendlyNeo4jContainer(Neo4jContainer):
    def get_container_host_ip(self) -> str:
        return os.environ.get("TESTCONTAINERS_HOST_OVERRIDE", "host.docker.internal")


@pytest.fixture(scope="session")
def neo4j_container() -> Neo4jContainer:
    with DockerFriendlyNeo4jContainer(image="neo4j:5.22") as container:
        yield container


@pytest.fixture(scope="session")
def neo4j_driver(neo4j_container: Neo4jContainer):
    driver = GraphDatabase.driver(
        neo4j_container.get_connection_url(),
        auth=(neo4j_container.username, neo4j_container.password),
    )
    with driver.session() as session:
        session.run("CREATE CONSTRAINT comment_id_unique IF NOT EXISTS FOR (c:Comment) REQUIRE c.id IS UNIQUE")
        session.run("CREATE CONSTRAINT comment_u_id_unique IF NOT EXISTS FOR (c:Comment) REQUIRE c.u_id IS UNIQUE")
    yield driver
    driver.close()


@pytest.fixture(autouse=True)
def clear_database(neo4j_driver):
    with neo4j_driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch, neo4j_driver):
    monkeypatch.setattr("app.main.init_db", lambda: None)
    app.dependency_overrides[get_db] = lambda: neo4j_driver

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()