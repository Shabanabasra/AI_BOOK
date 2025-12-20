#!/usr/bin/env python3
"""
Data ingestion script for AI_BOOK project.
Crawls documentation pages from Vercel URL, extracts content, chunks it,
generates embeddings using Cohere, and stores vectors in Qdrant Cloud.
"""
import os
import sys
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Set
from dotenv import load_dotenv

# Add the backend directory to the path so we can import rag modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Import from existing RAG modules
from rag.chunker import SemanticChunker
from rag.embedder import Embedder
from rag.retriever import Retriever


class DocumentationCrawler:
    """
    Crawls documentation pages from a given URL
    """

    def __init__(self, base_url: str, max_pages: int = 100):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited_urls: Set[str] = set()
        self.to_visit: List[str] = [base_url]
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and belongs to the same domain"""
        parsed_base = urlparse(self.base_url)
        parsed_url = urlparse(url)
        return parsed_base.netloc == parsed_url.netloc

    def extract_links(self, html_content: str, current_url: str) -> List[str]:
        """Extract all links from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(current_url, href)

            # Only consider internal links that are HTML pages
            if self.is_valid_url(full_url) and (full_url.endswith('.html') or not full_url.split('/')[-1].endswith(('.',))):
                # Remove query parameters and fragments
                clean_url = full_url.split('#')[0].split('?')[0]
                if clean_url not in self.visited_urls and clean_url not in self.to_visit:
                    links.append(clean_url)

        return links

    def extract_page_content(self, html_content: str) -> Dict[str, str]:
        """Extract title and main content from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else "Untitled Page"

        # Try to find main content area (common selectors for documentation sites)
        main_content = None
        for selector in ['main', '.main-content', '.content', '.doc-content', '.markdown']:
            main_content = soup.select_one(selector)
            if main_content:
                break

        # If no main content found, use body
        if not main_content:
            main_content = soup.find('body')

        # Extract text content
        if main_content:
            content = main_content.get_text(separator='\n', strip=True)
        else:
            content = soup.get_text(separator='\n', strip=True)

        # Clean up content (remove extra whitespace)
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        content = '\n'.join(lines)

        return {
            'title': title,
            'content': content
        }

    def crawl(self) -> List[Dict[str, str]]:
        """Crawl all pages starting from base URL"""
        documents = []

        while self.to_visit and len(self.visited_urls) < self.max_pages:
            current_url = self.to_visit.pop(0)

            if current_url in self.visited_urls:
                continue

            print(f"Crawling: {current_url}")

            try:
                response = self.session.get(current_url, timeout=10)
                response.raise_for_status()

                # Only process HTML content
                content_type = response.headers.get('content-type', '')
                if 'text/html' not in content_type:
                    continue

                # Extract content from page
                page_data = self.extract_page_content(response.text)

                document = {
                    'title': page_data['title'],
                    'content': page_data['content'],
                    'source_url': current_url
                }

                documents.append(document)
                self.visited_urls.add(current_url)

                # Extract and queue new links
                new_links = self.extract_links(response.text, current_url)
                self.to_visit.extend(new_links)

                # Be respectful to the server
                time.sleep(1)

            except requests.RequestException as e:
                print(f"Error crawling {current_url}: {str(e)}")
                self.visited_urls.add(current_url)  # Don't retry failed URLs
                continue
            except Exception as e:
                print(f"Unexpected error crawling {current_url}: {str(e)}")
                self.visited_urls.add(current_url)
                continue

        print(f"Crawled {len(documents)} pages")
        return documents


def main():
    """Main ingestion function"""
    # Configuration
    base_url = "https://ai-book-blond-pi.vercel.app/docs/Introduction-Physical-AI"
    collection_name = os.getenv("QDRANT_COLLECTION", "AI_BOOK")

    print("Starting documentation ingestion process...")
    print(f"Base URL: {base_url}")
    print(f"Collection: {collection_name}")

    # Initialize components
    crawler = DocumentationCrawler(base_url)
    chunker = SemanticChunker(max_chunk_size=1000, overlap_size=200)
    embedder = Embedder(model_name=os.getenv("EMBEDDING_MODEL", "embed-english-v3.0"))

    # Step 1: Crawl documentation pages
    print("\n1. Crawling documentation pages...")
    raw_documents = crawler.crawl()

    if not raw_documents:
        print("No documents were crawled. Exiting.")
        return

    print(f"Successfully crawled {len(raw_documents)} documents")

    # Step 2: Process and chunk documents
    print("\n2. Processing and chunking documents...")
    processed_documents = []

    for doc in raw_documents:
        # Chunk the document content
        chunks = chunker.chunk_text(doc['content'], doc['title'], doc['source_url'])

        for chunk in chunks:
            processed_doc = {
                'content': chunk.content,
                'title': f"{doc['title']} - Chunk {chunk.chunk_index + 1}/{chunk.total_chunks}",
                'source': doc['source_url'],
                'source_url': doc['source_url']
            }
            processed_documents.append(processed_doc)

    print(f"Processed into {len(processed_documents)} chunks")

    # Step 3: Add documents to Qdrant
    print("\n3. Adding documents to Qdrant Cloud...")
    try:
        retriever = Retriever(collection_name=collection_name)
        retriever.add_documents(processed_documents)

        # Step 4: Verify ingestion
        print("\n4. Verifying ingestion...")
        doc_count = retriever.get_all_document_count()
        print(f"Total documents in collection: {doc_count}")

        # Test a sample search
        if doc_count > 0:
            sample_search = retriever.search("Artificial Intelligence", top_k=1)
            if sample_search:
                print(f"Sample search result: '{sample_search[0]['title']}' (score: {sample_search[0]['score']:.3f})")
    except Exception as e:
        print(f"Error connecting to Qdrant: {str(e)}")
        print("Please verify your QDRANT_URL and QDRANT_API_KEY in the .env file")
        print("Documents processed but not stored in vector database.")

    print("\nIngestion process completed successfully!")


if __name__ == "__main__":
    main()