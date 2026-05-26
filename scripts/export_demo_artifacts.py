"""
Full pipeline: validate seed CSV, embed, compute similarity, project to 2D,
compute overlap and boundary scores, write artifact metadata.

By default, uses real sentence-transformers embeddings (all-MiniLM-L6-v2),
falling back to TF-IDF + TruncatedSVD if the model cannot be loaded.
Pass --synthetic to skip embedding entirely and use structured synthetic vectors.

Usage:
  python scripts/export_demo_artifacts.py              # real embeddings (or TF-IDF fallback)
  python scripts/export_demo_artifacts.py --synthetic  # synthetic, no model needed

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
from src.overlap import (
    compute_overlap_scores,
    compute_nearest_cross_band_sim,
    compute_centroid_sims,
    compute_boundary_blur_score,
    save_overlap_scores,
)
from src.projection import compute_projection, save_coordinates
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


def run_embeddings(texts: list[str]) -> tuple[np.ndarray, str]:
    from src.embedding import embed_texts
    return embed_texts(
        texts,
        model_name="all-MiniLM-L6-v2",
        normalize=True,
        batch_size=32,
        show_progress=True,
    )


def main(synthetic: bool) -> None:
    artifacts_dir = ROOT / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    seed_path = ROOT / "data" / "safe_examples_seed.csv"
    print(f"\n[1/6] Loading and validating seed data from {seed_path}")
    df = load_seed(seed_path)
    n = len(df)
    bands = df["safety_band"].tolist()
    texts = df["content_text"].tolist()
    ids = df["id"].tolist()
    print(f"  {n} examples loaded and validated.")

    examples_path = artifacts_dir / "demo_examples.csv"
    df.to_csv(examples_path, index=False)
    print(f"  Saved {examples_path.name}")

    embeddings_path = artifacts_dir / "semantic_embeddings.npy"

    if synthetic:
        print(f"\n[2/6] Generating synthetic embeddings (--synthetic mode)")
        embeddings = generate_synthetic_embeddings(bands)
        model_used = "synthetic"
    else:
        print(f"\n[2/6] Embedding content_text with sentence-transformers (TF-IDF fallback)")
        embeddings, model_used = run_embeddings(texts)

    np.save(str(embeddings_path), embeddings.astype(np.float32))
    print(f"  Model: {model_used}  |  Shape: {embeddings.shape} -> {embeddings_path.name}")

    similarity_path = artifacts_dir / "similarity_semantic.npy"
    print(f"\n[3/6] Computing cosine similarity matrix")
    sim = cosine_similarity_matrix(embeddings)
    np.save(str(similarity_path), sim.astype(np.float32))
    print(f"  Similarity matrix: {sim.shape} -> {similarity_path.name}")

    coordinates_path = artifacts_dir / "map_coordinates.csv"
    print(f"\n[4/6] Computing 2D projection")
    if synthetic:
        coords = generate_synthetic_2d_coords(bands)
        projection_method = "synthetic-2d"
    else:
        coords, projection_method = compute_projection(
            embeddings, n_neighbors=15, min_dist=0.1, metric="cosine", random_state=42
        )
    save_coordinates(ids, coords, coordinates_path)
    print(f"  Method: {projection_method}  |  {coords.shape} -> {coordinates_path.name}")

    overlap_path = artifacts_dir / "overlap_scores.csv"
    print(f"\n[5/6] Computing overlap and boundary scores")
    k = min(10, n - 1)
    overlap_scores = compute_overlap_scores(sim, bands, k=k)
    cross_band_sim = compute_nearest_cross_band_sim(sim, bands)
    c_sims = compute_centroid_sims(embeddings, bands)
    blur = compute_boundary_blur_score(c_sims)
    high_count = int((overlap_scores >= 0.6).sum())
    print(f"  High-overlap (>= 0.6): {high_count}/{n}")
    print(f"  boundary_blur: mean={blur.mean():.3f}  max={blur.max():.3f}")
    save_overlap_scores(
        ids,
        bands,
        overlap_scores,
        overlap_path,
        nearest_cross_band_sim=cross_band_sim,
        centroid_sims=c_sims,
        boundary_blur_scores=blur,
    )
    print(f"  Saved {overlap_path.name}")

    print(f"\n[6/6] Writing artifact metadata")
    write_artifact_metadata(
        artifacts_dir=artifacts_dir,
        n_concepts=n,
        embedding_model=model_used,
        embedding_dim=int(embeddings.shape[1]),
        projection_method=projection_method,
        is_synthetic=synthetic,
    )
    print(f"  artifact_metadata.json written.")

    print(f"\nAll artifacts written to {artifacts_dir}/")
    print("Run 'python scripts/validate_artifacts.py' to verify.")
    print("Run 'streamlit run app.py' to launch the app.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="Use structured synthetic embeddings instead of sentence-transformers.",
    )
    args = parser.parse_args()
    main(synthetic=args.synthetic)
