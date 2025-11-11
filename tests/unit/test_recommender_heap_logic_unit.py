import pytest
from src.social_graph.recommender import Recommender

@pytest.mark.asyncio
async def test_heap_keeps_top_k_only(mocker):
    """Ensure only top-k highest scoring candidates are returned in correct order."""
    rec = Recommender(alpha=0.7, beta=0.3)

    # Use mapping so return values depend on candidate (not call order)
    scores = {
        "u1": 0.1,
        "u2": 0.9,
        "u3": 0.3,
        "u4": 0.7,
        "u5": 0.5,
    }
    mocker.patch.object(rec, "compute_score", side_effect=lambda u, cand, mutuals: scores[cand])

    candidates = [{"username": u, "mutual_count": 1} for u in scores.keys()]
    results = await rec._get_top_k_candidates("me", candidates, k=3)

    # Enforce both content and order
    usernames = [r["username"] for r in results]
    assert usernames == ["u2", "u4", "u5"]  # top 3 by score desc

    # Scores must be descending
    assert [r["score"] for r in results] == sorted([r["score"] for r in results], reverse=True)

@pytest.mark.asyncio
async def test_heap_sorts_ties_by_username(mocker):
    """When scores are tied, usernames should sort alphabetically (ordering enforced)."""
    rec = Recommender(alpha=0.7, beta=0.3)

    # All same score -> deterministic alphabetical order expected
    mocker.patch.object(rec, "compute_score", return_value=1.0)

    candidates = [
        {"username": "bob", "mutual_count": 2},
        {"username": "alice", "mutual_count": 3},
        {"username": "carol", "mutual_count": 1},
    ]
    results = await rec._get_top_k_candidates("me", candidates, k=3)

    usernames = [r["username"] for r in results]
    # MUST be alphabetically ordered because scores tie
    assert usernames == ["alice", "bob", "carol"]

@pytest.mark.asyncio
async def test_heap_called_with_exact_k_ordered(mocker):
    """If candidates <= k, all should be returned and sorted by score desc then username."""
    rec = Recommender(alpha=0.7, beta=0.3)

    # Map per candidate so order is explicit
    score_map = {"x": 0.2, "y": 0.1}
    mocker.patch.object(rec, "compute_score", side_effect=lambda u, cand, mutuals: score_map[cand])

    candidates = [
        {"username": "x", "mutual_count": 1},
        {"username": "y", "mutual_count": 2},
    ]
    results = await rec._get_top_k_candidates("me", candidates, k=5)

    # Enforce ordered return: higher score first
    assert [r["username"] for r in results] == ["x", "y"]
