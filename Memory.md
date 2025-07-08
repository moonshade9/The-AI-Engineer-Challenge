# Memory: Planned/Desired Features for RAG App

## Features to Implement / Track

1. **Persistent Vector DB Storage**
   - Save and load vector database to/from disk or a persistent backend (e.g., FAISS, Chroma, Pinecone, etc.) so that embeddings are not lost on server restart.

2. **User/Session Isolation**
   - Ensure each user or session has their own isolated vector database and document context, for privacy and personalization.

3. **File Deduplication**
   - Detect and avoid ingesting duplicate files (by hash, filename, or content) to save storage and prevent redundant embeddings.

---

Add more features or notes as the project evolves.
