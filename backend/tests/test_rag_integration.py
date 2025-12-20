"""
Integration tests for the RAG system
Tests the complete flow from document ingestion to question answering
"""

import os
import tempfile
import pytest
from pathlib import Path

# Add backend to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.rag.loader import MarkdownLoader
from backend.rag.embedder import Embedder
from backend.rag.retriever import Retriever
from backend.rag.generator import Generator


def test_chunking_functionality():
    """Test that the chunking functionality works correctly"""
    # Create sample markdown content
    sample_content = """# Introduction to AI

Artificial Intelligence (AI) is intelligence demonstrated by machines. This paragraph contains information about AI concepts.

## History of AI

The field of AI research was born at a Dartmouth College workshop in 1956. This section describes the history of AI development.

Machine learning is a subset of AI that enables computers to learn from data. This concept is fundamental to modern AI applications.
"""

    # Create a temporary markdown file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(sample_content)
        temp_file_path = f.name

    try:
        # Test the loader with chunking
        loader = MarkdownLoader(docs_path=".", chunk_size=200, overlap_size=50)

        # Load and chunk the single file content
        from backend.rag.chunker import SemanticChunker, DocumentChunk
        chunker = SemanticChunker(max_chunk_size=200, overlap_size=50)
        chunks = chunker.chunk_text(sample_content, "Test Document", temp_file_path)

        # Verify we got multiple chunks
        assert len(chunks) > 1, "Content should be split into multiple chunks"

        # Verify chunk sizes are reasonable
        for chunk in chunks:
            assert len(chunk.content) <= 200, f"Chunk exceeds max size: {len(chunk.content)}"
            assert len(chunk.content) > 0, "Chunk should not be empty"

        print(f"✓ Successfully created {len(chunks)} chunks from sample content")

        # Verify chunk titles include the chunk index information
        for i, chunk in enumerate(chunks):
            assert f"Chunk {i+1}/{len(chunks)}" in chunk.title, f"Chunk title should include index: {chunk.title}"

        print("✓ Chunk titles correctly include index information")

    finally:
        # Clean up temp file
        os.unlink(temp_file_path)


def test_embedder_functionality():
    """Test that the embedder works correctly"""
    # Skip if COHERE_API_KEY is not set
    if not os.getenv("COHERE_API_KEY"):
        print("⚠️  Skipping embedder test - COHERE_API_KEY not set")
        return

    try:
        embedder = Embedder()

        # Test with sample texts
        sample_texts = [
            "Artificial Intelligence is a branch of computer science.",
            "Machine Learning is a subset of Artificial Intelligence.",
            "Natural Language Processing helps computers understand human language."
        ]

        embeddings = embedder.embed_texts(sample_texts)

        # Verify we got embeddings for all texts
        assert len(embeddings) == len(sample_texts), "Should get embeddings for all texts"

        # Verify each embedding has the right dimension
        expected_dim = embedder.get_embedding_dimension()
        for i, embedding in enumerate(embeddings):
            assert len(embedding) == expected_dim, f"Embedding {i} has wrong dimension: {len(embedding)} != {expected_dim}"

        print(f"✓ Successfully generated {len(embeddings)} embeddings with dimension {expected_dim}")

        # Test single text embedding
        single_embedding = embedder.embed_single_text("Test single text")
        assert len(single_embedding) == expected_dim, "Single embedding has wrong dimension"

        print("✓ Single text embedding works correctly")

    except ValueError as e:
        if "COHERE_API_KEY" in str(e):
            print("⚠️  Skipping embedder test - COHERE_API_KEY not set in environment")
        else:
            raise


def test_retriever_functionality():
    """Test that the retriever works correctly"""
    # Skip if required environment variables are not set
    if not (os.getenv("QDRANT_URL") and os.getenv("QDRANT_API_KEY")):
        print("⚠️  Skipping retriever test - QDRANT_URL or QDRANT_API_KEY not set")
        return

    try:
        retriever = Retriever(collection_name="test_ai_book_docs")

        # Test with sample documents
        sample_docs = [
            {
                "content": "Artificial Intelligence is intelligence demonstrated by machines.",
                "title": "AI Definition",
                "source": "test_doc1.md",
                "file_path": "test_doc1.md"
            },
            {
                "content": "Machine Learning is a subset of Artificial Intelligence that enables computers to learn.",
                "title": "Machine Learning",
                "source": "test_doc2.md",
                "file_path": "test_doc2.md"
            }
        ]

        # Add documents to retriever
        retriever.add_documents(sample_docs)

        # Verify documents were added
        doc_count = retriever.get_all_document_count()
        assert doc_count >= len(sample_docs), f"Expected at least {len(sample_docs)} documents, got {doc_count}"

        print(f"✓ Successfully added {len(sample_docs)} documents to retriever")

        # Test search functionality
        search_results = retriever.search("What is artificial intelligence?", top_k=2)
        assert len(search_results) > 0, "Should find relevant results"

        print(f"✓ Search returned {len(search_results)} relevant results")

        # Verify result structure
        for result in search_results:
            assert 'content' in result, "Result should have content"
            assert 'title' in result, "Result should have title"
            assert 'score' in result, "Result should have score"

        print("✓ Search results have correct structure")

    except ValueError as e:
        if "QDRANT" in str(e):
            print("⚠️  Skipping retriever test - QDRANT environment variables not set")
        else:
            raise


def test_complete_rag_flow():
    """Test the complete RAG flow: retrieval + generation"""
    # Skip if required environment variables are not set
    if not (os.getenv("COHERE_API_KEY") and os.getenv("QDRANT_URL") and os.getenv("QDRANT_API_KEY")):
        print("⚠️  Skipping complete RAG test - Required environment variables not set")
        return

    try:
        # Initialize components
        retriever = Retriever(collection_name="test_ai_book_docs")
        generator = Generator()

        # Test retrieval and generation
        query = "What is artificial intelligence?"
        context_chunks = retriever.search(query, top_k=2)

        if context_chunks:
            answer = generator.generate_answer(query, context_chunks)

            # Verify answer is not empty and not the fallback message
            assert answer != "This is not covered in the AI_BOOK.", "Generator should return valid answer when context is available"
            assert len(answer) > 0, "Answer should not be empty"

            print(f"✓ Successfully generated answer: {answer[:100]}...")
        else:
            print("⚠️  No context chunks found - this may be expected if no documents were ingested")

    except ValueError as e:
        if "COHERE_API_KEY" in str(e) or "QDRANT" in str(e):
            print("⚠️  Skipping complete RAG test - Required environment variables not set")
        else:
            raise


def main():
    """Run all integration tests"""
    print("Running RAG System Integration Tests...\n")

    print("1. Testing chunking functionality...")
    test_chunking_functionality()

    print("\n2. Testing embedder functionality...")
    test_embedder_functionality()

    print("\n3. Testing retriever functionality...")
    test_retriever_functionality()

    print("\n4. Testing complete RAG flow...")
    test_complete_rag_flow()

    print("\n✅ All integration tests completed!")


if __name__ == "__main__":
    main()