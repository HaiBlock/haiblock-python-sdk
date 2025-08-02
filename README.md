# HaiBlock Python SDK

Official Python SDK for HaiBlock - AI Content Optimization Platform for improving company visibility in AI model responses.

## Overview

HaiBlock is a platform that optimizes and hosts content for AI model ingestion, enabling companies to improve their visibility when users interact with AI chatbots like OpenAI, Perplexity, and Anthropic.

## Features

- **Content Upload & Management**: Upload and manage content for AI optimization
- **Content Transformation**: Transform content specifically for AI model consumption
- **AI Model Integration**: Submit content to major AI providers (Amazon Bedrock)
- **Analytics & Monitoring**: Track performance and cost optimization
- **Authentication**: Secure API access with AWS Cognito integration

## Installation

```bash
pip install haiblock
```

## Quick Start

```python
from haiblock import HaiBlockClient

# Initialize client
client = HaiBlockClient(
    api_url="https://api.haiblock.com",
    auth_token="your-auth-token"
)

# Upload content
content = client.upload_file("company-info.txt")

# Transform content for AI consumption
transformed = client.transform_content(content.id)

# Submit to AI providers
submission = client.submit_to_bedrock(content.id)

# Get analytics
analytics = client.get_analytics()
```

## Documentation

- [Installation Guide](docs/installation.md)
- [Authentication](docs/authentication.md)
- [API Reference](docs/api-reference.md)
- [Examples](examples/)

## Examples

See the [examples](examples/) directory for complete usage examples:

- [Basic Usage](examples/basic_usage.py)
- [Content Management](examples/content_management.py)
- [Analytics Dashboard](examples/analytics.py)
- [Authentication Flow](examples/auth_example.py)

## API Reference

### HaiBlockClient

Main client class for interacting with the HaiBlock API.

#### Methods

- `upload_file(file_path)` - Upload a file for processing
- `transform_content(content_id)` - Transform content for AI consumption
- `submit_to_bedrock(content_id)` - Submit content to Amazon Bedrock
- `get_analytics()` - Retrieve analytics data
- `list_content()` - List all uploaded content

## Development

```bash
# Clone the repository
git clone https://github.com/HaiBlock/haiblock-python-sdk.git
cd haiblock-python-sdk

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8 haiblock/
black haiblock/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run linting and tests
6. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- Documentation: https://docs.haiblock.com
- Issues: https://github.com/HaiBlock/haiblock-python-sdk/issues
- Contact: support@haiblock.com