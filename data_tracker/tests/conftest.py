import pytest
from unittest.mock import mock_open, patch

@pytest.fixture(autouse=True, scope="session")
def patch_connections_yaml():
    fake_yaml = """
credentials:
  tinybird: "token123"
  ree_api: "token456"
"""
    with patch("builtins.open", mock_open(read_data=fake_yaml)):
        yield 