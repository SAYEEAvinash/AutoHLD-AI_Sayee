from pathlib import Path
from app.services.document_processor import load_document, chunk_pages
from app.services.extractor import extract_entities, extract_relationships, detect_issues

def test_demo_document():
    path = Path("data/hld_corpus/HLD_01_vehicle_control.txt")
    pages = load_document(str(path))
    chunks = chunk_pages(pages)
    entities = extract_entities(chunks)
    relationships = extract_relationships(chunks)
    issues = detect_issues(chunks, entities, relationships)
    names = {e.name for e in entities}
    assert "VehicleController" in names
    assert "DiagnosticManager" in names
    assert len(relationships) >= 3
    assert len(issues) >= 1
