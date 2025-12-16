import asyncpg
import os
from typing import Optional, List, Dict
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class NeonDB:
    """
    Neon Postgres database connection for storing metadata
    """

    def __init__(self):
        self.db_url = os.getenv("NEON_DB_URL")

        if not self.db_url:
            raise ValueError("NEON_DB_URL environment variable is not set")

        self.pool = None

    async def connect(self):
        """
        Create a connection pool
        """
        try:
            self.pool = await asyncpg.create_pool(
                dsn=self.db_url,
                min_size=1,
                max_size=10,
                command_timeout=60
            )

            # Initialize tables if they don't exist
            await self._initialize_tables()

            print("Connected to Neon Postgres database")
        except Exception as e:
            print(f"Error connecting to Neon database: {str(e)}")
            raise

    async def _initialize_tables(self):
        """
        Create required tables if they don't exist
        """
        async with self.pool.acquire() as conn:
            # Create table for storing document metadata
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    source TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    embedding_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create table for storing chat history
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    context_chunks JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create table for storing document chunks
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id SERIAL PRIMARY KEY,
                    document_id INTEGER REFERENCES documents(id),
                    chunk_text TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    embedding_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            print("Database tables initialized")

    async def close(self):
        """
        Close the connection pool
        """
        if self.pool:
            await self.pool.close()

    async def store_document_metadata(self, title: str, source: str, file_path: str, content_hash: str, embedding_id: Optional[str] = None) -> int:
        """
        Store document metadata in the database
        Returns the document ID
        """
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow("""
                INSERT INTO documents (title, source, file_path, content_hash, embedding_id)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id
            """, title, source, file_path, content_hash, embedding_id)

            return result['id']

    async def get_document_by_path(self, file_path: str) -> Optional[Dict]:
        """
        Get document metadata by file path
        """
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow("""
                SELECT * FROM documents WHERE file_path = $1
            """, file_path)

            return dict(result) if result else None

    async def store_chat_history(self, session_id: str, question: str, answer: str, context_chunks: List[Dict]):
        """
        Store chat history in the database
        """
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO chat_history (session_id, question, answer, context_chunks)
                VALUES ($1, $2, $3, $4)
            """, session_id, question, answer, json.dumps(context_chunks))

    async def get_chat_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """
        Get chat history for a session
        """
        async with self.pool.acquire() as conn:
            results = await conn.fetch("""
                SELECT * FROM chat_history
                WHERE session_id = $1
                ORDER BY created_at DESC
                LIMIT $2
            """, session_id, limit)

            return [dict(row) for row in results]

    async def store_document_chunk(self, document_id: int, chunk_text: str, chunk_index: int, embedding_id: Optional[str] = None):
        """
        Store a document chunk in the database
        """
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO document_chunks (document_id, chunk_text, chunk_index, embedding_id)
                VALUES ($1, $2, $3, $4)
            """, document_id, chunk_text, chunk_index, embedding_id)

    async def get_document_chunks(self, document_id: int) -> List[Dict]:
        """
        Get all chunks for a document
        """
        async with self.pool.acquire() as conn:
            results = await conn.fetch("""
                SELECT * FROM document_chunks
                WHERE document_id = $1
                ORDER BY chunk_index
            """, document_id)

            return [dict(row) for row in results]

    async def update_document_embedding_id(self, document_id: int, embedding_id: str):
        """
        Update the embedding ID for a document
        """
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE documents
                SET embedding_id = $2, updated_at = CURRENT_TIMESTAMP
                WHERE id = $1
            """, document_id, embedding_id)

    async def get_all_documents(self) -> List[Dict]:
        """
        Get all documents from the database
        """
        async with self.pool.acquire() as conn:
            results = await conn.fetch("""
                SELECT * FROM documents ORDER BY created_at DESC
            """)

            return [dict(row) for row in results]

# For testing
if __name__ == "__main__":
    import asyncio

    async def test_db():
        try:
            db = NeonDB()
            await db.connect()

            # Test storing a document
            doc_id = await db.store_document_metadata(
                title="Test Document",
                source="test_source",
                file_path="/test/path.md",
                content_hash="abc123"
            )

            print(f"Stored document with ID: {doc_id}")

            # Test retrieving the document
            doc = await db.get_document_by_path("/test/path.md")
            print(f"Retrieved document: {doc}")

            await db.close()

        except ValueError as e:
            print(f"Database initialization failed: {e}")
            print("Please set NEON_DB_URL environment variable to test database connection")

    # Run the test
    asyncio.run(test_db())