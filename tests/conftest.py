import pytest
from unittest.mock import patch, MagicMock
from convertkit import ConvertKit

@pytest.fixture
def mock_kit():
    with patch('convertkit.client.requests') as mock_requests:
        # Mock the requests.get and requests.post methods
        mock_requests.get.return_value = MagicMock(status_code=200, json=lambda: {'custom_fields': [], 'tags': []})
        mock_requests.post.return_value = MagicMock(status_code=200, json=lambda: {'subscription': {'subscriber': {'id': 12345}}})
        
        yield ConvertKit(
            api_key="test_key",
            api_secret="test_secret",
            form_name="Test Form"
        )