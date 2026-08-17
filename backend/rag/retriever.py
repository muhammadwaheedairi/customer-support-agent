"""RAG retriever with Cohere Reranking (Corrective RAG)."""

import os
import logging
from typing import List, Dict, Any, Optional
import cohere

from rag.embedder import embed_query
from rag.qdrant_store import search_similar

logger = logging.getLogger(__name__)

_rerank_client = None


def get_rerank_client() -> cohere.AsyncClientV2:
    """Get Cohere client for reranking."""
    global _rerank_client
    if _rerank_client is None:
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY not set")
        _rerank_client = cohere.AsyncClientV2(api_key=api_key)
    return _rerank_client


async def retrieve(
    query: str,
    top_k: int = 3,
    category_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Full RAG retrieval pipeline with Corrective RAG:
    1. Embed query with Cohere (search_query type)
    2. Search Qdrant for top 10 candidates
    3. Rerank with Cohere Rerank v3 → return best top_k

    Args:
        query: Customer query text
        top_k: Final number of results after reranking
        category_filter: Optional category filter

    Returns:
        List of top_k reranked documents
    """
    if not query.strip():
        return []

    # Step 1: Embed query
    logger.info(f"Embedding query: {query[:60]}...")
    query_vector = await embed_query(query)

    # Step 2: Qdrant semantic search — get top 10 candidates
    candidates = await search_similar(
        query_vector=query_vector,
        limit=10,
        category_filter=category_filter,
    )

    if not candidates:
        logger.info("No candidates found in Qdrant")
        return []

    if len(candidates) <= top_k:
        # Not enough candidates to rerank — return as is
        return candidates

    # Step 3: Cohere Rerank — Corrective RAG
    logger.info(f"Reranking {len(candidates)} candidates with Cohere...")
    client = get_rerank_client()

    documents = [
        f"{c['title']}\n\n{c['content']}"
        for c in candidates
    ]

    rerank_response = await client.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=documents,
        top_n=top_k,
    )

    # Map reranked results back to original candidates
    reranked = []
    for result in rerank_response.results:
        original = candidates[result.index]
        reranked.append({
            **original,
            "relevance_score": result.relevance_score,
        })

    logger.info(f"Reranking complete — top {top_k} results selected")
    return reranked


def format_results_for_agent(results: List[Dict[str, Any]]) -> str:
    """
    Format retrieved results as clean text for agent context.

    Args:
        results: List of retrieved documents

    Returns:
        Formatted string for agent prompt
    """
    if not results:
        return "No relevant documentation found."

    formatted = []
    for i, doc in enumerate(results, 1):
        score = doc.get("relevance_score", doc.get("score", 0))
        formatted.append(
            f"{i}. **{doc['title']}**\n"
            f"   Relevance: {score:.2f}\n"
            f"   {doc['content'][:400]}"
        )

    return "\n\n".join(formatted)