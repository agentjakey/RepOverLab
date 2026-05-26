"""
Load the seed CSV, validate every entry against SafeExample schema, and write a
clean processed copy to artifacts/demo_examples.csv.

This is the first step in the pipeline. Run before export_demo_artifacts.py.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.data_schema import SafeExample, SafeExampleDataset, SafetyBand, Domain, Framing


def load_and_validate(seed_path: Path) -> SafeExampleDataset:
    df = pd.read_csv(seed_path, dtype=str).fillna("")
    entries = []
    errors = []

    for i, row in df.iterrows():
        try:
            entry = SafeExample(
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
            entries.append(entry)
        except Exception as e:
            errors.append(f"Row {i} (id={row.get('example_id', '?')}): {e}")

    if errors:
        for err in errors:
            print(f"VALIDATION ERROR: {err}")
        raise SystemExit(f"{len(errors)} validation error(s) found. Fix before proceeding.")

    dataset = SafeExampleDataset(entries=entries)

    ids = dataset.ids()
    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate IDs found in dataset.")

    band_counts = dataset.band_counts()
    print("Safety band distribution:")
    for band, count in sorted(band_counts.items()):
        pct = 100 * count / len(entries)
        flag = " [WARN: > 40%]" if pct > 40 else ""
        print(f"  {band}: {count} ({pct:.1f}%){flag}")

    return dataset


def write_examples(dataset: SafeExampleDataset, out_path: Path) -> None:
    rows = []
    for e in dataset.entries:
        rows.append({
            "example_id": e.example_id,
            "id": e.example_id,
            "title": e.title,
            "content_text": e.content_text,
            "domain": e.domain.value,
            "topic": e.topic,
            "safety_band": e.safety_band.value,
            "framing": e.framing.value,
            "safe_summary": e.safe_summary,
            "why_interesting": e.why_interesting,
            "allowed_for_demo": e.allowed_for_demo,
            "notes": e.notes or "",
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
