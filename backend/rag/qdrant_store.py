"""Qdrant vector store setup and operations."""

import os
import logging
from typing import List, Dict, Any, Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

logger = logging.getLogger(__name__)

# Cohere embed-english-v3.0 produces 1024-dimensional vectors
VECTOR_SIZE = 1024
COLLECTION_NAME = "knowledge_base"

_client: Optional[AsyncQdrantClient] = None


def get_qdrant_client() -> AsyncQdrantClient:
    """Get or create async Qdrant client."""
    global _client
    if _client is None:
        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")
        if not url or not api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set")
        _client = AsyncQdrantClient(url=url, api_key=api_key)
        logger.info("Qdrant async client initialized")
    return _client


async def create_collection_if_not_exists() -> None:
    """Create Qdrant collection if it doesn't exist."""
    client = get_qdrant_client()

    collections = await client.get_collections()
    existing = [c.name for c in collections.collections]

    if COLLECTION_NAME not in existing:
        await client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )
        logger.info(f"Collection '{COLLECTION_NAME}' created")
    else:
        logger.info(f"Collection '{COLLECTION_NAME}' already exists")


async def upsert_documents(
    ids: List[int],
    vectors: List[List[float]],
    payloads: List[Dict[str, Any]],
) -> None:
    """Insert or update documents in Qdrant."""
    client = get_qdrant_client()

    points = [
        PointStruct(
            id=ids[i],
            vector=vectors[i],
            payload=payloads[i],
        )
        for i in range(len(ids))
    ]

    await client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    logger.info(f"Upserted {len(points)} documents into Qdrant")


async def search_similar(
    query_vector: List[float],
    limit: int = 10,
    category_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search for similar documents in Qdrant."""
    client = get_qdrant_client()

    query_filter = None
    if category_filter:
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="category",
                    match=MatchValue(value=category_filter),
                )
            ]
        )

    results = await client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        query_filter=query_filter,
        with_payload=True,
    )

    return [
        {
            "id": hit.id,
            "score": hit.score,
            "title": hit.payload.get("title", ""),
            "content": hit.payload.get("content", ""),
            "category": hit.payload.get("category", ""),
        }
        for hit in results.points
    ]


async def get_collection_info() -> Dict[str, Any]:
    """Get collection stats."""
    client = get_qdrant_client()
    info = await client.get_collection(COLLECTION_NAME)
    return {
        "name": COLLECTION_NAME,
        "points_count": info.points_count or 0,
        "status": str(info.status),
    }