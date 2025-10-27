"""Neo4j database connection wrapper."""
from neo4j import GraphDatabase, basic_auth
from .config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, validate_config

class Neo4jDriver:
    def __init__(self):
        validate_config()
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD),
            max_connection_lifetime=100,
            connection_timeout=10
        )

    def run_query(self, query: str, params: dict | None = None):
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return [r.data() for r in result]

    def close(self):
        self.driver.close()
