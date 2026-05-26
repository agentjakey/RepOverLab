# data/

This directory contains the primary human-curated concept dataset.

## safe_examples_seed.csv

The source dataset for Representation Overlap Lab. Every entry was written and reviewed
by a human. The dataset is designed to illustrate why safety boundaries in semantic
embedding space are hard to draw cleanly - not to provide harmful information.

### Schema

| Column | Type | Description |
|--------|------|-------------|
| id | string | Unique identifier. Format: two uppercase letters + three digits (e.g. CB001). |
| name | string | Full concept name (up to 120 characters). |
| short_name | string | Brief display label (2-4 words). |
| description | string | 1-3 sentence explanation of the concept (max 600 characters). |
| category | enum | One of five categories (see below). |
| tension_type | enum | The mechanism of boundary ambiguity, or "none" for clearly benign concepts. |
| legitimate_use_note | string | For dual-use and context-dependent entries, a statement of the legitimate use case. |

### Categories

- **clearly_benign** - Educational, professional, or everyday content with no plausible path to harm.
- **dual_use** - Concepts with direct legitimate uses that could theoretically support harm if misapplied.
- **context_dependent** - Classification depends entirely on who is asking and why. The embedding cannot read intent.
- **sensitive_legitimate** - Uncomfortable topics with genuine research, clinical, or policy applications.
- **out_of_scope_abstract** - Names types of excluded content without reproducing it. Present to show the boundary exists.

### Tension types

- **none** - Concept sits clearly within a single category.
- **context_resolves** - Benign or harmful depending on context and intent.
- **domain_lens** - Same facts appear in legitimate and harmful contexts with different framing.
- **protective_vs_enabling** - Protective information lives near enabling information.
- **abstraction_gap** - Abstract description of a harm category near legitimate educational content.
- **creative_cover** - Fiction or hypothetical framing using sensitive-neighborhood language.

### What is not in this dataset

No entry provides:
- Step-by-step instructions for causing harm
- Specific quantities, procedures, or methods for harmful synthesis
- Operational detail for illegal activity
- Personally identifying information about any individual

The "out_of_scope_abstract" category names types of excluded content. The entries
describe what the category is and why it is not reproduced - they are not examples of it.

### Adding entries

If you want to add entries, validate them with:

    python scripts/build_safe_examples.py

Then regenerate artifacts:

    python scripts/export_demo_artifacts.py
