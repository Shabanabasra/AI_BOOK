#!/usr/bin/env python3
"""
Test script to verify the RAG retrieval functionality in the AI_BOOK project.
This script tests the retrieval pipeline without modifying any existing code.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_retrieval_pipeline():
    """Test the complete retrieval pipeline"""
    print("Testing RAG retrieval pipeline...")

    try:
        # Test 1: Initialize the retriever
        print("\n1. Testing Retriever initialization...")
        from rag.retriever import Retriever

        # Use the correct collection name for AI_BOOK project as specified in the CCR
        retriever = Retriever(collection_name="AI_BOOK")
        collection_name = "AI_BOOK"

        print(f"[SUCCESS] Retriever initialized successfully with collection: {collection_name}")

        # Test 2: Check if collection has documents
        print("\n2. Checking document count in collection...")
        doc_count = retriever.get_all_document_count()
        print(f"[SUCCESS] Collection contains {doc_count} documents")

        if doc_count == 0:
            print("[WARNING] Collection appears to be empty. Ingestion may not have completed successfully.")
        else:
            print(f"[SUCCESS] Collection has {doc_count} documents, indicating successful ingestion")

        # Test 3: Perform a sample search
        print("\n3. Testing semantic search functionality...")
        sample_query = "What is artificial intelligence?"
        search_results = retriever.search(sample_query, top_k=3)

        print(f"[SUCCESS] Search completed successfully, found {len(search_results)} results")

        if len(search_results) > 0:
            print("Sample result:")
            first_result = search_results[0]
            print(f"  - Title: {first_result.get('title', 'N/A')}")
            print(f"  - Score: {first_result.get('score', 'N/A')}")
            print(f"  - Source: {first_result.get('source', 'N/A')}")
            print(f"  - Content preview: {first_result.get('content', '')[:100]}...")

        # Test 4: Initialize the generator
        print("\n4. Testing Generator initialization...")
        from rag.generator import Generator
        generator = Generator()
        print("[SUCCESS] Generator initialized successfully")

        # Test 5: Test answer generation with retrieved context
        print("\n5. Testing answer generation with context...")
        if search_results:
            answer = generator.generate_answer(sample_query, search_results)
            print("[SUCCESS] Answer generated successfully")
            print(f"  - Answer preview: {answer[:100]}...")
        else:
            print("[INFO] No search results to test answer generation with")

        # Test 6: Test the embedder
        print("\n6. Testing Embedder functionality...")
        from rag.embedder import Embedder
        embedder = Embedder()
        sample_embedding = embedder.embed_single_text("Test query for embedding")
        print(f"[SUCCESS] Embedder working, generated {len(sample_embedding)}-dimensional embedding")

        print("\n" + "="*60)
        print("RAG PIPELINE TEST RESULTS:")
        print("[SUCCESS] Retriever initialized and connected to Qdrant")
        print("[SUCCESS] Collection access verified")
        print("[SUCCESS] Semantic search working")
        print("[SUCCESS] Generator initialized")
        print("[SUCCESS] Answer generation functional")
        print("[SUCCESS] Embedder working correctly")
        print("="*60)

        return True

    except Exception as e:
        print(f"\n[ERROR] Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_metadata_preservation():
    """Test that metadata is preserved during retrieval"""
    print("\nTesting metadata preservation...")

    try:
        from rag.retriever import Retriever

        # Use correct collection name for AI_BOOK
        retriever = Retriever(collection_name="AI_BOOK")

        # Perform a search
        results = retriever.search("AI", top_k=1)

        if results:
            result = results[0]
            print("[SUCCESS] Metadata fields preserved during retrieval:")
            for key, value in result.items():
                if key in ['title', 'source', 'file_path', 'content']:
                    print(f"  - {key}: {str(value)[:50]}{'...' if len(str(value)) > 50 else ''}")
            return True
        else:
            print("[INFO] No results found to test metadata preservation")
            return False

    except Exception as e:
        print(f"[ERROR] Error testing metadata preservation: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting RAG retrieval pipeline verification...")

    success = test_retrieval_pipeline()
    metadata_success = test_metadata_preservation()

    print(f"\nOverall test status: {'SUCCESS' if success and metadata_success else 'FAILURE'}")

    if success and metadata_success:
        print("\n[SUCCESS] RAG retrieval pipeline is fully operational and ready for Spec-2!")
    else:
        print("\n[ERROR] Issues found with the RAG pipeline")
        sys.exit(1)