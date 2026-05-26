from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


# Canonical column name for the row key in all artifact files.
# The examples CSV may carry both "example_id" and "id"; all coordinate and
# overlap files use "id".  Backward-compat aliases are added on load.
_KEY_COL = "id"


def load_all_artifacts(
    artifacts_dir: Path,
    config: Optional[dict] = None,
) -> dict:
    """
    Load all precomputed artifacts from disk.

    Returns a dict with keys:
        examples, embeddings, similarity, coordinates, overlap, merged, metadata.

    Raises FileNotFoundError with a clear message if any required file is missing.
    Raises ValueError if artifacts are internally inconsistent.
    """
    if config is None:
        config = {
            "examples_file": "demo_examples.csv",
            "embeddings_file": "semantic_embeddings.npy",
            "similarity_file": "similarity_semantic.npy",
            "coordinates_file": "map_coordinates.csv",
            "overlap_file": "overlap_scores.csv",
            "metadata_file": "artifact_metadata.json",
        }

    def _require(filename: str) -> Path:
        p = artifacts_dir / filename
        if not p.exists():
            raise FileNotFoundError(
                f"Required artifact not found: {p}\n"
                f"Run 'python scripts/export_demo_artifacts.py' to generate artifacts."
            )
        return p

    examples = pd.read_csv(_require(config["examples_file"]))
    embeddings = np.load(str(_require(config["embeddings_file"])))
    similarity = np.load(str(_require(config["similarity_file"])))
    coordinates = pd.read_csv(_require(config["coordinates_file"]))
    overlap = pd.read_csv(_require(config["overlap_file"]))
    with open(_require(config["metadata_file"]), encoding="utf-8") as f:
        metadata = json.load(f)

    # Ensure examples has an "id" column for merging (new schema uses example_id).
    examples = _normalize_examples(examples)

    _validate_artifact_consistency(examples, embeddings, similarity, coordinates, overlap)

    merged = examples.merge(coordinates, on=_KEY_COL).merge(
        overlap[[_KEY_COL, "overlap_score", "is_high_overlap"]], on=_KEY_COL
    )

    # Add backward-compatible display column aliases so that visualization code
    # written against the old schema continues to work without modification.
    merged = _add_display_aliases(merged)

    return {
        "examples": examples,
        "embeddings": embeddings,
        "similarity": similarity,
        "coordinates": coordinates,
        "overlap": overlap,
        "merged": merged,
        "metadata": metadata,
    }


def _normalize_examples(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure the examples DataFrame has an 'id' column for merging."""
    df = df.copy()
    if "id" not in df.columns:
        if "example_id" in df.columns:
            df["id"] = df["example_id"]
        else:
            raise ValueError(
                "examples CSV must have either an 'id' or 'example_id' column."
            )
    return df


def _add_display_aliases(merged: pd.DataFrame) -> pd.DataFrame:
    """
    Add aliased columns so visualization code using old column names still works.
    New column -> old alias added if the alias does not already exist.
    """
    merged = merged.copy()
    alias_map = {
        "example_id": "id",
        "title": "name",
        "topic": "short_name",
        "safety_band": "category",
        "framing": "tension_type",
        "content_text": "description",
    }
    for new_col, old_col in alias_map.items():
        if new_col in merged.columns and old_col not in merged.columns:
            merged[old_col] = merged[new_col]
    return merged


def _validate_artifact_consistency(
    examples: pd.DataFrame,
    embeddings: np.ndarray,
    similarity: np.ndarray,
    coordinates: pd.DataFrame,
    overlap: pd.DataFrame,
) -> None:
    n = len(examples)
    if embeddings.shape[0] != n:
        raise ValueError(
            f"Embedding count ({embeddings.shape[0]}) does not match "
            f"example count ({n}). Regenerate artifacts."
        )
    if similarity.shape != (n, n):
        raise ValueError(
            f"Similarity matrix shape {similarity.shape} expected ({n}, {n})."
        )
    if len(coordinates) != n:
        raise ValueError(f"Coordinate count ({len(coordinates)}) != example count ({n}).")
    if len(overlap) != n:
        raise ValueError(f"Overlap score count ({len(overlap)}) != example count ({n}).")


def write_artifact_metadata(
    artifacts_dir: Path,
    n_concepts: int,
    embedding_model: str,
    embedding_dim: int,
    projection_method: str,
    is_synthetic: bool,
    extra: Optional[dict] = None,
) -> None:
    metadata = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_concepts": n_concepts,
        "embedding_model": embedding_model,
        "embedding_dim": embedding_dim,
        "projection_method": projection_method,
        "is_synthetic": is_synthetic,
        "version": "0.1.0",
    }
    if extra:
        metadata.update(extra)

    out = artifacts_dir / "artifact_metadata.json"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
