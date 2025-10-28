from unittest.mock import MagicMock
from social_graph.models import User
from social_graph import service

def test_add_user_with_injected_driver():
    mock_driver = MagicMock()
    mock_driver.run_query.return_value = [{"username": "alice"}]

    result = service.add_user(User(username="alice"), driver=mock_driver)

    mock_driver.run_query.assert_called_once()
    assert result == [{"username": "alice"}]

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
