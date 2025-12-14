# Implementation Plan: AI_BOOK-generation

**Branch**: `1-ai-book-generation` | **Date**: 2025-12-06 | **Spec**: [specs/1-ai-book-generation/spec.md](specs/1-ai-book-generation/spec.md)
**Input**: Feature specification from `/specs/1-ai-book-generation/spec.md`

## Summary

The AI_BOOK-generation feature aims to deliver a Docusaurus-based textbook on Physical AI & Humanoid Robotics, featuring 6 concise, hands-on chapters. It integrates a RAG chatbot for context-aware Q&A, supports Urdu localization, and offers content versioning. The technical strategy emphasizes a static Docusaurus frontend, a FastAPI serverless backend for chatbot functionality, and Qdrant for vector embeddings, all designed within free-tier cloud constraints.

## Technical Context

**Language/Version**: Python 3.11+ (for FastAPI backend), Node.js 18+/JavaScript/TypeScript (for Docusaurus frontend)
**Primary Dependencies**: Docusaurus, FastAPI, Qdrant Client, Neon Postgres Client Libraries, Lightweight Embedding Model (e.g., from Hugging Face Transformers)
**Storage**: Neon Postgres (for Qdrant vector database storage)
**Testing**: `pytest` for FastAPI backend, Docusaurus built-in testing/visual regression for frontend (as applicable)
**Target Platform**: GitHub Pages (for Docusaurus static site), Serverless platform (e.g., Vercel, Render) for FastAPI backend
**Project Type**: Hybrid (static frontend + serverless backend)
**Performance Goals**: Fast page loads (under 1-2 seconds for Docusaurus), low latency chatbot responses (under 2 seconds p95), efficient content embedding generation (batch processing)
**Constraints**: No heavy GPUs, minimal embeddings (300-500 dims), file size < free-tier limits, static site (client-side only), FastAPI backend designed for serverless
**Scale/Scope**: 6 short chapters, integrated RAG chatbot, Urdu-optional toggle, versioning support

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Simplicity**: The plan emphasizes clear steps and minimal complexity (e.g., free-tier architecture, static site).
- [x] **II. Minimalism**: Focus on small content units and clean UI for Docusaurus, adhering to the principle.
- [x] **III. Accuracy**: The plan implicitly assumes technical accuracy in content generation and chatbot responses.
- [x] **IV. Fast Build**: Docusaurus and static site deployment support fast builds. CI/CD setup will further ensure this.
- [x] **V. Free-tier Architecture**: Explicitly constrained by "No heavy GPUs," "Minimal embeddings (300–500 dims)," "File size < free-tier limits," "Static site (client-side only)," and "Fast API backend design using serverless-friendly, zero GPU dependency."
- [x] **VI. RAG Honesty**: Chatbot integration explicitly states "Chatbot answers only from book text."
- [x] **VII. Beginner-First Writing**: The content generation implicitly targets beginner-first writing.
- [x] **VIII. Hands-on-First**: The plan includes "mini exercises in each chapter" for hands-on learning.

All constitution checks passed.

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-book-generation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/             # FastAPI endpoints (chatbot, embeddings generation)
│   ├── services/        # Business logic, Qdrant interaction, embedding models
│   └── models/          # Pydantic models for request/response, data structures
└── tests/
    ├── unit/            # Unit tests for services and models
    └── integration/     # Integration tests for API endpoints and external services

frontend/
├── src/
│   ├── components/      # React components for Docusaurus UI, chatbot widget, Urdu toggle
│   ├── pages/           # Docusaurus pages/layouts
│   ├── docs/AI_BOOK/    # Markdown files for chapters, lessons, quizzes
│   └── styles/          # Docusaurus theme overrides, custom styles
└── tests/
    ├── unit/            # Unit tests for React components
    └── e2e/             # End-to-end tests for Docusaurus navigation, chatbot interaction

.github/workflows/       # GitHub Actions for CI/CD
```

**Structure Decision**: The project will adopt a monorepo-like structure with distinct `backend/` and `frontend/` directories to clearly separate the Docusaurus static site and the FastAPI serverless application. This aligns with the hybrid project type and facilitates independent development and deployment of each component while maintaining a cohesive repository. The `docs/AI_BOOK/` within the frontend will house all textbook content.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - All constitution checks passed without violations.

## Phase 0: Outline & Research - Completed

- **Research performed**: See [specs/1-ai-book-generation/research.md](specs/1-ai-book-generation/research.md) for detailed research on Docusaurus setup, FastAPI serverless deployment, Qdrant embeddings generation, GitHub Pages CI/CD, and Urdu localization.

## Phase 1: Design & Contracts - Completed

- **Data Model**: See [specs/1-ai-book-generation/data-model.md](specs/1-ai-book-generation/data-model.md)
- **API Contracts**: See [specs/1-ai-book-generation/contracts/chatbot-api.yaml](specs/1-ai-book-generation/contracts/chatbot-api.yaml)
- **Quickstart Guide**: See [specs/1-ai-book-generation/quickstart.md](specs/1-ai-book-generation/quickstart.md)
- **Agent Context Update**: Not performed via script due to execution environment limitations. Key technologies added to context: Docusaurus, FastAPI, Qdrant, Neon Postgres.