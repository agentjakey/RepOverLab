# artifacts/

This directory contains precomputed files used by the Streamlit app at runtime.
The app loads these files directly and performs no embedding or model inference.

## Files

| File | Description |
|------|-------------|
| demo_examples.csv | Validated concept dataset (copy of seed CSV, post-validation). |
| semantic_embeddings.npy | float32 array, shape (N, 384). One row per concept. |
| similarity_semantic.npy | float32 array, shape (N, N). Pairwise cosine similarity. |
| map_coordinates.csv | 2D UMAP projection coordinates. Columns: id, x, y. |
| overlap_scores.csv | Per-concept overlap scores. Columns: id, category, overlap_score, is_high_overlap. |
| artifact_metadata.json | Build metadata: timestamp, model name, whether embeddings are synthetic. |

## Generating artifacts

Run this command from the project root to generate all artifacts at once:

    python scripts/export_demo_artifacts.py

By default, this uses synthetic embeddings (no model download, runs immediately).

To use real sentence-transformer embeddings:

    python scripts/export_demo_artifacts.py --use-model

This requires an internet connection on the first run and downloads approximately 90 MB.

## Validating artifacts

    python scripts/validate_artifacts.py

## Why these files are committed

The app is designed to work immediately after cloning, without downloading a model.
The artifacts are small enough to commit (< 2 MB for the default synthetic version).
If you use real embeddings, the .npy files will be larger (approximately 150-200 KB
for 95 concepts at 384 dimensions).

## Synthetic vs. real embeddings

The metadata file records whether embeddings are synthetic (`is_synthetic: true`).
The app displays a banner when running on synthetic data so users know what they
are looking at. Synthetic embeddings preserve cluster structure but are not
semantically meaningful. For research use, run with `--use-model`.
