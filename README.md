# ConvertKit Python Client

A Python client for the ConvertKit API.

## Installation

```bash
pip install convertkit-py
```

## Configuration

Copy the sample environment file:

```bash
cp .env-sample .env
```

Edit `.env` with your ConvertKit credentials:

```text
CONVERTKIT_API_KEY=your_api_key_here
CONVERTKIT_API_SECRET=your_secret_key_here
CONVERTKIT_FORM_NAME=your_form_name_here
```

## Usage

```python
from convertkit import ConvertKit
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the client
kit = ConvertKit(
    api_key=os.getenv('CONVERTKIT_API_KEY'),
    api_secret=os.getenv('CONVERTKIT_API_SECRET'),
    form_name=os.getenv('CONVERTKIT_FORM_NAME')
)

# Create a subscriber
subscriber_data = {
    'email': 'example@example.com',
    'fields': {'first_name': 'John'},
    'tags': ['tag1', 'tag2']
}
kit.create_subscriber_with_fields_and_tags(subscriber_data)
```

## Features

- Manage subscribers
- Handle custom fields 
- Manage tags
- Work with forms
- Full API coverage

## Development

### Setup

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Install test dependencies: `pip install pytest python-dotenv`

### Running Tests

1. Create a `.env` file in the project root:
```text
KIT_API_KEY=your_api_key_here
KIT_API_SECRET=your_secret_here
```

2. Run tests:
```bash
pytest tests -v
```

## License

MIT License
