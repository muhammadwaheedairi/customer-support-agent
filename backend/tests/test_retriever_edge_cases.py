"""Tests for RAG retriever edge cases and error handling."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from rag.retriever import retrieve


@pytest.mark.asyncio
async def test_retrieve_handles_out_of_bounds_rerank_index():
    """Test that retrieve() gracefully handles out-of-bounds indices from Cohere rerank."""

    # Mock candidates from Qdrant
    mock_candidates = [
        {"id": f"doc-{i}", "title": f"Title {i}", "content": f"Content {i}", "category": "general"}
        for i in range(10)
    ]

    # Mock rerank response with INVALID indices (out of bounds)
    mock_rerank_result_1 = MagicMock()
    mock_rerank_result_1.index = 999  # Out of bounds!
    mock_rerank_result_1.relevance_score = 0.95

    mock_rerank_result_2 = MagicMock()
    mock_rerank_result_2.index = -1  # Invalid negative index!
    mock_rerank_result_2.relevance_score = 0.92

    mock_rerank_result_3 = MagicMock()
    mock_rerank_result_3.index = 15  # Out of bounds!
    mock_rerank_result_3.relevance_score = 0.90

    mock_rerank_response = MagicMock()
    mock_rerank_response.results = [mock_rerank_result_1, mock_rerank_result_2, mock_rerank_result_3]

    mock_cohere_client = AsyncMock()
    mock_cohere_client.rerank = AsyncMock(return_value=mock_rerank_response)

    # Patch dependencies
    with patch('rag.retriever.embed_query', new_callable=AsyncMock) as mock_embed, \
         patch('rag.retriever.search_similar', new_callable=AsyncMock) as mock_search, \
         patch('rag.retriever.get_rerank_client', return_value=mock_cohere_client):

        mock_embed.return_value = [0.1] * 1024  # Mock embedding
        mock_search.return_value = mock_candidates

        # Call retrieve - should NOT crash despite invalid indices
        result = await retrieve(query="test query", top_k=3)

        # Verify: function should fall back to returning top_k candidates without reranking
        assert result is not None, "Result should not be None"
        assert len(result) == 3, f"Should return top_k=3 candidates, got {len(result)}"

        # Should be first 3 candidates (fallback behavior since all rerank indices were invalid)
        assert result[0]["id"] == "doc-0"
        assert result[1]["id"] == "doc-1"
        assert result[2]["id"] == "doc-2"

        print("✅ Test passed: Out-of-bounds rerank indices handled gracefully")
        print(f"   Returned {len(result)} fallback candidates")


@pytest.mark.asyncio
async def test_retrieve_handles_partial_invalid_rerank_indices():
    """Test that retrieve() handles mix of valid and invalid rerank indices."""

    # Mock candidates
    mock_candidates = [
        {"id": f"doc-{i}", "title": f"Title {i}", "content": f"Content {i}", "category": "general"}
        for i in range(10)
    ]

    # Mix of valid and invalid indices
    mock_rerank_result_1 = MagicMock()
    mock_rerank_result_1.index = 999  # Invalid!
    mock_rerank_result_1.relevance_score = 0.95

    mock_rerank_result_2 = MagicMock()
    mock_rerank_result_2.index = 2  # Valid
    mock_rerank_result_2.relevance_score = 0.90

    mock_rerank_result_3 = MagicMock()
    mock_rerank_result_3.index = 5  # Valid
    mock_rerank_result_3.relevance_score = 0.85

    mock_rerank_response = MagicMock()
    mock_rerank_response.results = [mock_rerank_result_1, mock_rerank_result_2, mock_rerank_result_3]

    mock_cohere_client = AsyncMock()
    mock_cohere_client.rerank = AsyncMock(return_value=mock_rerank_response)

    with patch('rag.retriever.embed_query', new_callable=AsyncMock) as mock_embed, \
         patch('rag.retriever.search_similar', new_callable=AsyncMock) as mock_search, \
         patch('rag.retriever.get_rerank_client', return_value=mock_cohere_client):

        mock_embed.return_value = [0.1] * 1024
        mock_search.return_value = mock_candidates

        result = await retrieve(query="test query", top_k=3)

        # Should return only the 2 valid reranked results (skipping invalid index 999)
        assert result is not None
        assert len(result) == 2, f"Should return 2 valid results, got {len(result)}"
        assert result[0]["id"] == "doc-2", "First result should be from valid index 2"
        assert result[1]["id"] == "doc-5", "Second result should be from valid index 5"
        assert "relevance_score" in result[0], "Should have relevance_score from reranking"

        print("✅ Test passed: Partial invalid indices handled, valid results returned")
        print(f"   Returned {len(result)} valid reranked candidates (skipped 1 invalid)")


@pytest.mark.asyncio
async def test_retrieve_handles_rerank_exception():
    """Test that retrieve() falls back gracefully when Cohere rerank throws exception."""

    mock_candidates = [
        {"id": f"doc-{i}", "title": f"Title {i}", "content": f"Content {i}", "category": "general"}
        for i in range(10)
    ]

    mock_cohere_client = AsyncMock()
    # Simulate Cohere API failure
    mock_cohere_client.rerank = AsyncMock(side_effect=Exception("Cohere API timeout"))

    with patch('rag.retriever.embed_query', new_callable=AsyncMock) as mock_embed, \
         patch('rag.retriever.search_similar', new_callable=AsyncMock) as mock_search, \
         patch('rag.retriever.get_rerank_client', return_value=mock_cohere_client):

        mock_embed.return_value = [0.1] * 1024
        mock_search.return_value = mock_candidates

        # Should NOT crash despite rerank exception
        result = await retrieve(query="test query", top_k=3)

        assert result is not None
        assert len(result) == 3, f"Should fall back to top 3 candidates, got {len(result)}"
        assert result[0]["id"] == "doc-0"

        print("✅ Test passed: Rerank exception handled, fallback to candidates")
        print(f"   Returned {len(result)} candidates without reranking")


if __name__ == "__main__":
    import asyncio

    print("\n" + "="*70)
    print("Testing RAG Retriever Edge Cases")
    print("="*70 + "\n")

    print("Test 1: All rerank indices out of bounds")
    print("-" * 70)
    asyncio.run(test_retrieve_handles_out_of_bounds_rerank_index())

    print("\n\nTest 2: Mix of valid and invalid rerank indices")
    print("-" * 70)
    asyncio.run(test_retrieve_handles_partial_invalid_rerank_indices())

    print("\n\nTest 3: Rerank API exception")
    print("-" * 70)
    asyncio.run(test_retrieve_handles_rerank_exception())

    print("\n" + "="*70)
    print("All edge case tests passed! ✅")
    print("="*70)
