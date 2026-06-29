from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile, os, uuid
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from main import extract_text_from_pdf, extract_text_from_docx, chunk_text, create_embeddings, build_faiss_index, search_index

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
document_store = {}

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    if file.filename.endswith(".docx"):
        text = extract_text_from_docx(tmp_path)
    else:
        text = extract_text_from_pdf(tmp_path)

    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    index = build_faiss_index(embeddings)

    doc_id = str(uuid.uuid4())
    document_store[doc_id] = {"chunks": chunks, "index": index}
    os.unlink(tmp_path)

    return JSONResponse({"doc_id": doc_id, "chunks_created": len(chunks)})


@app.post("/ask")
async def ask_question(doc_id: str, question: str):
    if doc_id not in document_store:
        return JSONResponse({"error": "doc_id not found"}, status_code=404)

    data = document_store[doc_id]
    results = search_index(data["index"], question, data["chunks"], k=3)

    if results[0]["distance"] > 1.8:
        return JSONResponse({
            "question": question,
            "answer": "I don't have enough information in the document to answer this.",
            "confidence": "low"
        })

    context = "\n\n".join([r["chunk"] for r in results])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Answer the question using only the provided context. Be concise."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )

    answer = response.choices[0].message.content

    return JSONResponse({
        "question": question,
        "answer": answer,
        "confidence": "high",
        "sources": [r["chunk"][:100] for r in results]
    })