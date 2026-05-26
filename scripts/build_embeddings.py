"""
Embed the example content_text fields using sentence-transformers.
Falls back to TF-IDF + TruncatedSVD if sentence-transformers cannot load.

Prerequisites:
  python scripts/export_demo_artifacts.py   (or build_safe_examples.py)

Outputs:
  artifacts/semantic_embeddings.npy  (float32, shape N x 384)
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.embedding import embed_texts, save_embeddings


def main() -> None:
    examples_path = ROOT / "artifacts" / "demo_examples.csv"
    out_path = ROOT / "artifacts" / "semantic_embeddings.npy"

    if not examples_path.exists():
        raise SystemExit(
            f"{examples_path} not found. Run export_demo_artifacts.py first."
        )

    df = pd.read_csv(examples_path)

    # Prefer content_text (new schema), fall back to description (old schema).
    if "content_text" in df.columns:
        texts = df["content_text"].tolist()
        print(f"Embedding {len(texts)} content_text fields...")
    elif "description" in df.columns:
        texts = df["description"].tolist()
        print(f"Embedding {len(texts)} description fields (legacy schema)...")
    else:
        raise SystemExit("examples CSV has neither 'content_text' nor 'description' column.")

    embeddings, model_used = embed_texts(
        texts,
        model_name="all-MiniLM-L6-v2",
        normalize=True,
        batch_size=32,
        show_progress=True,
    )

    save_embeddings(embeddings, out_path)
    print(f"Model used: {model_used}")
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
