import pytest
from social_graph import analytics_local

@pytest.fixture(autouse=True)
def block_database_access(mocker):
    """
    Automatically applied to all tests in this module.
    Ensures no real DB driver or DB methods are ever called.
    """
    # Prevent driver creation
    mocker.patch.object(
        analytics_local,
        "get_driver",
        side_effect=AssertionError("get_driver() should not be called in unit tests"),
    )

    # Prevent direct DB fetch functions
    mocker.patch.object(
        analytics_local,
        "_fetch_user_nodes",
        side_effect=AssertionError("_fetch_user_nodes should not be called"),
    )
    mocker.patch.object(
        analytics_local,
        "_fetch_friend_edges",
        side_effect=AssertionError("_fetch_friend_edges should not be called"),
    )

@pytest.mark.asyncio
async def test_pagerank_local_basic(mocker):
    # Mock graph snapshot: a -- b -- c
    mock_nodes = ["a", "b", "c"]
    mock_edges = [("a", "b"), ("b", "c")]

    mocker.patch.object(
        analytics_local,
        "_fetch_graph_snapshot",
        return_value=(mock_nodes, mock_edges),
    )

    result = await analytics_local.pagerank_local(top_n=10)

    # Expected sorted order from NetworkX + function sorting rules
    expected_users = ["b", "a", "c"]
    assert [user for user, _ in result] == expected_users

    # Scores should be rounded to 3 decimals
    for _, score in result:
        assert score == round(score, 3)

@pytest.mark.asyncio
async def test_guard_blocks_db_access(mocker):
    """
    Verify that failing to mock _fetch_graph_snapshot triggers
    DB-access guard and raises AssertionError.
    """
    with pytest.raises(AssertionError):
        await analytics_local.pagerank_local()
