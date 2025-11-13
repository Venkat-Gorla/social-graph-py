"""
Test utilities for the social graph project.
Provides helper functions for async test setup and teardown.
"""

from .models import User, Friendship
from .db_async import get_driver, AsyncNeo4jDriver
from .service_async import add_user, add_friendship

async def clear_graph(driver: AsyncNeo4jDriver | None = None) -> None:
    """
    Asynchronously clear all nodes and relationships in the Neo4j graph.

    This is used in integration tests to ensure a clean database state
    before each test run.
    """
    driver = driver or get_driver()
    query = "MATCH (n) DETACH DELETE n"
    await driver.run_query(query)

async def setup_test_graph(
        users: list[str], 
        friendships: list[tuple[str, str]]
    ) -> None:
    """
    Asynchronously set up a test graph with given users and friendships.

    Args:
        users: List of usernames to add as User nodes.
        friendships: List of tuples representing friendships (user1, user2).
    """
    for username in users:
        await add_user(User(username))
    for user_a, user_b in friendships:
        await add_friendship(Friendship(user_a, user_b))
