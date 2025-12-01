# Testing Quick Reference

## Running Tests - No Token Required!

The unit tests use **mocks** and don't require a real nanoHUB token:

```bash
# Install dependencies
pip install -e ".[dev]"

# Run all unit tests (no token needed)
pytest

# Run with coverage
pytest --cov=nanohubresults --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Test Types

### Unit Tests (Default - No Token)
- Mock all API calls
- Run by default
- Fast and reliable
- No network access needed

```bash
# Run only unit tests
pytest -m "not integration"
```

### Integration Tests (Token Required)
- Make real API calls
- Require NANOHUB_TOKEN environment variable
- Slower but test real behavior
- Skipped automatically if no token

```bash
# Set token
export NANOHUB_TOKEN="479a2e9a1542ee54cfc1dbbf59bbe2f83bf8154c"

# Run integration tests
pytest -m integration

# Run all tests (unit + integration)
pytest
```

## Quick Commands

```bash
# Run specific test file
pytest tests/test_query.py

# Run specific test class
pytest tests/test_query.py::TestQueryFiltering

# Run specific test
pytest tests/test_query.py::TestQueryFiltering::test_filter_valid_field

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run tests matching pattern
pytest -k "filter"
```

## Common Scenarios

**Just checking if tests pass:**
```bash
pytest
```

**Developing a new feature:**
```bash
# Run tests in watch mode
pip install pytest-watch
ptw
```

**Before committing:**
```bash
# Run all tests with coverage
pytest --cov=nanohubresults --cov-report=term-missing

# Format code
black nanohubresults tests
isort nanohubresults tests
```

**Testing with real API:**
```bash
export NANOHUB_TOKEN="your_token"
pytest tests/test_integration.py -v
```

## Understanding Test Output

```
tests/test_query.py::TestQueryFiltering::test_filter_valid_field PASSED [10%]
```

- `PASSED` ✓ - Test passed
- `FAILED` ✗ - Test failed
- `SKIPPED` ⊘ - Test was skipped
- `ERROR` ⚠ - Error in test setup

## Coverage Report

```bash
pytest --cov=nanohubresults --cov-report=term-missing
```

Output shows:
- `Stmts` - Total statements
- `Miss` - Statements not covered
- `Cover` - Coverage percentage
- `Missing` - Line numbers not covered

## Troubleshooting

**Import errors:**
```bash
pip install -e .
```

**Missing dependencies:**
```bash
pip install -e ".[dev]"
```

**Tests fail with "No module named 'nanohubresults'":**
```bash
# Make sure you're in the project root
pwd
# Should show: /path/to/nanohub-results

pip install -e .
```

**Integration tests skipped:**
```bash
# This is normal if NANOHUB_TOKEN is not set
# Set the token to run integration tests
export NANOHUB_TOKEN="your_token"
```

## Summary

- **Default: No token needed** - Unit tests use mocks
- **Integration: Token required** - Set `NANOHUB_TOKEN` environment variable
- **Quick test:** `pytest` (runs all unit tests)
- **Full test:** `export NANOHUB_TOKEN="..." && pytest` (runs all tests)
