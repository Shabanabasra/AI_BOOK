# Task Checklist: AI_BOOK-generation

**Feature Branch**: `1-ai-book-generation`
**Created**: 2025-12-06
**Plan**: [specs/1-ai-book-generation/plan.md](specs/1-ai-book-generation/plan.md)
**Status**: To Do

This document outlines the actionable tasks for the AI_BOOK-generation project, organized by development phase.

## Phase 1 — Docusaurus Setup

- [ ] Initialize Docusaurus project in the `frontend/` directory.
- [ ] Install necessary Docusaurus theme plugins.
- [ ] Create the Docusaurus sidebar configuration to auto-generate navigation.
- [ ] Configure `docusaurus.config.js` for navbar, footer, and site settings.
- [ ] Set up GitHub Pages deployment configuration within the Docusaurus project.
- [ ] Connect MCP server (SSH credentials, test connectivity - if applicable for Docusaurus plugins).

## Phase 2 — Chapter Writing Tasks

- [ ] Create 6 MDX chapter files under `frontend/src/docs/AI_BOOK/`.
- [ ] Add examples, quizzes, and hands-on exercises to each chapter/lesson.
- [ ] Integrate diagrams (ASCII/SVG) into relevant sections of the chapters.
- [ ] Implement the Urdu toggle option using Docusaurus i18n features.
- [ ] Add a mini glossary for key terms within each chapter/lesson.
- [ ] Sync chapter resources with MCP server if storing media/data remotely (e.g., images).

## Phase 3 — Chatbot Integration

- [ ] Initialize FastAPI backend project in the `backend/` directory.
- [ ] Set up Neon Postgres database and configure connection in FastAPI.
- [ ] Set up Qdrant vector database for embeddings, configure client in FastAPI.
- [ ] Generate and insert embeddings from book files (MDX content) into Qdrant.
- [ ] Implement API endpoints in FastAPI for RAG (Retrieval Augmented Generation) retrieval.
- [ ] Connect the front-end RAG widget within Docusaurus to the FastAPI backend.
- [ ] Enable the "Select-text → Ask AI" plugin functionality in Docusaurus.
- [ ] Ensure the chatbot can query the MCP server for additional resources (if needed for extended RAG capabilities).

## Phase 4 — Deployment Tasks

- [ ] Set up the GitHub repository for the AI_BOOK project (if not already done).
- [ ] Push initial `backend/` and `frontend/` code to the GitHub repository.
- [ ] Configure CI/CD pipelines using GitHub Actions for both frontend and backend.
- [ ] Build the static Docusaurus site using the CI/CD pipeline.
- [ ] Deploy the built Docusaurus site to GitHub Pages via CI/CD.
- [ ] **Smoke Test**:
    - [ ] Verify the deployed static site loads correctly in a browser.
    - [ ] Test chatbot responses for accuracy and relevance based on book content.
    - [ ] Confirm MCP server connectivity from both frontend (if applicable) and backend (if applicable).
