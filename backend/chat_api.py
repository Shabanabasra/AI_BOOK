#!/usr/bin/env python3
"""
CCR-compliant Retrieval Chatbot API
FastAPI backend for the AI_BOOK retrieval system
"""
import os
import logging
import sys
from typing import Dict, Any, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend directory to path to import rag modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the retrieval agent
from rag.retrieval_agent import RetrievalAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI_BOOK Retrieval Chatbot API",
    description="CCR-compliant retrieval chatbot system using Qdrant and Cohere",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    question: str

# Response model - matches the required CCR format
class RetrievedDocument(BaseModel):
    title: str
    source: str
    file_path: str
    score: float
    content: str

class ChatResponse(BaseModel):
    query: str
    retrieved_documents: List[RetrievedDocument]

# Global retrieval agent instance
retrieval_agent = None

@app.on_event("startup")
async def startup_event():
    """Initialize the retrieval agent on startup"""
    global retrieval_agent
    try:
        logger.info("Initializing retrieval agent...")
        retrieval_agent = RetrievalAgent()  # Will use QDRANT_COLLECTION from env, defaults to "AI_BOOK"
        logger.info("Retrieval agent initialized successfully")

        # Perform health check
        health = retrieval_agent.health_check()
        logger.info(f"Retrieval agent health: {health}")
    except Exception as e:
        logger.error(f"Failed to initialize retrieval agent: {str(e)}")
        raise

@app.get("/")
async def read_root():
    """Health check endpoint"""
    return {"message": "AI_BOOK Retrieval Chatbot API is running!"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        if retrieval_agent is None:
            raise HTTPException(status_code=500, detail="Retrieval agent not initialized")

        health = retrieval_agent.health_check()
        return health
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint that processes user questions and returns retrieved documents

    Args:
        request: ChatRequest with question field

    Returns:
        ChatResponse with query and retrieved documents
    """
    try:
        logger.info(f"Received chat request: {request.question}")

        if retrieval_agent is None:
            raise HTTPException(status_code=500, detail="Retrieval agent not initialized")

        # Use the retrieval agent to get results
        result = retrieval_agent.retrieve(request.question, top_k=5)

        # Handle the case where there's an error in retrieval
        if "error" in result:
            logger.error(f"Retrieval error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        # Convert the result to the required response format
        response = ChatResponse(
            query=result["query"],
            retrieved_documents=[
                RetrievedDocument(
                    title=doc["title"],
                    source=doc["source"],
                    file_path=doc["file_path"],
                    score=doc["score"],
                    content=doc["content"]
                )
                for doc in result["retrieved_documents"]
            ]
        )

        logger.info(f"Chat response generated successfully with {len(response.retrieved_documents)} documents")
        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "chat_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )