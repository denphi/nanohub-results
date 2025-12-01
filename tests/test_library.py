"""
Unit tests for the Results class.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from nanohubresults.library import Results
from nanohubresults.query import Query


class TestResultsInitialization:
    """Tests for Results initialization."""

    def test_results_init(self, mock_session):
        """Test Results object initialization."""
        results = Results(mock_session)

        assert results.session == mock_session
        assert results.base_api == "results"


class TestResultsQuery:
    """Tests for Results.query() method."""

    def test_query_returns_query_object(self, mock_session, mock_tool_schema):
        """Test that query() returns a Query object."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        results = Results(mock_session)
        query = results.query("2dfets", simtool=False)

        assert isinstance(query, Query)
        assert query.tool == "2dfets"
        assert query._simtool is False

    def test_query_simtool_parameter(self, mock_session):
        """Test query() with simtool parameter."""
        # Mock schema for st4pnjunction
        simtool_schema = {
            'success': True,
            'results': [{
                'st4pnjunction': {
                    'input': {
                        'temperature': {'type': 'number'},
                        'p_len': {'type': 'number'}
                    },
                    'output': {
                        'IV Characteristic': {'type': 'curve'},
                        'Total Current': {'type': 'curve'}
                    }
                }
            }]
        }
        mock_session.requestPost.return_value = Mock(json=lambda: simtool_schema)

        results = Results(mock_session)
        query = results.query("st4pnjunction", simtool=True)

        assert query._simtool is True


class TestResultsGetTools:
    """Tests for Results.get_tools() method."""

    def test_get_tools(self, mock_session):
        """Test getting list of tools."""
        mock_response = {
            'success': True,
            'results': [
                {'tool_id': '2dfets', 'last_version': 'r8'},
                {'tool_id': 'alphafold231', 'last_version': 'r8'}
            ]
        }
        mock_session.requestGet.return_value = Mock(json=lambda: mock_response)

        results = Results(mock_session)
        response = results.get_tools(simtool=False)

        assert response['success'] is True
        assert len(response['results']) == 2
        mock_session.requestGet.assert_called_once()

    def test_get_tools_with_simtool(self, mock_session):
        """Test getting simulation tools only."""
        mock_response = {
            'success': True,
            'results': [{'tool_id': 'st4pnjunction', 'last_version': 'r9'}]
        }
        mock_session.requestGet.return_value = Mock(json=lambda: mock_response)

        results = Results(mock_session)
        response = results.get_tools(simtool=True)

        assert response['success'] is True
        call_args = mock_session.requestGet.call_args[0][0]
        assert 'simtool=true' in call_args


class TestResultsGetToolDetail:
    """Tests for Results.get_tool_detail() method."""

    def test_get_tool_detail(self, mock_session, mock_tool_schema):
        """Test getting tool details."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        results = Results(mock_session)
        response = results.get_tool_detail("2dfets", simtool=False)

        assert response['success'] is True
        assert '2dfets' in response['results'][0]
        mock_session.requestPost.assert_called_once()

    def test_get_tool_detail_with_simtool(self, mock_session, mock_tool_schema):
        """Test getting simtool details."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        results = Results(mock_session)
        response = results.get_tool_detail("st4pnjunction", simtool=True)

        call_args = mock_session.requestPost.call_args
        assert call_args[1]['data']['simtool'] == 1


class TestResultsSearch:
    """Tests for Results.search() method."""

    def test_search_basic(self, mock_session, mock_search_response):
        """Test basic search."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_search_response)

        results = Results(mock_session)
        response = results.search(
            tool="2dfets",
            filters=[{"field": "input.Ef", "operation": ">", "value": 0.2}],
            results_fields=["input.Ef", "output.f41"],
            limit=10
        )

        assert len(response['results']) == 2
        mock_session.requestPost.assert_called_once()

    def test_search_with_simtool(self, mock_session, mock_search_response):
        """Test search with simtool parameter."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_search_response)

        results = Results(mock_session)
        response = results.search(
            tool="st4pnjunction",
            filters=[{"field": "input.temperature", "operation": ">", "value": 0}],
            results_fields=["input.temperature"],
            limit=10,
            simtool=True
        )

        call_args = mock_session.requestPost.call_args
        assert call_args[1]['data']['simtool'] == 1

    def test_search_with_offset(self, mock_session, mock_search_response):
        """Test search with offset."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_search_response)

        results = Results(mock_session)
        response = results.search(
            tool="2dfets",
            filters=[{"field": "input.Ef", "operation": ">", "value": 0.2}],
            results_fields=["input.Ef"],
            limit=10,
            offset=50
        )

        call_args = mock_session.requestPost.call_args
        assert call_args[1]['data']['offset'] == 50

    def test_search_with_sort(self, mock_session, mock_search_response):
        """Test search with sorting."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_search_response)

        results = Results(mock_session)
        response = results.search(
            tool="2dfets",
            filters=[{"field": "input.Ef", "operation": ">", "value": 0.2}],
            results_fields=["input.Ef"],
            limit=10,
            sort="input.Ef",
            sort_asc=False
        )

        call_args = mock_session.requestPost.call_args
        assert call_args[1]['data']['sort'] == "input.Ef"
        assert call_args[1]['data']['sort_asc'] == "false"


class TestResultsGetSquidDetail:
    """Tests for Results.get_squid_detail() method."""

    def test_get_squid_detail(self, mock_session):
        """Test getting SQUID details."""
        mock_response = {
            'success': True,
            'squid': '2dfets/8/abc123',
            'data': {'input.Ef': 0.3}
        }
        mock_session.requestGet.return_value = Mock(json=lambda: mock_response)

        results = Results(mock_session)
        response = results.get_squid_detail("2dfets/8/abc123", simtool=False)

        assert response['success'] is True
        assert response['squid'] == '2dfets/8/abc123'
        mock_session.requestGet.assert_called_once()

    def test_get_squid_detail_xml(self, mock_session):
        """Test getting SQUID details in XML format."""
        mock_session.requestGet.return_value = Mock(json=lambda: {'success': True})

        results = Results(mock_session)
        response = results.get_squid_detail("2dfets/8/abc123", output="xml")

        call_args = mock_session.requestGet.call_args[0][0]
        assert 'output=xml' in call_args


class TestResultsGetSquidFiles:
    """Tests for Results.get_squid_files() method."""

    def test_get_squid_files(self, mock_session):
        """Test getting SQUID files list."""
        mock_response = {
            'success': True,
            'total_files': 2,
            'results': [
                {'id': 1, 'name': 'output.dat', 'size': 1024},
                {'id': 2, 'name': 'data.csv', 'size': 2048}
            ]
        }
        mock_session.requestPost.return_value = Mock(json=lambda: mock_response)

        results = Results(mock_session)
        response = results.get_squid_files("st4pnjunction/r9/abc123", simtool=True)

        assert response['success'] is True
        assert response['total_files'] == 2
        assert len(response['results']) == 2

    def test_get_squid_files_with_simtool(self, mock_session):
        """Test get_squid_files with simtool parameter."""
        mock_session.requestPost.return_value = Mock(json=lambda: {'success': True})

        results = Results(mock_session)
        response = results.get_squid_files("st4pnjunction/r9/abc123", simtool=True)

        call_args = mock_session.requestPost.call_args
        assert call_args[1]['data']['simtool'] == 1


class TestResultsDownload:
    """Tests for Results.download() method."""

    def test_download_by_field(self, mock_session, mock_download_response):
        """Test downloading by field."""
        mock_session.requestGet.return_value = Mock(json=lambda: mock_download_response)

        results = Results(mock_session)
        response = results.download(
            tool="st4pnjunction",
            squid="st4pnjunction/r9/abc123",
            field="output.IV Characteristic",
            simtool=True
        )

        assert 'function' in response
        call_args = mock_session.requestGet.call_args[0][0]
        assert 'field=output.IV+Characteristic' in call_args or 'field=output.IV%20Characteristic' in call_args

    def test_download_by_filename(self, mock_session, mock_download_response):
        """Test downloading by filename."""
        mock_session.requestGet.return_value = Mock(json=lambda: mock_download_response)

        results = Results(mock_session)
        response = results.download(
            tool="st4pnjunction",
            squid="st4pnjunction/r9/abc123",
            file_name="output.dat",
            simtool=True
        )

        call_args = mock_session.requestGet.call_args[0][0]
        assert 'file=output.dat' in call_args

    def test_download_with_simtool(self, mock_session, mock_download_response):
        """Test download with simtool parameter."""
        mock_session.requestGet.return_value = Mock(json=lambda: mock_download_response)

        results = Results(mock_session)
        response = results.download(
            tool="st4pnjunction",
            squid="st4pnjunction/r9/abc123",
            field="output.data",
            simtool=True
        )

        call_args = mock_session.requestGet.call_args[0][0]
        assert 'simtool=1' in call_args


class TestResultsStats:
    """Tests for Results.stats() method."""

    def test_stats(self, mock_session):
        """Test getting statistics."""
        mock_response = {
            'success': True,
            'stats': {
                'total': 100,
                'min': 0.1,
                'max': 0.5,
                'mean': 0.3
            }
        }
        mock_session.requestPost.return_value = Mock(json=lambda: mock_response)

        results = Results(mock_session)
        response = results.stats(
            tool="2dfets",
            filters=[{"field": "input.Ef", "operation": ">", "value": 0}],
            results_fields=["input.Ef"],
            limit=100
        )

        assert response['success'] is True
        assert 'stats' in response
        mock_session.requestPost.assert_called_once()


class TestResultsRecords:
    """Tests for Results.records() method."""

    def test_records(self, mock_session):
        """Test getting record counts."""
        mock_response = {
            'success': True,
            'total_records': 50000,
            'tools': 150
        }
        mock_session.requestGet.return_value = Mock(json=lambda: mock_response)

        results = Results(mock_session)
        response = results.records(simtool=False)

        assert response['success'] is True
        mock_session.requestGet.assert_called_once()

    def test_records_with_simtool(self, mock_session):
        """Test getting records for simtools."""
        mock_session.requestGet.return_value = Mock(json=lambda: {'success': True})

        results = Results(mock_session)
        response = results.records(simtool=True)

        call_args = mock_session.requestGet.call_args[0][0]
        assert 'simtool=1' in call_args
