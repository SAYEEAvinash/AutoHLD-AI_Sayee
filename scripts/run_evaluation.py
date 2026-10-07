import sys, json, argparse
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.services.evaluator import evaluate_corpus

parser = argparse.ArgumentParser()
parser.add_argument("--embeddings", action="store_true")
args = parser.parse_args()

rows = evaluate_corpus("data/hld_corpus", "data/ground_truth", use_embeddings=args.embeddings)
Path("data/evaluation").mkdir(parents=True, exist_ok=True)
Path("data/evaluation/results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

def avg(k):
    return sum(r[k] for r in rows)/len(rows)

summary = {
    "documents": len(rows),
    "entity_precision": avg("entity_precision"),
    "entity_recall": avg("entity_recall"),
    "entity_f1": avg("entity_f1"),
    "relationship_precision": avg("relationship_precision"),
    "relationship_recall": avg("relationship_recall"),
    "relationship_f1": avg("relationship_f1"),
    "retrieval_hit_at_5": avg("retrieval_hit_at_5"),
}
Path("data/evaluation/summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
