import pytest
from src.fetcher import fetcher
from unittest.mock import patch
import requests

def test_get_date_values():
    now, prev = fetcher.get_date_values(30)
    assert now > prev

@patch('src.fetcher.fetcher.requests.get')
def test_fetch_data_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'indicator': {'name': 'test', 'id': 1, 'values_updated_at': 'now', 'values': []}}
    mock_get.return_value.raise_for_status = lambda: None
    result = fetcher.fetch_data(1, {})
    assert 'indicator' in result

@patch('src.fetcher.fetcher.requests.get')
def test_fetch_data_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("API error")
    result = fetcher.fetch_data(1, {})
    assert result is None