"""
Validate all artifacts for internal consistency.

Checks:
  - All required files are present
  - Row counts are consistent across files
  - Embedding shape matches example count
  - Similarity matrix is symmetric and in [-0.01, 1.01]
  - Coordinate and overlap files have correct IDs
  - Metadata is readable and has required fields
  - No content_text contains forbidden operational-detail patterns
  - Boundary blur columns are present (warns if missing, does not fail)

Run after any pipeline step to catch problems early.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
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
    "id", "title", "content_text", "safety_band", "domain", "framing",
}

VALID_BANDS = {
    "benign",
    "capability_building",
    "ambiguous",
    "policy_relevant_sanitized",
    "abstract_risk_placeholder",
}

# Subset of forbidden patterns from data_schema.py — enough for a quick scan.
FORBIDDEN_PATTERNS = [
    r"\bsynthesis route\b",
    r"\bsynthesis (step|procedure|protocol)\b",
    r"\bexploit (chain|payload|code)\b",
    r"\bpayload delivery\b",
    r"\bpersistence mechanism\b",
    r"\bevasion technique\b",
    r"\bgrooming script\b",
    r"\bmanipulation (script|playbook|sequence)\b",
    r"\bfraud (script|scheme|tutorial)\b",
]

OPTIONAL_OVERLAP_COLUMNS = {
    "nearest_cross_band_sim",
    "sim_to_benign",
    "sim_to_ambiguous",
    "sim_to_policy_relevant_sanitized",
    "boundary_blur_score",
}


def check(condition: bool, message: str, errors: list) -> None:
    if not condition:
        errors.append(f"FAIL: {message}")
    else:
        print(f"  OK  {message}")


def warn(condition: bool, message: str) -> None:
    if not condition:
        print(f"  WARN: {message}")
    else:
        print(f"  OK  {message}")


def main() -> None:
    errors: list[str] = []
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
    check(len(missing_cols) == 0, f"Required columns present (missing: {missing_cols})", errors)
    check(n >= 50, f"At least 50 examples ({n} found)", errors)

    id_col = "id" if "id" in examples.columns else "example_id"
    check(examples[id_col].nunique() == n, "No duplicate IDs", errors)

    if "safety_band" in examples.columns:
        unknown_bands = set(examples["safety_band"].unique()) - VALID_BANDS
        check(len(unknown_bands) == 0, f"All safety bands valid (unknown: {unknown_bands})", errors)

    print("\n-- Content safety scan --")
    violation_count = 0
    if "content_text" in examples.columns:
        for _, row in examples.iterrows():
            text = row["content_text"]
            for pattern in FORBIDDEN_PATTERNS:
                if re.search(pattern, str(text), re.IGNORECASE):
                    errors.append(
                        f"FAIL: Forbidden pattern '{pattern}' in {row.get(id_col, '?')}"
                    )
                    violation_count += 1
    check(violation_count == 0, f"No forbidden content patterns found", errors)

    print("\n-- Embeddings --")
    embeddings = np.load(str(ARTIFACTS / "semantic_embeddings.npy"))
    check(embeddings.ndim == 2, f"Embeddings 2D (shape: {embeddings.shape})", errors)
    check(embeddings.shape[0] == n, f"Embedding count == example count ({embeddings.shape[0]} == {n})", errors)
    check(embeddings.dtype == np.float32, "Embeddings dtype is float32", errors)

    print("\n-- Similarity matrix --")
    sim = np.load(str(ARTIFACTS / "similarity_semantic.npy"))
    check(sim.shape == (n, n), f"Similarity matrix shape {sim.shape} == ({n}, {n})", errors)
    check(float(sim.min()) >= -0.01, f"Similarity min >= 0 ({sim.min():.4f})", errors)
    check(float(sim.max()) <= 1.01, f"Similarity max <= 1 ({sim.max():.4f})", errors)
    sym_err = float(np.max(np.abs(sim - sim.T)))
    check(sym_err < 1e-4, f"Similarity symmetric (max asymmetry: {sym_err:.6f})", errors)

    print("\n-- Coordinates --")
    coords = pd.read_csv(ARTIFACTS / "map_coordinates.csv")
    check(len(coords) == n, f"Coordinate count == example count ({len(coords)} == {n})", errors)
    example_ids = set(examples[id_col].astype(str))
    coord_ids = set(coords["id"].astype(str))
    check(coord_ids == example_ids, "Coordinate IDs match example IDs", errors)

    print("\n-- Overlap scores --")
    overlap = pd.read_csv(ARTIFACTS / "overlap_scores.csv")
    check(len(overlap) == n, f"Overlap count == example count ({len(overlap)} == {n})", errors)
    overlap_ids = set(overlap["id"].astype(str))
    check(overlap_ids == example_ids, "Overlap IDs match example IDs", errors)
    check(
        overlap["overlap_score"].between(0, 1).all(),
        "All overlap scores in [0, 1]",
        errors,
    )
    for col in OPTIONAL_OVERLAP_COLUMNS:
        warn(col in overlap.columns, f"Optional column '{col}' present in overlap CSV")
    if "boundary_blur_score" in overlap.columns:
        check(
            overlap["boundary_blur_score"].between(0, 1).all(),
            "All boundary_blur_score values in [0, 1]",
            errors,
        )

    print("\n-- Metadata --")
    with open(ARTIFACTS / "artifact_metadata.json", encoding="utf-8") as f:
        meta = json.load(f)
    for field in ["generated_at", "n_concepts", "embedding_model", "is_synthetic", "projection_method"]:
        check(field in meta, f"Metadata has field '{field}'", errors)
    check(meta.get("n_concepts") == n, f"Metadata n_concepts == {n}", errors)

    print("\n" + "=" * 50)
    if errors:
        print(f"\nValidation FAILED with {len(errors)} error(s):\n")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print(f"\nAll checks passed. {n} examples, artifacts consistent.")


if __name__ == "__main__":
    main()
