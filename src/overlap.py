from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path

from src.similarity import top_k_neighbors


def compute_overlap_scores(
    similarity_matrix: np.ndarray,
    categories: list[str],
    k: int = 10,
) -> np.ndarray:
    """
    For each concept, compute the fraction of its top-k neighbors
    that belong to a different category. Score is in [0.0, 1.0].

    0.0 = all neighbors share the same category
    1.0 = all neighbors are from a different category
    """
    n = len(categories)
    neighbor_indices, _ = top_k_neighbors(similarity_matrix, k=k, exclude_self=True)
    scores = np.zeros(n, dtype=np.float32)

    for i in range(n):
        neighbor_cats = [categories[j] for j in neighbor_indices[i]]
        cross_category = sum(1 for c in neighbor_cats if c != categories[i])
        scores[i] = cross_category / k

    return scores


def cross_category_affinity(
    similarity_matrix: np.ndarray,
    categories: list[str],
    k: int = 10,
) -> pd.DataFrame:
    """
    For each ordered pair of categories (A, B), compute the mean cosine
    similarity between A-concepts and their top-k B-category neighbors.
    Returns a DataFrame with columns: category_a, category_b, mean_similarity, count.
    """
    unique_cats = sorted(set(categories))
    n = len(categories)
    neighbor_indices, neighbor_scores = top_k_neighbors(
        similarity_matrix, k=k, exclude_self=True
    )
    rows = []

    for cat_a in unique_cats:
        for cat_b in unique_cats:
            if cat_a == cat_b:
                continue
            sims = []
            for i, cat in enumerate(categories):
                if cat != cat_a:
                    continue
                for j_pos, j in enumerate(neighbor_indices[i]):
                    if categories[j] == cat_b:
                        sims.append(float(neighbor_scores[i, j_pos]))
            if sims:
                rows.append(
                    {
                        "category_a": cat_a,
                        "category_b": cat_b,
                        "mean_similarity": round(float(np.mean(sims)), 4),
                        "count": len(sims),
                    }
                )

    return pd.DataFrame(rows)


def load_overlap_scores(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"id", "overlap_score", "category"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Overlap file missing columns: {missing}")
    return df


def save_overlap_scores(
    ids: list[str],
    categories: list[str],
    scores: np.ndarray,
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(
        {
            "id": ids,
            "category": categories,
            "overlap_score": scores.round(4),
            "is_high_overlap": (scores >= 0.6).astype(int),
        }
    )
    df.to_csv(path, index=False)
