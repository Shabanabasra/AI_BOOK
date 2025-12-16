from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import logging
from backend.rag.retriever import Retriever
from backend.rag.generator import Generator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize RAG components
retriever = Retriever()
generator = Generator()

class AskFromSelectionRequest(BaseModel):
    selected_text: str
    question: str
    session_id: Optional[str] = None
    top_k: Optional[int] = 3

class AskFromSelectionResponse(BaseModel):
    answer: str
    context_chunks: List[Dict]
    session_id: str

@router.post("/ask-from-selection", response_model=AskFromSelectionResponse)
async def ask_from_selection_endpoint(request: AskFromSelectionRequest):
    """
    Endpoint for asking questions about selected text
    Takes selected text and a question, then returns an answer based on RAG
    """
    try:
        logger.info(f"Received ask-from-selection request for selected text: {request.selected_text[:100]}...")

        # Search for relevant documents using both selected text and question
        context_chunks = retriever.search_with_selected_text(
            request.selected_text,
            request.question,
            top_k=request.top_k
        )

        logger.info(f"Found {len(context_chunks)} relevant chunks for selected text query")

        # Generate answer based on selected text, question, and context
        answer = generator.generate_answer_with_selected_text(
            request.selected_text,
            request.question,
            context_chunks
        )

        # Create a simple session ID if not provided
        session_id = request.session_id or f"selection_session_{hash(request.selected_text + request.question) % 10000}"

        # Log the interaction (in a real app, you'd store this in the database)
        logger.info(f"Generated answer for selection session {session_id}")

        return AskFromSelectionResponse(
            answer=answer,
            context_chunks=context_chunks,
            session_id=session_id
        )

    except Exception as e:
        logger.error(f"Error in ask-from-selection endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/ask/health")
async def ask_health():
    """
    Health check for the ask-from-selection endpoint
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
    app.include_router(router, prefix="/api/v1", tags=["ask"])

    uvicorn.run(app, host="0.0.0.0", port=8000)