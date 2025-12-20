# AI_BOOK Documentation Ingestion Pipeline

This script implements the complete data ingestion pipeline for the AI_BOOK project as specified in Spec-1.

## Overview

The ingestion pipeline:
1. Crawls documentation pages from the Vercel deployment
2. Extracts clean readable text from each page
3. Splits content into semantic chunks
4. Generates embeddings using Cohere's `embed-english-v3.0` model
5. Stores vectors with metadata in Qdrant Cloud

## Features

- **Crawling**: Automatically discovers and crawls documentation pages starting from the main documentation URL
- **Text Extraction**: Extracts clean, readable content from HTML pages while preserving semantic structure
- **Chunking**: Uses semantic chunking to split documents into meaningful segments
- **Embeddings**: Generates 1024-dimensional embeddings using Cohere's latest model
- **Storage**: Stores vectors in Qdrant Cloud with rich metadata

## Metadata Stored

Each vector in Qdrant contains the following metadata:
- `content`: The text chunk content
- `title`: The title of the document/chunk
- `source`: The source URL of the document
- `source_url`: The original URL where the content was found

## Configuration

The script reads configuration from the `.env` file:
- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: Your Qdrant Cloud instance URL
- `QDRANT_API_KEY`: Your Qdrant Cloud API key
- `QDRANT_COLLECTION`: The collection name to use (defaults to "AI_BOOK")
- `EMBEDDING_MODEL`: The embedding model to use (defaults to "embed-english-v3.0")

## Usage

```bash
cd backend
python scripts/ingest_docs.py
```

## Output

The script provides detailed logging of the ingestion process:
- URLs discovered and crawled
- Number of documents processed
- Number of chunks created
- Status of vector storage in Qdrant

## Error Handling

- Graceful handling of network errors during crawling
- Fallback embedding generation in case of API failures
- Detailed error messages for configuration issues

## Architecture

The pipeline reuses existing RAG components:
- `rag.chunker.SemanticChunker` for content chunking
- `rag.embedder.Embedder` for generating embeddings
- `rag.retriever.Retriever` for Qdrant storage

## Spec-1 Compliance

✓ Crawls documentation pages from Vercel URL
✓ Extracts clean readable text from each page
✓ Splits content into semantic chunks
✓ Generates embeddings using Cohere
✓ Stores vectors with metadata in Qdrant Cloud
✓ Uses source_url, page title, and text chunk as metadata
✓ Uses fixed collection name related to AI_BOOK
✓ Fully reusable for the RAG chatbot
✓ Reads credentials from .env
✓ Logs progress clearly