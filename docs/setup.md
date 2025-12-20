# AI_BOOK RAG Chatbot Setup Guide

This guide will help you set up the Retrieval-Augmented Generation (RAG) chatbot for the AI_BOOK.

## Prerequisites

- Python 3.8 or higher
- Access to Cohere API (for embeddings and generation)
- Qdrant Cloud account (for vector storage)
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AI_BOOK
```

2. Install Python dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Install frontend dependencies (if needed):
```bash
cd frontend
npm install
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file and add your API keys and configuration:
```bash
# Edit the file with your preferred editor
nano .env  # or use any text editor
```

### Required Environment Variables

- `COHERE_API_KEY`: Your Cohere API key from [Cohere Dashboard](https://dashboard.cohere.ai/)
- `QDRANT_URL`: Your Qdrant Cloud URL from [Qdrant Cloud](https://cloud.qdrant.io/)
- `QDRANT_API_KEY`: Your Qdrant Cloud API key

### Optional Environment Variables

- `NEON_DB_URL`: Your Neon Postgres connection string (if using database features)
- `PORT`: Port for the backend server (default: 8000)
- `DEBUG`: Enable debug mode (default: false)
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (default: ai_book_docs)

## Document Ingestion

Before you can use the chatbot, you need to ingest the AI_BOOK documents into the vector database:

1. Make sure your environment variables are properly set
2. Run the ingestion script:
```bash
cd backend
python scripts/ingest_documents.py
```

### Ingestion Script Options

- `--docs-path`: Path to documentation directory (default: `../../docs`)
- `--chunk-size`: Maximum size of each text chunk (default: 1000)
- `--overlap-size`: Overlap between chunks (default: 200)
- `--collection-name`: Name of Qdrant collection (default: `ai_book_docs`)

Example:
```bash
python scripts/ingest_documents.py --docs-path ../../docs --chunk-size 1500 --overlap-size 300
```

## Running the Backend

1. Start the FastAPI backend server:
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Chat Endpoint
- **POST** `/api/v1/chat`
- Request body:
```json
{
  "question": "Your question about the AI book",
  "session_id": "optional session ID",
  "top_k": 5
}
```
- Response:
```json
{
  "answer": "The answer to your question",
  "references": ["List of references used"],
  "context_chunks": ["List of context chunks used"],
  "session_id": "Session ID"
}
```

### Ask from Selection Endpoint
- **POST** `/api/v1/ask-from-selection`
- Request body:
```json
{
  "selected_text": "The text that was selected",
  "question": "Your question about the selected text",
  "session_id": "optional session ID",
  "top_k": 3
}
```

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Testing

You can test the ingestion by running:
```bash
cd backend
python scripts/ingest_documents.py --docs-path ../../docs
```

Then test the API endpoints:
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is artificial intelligence?"}'
```

## Troubleshooting

### Common Issues

1. **API Key Errors**: Make sure your environment variables are properly set
2. **Connection Errors**: Verify your Qdrant URL and API key are correct
3. **Document Loading Errors**: Check that the docs path is correct and accessible

### Verifying Setup

1. Check if the backend is running: `curl http://localhost:8000/health`
2. Check if documents were ingested: `curl http://localhost:8000/api/v1/chat/health`

## Architecture

The RAG system consists of:

1. **Document Ingestion Pipeline**: Loads, chunks, and embeds documents
2. **Vector Storage**: Qdrant Cloud for semantic search
3. **Embedding Service**: Cohere for generating text embeddings
4. **Generation Service**: Cohere for answer generation
5. **API Layer**: FastAPI backend with chat endpoints
6. **Frontend**: React chatbot interface

## Security

- Never commit your `.env` file to version control
- Use environment variables for all sensitive information
- Consider using secrets management in production