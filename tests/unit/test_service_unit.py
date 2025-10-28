from unittest.mock import MagicMock
from social_graph.models import User, Friendship
from social_graph import service

def test_add_user_with_injected_driver():
    mock_driver = MagicMock()
    mock_driver.run_query.return_value = [{"username": "alice"}]

    result = service.add_user(User(username="alice"), driver=mock_driver)

    mock_driver.run_query.assert_called_once()
    assert result == [{"username": "alice"}]

def test_add_friendship_executes_expected_query():
    # Arrange
    mock_driver = MagicMock()
    mock_driver.run_query.return_value = [
        {"user1": "alice", "user2": "bob"},
    ]
    friendship = Friendship(user1="alice", user2="bob")

    # Act
    result = service.add_friendship(friendship, driver=mock_driver)

    # Assert
    mock_driver.run_query.assert_called_once_with(
        """
    MATCH (a:User {username: $user1}), (b:User {username: $user2})
    MERGE (a)-[:FRIEND_WITH]->(b)
    MERGE (b)-[:FRIEND_WITH]->(a)
    RETURN a.username AS user1, b.username AS user2
    """,
        {"user1": "alice", "user2": "bob"},
    )
    assert result == [{"user1": "alice", "user2": "bob"}]

def test_list_friends_returns_sorted_list():
    # Arrange
    mock_driver = MagicMock()
    mock_driver.run_query.return_value = [
        {"friend": "bob"},
        {"friend": "charlie"},
    ]

    # Act
    result = service.list_friends("alice", driver=mock_driver)

    # Assert
    mock_driver.run_query.assert_called_once_with(
        """
    MATCH (u:User {username: $username})-[:FRIEND_WITH]->(f:User)
    RETURN f.username AS friend
    ORDER BY f.username
    """,
        {"username": "alice"},
    )
    assert result == ["bob", "charlie"]
