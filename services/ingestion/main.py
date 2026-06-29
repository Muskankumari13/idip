from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Model ek baar load hota hai, baar baar nahi (taake fast rahe)
print("Loading embedding model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded.")


def extract_text_from_pdf(pdf_path: str) -> str:
    """PDF se pura text nikalta hai"""
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"
    return full_text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Text ko chunks mein todta hai"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )
    return splitter.split_text(text)


def create_embeddings(chunks: list[str]) -> np.ndarray:
    """Chunks ka embedding banata hai"""
    return embedding_model.encode(chunks)


def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """Embeddings se FAISS index banata hai"""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    return index


def search_index(index: faiss.IndexFlatL2, query: str, chunks: list[str], k: int = 2):
    """Query ke liye sabse relevant chunks dhoondta hai"""
    query_embedding = embedding_model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, k)
    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "chunk": chunks[idx],
            "distance": float(distances[0][i])
        })
    return results


# Yeh sirf testing ke liye hai - jab hum is file ko directly run karein
if __name__ == "__main__":
    pdf_path = "../../sample_docs/sample_file.pdf"

    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters")

    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")

    embeddings = create_embeddings(chunks)
    print(f"Embeddings shape: {embeddings.shape}")

    index = build_faiss_index(embeddings)
    print(f"Index has {index.ntotal} vectors")

    results = search_index(index, "What is batch processing?", chunks)
    print("\nSearch results:")
    for r in results:
        print(f"Distance {r['distance']:.4f}: {r['chunk'][:100]}")
def extract_text_from_docx(docx_path: str) -> str:
    """DOCX se pura text nikalta hai"""
    from docx import Document as DocxDocument
    doc = DocxDocument(docx_path)
    full_text = ""
    for para in doc.paragraphs:
        if para.text:
            full_text += para.text + "\n"
    return full_text

def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    """Scanned PDF se OCR ke zariye text nikalta hai"""
    images = convert_from_path(pdf_path)
    full_text = ""
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text + "\n"
    return full_text