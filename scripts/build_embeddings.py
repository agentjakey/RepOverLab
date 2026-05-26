"""
Embed the concept descriptions using sentence-transformers.

Prerequisites:
  python scripts/build_safe_examples.py

Outputs:
  artifacts/semantic_embeddings.npy  (float32, shape N x 384)

This script downloads the model on first run and caches it locally.
It is not called at app runtime. The app loads the precomputed file.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.embedding import embed_texts, save_embeddings


def main() -> None:
    examples_path = ROOT / "artifacts" / "demo_examples.csv"
    out_path = ROOT / "artifacts" / "semantic_embeddings.npy"

    if not examples_path.exists():
        raise SystemExit(
            f"{examples_path} not found. Run build_safe_examples.py first."
        )

    df = pd.read_csv(examples_path)
    texts = df["description"].tolist()
    print(f"Embedding {len(texts)} descriptions...")

    embeddings = embed_texts(
        texts,
        model_name="all-MiniLM-L6-v2",
        normalize=True,
        batch_size=32,
        show_progress=True,
    )

    save_embeddings(embeddings, out_path)
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
