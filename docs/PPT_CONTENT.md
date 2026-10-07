# Final Presentation — 12 Slides

## 1. Title
AutoHLD-AI
AI-Powered AUTOSAR HLD Analysis and Architecture Traceability Assistant

## 2. Problem
Large HLDs are difficult to search and cross-reference.
Manual interpretation creates effort and traceability challenges.

## 3. Motivation
Need an evidence-grounded assistant that supports engineers without replacing engineering approval.

## 4. Objectives
Search, extract, map, detect, cite, report.

## 5. Proposed Architecture
Streamlit → FastAPI → ingestion → retrieval → local LLM → validation → report.

## 6. Core Features
- document analysis
- architecture Q&A
- entity extraction
- relationship graph
- inconsistency detection
- report generation

## 7. Dataset
12 synthetic HLDs, ground truth annotations, intentional controlled issues.

## 8. AI Methodology
Chunking → embeddings/retrieval → evidence selection → constrained generation → citation → human review.

## 9. Evaluation
Precision, recall, F1, Hit@5, citation correctness, groundedness, latency.

## 10. Demo
Upload → ask question → inspect sources → view graph → review issues → export report.

## 11. Limitations & Ethics
Synthetic dataset, no compliance claim, human approval required, licensed sources only.

## 12. Conclusion
A reusable foundation for future HARA/TARA/UDS engineering assistants.
