import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class BaseRetriever:
    def search(self, query, k=5):
        raise NotImplementedError

class TFIDFRetriever(BaseRetriever):
    def __init__(self, chunks):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(
            stop_words="english", ngram_range=(1,2), max_features=20000
        )
        self.matrix = self.vectorizer.fit_transform([c.text for c in chunks]) if chunks else None

    def search(self, query, k=5):
        if not self.chunks or self.matrix is None:
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        idxs = scores.argsort()[::-1][:k]
        return [(self.chunks[i], float(scores[i])) for i in idxs if scores[i] > 0]

class SentenceTransformerRetriever(BaseRetriever):
    def __init__(self, chunks, model_name="all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.chunks = chunks
        self.model = SentenceTransformer(model_name)
        self.embeddings = self.model.encode(
            [c.text for c in chunks], normalize_embeddings=True, show_progress_bar=False
        )

    def search(self, query, k=5):
        import numpy as np
        q = self.model.encode([query], normalize_embeddings=True)[0]
        scores = self.embeddings @ q
        idxs = np.argsort(scores)[::-1][:k]
        return [(self.chunks[i], float(scores[i])) for i in idxs]

def build_retriever(chunks, prefer_embeddings=True):
    if prefer_embeddings:
        try:
            return SentenceTransformerRetriever(chunks)
        except Exception:
            pass
    return TFIDFRetriever(chunks)
