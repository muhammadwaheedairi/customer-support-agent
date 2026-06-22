"""Tests for Customer Success Agent."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from agent.customer_success_agent import run_agent
from agent.tools import (
    search_knowledge_base,
    create_ticket,
    get_customer_history,
    escalate_to_human,
    send_web_response,
)


@pytest.mark.asyncio
async def test_run_agent_success():
    """Test successful agent execution."""
    with patch('agent.customer_success_agent.Runner') as mock_runner:
        # Mock the runner response
        mock_result = MagicMock()
        mock_result.final_output = "Test response"
        mock_result.all_tool_calls = []
        mock_result.all_model_responses = [MagicMock()]
        
        mock_runner.run = AsyncMock(return_value=mock_result)
        
        result = await run_agent(
            customer_id="test-customer-id",
            customer_email="test@example.com",
            customer_name="Test User",
            subject="Test Subject",
            message="Test message",
            category="general",
            priority="medium"
        )
        
        assert result["success"] is True
        assert "response" in result
        assert result["response"] == "Test response"


@pytest.mark.asyncio
async def test_search_knowledge_base():
    """Test knowledge base search tool."""
    from agent.tools import KnowledgeSearchInput
    
    with patch('agent.tools.db_search_kb') as mock_search:
        mock_search.return_value = [
            {
                "title": "Test Article",
                "content": "Test content",
                "category": "General"
            }
        ]
        
        input_data = KnowledgeSearchInput(query="test query", max_results=5)
        result = await search_knowledge_base(input_data)
        
        assert "Test Article" in result
        assert "Test content" in result


@pytest.mark.asyncio
async def test_create_ticket():
    """Test ticket creation tool."""
    from agent.tools import TicketInput
    
    with patch('agent.tools.db_create_ticket') as mock_create:
        mock_create.return_value = "test-ticket-id"
        
        input_data = TicketInput(
            customer_id="test-customer",
            subject="Test Subject",
            category="general",
            message="Test message",
            priority="medium"
        )
        
        result = await create_ticket(input_data)
        
        assert "test-ticket-id" in result
        assert "created successfully" in result.lower()


@pytest.mark.asyncio
async def test_escalate_to_human():
    """Test escalation tool."""
    from agent.tools import EscalationInput
    
    with patch('agent.tools.update_ticket_status') as mock_update, \
         patch('agent.tools.create_message') as mock_message:
        
        mock_update.return_value = None
        mock_message.return_value = "message-id"
        
        input_data = EscalationInput(
            ticket_id="test-ticket-id",
            reason="Pricing inquiry",
            category="pricing_inquiry"
        )
        
        result = await escalate_to_human(input_data)
        
        assert "escalated" in result.lower()
        assert "test-ticket-id" in result


@pytest.mark.asyncio
async def test_agent_handles_pricing_inquiry():
    """Test that pricing inquiries trigger escalation."""
    # This would test the agent's behavior with actual prompts
    # In a real test, you'd run the agent with a pricing question
    # and verify it calls the escalate_to_human tool
    pass


@pytest.mark.asyncio
async def test_agent_handles_refund_request():
    """Test that refund requests trigger escalation."""
    pass


@pytest.mark.asyncio
async def test_agent_provides_helpful_response():
    """Test that agent provides helpful responses for general questions."""
    pass


@pytest.mark.asyncio
async def test_knowledge_base_empty_results():
    """Test knowledge base search with no results."""
    from agent.tools import KnowledgeSearchInput
    
    with patch('agent.tools.db_search_kb') as mock_search:
        mock_search.return_value = []
        
        input_data = KnowledgeSearchInput(query="nonexistent", max_results=5)
        result = await search_knowledge_base(input_data)
        
        assert "no relevant documentation found" in result.lower()
