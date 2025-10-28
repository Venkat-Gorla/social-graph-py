"""Basic integration test for the social graph service."""

"""
To run this test using uv from root folder:
uv run pytest -s tests/test_integration_basic.py
(-s lets you see the print() output.)
"""

from social_graph.models import User, Friendship
from social_graph.service import add_user, add_friendship, list_friends

def test_basic_graph_flow():
    # Create two users
    add_user(User("alice"))
    add_user(User("bob"))

    # Add friendship
    add_friendship(Friendship("alice", "bob"))

    # Verify both directions
    alice_friends = list_friends("alice")
    bob_friends = list_friends("bob")

    assert "bob" in alice_friends
    assert "alice" in bob_friends
    print("Integration test passed: Alice <-> Bob friendship created successfully.")

# vegorla
# check how this can be integrated into the test suite
def clear_graph():
    from social_graph.db import get_driver
    drv = get_driver()
    drv.run_query("MATCH (n) DETACH DELETE n")
