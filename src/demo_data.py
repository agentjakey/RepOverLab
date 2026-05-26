"""
Synthetic demo artifact generation.

When the real embedding pipeline has not been run (no sentence-transformers model
downloaded), this module generates structured synthetic embeddings that preserve
the geometric properties needed to demonstrate the overlap problem:
- Concepts within a safety band cluster together
- Bands partially overlap with their neighbors
- abstract_risk_placeholder is proximate to policy_relevant_sanitized
- Some ambiguous examples span multiple clusters

These synthetic embeddings are NOT semantic embeddings. They are designed for
demonstration and visual clarity, not for research conclusions. The app labels
synthetic artifacts clearly so users know what they are looking at.
"""
from __future__ import annotations

import numpy as np


CATEGORY_CENTERS = {
    "benign": np.array([2.0, 0.0]),
    "capability_building": np.array([1.0, 1.5]),
    "ambiguous": np.array([0.0, 1.0]),
    "policy_relevant_sanitized": np.array([-1.0, 1.2]),
    "abstract_risk_placeholder": np.array([-1.8, 0.3]),
}

WITHIN_CATEGORY_STD = 0.45
BOUNDARY_BLEND_FRACTION = 0.25
EMBEDDING_DIM = 384
RANDOM_STATE = 42


def generate_synthetic_embeddings(categories: list[str]) -> np.ndarray:
    """
    Generate high-dimensional synthetic embeddings with clustered structure.
    The 2D layout implied by CATEGORY_CENTERS is embedded into EMBEDDING_DIM
    via a fixed random projection, so UMAP will recover something close to
    the intended layout.
    """
    rng = np.random.default_rng(RANDOM_STATE)
    n = len(categories)

    projection_matrix = rng.normal(0, 1 / np.sqrt(EMBEDDING_DIM), (2, EMBEDDING_DIM))

    embeddings = []
    for cat in categories:
        center_2d = CATEGORY_CENTERS.get(cat, np.array([0.0, 0.0]))

        neighbors = _get_neighbor_categories(cat)
        if neighbors and rng.random() < BOUNDARY_BLEND_FRACTION:
            neighbor_cat = rng.choice(neighbors)
            neighbor_center = CATEGORY_CENTERS.get(neighbor_cat, np.array([0.0, 0.0]))
            blend = rng.uniform(0.3, 0.6)
            center_2d = (1 - blend) * center_2d + blend * neighbor_center

        noise_2d = rng.normal(0, WITHIN_CATEGORY_STD, 2)
        point_2d = center_2d + noise_2d

        high_dim = point_2d @ projection_matrix
        residual = rng.normal(0, 0.1, EMBEDDING_DIM)
        vec = high_dim + residual
        vec = vec / np.linalg.norm(vec)
        embeddings.append(vec.astype(np.float32))

    return np.stack(embeddings)


def _get_neighbor_categories(cat: str) -> list[str]:
    adjacency = {
        "benign": ["capability_building"],
        "capability_building": ["benign", "ambiguous"],
        "ambiguous": ["capability_building", "policy_relevant_sanitized"],
        "policy_relevant_sanitized": ["ambiguous", "abstract_risk_placeholder"],
        "abstract_risk_placeholder": ["policy_relevant_sanitized"],
    }
    return adjacency.get(cat, [])


def generate_synthetic_2d_coords(categories: list[str]) -> np.ndarray:
    """Generate 2D coordinates directly from category centers with noise."""
    rng = np.random.default_rng(RANDOM_STATE)
    coords = []
    for cat in categories:
        center = CATEGORY_CENTERS.get(cat, np.array([0.0, 0.0]))
        noise = rng.normal(0, WITHIN_CATEGORY_STD, 2)
        coords.append(center + noise)
    return np.array(coords, dtype=np.float32)
