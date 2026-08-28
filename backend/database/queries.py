"""Database queries using asyncpg for async PostgreSQL operations."""

import asyncpg
import os
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

_pool: Optional[asyncpg.Pool] = None


async def get_db_pool() -> asyncpg.Pool:
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
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")


# Customer operations

async def create_customer(
    email: str,
    name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    clerk_user_id: Optional[str] = None
) -> str:
    pool = await get_db_pool()

    async with pool.acquire() as conn:
        customer_id = await conn.fetchval(
            """
            INSERT INTO customers (email, name, metadata, clerk_user_id)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (email) DO UPDATE 
            SET name = EXCLUDED.name,
                clerk_user_id = COALESCE(EXCLUDED.clerk_user_id, customers.clerk_user_id)
            RETURNING id
            """,
            email,
            name,
            json.dumps(metadata or {}),
            clerk_user_id
        )

    logger.info(f"Customer created/updated: {customer_id}")
    return str(customer_id)

async def get_customer_by_email(email: str) -> Optional[Dict[str, Any]]:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, email, name, created_at, metadata, clerk_user_id FROM customers WHERE email = $1",
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
    channel: str = "web_form",
    clerk_user_id: Optional[str] = None
) -> str:
    """Create a support ticket linked to Clerk user."""
    pool = await get_db_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            ticket_id = await conn.fetchval(
                """
                INSERT INTO tickets (customer_id, subject, category, priority, channel, status, clerk_user_id)
                VALUES ($1, $2, $3, $4, $5, 'open', $6)
                RETURNING id
                """,
                customer_id,
                subject,
                category,
                priority,
                channel,
                clerk_user_id
            )

            await conn.execute(
                "INSERT INTO messages (ticket_id, role, content) VALUES ($1, 'customer', $2)",
                ticket_id,
                message
            )

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
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT t.id, t.customer_id, t.subject, t.category, t.status,
                   t.priority, t.channel, t.created_at, t.resolved_at,
                   t.clerk_user_id, t.deleted_at,
                   t.satisfaction_rating, t.satisfaction_comment,
                   c.email as customer_email, c.name as customer_name
            FROM tickets t
            JOIN customers c ON t.customer_id = c.id
            WHERE t.id = $1 AND t.deleted_at IS NULL
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
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        if status == "resolved":
            await conn.execute(
                """
                UPDATE tickets
                SET status = $1, resolution_notes = $2, resolved_at = NOW()
                WHERE id = $3
                """,
                status, resolution_notes, ticket_id
            )
        else:
            await conn.execute(
                "UPDATE tickets SET status = $1, resolution_notes = $2 WHERE id = $3",
                status, resolution_notes, ticket_id
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
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        message_id = await conn.fetchval(
            """
            INSERT INTO messages (ticket_id, role, content, sentiment_score, metadata)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
            """,
            ticket_id, role, content, sentiment_score, json.dumps(metadata or {})
        )
    return str(message_id)


async def get_messages_by_ticket(ticket_id: str) -> List[Dict[str, Any]]:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, ticket_id, role, content, sentiment_score, created_at, metadata
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
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        conversation_id = await conn.fetchval(
            """
            INSERT INTO conversations (ticket_id, customer_id, channel, status)
            VALUES ($1, $2, $3, 'active')
            RETURNING id
            """,
            ticket_id, customer_id, channel
        )
    return str(conversation_id)


async def get_conversation_by_id(conversation_id: str) -> Optional[Dict[str, Any]]:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT id, ticket_id, customer_id, channel, status,
                   created_at, ended_at, sentiment_score, metadata
            FROM conversations WHERE id = $1
            """,
            conversation_id
        )
    if row:
        return dict(row)
    return None


async def get_customer_history(customer_id: str, limit: int = 20) -> List[Dict[str, Any]]:
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
              AND t.deleted_at IS NULL
            ORDER BY m.created_at DESC
            LIMIT $2
            """,
            customer_id, limit
        )
    return [dict(row) for row in rows]


# Knowledge base operations
# NOTE: Semantic search for the agent is handled by rag/retriever.py
# (Cohere embeddings + Qdrant + Cohere rerank). insert_knowledge_entry
# below is kept for adding entries; the old plain-Postgres full-text
# search function was removed as unused dead code.

async def insert_knowledge_entry(
    title: str,
    content: str,
    category: Optional[str] = None
) -> str:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        entry_id = await conn.fetchval(
            "INSERT INTO knowledge_base (title, content, category) VALUES ($1, $2, $3) RETURNING id",
            title, content, category
        )
    return str(entry_id)


# Metrics operations

async def record_metric(
    metric_name: str,
    metric_value: float,
    channel: Optional[str] = None,
    dimensions: Optional[Dict[str, Any]] = None
) -> None:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO agent_metrics (metric_name, metric_value, channel, dimensions)
            VALUES ($1, $2, $3, $4)
            """,
            metric_name, metric_value, channel, json.dumps(dimensions or {})
        )


async def get_metrics_summary(
    hours: int = 24,
    channel: Optional[str] = None
) -> Dict[str, Any]:
    # Validate and clamp hours to prevent SQL injection via INTERVAL string interpolation
    hours = max(1, min(int(hours), 8760))  # 1 hour to 1 year (8760 hours)

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        query = f"""
            SELECT metric_name,
                   AVG(metric_value) as avg_value,
                   MIN(metric_value) as min_value,
                   MAX(metric_value) as max_value,
                   COUNT(*) as count
            FROM agent_metrics
            WHERE recorded_at > NOW() - INTERVAL '{hours} hours'
        """
        if channel:
            query += " AND channel = $1 GROUP BY metric_name"
            rows = await conn.fetch(query, channel)
        else:
            query += " GROUP BY metric_name"
            rows = await conn.fetch(query)
    return {row['metric_name']: dict(row) for row in rows}


async def anonymize_ticket_data(
    ticket_id: str,
    customer_id: str
) -> None:
    """
    Anonymize PII for GDPR 'right to erasure' compliance.

    Process:
    1. Anonymize all messages for this ticket
    2. Anonymize ticket subject
    3. Set gdpr_anonymized flag and resolution_notes
    4. If customer has NO other active tickets, anonymize customer record too

    Important: Does NOT set deleted_at — ticket remains visible in admin dashboard
    with anonymized content. Only regular soft-delete sets deleted_at.

    Args:
        ticket_id: Ticket to anonymize
        customer_id: Customer who owns the ticket
    """
    pool = await get_db_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            # Step 1: Anonymize all messages for this ticket
            await conn.execute(
                """
                UPDATE messages
                SET content = '[content removed per deletion request]',
                    metadata = jsonb_set(
                        COALESCE(metadata, '{}'::jsonb),
                        '{anonymized}',
                        'true'::jsonb
                    )
                WHERE ticket_id = $1
                """,
                ticket_id
            )

            # Step 2: Anonymize ticket subject and mark as GDPR anonymized
            # Note: Do NOT set deleted_at — ticket should remain visible in admin dashboard
            await conn.execute(
                """
                UPDATE tickets
                SET subject = '[content removed per deletion request]',
                    gdpr_anonymized = TRUE,
                    resolution_notes = COALESCE(resolution_notes || E'\n\n', '') ||
                                      'GDPR erasure: Data anonymized on ' || NOW()::text
                WHERE id = $1
                """,
                ticket_id
            )

            # Step 3: Check if customer has any other active (non-deleted) tickets
            # Active ticket = deleted_at IS NULL (simple, no text matching)
            other_tickets_count = await conn.fetchval(
                """
                SELECT COUNT(*)
                FROM tickets
                WHERE customer_id = $1
                  AND id != $2
                  AND deleted_at IS NULL
                """,
                customer_id,
                ticket_id
            )

            # Step 4: If this was the only active ticket, anonymize customer record
            if other_tickets_count == 0:
                await conn.execute(
                    """
                    UPDATE customers
                    SET name = '[deleted user]',
                        email = CONCAT('deleted-', id, '@privacy-request.invalid'),
                        metadata = jsonb_set(
                            COALESCE(metadata, '{}'::jsonb),
                            '{anonymized}',
                            'true'::jsonb
                        )
                    WHERE id = $1
                    """,
                    customer_id
                )
                logger.info(
                    f"Customer {customer_id} fully anonymized (no other active tickets)"
                )
            else:
                logger.info(
                    f"Customer {customer_id} has {other_tickets_count} other tickets, "
                    f"customer record NOT anonymized"
                )

    logger.info(f"Ticket {ticket_id} data anonymized for GDPR compliance")