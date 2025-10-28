"""Business logic and Neo4j operations for the social graph."""
from typing import Any
from dataclasses import asdict
from .db import get_driver
from .models import User, Friendship

# vegorla: consider how to unit test these functions using mock objects
# should we have async versions of these functions?
# what happens if the same user or friendship is created multiple times?
def add_user(user: User) -> dict[str, Any]:
    """Create a user node if it doesn't exist."""
    query = """
    MERGE (u:User {username: $username})
    RETURN u.username AS username
    """
    return _run_query(query, {"username": user.username})

def add_friendship(friendship: Friendship) -> dict[str, Any]:
    """Create mutual friendship between two users."""
    query = """
    MATCH (a:User {username: $user1}), (b:User {username: $user2})
    MERGE (a)-[:FRIEND_WITH]->(b)
    MERGE (b)-[:FRIEND_WITH]->(a)
    RETURN a.username AS user1, b.username AS user2
    """
    return _run_query(query, asdict(friendship))

def list_friends(username: str) -> list[str]:
    """Return list of friends for given user."""
    query = """
    MATCH (u:User {username: $username})-[:FRIEND_WITH]->(f:User)
    RETURN f.username AS friend
    ORDER BY f.username
    """
    result = _run_query(query, {"username": username})
    return [r["friend"] for r in result]

def _run_query(query: str, params: dict[str, Any]):
    """
        Execute a Cypher query using the shared Neo4j driver. 
        Always returns a list of result dicts.
    """
    driver = get_driver()
    return driver.run_query(query, params)
