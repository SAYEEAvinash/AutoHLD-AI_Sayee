# AutoHLD-AI v1.0 — Final Academic Prototype

## Purpose
AI-assisted analysis of AUTOSAR-style High-Level Design documents using local retrieval, optional local LLM generation, architecture extraction, traceability and consistency checks.

The project is aligned with the supplied Automotive Engineering AI case study, which describes an HLD analysis assistant using document ingestion, RAG, local vector storage, Python services, citations and human review.

## Main features
- PDF/TXT/MD ingestion
- local lexical retrieval baseline
- optional semantic embeddings
- optional Ollama local LLM
- architecture entity extraction
- relationship extraction
- interactive architecture graph
- terminology/missing-interface issue detection
- report generation
- FastAPI API
- reproducible synthetic dataset
- ground-truth annotations
- evaluation metrics and script
- report/paper/PPT/demo documentation

## Quick start
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Optional semantic retrieval:
```bash
pip install -r requirements-rag.txt
```

Optional local LLM:
Install Ollama separately, pull a suitable local model, and set environment variables from `.env.example`.

## Evaluate
```bash
python scripts/run_evaluation.py
```

Optional embeddings:
```bash
python scripts/run_evaluation.py --embeddings
```

## API
```bash
uvicorn app.api:app --reload
```
Then:
`GET /health`
`POST /analyze`

## Dataset
See `data/README.md`.

## Important academic integrity note
The HLD corpus is synthetic. It is intentionally not presented as official AUTOSAR/OEM content. Do not claim AUTOSAR compliance from this prototype. For real deployment, use approved and licensed documents.

## Final deliverables
- working application
- dataset
- ground truth
- evaluation script
- evaluation outputs
- project report structure
- research paper outline
- PPT content
- demo script
- evaluation protocol
