# AI_BOOK RAG Chatbot Backend

This is the FastAPI backend for the AI_BOOK RAG (Retrieval-Augmented Generation) chatbot system.

## Features

- **Document Loading**: Loads markdown files from Docusaurus documentation
- **Embedding Generation**: Uses Cohere API for semantic embeddings
- **Vector Search**: Qdrant-based similarity search
- **Answer Generation**: Cohere-powered response generation
- **Text Selection**: Special endpoint for questions about selected text

## Endpoints

- `POST /api/v1/chat` - General questions about the book content
- `POST /api/v1/ask-from-selection` - Questions about selected text
- `GET /health` - Health check endpoint

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and connection strings
   ```

3. Run the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Environment Variables

- `COHERE_API_KEY` - Your Cohere API key
- `QDRANT_API_KEY` - Your Qdrant API key
- `QDRANT_URL` - Your Qdrant cluster URL
- `NEON_DB_URL` - Your Neon Postgres connection string

## Architecture

- **RAG Pipeline**: Load → Embed → Retrieve → Generate
- **Vector Storage**: Qdrant for efficient similarity search
- **Metadata Storage**: Neon Postgres for document metadata
- **Language Model**: Cohere Command-R+ for answer generation