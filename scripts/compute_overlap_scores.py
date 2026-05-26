"""
Compute overlap scores for each concept.

The overlap score is the fraction of a concept's top-10 nearest neighbors
that belong to a different category. A high score means the concept sits at
a category boundary.

Prerequisites:
  python scripts/build_similarity.py

Outputs:
  artifacts/overlap_scores.csv  (columns: id, category, overlap_score, is_high_overlap)
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.overlap import compute_overlap_scores, save_overlap_scores


def main() -> None:
    similarity_path = ROOT / "artifacts" / "similarity_semantic.npy"
    examples_path = ROOT / "artifacts" / "demo_examples.csv"
    out_path = ROOT / "artifacts" / "overlap_scores.csv"

    if not similarity_path.exists():
        raise SystemExit(f"{similarity_path} not found. Run build_similarity.py first.")

    print(f"Loading similarity matrix from {similarity_path}")
    sim = np.load(str(similarity_path))

    examples = pd.read_csv(examples_path)
    ids = examples["id"].tolist()
    categories = examples["category"].tolist()

    print(f"Computing overlap scores for {len(ids)} concepts (k=10)...")
    scores = compute_overlap_scores(sim, categories, k=10)

    high_overlap_count = int((scores >= 0.6).sum())
    print(f"Overlap score stats:")
    print(f"  min={scores.min():.3f}  max={scores.max():.3f}  mean={scores.mean():.3f}")
    print(f"  High-overlap concepts (score >= 0.6): {high_overlap_count}")

    save_overlap_scores(ids, categories, scores, out_path)
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
