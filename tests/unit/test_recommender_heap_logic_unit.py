import pytest
from src.social_graph.recommender import Recommender

@pytest.mark.asyncio
async def test_heap_keeps_top_k_only(mocker):
    """Ensure only top-k highest scoring candidates are returned."""
    rec = Recommender(alpha=0.7, beta=0.3)

    # Mock compute_score to return predictable scores
    scores = {
        "u1": 0.1,
        "u2": 0.9,
        "u3": 0.3,
        "u4": 0.7,
        "u5": 0.5,
    }
    mocker.patch.object(
        rec, "compute_score",
        side_effect=lambda u, cand: scores[cand]
    )

    candidates = [{"username": u, "mutual_count": 1} for u in scores.keys()]
    results = await rec._get_candidates_scoring_data("me", candidates, k=3)

    usernames = [r["username"] for r in results]
    expected = ["u2", "u4", "u5"]  # top 3 by score desc
    assert usernames == expected
    # Ensure scores are descending
    assert [r["score"] for r in results] == sorted([r["score"] for r in results], reverse=True)

@pytest.mark.asyncio
async def test_heap_sorts_ties_by_username(mocker):
    """When scores are tied, usernames should sort alphabetically."""
    rec = Recommender(alpha=0.7, beta=0.3)
    mocker.patch.object(rec, "compute_score", return_value=1.0)

    candidates = [
        {"username": "bob", "mutual_count": 2},
        {"username": "alice", "mutual_count": 3},
        {"username": "carol", "mutual_count": 1},
    ]
    results = await rec._get_candidates_scoring_data("me", candidates, k=3)
    usernames = [r["username"] for r in results]
    assert usernames == ["alice", "bob", "carol"]  # alphabetical since scores equal

@pytest.mark.asyncio
async def test_heap_called_with_exact_k(mocker):
    """If candidates <= k, all should be returned (no pop)."""
    rec = Recommender(alpha=0.7, beta=0.3)
    mocker.patch.object(rec, "compute_score", side_effect=[0.1, 0.2])

    candidates = [
        {"username": "x", "mutual_count": 1},
        {"username": "y", "mutual_count": 2},
    ]
    results = await rec._get_candidates_scoring_data("me", candidates, k=5)
    assert len(results) == 2
    assert {"x", "y"} == {r["username"] for r in results}
