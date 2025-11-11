"""
Asynchronous Friend Recommendation Engine for the Social Graph.
---------------------------------------------------------------

This module provides algorithms to suggest new connections
based on mutual friends, 2nd-degree relationships, and
simple scoring heuristics.

All methods are asynchronous and integrate with the shared
AsyncNeo4jDriver for non-blocking Neo4j operations.
"""

import math
import heapq
from typing import Any, List, Dict, Optional
from .db_async import get_driver, AsyncNeo4jDriver

class Recommender:
    """
    Core asynchronous friend recommendation engine.
    
    Attributes:
        driver: Optional shared async Neo4j driver.
        alpha: Weight for mutual friend count in scoring.
        beta:  Weight for degree normalization penalty.
    """

    def __init__(
        self,
        driver: Optional[AsyncNeo4jDriver] = None,
        alpha: float = 0.7,
        beta: float = 0.3,
    ):
        self.driver = driver or get_driver()
        self.alpha = alpha
        self.beta = beta

    # -------------------------------
    # Core Relationship Utilities
    # -------------------------------

    async def mutual_friend_count(self, user_a: str, user_b: str) -> int:
        """
        Count mutual friends between two users (server-side aggregation).
        Returns an integer count.
        """
        query = """
        MATCH (a:User {username: $user_a})-[:FRIEND_WITH]-(f:User)-[:FRIEND_WITH]-(b:User {username: $user_b})
        WHERE a <> b
        RETURN count(DISTINCT f) AS mutual_count
        """
        params = {"user_a": user_a, "user_b": user_b}
        result = await self.driver.run_query(query, params)
        if not result:
            return 0
        return result[0].get("mutual_count", 0)

    async def list_mutual_friends(self, user_a: str, user_b: str) -> List[str]:
        """
        Return usernames of mutual friends between two users.
        """
        query = """
        MATCH (a:User {username: $user_a})-[:FRIEND_WITH]-(f:User)-[:FRIEND_WITH]-(b:User {username: $user_b})
        WHERE a <> b
        RETURN DISTINCT f.username AS mutual_friend
        ORDER BY f.username
        """
        params = {"user_a": user_a, "user_b": user_b}
        result = await self._run_query(query, params)
        return [r["mutual_friend"] for r in result if "mutual_friend" in r]

    # -------------------------------
    # Recommendation Algorithms
    # -------------------------------

    async def suggest_friends_2nd_degree(
        self, username: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Suggest friends-of-friends not already connected to the user.

        Returns a list of dicts:
        [
            {"username": "bob", "mutual_count": 3},
            {"username": "carol", "mutual_count": 2},
        ]
        """
        query = """
        MATCH (u:User {username: $username})-[:FRIEND_WITH]-(f:User)-[:FRIEND_WITH]-(fof:User)
        WHERE NOT (u)-[:FRIEND_WITH]-(fof) AND fof <> u
        WITH DISTINCT fof, f
        RETURN fof.username AS username, COUNT(DISTINCT f) AS mutual_count
        ORDER BY mutual_count DESC, username
        LIMIT $limit
        """
        params = {"username": username, "limit": limit}
        result = await self._run_query(query, params)
        return [
            {"username": r["username"], "mutual_count": r["mutual_count"]}
            for r in result if "username" in r
        ]

    async def compute_score(
        self, user: str, candidate: str, mutual_count: Optional[int] = None
    ) -> float:
        """
        Compute recommendation score combining mutual friend count (positive factor)
        and degree normalization penalty (negative factor).

        Formula:
            score = α * mutual_count - β * log(1 + degree(candidate))
        """
        if mutual_count is None:
            mutual_count = await self.mutual_friend_count(user, candidate)
        degree = await self._get_degree(candidate)

        # Defensive: avoid log(0)
        degree_penalty = math.log1p(degree)

        score = self.alpha * mutual_count - self.beta * degree_penalty
        return round(score, 4)

    async def recommend_top_k(
        self, username: str, k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Generate top-k ranked friend recommendations for a user.

        Uses:
          - suggest_friends_2nd_degree() for candidate discovery
          - compute_score() for ranking

        Returns a list of dicts with scoring metadata:
        [
            {"username": "bob", "score": 0.85, "mutuals": 3},
            {"username": "carol", "score": 0.65, "mutuals": 2},
        ]
        """
        # Step 1: discover 2nd-degree candidates
        candidates = await self.suggest_friends_2nd_degree(username, limit=k * 3)
        if not candidates:
            return []

        # Step 2: get top-k without doing a full sort
        return await self._get_top_k_candidates(username, candidates, k)

    # -------------------------------
    # Internal Helpers
    # -------------------------------

    async def _get_degree(self, username: str) -> int:
        """
        Internal helper: return number of friends (degree) for a user.
        Used in score normalization.
        """
        query = """
        MATCH (u:User {username: $username})-[:FRIEND_WITH]-(f:User)
        RETURN count(DISTINCT f) AS degree
        """
        result = await self._run_query(query, {"username": username})
        if not result:
            return 0
        return result[0].get("degree", 0)

    async def _get_top_k_candidates(
        self, username: str, candidates: List[Dict[str, Any]], k: int
    ) -> List[Dict[str, Any]]:
        """
        Internal helper to compute scores and return only the top-K candidates.
        Uses a bounded heap for efficiency.
        """
        scored_heap = []

        for c in candidates:
            candidate_username = c["username"]
            mutuals = c["mutual_count"]

            score = await self.compute_score(username, candidate_username, mutuals)

            item = (score, candidate_username, mutuals)
            if len(scored_heap) < k:
                heapq.heappush(scored_heap, item)
            else:
                # Keep only top-K highest scoring entries
                heapq.heappushpop(scored_heap, item)

        # Convert heap into sorted descending list by score, ascending username
        scored = [
            {"username": uname, "score": sc, "mutuals": m}
            for sc, uname, m in sorted(scored_heap, key=lambda x: (-x[0], x[1]))
        ]

        return scored

    async def _run_query(self, query: str, params: dict[str, Any]) -> list[dict]:
        """
        Execute an asynchronous Cypher query using the shared driver.
        """
        return await self.driver.run_query(query, params)
