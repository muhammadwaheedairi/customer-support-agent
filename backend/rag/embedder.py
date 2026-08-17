"""Cohere embeddings generator for RAG pipeline."""

import os
import logging
from typing import List
import cohere

logger = logging.getLogger(__name__)

_client = None


def get_cohere_client() -> cohere.AsyncClientV2:
    """Get or create Cohere async client."""
    global _client
    if _client is None:
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")
        _client = cohere.AsyncClientV2(api_key=api_key)
        logger.info("Cohere client initialized")
    return _client


async def embed_documents(texts: List[str]) -> List[List[float]]:
    """
    Embed documents for storage in Qdrant.
    Uses input_type='search_document' for optimized document storage.

    Args:
        texts: List of document texts to embed

    Returns:
        List of embedding vectors
    """
    client = get_cohere_client()

    response = await client.embed(
        model="embed-english-v3.0",
        input_type="search_document",
        texts=texts,
        embedding_types=["float"]
    )

    embeddings = response.embeddings.float_
    logger.info(f"Embedded {len(texts)} documents")
    return embeddings


async def embed_query(query: str) -> List[float]:
    """
    Embed a search query.
    Uses input_type='search_query' for optimized query retrieval.

    Args:
        query: Customer query text

    Returns:
        Embedding vector
    """
    client = get_cohere_client()

    response = await client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts=[query],
        embedding_types=["float"]
    )

    embedding = response.embeddings.float_[0]
    logger.info(f"Embedded query: {query[:50]}...")
    return embedding