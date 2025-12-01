# Testing Guide

This document describes how to run and write tests for the nanohub-results library.

## Setup

Install development dependencies:

```bash
pip install -e ".[dev]"
```

## Running Tests

### Run all tests

```bash
pytest
```

### Run with coverage

```bash
pytest --cov=nanohubresults --cov-report=html
```

Open `htmlcov/index.html` to view the coverage report.

### Run specific tests

```bash
# Run a specific test file
pytest tests/test_query.py

# Run a specific test class
pytest tests/test_query.py::TestQueryFiltering

# Run a specific test method
pytest tests/test_query.py::TestQueryFiltering::test_filter_valid_field
```

### Run with verbose output

```bash
pytest -v
```

### Run tests in parallel

```bash
pip install pytest-xdist
pytest -n auto
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Pytest fixtures and configuration
├── test_query.py        # Tests for Query class
└── test_library.py      # Tests for Results class
```

## Writing Tests

### Test Organization

Tests are organized by class:

- `TestQueryInitialization` - Tests for object initialization
- `TestQueryFiltering` - Tests for filter methods
- `TestQuerySelect` - Tests for select methods
- `TestQueryModifiers` - Tests for limit, offset, sort, etc.
- `TestQueryExecution` - Tests for execute and paginate
- `TestQuerySchema` - Tests for schema methods

### Using Fixtures

Use fixtures from `conftest.py`:

```python
def test_example(mock_session, mock_tool_schema):
    """Test using fixtures."""
    mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

    library = Results(mock_session)
    query = library.query("2dfets", simtool=False)

    assert query.tool == "2dfets"
```

### Mocking API Calls

Always mock API calls in unit tests:

```python
from unittest.mock import Mock

def test_with_mock(mock_session):
    """Test with mocked API response."""
    mock_response = {'success': True, 'results': []}
    mock_session.requestGet.return_value = Mock(json=lambda: mock_response)

    results = Results(mock_session)
    response = results.get_tools(simtool=False)

    assert response['success'] is True
```

### Testing Exceptions

Test that exceptions are raised correctly:

```python
def test_invalid_field(mock_session, mock_tool_schema):
    """Test that invalid field raises ValueError."""
    mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

    library = Results(mock_session)
    query = library.query("2dfets", simtool=False)

    with pytest.raises(ValueError, match="Invalid field"):
        query.filter("invalid.field", ">", 0)
```

## Test Coverage

### Current Coverage

Check current coverage:

```bash
pytest --cov=nanohubresults --cov-report=term-missing
```

### Coverage Goals

- Overall: > 90%
- Critical paths: 100%
- Error handling: 100%

### Viewing Coverage Report

Generate HTML coverage report:

```bash
pytest --cov=nanohubresults --cov-report=html
open htmlcov/index.html
```

## Integration Tests

Integration tests make real API calls and require a valid nanoHUB token.

### Setting Up for Integration Tests

Set your nanoHUB token as an environment variable:

```bash
export NANOHUB_TOKEN="your_token_here"
```

Or on Windows:

```cmd
set NANOHUB_TOKEN=your_token_here
```

### Running Integration Tests

Run only integration tests:

```bash
pytest -m integration
```

Skip integration tests (default for unit tests):

```bash
pytest -m "not integration"
```

Run all tests including integration:

```bash
export NANOHUB_TOKEN="your_token"
pytest
```

### Writing Integration Tests

Integration tests are marked with `@pytest.mark.integration`:

```python
import os
import pytest
from nanohubremote import Session
from nanohubresults import Results

@pytest.fixture
def real_session():
    """Create a real session with API token."""
    token = os.environ.get('NANOHUB_TOKEN')
    if not token:
        pytest.skip("NANOHUB_TOKEN not set")

    auth_data = {
        "grant_type": "personal_token",
        "token": token
    }
    return Session(auth_data, url="https://nanohub.org/api")

@pytest.mark.integration
def test_real_api_call(real_session):
    """Integration test requiring real API credentials."""
    results = Results(real_session)
    query = results.query("2dfets", simtool=False)
    schema = query.schema()
    assert len(schema) > 0
```

Integration tests are automatically skipped if `NANOHUB_TOKEN` is not set.

## Continuous Integration

Tests run automatically on GitHub Actions for:

- Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12
- Ubuntu, macOS, Windows

See `.github/workflows/tests.yml` for configuration.

## Best Practices

1. **One assertion per test** - Keep tests focused
2. **Descriptive names** - Test names should describe what they test
3. **Arrange-Act-Assert** - Structure tests clearly
4. **Mock external dependencies** - Don't make real API calls
5. **Test edge cases** - Include boundary conditions
6. **Test error paths** - Verify error handling

## Example Test

```python
def test_filter_multiple_conditions(mock_session, mock_tool_schema):
    """Test adding multiple filter conditions."""
    # Arrange
    mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)
    library = Results(mock_session)
    query = library.query("2dfets", simtool=False)

    # Act
    query.filter("input.Ef", ">", 0.2)
    query.filter("input.Ef", "<", 0.4)
    query.filter("input.Lg", ">", 15)

    # Assert
    assert len(query._filters) == 3
    assert query._filters[0]["field"] == "input.Ef"
    assert query._filters[0]["operation"] == ">"
    assert query._filters[0]["value"] == 0.2
```

## Troubleshooting

### Tests fail with import errors

Make sure you installed the package in development mode:

```bash
pip install -e .
```

### Mock not working

Ensure you're patching the right location:

```python
# Patch where the object is used, not where it's defined
with patch('nanohubresults.library.Results.search') as mock_search:
    pass
```

### Coverage not accurate

Clean coverage data and rerun:

```bash
coverage erase
pytest --cov=nanohubresults
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
