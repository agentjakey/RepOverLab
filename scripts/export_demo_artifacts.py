"""
Full pipeline: generate all demo artifacts from the seed CSV.

By default, this uses SYNTHETIC embeddings so it runs without downloading
the sentence-transformers model. Pass --use-model to use real embeddings.

Usage:
  python scripts/export_demo_artifacts.py              # synthetic (fast, no download)
  python scripts/export_demo_artifacts.py --use-model  # real embeddings (slow, 90MB download)

Outputs in artifacts/:
  demo_examples.csv
  semantic_embeddings.npy
  similarity_semantic.npy
  map_coordinates.csv
  overlap_scores.csv
  artifact_metadata.json
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.data_schema import SafeExample, SafetyBand, Domain, Framing
from src.overlap import compute_overlap_scores, save_overlap_scores
from src.projection import save_coordinates
from src.similarity import cosine_similarity_matrix
from src.artifact_io import write_artifact_metadata
from src.demo_data import generate_synthetic_embeddings, generate_synthetic_2d_coords


def load_seed(seed_path: Path) -> pd.DataFrame:
    df = pd.read_csv(seed_path, dtype=str).fillna("")
    errors = []
    valid_rows = []
    for i, row in df.iterrows():
        try:
            SafeExample(
                example_id=row["example_id"].strip(),
                title=row["title"].strip(),
                content_text=row["content_text"].strip(),
                domain=Domain(row["domain"].strip()),
                topic=row["topic"].strip(),
                safety_band=SafetyBand(row["safety_band"].strip()),
                framing=Framing(row["framing"].strip()),
                safe_summary=row["safe_summary"].strip(),
                why_interesting=row["why_interesting"].strip(),
                allowed_for_demo=row["allowed_for_demo"].strip().lower() in ("true", "1", "yes"),
                notes=row.get("notes", "").strip(),
            )
            valid_rows.append({
                "example_id": row["example_id"].strip(),
                "id": row["example_id"].strip(),
                "title": row["title"].strip(),
                "content_text": row["content_text"].strip(),
                "domain": row["domain"].strip(),
                "topic": row["topic"].strip(),
                "safety_band": row["safety_band"].strip(),
                "framing": row["framing"].strip(),
                "safe_summary": row["safe_summary"].strip(),
                "why_interesting": row["why_interesting"].strip(),
                "allowed_for_demo": row["allowed_for_demo"].strip().lower() in ("true", "1", "yes"),
                "notes": row.get("notes", "").strip(),
            })
        except Exception as e:
            errors.append(f"Row {i}: {e}")
    if errors:
        for err in errors:
            print(f"  VALIDATION ERROR: {err}")
        raise SystemExit(f"{len(errors)} validation errors. Fix before proceeding.")
    return pd.DataFrame(valid_rows)


def run_real_embeddings(texts: list[str]) -> np.ndarray:
    from src.embedding import embed_texts
    print("  Downloading / loading all-MiniLM-L6-v2...")
    embeddings = embed_texts(
        texts,
        model_name="all-MiniLM-L6-v2",
        normalize=True,
        batch_size=32,
        show_progress=True,
    )
    return embeddings


def run_umap_projection(embeddings: np.ndarray) -> np.ndarray:
    from src.projection import compute_umap
    print("  Running UMAP...")
    return compute_umap(embeddings, n_neighbors=15, min_dist=0.1, metric="cosine", random_state=42)


def main(use_model: bool) -> None:
    artifacts_dir = ROOT / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    seed_path = ROOT / "data" / "safe_examples_seed.csv"
    print(f"\n[1/6] Loading and validating seed data from {seed_path}")
    df = load_seed(seed_path)
    n = len(df)
    safety_bands = df["safety_band"].tolist()
    texts = df["content_text"].tolist()
    ids = df["id"].tolist()
    print(f"  {n} examples loaded and validated.")

    examples_path = artifacts_dir / "demo_examples.csv"
    df.to_csv(examples_path, index=False)
    print(f"  Saved {examples_path.name}")

    embeddings_path = artifacts_dir / "semantic_embeddings.npy"
    is_synthetic = not use_model

    if use_model:
        print(f"\n[2/6] Generating real embeddings with sentence-transformers")
        embeddings = run_real_embeddings(texts)
    else:
        print(f"\n[2/6] Generating synthetic demo embeddings (use --use-model for real)")
        embeddings = generate_synthetic_embeddings(safety_bands)

    np.save(str(embeddings_path), embeddings.astype(np.float32))
    print(f"  Embeddings shape: {embeddings.shape} -> {embeddings_path.name}")

    similarity_path = artifacts_dir / "similarity_semantic.npy"
    print(f"\n[3/6] Computing cosine similarity matrix")
    sim = cosine_similarity_matrix(embeddings)
    np.save(str(similarity_path), sim.astype(np.float32))
    print(f"  Similarity matrix: {sim.shape} -> {similarity_path.name}")

    coordinates_path = artifacts_dir / "map_coordinates.csv"
    print(f"\n[4/6] Computing 2D projection")
    if use_model:
        coords = run_umap_projection(embeddings)
    else:
        coords = generate_synthetic_2d_coords(safety_bands)
    save_coordinates(ids, coords, coordinates_path)
    print(f"  Coordinates: {coords.shape} -> {coordinates_path.name}")

    overlap_path = artifacts_dir / "overlap_scores.csv"
    print(f"\n[5/6] Computing overlap scores")
    scores = compute_overlap_scores(sim, safety_bands, k=min(10, n - 1))
    save_overlap_scores(ids, safety_bands, scores, overlap_path)
    high_count = int((scores >= 0.6).sum())
    print(f"  {high_count}/{n} examples flagged as high-overlap -> {overlap_path.name}")

    print(f"\n[6/6] Writing artifact metadata")
    write_artifact_metadata(
        artifacts_dir=artifacts_dir,
        n_concepts=n,
        embedding_model="all-MiniLM-L6-v2" if use_model else "synthetic",
        embedding_dim=int(embeddings.shape[1]),
        projection_method="umap" if use_model else "synthetic-2d",
        is_synthetic=is_synthetic,
    )
    print(f"  artifact_metadata.json written.")

    print(f"\nAll artifacts written to {artifacts_dir}/")
    print("Run 'streamlit run app.py' to launch the app.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use-model",
        action="store_true",
        help="Use real sentence-transformers embeddings (requires internet on first run).",
    )
    args = parser.parse_args()
    main(use_model=args.use_model)
