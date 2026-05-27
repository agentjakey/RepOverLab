"""
Export precomputed artifacts to public/data/ for the Next.js app.

Run this after scripts/export_demo_artifacts.py:
    python scripts/export_to_public.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent.parent
ARTIFACTS = ROOT / "artifacts"
PUBLIC = ROOT / "public" / "data"


def main() -> None:
    PUBLIC.mkdir(parents=True, exist_ok=True)

    # Verify artifacts exist
    required = [
        "demo_examples.csv",
        "map_coordinates.csv",
        "overlap_scores.csv",
        "similarity_semantic.npy",
        "artifact_metadata.json",
    ]
    missing = [f for f in required if not (ARTIFACTS / f).exists()]
    if missing:
        print(f"ERROR: missing artifacts: {missing}")
        print("Run: python scripts/export_demo_artifacts.py")
        sys.exit(1)

    df_ex = pd.read_csv(ARTIFACTS / "demo_examples.csv")
    df_coords = pd.read_csv(ARTIFACTS / "map_coordinates.csv")
    df_overlap = pd.read_csv(ARTIFACTS / "overlap_scores.csv")

    # Merge
    merged = (
        df_ex.merge(df_coords, on="id")
        .merge(df_overlap, on="id", suffixes=("", "_ov"))
    )

    keep = [
        "id", "title", "topic", "content_text", "domain", "safety_band", "framing",
        "safe_summary", "why_interesting", "x", "y", "overlap_score", "is_high_overlap",
        "nearest_cross_band_sim", "sim_to_benign", "sim_to_ambiguous",
        "sim_to_policy_relevant_sanitized", "boundary_blur_score",
    ]
    merged = merged[[c for c in keep if c in merged.columns]].fillna("")

    for col in ["x", "y", "overlap_score", "nearest_cross_band_sim",
                "sim_to_benign", "sim_to_ambiguous",
                "sim_to_policy_relevant_sanitized", "boundary_blur_score"]:
        if col in merged.columns:
            merged[col] = merged[col].round(4)

    if "is_high_overlap" in merged.columns:
        merged["is_high_overlap"] = merged["is_high_overlap"].astype(int)

    records = merged.to_dict(orient="records")
    with open(PUBLIC / "examples.json", "w", encoding="utf-8") as f:
        json.dump(records, f, separators=(",", ":"))
    print(f"examples.json: {len(records)} records, {(PUBLIC / 'examples.json').stat().st_size // 1024} KB")

    # Neighbors
    sim = np.load(str(ARTIFACTS / "similarity_semantic.npy"))
    ids = df_ex["id"].tolist()
    id_to_band = dict(zip(df_ex["id"], df_ex["safety_band"]))
    id_to_topic = dict(zip(df_ex["id"], df_ex["topic"]))

    neighbors: dict[str, list[dict]] = {}
    for i, eid in enumerate(ids):
        row = sim[i].copy()
        row[i] = -1.0
        top10_idx = row.argsort()[::-1][:10]
        neighbors[eid] = [
            {
                "id": ids[int(j)],
                "sim": round(float(sim[i, j]), 4),
                "band": id_to_band[ids[int(j)]],
                "topic": id_to_topic[ids[int(j)]],
            }
            for j in top10_idx
        ]

    with open(PUBLIC / "neighbors.json", "w", encoding="utf-8") as f:
        json.dump(neighbors, f, separators=(",", ":"))
    print(f"neighbors.json: {(PUBLIC / 'neighbors.json').stat().st_size // 1024} KB")

    # Metadata
    with open(ARTIFACTS / "artifact_metadata.json", encoding="utf-8") as f:
        meta = json.load(f)
    with open(PUBLIC / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print("metadata.json written")

    print("\nDone. Run: npm run build")


if __name__ == "__main__":
    main()
