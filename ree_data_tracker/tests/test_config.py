from src.config import config
from unittest.mock import mock_open, patch

def test_select_token():
    fake_yaml = """
credentials:
  tinybird: "token123"
  ree_api: "token456"
"""
    with patch("builtins.open", mock_open(read_data=fake_yaml)):
        token = config.select_token('tinybird')
        assert token == "token123" 

def get_headers():
    TOKEN = config.select_token(key='tinybird')
    return {'Authorization': f'Bearer {TOKEN}'}


