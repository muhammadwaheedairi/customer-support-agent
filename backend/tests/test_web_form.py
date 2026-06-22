"""Tests for web form submission endpoint."""

import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock

from api.main import app


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
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
    assert data["service"] == "TaskFlow Customer Support Agent API"


@pytest.mark.asyncio
async def test_submit_form_valid(client):
    """Test valid form submission."""
    with patch('channels.web_form_handler.handle_form_submission') as mock_handle:
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
    with patch('database.queries.get_ticket_by_id') as mock_get:
        mock_get.return_value = None
        
        response = await client.get("/support/status/nonexistent-id")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_customer_lookup_not_found(client):
    """Test customer lookup for non-existent customer."""
    with patch('database.queries.get_customer_by_email') as mock_get:
        mock_get.return_value = None
        
        response = await client.get("/customers/lookup?email=nonexistent@example.com")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_metrics_endpoint(client):
    """Test metrics endpoint."""
    with patch('database.queries.get_metrics_summary') as mock_metrics, \
         patch('database.queries.get_db_pool') as mock_pool:
        
        mock_metrics.return_value = {}
        
        # Mock database queries
        mock_conn = AsyncMock()
        mock_conn.fetchval = AsyncMock(side_effect=[10, 2.5])  # ticket count, avg response time
        mock_pool.return_value.acquire = AsyncMock(return_value=mock_conn)
        
        response = await client.get("/metrics/channels")
        assert response.status_code == 200
        data = response.json()
        assert "channels" in data
