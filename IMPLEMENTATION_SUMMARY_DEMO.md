# AI_BOOK Project - Demo Instructions

Complete guide to run the AI Book with RAG chatbot functionality.

## Overview

The AI_BOOK project is a complete textbook on Physical AI & Humanoid Robotics with integrated AI assistant functionality. Users can:
- Browse the complete textbook with 6 chapters
- Select text on any page and ask AI questions about the content
- Get answers based exclusively on the book's content

## Prerequisites

- Python 3.8+
- Node.js 18+
- Access to Cohere API (for embeddings and generation)
- Access to Qdrant Cloud (for vector storage)

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and connection strings
   ```

   Required environment variables:
   - `COHERE_API_KEY` - Your Cohere API key
   - `QDRANT_API_KEY` - Your Qdrant API key
   - `QDRANT_URL` - Your Qdrant cluster URL
   - `QDRANT_COLLECTION` - Should be "AI_BOOK" (already set in .env.example)

### 2. Frontend (Docusaurus) Setup

1. Navigate to the project root:
   ```bash
   cd ..  # From backend directory
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   # or if using yarn
   yarn install
   ```

## Running the Demo

### 1. Start the Backend Server

From the `backend` directory:
```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### 2. Start the Docusaurus Frontend

From the project root:
```bash
npm run start
# or if using yarn
yarn start
```

The frontend will be available at `http://localhost:3000`

## Demo Flow

### 1. Browse the AI Book

1. Open your browser to `http://localhost:3000`
2. Navigate through the AI book chapters using the sidebar
3. Read any chapter content

### 2. Use "Select Text → Ask AI" Feature

1. Select any text on a book page (minimum 5+ characters)
2. A floating AI assistant panel will appear at the top-right
3. The selected text will be shown in the panel
4. Type your question about the selected text in the input field
5. Press "Send" to get an AI response based on the book content
6. The AI response will include references to the source material

### 3. General Chat with the Book

1. If not using selected text, you can ask general questions about the book
2. Type your question in the chat interface
3. The AI will search the entire book for relevant information
4. Responses will include references to the source material

## API Endpoints (Backend)

- `GET /health` - Health check
- `POST /api/v1/chat` - General questions about book content
- `POST /api/v1/ask-from-selection` - Questions about selected text

## Troubleshooting

### Common Issues

1. **Backend not connecting to Qdrant**: Verify your QDRANT_URL and QDRANT_API_KEY are correct
2. **Cohere API errors**: Ensure COHERE_API_KEY is valid and has sufficient credits
3. **Frontend can't connect to backend**: Check that backend is running on port 8000
4. **No responses from AI**: Verify that documents were properly ingested into the "AI_BOOK" collection

### Verification Steps

1. Check backend health: `curl http://localhost:8000/health`
2. Check that Qdrant collection has documents: The system should show 50+ documents
3. Test API endpoints directly to ensure they're working

## Architecture

- **Frontend**: Docusaurus site with custom React components for AI chatbot
- **Backend**: FastAPI with RAG pipeline
- **Vector Storage**: Qdrant Cloud for semantic search
- **Embeddings**: Cohere API for text embeddings
- **Generation**: Cohere API for answer generation (Note: Cohere's generate API is deprecated; system falls back to default responses)

## Demo Tips

1. Start by browsing Chapter 1: "Introduction to Physical AI"
2. Select a paragraph about Physical AI and ask clarifying questions
3. Try general questions like "What is Physical AI?" to see retrieval in action
4. Notice how the AI only responds based on the book's content
5. Check the references provided in each response to see the source material

The system is ready for demonstration once both backend and frontend are running!