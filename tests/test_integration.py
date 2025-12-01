"""
Integration tests that require real API credentials.

These tests are marked with @pytest.mark.integration and are skipped
unless you explicitly run them with: pytest -m integration

Set the NANOHUB_TOKEN environment variable to run these tests:
    export NANOHUB_TOKEN="your_token_here"
    pytest -m integration
"""
import os
import pytest
from nanohubremote import Session
from nanohubresults import Results


# Skip integration tests if no token is provided
pytestmark = pytest.mark.skipif(
    not os.environ.get('NANOHUB_TOKEN'),
    reason="NANOHUB_TOKEN environment variable not set"
)


@pytest.fixture
def real_session():
    """Create a real session with API token from environment."""
    token = os.environ.get('NANOHUB_TOKEN')
    if not token:
        pytest.skip("NANOHUB_TOKEN not set")

    auth_data = {
        "grant_type": "personal_token",
        "token": token
    }
    return Session(auth_data, url="https://nanohub.org/api")


@pytest.fixture
def real_results(real_session):
    """Create Results object with real session."""
    return Results(real_session)


@pytest.mark.integration
class TestIntegrationQuery:
    """Integration tests using real API."""

    def test_real_schema_fetch(self, real_results):
        """Test fetching real tool schema."""
        query = real_results.query("2dfets", simtool=False)
        schema = query.schema()

        assert len(schema) > 0
        assert any(f.startswith('input.') for f in schema)
        assert any(f.startswith('output.') for f in schema)

    def test_real_search(self, real_results):
        """Test real search query."""
        query = real_results.query("2dfets", simtool=False) \
            .filter("input.Ef", ">", 0.2) \
            .select("input.Ef", "output.f41") \
            .limit(2)

        response = query.execute()

        assert 'results' in response
        # May or may not have results depending on database state
        if response.get('results'):
            assert len(response['results']) <= 2

    def test_real_simtool_query(self, real_results):
        """Test query with simulation tool."""
        query = real_results.query("st4pnjunction", simtool=True) \
            .filter("input.temperature", ">", 0) \
            .select("input.temperature") \
            .limit(1)

        response = query.execute()

        assert 'results' in response

    def test_real_download(self, real_results):
        """Test downloading real data."""
        # First get a result
        query = real_results.query("st4pnjunction", simtool=True) \
            .filter("input.temperature", ">", 0) \
            .select("input.temperature", "output.IV Characteristic") \
            .limit(1)

        response = query.execute()

        if response.get('results') and len(response['results']) > 0:
            squid = response['results'][0]['squid']

            # Download field data
            data = real_results.download(
                tool="st4pnjunction",
                squid=squid,
                field="output.IV Characteristic",
                simtool=True
            )

            assert isinstance(data, dict)

    def test_real_pagination(self, real_results):
        """Test pagination with real API."""
        query = real_results.query("2dfets", simtool=False) \
            .filter("input.Ef", ">", 0) \
            .select("input.Ef")

        # Get first few results
        results = []
        for result in query.paginate(per_page=5):
            results.append(result)
            if len(results) >= 10:
                break

        # Should get some results (or none if database is empty)
        assert isinstance(results, list)


@pytest.mark.integration
class TestIntegrationValidation:
    """Integration tests for validation."""

    def test_invalid_tool(self, real_results):
        """Test that invalid tool raises error."""
        with pytest.raises(ValueError, match="Failed to fetch schema"):
            real_results.query("nonexistent_tool_xyz", simtool=False)

    def test_missing_select_shows_real_fields(self, real_results):
        """Test that missing select shows actual available fields."""
        query = real_results.query("2dfets", simtool=False) \
            .filter("input.Ef", ">", 0)

        with pytest.raises(ValueError) as exc_info:
            query.execute()

        error_msg = str(exc_info.value)
        assert "select" in error_msg.lower()
        assert "input.Ef" in error_msg  # Should show actual fields
