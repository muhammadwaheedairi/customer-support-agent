"""Tests for GDPR 'right to erasure' ticket anonymization."""

import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch, AsyncMock
import asyncpg

from api.main import app, get_current_user
from database.queries import (
    get_db_pool,
    create_customer,
    create_ticket,
    create_message,
    get_ticket_by_id,
    get_messages_by_ticket,
    get_customer_by_email,
    anonymize_ticket_data,
)


# Mock authentication
def mock_get_current_user():
    return "test-user-gdpr-123"


app.dependency_overrides[get_current_user] = mock_get_current_user


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_anonymize_ticket_data_removes_pii():
    """
    Test that anonymize_ticket_data() properly removes all PII from ticket and messages.
    Verifies:
    - Message content is anonymized
    - Ticket subject is anonymized
    - Customer data is anonymized (if no other tickets)
    - Ticket record still exists for metrics
    """
    # Skip if no database connection available
    try:
        pool = await get_db_pool()
    except Exception:
        pytest.skip("Database not available for integration test")
        return

    # Setup: Create test customer, ticket, and messages
    test_email = f"gdpr-test-{id(test_anonymize_ticket_data_removes_pii)}@example.com"
    test_name = "John GDPR Tester"
    test_subject = "Sensitive information in subject line"
    test_message_1 = "My credit card number is 1234-5678-9012-3456"
    test_message_2 = "My SSN is 123-45-6789 and I live at 123 Main St"

    try:
        # Create customer
        customer_id = await create_customer(
            email=test_email,
            name=test_name,
            clerk_user_id="test-user-gdpr-123"
        )

        # Create ticket
        ticket_id = await create_ticket(
            customer_id=customer_id,
            subject=test_subject,
            category="billing",
            message=test_message_1,
            priority="high",
            channel="web_form",
            clerk_user_id="test-user-gdpr-123"
        )

        # Add additional message
        await create_message(
            ticket_id=ticket_id,
            role="agent",
            content=test_message_2
        )

        # Verify data exists BEFORE anonymization
        ticket_before = await get_ticket_by_id(ticket_id)
        messages_before = await get_messages_by_ticket(ticket_id)
        customer_before = await pool.fetchrow(
            "SELECT id, email, name FROM customers WHERE id = $1",
            customer_id
        )

        assert ticket_before["subject"] == test_subject
        assert any(test_message_1 in msg["content"] for msg in messages_before)
        assert customer_before["name"] == test_name
        assert customer_before["email"] == test_email

        # ACT: Anonymize ticket data
        await anonymize_ticket_data(ticket_id=ticket_id, customer_id=customer_id)

        # ASSERT: Verify PII is removed
        # Note: get_ticket_by_id filters deleted tickets, so query directly
        async with pool.acquire() as conn:
            ticket_after = await conn.fetchrow(
                """
                SELECT t.id, t.subject, t.status, t.category, t.created_at,
                       t.deleted_at, t.resolution_notes
                FROM tickets t
                WHERE t.id = $1
                """,
                ticket_id
            )

        messages_after = await get_messages_by_ticket(ticket_id)
        customer_after = await pool.fetchrow(
            "SELECT id, email, name FROM customers WHERE id = $1",
            customer_id
        )

        # 1. Ticket subject should be anonymized
        assert ticket_after["subject"] == "[content removed per deletion request]"
        assert ticket_after["subject"] != test_subject

        # 2. All messages should be anonymized
        for msg in messages_after:
            assert msg["content"] == "[content removed per deletion request]"
            assert test_message_1 not in msg["content"]
            assert test_message_2 not in msg["content"]
            assert "1234-5678" not in msg["content"]
            assert "123-45-6789" not in msg["content"]

        # 3. Customer record should be anonymized (since this was their only ticket)
        assert customer_after["name"] == "[deleted user]"
        assert customer_after["name"] != test_name
        assert customer_after["email"].startswith("deleted-")
        assert customer_after["email"] != test_email
        assert "@privacy-request.invalid" in customer_after["email"]

        # 4. Ticket record should STILL EXIST for metrics
        assert ticket_after is not None
        assert str(ticket_after["id"]) == ticket_id
        assert ticket_after["status"] is not None
        assert ticket_after["category"] == "billing"
        assert ticket_after["created_at"] is not None
        assert ticket_after["deleted_at"] is not None

        # 5. Verify GDPR erasure note in resolution_notes
        assert "GDPR erasure" in ticket_after.get("resolution_notes", "")

        print("✅ Test passed: All PII successfully anonymized")
        print(f"   - Ticket subject: anonymized")
        print(f"   - {len(messages_after)} messages: anonymized")
        print(f"   - Customer name: '{test_name}' → '[deleted user]'")
        print(f"   - Customer email: '{test_email}' → '{customer_after['email']}'")
        print(f"   - Ticket record preserved for metrics (ID: {ticket_id})")

    finally:
        # Cleanup: Delete test data
        async with pool.acquire() as conn:
            await conn.execute("DELETE FROM messages WHERE ticket_id = $1", ticket_id)
            await conn.execute("DELETE FROM conversations WHERE ticket_id = $1", ticket_id)
            await conn.execute("DELETE FROM tickets WHERE id = $1", ticket_id)
            await conn.execute("DELETE FROM customers WHERE id = $1", customer_id)


@pytest.mark.asyncio
async def test_anonymize_preserves_other_customer_tickets():
    """
    Test that customer record is NOT anonymized if they have other active tickets.
    """
    try:
        pool = await get_db_pool()
    except Exception:
        pytest.skip("Database not available")
        return

    test_email = f"multi-ticket-{id(test_anonymize_preserves_other_customer_tickets)}@example.com"
    test_name = "Jane Multi-Ticket User"

    try:
        # Create customer
        customer_id = await create_customer(
            email=test_email,
            name=test_name,
            clerk_user_id="test-user-gdpr-123"
        )

        # Create TWO tickets
        ticket_id_1 = await create_ticket(
            customer_id=customer_id,
            subject="First ticket",
            category="general",
            message="First ticket message",
            clerk_user_id="test-user-gdpr-123"
        )

        ticket_id_2 = await create_ticket(
            customer_id=customer_id,
            subject="Second ticket",
            category="technical",
            message="Second ticket message",
            clerk_user_id="test-user-gdpr-123"
        )

        # Anonymize only FIRST ticket
        await anonymize_ticket_data(ticket_id=ticket_id_1, customer_id=customer_id)

        # Verify: First ticket anonymized (query directly since it's deleted)
        async with pool.acquire() as conn:
            ticket_1_after = await conn.fetchrow(
                "SELECT subject FROM tickets WHERE id = $1",
                ticket_id_1
            )
        assert ticket_1_after["subject"] == "[content removed per deletion request]"

        # Verify: Customer record NOT anonymized (has other active ticket)
        customer_after = await pool.fetchrow(
            "SELECT name, email FROM customers WHERE id = $1",
            customer_id
        )
        assert customer_after["name"] == test_name  # NOT anonymized
        assert customer_after["email"] == test_email  # NOT anonymized

        print("✅ Test passed: Customer record preserved when other tickets exist")
        print(f"   - Ticket 1: anonymized")
        print(f"   - Ticket 2: active")
        print(f"   - Customer record: NOT anonymized (correctly)")

    finally:
        # Cleanup
        async with pool.acquire() as conn:
            await conn.execute("DELETE FROM messages WHERE ticket_id IN ($1, $2)", ticket_id_1, ticket_id_2)
            await conn.execute("DELETE FROM conversations WHERE ticket_id IN ($1, $2)", ticket_id_1, ticket_id_2)
            await conn.execute("DELETE FROM tickets WHERE id IN ($1, $2)", ticket_id_1, ticket_id_2)
            await conn.execute("DELETE FROM customers WHERE id = $1", customer_id)


@pytest.mark.asyncio
async def test_delete_endpoint_with_permanent_flag(client):
    """
    Test DELETE /tickets/{ticket_id}?permanent=true endpoint behavior.
    """
    ticket_id = "test-permanent-delete-123"

    # Mock the anonymize_ticket_data function
    with patch('api.main.anonymize_ticket_data', new_callable=AsyncMock) as mock_anonymize, \
         patch('api.main.get_db_pool') as mock_pool:

        # Mock database response
        mock_conn = AsyncMock()
        mock_ticket = {
            "id": ticket_id,
            "clerk_user_id": "test-user-gdpr-123",
            "customer_id": "cust-123"
        }
        mock_conn.fetchrow = AsyncMock(return_value=mock_ticket)

        # Create proper async context manager for acquire()
        from unittest.mock import MagicMock
        mock_acquire_cm = MagicMock()
        mock_acquire_cm.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_acquire_cm.__aexit__ = AsyncMock(return_value=None)

        mock_pool_instance = AsyncMock()
        mock_pool_instance.acquire = MagicMock(return_value=mock_acquire_cm)
        mock_pool.return_value = mock_pool_instance

        # Test with permanent=true
        response = await client.delete(f"/tickets/{ticket_id}?permanent=true")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["permanent"] is True
        assert "anonymized" in data["message"].lower()

        # Verify anonymize_ticket_data was called
        mock_anonymize.assert_called_once_with(
            ticket_id=ticket_id,
            customer_id="cust-123"
        )

        print("✅ Test passed: DELETE endpoint with permanent=true calls anonymization")


@pytest.mark.asyncio
async def test_delete_endpoint_without_permanent_flag(client):
    """
    Test DELETE /tickets/{ticket_id} (default soft delete).
    """
    ticket_id = "test-soft-delete-123"

    with patch('api.main.get_db_pool') as mock_pool:

        mock_conn = AsyncMock()
        mock_ticket = {
            "id": ticket_id,
            "clerk_user_id": "test-user-gdpr-123",
            "customer_id": "cust-123"
        }
        mock_conn.fetchrow = AsyncMock(return_value=mock_ticket)
        mock_conn.execute = AsyncMock()

        # Create proper async context manager for acquire()
        from unittest.mock import MagicMock
        mock_acquire_cm = MagicMock()
        mock_acquire_cm.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_acquire_cm.__aexit__ = AsyncMock(return_value=None)

        mock_pool_instance = AsyncMock()
        mock_pool_instance.acquire = MagicMock(return_value=mock_acquire_cm)
        mock_pool.return_value = mock_pool_instance

        # Test WITHOUT permanent flag (default soft delete)
        response = await client.delete(f"/tickets/{ticket_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["permanent"] is False
        assert "deleted successfully" in data["message"].lower()

        # Verify soft delete query was executed
        mock_conn.execute.assert_called_once()

        print("✅ Test passed: DELETE endpoint without permanent flag performs soft delete")


if __name__ == "__main__":
    import asyncio

    print("\n" + "="*70)
    print("Testing GDPR Anonymization Features")
    print("="*70 + "\n")

    print("Test 1: Complete PII anonymization")
    print("-" * 70)
    asyncio.run(test_anonymize_ticket_data_removes_pii())

    print("\n\nTest 2: Preserve customer with multiple tickets")
    print("-" * 70)
    asyncio.run(test_anonymize_preserves_other_customer_tickets())

    print("\n" + "="*70)
    print("GDPR anonymization tests completed! ✅")
    print("="*70)
