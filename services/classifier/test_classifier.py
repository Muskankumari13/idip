from classifier import classify_document

test_text = """
This agreement is entered into between Party A and Party B.
The terms and conditions of this contract are as follows:
Payment shall be made within 30 days of invoice receipt.
Both parties agree to the terms stated herein.
"""

result = classify_document(test_text)
print("Document Type:", result["document_type"])
print("Confidence:", result["confidence"])
print("All Scores:", result["all_scores"])