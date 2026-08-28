"""Tests for web form submission endpoint."""

import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch, AsyncMock
from fastapi import Depends

from api.main import app, get_current_user


# Mock authentication dependency
def mock_get_current_user():
    """Return a mock user ID for testing."""
    return "test-user-123"


# Override dependency for all tests
app.dependency_overrides[get_current_user] = mock_get_current_user


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "database" in data


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "LexDesk Customer Support Agent API"


@pytest.mark.asyncio
async def test_submit_form_valid(client):
    """Test valid form submission."""
    with patch('api.main.handle_form_submission') as mock_handle:
        mock_handle.return_value = {
            "ticket_id": "test-ticket-123",
            "customer_id": "test-customer-456",
            "status": "submitted"
        }

        response = await client.post("/support/submit", json={
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test Subject",
            "category": "general",
            "message": "This is a test message that is long enough to pass validation.",
            "priority": "medium"
        })

        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert "ticket_id" in data


@pytest.mark.asyncio
async def test_submit_form_invalid_email(client):
    """Test form submission with invalid email."""
    response = await client.post("/support/submit", json={
        "name": "Test User",
        "email": "invalid-email",
        "subject": "Test Subject",
        "category": "general",
        "message": "This is a test message that is long enough.",
        "priority": "medium"
    })
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_form_short_name(client):
    """Test form submission with name too short."""
    response = await client.post("/support/submit", json={
        "name": "A",
        "email": "test@example.com",
        "subject": "Test Subject",
        "category": "general",
        "message": "This is a test message that is long enough.",
        "priority": "medium"
    })
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_form_short_message(client):
    """Test form submission with message too short."""
    response = await client.post("/support/submit", json={
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "category": "general",
        "message": "Short",
        "priority": "medium"
    })
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_form_invalid_category(client):
    """Test form submission with invalid category."""
    response = await client.post("/support/submit", json={
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "category": "invalid_category",
        "message": "This is a test message that is long enough.",
        "priority": "medium"
    })
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_ticket_status_not_found(client):
    """Test getting status for non-existent ticket."""
    with patch('api.main.get_ticket_by_id') as mock_get:
        mock_get.return_value = None

        response = await client.get("/support/status/nonexistent-id")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_customer_lookup_not_found(client):
    """Test customer lookup for non-existent customer."""
    with patch('api.main.get_customer_by_email') as mock_get:
        mock_get.return_value = None

        response = await client.get("/customers/lookup?email=nonexistent@example.com")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_metrics_endpoint(client):
    """Test metrics endpoint."""
    with patch('api.main.get_metrics_summary') as mock_metrics, \
         patch('api.main.get_db_pool') as mock_pool:

        mock_metrics.return_value = {}

        # Mock database connection with proper async context manager
        mock_conn = AsyncMock()
        mock_conn.fetchval = AsyncMock(side_effect=[10, 2.5])  # ticket count, avg response time

        # Create async context manager mock for pool.acquire()
        from unittest.mock import MagicMock
        mock_acquire_cm = MagicMock()
        mock_acquire_cm.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_acquire_cm.__aexit__ = AsyncMock(return_value=None)

        mock_pool_instance = AsyncMock()
        mock_pool_instance.acquire = MagicMock(return_value=mock_acquire_cm)
        mock_pool.return_value = mock_pool_instance

        response = await client.get("/metrics/channels")
        assert response.status_code == 200
        data = response.json()
        assert "channels" in data
