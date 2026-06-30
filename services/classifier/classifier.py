from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

DOCUMENT_TYPES = ["contract", "invoice", "resume", "policy", "research paper", "report"]

def classify_document(text: str) -> dict:
    """Document ka type aur confidence return karta hai"""
    
    sample_text = text[:512]
    
    result = classifier(sample_text, DOCUMENT_TYPES)
    
    return {
        "document_type": result["labels"][0],
        "confidence": round(result["scores"][0], 2),
        "all_scores": {
            label: round(score, 2) 
            for label, score in zip(result["labels"], result["scores"])
        }
    }