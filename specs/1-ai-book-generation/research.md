# Research for AI_BOOK-generation

## Decisions and Rationale

### 1. Docusaurus Setup Best Practices
**Decision**: Utilize Docusaurus official documentation and community resources for optimal setup of multi-chapter books, custom themes, and plugin integration. Prioritize standard Docusaurus features where possible to maintain free-tier compatibility and ease of maintenance.
**Rationale**: Adhering to official guidelines ensures stability, long-term support, and access to a robust ecosystem. This minimizes custom development, aligning with simplicity and fast build principles.
**Alternatives considered**: Other static site generators (e.g., Next.js, Gatsby) - rejected due to Docusaurus's native support for documentation, versioning, and MDX, which aligns better with the textbook format and reduces initial setup complexity.

### 2. FastAPI Serverless Deployment
**Decision**: Explore serverless deployment options like Vercel, Render, or similar platforms for the FastAPI backend, prioritizing those with generous free-tier limits and good integration with PostgreSQL (Neon) and Qdrant. Focus on containerization (Docker) for consistent deployment across platforms.
**Rationale**: Aligns directly with the "Free-tier Architecture" and "Fast Build" principles. Serverless platforms provide scalability without managing infrastructure, reducing operational overhead. Docker ensures consistent environments.
**Alternatives considered**: Traditional VPS or managed Kubernetes - rejected due to higher cost, increased management overhead, and potential for GPU dependency (if not carefully configured).

### 3. Qdrant Embeddings Generation
**Decision**: Implement embedding generation using a lightweight, open-source embedding model (e.g., from Hugging Face Transformers) that can run efficiently on CPU within free-tier limits. Use Python for text processing and embedding generation, storing vectors directly into Qdrant via its client library. Focus on efficient batch processing for embedding large numbers of documents.
**Rationale**: Directly addresses the "Minimal embeddings (300-500 dims)" and "Zero GPU dependency" constraints. Python offers a rich ecosystem for NLP tasks. Efficient batching ensures timely content updates.
**Alternatives considered**: Cloud-based embedding services (e.g., OpenAI, Cohere) - rejected due to potential cost implications and reliance on external APIs, which might not align with free-tier and self-contained principles.

### 4. GitHub Pages CI/CD for Docusaurus
**Decision**: Implement CI/CD using GitHub Actions to automate the build and deployment of the Docusaurus site to GitHub Pages. Configure workflows to trigger on pushes to the `main` or feature branches, ensuring that every content update is automatically reflected.
**Rationale**: Aligns with "Fast Build" and "GitHub Pages deploy successful" criteria. Automates the deployment process, reduces manual errors, and ensures continuous availability of the latest content.
**Alternatives considered**: Manual deployment - rejected due to inefficiency, proneness to errors, and lack of version control for deployments.

### 5. Urdu Localization in Docusaurus
**Decision**: Utilize Docusaurus's built-in internationalization (i18n) features for managing Urdu translations. Implement the Urdu-optional toggle using Docusaurus's language switching mechanisms. Focus on clear translation keys and a manageable translation workflow for content authors.
**Rationale**: Leverages native Docusaurus capabilities, reducing custom code and improving maintainability. This directly supports the "Urdu-optional toggle" requirement and "Minimalism" principle for UI.
**Alternatives considered**: Custom translation frameworks or external services - rejected to avoid introducing additional complexity and dependencies, aligning with "Simplicity" and "Free-tier Architecture" principles.
