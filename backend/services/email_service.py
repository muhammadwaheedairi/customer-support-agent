"""Email notification service using Resend."""

import os
import logging
import resend
from typing import Optional

logger = logging.getLogger(__name__)

resend.api_key = os.getenv("RESEND_API_KEY")

FROM_EMAIL = "LexDesk Support <onboarding@resend.dev>"

async def send_ticket_created_email(
    to_email: str,
    customer_name: str,
    ticket_id: str,
    subject: str,
    category: str,
) -> bool:
    """Send email when ticket is created."""
    try:
        params = {
            "from": FROM_EMAIL,
            "to": [os.getenv("TEST_EMAIL", to_email)],
            "subject": f"[LexDesk] Your support request has been received — {subject}",
            "html": f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 600px; margin: 0 auto; padding: 40px 20px; color: #1a1a1a; background: #ffffff;">
  
  <!-- Header -->
  <div style="margin-bottom: 32px;">
    <div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 24px;">
      <div style="background: #c8f135; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; color: #1a1a1a;">L</div>
      <span style="font-size: 20px; font-weight: 600; color: #1a1a1a;">LexDesk</span>
    </div>
    <h1 style="font-size: 24px; font-weight: 600; margin: 0 0 8px 0; color: #1a1a1a;">We received your request</h1>
    <p style="font-size: 16px; color: #666; margin: 0;">Our AI assistant is processing your inquiry now.</p>
  </div>

  <!-- Ticket Info -->
  <div style="background: #f8f8f8; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
    <p style="font-size: 14px; color: #666; margin: 0 0 4px 0;">Hello {customer_name},</p>
    <p style="font-size: 15px; color: #1a1a1a; margin: 0 0 20px 0;">Your support request has been received and our AI assistant is working on it right now.</p>
    
    <div style="border-top: 1px solid #e5e5e5; padding-top: 16px;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <span style="font-size: 13px; color: #666;">Reference Number</span>
        <span style="font-size: 13px; font-family: monospace; color: #1a1a1a; font-weight: 600;">{ticket_id[:8].upper()}</span>
      </div>
      <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <span style="font-size: 13px; color: #666;">Subject</span>
        <span style="font-size: 13px; color: #1a1a1a;">{subject}</span>
      </div>
      <div style="display: flex; justify-content: space-between;">
        <span style="font-size: 13px; color: #666;">Category</span>
        <span style="font-size: 13px; color: #1a1a1a; text-transform: capitalize;">{category}</span>
      </div>
    </div>
  </div>

  <!-- CTA -->
  <div style="text-align: center; margin-bottom: 32px;">
    <a href="http://localhost:3000/conversations/{ticket_id}" 
       style="display: inline-block; background: #c8f135; color: #1a1a1a; padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 15px; text-decoration: none;">
      View Your Conversation
    </a>
  </div>

  <!-- Footer -->
  <div style="border-top: 1px solid #e5e5e5; padding-top: 24px; text-align: center;">
    <p style="font-size: 13px; color: #999; margin: 0 0 4px 0;">LexDesk Support Team</p>
    <p style="font-size: 13px; color: #999; margin: 0;">
      <a href="mailto:support@lexdesk.io" style="color: #666; text-decoration: none;">support@lexdesk.io</a>
    </p>
  </div>

</body>
</html>
            """,
        }

        resend.Emails.send(params)
        logger.info(f"Ticket created email sent to {to_email} for ticket {ticket_id}")
        return True

    except Exception as e:
        logger.error(f"Failed to send ticket created email: {e}")
        return False


async def send_agent_response_email(
    to_email: str,
    customer_name: str,
    ticket_id: str,
    subject: str,
    agent_response: str,
) -> bool:
    """Send email when agent responds."""
    try:
        # Truncate response for email preview
        response_preview = agent_response[:500] + "..." if len(agent_response) > 500 else agent_response

        params = {
            "from": FROM_EMAIL,
            "to": [os.getenv("TEST_EMAIL", to_email)],
            "subject": f"[LexDesk] Response to your request — {subject}",
            "html": f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 600px; margin: 0 auto; padding: 40px 20px; color: #1a1a1a; background: #ffffff;">

  <!-- Header -->
  <div style="margin-bottom: 32px;">
    <div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 24px;">
      <div style="background: #c8f135; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; color: #1a1a1a;">L</div>
      <span style="font-size: 20px; font-weight: 600; color: #1a1a1a;">LexDesk</span>
    </div>
    <h1 style="font-size: 24px; font-weight: 600; margin: 0 0 8px 0; color: #1a1a1a;">We have a response for you</h1>
    <p style="font-size: 16px; color: #666; margin: 0;">Our AI assistant has processed your request.</p>
  </div>

  <!-- Greeting -->
  <p style="font-size: 15px; color: #1a1a1a; margin: 0 0 24px 0;">Hello {customer_name},</p>

  <!-- Response -->
  <div style="background: #f0fdf4; border-left: 4px solid #c8f135; border-radius: 0 8px 8px 0; padding: 20px; margin-bottom: 24px;">
    <p style="font-size: 13px; font-weight: 600; color: #666; margin: 0 0 12px 0; text-transform: uppercase; letter-spacing: 0.05em;">LexDesk AI Assistant</p>
    <p style="font-size: 15px; color: #1a1a1a; margin: 0; line-height: 1.6; white-space: pre-wrap;">{response_preview}</p>
  </div>

  <!-- CTA -->
  <div style="text-align: center; margin-bottom: 32px;">
    <a href="http://localhost:3000/conversations/{ticket_id}"
       style="display: inline-block; background: #c8f135; color: #1a1a1a; padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 15px; text-decoration: none;">
      View Full Response
    </a>
  </div>

  <!-- Reference -->
  <div style="background: #f8f8f8; border-radius: 8px; padding: 16px; margin-bottom: 24px; text-align: center;">
    <p style="font-size: 13px; color: #666; margin: 0 0 4px 0;">Reference Number</p>
    <p style="font-size: 15px; font-family: monospace; font-weight: 600; color: #1a1a1a; margin: 0;">{ticket_id[:8].upper()}</p>
  </div>

  <!-- Footer -->
  <div style="border-top: 1px solid #e5e5e5; padding-top: 24px; text-align: center;">
    <p style="font-size: 13px; color: #999; margin: 0 0 4px 0;">LexDesk Support Team</p>
    <p style="font-size: 13px; color: #999; margin: 0;">
      <a href="mailto:support@lexdesk.io" style="color: #666; text-decoration: none;">support@lexdesk.io</a>
    </p>
  </div>

</body>
</html>
            """,
        }

        resend.Emails.send(params)
        logger.info(f"Agent response email sent to {to_email} for ticket {ticket_id}")
        return True

    except Exception as e:
        logger.error(f"Failed to send agent response email: {e}")
        return False


async def send_escalation_email(
    to_email: str,
    customer_name: str,
    ticket_id: str,
    subject: str,
    response_time: str = "4 hours",
) -> bool:
    """Send email when ticket is escalated to human."""
    try:
        params = {
            "from": FROM_EMAIL,
            "to": [os.getenv("TEST_EMAIL", to_email)],
            "subject": f"[LexDesk] Your request has been escalated — {subject}",
            "html": f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 600px; margin: 0 auto; padding: 40px 20px; color: #1a1a1a;">

  <div style="margin-bottom: 32px;">
    <div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 24px;">
      <div style="background: #c8f135; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px;">L</div>
      <span style="font-size: 20px; font-weight: 600;">LexDesk</span>
    </div>
    <h1 style="font-size: 24px; font-weight: 600; margin: 0 0 8px 0;">Your request needs human attention</h1>
    <p style="font-size: 16px; color: #666; margin: 0;">A specialist will contact you shortly.</p>
  </div>

  <p style="font-size: 15px; margin: 0 0 24px 0;">Hello {customer_name},</p>
  
  <div style="background: #fff8f0; border-left: 4px solid #f59e0b; border-radius: 0 8px 8px 0; padding: 20px; margin-bottom: 24px;">
    <p style="font-size: 15px; margin: 0; line-height: 1.6;">
      Your request regarding <strong>"{subject}"</strong> has been escalated to our specialist team. 
      A team member will reach out to you within <strong>{response_time}</strong> during business hours 
      (Mon–Fri, 9AM–6PM EST/GMT).
    </p>
  </div>

  <div style="background: #f8f8f8; border-radius: 8px; padding: 16px; margin-bottom: 24px; text-align: center;">
    <p style="font-size: 13px; color: #666; margin: 0 0 4px 0;">Reference Number</p>
    <p style="font-size: 15px; font-family: monospace; font-weight: 600; margin: 0;">{ticket_id[:8].upper()}</p>
  </div>

  <div style="border-top: 1px solid #e5e5e5; padding-top: 24px; text-align: center;">
    <p style="font-size: 13px; color: #999; margin: 0;">
      <a href="mailto:support@lexdesk.io" style="color: #666; text-decoration: none;">support@lexdesk.io</a>
    </p>
  </div>

</body>
</html>
            """,
        }

        resend.Emails.send(params)
        logger.info(f"Escalation email sent to {to_email} for ticket {ticket_id}")
        return True

    except Exception as e:
        logger.error(f"Failed to send escalation email: {e}")
        return False