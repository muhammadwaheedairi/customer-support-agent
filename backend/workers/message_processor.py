"""Message processor worker - processes support tickets with AI agent."""

import asyncio
import logging
import os
from datetime import datetime

from database.queries import (
    get_db_pool,
    close_db_pool,
)

logger = logging.getLogger(__name__)


class MessageProcessor:
    """Process incoming support messages with AI agent."""
    
    def __init__(self):
        """Initialize message processor."""
        self.running = False
    
    async def start(self):
        """Start the message processor worker."""
        logger.info("Starting message processor worker...")
        self.running = True
        
        try:
            # Initialize database pool
            await get_db_pool()
            logger.info("Message processor ready")
            
            # In production, this would consume from Kafka
            # For now, we process messages immediately in the API handler
            # This worker can be used for retry logic or batch processing
            
            while self.running:
                await asyncio.sleep(60)  # Health check interval
                logger.debug("Message processor heartbeat")
        
        except Exception as e:
            logger.error(f"Message processor failed: {e}", exc_info=True)
        
        finally:
            await close_db_pool()
            logger.info("Message processor stopped")
    
    async def stop(self):
        """Stop the message processor."""
        logger.info("Stopping message processor...")
        self.running = False
    
    async def process_message(self, message: dict):
        """
        Process a single message from Kafka.
        
        Args:
            message: Message payload from Kafka
        """
        try:
            ticket_id = message.get("ticket_id")
            logger.info(f"Processing message for ticket {ticket_id}")
            
            # Run AI agent
            from agent.customer_success_agent import run_agent
            
            result = await run_agent(
                customer_id=message["customer_id"],
                customer_email=message["customer_email"],
                customer_name=message.get("customer_name"),
                subject=message["subject"],
                message=message["message"],
                category=message.get("category", "general"),
                priority=message.get("priority", "medium")
            )
            
            if result.get("success"):
                logger.info(f"Successfully processed ticket {ticket_id}")
            else:
                logger.error(f"Failed to process ticket {ticket_id}: {result.get('error')}")
        
        except Exception as e:
            logger.error(f"Message processing failed: {e}", exc_info=True)


async def main():
    """Main entry point for message processor worker."""
    processor = MessageProcessor()
    
    try:
        await processor.start()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        await processor.stop()


if __name__ == "__main__":
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    asyncio.run(main())
