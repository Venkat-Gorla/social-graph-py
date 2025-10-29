import pytest
from social_graph.models import User, Friendship
from social_graph.db_async import get_driver, close_driver
from social_graph.service_async import (
    add_user,
    add_friendship,
)
from social_graph.test_utils import clear_graph
from social_graph.recommender import Recommender

@pytest.mark.asyncio
async def test_recommender_mutual_count():
    # Clear all data before running async test
    # consider having test setup and cleanup fixture
    async_driver = get_driver()
    await clear_graph(async_driver)

    users = ["alice", "bob", "charlie"]
    friendships = [
        ("alice", "bob"),
        ("bob", "charlie"),
    ]
    await _create_graph_mutuals(users, friendships)

    recommender = Recommender(driver=async_driver)
    mutual_count = await recommender.mutual_friend_count("alice", "charlie")
    assert mutual_count == 1  # Bob is the mutual friend

    await close_driver()

async def _create_graph_mutuals(users, friendships):
    for username in users:
        await add_user(User(username))

    for user_a, user_b in friendships:
        await add_friendship(Friendship(user_a, user_b))
