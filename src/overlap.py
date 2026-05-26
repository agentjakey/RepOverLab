"""
Overlap and boundary scoring for the Representation Overlap Lab.

IMPORTANT: All scores in this module are geometric heuristics for exploration.
They measure proximity in embedding space, not moral or risk similarity.
Embedding distance does not equal moral distance. Do not use these scores as
safety classifiers or to make policy decisions. They are intended to help users
see where safety categories are not cleanly separable.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional

from src.similarity import top_k_neighbors


# The three reference bands whose centroid similarities are included as named
# columns. These are the bands most relevant to understanding boundary blur.
REFERENCE_BANDS = ["benign", "ambiguous", "policy_relevant_sanitized"]


def compute_overlap_scores(
    similarity_matrix: np.ndarray,
    categories: list[str],
    k: int = 10,
) -> np.ndarray:
    """
    For each example, compute the fraction of its top-k neighbors that belong
    to a different safety band. Score is in [0.0, 1.0].

    0.0 = all neighbors share the same band
    1.0 = all neighbors are from a different band

    This is an exploration heuristic. High scores indicate the example sits near
    a category boundary in embedding space, not that it is unsafe.
    """
    n = len(categories)
    neighbor_indices, _ = top_k_neighbors(similarity_matrix, k=k, exclude_self=True)
    scores = np.zeros(n, dtype=np.float32)

    for i in range(n):
        neighbor_cats = [categories[j] for j in neighbor_indices[i]]
        cross_band = sum(1 for c in neighbor_cats if c != categories[i])
        scores[i] = cross_band / k

    return scores


def compute_nearest_cross_band_sim(
    similarity_matrix: np.ndarray,
    safety_bands: list[str],
) -> np.ndarray:
    """
    For each example, return the cosine similarity to its nearest neighbor from
    a different safety band. Returns 0.0 if all examples share one band.
    """
    n = len(safety_bands)
    result = np.zeros(n, dtype=np.float32)

    for i in range(n):
        row = similarity_matrix[i].copy()
        row[i] = -1.0  # exclude self
        for j in range(n):
            if safety_bands[j] == safety_bands[i]:
                row[j] = -1.0  # exclude same-band members
        best = float(row.max())
        result[i] = max(0.0, best)

    return result


def compute_centroid_sims(
    embeddings: np.ndarray,
    safety_bands: list[str],
    reference_bands: Optional[list[str]] = None,
) -> dict[str, np.ndarray]:
    """
    For each reference band, compute the L2-normalized centroid of its members,
    then return the cosine similarity from every example to that centroid.

    Returns a dict: band_key -> float32 array of shape (N,), values in [0, 1].
    Bands with no members are omitted from the result.
    """
    if reference_bands is None:
        reference_bands = REFERENCE_BANDS

    bands_array = np.array(safety_bands)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    normed = embeddings / norms

    result: dict[str, np.ndarray] = {}
    for band in reference_bands:
        mask = bands_array == band
        if not mask.any():
            continue
        centroid = normed[mask].mean(axis=0)
        c_norm = np.linalg.norm(centroid)
        if c_norm == 0:
            continue
        centroid = centroid / c_norm
        sims = (normed @ centroid).clip(0.0, 1.0).astype(np.float32)
        result[band] = sims

    return result


def compute_boundary_blur_score(
    centroid_sims: dict[str, np.ndarray],
) -> np.ndarray:
    """
    Boundary blur is an exploration heuristic: high when an example sits near
    multiple safety bands simultaneously, low when it sits firmly within one band.

    Method: normalized entropy of per-band centroid similarities treated as a
    probability distribution (divided by their sum). Score is in [0, 1].

    1.0 = equidistant from all reference bands (maximally blurry boundary)
    0.0 = strongly associated with a single band

    IMPORTANT: This is a geometric proximity score, not a safety judgment.
    It is useful for finding interesting examples to examine, not for classifying
    content as safe or unsafe. Embedding distance does not equal moral distance.
    """
    if not centroid_sims:
        return np.array([], dtype=np.float32)

    bands = sorted(centroid_sims.keys())
    if len(bands) == 1:
        n = len(next(iter(centroid_sims.values())))
        return np.zeros(n, dtype=np.float32)

    sim_matrix = np.stack([centroid_sims[b] for b in bands], axis=1).clip(0.0)

    # Normalize each row to sum to 1 (treat cosine sims as proportional weights).
    row_sums = sim_matrix.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums == 0, 1.0, row_sums)
    probs = sim_matrix / row_sums

    eps = 1e-9
    entropy = -np.sum(probs * np.log(probs + eps), axis=1)
    max_entropy = np.log(len(bands))

    blur = (entropy / max_entropy).clip(0.0, 1.0).astype(np.float32)
    return blur


def cross_category_affinity(
    similarity_matrix: np.ndarray,
    categories: list[str],
    k: int = 10,
) -> pd.DataFrame:
    """
    For each ordered pair of bands (A, B), compute the mean cosine similarity
    between A-examples and their top-k B-band neighbors.
    Returns a DataFrame: category_a, category_b, mean_similarity, count.
    """
    unique_cats = sorted(set(categories))
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


def save_overlap_scores(
    ids: list[str],
    safety_bands: list[str],
    scores: np.ndarray,
    path: Path,
    *,
    nearest_cross_band_sim: Optional[np.ndarray] = None,
    centroid_sims: Optional[dict[str, np.ndarray]] = None,
    boundary_blur_scores: Optional[np.ndarray] = None,
) -> None:
    """
    Save overlap scores to CSV.

    Required columns: id, safety_band, overlap_score, is_high_overlap.
    Optional columns (included when provided): nearest_cross_band_sim,
    sim_to_benign, sim_to_ambiguous, sim_to_policy_relevant, boundary_blur_score.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    data: dict[str, object] = {
        "id": ids,
        "safety_band": safety_bands,
        "overlap_score": scores.round(4),
        "is_high_overlap": (scores >= 0.6).astype(int),
    }

    if nearest_cross_band_sim is not None:
        data["nearest_cross_band_sim"] = nearest_cross_band_sim.round(4)

    if centroid_sims is not None:
        for band_key in REFERENCE_BANDS:
            col = f"sim_to_{band_key}"
            if band_key in centroid_sims:
                data[col] = centroid_sims[band_key].round(4)
            else:
                data[col] = np.zeros(len(ids), dtype=np.float32)

    if boundary_blur_scores is not None:
        data["boundary_blur_score"] = boundary_blur_scores.round(4)

    pd.DataFrame(data).to_csv(path, index=False)


def load_overlap_scores(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"id", "overlap_score"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Overlap file missing columns: {missing}")
    return df
