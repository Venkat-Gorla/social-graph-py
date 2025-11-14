import networkx as nx
from typing import List, Tuple, Dict, Optional
from .db_async import get_driver, AsyncNeo4jDriver

# --- Helper: fetch snapshot of nodes + edges from Neo4j ---
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

    # vegorla: follow clean code and create small focused functions
    # Fetch nodes to capture isolated users
    node_query = "MATCH (u:User) RETURN u.username AS username"
    node_rows = await driver.run_query(node_query, {})
    nodes = [r["username"] for r in node_rows] if node_rows else []

    # vegorla: apply query optimization to fetch unique key value pairs
    # Fetch friendships (both directions may exist in DB; we store as undirected edges)
    edge_query = """
    MATCH (u:User)-[:FRIEND_WITH]-(v:User)
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

    return nodes, edges


# --- Public: local PageRank fallback ---
async def pagerank_local(
    top_n: int = 10,
    alpha: float = 0.85,
    max_iter: int = 100,
    tol: float = 1e-06,
    driver: Optional[AsyncNeo4jDriver] = None,
) -> List[Tuple[str, float]]:
    """
    Compute PageRank locally (NetworkX) as a fallback when GDS is unavailable.

    Returns:
        List of (username, score) sorted by score desc, then username for tie-breaks.
        Scores are rounded to 3 decimal places for presentation.
    """
    nodes, edges = await _fetch_graph_snapshot(driver)

    # Build undirected graph; NetworkX will deduplicate edges
    G = nx.Graph()
    if nodes:
        G.add_nodes_from(nodes)
    if edges:
        G.add_edges_from(edges)

    if G.number_of_nodes() == 0:
        return []

    # vegorla: the structure of "pr" seems different for try and except cases, also
    # we are accessing it outside the block where it is created. 
    # Can we remove the fallback?

    # Compute PageRank (NetworkX implements the power-iteration algorithm)
    try:
        pr: Dict[str, float] = nx.pagerank(
            G, alpha=alpha, max_iter=max_iter, tol=tol
        )
    except Exception as exc:
        # For robustness in MVP: fall back to degree-based proxy if pagerank fails
        # (e.g., convergence issues on pathological graphs)
        degs = dict(G.degree())
        if not degs:
            return []
        max_deg = max(degs.values()) or 1
        pr = {n: degs[n] / max_deg for n in degs}

    # Stable ordering: sort by score desc, then username asc
    # vegorla: better to use min heap technique and avoid sort of full list
    sorted_items = sorted(
        pr.items(),
        key=lambda it: (-it[1], it[0])  # negative score => descending, then username
    )

    # Normalize or present as-is: keep raw pagerank scores but round for display
    top = sorted_items[:top_n]
    return [(user, round(score, 3)) for user, score in top]
