# Evaluation Protocol

## A. Entity extraction
For every corpus document:
1. Run extraction.
2. Compare `(entity_type, entity_name)` with ground truth.
3. Compute TP, FP, FN.
4. Report precision, recall and F1.

## B. Relationship extraction
Compare `(source, relation, target)` with ground truth.

## C. Retrieval
For each ground-truth question:
1. retrieve top 5 chunks;
2. check whether the gold page is retrieved;
3. calculate Hit@5.

## D. Q&A human review
Create at least 30 questions:
- 10 direct lookup
- 10 multi-hop/relationship
- 10 paraphrased
Rate each answer 0/1 for:
- correct
- grounded
- citation correct

## E. Issue detection
Use the five intentionally modified documents as positive cases.
Measure:
- precision
- recall
- F1

## F. Efficiency
For a fixed document set, record:
- manual review time
- AI-assisted review time
- percentage time reduction

## G. Reproducibility
Run:
`python scripts/run_evaluation.py`
and save:
`data/evaluation/summary.json`
