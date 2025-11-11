import pytest
import pytest_asyncio
from social_graph.models import User, Friendship
from social_graph.db_async import get_driver, close_driver
from social_graph.service_async import (
    add_user,
    add_friendship,
)
from social_graph.test_utils import clear_graph
from social_graph.recommender import Recommender

@pytest_asyncio.fixture
async def setup_graph():
    driver = get_driver()
    await clear_graph(driver)
    yield driver
    await close_driver()

# vegorla: can we have tests with a more complex graph aka real world?
@pytest.mark.asyncio
async def test_recommender_mutual_friends(setup_graph):
    async_driver = setup_graph

    users = ["alice", "bob", "charlie"]
    friendships = [
        ("alice", "bob"),
        ("bob", "charlie"),
    ]
    await _create_graph_mutuals(users, friendships)

    recommender = Recommender(driver=async_driver)
    mutual_count = await recommender.mutual_friend_count("alice", "charlie")
    assert mutual_count == 1  # Bob is the mutual friend

    # test mutual friends in both directions
    assert await recommender.list_mutual_friends("alice", "charlie") == ["bob"]
    assert await recommender.list_mutual_friends("charlie", "alice") == ["bob"]

async def _create_graph_mutuals(users, friendships):
    for username in users:
        await add_user(User(username))

    for user_a, user_b in friendships:
        await add_friendship(Friendship(user_a, user_b))

@pytest.mark.asyncio
async def test_recommender_suggest_friends(setup_graph):
    async_driver = setup_graph

    # Graph structure:
    # A---B---C
    # A---D---F
    # A---E---F

    users = ["A", "B", "C", "D", "E", "F"]
    friendships = [
        ("A", "B"),
        ("B", "C"),
        ("A", "D"),
        ("D", "F"),
        ("A", "E"),
        ("E", "F"),
    ]
    await _create_graph_mutuals(users, friendships)

    recommender = Recommender(driver=async_driver)
    suggestions = await recommender.suggest_friends_2nd_degree("A", limit=10)
    expected_suggestions = [
        {"username": "F", "mutual_count": 2},
        {"username": "C", "mutual_count": 1},
    ]
    assert suggestions == expected_suggestions

@pytest.mark.asyncio
async def test_recommender_recommend_top_k(setup_graph):
    async_driver = setup_graph

    # Graph structure:
    # A---B---C
    # A---D---F
    # A---E---F
    #
    # Expected second-degree candidates for A:
    #   F (mutuals=2: D,E)
    #   C (mutuals=1: B)
    # F has higher degree penalty (2 friends: D,E)
    # but more mutuals, so should still rank first.

    users = ["A", "B", "C", "D", "E", "F"]
    friendships = [
        ("A", "B"),
        ("B", "C"),
        ("A", "D"),
        ("D", "F"),
        ("A", "E"),
        ("E", "F"),
    ]
    await _create_graph_mutuals(users, friendships)

    recommender = Recommender(driver=async_driver)

    results = await recommender.recommend_top_k("A", k=5)

    # We only expect F and C as candidates; F should rank higher than C
    usernames = [r["username"] for r in results]
    assert usernames == ["F", "C"], "Only F and C should be recommended"

    # Basic sanity checks on score fields
    for rec in results:
        assert "score" in rec
        assert "mutuals" in rec
        assert isinstance(rec["score"], float)
        assert rec["mutuals"] > 0

@pytest.mark.asyncio
async def test_recommender_recommend_top_k_no_candidates(setup_graph):
    async_driver = setup_graph

    # Graph structure:
    # X---Y
    # Z (isolated)
    users = ["X", "Y", "Z"]
    friendships = [("X", "Y")]
    await _create_graph_mutuals(users, friendships)

    recommender = Recommender(driver=async_driver)

    # User Z has no friends at all -> should yield no 2nd-degree connections
    results_z = await recommender.recommend_top_k("Z", k=5)
    assert results_z == [], "Isolated user Z should have no recommendations"

    # User X only has Y, who has no other connections -> also no recommendations
    results_x = await recommender.recommend_top_k("X", k=5)
    assert results_x == [], "User X should have no 2nd-degree candidates"
