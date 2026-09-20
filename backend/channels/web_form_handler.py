"""Web form handler for customer support submissions."""

import logging
import bleach
from typing import Dict, Any, Optional

from database.queries import create_customer, create_ticket, update_ticket_status
from services.email_service import (
    send_ticket_created_email,
    send_agent_response_email,
    send_escalation_email,
)

logger = logging.getLogger(__name__)


def sanitize_text(text: str, max_length: int = None) -> str:
    """Strip all HTML tags and sanitize input text."""
    cleaned = bleach.clean(text, tags=[], strip=True)
    cleaned = " ".join(cleaned.split())
    if max_length:
        cleaned = cleaned[:max_length]
    return cleaned.strip()


async def handle_form_submission(
    name: str,
    email: str,
    subject: str,
    category: str,
    message: str,
    priority: str = "medium",
    clerk_user_id: Optional[str] = None
) -> Dict[str, Any]:
    try:
        # Sanitize all inputs
        name = sanitize_text(name, max_length=255)
        subject = sanitize_text(subject, max_length=500)
        message = sanitize_text(message, max_length=5000)
        email = email.strip().lower()
        category = category.strip().lower()
        priority = priority.strip().lower()

        logger.info(f"Sanitized submission — name={name}, email={email}")

        # Step 1: Create or update customer
        customer_id = await create_customer(
            email=email,
            name=name,
            metadata={"source": "web_form"},
            clerk_user_id=clerk_user_id
        )
        logger.info(f"Customer created/updated: {customer_id}")

        # Step 2: Create ticket
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

        # Step 3: Send ticket created email
        await send_ticket_created_email(
            to_email=email,
            customer_name=name,
            ticket_id=ticket_id,
            subject=subject,
            category=category,
        )

        # Step 4: Run agent
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

                agent_response = agent_result.get("response", "")
                action = agent_result.get("action")  # "escalated", "resolved", or None

                # Use explicit action field instead of unreliable text matching
                if action == "escalated":
                    logger.info(f"Sending escalation email for ticket {ticket_id}")
                    await send_escalation_email(
                        to_email=email,
                        customer_name=name,
                        ticket_id=ticket_id,
                        subject=subject,
                    )
                elif action == "resolved":
                    # Ticket was explicitly resolved by agent
                    logger.info(f"Sending agent response email for ticket {ticket_id} (action=resolved)")
                    await send_agent_response_email(
                        to_email=email,
                        customer_name=name,
                        ticket_id=ticket_id,
                        subject=subject,
                        agent_response=agent_response,
                    )
                elif action is None:
                    # Agent didn't explicitly resolve or escalate — auto-escalate as safe default
                    logger.warning(
                        f"Agent did not set explicit action for ticket {ticket_id}. "
                        f"Auto-escalating for human review."
                    )

                    # Update ticket status to escalated in database
                    await update_ticket_status(
                        ticket_id=ticket_id,
                        status="escalated",
                        resolution_notes="Auto-escalated: agent did not explicitly resolve or escalate this ticket"
                    )

                    # Send escalation email to customer
                    await send_escalation_email(
                        to_email=email,
                        customer_name=name,
                        ticket_id=ticket_id,
                        subject=subject,
                    )
                    logger.info(f"Auto-escalated ticket {ticket_id} and sent escalation email")
                else:
                    # Unexpected action value — log and send normal response as fallback
                    logger.error(f"Unexpected action value '{action}' for ticket {ticket_id}. Sending normal response email.")
                    await send_agent_response_email(
                        to_email=email,
                        customer_name=name,
                        ticket_id=ticket_id,
                        subject=subject,
                        agent_response=agent_response,
                    )
            else:
                logger.error(f"Agent failed for ticket {ticket_id}: {agent_result.get('error')}")

        except Exception as e:
            logger.error(f"Agent execution failed for ticket {ticket_id}: {e}", exc_info=True)

            # Send fallback email to customer
            try:
                fallback_message = (
                    "Thank you for contacting FlowSync Support.\n\n"
                    "We've received your request and our team is currently reviewing it. "
                    "A support specialist will get back to you shortly with a detailed response.\n\n"
                    "We appreciate your patience."
                )
                await send_agent_response_email(
                    to_email=email,
                    customer_name=name,
                    ticket_id=ticket_id,
                    subject=subject,
                    agent_response=fallback_message,
                )
                logger.info(f"Fallback email sent for ticket {ticket_id} after agent failure")
            except Exception as email_error:
                logger.error(f"Failed to send fallback email for ticket {ticket_id}: {email_error}", exc_info=True)

        return {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "status": "submitted"
        }

    except Exception as e:
        logger.error(f"Form submission handling failed: {e}", exc_info=True)
        raise