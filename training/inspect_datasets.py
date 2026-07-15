import os
import warnings
os.environ["HF_HUB_VERBOSITY"] = "error"
warnings.filterwarnings("ignore")

from datasets import load_dataset
from itertools import islice

print("=== Invoice dataset (streaming) ===")
try:
    ds = load_dataset("mychen76/invoices-and-receipts_ocr_v1", split="train", streaming=True)
    sample = list(islice(ds, 3))
    for s in sample:
        print(s)
except Exception as e:
    print("ERROR:", e)

print("\n=== Research paper abstracts (streaming) ===")
try:
    ds = load_dataset("ccdv/arxiv-classification", split="train", streaming=True)
    sample = list(islice(ds, 3))
    for s in sample:
        print(s)
except Exception as e:
    print("ERROR:", e)
print("\n=== CUAD Contracts (streaming) ===")
try:
    ds = load_dataset("dvgodoy/CUAD_v1_Contract_Understanding_PDF", split="train", streaming=True)
    sample = list(islice(ds, 3))
    for s in sample:
        print(s["file_name"])
        text = s["text"] or ""
        print(text[:500])
        print("---")
except Exception as e:
    print("ERROR:", e)