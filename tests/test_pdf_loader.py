from aimakerspace.text_utils import PDFLoader
import os

# Create a sample PDF file for testing
sample_pdf_path = "tests/sample_test.pdf"

# Only create the PDF if it doesn't exist
if not os.path.exists(sample_pdf_path):
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        c = canvas.Canvas(sample_pdf_path, pagesize=letter)
        c.drawString(100, 750, "Test PDF")
        c.drawString(100, 735, "This is a test PDF file.")
        c.save()
    except ImportError:
        print("reportlab is required to generate a sample PDF. Please install it with 'uv pip install reportlab'.")
        exit(1)

# Test the PDFLoader
loader = PDFLoader(sample_pdf_path)
loader.load()
docs = loader.documents

print("Loaded documents:")
for doc in docs:
    print(doc) 