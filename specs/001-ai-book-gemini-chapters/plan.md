# AI_BOOK Project Generation Plan

## 1. Project Setup & Structure
- Create top-level directories: `frontend/`, `backend/`, `docs/`, `history/`, `specs/`, `.specify/`.
- Create `frontend/src/docs/AI_BOOK/` for Docusaurus chapters.
- Create `backend/` subdirectories: `chatbot/`, `config/`, `model/`, `service/`.
- Generate a comprehensive `.gitignore` file for both frontend and backend.
- Create a main `README.md` for the entire project.
- Configure `.env` file with provided environment variables.

## 2. Frontend (Docusaurus) Implementation
- Create `docusaurus.config.js` in `frontend/` with basic configuration.
- Generate `frontend/src/docs/AI_BOOK/_category_.json` for sidebar.
- For each chapter specified:
    - Create `frontend/src/docs/AI_BOOK/<chapter-file>.mdx`.
    - Populate each `.mdx` file with:
        - Frontmatter including title.
        - Placeholder sections for "Introduction", "Hands-on Exercise", "Code Snippets", "Diagrams", "Mini Glossary", "Quiz", and "Urdu Toggle" (as comments/placeholders).
        - Ensure content is beginner-friendly and hands-on focused.

## 3. Backend (FastAPI) Implementation
- Create `backend/requirements.txt` with necessary dependencies (FastAPI, uvicorn, qdrant-client, supabase, psycopg2-binary, etc.).
- Implement `backend/main.py` as the main FastAPI application:
    - Initialize FastAPI app.
    - Include API routes: `/signup`, `/login`, `/embed`, `/query`, `/health`.
    - Integrate with Supabase and Neon.
    - Configure CORS.
- Implement `backend/signup.py` for user registration logic.
- **Chatbot Module (`backend/chatbot/`)**:
    - `__init__.py`
    - `agent.py`: Implement the core chatbot logic, likely using LangChain or similar.
    - `qdrant_retriever.py`: Implement Qdrant integration for RAG embeddings.
- **Config Module (`backend/config/`)**:
    - `connection.py`: Database connection setup for Neon/Supabase.
    - `schema.sql`: SQL schema definition.
- **Model Module (`backend/model/`)**:
    - `schemas.py`: Pydantic models for request/response bodies, e.g., for users, chat messages.
    - `user.py`: SQLAlchemy/ORM models for user data.
- **Service Module (`backend/service/`)**:
    - `user_service.py`: Business logic for user-related operations (signup, login).
- Ensure seamless integration between Qdrant, Supabase, and Neon.

## 4. Documentation & Setup
- Create `docs/setup/neon_setup.md`, `docs/setup/supabase_setup.md`, `docs/setup/qdrant_setup.md`, `docs/setup/backend_setup.md` with detailed setup instructions.

## 5. Deployment & Finalization
- Add a note in `README.md` or a dedicated deployment guide for `npx neonctl@latest init`.
- Ensure Python's default behavior for `__pycache__` and `.pyc` files is maintained. If not, add explicit instructions.
- Add GitHub Pages configuration for frontend deployment.
- Prepare Vercel deployment configuration for the backend (e.g., `vercel.json`).
- Verify that the project structure and content will allow for copy-paste deployment.
- Manual verification step: check if all chapters render correctly in the browser.
- Manual verification step: ensure project is ready for GitHub push and Vercel deployment.

## Critical Files to be Modified/Created:
- `.gitignore`
- `README.md`
- `.env`
- `frontend/package.json` (for Docusaurus setup)
- `frontend/docusaurus.config.js`
- `frontend/src/docs/AI_BOOK/_category_.json`
- `frontend/src/docs/AI_BOOK/*.mdx` (all chapter files)
- `backend/requirements.txt`
- `backend/main.py`
- `backend/signup.py`
- `backend/chatbot/__init__.py`
- `backend/chatbot/agent.py`
- `backend/chatbot/qdrant_retriever.py`
- `backend/config/connection.py`
- `backend/config/schema.sql`
- `backend/model/schemas.py`
- `backend/model/user.py`
- `backend/service/user_service.py`
- `docs/setup/neon_setup.md`
- `docs/setup/supabase_setup.md`
- `docs/setup/qdrant_setup.md`
- `docs/setup/backend_setup.md`
- `vercel.json` (for backend deployment, if needed)
