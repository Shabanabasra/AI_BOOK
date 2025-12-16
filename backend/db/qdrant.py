from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class QdrantDB:
    """
    Qdrant vector database client for storing and retrieving embeddings
    """

    def __init__(self):
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

    def create_collection(self, collection_name: str, vector_size: int = 384, distance: str = "Cosine"):
        """
        Create a collection in Qdrant
        """
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance[distance.upper()]
                ),
            )
            print(f"Created collection '{collection_name}' with {vector_size}-dimensional vectors")
        except Exception as e:
            print(f"Collection '{collection_name}' already exists or error occurred: {str(e)}")

    def delete_collection(self, collection_name: str):
        """
        Delete a collection in Qdrant
        """
        try:
            self.client.delete_collection(collection_name=collection_name)
            print(f"Deleted collection '{collection_name}'")
        except Exception as e:
            print(f"Error deleting collection '{collection_name}': {str(e)}")

    def collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists
        """
        try:
            self.client.get_collection(collection_name=collection_name)
            return True
        except:
            return False

    def upsert_points(self, collection_name: str, ids: List[int], vectors: List[List[float]], payloads: List[Dict]):
        """
        Upsert points (vectors with metadata) to a collection
        """
        if len(ids) != len(vectors) or len(vectors) != len(payloads):
            raise ValueError("IDs, vectors, and payloads must have the same length")

        self.client.upsert(
            collection_name=collection_name,
            points=models.Batch(
                ids=ids,
                vectors=vectors,
                payloads=payloads
            )
        )

    def search(self, collection_name: str, query_vector: List[float], top_k: int = 5, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar vectors in the collection
        """
        # Convert filters to Qdrant format if provided
        qdrant_filters = None
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value)
                ))
            if conditions:
                qdrant_filters = models.Filter(must=conditions)

        search_results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=qdrant_filters,
            with_payload=True
        )

        # Format results
        results = []
        for hit in search_results:
            result = {
                'id': hit.id,
                'score': hit.score,
                'payload': hit.payload,
                'vector': hit.vector
            }
            results.append(result)

        return results

    def get_point(self, collection_name: str, point_id: int):
        """
        Get a specific point by ID
        """
        try:
            points = self.client.retrieve(
                collection_name=collection_name,
                ids=[point_id],
                with_payload=True,
                with_vectors=True
            )
            if points:
                point = points[0]
                return {
                    'id': point.id,
                    'payload': point.payload,
                    'vector': point.vector
                }
            return None
        except Exception as e:
            print(f"Error retrieving point {point_id}: {str(e)}")
            return None

    def delete_points(self, collection_name: str, point_ids: List[int]):
        """
        Delete specific points by IDs
        """
        try:
            self.client.delete(
                collection_name=collection_name,
                points_selector=models.PointIdsList(
                    points=point_ids
                )
            )
            print(f"Deleted {len(point_ids)} points from collection '{collection_name}'")
        except Exception as e:
            print(f"Error deleting points: {str(e)}")

    def get_collection_info(self, collection_name: str) -> Dict:
        """
        Get information about a collection
        """
        try:
            collection_info = self.client.get_collection(collection_name=collection_name)
            return {
                'name': collection_info.config.params.vectors.size,
                'vector_size': collection_info.config.params.vectors.size,
                'distance': collection_info.config.params.vectors.distance,
                'point_count': collection_info.points_count
            }
        except Exception as e:
            print(f"Error getting collection info: {str(e)}")
            return {}

    def get_all_collections(self) -> List[Dict]:
        """
        Get all collections in the Qdrant instance
        """
        try:
            collections = self.client.get_collections()
            return [
                {
                    'name': collection.name,
                    'vector_size': collection.config.params.vectors.size,
                    'distance': collection.config.params.vectors.distance,
                    'point_count': collection.points_count
                }
                for collection in collections.collections
            ]
        except Exception as e:
            print(f"Error getting collections: {str(e)}")
            return []

    def scroll_points(self, collection_name: str, limit: int = 10) -> List[Dict]:
        """
        Scroll through points in a collection
        """
        try:
            points, next_page = self.client.scroll(
                collection_name=collection_name,
                limit=limit,
                with_payload=True,
                with_vectors=True
            )

            results = []
            for point in points:
                result = {
                    'id': point.id,
                    'payload': point.payload,
                    'vector': point.vector
                }
                results.append(result)

            return results
        except Exception as e:
            print(f"Error scrolling points: {str(e)}")
            return []

# For testing
if __name__ == "__main__":
    try:
        qdrant_db = QdrantDB()

        # Test creating a collection
        qdrant_db.create_collection("test_collection", vector_size=384)

        # Check if collection exists
        exists = qdrant_db.collection_exists("test_collection")
        print(f"Collection exists: {exists}")

        # Get collection info
        info = qdrant_db.get_collection_info("test_collection")
        print(f"Collection info: {info}")

        # Clean up
        qdrant_db.delete_collection("test_collection")

    except ValueError as e:
        print(f"QdrantDB initialization failed: {e}")
        print("Please set QDRANT_URL and QDRANT_API_KEY environment variables to test Qdrant connection")