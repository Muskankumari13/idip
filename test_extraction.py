from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
pdf_path = "sample_docs/sample_file.pdf"

reader = PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")

# Step 1: Sare pages ka text ek saath jod do
full_text = ""
for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        full_text += page_text + "\n"

print(f"\nTotal characters extracted: {len(full_text)}")

# Step 2: Text ko chunks mein todo
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # har chunk ~500 characters ka
    chunk_overlap=50,    # 50 characters overlap agle chunk se
)

chunks = splitter.split_text(full_text)

print(f"Total chunks created: {len(chunks)}")
print(f"\n--- First chunk ---")
print(chunks[0])
print(f"\n--- Second chunk ---")
print(chunks[1])

from sentence_transformers import SentenceTransformer

print("\nLoading embedding model... (pehli baar thoda time lagega)")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sirf pehle 3 chunks ka embedding banate hain test ke liye
sample_chunks = chunks[:3]
embeddings = model.encode(sample_chunks)

print(f"\nEmbedding shape: {embeddings.shape}")
print(f"Pehle chunk ka embedding (pehle 5 numbers): {embeddings[0][:5]}")


import faiss
import numpy as np

print("\n--- FAISS Vector Store Test ---")

# Sab chunks ka embedding banao (sirf 3 nahi, sab)
all_embeddings = model.encode(chunks)
print(f"All embeddings shape: {all_embeddings.shape}")

# FAISS index banao
dimension = all_embeddings.shape[1]  # 384
index = faiss.IndexFlatL2(dimension)
index.add(np.array(all_embeddings).astype('float32'))

print(f"Total vectors in index: {index.ntotal}")

# Ab ek query test karte hain
query = "What is batch processing?"
query_embedding = model.encode([query]).astype('float32')

# Top 2 sabse similar chunks dhoondo
k = 2
distances, indices = index.search(query_embedding, k)

print(f"\nQuery: '{query}'")
print(f"Sabse relevant chunks:")
for i, idx in enumerate(indices[0]):
    print(f"\n  Match {i+1} (distance: {distances[0][i]:.4f}):")
    print(f"  {chunks[idx][:200]}")