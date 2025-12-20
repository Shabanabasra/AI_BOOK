import os
import glob
from typing import List, Dict
from pathlib import Path
import markdown
from bs4 import BeautifulSoup
import re
from .chunker import SemanticChunker, DocumentChunk

class MarkdownLoader:
    """
    Loads markdown files from Docusaurus documentation structure
    """

    def __init__(self, docs_path: str = "../../docs", chunk_size: int = 1000, overlap_size: int = 200):
        self.docs_path = docs_path
        self.chunker = SemanticChunker(max_chunk_size=chunk_size, overlap_size=overlap_size)

    def load_documents(self) -> List[Dict[str, str]]:
        """
        Load all markdown documents from the docs directory
        Returns a list of dictionaries with content and metadata
        """
        documents = []

        # Find all markdown files in the docs directory
        md_files = glob.glob(f"{self.docs_path}/**/*.md", recursive=True)
        mdx_files = glob.glob(f"{self.docs_path}/**/*.mdx", recursive=True)

        all_files = md_files + mdx_files

        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title from the markdown content
                title = self._extract_title(content)

                # Clean the content by removing frontmatter if present
                clean_content = self._remove_frontmatter(content)

                # Convert markdown to plain text for better embedding
                plain_text = self._markdown_to_text(clean_content)

                # Create document
                document = {
                    "content": plain_text,
                    "title": title,
                    "source": file_path,
                    "file_path": file_path
                }

                documents.append(document)

            except Exception as e:
                print(f"Error loading document {file_path}: {str(e)}")
                continue

        return documents

    def load_and_chunk_documents(self) -> List[Dict[str, str]]:
        """
        Load all markdown documents and chunk them into semantic pieces
        Returns a list of dictionaries with chunked content and metadata
        """
        documents = []

        # Find all markdown files in the docs directory
        md_files = glob.glob(f"{self.docs_path}/**/*.md", recursive=True)
        mdx_files = glob.glob(f"{self.docs_path}/**/*.mdx", recursive=True)

        all_files = md_files + mdx_files

        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title from the markdown content
                title = self._extract_title(content)

                # Clean the content by removing frontmatter if present
                clean_content = self._remove_frontmatter(content)

                # Convert markdown to plain text for better embedding
                plain_text = self._markdown_to_text(clean_content)

                # Chunk the document
                chunks = self.chunker.chunk_text(plain_text, title, file_path)

                # Convert chunks to the expected format
                for chunk in chunks:
                    document = {
                        "content": chunk.content,
                        "title": f"{title} - Chunk {chunk.chunk_index + 1}/{chunk.total_chunks}",
                        "source": file_path,
                        "file_path": file_path,
                        "chunk_index": chunk.chunk_index,
                        "total_chunks": chunk.total_chunks
                    }
                    documents.append(document)

            except Exception as e:
                print(f"Error processing document {file_path}: {str(e)}")
                continue

        return documents

    def _extract_title(self, content: str) -> str:
        """
        Extract title from markdown content (either from frontmatter or first heading)
        """
        # Try to extract from frontmatter
        import yaml
        try:
            if content.startswith('---'):
                end_frontmatter = content.find('---', 3)
                if end_frontmatter != -1:
                    frontmatter_str = content[3:end_frontmatter].strip()
                    frontmatter = yaml.safe_load(frontmatter_str)
                    if frontmatter and 'title' in frontmatter:
                        return frontmatter['title']
        except:
            pass

        # Try to extract from first heading
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('# '):
                return line.strip()[2:].strip()  # Remove '# ' prefix

        # Return filename as fallback
        return "Untitled Document"

    def _remove_frontmatter(self, content: str) -> str:
        """
        Remove YAML frontmatter from markdown content
        """
        if content.startswith('---'):
            end_frontmatter = content.find('---', 3)
            if end_frontmatter != -1:
                return content[end_frontmatter + 3:].strip()

        return content

    def _markdown_to_text(self, content: str) -> str:
        """
        Convert markdown to plain text
        """
        try:
            # Use markdown to convert to HTML first
            html = markdown.markdown(content)

            # Use BeautifulSoup to extract plain text
            soup = BeautifulSoup(html, 'html.parser')

            # Get text and clean it up
            text = soup.get_text()

            # Clean up whitespace
            text = re.sub(r'\n\s*\n', '\n\n', text)  # Replace multiple newlines with double newline
            text = re.sub(r'[ \t]+', ' ', text)  # Replace multiple spaces with single space

            return text.strip()
        except:
            # Fallback: just return the original content without frontmatter
            return content.strip()

    def load_document_by_path(self, file_path: str) -> Dict[str, str]:
        """
        Load a single document by its file path
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            title = self._extract_title(content)
            clean_content = self._remove_frontmatter(content)
            plain_text = self._markdown_to_text(clean_content)

            return {
                "content": plain_text,
                "title": title,
                "source": file_path,
                "file_path": file_path
            }
        except Exception as e:
            print(f"Error loading document {file_path}: {str(e)}")
            return None

# For testing
if __name__ == "__main__":
    loader = MarkdownLoader()
    docs = loader.load_documents()
    print(f"Loaded {len(docs)} documents")
    if docs:
        print(f"First document title: {docs[0]['title']}")
        print(f"First document length: {len(docs[0]['content'])} characters")