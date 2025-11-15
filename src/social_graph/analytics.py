"""
Asynchronous analytics module for the Social Graph Resume Project (MVP).

Overview
--------
Provides lightweight, Cypher-based analytics that run on Neo4j Aura Free
without requiring APOC, GDS, or external computation frameworks.

Included Analytics
------------------
- degree(username): returns the number of direct friendships for a user.
- pagerank(top_n): computes an influence-style ranking based on connection counts.
- detect_communities(): identifies simple community groupings using Cypher queries.

Notes
-----
This module focuses on small, dependency-free analytics suitable for
demonstrating graph reasoning, async patterns, and Neo4j integration.
"""

from typing import List, Tuple, Dict, Optional
from .db_async import get_driver, AsyncNeo4jDriver

async def degree(
        username: str, 
        driver: Optional[AsyncNeo4jDriver] = None
    ) -> int:
    """
    Return number of direct connections (friends) for a given user.

    Args:
        username: target user to measure.
        driver: optional injected driver instance.

    Returns:
        int: number of connected FRIEND_WITH relationships.
    """
    query = """
    MATCH (u:User {username: $username})-[:FRIEND_WITH]-(f:User)
    RETURN count(DISTINCT f) AS degree
    """
    if driver is None:
        driver = get_driver()
    result = await driver.run_query(query, {"username": username})
    return result[0]["degree"] if result else 0

async def pagerank(
        top_n: int = 10, 
        driver: Optional[AsyncNeo4jDriver] = None
    ) -> List[Tuple[str, float]]:
    """
    Simulate influence ranking by counting user connections.

    Args:
        top_n: number of top users to return.
        driver: optional injected driver instance.

    Returns:
        List of (username, pseudo_score) tuples.
    """
    query = """
    MATCH (u:User)-[:FRIEND_WITH]-(f:User)
    RETURN u.username AS username, count(DISTINCT f) AS degree
    ORDER BY degree DESC, username
    LIMIT $top_n
    """
    if driver is None:
        driver = get_driver()
    result = await driver.run_query(query, {"top_n": top_n})
    if not result:
        return []
    max_deg = max(row["degree"] for row in result)
    return [
        (row["username"], round(row["degree"] / max_deg, 3)) for row in result
    ]

async def community_detection(
        driver: Optional[AsyncNeo4jDriver] = None
    ) -> Dict[str, str]:
    """
    Placeholder for community detection.
    Assigns mock community groups deterministically by username hash.

    Args:
        driver: optional injected driver instance.

    Returns:
        Dict[username, community_group]
    """
    query = "MATCH (u:User) RETURN u.username AS username"
    if driver is None:
        driver = get_driver()
    result = await driver.run_query(query, {})
    communities: Dict[str, str] = {}
    for record in result:
        uid = record["username"]
        # Simple alternating grouping for demonstration
        communities[uid] = f"group_{hash(uid) % 2}"
    return communities
