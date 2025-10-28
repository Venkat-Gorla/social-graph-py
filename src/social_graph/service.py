"""Business logic and Neo4j operations for the social graph."""
from typing import Any
from dataclasses import asdict
from .db import get_driver
from .models import User, Friendship

# vegorla: what happens if the same user or friendship is created multiple times?
def add_user(user: User, driver=None) -> list[dict[str, Any]]:
    """Create a user node if it doesn't exist."""
    query = """
    MERGE (u:User {username: $username})
    RETURN u.username AS username
    """
    return _run_query(query, {"username": user.username}, driver)

def add_friendship(friendship: Friendship, driver=None) -> list[dict[str, Any]]:
    """Create mutual friendship between two users."""
    query = """
    MATCH (a:User {username: $user1}), (b:User {username: $user2})
    MERGE (a)-[:FRIEND_WITH]->(b)
    MERGE (b)-[:FRIEND_WITH]->(a)
    RETURN a.username AS user1, b.username AS user2
    """
    return _run_query(query, asdict(friendship), driver)

def list_friends(username: str, driver=None) -> list[str]:
    """Return list of friends for given user."""
    query = """
    MATCH (u:User {username: $username})-[:FRIEND_WITH]->(f:User)
    RETURN f.username AS friend
    ORDER BY f.username
    """
    result = _run_query(query, {"username": username}, driver)
    return [r["friend"] for r in result]

# Internal helper, not for external use.
def _run_query(query: str, params: dict[str, Any], driver=None):
    """
        Execute a Cypher query using the provided or default Neo4j driver.
        Always returns a list of result dicts.
    """
    if driver is None:
        driver = get_driver()
    return driver.run_query(query, params)
