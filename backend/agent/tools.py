"""Function tools for Customer Success Agent using OpenAI Agents SDK."""

from agents import function_tool
from pydantic import BaseModel, Field
from typing import Optional
import logging

from database.queries import (
    search_knowledge_base as db_search_kb,
    create_ticket as db_create_ticket,
    get_customer_history as db_get_history,
    update_ticket_status,
    create_message,
)

logger = logging.getLogger(__name__)


# Input schemas using Pydantic

class KnowledgeSearchInput(BaseModel):
    """Input schema for knowledge base search."""
    query: str = Field(..., description="Search query for product documentation")
    max_results: int = Field(default=5, ge=1, le=10, description="Maximum number of results to return")


class TicketInput(BaseModel):
    """Input schema for ticket creation."""
    customer_id: str = Field(..., description="Customer UUID")
    subject: str = Field(..., description="Ticket subject/title")
    category: str = Field(..., description="Category: general, technical, billing, bug_report, feedback")
    message: str = Field(..., description="Customer's message content")
    priority: str = Field(default="medium", description="Priority: low, medium, high")


class EscalationInput(BaseModel):
    """Input schema for escalation to human."""
    ticket_id: str = Field(..., description="Ticket UUID to escalate")
    reason: str = Field(..., description="Reason for escalation")
    category: str = Field(..., description="Escalation category: pricing_inquiry, refund_request, legal_matter, high_frustration, technical_complex, security_concern, explicit_request")


class WebResponseInput(BaseModel):
    """Input schema for web response."""
    ticket_id: str = Field(..., description="Ticket UUID")
    response: str = Field(..., description="Response message to send to customer")


# Function tools

@function_tool
async def search_knowledge_base(input: KnowledgeSearchInput) -> str:
    """Search TaskFlow product documentation for relevant information.
    
    Use this when the customer asks questions about:
    - Product features ("How do I create tasks?")
    - How-to guidance ("How to set up automation?")
    - Troubleshooting steps ("Tasks not syncing")
    - Account management ("How to change my plan?")
    
    Returns formatted search results with titles and content snippets.
    If no results found, returns message indicating no documentation available.
    """
    try:
        results = await db_search_kb(input.query, input.max_results)
        
        if not results:
            return "No relevant documentation found. Consider escalating to human support if this is a critical issue."
        
        # Format results
        formatted_results = []
        for idx, result in enumerate(results, 1):
            formatted_results.append(
                f"{idx}. **{result['title']}**\n"
                f"   Category: {result.get('category', 'General')}\n"
                f"   {result['content'][:300]}..."
            )
        
        return "\n\n".join(formatted_results)
    
    except Exception as e:
        logger.error(f"Knowledge base search failed: {e}")
        return "Knowledge base temporarily unavailable. Please try again or escalate to human support."


@function_tool
async def create_ticket(input: TicketInput) -> str:
    """Create a support ticket to log the customer inquiry.
    
    **ALWAYS call this FIRST** in every conversation before doing anything else.
    This is required to track all customer interactions properly.
    
    Args:
        input: Ticket information including customer_id, subject, category, message
    
    Returns:
        Confirmation message with ticket ID that can be referenced in responses.
    """
    try:
        ticket_id = await db_create_ticket(
            customer_id=input.customer_id,
            subject=input.subject,
            category=input.category,
            message=input.message,
            priority=input.priority,
            channel="web_form"
        )
        
        logger.info(f"Ticket created: {ticket_id}")
        return f"Ticket created successfully. Ticket ID: {ticket_id}"
    
    except Exception as e:
        logger.error(f"Ticket creation failed: {e}")
        return f"Failed to create ticket: {str(e)}"


@function_tool
async def get_customer_history(customer_id: str) -> str:
    """Get customer's past support interactions and conversation history.
    
    Use this to:
    - Check if customer has contacted support before
    - Understand context from previous issues
    - Reference past resolutions
    - Provide personalized assistance
    
    Returns formatted conversation history or message if customer is new.
    """
    try:
        history = await db_get_history(customer_id, limit=10)
        
        if not history:
            return "This is a new customer with no previous support history."
        
        # Format history
        formatted_history = [f"Found {len(history)} previous interactions:\n"]
        
        # Group by ticket
        tickets = {}
        for record in history:
            ticket_id = str(record['ticket_id'])
            if ticket_id not in tickets:
                tickets[ticket_id] = {
                    'subject': record['subject'],
                    'category': record['category'],
                    'status': record['ticket_status'],
                    'created': record['created_at'],
                    'messages': []
                }
            if record['content']:
                tickets[ticket_id]['messages'].append({
                    'role': record['role'],
                    'content': record['content'][:150]
                })
        
        # Format each ticket
        for ticket_id, data in list(tickets.items())[:3]:  # Show last 3 tickets
            formatted_history.append(
                f"\n**Ticket:** {data['subject']}\n"
                f"Category: {data['category']} | Status: {data['status']}\n"
                f"Date: {data['created'].strftime('%Y-%m-%d')}"
            )
        
        return "\n".join(formatted_history)
    
    except Exception as e:
        logger.error(f"Get customer history failed: {e}")
        return "Unable to retrieve customer history at this time."


@function_tool
async def escalate_to_human(input: EscalationInput) -> str:
    """Escalate this ticket to human support team.
    
    **Use immediately when:**
    - Pricing negotiations, refunds, billing disputes
    - Legal threats or compliance requests
    - Angry customer (profanity, all caps, threats)
    - Cannot find solution after 2 knowledge base searches
    - Customer explicitly requests human help
    
    Args:
        input: Escalation details including ticket_id, reason, category
    
    Returns:
        Confirmation that ticket has been escalated with expected response time.
    """
    try:
        # Update ticket status to escalated
        await update_ticket_status(
            ticket_id=input.ticket_id,
            status="escalated",
            resolution_notes=f"Escalated: {input.category} - {input.reason}"
        )
        
        # Log escalation
        await create_message(
            ticket_id=input.ticket_id,
            role="system",
            content=f"Ticket escalated to human support. Reason: {input.reason}",
            metadata={"escalation_category": input.category}
        )
        
        # Determine response time based on category
        response_times = {
            "pricing_inquiry": "2 hours",
            "refund_request": "2 hours",
            "legal_matter": "2 hours",
            "high_frustration": "1 hour",
            "technical_complex": "4 hours",
            "security_concern": "2 hours",
            "explicit_request": "4 hours"
        }
        
        response_time = response_times.get(input.category, "4 hours")
        
        logger.info(f"Ticket {input.ticket_id} escalated: {input.category}")
        
        return f"Ticket successfully escalated to human support. Category: {input.category}. Expected response time: {response_time}. Reference: {input.ticket_id}"
    
    except Exception as e:
        logger.error(f"Escalation failed: {e}")
        return f"Failed to escalate ticket: {str(e)}"


@function_tool
async def send_web_response(input: WebResponseInput) -> str:
    """Send the final response to the customer via web form.
    
    **ALWAYS call this as the FINAL step** to send your response.
    Never respond to the customer without calling this tool.
    
    The response will be:
    - Formatted appropriately for web display
    - Stored in the database
    - Made available for customer to view
    
    Args:
        input: Response details including ticket_id and response message
    
    Returns:
        Confirmation that response has been sent successfully.
    """
    try:
        # Store the agent's response as a message
        await create_message(
            ticket_id=input.ticket_id,
            role="agent",
            content=input.response,
            metadata={"channel": "web_form", "response_type": "ai_agent"}
        )
        
        logger.info(f"Web response sent for ticket {input.ticket_id}")
        
        return f"Response successfully sent to customer. Ticket ID: {input.ticket_id}"
    
    except Exception as e:
        logger.error(f"Send web response failed: {e}")
        return f"Failed to send response: {str(e)}"


# Export all tools as a list for easy agent initialization
ALL_TOOLS = [
    search_knowledge_base,
    create_ticket,
    get_customer_history,
    escalate_to_human,
    send_web_response,
]
