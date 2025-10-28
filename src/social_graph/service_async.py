"""Asynchronous business logic and Neo4j operations for the social graph."""
from typing import Any
from dataclasses import asdict
from .db_async import get_driver
from .models import User, Friendship

# vegorla unit tests using mocks for these functions
async def add_user(user: User, driver=None) -> list[dict[str, Any]]:
    """Asynchronously create a user node if it doesn't exist."""
    query = """
    MERGE (u:User {username: $username})
    RETURN u.username AS username
    """
    return await _run_query(query, {"username": user.username}, driver)

async def add_friendship(friendship: Friendship, driver=None) -> list[dict[str, Any]]:
    """Asynchronously create mutual friendship between two users."""
    query = """
    MATCH (a:User {username: $user1}), (b:User {username: $user2})
    MERGE (a)-[:FRIEND_WITH]->(b)
    MERGE (b)-[:FRIEND_WITH]->(a)
    RETURN a.username AS user1, b.username AS user2
    """
    return await _run_query(query, asdict(friendship), driver)

async def list_friends(username: str, driver=None) -> list[str]:
    """Asynchronously return list of friends for given user."""
    query = """
    MATCH (u:User {username: $username})-[:FRIEND_WITH]->(f:User)
    RETURN f.username AS friend
    ORDER BY f.username
    """
    result = await _run_query(query, {"username": username}, driver)
    return [r["friend"] for r in result]

# Internal helper, not for external use.
async def _run_query(query: str, params: dict[str, Any], driver=None):
    """
    Execute a Cypher query asynchronously using the provided or default Neo4j driver.
    Always returns a list of result dicts.
    """
    if driver is None:
        driver = get_driver()
    return await driver.run_query(query, params)
