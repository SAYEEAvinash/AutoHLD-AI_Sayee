# AutoHLD-AI — Final Project Report Structure

## Title
AI-Powered AUTOSAR HLD Analysis and Architecture Traceability Assistant

## Abstract
Large automotive High-Level Design documents contain architecture entities, interfaces, signals, dependencies and functional flows. Manual review can be time-consuming and can make architecture knowledge difficult to search and trace. AutoHLD-AI is an AI-assisted prototype that combines document ingestion, local retrieval, architecture entity extraction, relationship mapping, evidence-grounded question answering, deterministic consistency checks and report generation. The prototype uses synthetic HLD documents so that the evaluation is reproducible and does not expose proprietary engineering information.

## 1. Introduction
Describe the engineering documentation problem, why architecture traceability matters, and why an evidence-grounded AI assistant is appropriate.

## 2. Problem Statement
Manual interpretation of large HLD documents can require repeated search and cross-reference work. The project aims to reduce this effort while retaining human review.

## 3. Objectives
- searchable HLD knowledge
- architecture extraction
- cited Q&A
- relationship mapping
- issue detection
- structured reporting
- measurable evaluation

## 4. System Design
Include the architecture:
User → Streamlit → FastAPI → ingestion → chunking → embeddings/retrieval → LLM → validation → report.

## 5. Methodology
### 5.1 Ingestion
PDF/TXT/MD extraction using PyMuPDF/text parser.

### 5.2 Chunking
Context-preserving chunks with overlap.

### 5.3 Retrieval
Baseline: TF-IDF.
Enhanced mode: Sentence Transformer embeddings.
Future production mode: BGE/E5 + ChromaDB.

### 5.4 Generation
Optional local Ollama model receives only retrieved evidence.

### 5.5 Architecture Extraction
Regex/rule-based extraction for the controlled synthetic dataset.

### 5.6 Validation
Deterministic checks identify potential terminology ambiguity and missing interfaces.

## 6. Dataset
12 synthetic HLD documents with ground-truth entity and relationship annotations. Five documents contain intentional terminology-change issues.

## 7. Evaluation
Report actual values from `data/evaluation/summary.json`.

### Metrics
**Precision** = TP / (TP + FP)

**Recall** = TP / (TP + FN)

**F1** = 2 × Precision × Recall / (Precision + Recall)

**Retrieval Hit@5** = queries where the gold page appears in the top 5 retrieved chunks / total queries.

Also report:
- citation correctness
- answer groundedness
- issue detection precision/recall
- response latency
- manual vs AI-assisted review time

Do not invent these measurements. Run controlled experiments and record the observed values.

## 8. Results
Use the generated evaluation files and add a manual review table for Q&A quality.

## 9. Limitations
- synthetic dataset
- controlled extraction patterns
- no formal AUTOSAR compliance claim
- optional LLM variability
- no production vehicle integration
- no automatic architecture approval

## 10. Security and Governance
- local/private inference where required
- project-level data isolation
- repository/document text treated as untrusted content
- human review
- audit logging in a production extension
- approved/licensed standards only

## 11. Future Work
- OCR
- BGE/E5 + ChromaDB
- Neo4j traceability
- revision comparison
- RBAC
- enterprise IAM
- approved engineering repository integration
- domain-specific benchmark

## 12. Conclusion
AutoHLD-AI demonstrates a practical architecture-aware AI workflow for HLD analysis while keeping outputs evidence-based and reviewable.
