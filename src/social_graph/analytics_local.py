import networkx as nx
from typing import List, Tuple, Dict, Optional
from .db_async import get_driver, AsyncNeo4jDriver

# vegorla: community detection using NetworkX
async def pagerank_local(
    top_n: int = 10,
    alpha: float = 0.85,
    max_iter: int = 100,
    tol: float = 1e-06,
    driver: Optional[AsyncNeo4jDriver] = None,
) -> List[Tuple[str, float]]:
    """
    Compute PageRank locally (NetworkX) as a fallback when GDS is unavailable.

    Notes:
        NetworkX implements the power-iteration algorithm — repeatedly updating
        PageRank scores until the change between iterations is below `tol`.

    Returns:
        List of (username, score) sorted by score desc, then username asc.
        Scores are rounded to 3 decimal places for presentation.
    """
    nodes, edges = await _fetch_graph_snapshot(driver)

    G = nx.Graph()
    if nodes:
        G.add_nodes_from(nodes)
    if edges:
        G.add_edges_from(edges)

    if G.number_of_nodes() == 0:
        return []

    # Compute PageRank (no fallback; bubble up errors if any)
    pr: Dict[str, float] = nx.pagerank(
        G, alpha=alpha, max_iter=max_iter, tol=tol
    )

    # Stable ordering: sort by score desc, then username asc
    sorted_items = sorted(
        pr.items(),
        key=lambda it: (-it[1], it[0])
    )

    top = sorted_items[:top_n]
    return [(user, round(score, 3)) for user, score in top]

async def _fetch_graph_snapshot(
    driver: Optional[AsyncNeo4jDriver] = None,
) -> Tuple[List[str], List[Tuple[str, str]]]:
    """
    Return a snapshot of the user graph as (nodes, edges).
    - nodes: list of usernames (includes isolated users)
    - edges: list of (src, dst) username tuples (undirected)
    """
    if driver is None:
        driver = get_driver()

    nodes = await _fetch_user_nodes(driver)
    edges = await _fetch_friend_edges(driver)

    return nodes, edges

async def _fetch_user_nodes(
    driver: AsyncNeo4jDriver,
) -> List[str]:
    """
    Fetch all user nodes from the database.
    """
    node_query = "MATCH (u:User) RETURN u.username AS username"
    node_rows = await driver.run_query(node_query, {})
    return [r["username"] for r in node_rows] if node_rows else []

async def _fetch_friend_edges(
    driver: AsyncNeo4jDriver,
) -> List[Tuple[str, str]]:
    """
    Fetch all friendship edges from the database.
    """

    edge_query = """
    MATCH (u:User)-[:FRIEND_WITH]-(v:User)
    WHERE u.username < v.username
    RETURN u.username AS src, v.username AS dst
    """
    edge_rows = await driver.run_query(edge_query, {})
    edges: List[Tuple[str, str]] = []
    if edge_rows:
        for r in edge_rows:
            src = r["src"]
            dst = r["dst"]
            # ignore self-loops
            if src and dst and src != dst:
                edges.append((src, dst))
    return edges
