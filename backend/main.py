from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API routers
from api.chat import router as chat_router
from api.ask import router as ask_router

app = FastAPI(
    title="AI_BOOK RAG Chatbot API",
    description="FastAPI backend for AI_BOOK RAG system",
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

# Include API routes
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
app.include_router(ask_router, prefix="/api/v1", tags=["ask"])

@app.get("/")
def read_root():
    return {"message": "AI_BOOK RAG Chatbot API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))