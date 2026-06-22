"""Metrics collector worker - collects and aggregates performance metrics."""

import asyncio
import logging
import os
from datetime import datetime

from database.queries import (
    get_db_pool,
    close_db_pool,
    record_metric,
)

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collect and record agent performance metrics."""
    
    def __init__(self, interval_seconds: int = 300):
        """
        Initialize metrics collector.
        
        Args:
            interval_seconds: How often to collect metrics (default: 5 minutes)
        """
        self.interval = interval_seconds
        self.running = False
    
    async def start(self):
        """Start the metrics collector worker."""
        logger.info("Starting metrics collector worker...")
        self.running = True
        
        try:
            # Initialize database pool
            await get_db_pool()
            logger.info("Metrics collector ready")
            
            while self.running:
                try:
                    await self.collect_metrics()
                except Exception as e:
                    logger.error(f"Metrics collection failed: {e}", exc_info=True)
                
                await asyncio.sleep(self.interval)
        
        finally:
            await close_db_pool()
            logger.info("Metrics collector stopped")
    
    async def stop(self):
        """Stop the metrics collector."""
        logger.info("Stopping metrics collector...")
        self.running = False
    
    async def collect_metrics(self):
        """Collect and record metrics."""
        logger.info("Collecting metrics...")
        
        pool = await get_db_pool()
        
        async with pool.acquire() as conn:
            # Ticket metrics - last hour
            ticket_count = await conn.fetchval(
                """
                SELECT COUNT(*) 
                FROM tickets 
                WHERE created_at > NOW() - INTERVAL '1 hour'
                """
            )
            
            # Escalation rate
            escalated_count = await conn.fetchval(
                """
                SELECT COUNT(*) 
                FROM tickets 
                WHERE status = 'escalated' 
                  AND created_at > NOW() - INTERVAL '1 hour'
                """
            )
            
            # Average response time
            avg_response_time = await conn.fetchval(
                """
                SELECT AVG(EXTRACT(EPOCH FROM (m.created_at - t.created_at)))
                FROM messages m
                JOIN tickets t ON m.ticket_id = t.id
                WHERE m.role = 'agent'
                  AND t.created_at > NOW() - INTERVAL '1 hour'
                """
            )
            
            # Resolution rate
            resolved_count = await conn.fetchval(
                """
                SELECT COUNT(*)
                FROM tickets
                WHERE status = 'resolved'
                  AND resolved_at > NOW() - INTERVAL '1 hour'
                """
            )
        
        # Record metrics
        await record_metric(
            metric_name="tickets_created_hourly",
            metric_value=float(ticket_count),
            channel="web_form"
        )
        
        if ticket_count > 0:
            escalation_rate = (escalated_count / ticket_count) * 100
            await record_metric(
                metric_name="escalation_rate_percent",
                metric_value=escalation_rate,
                channel="web_form"
            )
        
        if avg_response_time:
            await record_metric(
                metric_name="avg_response_time_seconds",
                metric_value=float(avg_response_time),
                channel="web_form"
            )
        
        if ticket_count > 0:
            resolution_rate = (resolved_count / ticket_count) * 100
            await record_metric(
                metric_name="resolution_rate_percent",
                metric_value=resolution_rate,
                channel="web_form"
            )
        
        logger.info(
            f"Metrics collected: tickets={ticket_count}, "
            f"escalated={escalated_count}, resolved={resolved_count}, "
            f"avg_response_time={avg_response_time:.2f}s" if avg_response_time else "avg_response_time=N/A"
        )


async def main():
    """Main entry point for metrics collector worker."""
    collector = MetricsCollector(interval_seconds=300)  # 5 minutes
    
    try:
        await collector.start()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        await collector.stop()


if __name__ == "__main__":
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    asyncio.run(main())
