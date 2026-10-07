from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from tempfile import NamedTemporaryFile
from app.services.document_processor import load_document, chunk_pages
from app.services.extractor import extract_entities, extract_relationships, detect_issues

app = FastAPI(title="AutoHLD-AI", version="1.0")

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".txt", ".md"}:
        raise HTTPException(400, "Supported formats: PDF, TXT, MD")
    data = await file.read()
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(data)
        path = tmp.name
    pages = load_document(path)
    chunks = chunk_pages(pages)
    entities = extract_entities(chunks)
    relationships = extract_relationships(chunks)
    issues = detect_issues(chunks, entities, relationships)
    return {
        "filename": file.filename,
        "pages": len(pages),
        "chunks": len(chunks),
        "entities": [e.__dict__ for e in entities],
        "relationships": [r.__dict__ for r in relationships],
        "issues": issues
    }
