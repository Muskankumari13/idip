import re

def calculate_risk_score(text: str, document_type: str) -> dict:
    """
    Document mein anomalies check karta hai aur risk score deta hai.
    Score 0-100: jitna zyada, utna zyada risk/unusual.
    """
    flags = []
    score = 0

    word_count = len(text.split())

    # Check 1: Document bahut chhota hai (incomplete ho sakta hai)
    if word_count < 50:
        flags.append("Document is unusually short — may be incomplete")
        score += 30

    # Check 2: Amount mismatches (invoice/contract ke liye)
    amounts = re.findall(r'\$\s?[\d,]+\.?\d*|\bRs\.?\s?[\d,]+\.?\d*', text)
    if document_type in ["invoice", "contract"] and len(amounts) == 0:
        flags.append(f"No monetary amounts found in a {document_type} — unusual")
        score += 20

    # Check 3: Dates missing (contracts/policies should have dates)
    dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b', text)
    if document_type in ["contract", "policy"] and len(dates) == 0:
        flags.append(f"No dates found in a {document_type} — unusual")
        score += 20

    # Check 4: Suspicious keywords (urgency/pressure tactics often used in scam docs)
    suspicious_keywords = ["wire transfer immediately", "urgent action required", "confidential - do not share", "act now"]
    found_suspicious = [kw for kw in suspicious_keywords if kw.lower() in text.lower()]
    if found_suspicious:
        flags.append(f"Suspicious language detected: {', '.join(found_suspicious)}")
        score += 25

    # Check 5: Repeated content (possible OCR error or corrupted doc)
    sentences = text.split('.')
    if len(sentences) > 5:
        unique_ratio = len(set(sentences)) / len(sentences)
        if unique_ratio < 0.5:
            flags.append("High content repetition detected — possible OCR or extraction error")
            score += 15

    score = min(score, 100)

    if score >= 60:
        risk_level = "high"
    elif score >= 30:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "flags": flags if flags else ["No anomalies detected"]
    }