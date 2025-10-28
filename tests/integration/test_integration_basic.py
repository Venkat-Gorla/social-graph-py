"""Basic integration test for the social graph service."""

"""
To run this test using uv, from root folder:
uv run pytest -s tests/test_integration_basic.py
(-s lets you see the print() output.)
"""

import pytest
from social_graph.models import User, Friendship
from social_graph.db_async import get_driver, close_driver
from social_graph.service_async import (
    add_user,
    add_friendship,
    list_friends,
)
from social_graph.test_utils import clear_graph

@pytest.mark.asyncio
async def test_basic_graph_flow_async():
    """Async integration test for the social graph service."""
    # Clear all data before running async test
    async_driver = get_driver()
    await clear_graph(async_driver)

    # Create two users
    await add_user(User("alice"))
    await add_user(User("bob"))

    # Add friendship
    await add_friendship(Friendship("alice", "bob"))

    # Verify both directions
    alice_friends = await list_friends("alice")
    bob_friends = await list_friends("bob")

    assert "bob" in alice_friends
    assert "alice" in bob_friends
    print("Async Integration test passed: Alice <-> Bob")

    await close_driver()
