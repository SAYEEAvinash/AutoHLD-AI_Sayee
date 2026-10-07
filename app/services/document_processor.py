from pathlib import Path
import re
import fitz
from .models import DocumentChunk

SUPPORTED = {".pdf", ".txt", ".md"}

def extract_pdf(path):
    doc = fitz.open(path)
    return [(i, page.get_text("text") or "") for i, page in enumerate(doc, start=1)]

def extract_text(path):
    return [(1, Path(path).read_text(encoding="utf-8"))]

def load_document(path):
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix in {".txt", ".md"}:
        return extract_text(path)
    raise ValueError(f"Unsupported file type: {suffix}")

def chunk_pages(pages, max_chars=1500, overlap=220):
    """Chunk on line/paragraph boundaries so architecture statements are not cut in half."""
    chunks, idx = [], 1
    for page_no, raw in pages:
        raw = raw.replace("\r\n", "\n").replace("\r", "\n")
        lines = [re.sub(r"[ \t]+", " ", x).strip() for x in raw.split("\n")]
        lines = [x for x in lines if x]
        if not lines:
            continue

        current = []
        current_len = 0
        previous_tail = ""

        for line in lines:
            if current and current_len + len(line) + 1 > max_chars:
                text = " ".join(current).strip()
                chunks.append(DocumentChunk(
                    chunk_id=f"chunk_{idx}",
                    page=page_no,
                    text=text,
                    metadata={"page": page_no}
                ))
                idx += 1
                # Keep a small number of previous characters as context, but don't split statements.
                previous_tail = text[-overlap:]
                current = [previous_tail] if previous_tail else []
                current_len = len(previous_tail)

            current.append(line)
            current_len += len(line) + 1

        if current:
            chunks.append(DocumentChunk(
                chunk_id=f"chunk_{idx}",
                page=page_no,
                text=" ".join(current).strip(),
                metadata={"page": page_no}
            ))
            idx += 1

    return chunks
