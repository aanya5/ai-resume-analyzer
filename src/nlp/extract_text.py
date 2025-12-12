# Minimal helper: takes either raw text or a path to a simple text/pdf/docx file.
import os
from pdfminer.high_level import extract_text as pdf_extract
from docx import Document

def extract_text_from_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return pdf_extract(path)
    elif ext in [".docx", ".doc"]:
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        # txt or fallback
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def extract_text_from_string(s: str) -> str:
    return s or ""