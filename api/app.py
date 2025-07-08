# --- RAG-ENABLED FastAPI APP ---
# This app loads a PDF, builds a vector DB, initializes the RAG pipeline, and exposes a /rag_answer endpoint.
# You can adapt the ingestion logic as needed for other document types or persistent storage.

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from typing import Optional
import os
import shutil

from aimakerspace.text_utils import PDFLoader, DocxLoader, TextFileLoader, MarkdownLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase
from aimakerspace.openai_utils.chatmodel import ChatOpenAI
from aimakerspace.rag_pipeline import RetrievalAugmentedQAPipeline

app = FastAPI()

# --- Add CORS middleware for cross-origin requests (frontend-backend integration) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin
    allow_credentials=True,  # Allows cookies to be included in requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers in requests
)

# --- RAG Pipeline Initialization (at startup) ---
print("Loading and ingesting PDF for RAG pipeline...")
pdf_path = "tests/tp_mayor_election.pdf"  # Change to your actual PDF path

# 1. Load and split PDF
documents = PDFLoader(pdf_path).load_documents()
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_texts(documents)

# 2. Build vector database (async)
vector_db = VectorDatabase()
vector_db = asyncio.run(vector_db.abuild_from_list(chunks))

# 3. Initialize LLM and RAG pipeline
llm = ChatOpenAI()
rag_pipeline = RetrievalAugmentedQAPipeline(
    vector_db_retriever=vector_db,
    llm=llm,
    response_style="detailed",
    include_scores=True
)

# --- Request/Response Models ---
class RAGQueryRequest(BaseModel):
    question: str
    k: int = 3

class RAGQueryResponse(BaseModel):
    answer: str
    context: Optional[list] = None
    

# --- Endpoint for user queries ---
@app.post("/rag_answer", response_model=RAGQueryResponse)
def rag_answer(request: RAGQueryRequest):
    try:
        result = rag_pipeline.run_pipeline(request.question, k=request.k)
        return RAGQueryResponse(
            answer=result["response"],
            context=result["context"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- New endpoint for chat+file upload ---
def get_loader_for_file(filename: str, path: str):
    ext = filename.lower().split('.')[-1]
    if ext == "pdf":
        return PDFLoader(path)
    elif ext == "docx":
        return DocxLoader(path)
    elif ext == "txt":
        return TextFileLoader(path)
    elif ext == "md":
        return MarkdownLoader(path)
    else:
        raise ValueError("Unsupported file type")

@app.post("/upload_and_ask")
async def upload_and_ask(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    # 1. If file is present, save and ingest it
    if file:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Uploaded file must have a filename.")
        ext = file.filename.split('.')[-1]
        temp_path = f"temp_upload.{ext}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        try:
            loader = get_loader_for_file(file.filename, temp_path)
            documents = loader.load_documents()
            splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_texts(documents)
            # Ingest into the global vector_db (async)
            await asyncio.get_event_loop().run_in_executor(
                None, lambda: asyncio.run(vector_db.abuild_from_list(chunks))
            )
        finally:
            os.remove(temp_path)

    # 2. Run the RAG pipeline with the user's question
    result = rag_pipeline.run_pipeline(message, k=3)
    return {"answer": result["response"], "context": result.get("context", [])}

# Define a health check endpoint to verify API status
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Entry point for running the application directly
if __name__ == "__main__":
    import uvicorn
    # Start the server on all network interfaces (0.0.0.0) on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

