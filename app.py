import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"

def upload_and_ingest(file):
    if file is None:
        return "Koi file select nahi ki", ""
    
    with open(file, "rb") as f:
        files = {"file": (file.split("\\")[-1], f)}
        response = requests.post(f"{API_URL}/ingest", files=files)
    
    if response.status_code == 200:
        data = response.json()
        doc_id = data["doc_id"]
        info = f"✅ Document uploaded!\n\nDoc ID: {doc_id}\nChunks: {data['chunks_created']}\nType: {data.get('document_type', 'N/A')} (confidence: {data.get('type_confidence', 'N/A')})"
        return info, doc_id
    else:
        return f"❌ Error: {response.text}", ""


def ask_question(doc_id, question):
    if not doc_id:
        return "Pehle koi document upload karo"
    if not question:
        return "Koi sawaal likho"
    
    response = requests.post(f"{API_URL}/ask", params={"doc_id": doc_id, "question": question})
    
    if response.status_code == 200:
        data = response.json()
        answer = data["answer"]
        confidence = data.get("confidence", "unknown")
        return f"**Answer:** {answer}\n\n**Confidence:** {confidence}"
    else:
        return f"❌ Error: {response.text}"


with gr.Blocks(title="IDIP - Document Intelligence Platform") as demo:
    gr.Markdown("# 📄 IDIP — Intelligent Document Intelligence Platform")
    gr.Markdown("Upload a document, then ask questions about it.")
    
    doc_id_state = gr.State("")
    
    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload PDF or DOCX", type="filepath")
            upload_btn = gr.Button("Upload & Process", variant="primary")
            upload_output = gr.Textbox(label="Upload Status", lines=5)
        
        with gr.Column():
            question_input = gr.Textbox(label="Ask a question about the document")
            ask_btn = gr.Button("Ask", variant="primary")
            answer_output = gr.Markdown(label="Answer")
    
    upload_btn.click(
        fn=upload_and_ingest,
        inputs=[file_input],
        outputs=[upload_output, doc_id_state]
    )
    
    ask_btn.click(
        fn=ask_question,
        inputs=[doc_id_state, question_input],
        outputs=[answer_output]
    )

demo.launch()