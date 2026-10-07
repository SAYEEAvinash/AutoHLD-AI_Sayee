# Research Paper Outline

## Proposed title
Retrieval-Augmented and Rule-Assisted AI for Evidence-Grounded Analysis of Automotive High-Level Design Documents

## Research question
Can an architecture-aware retrieval and validation pipeline improve the accuracy, traceability and consistency of AI-assisted HLD analysis compared with ungrounded or generic retrieval approaches?

## Contributions
1. Synthetic reproducible HLD benchmark.
2. Architecture entity and relationship extraction pipeline.
3. Evidence-grounded Q&A with source-page attribution.
4. Deterministic consistency checks.
5. Evaluation framework using entity F1, relationship F1, retrieval Hit@5 and human-reviewed citation correctness.

## Experimental comparison
A. Extractive baseline / TF-IDF retrieval
B. Sentence-transformer retrieval
C. Optional local LLM + retrieval

Compare:
- retrieval Hit@5
- entity precision/recall/F1
- relationship precision/recall/F1
- citation correctness
- groundedness
- latency

## Hypotheses
H1: semantic embeddings improve retrieval Hit@5 over lexical retrieval on paraphrased architecture questions.
H2: retrieval grounding reduces unsupported answers.
H3: deterministic validation catches controlled terminology inconsistencies that free-form generation alone may miss.

## Reproducibility
All synthetic documents, ground truth and evaluation scripts are included in the project repository.
