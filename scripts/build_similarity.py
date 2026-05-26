"""
Compute the pairwise cosine similarity matrix from precomputed embeddings.

Prerequisites:
  python scripts/build_embeddings.py

Outputs:
  artifacts/similarity_semantic.npy  (float32, shape N x N)
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.embedding import load_embeddings
from src.similarity import cosine_similarity_matrix


def main() -> None:
    embeddings_path = ROOT / "artifacts" / "semantic_embeddings.npy"
    out_path = ROOT / "artifacts" / "similarity_semantic.npy"

    if not embeddings_path.exists():
        raise SystemExit(
            f"{embeddings_path} not found. Run build_embeddings.py first."
        )

    print(f"Loading embeddings from {embeddings_path}")
    embeddings = load_embeddings(embeddings_path)
    print(f"Shape: {embeddings.shape}")

    print("Computing cosine similarity matrix...")
    sim = cosine_similarity_matrix(embeddings)

    print(f"Similarity matrix shape: {sim.shape}")
    print(f"  min={sim.min():.4f}  max={sim.max():.4f}  mean={sim.mean():.4f}")

    np.save(str(out_path), sim.astype(np.float32))
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
