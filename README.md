# Representation Overlap Lab

**Why safety boundaries are not always cleanly separable.**

An interactive visual essay about how concepts from different safety categories overlap in
semantic embedding space — and what that means for AI safety systems that use embeddings
to draw lines.

> A map for thinking, not a judge.

---

## What this is

When an AI safety system classifies text, it often does so using embedding similarity.
Sentence embedding models turn text into vectors, and similar texts land near each other.
The problem is that similarity is statistical, not semantic. A clinical question about
medication dosage lands near a question about overdose. A security research description
shares vocabulary with an exploitation technique.

This project makes those neighborhoods visible. It does not argue for loosening safety
standards. It argues for understanding what those standards are geometrically doing —
and where they will struggle.

**It is not a classifier. It is not a moderation system. It is not ground truth.**

---

## What this is not

- Not a safety classifier
- Not a moderation tool
- Not a benchmark
- Not a ground-truth measure of risk
- Not a claim that any concept is "close enough" to warrant restriction or permission

Embedding distance is not moral distance.

---

## Why it matters

Safety categories rarely fail in neat boxes. False positives catch legitimate content that
lives near restricted content. False negatives let through harmful content that adopted
clinical framing. Neither failure mode is fixable by just improving the threshold — both
are consequences of how the representation space is shaped.

---

## Tech stack

| Layer | Tool |
|-------|------|
| Framework | Next.js 14 (App Router, static export) |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Deployment | Vercel |
| Data pipeline | Python (offline only) |
| Embeddings | all-MiniLM-L6-v2 (precomputed) |
| Projection | UMAP → 2D (precomputed) |

No external API required at runtime. No server-side model inference. All artifacts are
precomputed and served as static JSON from `public/data/`.

---

## Local setup

```bash
git clone https://github.com/agentjakey/representation-overlap-lab
cd representation-overlap-lab

# Install dependencies
npm install

# Run development server
npm run dev
# → Open http://localhost:3000
```

---

## Regenerating data artifacts

The JSON files in `public/data/` are precomputed. To regenerate them from the source CSV:

```bash
# 1. Install Python pipeline dependencies
pip install -r archive/requirements.txt

# 2. Run the full artifact pipeline (downloads ~90MB model on first run)
python scripts/export_demo_artifacts.py

# 3. Export artifacts to public/data/
python scripts/export_to_public.py
```

For synthetic demo embeddings (no model download):

```bash
python scripts/export_demo_artifacts.py --synthetic
python scripts/export_to_public.py
```

---

## Vercel deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Build locally first to verify
npm run build

# Deploy preview
vercel

# Deploy to production
vercel --prod
```

No environment variables required. No API keys. No secrets.

The app is fully static — `next build` produces a static export that Vercel serves directly.

---

## Project structure

```
representation-overlap-lab/
  app/
    layout.tsx           Root layout (Next.js App Router)
    page.tsx             Main essay + lab page
    globals.css          Design tokens and base styles
  components/
    Nav.tsx              Fixed top navigation
    Hero.tsx             Title, reading mode toggle
    Section.tsx          Numbered section wrapper
    OverlapMap.tsx        Interactive SVG scatter map
    BoundaryBlur.tsx      Ranked blur score explorer
    ComparePanel.tsx      Pairwise similarity comparison
    MethodCard.tsx        Pipeline step cards
    CareNote.tsx          Highlighted callout boxes
    Footer.tsx            Project footer
  lib/
    types.ts             TypeScript types and metadata constants
  public/
    data/
      examples.json      113 merged examples with coordinates and scores
      neighbors.json     Top-10 neighbors per example
      metadata.json      Artifact generation metadata
  src/                   Python source modules (offline pipeline)
  scripts/               Python pipeline scripts
  data/
    safe_examples_seed.csv  Source dataset (113 hand-reviewed entries)
  archive/               Old Streamlit files (not used in production)
```

---

## Dataset

`data/safe_examples_seed.csv` contains 113 concept descriptions across 10 domains and
five safety bands:

| Band | Description |
|------|-------------|
| Benign | Educational and everyday concepts |
| Capability-Building | Legitimate professional applications that share vocabulary with dual-use areas |
| Ambiguous | Classification depends on intent, which the embedding cannot read |
| Policy-Relevant / Sanitized | Sensitive but genuine research or clinical topics |
| Abstract Placeholder | Names types of excluded content without reproducing them |

Every entry was written and reviewed individually. No entry provides step-by-step
instructions for causing harm.

---

## Content policy

- No actionable synthesis routes, attack instructions, or operational harm guidance
- No exploit code, weaponization details, or material that would provide uplift
- No manipulation scripts, grooming content, or fraud tutorials
- Abstract risk placeholders name categories of restricted content — without reproducing the content

If you believe any entry crossed these lines, open a GitHub issue. The dataset is a plain
CSV file and is easy to audit line by line.

---

## Limitations

**Projection distortion.** The 2D UMAP map loses information. Points that appear close may
be further apart in 384-dimensional space.

**Model bias.** all-MiniLM-L6-v2 encodes statistical patterns from its training corpus,
including biases about language, framing, and domain.

**Non-representative dataset.** 113 illustrative examples — not a sample of any real
query distribution. Do not use as a benchmark or training data.

**Editorial categories.** The five safety bands are editorial judgments, not ground truth.

---

## License

MIT. See `LICENSE`.

This license permits free use, modification, and redistribution. It does not grant
permission to use this project as a safety classifier or to use its dataset as training
data for content moderation systems without independent human review.
