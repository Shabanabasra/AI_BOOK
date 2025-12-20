#!/usr/bin/env python3
"""
Test script to verify the retrieval functionality is working with the correct Qdrant collection.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.retriever import Retriever
from rag.generator import Generator
import os
from dotenv import load_dotenv

def test_retrieval_functionality():
    # Load environment variables
    load_dotenv()

    print("Testing retrieval functionality...")
    print(f"QDRANT_COLLECTION: {os.getenv('QDRANT_COLLECTION', 'AI_BOOK')}")
    print(f"QDRANT_URL: {os.getenv('QDRANT_URL', 'Not set')}")
    print(f"QDRANT_API_KEY: {'Set' if os.getenv('QDRANT_API_KEY') else 'Not set'}")

    try:
        # Initialize retriever (will use QDRANT_COLLECTION environment variable)
        retriever = Retriever()
        print(f"[SUCCESS] Retriever initialized successfully with collection: {retriever.collection_name}")

        # Check collection info
        collection_info = retriever.client.get_collection(collection_name=retriever.collection_name)
        print(f"[SUCCESS] Collection '{retriever.collection_name}' exists with {collection_info.points_count} points")

        if collection_info.points_count == 0:
            print("[WARNING] Collection is empty. This might be expected if no documents have been ingested yet.")
        else:
            print(f"[SUCCESS] Collection contains {collection_info.points_count} documents")

            # Test a sample search
            sample_query = "artificial intelligence"
            results = retriever.search(sample_query, top_k=1)
            print(f"[SUCCESS] Sample search completed. Found {len(results)} results for query: '{sample_query}'")

            if results:
                first_result = results[0]
                print(f"   First result - Title: '{first_result.get('title', 'N/A')}'")
                print(f"   First result - Score: {first_result.get('score', 0):.3f}")
                print(f"   First result - Content preview: '{first_result.get('content', '')[:100]}...'")

        # Test generator initialization
        generator = Generator()
        print("[SUCCESS] Generator initialized successfully")

        # Test sample generation if we have results
        if results:
            answer = generator.generate_answer(sample_query, results)
            print(f"[SUCCESS] Sample answer generated: '{answer[:100]}...'")

        return True

    except Exception as e:
        print(f"[ERROR] Error during retrieval functionality test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting retrieval functionality test...")
    success = test_retrieval_functionality()
    if success:
        print("\n[SUCCESS] Retrieval functionality test successful!")
        print("The system is properly configured to connect to Qdrant and retrieve documents.")
    else:
        print("\n[ERROR] Retrieval functionality test failed!")
        sys.exit(1)