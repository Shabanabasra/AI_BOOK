<!-- Sync Impact Report:
Version change: None (initial creation) -> v0.1.0
List of modified principles: None (initial creation)
Added sections: Project Vision and Goals, Project Constraints, Stakeholders, Brand Voice
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ updated (implicit alignment)
  - .specify/templates/spec-template.md: ✅ updated (implicit alignment)
  - .specify/templates/tasks-template.md: ✅ updated (implicit alignment)
  - .specify/templates/commands/*.md: ✅ updated (implicit alignment)
Follow-up TODOs: None
-->
# AI_BOOK Constitution

## Core Principles

### I. Simplicity
No complexity, clear steps. Principles must be easily understood and actionable, avoiding unnecessary abstraction or convoluted processes.

### II. Minimalism
Small content units, clean UI. Focus on essential elements and a streamlined user experience, reducing cognitive load and maximizing clarity.

### III. Accuracy
Robotics + AI content must remain technically correct. All presented information and exercises must adhere to established scientific and engineering principles.

### IV. Fast Build
Easy to generate, update, and redeploy. The development and deployment pipeline must be optimized for speed and efficiency, enabling rapid iteration.

### V. Free-tier Architecture
No heavy GPUs. Minimal embeddings (300–500 dims). File size < free-tier limits. Static site (client-side only). Fast API backend design using serverless-friendly, zero GPU dependency. Architectural choices must prioritize cost-effectiveness and accessibility, enabling deployment on free-tier services.

### VI. RAG Honesty
Chatbot answers only from book text. The integrated RAG chatbot must strictly derive its responses from the provided textbook content, without external knowledge or fabrication.

### VII. Beginner-First Writing
Clear, short lessons. Content must be tailored for beginners, using concise language, avoiding jargon where possible, and providing clear explanations.

### VIII. Hands-on-First
Mini exercises in each chapter. Learning is reinforced through practical, interactive exercises embedded directly within the content.

## Project Vision and Goals

**Vision**: Build a fast, clean, free-tier-friendly learning book that teaches Physical AI & Humanoid Robotics through simple explanations, visuals, and hands-on exercises — all deployable as a static Docusaurus site with an integrated RAG chatbot.

**Success Criteria**:
- Full AI_BOOK textbook auto-generated
- 6 short chapters produced
- Qdrant Neon RAG chatbot fully integrated
- Clean Docusaurus UI
- GitHub Pages deploy successful
- Select-Text → Ask AI works
- Claude/Gemini CLI fully connected

## Project Constraints

- No heavy GPUs
- Minimal embeddings (300–500 dims)
- File size < free-tier limits
- Static site (client-side only)
- Fast API backend design using serverless-friendly
- Zero GPU dependency

## Stakeholders

- **Primary**: Beginners → Intermediate learners
- **Secondary**: Robotics students, AI hobbyists
- **Providers**: Claude/Gemini AI, Docusaurus, Qdrant, Neon, FastAPI

## Brand Voice

- Clean
- Technical
- Calm
- Beginner-friendly
- Short sentences
- Hands-on tone

## Governance

All governance rules are defined by the principles outlined above. Any amendments to this constitution require documentation, approval, and a migration plan if changes are significant. All pull requests and code reviews must verify compliance with these principles. Complexity must always be justified.

**Version**: v0.1.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
