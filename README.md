# IDIP — Intelligent Document Intelligence Platform

A production-grade RAG (Retrieval-Augmented Generation) system that ingests documents and answers questions using semantic search and LLMs.

## Features

- PDF and DOCX document ingestion
- Semantic chunking and embedding (Sentence Transformers)
- FAISS vector search with confidence gating
- LLM-powered answers via Groq (Llama 3.3)
- REST API with FastAPI

## Tech Stack

Python, FastAPI, LangChain, Sentence Transformers, FAISS, Groq LLM, Docker (coming soon)

## Setup

```bash
pip install -r requirements.txt
uvicorn services/ingestion/api:app --reload
```

## API Endpoints

- `POST /ingest` — Upload a PDF or DOCX file
- `POST /ask` — Ask a question about the uploaded document
