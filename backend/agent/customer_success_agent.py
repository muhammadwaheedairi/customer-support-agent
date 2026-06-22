"""Customer Success Agent implementation using OpenAI Agents SDK."""

from agents import Agent
from typing import Optional, Dict, Any
import logging

from .prompts import get_system_prompt
from .tools import ALL_TOOLS

logger = logging.getLogger(__name__)


def create_customer_success_agent(
    model: str = "gpt-4o",
    temperature: float = 0.7
) -> Agent:
    """Create and configure the Customer Success Agent.
    
    Args:
        model: OpenAI model to use (default: gpt-4o)
        temperature: Model temperature for response generation
    
    Returns:
        Configured Agent instance ready to handle support queries
    """
    agent = Agent(
        name="TaskFlow Customer Success Agent",
        instructions=get_system_prompt(),
        model=model,
        tools=ALL_TOOLS,
    )
    
    logger.info(f"Customer Success Agent created with model {model}")
    return agent


# Create a global agent instance
customer_success_agent = create_customer_success_agent()


async def run_agent(
    customer_id: str,
    customer_email: str,
    customer_name: Optional[str],
    subject: str,
    message: str,
    category: str = "general",
    priority: str = "medium"
) -> Dict[str, Any]:
    """Run the customer success agent for a support query.
    
    Args:
        customer_id: Customer UUID
        customer_email: Customer email address
        customer_name: Customer name (optional)
        subject: Support ticket subject
        message: Customer's message/question
        category: Ticket category
        priority: Priority level
    
    Returns:
        Dict containing agent response, ticket_id, and metadata
    """
    from agents import Runner
    
    # Construct the user input with context
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

Please handle this support request following the standard workflow."""
    
    try:
        # Run the agent
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
            }
        )
        
        logger.info(f"Agent completed successfully for customer {customer_id}")
        
        return {
            "success": True,
            "response": result.final_output,
            "tool_calls": [
                {
                    "tool": call.tool_name,
                    "result": str(call.result)[:200]  # Truncate for logging
                }
                for call in result.all_tool_calls
            ],
            "turn_count": len(result.all_model_responses)
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
