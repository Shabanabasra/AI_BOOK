from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI BOOK RAG API",
    description="Retrieval Augmented Generation API for AI BOOK content",
    version="1.0.0"
)

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # Lightweight model for embeddings

# Initialize embedding model
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    prefer_grpc=False
)

# Collection name for AI BOOK content
COLLECTION_NAME = "ai_book_content"

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    query: str
    results: List[dict]
    answer: str

class Document(BaseModel):
    content: str
    metadata: dict

class DocumentResponse(BaseModel):
    success: bool
    message: str

@app.on_event("startup")
async def startup_event():
    """Initialize the Qdrant collection on startup"""
    try:
        # Check if collection exists, if not create it
        collections = qdrant_client.get_collections()
        collection_exists = any(col.name == COLLECTION_NAME for col in collections.collections)

        if not collection_exists:
            # Create collection with vector configuration
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=embedding_model.get_sentence_embedding_dimension(),
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created collection: {COLLECTION_NAME}")

            # Add sample documents for initial content
            await initialize_sample_documents()
        else:
            logger.info(f"Collection {COLLECTION_NAME} already exists")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

async def initialize_sample_documents():
    """Add sample AI BOOK content to the vector database"""
    sample_documents = [
        {
            "content": "Physical AI represents an exciting frontier where artificial intelligence meets the physical world. Unlike traditional AI systems that operate purely in digital spaces, Physical AI involves AI systems that interact with, manipulate, and learn from the physical environment around us.",
            "metadata": {
                "chapter": "Introduction to Physical AI",
                "section": "Concept",
                "source": "AI_BOOK_01"
            }
        },
        {
            "content": "Humanoid robots are robots that look and move like humans! They have heads, arms, legs, and bodies similar to ours. These robots can walk, talk, wave, and do many things humans can do. Think of them as mechanical friends that can help us and interact with the world just like people do.",
            "metadata": {
                "chapter": "Basics of Humanoid Robotics",
                "section": "Concept",
                "source": "AI_BOOK_02"
            }
        },
        {
            "content": "ROS 2 (Robot Operating System 2) is like a robot toolkit that helps people build robots without starting from scratch. It's a collection of tools, instructions, and building blocks that let robot builders focus on making their robots smart instead of worrying about basic communication and control systems.",
            "metadata": {
                "chapter": "ROS 2 Fundamentals",
                "section": "Concept",
                "source": "AI_BOOK_03"
            }
        },
        {
            "content": "A Digital Twin is like having a virtual copy of a real robot or machine! It's a computer simulation that behaves exactly like the real thing. If you move the real robot, the virtual one moves the same way. If the real robot has a problem, you can test solutions on the virtual one first.",
            "metadata": {
                "chapter": "Digital Twin Simulation",
                "section": "Concept",
                "source": "AI_BOOK_04"
            }
        },
        {
            "content": "This capstone chapter brings together everything you've learned! It shows how to connect AI systems to real robots - taking smart algorithms and making them control physical machines. This is where virtual AI meets the real world!",
            "metadata": {
                "chapter": "Capstone: AI to Robot",
                "section": "Concept",
                "source": "AI_BOOK_06"
            }
        }
    ]

    # Prepare points for insertion
    points = []
    for i, doc in enumerate(sample_documents):
        # Create embedding for the content
        vector = embedding_model.encode(doc["content"]).tolist()

        points.append(
            models.PointStruct(
                id=i,
                vector=vector,
                payload={
                    "content": doc["content"],
                    "metadata": doc["metadata"]
                }
            )
        )

    # Upload points to Qdrant
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    logger.info(f"Added {len(sample_documents)} sample documents to the collection")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI BOOK RAG API is running", "status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the AI BOOK content using RAG"""
    try:
        # Generate embedding for the query
        query_vector = embedding_model.encode(request.query).tolist()

        # Search in Qdrant
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=request.top_k,
            with_payload=True
        )

        # Format results
        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "score": result.score,
                "content": result.payload.get("content", ""),
                "metadata": result.payload.get("metadata", {})
            })

        # Generate a simple answer based on the best match
        answer = ""
        if results:
            best_match = results[0]
            answer = f"Based on the AI BOOK content: {best_match['content'][:500]}..."  # Limit length
        else:
            answer = "I couldn't find relevant information in the AI BOOK for your query."

        return QueryResponse(
            query=request.query,
            results=results,
            answer=answer
        )
    except Exception as e:
        logger.error(f"Error querying documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error querying documents: {str(e)}")

@app.post("/documents", response_model=DocumentResponse)
async def add_document(document: Document):
    """Add a document to the vector database"""
    try:
        # Generate embedding for the document content
        vector = embedding_model.encode(document.content).tolist()

        # Generate a unique ID (in production, you might want to use UUID)
        import time
        doc_id = int(time.time() * 1000000)  # Use timestamp as ID

        # Create point in Qdrant
        point = models.PointStruct(
            id=doc_id,
            vector=vector,
            payload={
                "content": document.content,
                "metadata": document.metadata
            }
        )

        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[point]
        )

        logger.info(f"Added document with ID {doc_id}")
        return DocumentResponse(
            success=True,
            message=f"Document added successfully with ID {doc_id}"
        )
    except Exception as e:
        logger.error(f"Error adding document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding document: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "AI BOOK RAG API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)