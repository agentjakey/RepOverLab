"""
Load the seed CSV, validate every entry against the schema, and write a clean
processed copy to artifacts/demo_examples.csv.

This is the first step in the pipeline. Run it before build_embeddings.py.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.data_schema import Category, ConceptDataset, ConceptEntry, TensionType


def load_and_validate(seed_path: Path) -> ConceptDataset:
    df = pd.read_csv(seed_path, dtype=str).fillna("")
    entries = []
    errors = []

    for i, row in df.iterrows():
        try:
            entry = ConceptEntry(
                id=row["id"].strip(),
                name=row["name"].strip(),
                short_name=row["short_name"].strip(),
                description=row["description"].strip(),
                category=Category(row["category"].strip()),
                tension_type=TensionType(row["tension_type"].strip()),
                legitimate_use_note=row.get("legitimate_use_note", "").strip(),
            )
            entries.append(entry)
        except Exception as e:
            errors.append(f"Row {i} (id={row.get('id', '?')}): {e}")

    if errors:
        for err in errors:
            print(f"VALIDATION ERROR: {err}")
        raise SystemExit(f"{len(errors)} validation error(s) found. Fix before proceeding.")

    dataset = ConceptDataset(entries=entries)

    ids = dataset.ids()
    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate IDs found in dataset.")

    cat_counts = dataset.category_counts()
    print("Category distribution:")
    for cat, count in sorted(cat_counts.items()):
        pct = 100 * count / len(entries)
        flag = " [WARN: > 40%]" if pct > 40 else ""
        print(f"  {cat}: {count} ({pct:.1f}%){flag}")

    return dataset


def write_examples(dataset: ConceptDataset, out_path: Path) -> None:
    rows = []
    for e in dataset.entries:
        rows.append({
            "id": e.id,
            "name": e.name,
            "short_name": e.short_name,
            "description": e.description,
            "category": e.category.value,
            "tension_type": e.tension_type.value,
            "legitimate_use_note": e.legitimate_use_note or "",
        })
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print(f"Wrote {len(rows)} validated entries to {out_path}")


def main() -> None:
    seed_path = ROOT / "data" / "safe_examples_seed.csv"
    out_path = ROOT / "artifacts" / "demo_examples.csv"

    print(f"Loading seed data from {seed_path}")
    dataset = load_and_validate(seed_path)
    write_examples(dataset, out_path)
    print("Done.")


if __name__ == "__main__":
    main()
