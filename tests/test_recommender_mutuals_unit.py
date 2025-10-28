import pytest
import pytest_asyncio
from src.social_graph.recommender import Recommender

class MockDriver:
    """Mock async driver to simulate Neo4j query results."""
    async def run_query(self, query: str, params: dict) -> list[dict]:
        if params == {"user_a": "alice", "user_b": "bob"}:
            return [{"mutual_count": 3}]
        elif params == {"user_a": "alice", "user_b": "carol"}:
            return [{"mutual_count": 0}]
        return []

@pytest_asyncio.fixture
async def recommender():
    return Recommender(driver=MockDriver())

@pytest.mark.asyncio
async def test_mutual_friend_count_positive(recommender):
    count = await recommender.mutual_friend_count("alice", "bob")
    assert count == 3

@pytest.mark.asyncio
async def test_mutual_friend_count_zero(recommender):
    count = await recommender.mutual_friend_count("alice", "carol")
    assert count == 0

@pytest.mark.asyncio
async def test_mutual_friend_count_no_result(recommender):
    count = await recommender.mutual_friend_count("foo", "bar")
    assert count == 0
