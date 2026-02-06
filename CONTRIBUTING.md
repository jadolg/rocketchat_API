# Contributing

Thank you for your interest in contributing to rocketchat_API. This document outlines the guidelines for contributing to the project.


## Pull Requests

Contributions are welcome via pull requests. It may take some time to review and merge your code, but quality contributions will be merged.

### Requirements

Before submitting a pull request, ensure the following:

1. **Tests are required.** All new code must include corresponding tests. Pull requests without adequate test coverage will not be merged.

2. **Code must be formatted with black.** This project uses [black](https://github.com/psf/black) for code formatting. Run `black .` before committing. The CI pipeline will reject improperly formatted code.

3. **Tests must pass.** All pull requests are tested against the latest Rocket.Chat version. Verify that your tests pass locally before submitting.

4. **Maintain coverage.** Ensure that your changes do not decrease the overall test coverage.

### Formatting Your Code

```bash
black .
```

### Running Tests

```bash
docker compose up -d
until curl --silent http://localhost:3000/api/info/; do sleep 15; done
pytest
docker compose down
```


## Reporting Issues

Reporting bugs and requesting features is also a valuable contribution. Feel free to open issues to help improve the project.


## Community

Join the discussion at [#python_rocketchat_api](https://open.rocket.chat/channel/python_rocketchat_api) on the Rocket.Chat community server.


## Code of Conduct

Be respectful and considerate of others. Have fun and be nice to each other.
