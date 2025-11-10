import math
import pytest
from src.social_graph.recommender import Recommender

@pytest.mark.asyncio
async def test_compute_score_math_only(mocker):
    """Test compute_score() math logic using async mocks (no DB)."""

    rec = Recommender(alpha=0.7, beta=0.3)

    # Spy on driver to ensure it's never used
    mock_driver = mocker.spy(rec.driver, "run_query")

    mocker.patch.object(rec, "mutual_friend_count", return_value=3)
    mocker.patch.object(rec, "_get_degree", return_value=50)

    score = await rec.compute_score("alice", "bob")
    expected = 0.7 * 3 - 0.3 * math.log1p(50)
    assert score == round(expected, 4)

    # Ensure no DB calls were made
    mock_driver.assert_not_called()

@pytest.mark.asyncio
async def test_compute_score_zero_cases(mocker):
    rec = Recommender(alpha=0.7, beta=0.3)

    mocker.patch.object(rec, "mutual_friend_count", return_value=0)
    mocker.patch.object(rec, "_get_degree", return_value=0)

    score = await rec.compute_score("alice", "bob")
    assert score == 0.0  # 0 mutuals → 0 score
