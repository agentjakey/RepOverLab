"""
Compute overlap and boundary scores for each example.

overlap_score: fraction of top-k neighbors from a different safety band.
nearest_cross_band_sim: similarity to nearest neighbor in a different band.
sim_to_benign / ambiguous / policy_relevant_sanitized: cosine similarity to
  each reference band's centroid embedding.
boundary_blur_score: normalized entropy of band-centroid similarity distribution.
  High = example sits near multiple bands simultaneously. Low = firmly within
  a single band. This is an exploration heuristic, not a safety classifier.

Prerequisites:
  python scripts/build_embeddings.py
  python scripts/build_similarity.py

Outputs:
  artifacts/overlap_scores.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.embedding import load_embeddings
from src.overlap import (
    compute_overlap_scores,
    compute_nearest_cross_band_sim,
    compute_centroid_sims,
    compute_boundary_blur_score,
    save_overlap_scores,
)


def main() -> None:
    similarity_path = ROOT / "artifacts" / "similarity_semantic.npy"
    embeddings_path = ROOT / "artifacts" / "semantic_embeddings.npy"
    examples_path = ROOT / "artifacts" / "demo_examples.csv"
    out_path = ROOT / "artifacts" / "overlap_scores.csv"

    for p in [similarity_path, embeddings_path, examples_path]:
        if not p.exists():
            raise SystemExit(f"{p} not found. Run the prerequisite scripts first.")

    print(f"Loading similarity matrix from {similarity_path}")
    sim = np.load(str(similarity_path))

    print(f"Loading embeddings from {embeddings_path}")
    embeddings = load_embeddings(embeddings_path)

    examples = pd.read_csv(examples_path)
    ids = examples["id"].tolist()

    # Prefer safety_band column; fall back to category for legacy artifacts.
    if "safety_band" in examples.columns:
        bands = examples["safety_band"].tolist()
    else:
        bands = examples["category"].tolist()

    n = len(ids)
    k = min(10, n - 1)
    print(f"Computing overlap scores for {n} examples (k={k})...")

    overlap_scores = compute_overlap_scores(sim, bands, k=k)
    high_count = int((overlap_scores >= 0.6).sum())
    print(f"  Cross-band overlap: min={overlap_scores.min():.3f} "
          f"max={overlap_scores.max():.3f} mean={overlap_scores.mean():.3f}")
    print(f"  High-overlap (>= 0.6): {high_count}/{n}")

    print("Computing nearest cross-band similarities...")
    cross_band_sim = compute_nearest_cross_band_sim(sim, bands)

    print("Computing centroid similarities (benign, ambiguous, policy_relevant_sanitized)...")
    c_sims = compute_centroid_sims(embeddings, bands)
    for band, arr in c_sims.items():
        print(f"  sim_to_{band}: mean={arr.mean():.3f}")

    print("Computing boundary blur scores...")
    blur = compute_boundary_blur_score(c_sims)
    print(f"  boundary_blur: min={blur.min():.3f} max={blur.max():.3f} mean={blur.mean():.3f}")

    save_overlap_scores(
        ids,
        bands,
        overlap_scores,
        out_path,
        nearest_cross_band_sim=cross_band_sim,
        centroid_sims=c_sims,
        boundary_blur_scores=blur,
    )
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
