"""
CCR-compliant retrieval agent for the AI_BOOK project.
Implements the retrieval pipeline with Cohere embeddings and Qdrant vector search.
"""
import os
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import required modules
try:
    import cohere
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
except ImportError as e:
    logger.error(f"Missing required dependencies: {e}")
    raise ImportError("Please install required dependencies: pip install cohere qdrant-client python-dotenv")


@dataclass
class RetrievedDocument:
    """Represents a single retrieved document with metadata."""
    content: str
    title: str
    source: str
    file_path: str
    score: float


class RetrievalAgent:
    """
    CCR-compliant retrieval agent for the AI_BOOK project.

    Accepts user queries, generates embeddings using Cohere,
    performs semantic search over the AI_BOOK collection in Qdrant,
    and returns structured JSON results with preserved metadata.
    """

    def __init__(self, collection_name: str = None):
        """
        Initialize the retrieval agent with required configuration.

        Args:
            collection_name: Name of the Qdrant collection to search (defaults to AI_BOOK from env)
        """
        # Get environment variables
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.collection_name = collection_name or os.getenv("QDRANT_COLLECTION", "AI_BOOK")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")
        self.embedding_dim = int(os.getenv("EMBEDDING_DIM", "1024"))  # Default to 1024 for Cohere

        if not all([self.qdrant_url, self.qdrant_api_key, self.cohere_api_key]):
            missing_vars = []
            if not self.qdrant_url:
                missing_vars.append("QDRANT_URL")
            if not self.qdrant_api_key:
                missing_vars.append("QDRANT_API_KEY")
            if not self.cohere_api_key:
                missing_vars.append("COHERE_API_KEY")

            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        # Initialize Cohere client
        self.cohere_client = cohere.Client(self.cohere_api_key)

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            timeout=30
        )

        logger.info(f"RetrievalAgent initialized with collection: {self.collection_name}")
        logger.info(f"Using embedding model: {self.embedding_model}")
        logger.info(f"Embedding dimension: {self.embedding_dim}")

    def _generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for the user query using Cohere.

        Args:
            query: User query text

        Returns:
            Embedding vector as a list of floats
        """
        logger.info(f"Generating embedding for query: {query[:50]}...")

        try:
            response = self.cohere_client.embed(
                texts=[query],
                model=self.embedding_model,
                input_type="search_query"  # Using search_query for better retrieval performance
            )

            embedding = response.embeddings[0]
            logger.info(f"Generated {len(embedding)}-dimensional embedding")

            return embedding

        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            raise

    def _search_vectors(self, query_embedding: List[float], top_k: int = 5) -> List[RetrievedDocument]:
        """
        Perform semantic search in Qdrant using the query embedding.

        Args:
            query_embedding: Query embedding vector
            top_k: Number of top results to retrieve

        Returns:
            List of retrieved documents with metadata
        """
        logger.info(f"Performing semantic search in collection: {self.collection_name}, top_k: {top_k}")

        try:
            # Check if collection exists
            try:
                collection_info = self.qdrant_client.get_collection(collection_name=self.collection_name)
                logger.info(f"Collection {self.collection_name} found with {collection_info.points_count} vectors")

                if collection_info.points_count == 0:
                    logger.warning(f"Collection {self.collection_name} is empty")
                    return []
            except Exception as e:
                logger.error(f"Collection {self.collection_name} does not exist: {str(e)}")
                return []

            # Perform search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True,
                score_threshold=0.0  # Return all results above minimum similarity
            )

            logger.info(f"Found {len(search_results)} results from semantic search")

            # Convert search results to RetrievedDocument objects
            results = []
            for hit in search_results:
                payload = hit.payload or {}

                result = RetrievedDocument(
                    content=payload.get('content', ''),
                    title=payload.get('title', ''),
                    source=payload.get('source', ''),
                    file_path=payload.get('file_path', ''),
                    score=hit.score
                )
                results.append(result)

            return results

        except Exception as e:
            logger.error(f"Error performing semantic search: {str(e)}")
            raise

    def retrieve(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Main retrieval method that accepts a user query and returns structured JSON results.

        Args:
            query: User query text
            top_k: Number of top results to retrieve (default: 5)

        Returns:
            Dictionary with query and retrieved documents with metadata in JSON format
        """
        logger.info(f"Starting retrieval for query: {query}")

        try:
            # Check if collection has any points
            collection_info = self.qdrant_client.get_collection(collection_name=self.collection_name)
            if collection_info.points_count == 0:
                logger.error("No vectors found in AI_BOOK collection.")
                return {
                    "query": query,
                    "retrieved_documents": [],
                    "error": "No vectors found in AI_BOOK collection."
                }

            # Generate embedding for the query
            query_embedding = self._generate_query_embedding(query)

            # Perform semantic search
            search_results = self._search_vectors(query_embedding, top_k)

            # Format results as specified in requirements
            retrieved_documents = []
            for result in search_results:
                formatted_result = {
                    "content": result.content,
                    "title": result.title,
                    "source": result.source,
                    "file_path": result.file_path,
                    "score": result.score
                }
                retrieved_documents.append(formatted_result)

            response = {
                "query": query,
                "retrieved_documents": retrieved_documents
            }

            logger.info(f"Retrieval completed successfully, returned {len(retrieved_documents)} documents")
            return response

        except Exception as e:
            logger.error(f"Error in retrieval process: {str(e)}")
            return {
                "query": query,
                "retrieved_documents": [],
                "error": f"Retrieval failed: {str(e)}"
            }

    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the retrieval system.

        Returns:
            Health status information
        """
        try:
            # Check if Qdrant collection exists and has documents
            collection_info = self.qdrant_client.get_collection(collection_name=self.collection_name)

            status = {
                "status": "healthy",
                "collection_name": self.collection_name,
                "document_count": collection_info.points_count,
                "qdrant_connected": True,
                "cohere_connected": True,
                "embedding_model": self.embedding_model,
                "embedding_dimension": self.embedding_dim
            }

            return status

        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "qdrant_connected": False
            }


# Example usage and testing
if __name__ == "__main__":
    try:
        # Initialize the retrieval agent
        agent = RetrievalAgent()

        # Perform a sample retrieval
        sample_query = "What is artificial intelligence?"
        result = agent.retrieve(sample_query, top_k=3)

        print("Retrieval Result:")
        print(f"Query: {result['query']}")
        print(f"Number of retrieved documents: {len(result.get('retrieved_documents', []))}")

        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            for i, res in enumerate(result['retrieved_documents']):
                print(f"\nResult {i+1}:")
                print(f"  Title: {res['title']}")
                print(f"  Score: {res['score']:.3f}")
                print(f"  Source: {res['source']}")
                print(f"  Content preview: {res['content'][:100]}...")

        # Health check
        health = agent.health_check()
        print(f"\nHealth Check: {health}")

    except Exception as e:
        print(f"Error running test: {str(e)}")