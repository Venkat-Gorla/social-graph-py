"""Basic integration test for the social graph service."""

"""
To run this test using uv, from root folder:
uv run pytest -s tests/test_integration_basic.py
(-s lets you see the print() output.)
"""

import pytest
from social_graph.models import User, Friendship
from social_graph.service import add_user, add_friendship, list_friends
from social_graph.db import get_driver
from social_graph.service_async import add_user as add_user_async, add_friendship as add_friendship_async, list_friends as list_friends_async
from social_graph.db_async import close_driver as close_driver_async

def clear_graph():
    """Remove all nodes and relationships in the graph."""
    drv = get_driver()
    drv.run_query("MATCH (n) DETACH DELETE n")

# to run this test, remove the __ prefix
def __test_basic_graph_flow():
    """Sync integration test for reference."""
    clear_graph()
    add_user(User("alice"))
    add_user(User("bob"))
    add_friendship(Friendship("alice", "bob"))
    alice_friends = list_friends("alice")
    bob_friends = list_friends("bob")
    assert "bob" in alice_friends
    assert "alice" in bob_friends
    print("Integration test passed: Alice <-> Bob (sync)")

@pytest.mark.asyncio
async def test_basic_graph_flow_async():
    """Async integration test for the social graph service."""
    # Clear all data before running async test
    from social_graph.db_async import get_driver
    async_driver = get_driver()
    await async_driver.run_query("MATCH (n) DETACH DELETE n")

    # Create two users
    await add_user_async(User("alice"))
    await add_user_async(User("bob"))

    # Add friendship
    await add_friendship_async(Friendship("alice", "bob"))

    # Verify both directions
    alice_friends = await list_friends_async("alice")
    bob_friends = await list_friends_async("bob")

    assert "bob" in alice_friends
    assert "alice" in bob_friends
    print("Async Integration test passed: Alice <-> Bob")

    await close_driver_async()
