"""
Unit tests for the Query class.
"""
import pytest
from unittest.mock import Mock, patch
from nanohubresults.query import Query
from nanohubresults.library import Results


class TestQueryInitialization:
    """Tests for Query initialization."""

    def test_query_init(self, mock_session, mock_tool_schema):
        """Test Query object initialization."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)

        assert query.tool == "2dfets"
        assert query._simtool is False
        assert len(query._valid_fields) > 0
        assert "input.Ef" in query._valid_fields
        assert "output.f41" in query._valid_fields

    def test_query_invalid_tool(self, mock_session):
        """Test Query with invalid tool name."""
        mock_session.requestPost.return_value = Mock(
            json=lambda: {'success': False, 'message': 'Tool not found'}
        )

        library = Results(mock_session)
        with pytest.raises(ValueError, match="Failed to fetch schema"):
            Query(library, "invalid_tool", simtool=False)


class TestQueryFiltering:
    """Tests for Query filtering methods."""

    def test_filter_valid_field(self, mock_session, mock_tool_schema):
        """Test adding a valid filter."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)
        query.filter("input.Ef", ">", 0.2)

        assert len(query._filters) == 1
        assert query._filters[0]["field"] == "input.Ef"
        assert query._filters[0]["operation"] == ">"
        assert query._filters[0]["value"] == 0.2

    def test_filter_invalid_field(self, mock_session, mock_tool_schema):
        """Test adding filter with invalid field."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)

        with pytest.raises(ValueError, match="Invalid field"):
            query.filter("invalid.field", ">", 0)

    def test_filter_invalid_operation(self, mock_session, mock_tool_schema):
        """Test adding filter with invalid operation."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)

        with pytest.raises(ValueError, match="Invalid operation"):
            query.filter("input.Ef", "invalid_op", 0)

    def test_multiple_filters(self, mock_session, mock_tool_schema):
        """Test adding multiple filters."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)
        query.filter("input.Ef", ">", 0.2)
        query.filter("input.Ef", "<", 0.4)
        query.filter("input.Lg", ">", 15)

        assert len(query._filters) == 3


class TestQuerySelect:
    """Tests for Query select method."""

    def test_select_valid_fields(self, mock_session, mock_tool_schema):
        """Test selecting valid fields."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)
        query.select("input.Ef", "output.f41")

        assert len(query._results_fields) == 2
        assert "input.Ef" in query._results_fields
        assert "output.f41" in query._results_fields

    def test_select_invalid_field(self, mock_session, mock_tool_schema):
        """Test selecting invalid field."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)

        with pytest.raises(ValueError, match="Invalid field"):
            query.select("invalid.field")


class TestQueryModifiers:
    """Tests for Query modifier methods."""

    def test_limit(self, mock_session, mock_tool_schema):
        """Test setting limit."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)
        query.limit(100)

        assert query._limit == 100

    def test_offset(self, mock_session, mock_tool_schema):
        """Test setting offset."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)
        query.offset(50)

        assert query._offset == 50

    def test_sort(self, mock_session, mock_tool_schema):
        """Test setting sort."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)
        query.sort("input.Ef", asc=False)

        assert query._sort == "input.Ef"
        assert query._sort_asc is False

    def test_sort_invalid_field(self, mock_session, mock_tool_schema):
        """Test sorting by invalid field."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)

        with pytest.raises(ValueError, match="Invalid sort field"):
            query.sort("invalid.field")


class TestQueryExecution:
    """Tests for Query execution methods."""

    def test_execute_without_filters(self, mock_session, mock_tool_schema):
        """Test executing query without filters."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)

        with pytest.raises(ValueError, match="At least one filter is required"):
            query.execute()

    def test_execute_without_select(self, mock_session, mock_tool_schema):
        """Test executing query without select."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)
        query.filter("input.Ef", ">", 0)

        with pytest.raises(ValueError, match="At least one result field must be selected"):
            query.execute()

    def test_execute_valid_query(self, mock_session, mock_tool_schema, mock_search_response):
        """Test executing valid query."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        library.search = Mock(return_value=mock_search_response)

        query = Query(library, "2dfets", simtool=False)
        query.filter("input.Ef", ">", 0.2)
        query.select("input.Ef", "output.f41")

        response = query.execute()

        assert response == mock_search_response
        assert len(response['results']) == 2

    def test_paginate_without_filters(self, mock_session, mock_tool_schema):
        """Test paginating without filters."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)

        with pytest.raises(ValueError, match="At least one filter is required"):
            list(query.paginate())

    def test_paginate_without_select(self, mock_session, mock_tool_schema):
        """Test paginating without select."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)
        query.filter("input.Ef", ">", 0)

        with pytest.raises(ValueError, match="At least one result field must be selected"):
            list(query.paginate())

    def test_paginate_valid_query(self, mock_session, mock_tool_schema, mock_search_response):
        """Test paginating with valid query."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)

        # Mock search to return results on first call, empty on second
        library.search = Mock(side_effect=[
            mock_search_response,
            {'results': []}
        ])

        query = Query(library, "2dfets", simtool=False)
        query.filter("input.Ef", ">", 0.2)
        query.select("input.Ef", "output.f41")

        results = list(query.paginate(per_page=10))

        assert len(results) == 2
        assert results[0]['squid'] == '2dfets/8/abc123'


class TestQuerySchema:
    """Tests for Query schema method."""

    def test_schema_method(self, mock_session, mock_tool_schema):
        """Test getting schema."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = Query(library, "2dfets", simtool=False)

        schema = query.schema()

        assert isinstance(schema, list)
        assert len(schema) > 0
        assert "input.Ef" in schema
        assert "output.f41" in schema


class TestQueryChaining:
    """Tests for Query method chaining."""

    def test_method_chaining(self, mock_session, mock_tool_schema):
        """Test that methods return self for chaining."""
        mock_session.requestPost.return_value = Mock(json=lambda: mock_tool_schema)

        library = Results(mock_session)
        query = (Query(library, "2dfets", simtool=False)
                .filter("input.Ef", ">", 0.2)
                .filter("input.Lg", ">", 15)
                .select("input.Ef", "output.f41")
                .sort("input.Ef", asc=False)
                .limit(20)
                .offset(10))

        assert len(query._filters) == 2
        assert len(query._results_fields) == 2
        assert query._sort == "input.Ef"
        assert query._limit == 20
        assert query._offset == 10
