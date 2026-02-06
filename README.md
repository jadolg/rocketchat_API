# rocketchat_API

Python API wrapper for [Rocket.Chat](https://developer.rocket.chat/reference/api/rest-api/)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fff725d9a0974c6597c2dd007daaa86e)](https://www.codacy.com/app/jadolg/rocketchat_API?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jadolg/rocketchat_API&amp;utm_campaign=Badge_Grade) [![Test](https://github.com/jadolg/rocketchat_API/actions/workflows/test.yml/badge.svg)](https://github.com/jadolg/rocketchat_API/actions/workflows/test.yml) [![Test against latest Rocket.Chat version](https://github.com/jadolg/rocketchat_API/actions/workflows/test_latest.yml/badge.svg)](https://github.com/jadolg/rocketchat_API/actions/workflows/test_latest.yml) [![codecov](https://codecov.io/gh/jadolg/rocketchat_API/branch/master/graph/badge.svg)](https://codecov.io/gh/jadolg/rocketchat_API) ![PyPI](https://img.shields.io/pypi/v/rocketchat_API.svg) ![](https://img.shields.io/pypi/dm/rocketchat-api.svg)


## Installation

**From PyPI (recommended):**

```bash
pip install rocketchat_API
```

**From source:**

```bash
git clone https://github.com/jadolg/rocketchat_API.git
cd rocketchat_API
pip install .
```


## Requirements

- Python 3.10 or higher
- [requests](https://github.com/kennethreitz/requests)


## Compatibility

This library is tested against the following versions:

**Python:** 3.10, 3.11, 3.12, 3.13, 3.14

**Rocket.Chat:** 7.10.x, 7.11.x, 7.12.x, 7.13.x, 8.0.x

The library is also continuously tested against the latest Rocket.Chat release to ensure compatibility with new versions.


## Usage

### Basic Authentication

```python
from rocketchat_API.rocketchat import RocketChat

rocket = RocketChat('user', 'pass', server_url='https://demo.rocket.chat')

# Get current user info
rocket.me()

# List all channels
for channel in rocket.channels_list():
    print(channel.get("name"))

# Post a message
rocket.chat_post_message('good news everyone!', channel='GENERAL', alias='Farnsworth')

# Get channel history
rocket.channels_history('GENERAL', count=5)
```

### Token-Based Authentication

If you already have a user ID and authentication token, you can use them directly:

```python
from rocketchat_API.rocketchat import RocketChat

rocket = RocketChat(
    user_id='WPXGmQ64S3BXdCRb6',
    auth_token='jvNyOYw2f0YKwtiFS06Fk21HBRBBuV7zI43HmkNzI_s',
    server_url='https://demo.rocket.chat'
)

rocket.me()
```

### Method Parameters

Only required parameters are explicitly defined in the RocketChat class methods. However, you can pass any additional parameters supported by the Rocket.Chat API. For a complete list of available parameters, refer to the [official Rocket.Chat API documentation](https://developer.rocket.chat/reference/api/rest-api).

## Development

### Setting Up the Development Environment

1. Clone the repository:

```bash
git clone https://github.com/jadolg/rocketchat_API.git
cd rocketchat_API
```

2. Install development dependencies:

```bash
pip install -e ".[test]"
```

### Running Tests

Tests run against a Rocket.Chat instance in Docker. Make sure you have Docker and Docker Compose installed.

1. Start the test server:

```bash
docker compose up -d
```

2. Wait for Rocket.Chat to be ready:

```bash
until curl --silent http://localhost:3000/api/info/; do sleep 15; echo "waiting for Rocket.Chat server to start"; done
```

3. Run the tests:

```bash
pytest
```

4. To run tests with coverage:

```bash
pytest --cov=rocketchat_API
```

5. When finished, stop the test server:

```bash
docker compose down
```

### Code Style

This project uses [black](https://github.com/psf/black) for code formatting. All code must be formatted with black before submitting a pull request.

To format your code:

```bash
black .
```

To check if your code is properly formatted:

```bash
black --check --diff .
```

The CI pipeline will automatically reject pull requests that are not properly formatted.



## Contributing

Contributions are welcome. Please follow these guidelines:

1. **Tests are required.** All new code must include corresponding tests. Pull requests without adequate test coverage will not be merged.

2. **Code style.** All code must be formatted using [black](https://github.com/psf/black). Run `black .` before committing.

3. **Maintain coverage.** Ensure that your changes do not decrease the overall test coverage.

4. **Pull requests.** It may take some time to review and merge your code, but quality contributions will be merged.

5. **Issues.** Reporting bugs and requesting features is also a valuable contribution. Feel free to open issues.

For more details, see [CONTRIBUTING.md](CONTRIBUTING.md).

Join the discussion at [#python_rocketchat_api](https://open.rocket.chat/channel/python_rocketchat_api) on the Rocket.Chat community server.


## License

This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.


## Supporters

[![JetBrains logo.](https://resources.jetbrains.com/storage/products/company/brand/logos/jetbrains.svg)](https://jb.gg/OpenSourceSupport)

[JetBrains](https://www.jetbrains.com/) supports this project by providing licenses for their development tools.
