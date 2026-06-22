"""Database module for Customer Success Agent."""

from .queries import (
    get_db_pool,
    close_db_pool,
    create_customer,
    get_customer_by_email,
    create_ticket,
    get_ticket_by_id,
    update_ticket_status,
    create_message,
    get_messages_by_ticket,
    create_conversation,
    get_conversation_by_id,
    search_knowledge_base,
    record_metric,
)

__all__ = [
    "get_db_pool",
    "close_db_pool",
    "create_customer",
    "get_customer_by_email",
    "create_ticket",
    "get_ticket_by_id",
    "update_ticket_status",
    "create_message",
    "get_messages_by_ticket",
    "create_conversation",
    "get_conversation_by_id",
    "search_knowledge_base",
    "record_metric",
]
