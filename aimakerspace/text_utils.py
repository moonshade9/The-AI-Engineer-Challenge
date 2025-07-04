import os
from typing import List
from pypdf import PdfReader
from PIL import Image
import pytesseract
import docx


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith(".txt"):
            self.load_file()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .txt file."
            )

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            self.documents.append(f.read())

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".txt"):
                    with open(
                        os.path.join(root, file), "r", encoding=self.encoding
                    ) as f:
                        self.documents.append(f.read())

    def load_documents(self):
        self.load()
        return self.documents


class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


class PDFLoader:
    def __init__(self, path: str):
        self.documents = []
        self.path = path
        print(f"PDFLoader initialized with path: {self.path}")

    def load(self):
        print(f"Loading PDF from path: {self.path}")
        print(f"Path exists: {os.path.exists(self.path)}")
        print(f"Is file: {os.path.isfile(self.path)}")
        print(f"Is directory: {os.path.isdir(self.path)}")
        print(f"File permissions: {oct(os.stat(self.path).st_mode)[-3:]}")
        
        try:
            # Try to open the file first to verify access
            with open(self.path, 'rb') as test_file:
                pass
            
            # If we can open it, proceed with loading
            self.load_file()
            
        except IOError as e:
            raise ValueError(f"Cannot access file at '{self.path}': {str(e)}")
        except Exception as e:
            raise ValueError(f"Error processing file at '{self.path}': {str(e)}")

    def load_file(self):
        with open(self.path, 'rb') as file:
            # Create PDF reader object
            pdf_reader = PdfReader(file)
            
            # Extract text from each page
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            self.documents.append(text)

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        pdf_reader = PdfReader(f)
                        
                        # Extract text from each page
                        text = ""
                        for page in pdf_reader.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        
                        self.documents.append(text)

    def load_documents(self):
        self.load()
        return self.documents


class MarkdownLoader:
    """
    Loader for Markdown (.md) files. Treats markdown as plain text.
    Usage:
        loader = MarkdownLoader(path_to_md)
        loader.load()
        docs = loader.documents
    """
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith(".md"):
            self.load_file()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .md file."
            )

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            self.documents.append(f.read())

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".md"):
                    with open(
                        os.path.join(root, file), "r", encoding=self.encoding
                    ) as f:
                        self.documents.append(f.read())

    def load_documents(self):
        self.load()
        return self.documents


class ImageLoader:
    """
    Loader for image files (.png, .jpg, .jpeg) using OCR (pytesseract).
    Requires: pillow, pytesseract
    Usage:
        loader = ImageLoader(path_to_image_or_directory)
        loader.load()
        docs = loader.documents
    """
    def __init__(self, path: str):
        self.documents = []
        self.path = path

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self._is_image_file(self.path):
            self.load_file(self.path)
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a supported image file (.png, .jpg, .jpeg)."
            )

    def _is_image_file(self, filename):
        return filename.lower().endswith((".png", ".jpg", ".jpeg"))

    def load_file(self, file_path):
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            self.documents.append(text)
        except Exception as e:
            raise ValueError(f"Error processing image '{file_path}': {e}")

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if self._is_image_file(file):
                    file_path = os.path.join(root, file)
                    self.load_file(file_path)

    def load_documents(self):
        self.load()
        return self.documents


class DocxLoader:
    """
    Loader for Microsoft Word (.docx) files using python-docx.
    Requires: python-docx
    Usage:
        loader = DocxLoader(path_to_docx_or_directory)
        loader.load()
        docs = loader.documents
    """
    def __init__(self, path: str):
        self.documents = []
        self.path = path

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.endswith(".docx"):
            self.load_file(self.path)
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .docx file."
            )

    def load_file(self, file_path):
        try:
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            self.documents.append(text)
        except Exception as e:
            raise ValueError(f"Error processing docx file '{file_path}': {e}")

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".docx"):
                    file_path = os.path.join(root, file)
                    self.load_file(file_path)

    def load_documents(self):
        self.load()
        return self.documents


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
