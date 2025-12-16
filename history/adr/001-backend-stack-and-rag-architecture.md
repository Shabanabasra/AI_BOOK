# ADR-001: Backend Stack and RAG Architecture for AI_BOOK Chatbot

## Status
Proposed → Accepted on 2025-12-16

## Context
In implementing the AI_BOOK chatbot backend, several architectural decisions were made to support a robust RAG (Retrieval-Augmented Generation) pipeline. These decisions impact maintainability, scalability, and integration with external services. The system needs to be free-tier compatible, avoid hallucinations, and provide fast responses for a textbook on Physical AI & Humanoid Robotics.

## Decision
1. **Cohere** was chosen as the model provider for embeddings and text generation due to its reliability, support for both functions in a single API, and multilingual capabilities which are important for the diverse AI community.

2. **Qdrant** was selected for vector storage and similarity search because of its performance, Python client integration, and free-tier availability for the project's needs.

3. **Neon Postgres** is used for metadata storage to keep document records and retrieval indices, supporting relational queries alongside vector search for comprehensive data management.

4. The **RAG pipeline** architecture was designed with four distinct modules (loader, embedder, retriever, generator) to maintain clean separation of concerns and enable independent testing and updates.

5. **Text selection queries** are handled by combining the selected text with the user's question for more context-aware retrieval, then passing relevant chunks to the generator for answer synthesis.

## Alternatives Considered
1. **Model Providers**: OpenAI embeddings/generation vs Cohere vs Hugging Face models
   - OpenAI: More expensive, potentially better known but higher costs for free-tier project
   - Hugging Face: Self-hosted models would require GPU resources, violating constraints
   - Cohere: Good balance of cost, performance, and API reliability

2. **Vector Databases**: Pinecone vs Weaviate vs Qdrant vs Chroma
   - Pinecone: Managed but more expensive
   - Weaviate: Good features but larger resource footprint
   - Qdrant: Good performance, Python integration, free-tier friendly
   - Chroma: Open source but requires more self-management

3. **Database for Metadata**: Neon Postgres vs Supabase vs SQLite
   - Supabase: Good but already using multiple services, Neon was simpler
   - SQLite: Simpler but less scalable for future growth
   - Neon: Serverless, integrates well with Python stack

## Consequences

### Pros:
- Centralized vector search and generation with Cohere simplifies integration
- Qdrant provides fast similarity search for RAG with efficient cosine similarity
- Neon Postgres ensures persistent metadata management with ACID properties
- Modular design allows future swapping of providers or DB backends
- Cohere's embed-multilingual-v2.0 model provides good performance with 384 dimensions
- Architecture supports both general questions and text selection queries

### Cons:
- Cohere dependency could be a single point of failure
- Tight coupling between retrieval and generation modules requires careful testing
- External service dependencies increase operational complexity
- Rate limits on API services could impact performance

### Future Considerations:
- Potential multi-model support (other embeddings/providers)
- Caching frequently retrieved documents for faster responses
- Local embedding models if API costs become prohibitive
- Integration with additional document formats beyond markdown

## References
- AI_BOOK specification for Physical AI & Humanoid Robotics textbook
- Free-tier compatibility requirements
- No hallucination constraint (responses must be grounded in book content)