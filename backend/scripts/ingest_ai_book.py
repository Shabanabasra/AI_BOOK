#!/usr/bin/env python3
"""
AI Book Embedding Pipeline

This script processes all .md and .mdx files from the docs/ directory,
chunks them into ~500-token chunks with ~50-token overlap,
generates embeddings using Cohere API, and stores them in Qdrant.
"""
import os
import sys
import re
import glob
from pathlib import Path
from typing import List, Dict, Tuple
import argparse
from dotenv import load_dotenv

# Add the backend directory to the path so we can import rag modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.embedder import Embedder
from rag.retriever import Retriever


def load_docs(docs_path: str = "docs") -> List[Dict]:
    """
    Load all .md and .mdx files from the docs directory.

    Args:
        docs_path: Path to the documentation directory

    Returns:
        List of dictionaries containing content and metadata
    """
    print(f"Loading documents from: {docs_path}")

    # Find all markdown files in the docs directory
    md_files = glob.glob(f"{docs_path}/**/*.md", recursive=True)
    mdx_files = glob.glob(f"{docs_path}/**/*.mdx", recursive=True)

    all_files = md_files + mdx_files
    print(f"Found {len(all_files)} markdown files")

    documents = []

    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract title from frontmatter or first heading
            title = extract_title(content)

            # Clean content by removing frontmatter
            clean_content = remove_frontmatter(content)

            # Extract week information from path
            week_match = re.search(r'week(\d+)', file_path.lower())
            week = week_match.group(1) if week_match else None

            # Extract section heading if available
            section_heading = extract_section_heading(clean_content)

            document = {
                'content': clean_content,
                'title': title,
                'source_file': file_path,
                'week': week,
                'section_heading': section_heading,
                'file_path': file_path
            }

            documents.append(document)
            print(f"  Loaded: {file_path}")

        except Exception as e:
            print(f"  Error loading {file_path}: {str(e)}")
            continue

    print(f"Successfully loaded {len(documents)} documents")
    return documents


def extract_title(content: str) -> str:
    """
    Extract title from markdown content (either from frontmatter or first heading)
    """
    # Try to extract from frontmatter
    try:
        if content.startswith('---'):
            end_frontmatter = content.find('---', 3)
            if end_frontmatter != -1:
                frontmatter_str = content[3:end_frontmatter].strip()
                import yaml
                frontmatter = yaml.safe_load(frontmatter_str)
                if frontmatter and 'title' in frontmatter:
                    return frontmatter['title']
    except:
        pass

    # Try to extract from first heading
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith('# '):
            return line.strip()[2:].strip()  # Remove '# ' prefix

    # Return filename as fallback
    return "Untitled Document"


def remove_frontmatter(content: str) -> str:
    """
    Remove YAML frontmatter from markdown content
    """
    if content.startswith('---'):
        end_frontmatter = content.find('---', 3)
        if end_frontmatter != -1:
            return content[end_frontmatter + 3:].strip()

    return content


def extract_section_heading(content: str) -> str:
    """
    Extract the first heading from content to use as section heading
    """
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith('# '):
            return line.strip()[2:].strip()  # Remove '# ' prefix
    return "No Heading"


def chunk_text(documents: List[Dict], max_chunk_size: int = 500, overlap_size: int = 50) -> List[Dict]:
    """
    Chunk text into ~500 token chunks with ~50 token overlap.

    Args:
        documents: List of documents with content and metadata
        max_chunk_size: Maximum size of each chunk (in characters)
        overlap_size: Overlap between chunks (in characters)

    Returns:
        List of chunked documents with metadata
    """
    print(f"Chunking documents (max_chunk_size={max_chunk_size}, overlap_size={overlap_size})")

    chunked_docs = []
    total_chunks = 0

    for doc_idx, doc in enumerate(documents):
        content = doc['content']
        title = doc['title']
        source_file = doc['source_file']
        week = doc['week']
        section_heading = doc['section_heading']

        # Simple character-based chunking (approximating token count)
        # In practice, you might want to use a proper tokenizer
        chunks = []
        start = 0

        while start < len(content):
            end = start + max_chunk_size

            # If we're near the end, just take the remaining content
            if end >= len(content):
                chunk_content = content[start:]
            else:
                # Try to break at sentence or paragraph boundary
                chunk_content = content[start:end]

                # Find a good breaking point
                break_point = -1
                for bp in ['\n\n', '. ', '! ', '? ', '; ']:
                    last_break = chunk_content.rfind(bp)
                    if last_break > len(chunk_content) // 2:  # Prefer breaking in the second half
                        break_point = last_break + len(bp)
                        break

                if break_point > 0:
                    end = start + break_point
                    chunk_content = content[start:end]

            # Create chunk with metadata
            chunk_doc = {
                'content': chunk_content,
                'title': f"{title} - Chunk {len(chunks) + 1}",
                'source_file': source_file,
                'week': week,
                'section_heading': section_heading,
                'chunk_index': len(chunks),
                'original_doc_index': doc_idx
            }

            chunks.append(chunk_doc)

            # Move start position with overlap
            if end >= len(content):
                break
            start = end - overlap_size

            # Prevent infinite loops if overlap is too large
            if start >= end:
                start = end

        chunked_docs.extend(chunks)
        total_chunks += len(chunks)

        print(f"  Document '{title}' chunked into {len(chunks)} parts")

    print(f"Total chunks created: {total_chunks}")
    return chunked_docs


def embed_chunks(chunked_docs: List[Dict]) -> List[Dict]:
    """
    Generate embeddings for chunked documents using Cohere API.

    Args:
        chunked_docs: List of chunked documents

    Returns:
        List of documents with embeddings
    """
    print("Generating embeddings using Cohere API...")

    # Initialize embedder
    embedder = Embedder(model_name="embed-english-v3.0")

    # Extract content for embedding
    texts = [doc['content'] for doc in chunked_docs]

    try:
        embeddings = embedder.embed_texts(texts)
        print(f"Generated {len(embeddings)} embeddings")
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        return []

    # Attach embeddings to documents
    for i, doc in enumerate(chunked_docs):
        doc['embedding'] = embeddings[i]

    return chunked_docs


def upload_to_qdrant(processed_docs: List[Dict], collection_name: str = "ai_book_embeddings"):
    """
    Upload processed documents with embeddings to Qdrant collection.

    Args:
        processed_docs: List of documents with embeddings and metadata
        collection_name: Name of the Qdrant collection
    """
    print(f"Uploading documents to Qdrant collection: {collection_name}")

    # Initialize retriever
    retriever = Retriever(collection_name=collection_name)

    # Prepare documents in the format expected by Qdrant
    qdrant_docs = []
    for doc in processed_docs:
        qdrant_doc = {
            'content': doc['content'],
            'title': doc['title'],
            'source': doc['source_file'],  # Using source_file as source for Qdrant
            'file_path': doc['source_file'],
            'week': doc.get('week', ''),
            'section_heading': doc.get('section_heading', ''),
            'chunk_index': doc.get('chunk_index', 0)
        }
        qdrant_docs.append(qdrant_doc)

    # Add documents to Qdrant
    try:
        retriever.add_documents(qdrant_docs)
        print(f"Successfully uploaded {len(qdrant_docs)} documents to Qdrant")
    except Exception as e:
        print(f"Error uploading to Qdrant: {str(e)}")
        return False

    # Verify the documents were stored
    try:
        doc_count = retriever.get_all_document_count()
        print(f"Verification: Qdrant collection '{collection_name}' now contains {doc_count} documents")
    except Exception as e:
        print(f"Error verifying document count: {str(e)}")

    return True


def main():
    """Main function to run the complete embedding pipeline."""
    # Load environment variables
    load_dotenv()

    parser = argparse.ArgumentParser(description="AI Book Embedding Pipeline")
    parser.add_argument(
        "--docs-path",
        type=str,
        default="docs",
        help="Path to the documentation directory (default: docs)"
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        default="ai_book_embeddings",
        help="Name of the Qdrant collection (default: ai_book_embeddings)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Maximum size of each chunk in characters (default: 500)"
    )
    parser.add_argument(
        "--overlap-size",
        type=int,
        default=50,
        help="Overlap between chunks in characters (default: 50)"
    )

    args = parser.parse_args()

    print("="*60)
    print("AI BOOK EMBEDDING PIPELINE")
    print("="*60)
    print(f"Documentation path: {args.docs_path}")
    print(f"Qdrant collection: {args.collection_name}")
    print(f"Chunk size: {args.chunk_size} characters")
    print(f"Overlap size: {args.overlap_size} characters")
    print("-"*60)

    # Step 1: Load documents
    print("\n1. LOADING DOCUMENTS")
    documents = load_docs(args.docs_path)

    if not documents:
        print("No documents found. Exiting.")
        return

    # Step 2: Chunk text
    print("\n2. CHUNKING TEXT")
    chunked_docs = chunk_text(documents, args.chunk_size, args.overlap_size)

    if not chunked_docs:
        print("No chunks created. Exiting.")
        return

    # Step 3: Generate embeddings
    print("\n3. GENERATING EMBEDDINGS")
    embedded_docs = embed_chunks(chunked_docs)

    if not embedded_docs:
        print("Failed to generate embeddings. Exiting.")
        return

    # Step 4: Upload to Qdrant
    print("\n4. UPLOADING TO QDRANT")
    success = upload_to_qdrant(embedded_docs, args.collection_name)

    if success:
        print("\n" + "="*60)
        print("EMBEDDING PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Total documents processed: {len(documents)}")
        print(f"Total chunks created: {len(embedded_docs)}")
        print(f"Uploaded to collection: {args.collection_name}")
    else:
        print("\n" + "="*60)
        print("EMBEDDING PIPELINE FAILED!")
        print("="*60)


if __name__ == "__main__":
    main()