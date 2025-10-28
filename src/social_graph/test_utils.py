"""
Test utilities for the social graph project.
Provides helper functions for async test setup and teardown.
"""

from .db_async import get_driver, AsyncNeo4jDriver

async def clear_graph(driver: AsyncNeo4jDriver | None = None) -> None:
    """
    Asynchronously clear all nodes and relationships in the Neo4j graph.

    This is used in integration tests to ensure a clean database state
    before each test run.
    """
    driver = driver or get_driver()
    query = "MATCH (n) DETACH DELETE n"
    await driver.run_query(query)
