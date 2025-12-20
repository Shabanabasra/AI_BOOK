#!/usr/bin/env python3
"""
Document Ingestion Script for AI_BOOK RAG System

This script crawls all Docusaurus markdown pages from the AI_BOOK,
cleans and splits them into semantic chunks, generates embeddings
using Cohere API, and stores them with metadata in Qdrant Cloud.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.rag.loader import MarkdownLoader
from backend.rag.embedder import Embedder
from backend.rag.retriever import Retriever


def load_environment_variables():
    """Load and validate required environment variables"""
    required_vars = ['COHERE_API_KEY', 'QDRANT_URL', 'QDRANT_API_KEY']

    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease set these environment variables:")
        print("- COHERE_API_KEY: Your Cohere API key")
        print("- QDRANT_URL: Your Qdrant Cloud URL")
        print("- QDRANT_API_KEY: Your Qdrant Cloud API key")
        print("\nYou can also create a .env file with these variables.")
        sys.exit(1)


def ingest_documents(docs_path: str, chunk_size: int = 1000, overlap_size: int = 200, collection_name: str = "ai_book_docs"):
    """
    Main function to ingest documents into the RAG system

    Args:
        docs_path: Path to the documentation directory
        chunk_size: Maximum size of each text chunk
        overlap_size: Overlap between chunks
        collection_name: Name of the Qdrant collection to store documents
    """
    print(f"Starting document ingestion from: {docs_path}")
    print(f"Using chunk size: {chunk_size}, overlap: {overlap_size}")
    print(f"Storing in Qdrant collection: {collection_name}")

    # Initialize components
    print("\n1. Initializing components...")
    loader = MarkdownLoader(docs_path=docs_path, chunk_size=chunk_size, overlap_size=overlap_size)
    embedder = Embedder()
    retriever = Retriever(collection_name=collection_name)

    print("\n2. Loading and chunking documents...")
    documents = loader.load_and_chunk_documents()

    if not documents:
        print(f"No documents found in {docs_path}")
        return

    print(f"Loaded and chunked {len(documents)} document chunks")

    # Display some statistics
    print("\nDocument statistics:")
    print(f"- Total chunks: {len(documents)}")
    avg_length = sum(len(doc['content']) for doc in documents) / len(documents) if documents else 0
    print(f"- Average chunk length: {avg_length:.2f} characters")

    # Extract content for embedding
    print("\n3. Generating embeddings...")
    texts = [doc['content'] for doc in documents]

    try:
        embeddings = embedder.embed_texts(texts)
        print(f"Generated {len(embeddings)} embeddings")
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        return

    # Prepare documents in the format expected by the retriever
    formatted_docs = []
    for i, doc in enumerate(documents):
        formatted_doc = {
            'content': doc['content'],
            'title': doc['title'],
            'source': doc['source'],
            'file_path': doc['file_path'],
            'chunk_index': doc.get('chunk_index', 0),
            'total_chunks': doc.get('total_chunks', 1)
        }
        formatted_docs.append(formatted_doc)

    print("\n4. Storing documents in Qdrant...")
    try:
        retriever.add_documents(formatted_docs)
        print(f"Successfully stored {len(formatted_docs)} documents in Qdrant")
    except Exception as e:
        print(f"Error storing documents in Qdrant: {str(e)}")
        return

    # Verify the documents were stored
    try:
        doc_count = retriever.get_all_document_count()
        print(f"\n5. Verification: Qdrant collection now contains {doc_count} documents")
    except Exception as e:
        print(f"Error verifying document count: {str(e)}")

    print("\nDocument ingestion completed successfully!")


def main():
    parser = argparse.ArgumentParser(description="Ingest AI_BOOK documents into RAG system")
    parser.add_argument(
        "--docs-path",
        type=str,
        default="../../docs",
        help="Path to the documentation directory (default: ../../docs)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Maximum size of each text chunk (default: 1000)"
    )
    parser.add_argument(
        "--overlap-size",
        type=int,
        default=200,
        help="Overlap between chunks (default: 200)"
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        default="ai_book_docs",
        help="Name of the Qdrant collection (default: ai_book_docs)"
    )

    args = parser.parse_args()

    # Validate paths
    if not os.path.exists(args.docs_path):
        print(f"Error: Documentation path does not exist: {args.docs_path}")
        sys.exit(1)

    # Load environment variables
    load_environment_variables()

    # Run the ingestion process
    ingest_documents(
        docs_path=args.docs_path,
        chunk_size=args.chunk_size,
        overlap_size=args.overlap_size,
        collection_name=args.collection_name
    )


if __name__ == "__main__":
    main()