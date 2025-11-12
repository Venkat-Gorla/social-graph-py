# vegorla: check if "distinct" is needed in the Cypher queries in this module

"""
Asynchronous analytics module for Social Graph Resume Project (MVP).

Purpose
-------
Provide minimal, Cypher-only analytics functions compatible with Neo4j Aura Free.

Functions
---------
- degree(username): count direct connections for a given user.
- pagerank(top_n): simulate user influence ranking by connection counts.
- community_detection(): simple placeholder illustrating community concept.

Integration
-----------
Uses the existing async driver abstraction (`get_driver`) from db_async.py.
No direct driver/session management is reimplemented here.

Trade-offs
----------
- No APOC / GDS algorithms (unsupported on Aura Free).
- No NetworkX or local computation fallback (out of MVP scope).
- Simulated PageRank and mock communities to demonstrate understanding.

Future extensions (TODO)
------------------------
- Add real PageRank, Louvain, or Label Propagation using GDS.
- Optionally implement local fallback analytics via NetworkX.
"""

from typing import Any, List, Tuple, Dict
from .db_async import get_driver


async def degree(username: str, driver=None) -> int:
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
    RETURN count(f) AS degree
    """
    if driver is None:
        driver = get_driver()
    result = await driver.run_query(query, {"username": username})
    return result[0]["degree"] if result else 0


async def pagerank(top_n: int = 10, driver=None) -> List[Tuple[str, float]]:
    """
    Simulate influence ranking by counting user connections.

    Args:
        top_n: number of top users to return.
        driver: optional injected driver instance.

    Returns:
        List of (username, pseudo_score) tuples.
    """
    query = """
    MATCH (u:User)-[:FRIEND_WITH]-()
    RETURN u.username AS username, count(*) AS degree
    ORDER BY degree DESC
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


async def community_detection(driver=None) -> Dict[str, str]:
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
