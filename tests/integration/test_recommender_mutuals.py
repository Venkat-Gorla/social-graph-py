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
