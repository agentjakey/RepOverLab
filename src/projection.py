from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path


def compute_umap(
    embeddings: np.ndarray,
    n_neighbors: int = 15,
    min_dist: float = 0.1,
    metric: str = "cosine",
    n_components: int = 2,
    random_state: int = 42,
) -> np.ndarray:
    """
    Project embeddings to 2D using UMAP.
    Raises ImportError if umap-learn is not installed; call compute_projection
    instead to get a PCA fallback automatically.
    """
    import umap

    reducer = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric=metric,
        n_components=n_components,
        random_state=random_state,
    )
    coords = reducer.fit_transform(embeddings)
    return coords.astype(np.float32)


def compute_pca(
    embeddings: np.ndarray,
    n_components: int = 2,
    random_state: int = 42,
) -> np.ndarray:
    """Project embeddings to 2D using PCA (deterministic, always available)."""
    from sklearn.decomposition import PCA

    pca = PCA(n_components=n_components, random_state=random_state)
    coords = pca.fit_transform(embeddings)
    return coords.astype(np.float32)


def compute_projection(
    embeddings: np.ndarray,
    n_neighbors: int = 15,
    min_dist: float = 0.1,
    metric: str = "cosine",
    n_components: int = 2,
    random_state: int = 42,
) -> tuple[np.ndarray, str]:
    """
    Project embeddings to n_components dimensions. Tries UMAP first; falls back
    to PCA if umap-learn is not installed.

    Returns (coords, method) where method is "umap" or "pca".
    """
    try:
        coords = compute_umap(
            embeddings,
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            metric=metric,
            n_components=n_components,
            random_state=random_state,
        )
        return coords, "umap"
    except ImportError:
        print("[project] umap-learn not installed, falling back to PCA.")
        coords = compute_pca(embeddings, n_components=n_components, random_state=random_state)
        return coords, "pca"


def load_coordinates(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"id", "x", "y"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Coordinate file missing columns: {missing}")
    return df


def save_coordinates(ids: list[str], coords: np.ndarray, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame({"id": ids, "x": coords[:, 0], "y": coords[:, 1]})
    df.to_csv(path, index=False)
