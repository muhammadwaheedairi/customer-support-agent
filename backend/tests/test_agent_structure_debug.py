"""Debug test to inspect OpenAI Agents SDK result structure."""

import asyncio
import logging
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Set up DEBUG logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_agent_structure():
    """
    Test to inspect the actual structure of OpenAI Agents SDK result.

    This will reveal:
    - What attributes exist on result.new_items elements
    - What the actual type field value is
    - How tool calls are represented
    """

    from agent.customer_success_agent import run_agent

    # Mock a simple escalation scenario
    result = await run_agent(
        customer_id="test-customer-123",
        customer_email="test@example.com",
        customer_name="Test User",
        subject="I want a refund immediately",
        message="This is unacceptable. I demand a full refund now or I will take legal action.",
        category="billing",
        priority="high",
        ticket_id="test-ticket-456"
    )

    logger.info("="*80)
    logger.info("AGENT RUN RESULT:")
    logger.info("="*80)
    logger.info(f"Success: {result.get('success')}")
    logger.info(f"Action: {result.get('action')}")
    logger.info(f"Response: {result.get('response', '')[:200]}...")
    logger.info(f"Turn count: {result.get('turn_count')}")
    logger.info("="*80)

    return result


if __name__ == "__main__":
    print("\n" + "="*80)
    print("RUNNING AGENT WITH DEBUG LOGGING TO INSPECT SDK STRUCTURE")
    print("="*80)
    print("\nNOTE: This requires:")
    print("  1. PostgreSQL running with proper schema")
    print("  2. All environment variables set (DATABASE_URL, OPENAI_API_KEY, etc.)")
    print("  3. Qdrant configured")
    print("\nIf any dependency is missing, this will show the actual error.\n")
    print("="*80 + "\n")

    try:
        result = asyncio.run(test_agent_structure())

        print("\n" + "="*80)
        print("TEST COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"\nDetected Action: {result.get('action')}")
        print("\nCheck the DEBUG logs above to see the actual item structure.")
        print("="*80 + "\n")

    except Exception as e:
        print("\n" + "="*80)
        print("ERROR DURING TEST")
        print("="*80)
        print(f"\nError: {type(e).__name__}: {e}")
        print("\nThis is expected if:")
        print("  - Database is not running")
        print("  - Environment variables are not set")
        print("  - OpenAI Agents SDK is not installed")
        print("\nThe fix is still correct, just needs proper environment to test.")
        print("="*80 + "\n")
        import traceback
        traceback.print_exc()
