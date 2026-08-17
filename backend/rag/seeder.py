"""Seed product documentation into Qdrant vector store."""

import os
import sys
import asyncio
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.embedder import embed_documents
from rag.qdrant_store import create_collection_if_not_exists, upsert_documents, get_collection_info

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def chunk_markdown(content: str, max_chunk_size: int = 500) -> List[Dict[str, Any]]:
    """
    Split markdown content into chunks by ## headers.
    Each section becomes one chunk.

    Args:
        content: Full markdown text
        max_chunk_size: Max characters per chunk

    Returns:
        List of dicts with title, content, category
    """
    chunks = []
    sections = content.split("\n## ")

    for i, section in enumerate(sections):
        if not section.strip():
            continue

        lines = section.strip().split("\n")
        title = lines[0].replace("#", "").strip()
        body = "\n".join(lines[1:]).strip()

        if not body:
            continue

        # Determine category from title
        title_lower = title.lower()
        if any(word in title_lower for word in ["price", "plan", "billing", "cost"]):
            category = "billing"
        elif any(word in title_lower for word in ["error", "bug", "fix", "troubleshoot", "issue"]):
            category = "technical"
        elif any(word in title_lower for word in ["how to", "guide", "setup", "install", "start"]):
            category = "guide"
        else:
            category = "general"

        # Split large sections further if needed
        if len(body) > max_chunk_size:
            sub_sections = body.split("\n### ")
            for j, sub in enumerate(sub_sections):
                if not sub.strip():
                    continue
                sub_lines = sub.strip().split("\n")
                sub_title = sub_lines[0].replace("#", "").strip()
                sub_body = "\n".join(sub_lines[1:]).strip()
                if sub_body:
                    chunks.append({
                        "title": f"{title} — {sub_title}" if sub_title != sub_lines[0] else title,
                        "content": sub_body[:max_chunk_size],
                        "category": category,
                    })
        else:
            chunks.append({
                "title": title,
                "content": body,
                "category": category,
            })

    return chunks


async def seed_from_file(filepath: str) -> int:
    """
    Read a markdown file, chunk it, embed it, and store in Qdrant.

    Args:
        filepath: Path to markdown file

    Returns:
        Number of chunks seeded
    """
    logger.info(f"Reading file: {filepath}")
    content = open(filepath, "r").read()

    # Chunk the content
    chunks = chunk_markdown(content)
    logger.info(f"Created {len(chunks)} chunks")

    if not chunks:
        logger.warning("No chunks created — check file content")
        return 0

    # Create Qdrant collection
    await create_collection_if_not_exists()

    # Embed all chunks
    texts = [f"{c['title']}\n\n{c['content']}" for c in chunks]
    logger.info(f"Embedding {len(texts)} chunks with Cohere...")
    vectors = await embed_documents(texts)

    # Prepare IDs and payloads
    ids = list(range(1, len(chunks) + 1))
    payloads = chunks

    # Upsert into Qdrant
    await upsert_documents(ids=ids, vectors=vectors, payloads=payloads)

    # Verify
    info = await get_collection_info()
    logger.info(f"Qdrant collection info: {info}")

    return len(chunks)


async def main():
    """Main seeding function."""
    # Path to product docs
    docs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "context",
        "product-docs.md"
    )

    if not os.path.exists(docs_path):
        logger.error(f"File not found: {docs_path}")
        logger.error("Make sure context/product-docs.md exists in project root")
        return

    count = await seed_from_file(docs_path)
    print(f"\n✅ Successfully seeded {count} chunks into Qdrant!")
    print("Knowledge base is ready for semantic search.")


if __name__ == "__main__":
    asyncio.run(main())