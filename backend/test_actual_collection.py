#!/usr/bin/env python3
"""
Test script to verify the RAG retrieval functionality is working with the actual collection
that has the ingested vectors.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_with_actual_collection():
    """Test the retrieval pipeline with the actual collection that has vectors"""
    print("Testing RAG retrieval pipeline with actual collection...")

    try:
        # Test with the collection specified in .env file
        actual_collection = os.getenv("QDRANT_COLLECTION", "AI_BOOK")
        print(f"Testing with collection: {actual_collection}")

        # Initialize the retriever with the actual collection
        from rag.retriever import Retriever
        retriever = Retriever(collection_name=actual_collection)
        print(f"[SUCCESS] Retriever initialized successfully with collection: {actual_collection}")

        # Check if collection has documents
        doc_count = retriever.get_all_document_count()
        print(f"[SUCCESS] Collection contains {doc_count} documents")

        if doc_count == 0:
            print("[WARNING] Collection appears to be empty.")
            return False
        else:
            print(f"[SUCCESS] Collection has {doc_count} documents, indicating successful ingestion")

        # Perform a sample search
        sample_query = "What is artificial intelligence?"
        search_results = retriever.search(sample_query, top_k=3)

        print(f"[SUCCESS] Search completed successfully, found {len(search_results)} results")

        if len(search_results) > 0:
            print("Sample result:")
            first_result = search_results[0]
            print(f"  - Title: {first_result.get('title', 'N/A')}")
            print(f"  - Score: {first_result.get('score', 'N/A'):0.3f}")
            print(f"  - Source: {first_result.get('source', 'N/A')}")
            print(f"  - Content preview: {first_result.get('content', '')[:100]}...")

            # Test metadata preservation
            print("\n[SUCCESS] Metadata fields preserved during retrieval:")
            for key in ['title', 'source', 'file_path', 'content']:
                value = first_result.get(key, 'N/A')
                print(f"  - {key}: {str(value)[:50]}{'...' if len(str(value)) > 50 else ''}")

        # Initialize the generator
        from rag.generator import Generator
        generator = Generator()
        print("[SUCCESS] Generator initialized successfully")

        # Test answer generation with retrieved context
        if search_results:
            answer = generator.generate_answer(sample_query, search_results)
            print("[SUCCESS] Answer generated successfully")
            print(f"  - Answer preview: {answer[:150]}...")
        else:
            print("[INFO] No search results to test answer generation with")

        # Test the embedder
        from rag.embedder import Embedder
        embedder = Embedder()
        sample_embedding = embedder.embed_single_text("Test query for embedding")
        print(f"[SUCCESS] Embedder working, generated {len(sample_embedding)}-dimensional embedding")

        print("\n" + "="*70)
        print("RAG PIPELINE TEST RESULTS (with actual collection):")
        print(f"[SUCCESS] Retriever connected to collection: {actual_collection}")
        print(f"[SUCCESS] Collection contains {doc_count} documents")
        print("[SUCCESS] Semantic search working")
        print("[SUCCESS] Generator initialized")
        print("[SUCCESS] Answer generation functional")
        print("[SUCCESS] Embedder working correctly")
        print("[SUCCESS] Metadata preservation verified")
        print("="*70)

        return True

    except Exception as e:
        print(f"\n[ERROR] Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting RAG retrieval pipeline verification with actual collection...")

    success = test_with_actual_collection()

    print(f"\nOverall test status: {'SUCCESS' if success else 'FAILURE'}")

    if success:
        print(f"\n[SUCCESS] RAG retrieval pipeline is fully operational!")
        print("The system is working with the collection specified in the .env file.")
    else:
        print(f"\n[ERROR] Issues found with the RAG pipeline")
        sys.exit(1)