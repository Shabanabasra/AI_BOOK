import cohere
from typing import List, Union
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Embedder:
    """
    Embedding generator using Cohere API
    """

    def __init__(self, model_name: str = "embed-multilingual-v2.0", max_batch_size: int = 96):
        self.model_name = model_name
        self.max_batch_size = max_batch_size
        self.api_key = os.getenv("COHERE_API_KEY")

        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set")

        self.client = cohere.Client(self.api_key)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts
        """
        all_embeddings = []

        # Process in batches to respect API limits
        for i in range(0, len(texts), self.max_batch_size):
            batch = texts[i:i + self.max_batch_size]

            try:
                response = self.client.embed(
                    texts=batch,
                    model=self.model_name,
                    input_type="search_document"  # Using search_document for knowledge retrieval
                )

                batch_embeddings = [embedding for embedding in response.embeddings]
                all_embeddings.extend(batch_embeddings)

            except Exception as e:
                print(f"Error generating embeddings for batch: {str(e)}")
                # Return zero vectors as fallback for failed embeddings
                fallback_embeddings = [[0.0] * 384 for _ in range(len(batch))]
                all_embeddings.extend(fallback_embeddings)

        return all_embeddings

    def embed_single_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        embeddings = self.embed_texts([text])
        return embeddings[0] if embeddings else [0.0] * 384

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        """
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        # Normalize vectors
        v1_norm = v1 / np.linalg.norm(v1)
        v2_norm = v2 / np.linalg.norm(v2)

        # Calculate cosine similarity
        similarity = np.dot(v1_norm, v2_norm)

        # Ensure the result is in the range [-1, 1] to avoid numerical errors
        return float(np.clip(similarity, -1.0, 1.0))

    def get_embedding_dimension(self) -> int:
        """
        Return the dimension of the embeddings
        For Cohere's embed-multilingual-v2.0, it's 384
        """
        return 384

# For testing
if __name__ == "__main__":
    # This would require COHERE_API_KEY to be set in environment
    try:
        embedder = Embedder()
        sample_texts = [
            "Artificial Intelligence is a branch of computer science.",
            "Machine Learning is a subset of Artificial Intelligence.",
            "Natural Language Processing helps computers understand human language."
        ]

        embeddings = embedder.embed_texts(sample_texts)
        print(f"Generated {len(embeddings)} embeddings")
        print(f"Embedding dimension: {len(embeddings[0])}")

        # Test similarity
        similarity = embedder.cosine_similarity(embeddings[0], embeddings[1])
        print(f"Similarity between first two texts: {similarity}")

    except ValueError as e:
        print(f"Embedder initialization failed: {e}")
        print("Please set COHERE_API_KEY environment variable to test embeddings")