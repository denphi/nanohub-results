"""
Pytest configuration and fixtures for nanohub-results tests.
"""
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_session():
    """Create a mock nanohubremote.Session for testing."""
    session = Mock()
    session.requestGet = Mock()
    session.requestPost = Mock()
    return session


@pytest.fixture
def mock_tool_schema():
    """Mock tool schema response."""
    return {
        'success': True,
        'results': [{
            '2dfets': {
                'input': {
                    'Ef': {'type': 'number'},
                    'Lg': {'type': 'number'},
                    'temperature': {'type': 'number'}
                },
                'output': {
                    'f41': {'type': 'curve'},
                    'f42': {'type': 'curve'},
                    'f11': {'type': 'number'}
                }
            }
        }]
    }


@pytest.fixture
def mock_search_response():
    """Mock search response with results."""
    return {
        'success': True,
        'results': [
            {
                'squid': '2dfets/8/abc123',
                'input.Ef': 0.3,
                'input.Lg': 20,
                'output.f41': {
                    'xaxis': [0, 1, 2],
                    'yaxis': [0, 0.5, 1]
                }
            },
            {
                'squid': '2dfets/8/def456',
                'input.Ef': 0.35,
                'input.Lg': 25,
                'output.f41': {
                    'xaxis': [0, 1, 2],
                    'yaxis': [0, 0.6, 1.2]
                }
            }
        ],
        'searchTime': 0.123
    }


@pytest.fixture
def mock_download_response():
    """Mock download response."""
    return {
        'function': [1.0, 2.0, 3.0, 4.0, 5.0],
        'xaxis': [0, 1, 2, 3, 4],
        'yaxis': [1.0, 2.0, 3.0, 4.0, 5.0]
    }
