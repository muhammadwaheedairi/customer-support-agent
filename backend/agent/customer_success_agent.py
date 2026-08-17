"""Customer Success Agent implementation using OpenAI Agents SDK."""

from agents import Agent, Runner
from typing import Optional, Dict, Any
import logging

from .prompts import get_system_prompt
from .tools import ALL_TOOLS

logger = logging.getLogger(__name__)


def create_customer_success_agent(
    model: str = "gpt-4o",
) -> Agent:
    """Create and configure the Customer Success Agent."""
    agent = Agent(
        name="TaskFlow Customer Success Agent",
        instructions=get_system_prompt(),
        model=model,
        tools=ALL_TOOLS,
    )
    logger.info(f"Customer Success Agent created with model {model}")
    return agent


customer_success_agent = create_customer_success_agent()


async def run_agent(
    customer_id: str,
    customer_email: str,
    customer_name: Optional[str],
    subject: str,
    message: str,
    category: str = "general",
    priority: str = "medium",
    ticket_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Run the customer success agent for a support query."""

    # Tell agent ticket is already created so it skips create_ticket tool
    ticket_context = (
        f"TICKET ALREADY CREATED — Ticket ID: {ticket_id}. "
        f"DO NOT call create_ticket again. Use this ticket_id for all tool calls."
        if ticket_id
        else "No ticket created yet. Call create_ticket first."
    )

    user_input = f"""New support request from {customer_name or customer_email}:

Subject: {subject}
Category: {category}
Priority: {priority}

Message:
{message}

Customer Context:
- Customer ID: {customer_id}
- Email: {customer_email}
- Name: {customer_name or 'Not provided'}

Ticket Context:
{ticket_context}

Please handle this support request following the standard workflow."""

    try:
        result = await Runner.run(
            customer_success_agent,
            user_input,
            context={
                "customer_id": customer_id,
                "customer_email": customer_email,
                "customer_name": customer_name,
                "subject": subject,
                "category": category,
                "priority": priority,
                "ticket_id": ticket_id,
            }
        )

        logger.info(f"Agent completed successfully for customer {customer_id}")

        return {
            "success": True,
            "response": result.final_output,
            "turn_count": len(result.new_items)
        }

    except Exception as e:
        logger.error(f"Agent execution failed: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "response": "We apologize, but we encountered an error processing your request. Our team has been notified and will follow up shortly."
        }


__all__ = [
    "customer_success_agent",
    "create_customer_success_agent",
    "run_agent"
]