"""
Project embeddings to 2D using UMAP for the interactive map.

Prerequisites:
  python scripts/build_embeddings.py

Outputs:
  artifacts/map_coordinates.csv  (columns: id, x, y)
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.embedding import load_embeddings
from src.projection import compute_umap, save_coordinates


def main() -> None:
    embeddings_path = ROOT / "artifacts" / "semantic_embeddings.npy"
    examples_path = ROOT / "artifacts" / "demo_examples.csv"
    out_path = ROOT / "artifacts" / "map_coordinates.csv"

    if not embeddings_path.exists():
        raise SystemExit(f"{embeddings_path} not found. Run build_embeddings.py first.")

    print(f"Loading embeddings from {embeddings_path}")
    embeddings = load_embeddings(embeddings_path)

    examples = pd.read_csv(examples_path)
    ids = examples["id"].tolist()

    print(f"Running UMAP on {len(ids)} concepts (n_neighbors=15, min_dist=0.1)...")
    coords = compute_umap(
        embeddings,
        n_neighbors=15,
        min_dist=0.1,
        metric="cosine",
        n_components=2,
        random_state=42,
    )

    save_coordinates(ids, coords, out_path)
    print(f"Saved coordinates to {out_path}")
    print(f"  x range: [{coords[:, 0].min():.3f}, {coords[:, 0].max():.3f}]")
    print(f"  y range: [{coords[:, 1].min():.3f}, {coords[:, 1].max():.3f}]")


if __name__ == "__main__":
    main()
