import pytest
from src.sender import tinybird_sender
from unittest.mock import patch
import requests

@patch('src.sender.tinybird_sender.requests.post')
def test_send_to_tinybird_success(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'result': 'ok'}
    mock_post.return_value.raise_for_status = lambda: None
    result = tinybird_sender.send_to_tinybird([{'a': 1}], 'test_ds')
    assert result is True

@patch('src.sender.tinybird_sender.requests.post')
def test_send_to_tinybird_failure(mock_post):
    mock_post.side_effect = requests.exceptions.RequestException("API error")
    result = tinybird_sender.send_to_tinybird([{'a': 1}], 'test_ds')
    assert result is False 