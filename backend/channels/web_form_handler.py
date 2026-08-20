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
    priority: str = "medium",
    clerk_user_id: str = None
) -> Dict[str, Any]:
    try:
        # Step 1: Create or update customer
        customer_id = await create_customer(
            email=email,
            name=name,
            metadata={"source": "web_form"},
            clerk_user_id=clerk_user_id
        )
        logger.info(f"Customer created/updated: {customer_id}")

        # Step 2: Create ticket with clerk_user_id
        ticket_id = await create_ticket(
            customer_id=customer_id,
            subject=subject,
            category=category,
            message=message,
            priority=priority,
            channel="web_form",
            clerk_user_id=clerk_user_id
        )
        logger.info(f"Ticket created: {ticket_id}")

        # Step 3: Run agent
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
                logger.error(f"Agent failed for ticket {ticket_id}: {agent_result.get('error')}")

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