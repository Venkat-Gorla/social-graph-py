import pytest
from unittest.mock import MagicMock
from social_graph.models import User
from social_graph import service

# vegorla this is not general purpose mock, it will work only for the specific test
@pytest.fixture(autouse=True)
def mock_driver(monkeypatch):
    mock_driver = MagicMock()
    mock_driver.run_query.return_value = [{"username": "alice"}]
    monkeypatch.setattr(service, "get_driver", lambda: mock_driver)
    return mock_driver

def test_add_user(monkeypatch, mock_driver):
    result = service.add_user(User(username="alice"))
    mock_driver.run_query.assert_called_once()
    assert result == [{"username": "alice"}]
