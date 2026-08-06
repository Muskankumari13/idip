# Build Log

## Initial Goal
Build an AI-powered document intelligence platform that allows users to upload documents and ask questions using Retrieval-Augmented Generation (RAG).

---

## Initial Features

- Upload PDF
- Upload DOCX
- Document classification
- Semantic search
- Question Answering
- FastAPI backend

---

## Challenges

### Problem 1
Groq API key was not loading correctly.

Solution:
Moved the API key to a .env file and initialized the client only when needed.

---

### Problem 2
SentenceTransformer attempted to use GPU on Hugging Face Spaces.

Solution:
Forced the embedding model to run on CPU.

---

### Problem 3
Large PDF files produced extraction issues.

Solution:
Improved preprocessing and document chunking.

---

## Features Removed

Originally planned:
- OCR support
- Multi-document chat

Reason:
Focused on completing a reliable MVP first.

---

## Final Workflow

Upload Document
↓

Extract Text
↓

Generate Embeddings

↓

Store in FAISS

↓

Ask Question

↓

Retrieve Context

↓

Groq Llama 3.3

↓

Display Answer
