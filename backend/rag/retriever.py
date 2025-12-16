from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from dotenv import load_dotenv
from .embedder import Embedder

# Load environment variables
load_dotenv()

class Retriever:
    """
    Qdrant-based retriever for semantic search
    """

    def __init__(self, collection_name: str = "ai_book_docs"):
        self.collection_name = collection_name
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not self.qdrant_url or not self.qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set")

        # Initialize Qdrant client
        self.client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            timeout=10
        )

        # Initialize embedder
        self.embedder = Embedder()

        # Create collection if it doesn't exist
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """
        Create the collection if it doesn't exist
        """
        try:
            # Check if collection exists
            self.client.get_collection(collection_name=self.collection_name)
        except:
            # Collection doesn't exist, create it
            vector_size = self.embedder.get_embedding_dimension()

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                ),
            )

            print(f"Created collection '{self.collection_name}' with {vector_size}-dimensional vectors")

    def add_documents(self, documents: List[Dict]):
        """
        Add documents to the Qdrant collection
        Each document should have 'content', 'title', 'source' keys
        """
        if not documents:
            return

        # Prepare payloads and vectors
        payloads = []
        vectors = []
        ids = []

        for idx, doc in enumerate(documents):
            # Generate embedding for the content
            embedding = self.embedder.embed_single_text(doc['content'])

            payload = {
                'content': doc['content'],
                'title': doc.get('title', ''),
                'source': doc.get('source', ''),
                'file_path': doc.get('file_path', '')
            }

            payloads.append(payload)
            vectors.append(embedding)
            ids.append(idx)  # Using index as ID

        # Upload to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(
                ids=ids,
                vectors=vectors,
                payloads=payloads
            )
        )

        print(f"Added {len(documents)} documents to collection '{self.collection_name}'")

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for relevant documents based on the query
        """
        # Generate embedding for the query
        query_embedding = self.embedder.embed_single_text(query)

        # Perform search in Qdrant
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        # Format results
        results = []
        for hit in search_results:
            result = {
                'id': hit.id,
                'score': hit.score,
                'content': hit.payload.get('content', ''),
                'title': hit.payload.get('title', ''),
                'source': hit.payload.get('source', ''),
                'file_path': hit.payload.get('file_path', '')
            }
            results.append(result)

        return results

    def search_with_selected_text(self, selected_text: str, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search using both selected text and query for better context
        """
        # Combine selected text and query for search
        combined_query = f"Context: {selected_text}\nQuestion: {query}"

        return self.search(combined_query, top_k)

    def get_all_document_count(self) -> int:
        """
        Get total number of documents in the collection
        """
        collection_info = self.client.get_collection(collection_name=self.collection_name)
        return collection_info.points_count

# For testing
if __name__ == "__main__":
    try:
        retriever = Retriever()

        # Test search (this would require documents to be added first)
        sample_query = "What is artificial intelligence?"
        results = retriever.search(sample_query, top_k=3)

        print(f"Found {len(results)} results for query: '{sample_query}'")
        if results:
            print(f"Top result score: {results[0]['score']}")

    except ValueError as e:
        print(f"Retriever initialization failed: {e}")
        print("Please set QDRANT_URL and QDRANT_API_KEY environment variables to test retrieval")