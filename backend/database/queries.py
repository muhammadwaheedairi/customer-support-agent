"""Database queries using asyncpg for async PostgreSQL operations."""

import asyncpg
import os
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def get_db_pool() -> asyncpg.Pool:
    """Get or create database connection pool."""
    global _pool
    
    if _pool is None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        _pool = await asyncpg.create_pool(
            database_url,
            min_size=5,
            max_size=20,
            command_timeout=60,
        )
        logger.info("Database connection pool created")
    
    return _pool


async def close_db_pool() -> None:
    """Close database connection pool."""
    global _pool
    
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")


# Customer operations

async def create_customer(
    email: str,
    name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """Create a new customer and return customer ID."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        customer_id = await conn.fetchval(
            """
            INSERT INTO customers (email, name, metadata)
            VALUES ($1, $2, $3)
            ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
            RETURNING id
            """,
            email,
            name,
            metadata or {}
        )
    
    logger.info(f"Customer created/updated: {customer_id}")
    return str(customer_id)


async def get_customer_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get customer by email address."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT id, email, name, created_at, metadata
            FROM customers
            WHERE email = $1
            """,
            email
        )
    
    if row:
        return dict(row)
    return None


# Ticket operations

async def create_ticket(
    customer_id: str,
    subject: str,
    category: str,
    message: str,
    priority: str = "medium",
    channel: str = "web_form"
) -> str:
    """Create a support ticket and initial message."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        async with conn.transaction():
            # Create ticket
            ticket_id = await conn.fetchval(
                """
                INSERT INTO tickets (customer_id, subject, category, priority, channel, status)
                VALUES ($1, $2, $3, $4, $5, 'open')
                RETURNING id
                """,
                customer_id,
                subject,
                category,
                priority,
                channel
            )
            
            # Create initial message
            await conn.execute(
                """
                INSERT INTO messages (ticket_id, role, content)
                VALUES ($1, 'customer', $2)
                """,
                ticket_id,
                message
            )
            
            # Create conversation
            await conn.execute(
                """
                INSERT INTO conversations (ticket_id, customer_id, channel, status)
                VALUES ($1, $2, $3, 'active')
                """,
                ticket_id,
                customer_id,
                channel
            )
    
    logger.info(f"Ticket created: {ticket_id}")
    return str(ticket_id)


async def get_ticket_by_id(ticket_id: str) -> Optional[Dict[str, Any]]:
    """Get ticket details by ID."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT t.id, t.customer_id, t.subject, t.category, t.status,
                   t.priority, t.channel, t.created_at, t.resolved_at,
                   c.email as customer_email, c.name as customer_name
            FROM tickets t
            JOIN customers c ON t.customer_id = c.id
            WHERE t.id = $1
            """,
            ticket_id
        )
    
    if row:
        return dict(row)
    return None


async def update_ticket_status(
    ticket_id: str,
    status: str,
    resolution_notes: Optional[str] = None
) -> None:
    """Update ticket status."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        if status == "resolved":
            await conn.execute(
                """
                UPDATE tickets
                SET status = $1, resolution_notes = $2, resolved_at = NOW()
                WHERE id = $3
                """,
                status,
                resolution_notes,
                ticket_id
            )
        else:
            await conn.execute(
                """
                UPDATE tickets
                SET status = $1, resolution_notes = $2
                WHERE id = $3
                """,
                status,
                resolution_notes,
                ticket_id
            )
    
    logger.info(f"Ticket {ticket_id} status updated to {status}")


# Message operations

async def create_message(
    ticket_id: str,
    role: str,
    content: str,
    sentiment_score: Optional[float] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """Create a message in a ticket."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        message_id = await conn.fetchval(
            """
            INSERT INTO messages (ticket_id, role, content, sentiment_score, metadata)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
            """,
            ticket_id,
            role,
            content,
            sentiment_score,
            metadata or {}
        )
    
    return str(message_id)


async def get_messages_by_ticket(ticket_id: str) -> List[Dict[str, Any]]:
    """Get all messages for a ticket."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, ticket_id, role, content, sentiment_score,
                   created_at, metadata
            FROM messages
            WHERE ticket_id = $1
            ORDER BY created_at ASC
            """,
            ticket_id
        )
    
    return [dict(row) for row in rows]


# Conversation operations

async def create_conversation(
    ticket_id: str,
    customer_id: str,
    channel: str = "web_form"
) -> str:
    """Create a conversation record."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        conversation_id = await conn.fetchval(
            """
            INSERT INTO conversations (ticket_id, customer_id, channel, status)
            VALUES ($1, $2, $3, 'active')
            RETURNING id
            """,
            ticket_id,
            customer_id,
            channel
        )
    
    return str(conversation_id)


async def get_conversation_by_id(conversation_id: str) -> Optional[Dict[str, Any]]:
    """Get conversation details."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT id, ticket_id, customer_id, channel, status,
                   created_at, ended_at, sentiment_score, metadata
            FROM conversations
            WHERE id = $1
            """,
            conversation_id
        )
    
    if row:
        return dict(row)
    return None


async def get_customer_history(customer_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Get customer's conversation history."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT c.id as conversation_id, c.channel, c.status, c.created_at,
                   t.id as ticket_id, t.subject, t.category, t.status as ticket_status,
                   m.role, m.content, m.created_at as message_created_at
            FROM conversations c
            JOIN tickets t ON c.ticket_id = t.id
            LEFT JOIN messages m ON m.ticket_id = t.id
            WHERE c.customer_id = $1
            ORDER BY m.created_at DESC
            LIMIT $2
            """,
            customer_id,
            limit
        )
    
    return [dict(row) for row in rows]


# Knowledge base operations

async def search_knowledge_base(
    query: str,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """Search knowledge base using text similarity."""
    pool = await get_db_pool()
    
    # Simple text search (full semantic search would require embeddings)
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, title, content, category,
                   ts_rank(
                       to_tsvector('english', title || ' ' || content),
                       plainto_tsquery('english', $1)
                   ) as relevance
            FROM knowledge_base
            WHERE to_tsvector('english', title || ' ' || content) @@ plainto_tsquery('english', $1)
            ORDER BY relevance DESC
            LIMIT $2
            """,
            query,
            limit
        )
    
    return [dict(row) for row in rows]


async def insert_knowledge_entry(
    title: str,
    content: str,
    category: Optional[str] = None
) -> str:
    """Insert a knowledge base entry."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        entry_id = await conn.fetchval(
            """
            INSERT INTO knowledge_base (title, content, category)
            VALUES ($1, $2, $3)
            RETURNING id
            """,
            title,
            content,
            category
        )
    
    return str(entry_id)


# Metrics operations

async def record_metric(
    metric_name: str,
    metric_value: float,
    channel: Optional[str] = None,
    dimensions: Optional[Dict[str, Any]] = None
) -> None:
    """Record a performance metric."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO agent_metrics (metric_name, metric_value, channel, dimensions)
            VALUES ($1, $2, $3, $4)
            """,
            metric_name,
            metric_value,
            channel,
            dimensions or {}
        )


async def get_metrics_summary(
    hours: int = 24,
    channel: Optional[str] = None
) -> Dict[str, Any]:
    """Get metrics summary for the last N hours."""
    pool = await get_db_pool()
    
    async with pool.acquire() as conn:
        query = """
            SELECT 
                metric_name,
                AVG(metric_value) as avg_value,
                MIN(metric_value) as min_value,
                MAX(metric_value) as max_value,
                COUNT(*) as count
            FROM agent_metrics
            WHERE recorded_at > NOW() - INTERVAL '%s hours'
        """ % hours
        
        if channel:
            query += " AND channel = $1"
            rows = await conn.fetch(query + " GROUP BY metric_name", channel)
        else:
            rows = await conn.fetch(query + " GROUP BY metric_name")
    
    return {row['metric_name']: dict(row) for row in rows}
