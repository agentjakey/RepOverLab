"""
Tests for artifact_io.py loading and validation logic.
These tests use small in-memory DataFrames and numpy arrays to verify
that the loader raises clear errors for inconsistent artifacts.
"""
import json
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.artifact_io import load_all_artifacts, write_artifact_metadata


def make_artifacts(tmp_dir: Path, n: int = 5, dim: int = 16) -> None:
    ids = [f"CB{i:03d}" for i in range(1, n + 1)]

    examples = pd.DataFrame(
        {
            "id": ids,
            "name": [f"Concept {i}" for i in range(n)],
            "short_name": [f"Concept {i}" for i in range(n)],
            "description": [f"Description of concept {i} with enough text." for i in range(n)],
            "category": ["clearly_benign"] * n,
            "tension_type": ["none"] * n,
            "legitimate_use_note": [""] * n,
        }
    )
    examples.to_csv(tmp_dir / "demo_examples.csv", index=False)

    rng = np.random.default_rng(42)
    emb = rng.normal(0, 1, (n, dim)).astype(np.float32)
    np.save(str(tmp_dir / "semantic_embeddings.npy"), emb)

    sim = emb @ emb.T
    sim = (sim - sim.min()) / (sim.max() - sim.min() + 1e-8)
    np.save(str(tmp_dir / "similarity_semantic.npy"), sim.astype(np.float32))

    coords = pd.DataFrame({"id": ids, "x": rng.uniform(-1, 1, n), "y": rng.uniform(-1, 1, n)})
    coords.to_csv(tmp_dir / "map_coordinates.csv", index=False)

    overlap = pd.DataFrame(
        {"id": ids, "category": ["clearly_benign"] * n, "overlap_score": [0.0] * n, "is_high_overlap": [0] * n}
    )
    overlap.to_csv(tmp_dir / "overlap_scores.csv", index=False)

    meta = {
        "generated_at": "2026-05-26T00:00:00+00:00",
        "n_concepts": n,
        "embedding_model": "test",
        "embedding_dim": dim,
        "projection_method": "test",
        "is_synthetic": True,
        "version": "0.1.0",
    }
    with open(tmp_dir / "artifact_metadata.json", "w") as f:
        json.dump(meta, f)


def test_load_valid_artifacts():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        make_artifacts(tmp_dir, n=5)
        result = load_all_artifacts(tmp_dir)
        assert "examples" in result
        assert "embeddings" in result
        assert "similarity" in result
        assert "merged" in result
        assert len(result["examples"]) == 5


def test_missing_file_raises_file_not_found():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        make_artifacts(tmp_dir, n=4)
        (tmp_dir / "demo_examples.csv").unlink()
        with pytest.raises(FileNotFoundError, match="export_demo_artifacts"):
            load_all_artifacts(tmp_dir)


def test_embedding_count_mismatch_raises():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        make_artifacts(tmp_dir, n=5)
        bad_emb = np.random.default_rng(0).normal(0, 1, (3, 16)).astype(np.float32)
        np.save(str(tmp_dir / "semantic_embeddings.npy"), bad_emb)
        with pytest.raises(ValueError, match="Embedding count"):
            load_all_artifacts(tmp_dir)


def test_similarity_shape_mismatch_raises():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        make_artifacts(tmp_dir, n=5)
        bad_sim = np.random.default_rng(0).uniform(0, 1, (3, 3)).astype(np.float32)
        np.save(str(tmp_dir / "similarity_semantic.npy"), bad_sim)
        with pytest.raises(ValueError, match="Similarity matrix shape"):
            load_all_artifacts(tmp_dir)


def test_write_artifact_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        write_artifact_metadata(
            artifacts_dir=tmp_dir,
            n_concepts=10,
            embedding_model="all-MiniLM-L6-v2",
            embedding_dim=384,
            projection_method="umap",
            is_synthetic=False,
        )
        meta_path = tmp_dir / "artifact_metadata.json"
        assert meta_path.exists()
        with open(meta_path) as f:
            meta = json.load(f)
        assert meta["n_concepts"] == 10
        assert meta["is_synthetic"] is False
        assert "generated_at" in meta
