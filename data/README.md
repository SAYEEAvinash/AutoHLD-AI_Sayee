# AutoHLD-AI Synthetic Dataset

This dataset contains 12 synthetic AUTOSAR-style HLD documents created for academic testing.

## Important
These files are fictional and are **not** official AUTOSAR specifications, OEM documents, or production vehicle architecture. They must not be represented as such.

## Corpus
- 12 HLD documents
- 5–6 software components per document
- 4–5 interfaces per document
- 3–5 signals per document
- explicit relationships
- 5 documents intentionally contain revision terminology changes

## Ground truth
`data/ground_truth/*.json` stores:
- expected entities
- expected relationships
- retrieval questions and gold page
- whether an intentional issue was introduced

## Why synthetic data?
It permits reproducible evaluation without exposing proprietary engineering information.
For a real deployment, replace it with approved, licensed engineering documents.
