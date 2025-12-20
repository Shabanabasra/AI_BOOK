import re
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class DocumentChunk:
    """Represents a chunk of a document with metadata"""
    content: str
    title: str
    source: str
    chunk_index: int
    total_chunks: int
    metadata: Dict = None


class SemanticChunker:
    """
    Splits documents into semantic chunks based on document structure
    """

    def __init__(self, max_chunk_size: int = 1000, overlap_size: int = 200, min_chunk_size: int = 100):
        """
        Initialize the chunker with size parameters

        Args:
            max_chunk_size: Maximum number of characters per chunk
            overlap_size: Number of characters to overlap between chunks
            min_chunk_size: Minimum number of characters for a valid chunk
        """
        self.max_chunk_size = max_chunk_size
        self.overlap_size = overlap_size
        self.min_chunk_size = min_chunk_size

    def chunk_by_headings(self, text: str, title: str, source: str) -> List[DocumentChunk]:
        """
        Split text into chunks based on headings and paragraphs
        """
        # Split by markdown headings (h1, h2, h3, etc.)
        heading_pattern = r'\n(#{1,6}\s+.*?)(?=\n#{1,6}\s+|\n$)'
        parts = re.split(heading_pattern, '\n' + text)

        # The first element might be content before the first heading
        if parts and parts[0].strip() == '':
            parts = parts[1:]

        chunks = []
        chunk_index = 0

        i = 0
        while i < len(parts):
            if i % 2 == 0:  # Content part
                content = parts[i].strip()
                if content:
                    # If content is too large, split by paragraphs
                    sub_chunks = self._split_large_content(content, title, source, chunk_index)
                    chunks.extend(sub_chunks)
                    chunk_index += len(sub_chunks)
            else:  # Heading part
                heading = parts[i].strip()
                if i + 1 < len(parts):  # Next part is the content under this heading
                    content = parts[i + 1].strip()
                    full_content = f"{heading}\n{content}".strip()
                    sub_chunks = self._split_large_content(full_content, title, source, chunk_index)
                    chunks.extend(sub_chunks)
                    chunk_index += len(sub_chunks)
                    i += 1  # Skip the content part since we processed it
            i += 1

        return chunks

    def _split_large_content(self, content: str, title: str, source: str, start_index: int) -> List[DocumentChunk]:
        """
        Split large content into smaller chunks if needed
        """
        if len(content) <= self.max_chunk_size:
            return [DocumentChunk(
                content=content,
                title=title,
                source=source,
                chunk_index=start_index,
                total_chunks=1
            )]

        # Split by paragraphs first
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        chunk_index = start_index

        for paragraph in paragraphs:
            # If adding this paragraph would exceed the max size
            if len(current_chunk) + len(paragraph) > self.max_chunk_size:
                # If the current chunk is substantial, save it
                if len(current_chunk) >= self.min_chunk_size:
                    chunks.append(DocumentChunk(
                        content=current_chunk.strip(),
                        title=title,
                        source=source,
                        chunk_index=chunk_index,
                        total_chunks=0  # Will be updated at the end
                    ))
                    chunk_index += 1

                # Start a new chunk
                current_chunk = paragraph
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

        # Add the final chunk if it's substantial
        if current_chunk and len(current_chunk) >= self.min_chunk_size:
            chunks.append(DocumentChunk(
                content=current_chunk.strip(),
                title=title,
                source=source,
                chunk_index=chunk_index,
                total_chunks=0  # Will be updated at the end
            ))
            chunk_index += 1

        # Handle any remaining content that might still be too large
        final_chunks = []
        for chunk in chunks:
            if len(chunk.content) > self.max_chunk_size:
                # Split by sentences if the chunk is still too large
                sub_chunks = self._split_by_sentences(chunk.content, title, source, chunk_index)
                final_chunks.extend(sub_chunks)
                chunk_index += len(sub_chunks)
            else:
                final_chunks.append(chunk)

        # Update total_chunks for all chunks
        for i, chunk in enumerate(final_chunks):
            chunk.total_chunks = len(final_chunks)

        return final_chunks

    def _split_by_sentences(self, content: str, title: str, source: str, start_index: int) -> List[DocumentChunk]:
        """
        Split content by sentences when it's still too large
        """
        # Split by sentence endings
        sentences = re.split(r'(?<=[.!?])\s+', content)
        chunks = []
        current_chunk = ""
        chunk_index = start_index

        for sentence in sentences:
            # If adding this sentence would exceed the max size
            if len(current_chunk) + len(sentence) > self.max_chunk_size:
                # If the current chunk is substantial, save it
                if len(current_chunk) >= self.min_chunk_size:
                    chunks.append(DocumentChunk(
                        content=current_chunk.strip(),
                        title=title,
                        source=source,
                        chunk_index=chunk_index,
                        total_chunks=0  # Will be updated at the end
                    ))
                    chunk_index += 1

                # Start a new chunk with overlap if possible
                if len(sentence) > self.overlap_size:
                    # If sentence is longer than overlap, just add the sentence
                    current_chunk = sentence
                else:
                    # Add the sentence and try to include some overlap from the previous content
                    current_chunk = sentence
            else:
                # Add sentence to current chunk
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence

        # Add the final chunk if it's substantial
        if current_chunk and len(current_chunk) >= self.min_chunk_size:
            chunks.append(DocumentChunk(
                content=current_chunk.strip(),
                title=title,
                source=source,
                chunk_index=chunk_index,
                total_chunks=0  # Will be updated at the end
            ))

        # Update total_chunks for all chunks
        for i, chunk in enumerate(chunks):
            chunk.total_chunks = len(chunks)

        return chunks

    def chunk_text(self, text: str, title: str = "", source: str = "") -> List[DocumentChunk]:
        """
        Main method to chunk text using the best strategy
        """
        # First try to chunk by headings
        chunks = self.chunk_by_headings(text, title, source)

        # If chunks are still too large, apply additional splitting
        final_chunks = []
        for chunk in chunks:
            if len(chunk.content) > self.max_chunk_size:
                # Further split this chunk
                sub_chunks = self._split_large_content(chunk.content, chunk.title, chunk.source, len(final_chunks))
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk)

        return final_chunks


# For testing
if __name__ == "__main__":
    chunker = SemanticChunker(max_chunk_size=500, overlap_size=100)

    sample_text = """
# Introduction to AI

Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.

## History of AI

The field of AI research was born at a Dartmouth College workshop in 1956. Attendees Allen Newell, Herbert Simon, John McCarthy, Marvin Minsky and Arthur Samuel became the founders and leaders of AI research.

The workshop set the agenda for AI research for decades to come. Early achievements included solving geometry theorems and solving calculus problems.

## Machine Learning

Machine learning is a subset of AI that enables computers to learn and make decisions from data without being explicitly programmed. It's the science of getting computers to learn and act like humans do, and improve their learning over time in autonomous fashion, by feeding them data and information in the form of observations and real-world interactions.

There are several types of machine learning: supervised learning, unsupervised learning, and reinforcement learning. Each type has its own applications and use cases.

Supervised learning uses labeled datasets to train algorithms to classify data or predict outcomes. Unsupervised learning uses machine learning algorithms to analyze and cluster unlabeled datasets. Reinforcement learning trains machines through trial and error to take actions that maximize reward.

This is a very long paragraph that might need to be split into smaller chunks for better processing. It contains a lot of information that should be preserved in the semantic chunks. The content should remain coherent and meaningful even when split into smaller pieces. This ensures that the RAG system can properly retrieve and use the information for question answering.
"""

    chunks = chunker.chunk_text(sample_text, "Test Document", "test.md")

    print(f"Split into {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}/{chunk.total_chunks}:")
        print(f"Content preview: {chunk.content[:100]}...")
        print(f"Length: {len(chunk.content)} characters")