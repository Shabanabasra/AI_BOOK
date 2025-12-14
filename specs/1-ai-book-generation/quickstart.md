# Quickstart Guide: AI_BOOK-generation

This guide provides a quick overview to get started with the AI_BOOK project components.

## 1. Project Structure

The project is organized into `backend/` and `frontend/` directories:

- `backend/`: Contains the FastAPI application for the RAG chatbot and embedding generation.
- `frontend/`: Contains the Docusaurus static site for the textbook, including content and UI components.

## 2. Local Development Setup

### Backend (FastAPI)

1.  **Navigate to the backend directory**:
    ```bash
    cd backend/
    ```
2.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt # (assuming a requirements.txt will be generated)
    ```
3.  **Set up environment variables**: (e.g., for Neon Postgres connection, Qdrant API key)
    Create a `.env` file based on `.env.example`.
4.  **Run the FastAPI application**:
    ```bash
    uvicorn src.main:app --reload
    ```
    The API will be available at `http://localhost:8000` (or configured port).

### Frontend (Docusaurus)

1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend/
    ```
2.  **Install Node.js dependencies**:
    ```bash
    npm install # or yarn install
    ```
3.  **Start the Docusaurus development server**:
    ```bash
    npm run start # or yarn start
    ```
    The Docusaurus site will be available at `http://localhost:3000`.

## 3. Key Development Artifacts

- **Specification**: `specs/1-ai-book-generation/spec.md`
- **Implementation Plan**: `specs/1-ai-book-generation/plan.md`
- **Research Findings**: `specs/1-ai-book-generation/research.md`
- **Data Model**: `specs/1-ai-book-generation/data-model.md`
- **API Contracts**: `specs/1-ai-book-generation/contracts/chatbot-api.yaml`

## 4. Deployment

Automated CI/CD is planned using GitHub Actions for deployment to GitHub Pages (frontend) and a serverless platform (backend). Refer to `.github/workflows/` for deployment configurations.
