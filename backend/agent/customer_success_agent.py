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
        name="LexDesk Customer Success Agent",
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

        # Log result structure for debugging
        logger.debug(f"Result type: {type(result)}")
        logger.debug(f"Result attributes: {dir(result)}")
        logger.debug(f"Result new_items count: {len(result.new_items) if hasattr(result, 'new_items') else 'N/A'}")

        # Parse tool calls to determine action taken
        action = None

        # Try multiple possible SDK structures
        items_to_check = []

        # Structure 1: result.new_items (confirmed to exist from line 89)
        if hasattr(result, 'new_items'):
            items_to_check = result.new_items
            logger.debug(f"Using result.new_items structure")
        # Structure 2: result.all_tool_calls (from old test)
        elif hasattr(result, 'all_tool_calls'):
            items_to_check = result.all_tool_calls
            logger.debug(f"Using result.all_tool_calls structure")
        else:
            logger.warning(f"Unknown result structure. Available attributes: {dir(result)}")

        for idx, item in enumerate(items_to_check):
            # Log raw item for debugging
            logger.debug(f"Item {idx}: type={type(item).__name__}, attributes={dir(item)}")
            logger.debug(f"Item {idx} repr: {repr(item)}")

            # Try to extract tool name from various possible structures
            tool_name = None

            # Check 1: item.type indicates a tool call
            if hasattr(item, 'type'):
                item_type = getattr(item, 'type', None)
                logger.debug(f"Item {idx} has type attribute: {item_type}")

                if item_type in ['function_call', 'tool_call', 'function', 'tool_call_item']:
                    tool_name = (
                        getattr(item, 'tool_name', None) or
                        getattr(item, 'name', None) or
                        getattr(item, 'function_name', None)
                    )
                    logger.debug(f"Extracted tool_name from type check: {tool_name}")

            # Check 2: Direct attributes (name, function, tool)
            if not tool_name and hasattr(item, 'name'):
                tool_name = getattr(item, 'name', None)
                logger.debug(f"Extracted tool_name from item.name: {tool_name}")

            if not tool_name and hasattr(item, 'function'):
                func = getattr(item, 'function', None)
                if hasattr(func, 'name'):
                    tool_name = func.name
                    logger.debug(f"Extracted tool_name from item.function.name: {tool_name}")

            # Check 3: Dictionary structure
            if not tool_name and isinstance(item, dict):
                tool_name = (
                    item.get('name') or
                    item.get('function_name') or
                    item.get('tool_name') or
                    item.get('function', {}).get('name')
                )
                logger.debug(f"Extracted tool_name from dict: {tool_name}")

            # Match against our target tools
            if tool_name:
                logger.info(f"Tool call detected: {tool_name}")

                if tool_name == 'escalate_to_human':
                    action = "escalated"
                    logger.info(f"✅ Escalation detected via tool call")
                elif tool_name == 'resolve_ticket':
                    action = "resolved"
                    logger.info(f"✅ Resolution detected via tool call")

        if action is None:
            logger.warning(
                f"No explicit action (escalated/resolved) detected for ticket {ticket_id}. "
                f"Checked {len(items_to_check)} items."
            )

        return {
            "success": True,
            "response": result.final_output,
            "turn_count": len(result.new_items) if hasattr(result, 'new_items') else len(items_to_check),
            "action": action  # "escalated", "resolved", or None
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