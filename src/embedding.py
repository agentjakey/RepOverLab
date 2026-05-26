from __future__ import annotations

import numpy as np
from pathlib import Path


def embed_texts(
    texts: list[str],
    model_name: str = "all-MiniLM-L6-v2",
    normalize: bool = True,
    batch_size: int = 32,
    show_progress: bool = True,
) -> tuple[np.ndarray, str]:
    """
    Embed texts using sentence-transformers.

    Falls back to TF-IDF + TruncatedSVD if sentence-transformers cannot be
    imported or the model cannot load. The fallback produces embeddings of the
    same dimensionality (384) but they are lexical rather than semantic.

    Returns (embeddings, model_used) where model_used identifies which backend ran.
    Call this from build scripts only; the runtime app loads precomputed artifacts.
    """
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(model_name)
        embeddings = model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=normalize,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
        )
        return embeddings.astype(np.float32), model_name
    except Exception as exc:
        print(f"[embed] sentence-transformers unavailable ({type(exc).__name__}: {exc})")
        print("[embed] Falling back to TF-IDF + TruncatedSVD (384 components).")
        return _tfidf_svd_fallback(texts, n_components=384, normalize=normalize), "tfidf-truncated-svd"


def _tfidf_svd_fallback(
    texts: list[str],
    n_components: int = 384,
    normalize: bool = True,
) -> np.ndarray:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import TruncatedSVD

    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2), sublinear_tf=True)
    tfidf = vectorizer.fit_transform(texts)

    actual_dim = min(n_components, tfidf.shape[1] - 1, tfidf.shape[0] - 1)
    svd = TruncatedSVD(n_components=actual_dim, random_state=42)
    reduced = svd.fit_transform(tfidf).astype(np.float32)

    if reduced.shape[1] < n_components:
        pad = np.zeros((reduced.shape[0], n_components - reduced.shape[1]), dtype=np.float32)
        reduced = np.concatenate([reduced, pad], axis=1)

    if normalize:
        norms = np.linalg.norm(reduced, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        reduced = reduced / norms

    return reduced


def load_embeddings(path: Path) -> np.ndarray:
    arr = np.load(str(path))
    if arr.ndim != 2:
        raise ValueError(f"Expected 2D embedding array, got shape {arr.shape}")
    return arr.astype(np.float32)


def save_embeddings(embeddings: np.ndarray, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(str(path), embeddings.astype(np.float32))
