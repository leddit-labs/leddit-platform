import os

from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def get_db():
    try:
        yield driver
    finally:
        pass


def init_db() -> None:
    with driver.session() as session:
        session.run(
            "CREATE CONSTRAINT comment_id_unique IF NOT EXISTS FOR (c:Comment) REQUIRE c.id IS UNIQUE"
        )


def check_db_connection() -> bool:
    with driver.session() as session:
        result = session.run("RETURN 1 AS ok").single()
        return result is not None and result["ok"] == 1
