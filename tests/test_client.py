import os
import pytest
from dotenv import load_dotenv
from convertkit import ConvertKit

@pytest.fixture
def kit_client():
    """Create a ConvertKit client fixture."""
    load_dotenv()  # This will load from .env in the package root
    return ConvertKit(
        api_key=os.getenv('CONVERTKIT_API_KEY'),
        api_secret=os.getenv('CONVERTKIT_API_SECRET'),
        form_name="Signup Form"
    )

def test_list_forms(kit_client):
    """Test listing forms."""
    forms = kit_client.list_forms()
    assert isinstance(forms, list)

def test_list_tags(kit_client):
    """Test listing tags."""
    tags = kit_client.list_tags()
    assert isinstance(tags, list)

def test_list_custom_fields(kit_client):
    """Test listing custom fields."""
    fields = kit_client.list_custom_fields()
    assert isinstance(fields, list)