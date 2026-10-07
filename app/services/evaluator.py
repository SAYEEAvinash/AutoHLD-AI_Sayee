import json, re
from pathlib import Path
from app.services.document_processor import load_document, chunk_pages
from app.services.extractor import extract_entities, extract_relationships, detect_issues
from app.services.retriever import build_retriever

def prf(tp, fp, fn):
    p = tp/(tp+fp) if tp+fp else 0
    r = tp/(tp+fn) if tp+fn else 0
    f = 2*p*r/(p+r) if p+r else 0
    return p, r, f

def entity_metrics(pred, gold):
    pred_set = {(e.entity_type, e.name.lower()) for e in pred}
    gold_set = {(x["type"], x["name"].lower()) for x in gold}
    tp = len(pred_set & gold_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)
    return prf(tp, fp, fn), {"tp":tp, "fp":fp, "fn":fn}

def relationship_metrics(pred, gold):
    pred_set = {(r.source.lower(), r.relation, r.target.lower()) for r in pred}
    gold_set = {(x["source"].lower(), x["relation"], x["target"].lower()) for x in gold}
    tp = len(pred_set & gold_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)
    return prf(tp, fp, fn), {"tp":tp, "fp":fp, "fn":fn}

def evaluate_corpus(corpus_dir, ground_truth_dir, use_embeddings=False):
    results = []
    for truth_path in sorted(Path(ground_truth_dir).glob("*.json")):
        truth = json.loads(truth_path.read_text(encoding="utf-8"))
        doc_path = Path(corpus_dir) / truth["filename"]
        pages = load_document(str(doc_path))
        chunks = chunk_pages(pages)
        entities = extract_entities(chunks)
        relationships = extract_relationships(chunks)
        ep, ec = entity_metrics(entities, truth["entities"])
        rp, rc = relationship_metrics(relationships, truth["relationships"])

        retriever = build_retriever(chunks, prefer_embeddings=use_embeddings)
        hits = []
        for q in truth.get("queries", []):
            ranked = retriever.search(q["question"], k=5)
            retrieved_pages = {c.page for c, _ in ranked}
            hits.append(q["gold_page"] in retrieved_pages)

        results.append({
            "filename": truth["filename"],
            "entity_precision": ep[0],
            "entity_recall": ep[1],
            "entity_f1": ep[2],
            "relationship_precision": rp[0],
            "relationship_recall": rp[1],
            "relationship_f1": rp[2],
            "retrieval_hit_at_5": sum(hits)/len(hits) if hits else 0,
        })
    return results
