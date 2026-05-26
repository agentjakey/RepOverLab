from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional


def compute_umap(
    embeddings: np.ndarray,
    n_neighbors: int = 15,
    min_dist: float = 0.1,
    metric: str = "cosine",
    n_components: int = 2,
    random_state: int = 42,
) -> np.ndarray:
    """
    Project high-dimensional embeddings to 2D using UMAP.
    Returns float32 array of shape (N, 2).
    Called by the build pipeline only.
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
