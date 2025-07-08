import asyncio
import pytest
from aimakerspace.text_utils import PDFLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase
from aimakerspace.openai_utils.chatmodel import ChatOpenAI
from aimakerspace.rag_pipeline import RetrievalAugmentedQAPipeline

# Create a sample PDF file for testing
sample_pdf_path = "tests/tp_mayor_election.pdf"

@pytest.mark.parametrize("pdf_path,question", [
    ("tests/sample_test.pdf", "What is this document about?")
])
def test_rag_with_pdf(pdf_path, question):
    loader = PDFLoader(pdf_path)
    docs = loader.load_documents()
    assert len(docs) > 0, "No documents loaded from PDF!"
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # Use split_texts if split_documents does not exist
    chunks = splitter.split_texts(docs)
    assert len(chunks) > 0, "No chunks created from PDF!"
    print(f"Loaded {len(chunks)} chunks from {pdf_path}")

    # 3. Build vector database (async)
    vector_db = VectorDatabase()
    vector_db = asyncio.run(vector_db.abuild_from_list(chunks))

    # 4. Initialize LLM and RAG pipeline
    llm = ChatOpenAI()
    rag_pipeline = RetrievalAugmentedQAPipeline(
        vector_db_retriever=vector_db,
        llm=llm,
        response_style="detailed",
        include_scores=True
    )

    # 5. Ask a question
    result = rag_pipeline.run_pipeline(question, k=3)
    print("\n=== RAG Answer ===")
    print(result["response"])
    print("\n=== Context Used ===")
    for i, (context, score) in enumerate(result["context"], 1):
        print(f"[Source {i} | Score: {score:.3f}]:\n{context}\n")

if __name__ == "__main__":
    # Set your PDF path and a relevant question here 
    test_question = "請用50字介紹張家豪候選人?"
    test_rag_with_pdf(sample_pdf_path, test_question) 