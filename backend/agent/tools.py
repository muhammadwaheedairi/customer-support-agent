"""Function tools for Customer Success Agent using OpenAI Agents SDK."""

from agents import function_tool
from pydantic import BaseModel, Field
from typing import Optional
import logging
import json

from database.queries import (
    create_ticket as db_create_ticket,
    get_customer_history as db_get_history,
    update_ticket_status,
    create_message,
)
from rag.retriever import retrieve, format_results_for_agent

logger = logging.getLogger(__name__)


# Input schemas

class KnowledgeSearchInput(BaseModel):
    query: str = Field(..., description="Search query for product documentation")
    top_k: int = Field(default=3, ge=1, le=5, description="Number of results to return")


class TicketInput(BaseModel):
    customer_id: str = Field(..., description="Customer UUID")
    subject: str = Field(..., description="Ticket subject/title")
    category: str = Field(..., description="Category: general, technical, billing, bug_report, feedback")
    message: str = Field(..., description="Customer's message content")
    priority: str = Field(default="medium", description="Priority: low, medium, high")


class EscalationInput(BaseModel):
    ticket_id: str = Field(..., description="Ticket UUID to escalate")
    reason: str = Field(..., description="Reason for escalation")
    category: str = Field(..., description="Escalation category: pricing_inquiry, refund_request, legal_matter, high_frustration, technical_complex, security_concern, explicit_request")


class WebResponseInput(BaseModel):
    ticket_id: str = Field(..., description="Ticket UUID")
    response: str = Field(..., description="Response message to send to customer")


# Tools

@function_tool
async def search_knowledge_base(input: KnowledgeSearchInput) -> str:
    """Search TaskFlow product documentation using semantic search + reranking.

    Use this when the customer asks questions about:
    - Product features ("How do I create tasks?")
    - How-to guidance ("How to set up automation?")
    - Troubleshooting steps ("Tasks not syncing")
    - Account management ("How to change my plan?")

    Returns top relevant documentation with relevance scores.
    """
    try:
        results = await retrieve(
            query=input.query,
            top_k=input.top_k,
        )

        formatted = format_results_for_agent(results)
        logger.info(f"KB search returned {len(results)} results for: {input.query[:50]}")
        return formatted

    except Exception as e:
        logger.error(f"Knowledge base search failed: {e}")
        return "Knowledge base temporarily unavailable. Please escalate to human support."


@function_tool
async def create_ticket(input: TicketInput) -> str:
    """Create a support ticket to log the customer inquiry.

    **ALWAYS call this FIRST** in every conversation before doing anything else.
    This is required to track all customer interactions properly.
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

    Use this to check previous issues, understand context, and provide
    personalized assistance.
    """
    try:
        history = await db_get_history(customer_id, limit=10)

        if not history:
            return "This is a new customer with no previous support history."

        formatted_history = [f"Found {len(history)} previous interactions:\n"]

        tickets = {}
        for record in history:
            ticket_id = str(record['ticket_id'])
            if ticket_id not in tickets:
                created_at = record.get('created_at')
                tickets[ticket_id] = {
                    'subject': record['subject'],
                    'category': record['category'],
                    'status': record['ticket_status'],
                    'created': created_at.strftime('%Y-%m-%d') if created_at else 'N/A',
                }

        for ticket_id, data in list(tickets.items())[:3]:
            formatted_history.append(
                f"\n**Ticket:** {data['subject']}\n"
                f"Category: {data['category']} | Status: {data['status']}\n"
                f"Date: {data['created']}"
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
    """
    try:
        await update_ticket_status(
            ticket_id=input.ticket_id,
            status="escalated",
            resolution_notes=f"Escalated: {input.category} - {input.reason}"
        )

        await create_message(
            ticket_id=input.ticket_id,
            role="system",
            content=f"Ticket escalated to human support. Reason: {input.reason}",
        )

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
        return f"Ticket escalated. Category: {input.category}. Response time: {response_time}. Reference: {input.ticket_id}"

    except Exception as e:
        logger.error(f"Escalation failed: {e}")
        return f"Failed to escalate ticket: {str(e)}"


@function_tool
async def send_web_response(input: WebResponseInput) -> str:
    """Send the final response to the customer via web form.

    **ALWAYS call this as the FINAL step** to send your response.
    Never respond to the customer without calling this tool.
    """
    try:
        await create_message(
            ticket_id=input.ticket_id,
            role="agent",
            content=input.response,
        )
        logger.info(f"Web response sent for ticket {input.ticket_id}")
        return f"Response successfully sent to customer. Ticket ID: {input.ticket_id}"

    except Exception as e:
        logger.error(f"Send web response failed: {e}")
        return f"Failed to send response: {str(e)}"


ALL_TOOLS = [
    search_knowledge_base,
    create_ticket,
    get_customer_history,
    escalate_to_human,
    send_web_response,
]