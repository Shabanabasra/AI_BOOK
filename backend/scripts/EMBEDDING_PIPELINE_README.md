# AI Book Embedding Pipeline

This script processes all .md and .mdx files from the docs/ directory,
chunks them into ~500-token chunks with ~50-token overlap,
generates embeddings using Cohere API, and stores them in Qdrant.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional, for cloning the repository)

## Setup Instructions

### 1. Clone the Repository (if needed)
```bash
git clone <repository-url>
cd AI_BOOK
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

```bash
# Create virtual environment
python -m venv ai_book_env

# Activate virtual environment
# On Windows:
ai_book_env\Scripts\activate
# On macOS/Linux:
source ai_book_env/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r backend/requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION=ai_book_embeddings
```

You can copy the existing `.env.example` file and fill in your credentials:

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

## Running the Embedding Pipeline

### Basic Usage

```bash
python backend/scripts/ingest_ai_book.py
```

### Advanced Usage with Options

```bash
# Custom documentation path and collection name
python backend/scripts/ingest_ai_book.py \
    --docs-path "docs" \
    --collection-name "ai_book_embeddings" \
    --chunk-size 500 \
    --overlap-size 50
```

Available options:
- `--docs-path`: Path to documentation directory (default: "docs")
- `--collection-name`: Qdrant collection name (default: "ai_book_embeddings")
- `--chunk-size`: Maximum chunk size in characters (default: 500)
- `--overlap-size`: Overlap size in characters (default: 50)

## Pipeline Process

The pipeline performs the following steps:

1. **Load Documents**: Reads all `.md` and `.mdx` files from the specified directory
2. **Chunk Text**: Splits documents into ~500-token chunks with ~50-token overlap
3. **Generate Embeddings**: Creates vector embeddings using Cohere API
4. **Upload to Qdrant**: Stores vectors with metadata in Qdrant collection

## Metadata Attached to Each Chunk

- `source_file`: Original file path
- `week`: Week number if extracted from path (e.g., from "week1/", "week2/", etc.)
- `section_heading`: First heading from the content
- `chunk_index`: Index of the chunk within the original document

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your Cohere and Qdrant API keys are correctly set in the `.env` file
2. **File Not Found**: Verify that the docs directory exists and contains markdown files
3. **Qdrant Connection**: Check that your Qdrant URL and API key are correct
4. **Cohere Rate Limits**: If you see 429 errors, you've hit the Cohere API rate limit. For free tier users, consider processing documents in smaller batches or upgrading your Cohere plan.

### Environment Variables Not Loading

If environment variables are not loading, try:
```bash
# Verify the .env file exists in the correct location
ls -la .env

# Verify environment variables are set
python -c "import os; print(os.getenv('COHERE_API_KEY'))"
```

### Handling Large Document Sets

When processing large numbers of documents, you may encounter Cohere API rate limits. Consider these approaches:
- Process documents in smaller batches
- Add delays between API calls
- Upgrade to a paid Cohere plan for higher rate limits
- Use the script with smaller sections of your documentation at a time

## Verification

After running the pipeline, you can verify the embeddings were created by checking:
- The Qdrant collection contains the expected number of documents
- The console output shows successful processing of all steps