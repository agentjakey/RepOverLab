from __future__ import annotations

import numpy as np


def cosine_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
    """
    Compute pairwise cosine similarity for L2-normalized embeddings.
    For normalized vectors, cosine similarity == dot product.
    Returns a symmetric float32 matrix of shape (N, N) in [0, 1].
    """
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    normed = embeddings / norms
    sim = normed @ normed.T
    return np.clip(sim, 0.0, 1.0).astype(np.float32)


def top_k_neighbors(
    similarity_matrix: np.ndarray,
    k: int = 10,
    exclude_self: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Return indices and similarity scores of the top-k neighbors for each concept.
    Returns:
        indices: shape (N, k)
        scores: shape (N, k)
    """
    n = similarity_matrix.shape[0]
    indices = np.zeros((n, k), dtype=np.int32)
    scores = np.zeros((n, k), dtype=np.float32)

    for i in range(n):
        row = similarity_matrix[i].copy()
        if exclude_self:
            row[i] = -1.0
        top = np.argsort(row)[::-1][:k]
        indices[i] = top
        scores[i] = similarity_matrix[i, top]

    return indices, scores


def neighbors_for_concept(
    concept_idx: int,
    similarity_matrix: np.ndarray,
    k: int = 10,
    exclude_self: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """Return sorted neighbor indices and scores for a single concept."""
    row = similarity_matrix[concept_idx].copy()
    if exclude_self:
        row[concept_idx] = -1.0
    top = np.argsort(row)[::-1][:k]
    return top, similarity_matrix[concept_idx, top]
