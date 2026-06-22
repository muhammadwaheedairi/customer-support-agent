"""Response formatters for different channels."""

from typing import Optional
import re


def format_for_web(
    response: str,
    ticket_id: Optional[str] = None,
    max_length: int = 300
) -> str:
    """Format response for web form display.
    
    Web form responses should be:
    - Semi-formal and professional
    - Clear and well-structured
    - 150-300 words maximum
    - Include helpful formatting (bullets, bold)
    
    Args:
        response: Raw response text from agent
        ticket_id: Optional ticket ID to include
        max_length: Maximum word count (default 300)
    
    Returns:
        Formatted response ready for web display
    """
    # Trim excessive whitespace
    response = re.sub(r'\n\s*\n\s*\n', '\n\n', response)
    response = response.strip()
    
    # Check word count and truncate if necessary
    words = response.split()
    if len(words) > max_length:
        response = ' '.join(words[:max_length]) + "..."
        response += "\n\n*Response truncated for length. For more details, please reply to this ticket.*"
    
    # Add footer with ticket reference if provided
    if ticket_id:
        response += f"\n\n---\n**Ticket Reference:** {ticket_id}\n"
        response += "*Need more help? Reply to this ticket or visit our [Help Center](https://help.taskflow.com).*"
    
    return response


def format_escalation_message(
    ticket_id: str,
    escalation_reason: str,
    response_time: str = "4 hours"
) -> str:
    """Format message for escalated tickets.
    
    Args:
        ticket_id: Ticket reference ID
        escalation_reason: Why the ticket was escalated
        response_time: Expected response time from human team
    
    Returns:
        Formatted escalation message for customer
    """
    return f"""Thank you for contacting TaskFlow support.

I've reviewed your request and determined it requires specialized attention from our team. Your inquiry has been escalated to the appropriate department.

**What happens next:**
- A human specialist will review your case
- You'll receive a response within {response_time}
- We'll contact you at the email address on file

**Your ticket reference:** {ticket_id}

We appreciate your patience and will ensure your issue receives the attention it deserves.

---
*Need immediate assistance? Visit our [Help Center](https://help.taskflow.com) for self-service options.*"""


def format_error_message(
    ticket_id: Optional[str] = None,
    include_escalation: bool = True
) -> str:
    """Format a generic error message when something goes wrong.
    
    Args:
        ticket_id: Optional ticket ID
        include_escalation: Whether to mention human follow-up
    
    Returns:
        Formatted error message
    """
    message = """We apologize, but we're experiencing a technical issue processing your request right now.

**What you can do:**
- Try refreshing your browser and submitting again
- Check our [Status Page](https://status.taskflow.com) for any ongoing issues
- Visit our [Help Center](https://help.taskflow.com) for self-service options"""
    
    if include_escalation:
        message += "\n\nA member of our support team will also follow up with you shortly to ensure your issue is resolved."
    
    if ticket_id:
        message += f"\n\n**Ticket Reference:** {ticket_id}"
    
    return message


def sanitize_response(response: str) -> str:
    """Sanitize response to remove any potential sensitive information.
    
    Args:
        response: Raw response text
    
    Returns:
        Sanitized response
    """
    # Remove potential API keys or tokens
    response = re.sub(r'sk-[a-zA-Z0-9]{32,}', '[API_KEY_REDACTED]', response)
    response = re.sub(r'Bearer [a-zA-Z0-9\-_\.]+', '[TOKEN_REDACTED]', response)
    
    # Remove potential email addresses that aren't support@taskflow.com
    response = re.sub(
        r'\b[A-Za-z0-9._%+-]+@(?!taskflow\.com)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '[EMAIL_REDACTED]',
        response
    )
    
    # Remove potential internal URLs
    response = re.sub(r'https?://internal\.', '[INTERNAL_URL_REDACTED]', response)
    response = re.sub(r'https?://admin\.', '[ADMIN_URL_REDACTED]', response)
    
    return response


def calculate_word_count(text: str) -> int:
    """Calculate word count of text.
    
    Args:
        text: Text to count words in
    
    Returns:
        Number of words
    """
    return len(text.split())


def validate_response_length(response: str, max_words: int = 300) -> bool:
    """Check if response is within acceptable length.
    
    Args:
        response: Response text to check
        max_words: Maximum allowed words
    
    Returns:
        True if within limit, False otherwise
    """
    return calculate_word_count(response) <= max_words
