import pytest
from src.social_graph.recommender import Recommender

@pytest.mark.asyncio
async def test_recommend_top_k_ranking(mocker):
    rec = Recommender(alpha=0.7, beta=0.3)

    # Mock candidate discovery (2nd-degree)
    mocker.patch.object(
        rec,
        "suggest_friends_2nd_degree",
        return_value=[
            {"username": "bob", "mutual_count": 3},
            {"username": "carol", "mutual_count": 2},
            {"username": "dave", "mutual_count": 1},
        ],
    )

    # Mock compute_score to assign custom scores
    async def fake_score(user, candidate, mutuals):
        return {"bob": 0.9, "carol": 0.7, "dave": 0.4}[candidate]

    mocker.patch.object(rec, "compute_score", side_effect=fake_score)

    result = await rec.recommend_top_k("alice", k=2)
    expected = [
        {"username": "bob", "score": 0.9, "mutuals": 3},
        {"username": "carol", "score": 0.7, "mutuals": 2},
    ]

    assert result == expected
