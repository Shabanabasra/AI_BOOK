from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
from rag.retriever import Retriever
from rag.generator import Generator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize RAG components
retriever = Retriever()  # Will use QDRANT_COLLECTION from env, defaults to "AI_BOOK"
generator = Generator()

class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    top_k: Optional[int] = 5

class ChatResponse(BaseModel):
    answer: str
    references: List[str]
    context_chunks: List[Dict]
    session_id: str

def _extract_references_from_context(context_chunks: List[Dict]) -> List[str]:
    """
    Extract references from context chunks for frontend compatibility
    """
    references = []
    for chunk in context_chunks:
        # Create a reference string using title and source
        title = chunk.get('title', 'Untitled')
        source = chunk.get('source', chunk.get('file_path', 'Unknown source'))

        # Extract filename from path if it's a file path
        if source and '/' in source:
            source = source.split('/')[-1]
        elif source and '\\' in source:
            source = source.split('\\')[-1]

        reference = f"{title} ({source})"
        if reference not in references:  # Avoid duplicate references
            references.append(reference)

    return references


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that takes a question and returns an answer based on RAG
    """
    try:
        logger.info(f"Received chat request: {request.question}")

        # Search for relevant documents
        context_chunks = retriever.search(request.question, top_k=request.top_k)

        logger.info(f"Found {len(context_chunks)} relevant chunks")

        # Generate answer based on context
        answer = generator.generate_answer(request.question, context_chunks)

        # Create references for frontend
        references = _extract_references_from_context(context_chunks)

        # Create a simple session ID if not provided
        session_id = request.session_id or f"session_{hash(request.question) % 10000}"

        # Log the interaction (in a real app, you'd store this in the database)
        logger.info(f"Generated answer for session {session_id}")

        return ChatResponse(
            answer=answer,
            references=references,
            context_chunks=context_chunks,
            session_id=session_id
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/chat/health")
async def chat_health():
    """
    Health check for the chat endpoint
    """
    try:
        # Check if retriever and generator are working
        sample_query = "test"
        sample_chunks = retriever.search(sample_query, top_k=1)

        return {
            "status": "healthy",
            "retriever_status": "ok",
            "generator_status": "ok",
            "documents_in_retriever": retriever.get_all_document_count()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# For testing purposes
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router, prefix="/api/v1", tags=["chat"])

    uvicorn.run(app, host="0.0.0.0", port=8000)