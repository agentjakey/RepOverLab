from __future__ import annotations

import numpy as np
from pathlib import Path
from typing import Optional


def embed_texts(
    texts: list[str],
    model_name: str = "all-MiniLM-L6-v2",
    normalize: bool = True,
    batch_size: int = 32,
    show_progress: bool = True,
) -> np.ndarray:
    """
    Embed a list of texts using sentence-transformers.
    Returns a float32 array of shape (N, embedding_dim).
    This function is called by the build pipeline, never by the runtime app.
    """
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=normalize,
        show_progress_bar=show_progress,
        convert_to_numpy=True,
    )
    return embeddings.astype(np.float32)


def load_embeddings(path: Path) -> np.ndarray:
    arr = np.load(str(path))
    if arr.ndim != 2:
        raise ValueError(f"Expected 2D embedding array, got shape {arr.shape}")
    return arr.astype(np.float32)


def save_embeddings(embeddings: np.ndarray, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(str(path), embeddings.astype(np.float32))
