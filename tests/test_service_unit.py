from unittest.mock import MagicMock
from social_graph.models import User
from social_graph import service

def test_add_user_with_injected_driver():
    mock_driver = MagicMock()
    mock_driver.run_query.return_value = [{"username": "alice"}]

    result = service.add_user(User(username="alice"), driver=mock_driver)

    mock_driver.run_query.assert_called_once()
    assert result == [{"username": "alice"}]
