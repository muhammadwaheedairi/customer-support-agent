"""Web form handler for customer support submissions."""

import logging
from typing import Dict, Any

from database.queries import create_customer, create_ticket

logger = logging.getLogger(__name__)


async def handle_form_submission(
    name: str,
    email: str,
    subject: str,
    category: str,
    message: str,
    priority: str = "medium"
) -> Dict[str, Any]:
    """
    Handle web form submission.

    Steps:
    1. Create or update customer record
    2. Create support ticket with initial message
    3. Run AI agent with existing ticket_id (no duplicate ticket creation)

    Returns:
        Dict with ticket_id and status
    """
    try:
        # Step 1: Create or update customer
        customer_id = await create_customer(
            email=email,
            name=name,
            metadata={"source": "web_form"}
        )
        logger.info(f"Customer created/updated: {customer_id}")

        # Step 2: Create ticket
        ticket_id = await create_ticket(
            customer_id=customer_id,
            subject=subject,
            category=category,
            message=message,
            priority=priority,
            channel="web_form"
        )
        logger.info(f"Ticket created: {ticket_id}")

        # Step 3: Run agent — pass ticket_id so agent does NOT create another ticket
        from agent.customer_success_agent import run_agent

        try:
            agent_result = await run_agent(
                customer_id=customer_id,
                customer_email=email,
                customer_name=name,
                subject=subject,
                message=message,
                category=category,
                priority=priority,
                ticket_id=ticket_id,
            )

            if agent_result.get("success"):
                logger.info(f"Agent processed ticket {ticket_id} successfully")
            else:
                logger.error(f"Agent processing failed for ticket {ticket_id}: {agent_result.get('error')}")

        except Exception as e:
            logger.error(f"Agent execution failed for ticket {ticket_id}: {e}", exc_info=True)

        return {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "status": "submitted"
        }

    except Exception as e:
        logger.error(f"Form submission handling failed: {e}", exc_info=True)
        raise