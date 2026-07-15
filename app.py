import gradio as gr
import requests
import os
import sys
import threading
import time

# ---------------------------------------------------------------------------
# Start FastAPI in a background thread when API_URL is not externally set.
# This is required for HuggingFace Spaces (single-process environment).
# ---------------------------------------------------------------------------
if not os.getenv("API_URL"):
    import uvicorn
    def _start_api():
        uvicorn.run(
            "services.ingestion.api:app",
            host="0.0.0.0",
            port=8000,
            log_level="warning"
        )
    threading.Thread(target=_start_api, daemon=True).start()
    time.sleep(5)   # wait for the server to be ready

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

CSS = """
:root {
    --bg:      #0d1117;
    --surface: #161b22;
    --border:  #30363d;
    --text:    #e6edf3;
    --muted:   #8b949e;
    --accent:  #2f81f7;
    --radius:  6px;
    --mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}

body, .gradio-container {
    background: var(--bg) !important;
    font-family: var(--font) !important;
    color: var(--text) !important;
}
.gradio-container {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* topbar */
.topbar {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 0.85rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.75rem;
}
.topbar-product { font-size: 1rem; font-weight: 700; color: var(--text); }
.topbar-desc    { font-size: 0.72rem; color: var(--muted); margin-top: 2px; }
.chip {
    font-size: 0.68rem; font-weight: 500;
    padding: 2px 9px; border-radius: 999px;
    border: 1px solid var(--border); color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.05em;
}

/* main content area */
.content-wrap {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1.5rem;
}

/* make Gradio row fill */
.gradio-container > .main > .wrap,
.gradio-container .tabs-container { padding: 0 !important; }

/* panel headings */
.panel-head {
    font-size: 0.7rem; font-weight: 600;
    color: var(--muted); text-transform: uppercase;
    letter-spacing: 0.07em; padding-bottom: 0.7rem;
    border-bottom: 1px solid var(--border); margin-bottom: 0.85rem;
}

/* labels */
.gradio-container label > span,
.gradio-container .label-wrap > span {
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
}

/* inputs */
.gradio-container textarea,
.gradio-container input[type="text"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-size: 0.875rem !important;
}
.gradio-container textarea:focus,
.gradio-container input[type="text"]:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(47,129,247,.15) !important;
    outline: none !important;
}

/* result textbox */
.result-box textarea {
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    line-height: 1.65 !important;
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

/* answer area */
.answer-area {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.15rem !important;
    min-height: 200px;
    font-size: 0.875rem !important;
    line-height: 1.75 !important;
    color: var(--text) !important;
}
.answer-area p      { color: var(--text); margin: 0 0 0.6rem; }
.answer-area strong { color: var(--text); font-weight: 600; }
.answer-area hr     { border: none; border-top: 1px solid var(--border); margin: 0.85rem 0; }
.answer-area blockquote {
    margin: 0.35rem 0; padding: 0.4rem 0.85rem;
    border-left: 3px solid var(--border); color: var(--muted);
    font-size: 0.8rem; background: #1c2128;
    border-radius: 0 var(--radius) var(--radius) 0;
}

/* buttons */
.gradio-container button.lg {
    background: var(--accent) !important;
    border: none !important; border-radius: var(--radius) !important;
    color: #fff !important; font-size: 0.85rem !important;
    font-weight: 600 !important; width: 100% !important;
    transition: filter .15s !important;
}
.gradio-container button.lg:hover { filter: brightness(1.12) !important; }

footer { display: none !important; }

@media (max-width: 720px) {
    .topbar { flex-direction: column; align-items: flex-start; }
    .content-wrap { padding: 1rem; }
}
"""


def upload_and_ingest(file):
    if file is None:
        return "No file selected.", ""
    try:
        with open(file, "rb") as f:
            response = requests.post(
                f"{API_URL}/ingest",
                files={"file": (os.path.basename(file), f)},
                timeout=60
            )
    except requests.exceptions.ConnectionError:
        return "Error: cannot reach API server.", ""

    if response.status_code == 200:
        d = response.json()
        flags = "\n".join(f"    {fl}" for fl in d.get("risk_flags", []))
        info = (
            f"Status        : OK\n"
            f"{'─' * 38}\n"
            f"File          : {os.path.basename(file)}\n"
            f"Document type : {d.get('document_type','—').capitalize()} "
            f"({round(d.get('type_confidence',0)*100)}% confidence)\n"
            f"Chunks created: {d['chunks_created']}\n"
            f"Risk level    : {d.get('risk_level','—').upper()} "
            f"(score {d.get('risk_score',0)}/100)\n"
            f"Risk flags    :\n{flags}\n"
            f"{'─' * 38}\n"
            f"Document ID   : {d['doc_id']}"
        )
        return info, d["doc_id"]
    return f"Error {response.status_code}: {response.text}", ""


def ask_question(doc_id, question):
    if not doc_id:
        return "No document loaded. Upload a document first."
    if not question.strip():
        return "Question is empty."
    try:
        response = requests.post(
            f"{API_URL}/ask",
            params={"doc_id": doc_id, "question": question},
            timeout=60
        )
    except requests.exceptions.ConnectionError:
        return "Error: cannot reach API server."

    if response.status_code == 200:
        d = response.json()
        conf = d.get("confidence", "unknown").upper()
        answer = d["answer"]
        sources = d.get("sources", [])
        out = f"**Retrieval confidence: {conf}**\n\n{answer}"
        if sources:
            out += "\n\n---\n**Source excerpts**\n\n"
            out += "\n\n".join(f"> {s.strip()[:160]}..." for s in sources)
        return out
    return f"Error {response.status_code}: {response.text}"


with gr.Blocks(
    css=CSS,
    title="IDIP — Document Intelligence Platform",
    theme=gr.themes.Base()
) as demo:

    doc_id_state = gr.State("")

    gr.HTML("""
    <div class="topbar">
        <div>
            <div class="topbar-product">IDIP</div>
            <div class="topbar-desc">Intelligent Document Intelligence Platform</div>
        </div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;">
            <span class="chip">Llama 3.3 70B</span>
            <span class="chip">FAISS</span>
            <span class="chip">BART</span>
            <span class="chip">Sentence Transformers</span>
            <span class="chip">FastAPI</span>
        </div>
    </div>
    """)

    with gr.Row(elem_classes=["content-wrap"]):
        with gr.Column(scale=1, min_width=280):
            gr.HTML('<div class="panel-head">Document Upload</div>')
            file_input = gr.File(
                label="Select a PDF or DOCX file",
                file_types=[".pdf", ".docx"],
                type="filepath"
            )
            upload_btn = gr.Button("Process Document", variant="primary", size="lg")
            upload_output = gr.Textbox(
                label="Processing result",
                lines=11,
                interactive=False,
                elem_classes=["result-box"]
            )

        with gr.Column(scale=1, min_width=280):
            gr.HTML('<div class="panel-head">Query Interface</div>')
            question_input = gr.Textbox(
                placeholder="Ask a question about the document...",
                label="Question",
                lines=3
            )
            ask_btn = gr.Button("Submit Query", variant="primary", size="lg")
            answer_output = gr.Markdown(
                label="Response",
                elem_classes=["answer-area"]
            )

    upload_btn.click(upload_and_ingest, [file_input], [upload_output, doc_id_state])
    ask_btn.click(ask_question, [doc_id_state, question_input], [answer_output])
    question_input.submit(ask_question, [doc_id_state, question_input], [answer_output])

demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)))
