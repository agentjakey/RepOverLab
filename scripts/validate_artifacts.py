"""
Validate all artifacts for internal consistency.

Checks:
  - All required files are present
  - Row counts are consistent across files
  - Embedding shape matches concept count
  - Similarity matrix is symmetric and in [0, 1]
  - Coordinate and overlap files have correct IDs
  - Metadata is readable and has required fields
  - No description in examples contains procedural harm patterns

Run this after any pipeline step to catch problems early.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent.parent
ARTIFACTS = ROOT / "artifacts"

REQUIRED_FILES = [
    "demo_examples.csv",
    "semantic_embeddings.npy",
    "similarity_semantic.npy",
    "map_coordinates.csv",
    "overlap_scores.csv",
    "artifact_metadata.json",
]

REQUIRED_EXAMPLE_COLUMNS = {
    "id", "name", "short_name", "description", "category", "tension_type"
}

FORBIDDEN_PATTERNS = [
    r"\bstep[- ]by[- ]step\s+(instructions?|guide|method)\b",
    r"\b(mix|combine|add)\s+\d+\s*(ml|g|oz|grams?|mg)\b",
    r"\b(synthesis route|reaction pathway)\b",
]

VALID_CATEGORIES = {
    "clearly_benign",
    "dual_use",
    "context_dependent",
    "sensitive_legitimate",
    "out_of_scope_abstract",
}


def check(condition: bool, message: str, errors: list) -> None:
    if not condition:
        errors.append(f"FAIL: {message}")
    else:
        print(f"  OK  {message}")


def main() -> None:
    errors = []
    print("Validating artifacts...\n")

    print("-- File presence --")
    for fname in REQUIRED_FILES:
        path = ARTIFACTS / fname
        check(path.exists(), f"{fname} exists", errors)

    if errors:
        for e in errors:
            print(e)
        raise SystemExit("Missing required files. Aborting further checks.")

    print("\n-- Example dataset --")
    examples = pd.read_csv(ARTIFACTS / "demo_examples.csv")
    n = len(examples)
    missing_cols = REQUIRED_EXAMPLE_COLUMNS - set(examples.columns)
    check(len(missing_cols) == 0, f"All required columns present (missing: {missing_cols})", errors)
    check(n >= 50, f"At least 50 concepts ({n} found)", errors)
    check(examples["id"].nunique() == n, "No duplicate IDs", errors)
    unknown_cats = set(examples["category"].unique()) - VALID_CATEGORIES
    check(len(unknown_cats) == 0, f"All categories valid (unknown: {unknown_cats})", errors)

    print("\n-- Content safety check --")
    violation_count = 0
    for _, row in examples.iterrows():
        desc = row["description"]
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, desc, re.IGNORECASE):
                errors.append(
                    f"FAIL: Content pattern '{pattern}' in {row['id']}: {desc[:80]}"
                )
                violation_count += 1
    check(violation_count == 0, f"No forbidden content patterns found", errors)

    print("\n-- Embeddings --")
    embeddings = np.load(str(ARTIFACTS / "semantic_embeddings.npy"))
    check(embeddings.ndim == 2, f"Embeddings is 2D (shape: {embeddings.shape})", errors)
    check(embeddings.shape[0] == n, f"Embedding count matches examples ({embeddings.shape[0]} == {n})", errors)
    check(embeddings.dtype == np.float32, f"Embeddings dtype is float32", errors)

    print("\n-- Similarity matrix --")
    sim = np.load(str(ARTIFACTS / "similarity_semantic.npy"))
    check(sim.shape == (n, n), f"Similarity matrix shape ({sim.shape} == ({n}, {n}))", errors)
    check(float(sim.min()) >= -0.01, f"Similarity min >= 0 ({sim.min():.4f})", errors)
    check(float(sim.max()) <= 1.01, f"Similarity max <= 1 ({sim.max():.4f})", errors)
    sym_error = float(np.max(np.abs(sim - sim.T)))
    check(sym_error < 1e-4, f"Similarity matrix is symmetric (max asymmetry: {sym_error:.6f})", errors)

    print("\n-- Coordinates --")
    coords = pd.read_csv(ARTIFACTS / "map_coordinates.csv")
    check(len(coords) == n, f"Coordinate count matches examples ({len(coords)} == {n})", errors)
    check(set(coords["id"]) == set(examples["id"]), "Coordinate IDs match example IDs", errors)

    print("\n-- Overlap scores --")
    overlap = pd.read_csv(ARTIFACTS / "overlap_scores.csv")
    check(len(overlap) == n, f"Overlap count matches examples ({len(overlap)} == {n})", errors)
    check(set(overlap["id"]) == set(examples["id"]), "Overlap IDs match example IDs", errors)
    check(
        overlap["overlap_score"].between(0, 1).all(),
        f"All overlap scores in [0, 1]",
        errors,
    )

    print("\n-- Metadata --")
    with open(ARTIFACTS / "artifact_metadata.json", encoding="utf-8") as f:
        meta = json.load(f)
    for field in ["generated_at", "n_concepts", "embedding_model", "is_synthetic"]:
        check(field in meta, f"Metadata has field '{field}'", errors)
    check(meta.get("n_concepts") == n, f"Metadata n_concepts == {n}", errors)

    print("\n" + "=" * 50)
    if errors:
        print(f"\nValidation FAILED with {len(errors)} error(s):\n")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print(f"\nAll checks passed. {n} concepts, artifacts consistent.")


if __name__ == "__main__":
    main()
