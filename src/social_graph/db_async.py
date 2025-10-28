"""Async Neo4j database connection wrapper."""
from neo4j import AsyncGraphDatabase, AsyncDriver, basic_auth
from .config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, validate_config

class AsyncNeo4jDriver:
    """Manages an asynchronous Neo4j driver instance."""

    def __init__(self):
        validate_config()
        self.driver: AsyncDriver = AsyncGraphDatabase.driver(
            NEO4J_URI,
            auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD),
            max_connection_lifetime=100,
            connection_timeout=10
        )

    async def run_query(self, query: str, params: dict | None = None) -> list[dict]:
        """Execute a Cypher query asynchronously and return result records as dicts."""
        async with self.driver.session() as session:
            result = await session.run(query, params or {})
            records = []
            async for record in result:
                records.append(record.data())
            return records

    async def close(self):
        """Close the underlying driver asynchronously."""
        await self.driver.close()

# Singleton instance
_driver_instance: AsyncNeo4jDriver | None = None

def get_driver() -> AsyncNeo4jDriver:
    """Return the singleton async Neo4j driver instance."""
    global _driver_instance
    if _driver_instance is None:
        _driver_instance = AsyncNeo4jDriver()
    return _driver_instance

async def close_driver():
    """Close and reset the global driver instance."""
    global _driver_instance
    if _driver_instance is not None:
        await _driver_instance.close()
        _driver_instance = None
