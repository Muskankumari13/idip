
````
---
title: IDIP
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: "5.0.0"
app_file: app.py
pinned: false
---

# IDIP — Intelligent Document Intelligence Platform

IDIP is a document intelligence agent that ingests PDF and DOCX files, retrieves relevant information using semantic search, and generates answers using an LLM.

It is designed for users who need to quickly understand and query information from documents without manually searching through every page.

## What the Agent Does

IDIP follows a document-question-answering workflow:

1. Accepts a PDF or DOCX document.
2. Extracts and processes the document content.
3. Splits the content into searchable chunks.
4. Creates semantic embeddings using Sentence Transformers.
5. Stores and searches embeddings using FAISS.
6. Retrieves relevant document context for a question.
7. Uses Groq with Llama 3.3 to generate an answer.
8. Applies confidence gating to reduce unreliable answers.

## Who It Is For

IDIP is useful for:

- Students working with research papers and reports
- Researchers reviewing long documents
- Professionals working with resumes, reports, and business documents
- Anyone who needs to ask questions about uploaded documents

## Key Features

- PDF and DOCX document ingestion
- Semantic chunking
- Sentence Transformer embeddings
- FAISS vector search
- Confidence gating
- LLM-powered answers
- Groq API with Llama 3.3
- FastAPI REST endpoints
- Gradio interface

## Tech Stack

- Python
- FastAPI
- Gradio
- Sentence Transformers
- FAISS
- Groq
- Llama 3.3
- LangChain

## Architecture

```text
                User
                  |
                  v
          Upload PDF / DOCX
                  |
                  v
          Document Ingestion
                  |
                  v
          Text Processing
                  |
                  v
        Semantic Chunking
                  |
                  v
      Sentence Transformer
           Embeddings
                  |
                  v
            FAISS Index
                  |
                  v
        Semantic Retrieval
                  |
                  v
        Confidence Gating
                  |
                  v
       Groq / Llama 3.3 LLM
                  |
                  v
             Answer
````

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Muskankumari13/idip.git
cd idip
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Groq API key

Create an environment variable containing your Groq API key.

```bash
export GROQ_API_KEY="your_api_key_here"
```

On Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

### 4. Start the FastAPI service

```bash
uvicorn services.ingestion.api:app --reload
```

## Usage

### Document ingestion

Upload a PDF or DOCX document through the application.

The system processes the document and creates searchable semantic representations.

### Ask a question

After ingestion, ask a natural-language question about the document.

Example:

```text
What is the main purpose of this document?
```

Another example:

```text
What are the key findings mentioned in the report?
```

The system retrieves relevant document context and uses the LLM to generate the answer.

## API Endpoints

### POST /ingest

Uploads and processes a PDF or DOCX document.

### POST /ask

Accepts a question and retrieves relevant information from the uploaded document.

## Evaluation

### V2 Evaluation Results

The V2 version was tested through end-to-end document processing and question answering.

Observed checks included:

* Document ingestion
* Document classification/processing
* Semantic chunk creation
* Retrieval of relevant content
* LLM-generated responses
* Confidence/risk assessment

> Add the exact V2 evaluation numbers/results from the FL-07 evaluation here. Do not use estimated or invented numbers.

## Limitations

* Answer quality depends on the quality and structure of the uploaded document.
* OCR-heavy or poorly formatted documents may produce weaker results.
* Retrieval can miss information when the relevant content is not represented clearly in the indexed chunks.
* LLM-generated answers can still contain errors.
* The system depends on the availability of the Groq API.
* Large or complex documents may require additional processing time.

## Guardrails

IDIP uses retrieval and confidence gating to reduce unsupported answers.

When the system does not have sufficiently relevant document context, the response should not be treated as reliable evidence.

The system is intended to answer questions based on the uploaded documents rather than replace human verification.

## Design Decision

A key design decision was to use semantic retrieval with FAISS instead of relying only on keyword matching.

This allows the system to retrieve information based on meaning and similarity, which is more useful when the user's question uses different wording from the document.

## Development / Iteration

The system was developed iteratively by testing document ingestion, retrieval, embeddings, LLM responses, and deployment behavior.

Issues encountered during development were addressed through implementation and configuration changes rather than treating the final version as a one-step build.

## Project Repository

GitHub:
[https://github.com/Muskankumari13/idip](https://github.com/Muskankumari13/idip)

```


Uske baad mujhe **screenshot bhejo**. Phir hum **3–5 minute FL-09 video** step-by-step banayenge.
```
