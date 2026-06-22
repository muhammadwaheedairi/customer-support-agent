"""Web form handler for customer support submissions."""

import logging
from typing import Dict, Any
import json

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
    3. Publish to Kafka for agent processing (simplified - direct processing for now)
    
    Args:
        name: Customer name
        email: Customer email
        subject: Ticket subject
        category: Ticket category
        message: Customer message
        priority: Priority level
    
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
        
        # Step 2: Create ticket (which also creates initial message and conversation)
        ticket_id = await create_ticket(
            customer_id=customer_id,
            subject=subject,
            category=category,
            message=message,
            priority=priority,
            channel="web_form"
        )
        
        logger.info(f"Ticket created: {ticket_id}")
        
        # Step 3: Process with AI agent immediately (simplified approach)
        # In production, this would publish to Kafka and be processed by a worker
        from agent.customer_success_agent import run_agent
        
        try:
            agent_result = await run_agent(
                customer_id=customer_id,
                customer_email=email,
                customer_name=name,
                subject=subject,
                message=message,
                category=category,
                priority=priority
            )
            
            if agent_result.get("success"):
                logger.info(f"Agent processed ticket {ticket_id} successfully")
            else:
                logger.error(f"Agent processing failed for ticket {ticket_id}: {agent_result.get('error')}")
        
        except Exception as e:
            logger.error(f"Agent execution failed for ticket {ticket_id}: {e}", exc_info=True)
            # Continue anyway - ticket is created, agent can retry later
        
        return {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "status": "submitted"
        }
    
    except Exception as e:
        logger.error(f"Form submission handling failed: {e}", exc_info=True)
        raise


async def publish_to_kafka(topic: str, message: Dict[str, Any]) -> None:
    """
    Publish message to Kafka topic.
    
    Simplified implementation - in production, use aiokafka producer.
    
    Args:
        topic: Kafka topic name
        message: Message payload
    """
    try:
        # TODO: Implement Kafka producer
        # from aiokafka import AIOKafkaProducer
        # producer = AIOKafkaProducer(bootstrap_servers=...)
        # await producer.send_and_wait(topic, json.dumps(message).encode())
        
        logger.info(f"Would publish to Kafka topic {topic}: {message}")
    
    except Exception as e:
        logger.error(f"Kafka publish failed: {e}", exc_info=True)
        # Don't fail the request if Kafka is unavailable
