# Representation Overlap Lab

**Why safety boundaries are not always cleanly separable.**

An interactive AI safety education project that visualizes how benign, ambiguous,
and risk-relevant concepts overlap in semantic embedding space. Built as a Streamlit
application with precomputed local artifacts - no API required at runtime.

---

## What this is

When you embed a phrase into a vector space, it lands in a neighborhood. Its neighbors
are determined by the statistics of the model's training data - not by intent, not by
context, not by who is asking.

"How does a lock work?" and "how do I pick a lock?" are close in embedding space.
Clinical self-harm assessment tools and harmful self-harm guidance share vocabulary.
Security research descriptions and exploitation instructions often use identical
technical language. Protective information about domestic violence lives next to
enabling information about the same dynamics.

Safety systems that operate on these representations - classifiers, RLHF reward models,
prompt filters - inherit these neighborhoods. A rule that covers one concept will, by
geometry, cover some fraction of its neighbors. Some of those neighbors are benign.

This project makes those neighborhoods visible.

**It is a map for thinking, not a decision system.**

---

## What this is not

This project does not classify content as safe or unsafe. It does not reflect the
internal representations of any deployed model. Proximity on the map does not mean
the concepts are morally equivalent or should be treated identically.

Embedding distance is not moral distance.

Do not use this to justify moderation decisions, build training datasets, or claim that
any concept is "close enough" to another to warrant restriction or permission. Do not
present this visualization as an argument that any specific safety system is wrong.

---

## Why someone should care

**If you are building content moderation or RLHF reward models:** This shows you
where your rules will fire on benign content and where they will miss harmful content
because harm wore a different label. The failure mode is not random - it has a shape.

**If you are doing evals:** This gives you a vocabulary for what "near-miss" means
beyond a binary pass/fail.

**If you are a safety researcher:** This is a visual argument for why "just train a
better classifier" is incomplete. The problem is representational, not just
architectural.

**If you are an educator or policymaker:** This is an honest picture of what AI safety
filtering actually involves technically. Not PR. Not doom. The actual geometry.

**If you are new to alignment:** This is an entry point that does not require reading
papers first.

---

## The pipeline

```
data/safe_examples_seed.csv
        |
        | (human-curated, hand-reviewed)
        v
scripts/build_safe_examples.py
        |
        | (schema validation, category distribution check)
        v
artifacts/demo_examples.csv
        |
        | (sentence-transformers all-MiniLM-L6-v2, or synthetic for demo)
        v
artifacts/semantic_embeddings.npy     [N x 384 float32]
        |
        | (pairwise cosine similarity)
        v
artifacts/similarity_semantic.npy     [N x N float32]
        |
        +---> UMAP projection --> artifacts/map_coordinates.csv
        |
        +---> overlap scoring --> artifacts/overlap_scores.csv
        |
        v
streamlit run app.py
```

At runtime, the app loads the precomputed artifact files and performs no
model inference. The pipeline runs once, offline, by the developer.

---

## Local setup

```bash
git clone https://github.com/agentjakey/representation-overlap-lab
cd representation-overlap-lab

pip install -r requirements.txt

# Generate artifacts with real embeddings (downloads ~90MB model on first run, ~60s)
python scripts/export_demo_artifacts.py

# Or use synthetic demo embeddings (no download, ~5 seconds)
python scripts/export_demo_artifacts.py --synthetic

# Run the app
streamlit run app.py

# Run tests
pytest
```

Python 3.10 or later is required. The app has been tested on Linux, macOS, and Windows.

---

## Project structure

```
representation-overlap-lab/
    app.py                         Main Streamlit application
    config/                        YAML configuration files
        app_config.yaml
        safety_taxonomy.yaml       Category and tension type definitions
        design_tokens.yaml         Colors, fonts, spacing
    scripts/                       Offline pipeline scripts
        export_demo_artifacts.py   Full pipeline (synthetic or real)
        build_safe_examples.py     Validate seed data
        build_embeddings.py        Run sentence-transformers
        build_similarity.py        Compute similarity matrix
        build_projection.py        UMAP projection
        compute_overlap_scores.py  Overlap scoring
        validate_artifacts.py      Artifact consistency checks
    src/                           Python modules
        data_schema.py             Pydantic models for concept entries
        safety_taxonomy.py         Category metadata loader
        embedding.py               Embedding utilities
        similarity.py              Cosine similarity and KNN
        projection.py              UMAP wrapper
        overlap.py                 Overlap score computation
        recommender.py             Nearest neighbor results for UI
        plotting.py                Plotly figure builders
        ethics_copy.py             All user-facing microcopy strings
        demo_data.py               Synthetic embedding generation
        artifact_io.py             Load/save artifacts with validation
    data/
        safe_examples_seed.csv     Human-curated concept dataset (source of truth)
    artifacts/                     Precomputed files loaded by the app
    assets/                        CSS and SVG
    tests/                         pytest test suite
    deployment/                    HF Spaces and Render deployment guides
```

---

## Deployment

### Hugging Face Spaces (recommended)

See `deployment/HUGGINGFACE_SPACES.md` for step-by-step instructions.

Summary:
1. Create a Streamlit Space at huggingface.co/new-space
2. Add the Spaces YAML frontmatter to README.md
3. `git push space main`

No API keys or environment variables required.

### Render (fallback)

See `deployment/RENDER.md` for step-by-step instructions.

Summary:
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Environment variables: `STREAMLIT_SERVER_HEADLESS=true`

---

## Dataset

The dataset in `data/safe_examples_seed.csv` contains 113 concept descriptions
across 10 domains and five safety bands:

- **Benign** - Educational and everyday concepts.
- **Capability-Building** - Concepts with dual-use professional applications.
- **Ambiguous** - Classification depends on intent, which the embedding cannot read.
- **Policy-Relevant / Sanitized** - Uncomfortable but genuine research or clinical topics.
- **Abstract Risk Placeholder** - Names types of excluded content without reproducing it.

Every entry was written and reviewed by a human. No entry provides step-by-step
instructions for causing harm. The "out-of-scope abstract" category names types of
excluded content - the entries describe what those categories are, not examples of them.

See `data/README.md` for the full schema documentation.

---

## Limitations and ethics

**The taxonomy is editorial.** The categories reflect human judgment, not an objective
standard. A different thoughtful person might draw some lines differently.

**The embedding model is not a safety model.** `all-MiniLM-L6-v2` was trained for
general semantic similarity. Its neighborhoods reflect the statistics of general text,
not a theory of harm.

**The 2D projection is lossy.** UMAP reduces 384 dimensions to 2. Information is lost.
Treat the layout as suggestive, not definitive.

**This dataset is not representative.** It is an illustrative sample designed to show
entanglement across representative cases. Do not use it as a benchmark or training data.

**This project cannot be misread as a safety system.** It is an educational visualization.
Any claim that it "detects unsafe content" or "measures how dangerous a concept is"
would be a misuse of the project.

---

## Content policy

No entry in this dataset provides actionable procedural guidance for causing harm.
If you believe any entry crosses this line, please open a GitHub issue. The dataset
is in a plain CSV file and is easy to audit line by line.

This project will not accept contributions that add procedural harmful content,
regardless of the stated educational framing.

---

## License

MIT. See `LICENSE`.

This license permits free use, modification, and redistribution. It does not
grant permission to use this project as a safety classifier or to use its dataset
as training data for content moderation systems without independent review.
