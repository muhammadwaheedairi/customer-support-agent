"""End-to-end tests for Customer Support Agent system."""

import pytest
import asyncio
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock

from api.main import app


@pytest.mark.asyncio
async def test_e2e_submit_and_get_status():
    """Test complete flow: submit form -> check status."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Mock database and agent operations
        with patch('channels.web_form_handler.create_customer') as mock_create_customer, \
             patch('channels.web_form_handler.create_ticket') as mock_create_ticket, \
             patch('agent.customer_success_agent.run_agent') as mock_run_agent:
            
            mock_create_customer.return_value = "customer-123"
            mock_create_ticket.return_value = "ticket-456"
            mock_run_agent.return_value = {
                "success": True,
                "response": "Thank you for contacting us!",
                "tool_calls": []
            }
            
            # Step 1: Submit form
            submit_response = await client.post("/support/submit", json={
                "name": "John Doe",
                "email": "john@example.com",
                "subject": "Help with password reset",
                "category": "technical",
                "message": "I cannot reset my password using the forgot password link.",
                "priority": "medium"
            })
            
            assert submit_response.status_code == 201
            submit_data = submit_response.json()
            assert submit_data["success"] is True
            ticket_id = submit_data["ticket_id"]
            
            # Step 2: Check ticket status (would normally poll)
            with patch('database.queries.get_ticket_by_id') as mock_get_ticket, \
                 patch('database.queries.get_messages_by_ticket') as mock_get_messages:
                
                mock_get_ticket.return_value = {
                    "id": ticket_id,
                    "customer_id": "customer-123",
                    "subject": "Help with password reset",
                    "category": "technical",
                    "status": "open",
                    "priority": "medium",
                    "channel": "web_form",
                    "created_at": asyncio.get_event_loop().time(),
                    "customer_email": "john@example.com",
                    "customer_name": "John Doe"
                }
                
                mock_get_messages.return_value = [
                    {
                        "role": "customer",
                        "content": "I cannot reset my password using the forgot password link.",
                        "created_at": asyncio.get_event_loop().time()
                    },
                    {
                        "role": "agent",
                        "content": "Thank you for contacting us!",
                        "created_at": asyncio.get_event_loop().time()
                    }
                ]
                
                status_response = await client.get(f"/support/status/{ticket_id}")
                assert status_response.status_code == 200
                status_data = status_response.json()
                assert status_data["ticket_id"] == ticket_id
                assert len(status_data["messages"]) == 2


@pytest.mark.asyncio
async def test_e2e_escalation_flow():
    """Test escalation flow for pricing inquiry."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        with patch('channels.web_form_handler.create_customer') as mock_create_customer, \
             patch('channels.web_form_handler.create_ticket') as mock_create_ticket, \
             patch('agent.customer_success_agent.run_agent') as mock_run_agent:
            
            mock_create_customer.return_value = "customer-789"
            mock_create_ticket.return_value = "ticket-escalated"
            
            # Simulate agent deciding to escalate
            mock_run_agent.return_value = {
                "success": True,
                "response": "I've escalated your pricing inquiry to our billing team.",
                "tool_calls": [
                    {"tool": "create_ticket", "result": "Ticket created"},
                    {"tool": "escalate_to_human", "result": "Escalated"}
                ]
            }
            
            # Submit pricing inquiry
            response = await client.post("/support/submit", json={
                "name": "Jane Smith",
                "email": "jane@example.com",
                "subject": "Enterprise pricing inquiry",
                "category": "billing",
                "message": "Can you provide custom pricing for 500 users with annual billing?",
                "priority": "high"
            })
            
            assert response.status_code == 201
            data = response.json()
            assert data["success"] is True


@pytest.mark.asyncio
async def test_e2e_customer_history():
    """Test customer with previous tickets."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        with patch('database.queries.get_customer_by_email') as mock_get_customer, \
             patch('database.queries.get_db_pool') as mock_pool:
            
            mock_get_customer.return_value = {
                "id": "existing-customer",
                "email": "repeat@example.com",
                "name": "Repeat Customer",
                "created_at": asyncio.get_event_loop().time()
            }
            
            # Mock ticket count query
            mock_conn = AsyncMock()
            mock_conn.fetchval = AsyncMock(return_value=3)
            mock_pool.return_value.acquire = AsyncMock(return_value=mock_conn)
            
            response = await client.get("/customers/lookup?email=repeat@example.com")
            
            assert response.status_code == 200
            data = response.json()
            assert data["ticket_count"] == 3


@pytest.mark.asyncio
async def test_e2e_invalid_input_handling():
    """Test system handles invalid inputs gracefully."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test with multiple validation errors
        response = await client.post("/support/submit", json={
            "name": "X",  # Too short
            "email": "not-an-email",  # Invalid format
            "subject": "Hi",  # Too short
            "category": "invalid",  # Invalid category
            "message": "Short",  # Too short
            "priority": "urgent"  # Invalid priority
        })
        
        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data


@pytest.mark.asyncio
async def test_e2e_metrics_collection():
    """Test that metrics are collected properly."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        with patch('database.queries.get_metrics_summary') as mock_metrics, \
             patch('database.queries.get_db_pool') as mock_pool:
            
            mock_metrics.return_value = {
                "tickets_created_hourly": {"avg_value": 15.5},
                "escalation_rate_percent": {"avg_value": 12.3}
            }
            
            mock_conn = AsyncMock()
            mock_conn.fetchval = AsyncMock(side_effect=[42, 3.2])
            mock_pool.return_value.acquire = AsyncMock(return_value=mock_conn)
            
            response = await client.get("/metrics/channels?hours=24")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_tickets"] == 42
            assert data["avg_response_time"] == 3.2
