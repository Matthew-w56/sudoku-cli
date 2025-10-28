# Contributing to Sudoku CLI

Thank you for your interest in contributing to Sudoku CLI!

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run tests to ensure everything works: `python -m unittest discover tests/ -v`

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and single-purpose

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PRs
- Aim for good test coverage of core logic

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `python -m unittest discover tests/ -v`
4. Commit with clear messages
5. Push to your fork
6. Submit a pull request with a clear description

## Reporting Bugs

Please include:
- Python version
- Operating system
- Terminal emulator
- Steps to reproduce
- Expected vs actual behavior

## Feature Requests

Feature requests are welcome! Please provide:
- Clear description of the feature
- Use case / motivation
- Any implementation ideas (optional)

## Questions?

Feel free to open an issue for any questions about development or usage.
