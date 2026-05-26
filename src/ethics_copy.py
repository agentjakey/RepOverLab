"""
All user-facing copy for Representation Overlap Lab.

Separated from logic so it can be reviewed for tone and accuracy independently.
If you are auditing this project's claims, start here.
"""

TAGLINE = "A map for thinking, not a judge."

# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------

HOME_INTRO = """
Safety systems for AI models have to draw lines. What counts as harmful? What is
sensitive but legitimate? What is dual-use, context-dependent, or merely adjacent
to something that should be restricted?

The problem is that language does not organize itself the way those lines require.

When you embed a sentence into a vector space, it lands in a neighborhood. Its
neighbors are shaped by the statistics of training data - not by intent, not by
context, not by who is asking or why. A clinical question about medication dosage
lands near a question about overdose. A security research description lands near
an exploitation technique. A policy analysis of extremism lands near the extremism
itself.

This project makes those neighborhoods visible. It is not an argument for loosening
safety standards. It is an argument for understanding what those standards are
actually doing - and where they will struggle.
"""

HOME_WHAT_IS_OVERLAP = """
Representation overlap is what happens when two concepts from different categories
end up in the same region of semantic space.

A sentence embedding model turns text into a point in a high-dimensional space.
Points that are close together have similar embeddings - similar patterns of words,
similar syntactic structure, similar conceptual territory. The model doesn't know
which category a concept belongs to. It doesn't know your intent. It just knows
that two pieces of text look similar, by the statistical standards of its training.

When a safety system uses embedding distance to decide what is safe, it inherits
all of this. A benign concept that sounds like a restricted one will land near it.
A restricted concept that sounds clinical will land near clinical education. The
geometry is not the categorization.

This matters because:
- **False positives** suppress legitimate content that lives near restricted content.
- **False negatives** allow restricted content that successfully mimics safe language.
- **Neither is fixable with a threshold** on the same embedding space that created the problem.
"""

HOME_HOW_TO_USE = """
The **Overlap Map** shows where 113 concept descriptions fall in 2D semantic space.
Color encodes the safety band each concept was assigned. Click any point to see its
description, domain, and nearest neighbors.

The **Boundary Explorer** sorts concepts by how close they sit to multiple safety
bands simultaneously. These are the cases where classification is hardest.

The **Compare** page lets you select any two concepts and see their exact cosine
similarity in 384-dimensional embedding space.

**Methods** explains the pipeline: how embeddings were computed, how the map was
projected, and what the scores mean.

**Ethics and Limitations** is not a footnote. Read it.
"""

HOME_JUDGE_NOTE = "This is a map for thinking, not a judge."

HOME_QUICK_STATS_LABEL = "At a glance"

# ---------------------------------------------------------------------------
# Overlap Map page
# ---------------------------------------------------------------------------

MAP_CAPTION = (
    "Each point is a concept description. Color encodes safety band. "
    "Click any point to see its content, nearest neighbors, and overlap score."
)

MAP_HOVER_CAVEAT = (
    "The model that produced these embeddings does not know the safety bands. "
    "The geometry reflects language statistics, not editorial judgment."
)

OVERLAP_SCORE_EXPLAINER = """
The overlap score for a concept is the fraction of its 10 nearest neighbors that
belong to a different safety band. A score of 0.0 means all neighbors share the
same band. A score of 1.0 means every neighbor is from a different band. High-
overlap concepts are the ones sitting at real category boundaries - the ones where
any simple rule will produce errors in both directions.
"""

SIMILARITY_CAVEAT = (
    "Closer in embedding space does not mean closer in meaning or intent. "
    "It means the descriptions used similar vocabulary and structure."
)

CROSS_BAND_NOTE = (
    "Cross-band neighbors are semantically similar but assigned to a different "
    "safety band. These are the cases that make threshold-based filtering hard."
)

# ---------------------------------------------------------------------------
# Boundary Explorer page
# ---------------------------------------------------------------------------

BLUR_INTRO = """
The boundary blur score estimates how close a concept sits to multiple safety bands
at once. A high score means the concept's embedding is roughly equidistant from
several band centroids - it does not sit firmly within any single cluster.

A low score means the concept sits clearly within one band, far from others.

**This score does not indicate that a concept is unsafe.** Many high-blur concepts
are straightforwardly benign. Blur is a geometric property of where the concept
lands in embedding space, not a judgment about its content.

Think of it as a map of interesting cases - the ones where any classification rule
will be under the most pressure.
"""

BLUR_METHODOLOGY_NOTE = """
Boundary blur is computed as the normalized entropy of each concept's cosine
similarities to three reference band centroids: benign, ambiguous, and
policy-relevant sanitized. Entropy is high when the similarities are roughly
equal; low when one band dominates. See Methods for details.

This is an exploration heuristic. Do not use it as a safety signal.
"""

BLUR_NO_DATA_MSG = (
    "Boundary blur scores are not available in the current artifacts. "
    "Re-run the full pipeline to compute them: "
    "`python scripts/export_demo_artifacts.py`"
)

# ---------------------------------------------------------------------------
# Compare Examples page
# ---------------------------------------------------------------------------

COMPARE_INTRO = """
Select any two examples to see their cosine similarity in full embedding space.

Cosine similarity measures how similar the two descriptions are as vectors. A score
near 1.0 means they point in nearly the same direction in 384-dimensional space. A
score near 0.0 means they are nearly orthogonal.

This is not a judgment about whether the two concepts are morally equivalent, or
whether one should be treated like the other. It is a measurement of how the
embedding model represents them.
"""

COMPARE_HIGH_SIM_INTERP = (
    "These two examples are highly similar in embedding space. A system using "
    "embedding distance to distinguish them would need a very fine threshold - "
    "one that may not generalize across rephrasing."
)

COMPARE_MED_SIM_INTERP = (
    "These examples are moderately similar. They share some vocabulary or conceptual "
    "territory, but the embedding model does distinguish them somewhat."
)

COMPARE_LOW_SIM_INTERP = (
    "These examples are relatively distinct in embedding space. A threshold-based "
    "system would separate them without much difficulty - assuming similar phrasing."
)

COMPARE_SAME_BAND_NOTE = (
    "These examples share a safety band. High similarity between same-band examples "
    "is expected. The more interesting question is how they compare to examples "
    "from adjacent bands."
)

COMPARE_DIFF_BAND_NOTE = (
    "These examples are from different safety bands, but their embedding similarity "
    "is {sim:.2f}. This illustrates the overlap problem directly: a system that used "
    "this threshold to separate these bands would need to accept that some pairs "
    "are this close."
)

# ---------------------------------------------------------------------------
# Methods page
# ---------------------------------------------------------------------------

METHODS_INTRO = """
This page describes how the artifacts were produced. Understanding the pipeline
is important for interpreting the results correctly. Every step involves choices
that affect what the map shows and what it cannot show.
"""

METHODS_DATASET = """
The dataset was written by hand: 113 concept descriptions across 10 domains and
5 safety bands. Each entry was individually reviewed against a set of content
constraints. No entry provides actionable procedural guidance for causing harm.
Abstract risk placeholder entries name restricted categories at the level of
abstraction only - what the category is and why it is excluded.

The dataset is not a representative sample of any real query distribution. It was
designed to illustrate the overlap problem across representative cases.
"""

METHODS_EMBEDDING = """
Embeddings were computed using **all-MiniLM-L6-v2** from sentence-transformers: a
general-purpose semantic similarity model trained to map sentences to a 384-
dimensional vector space. The model was not trained for safety classification.

If sentence-transformers is unavailable, the pipeline falls back to TF-IDF with
TruncatedSVD (384 components). This fallback is lexical rather than semantic, and
the resulting map will look different. The metadata file records which mode was used.

The app never calls a model at runtime. All embeddings are precomputed and saved
as `.npy` files in the `artifacts/` directory.
"""

METHODS_PROJECTION = """
The 2D map is produced by projecting 384-dimensional embeddings down to 2 dimensions
using **UMAP** (Uniform Manifold Approximation and Projection), with parameters
n_neighbors=15, min_dist=0.1, cosine metric, and random_state=42.

If UMAP is not installed, the pipeline falls back to **PCA**. The PCA layout is
deterministic and preserves global variance, but does not preserve local neighborhood
structure as well as UMAP does.

**Important:** 2D projection always loses information. Points that appear close on
this map may be further apart in the full embedding space. Points that appear far
may share a cluster from a different projection angle. The layout is suggestive,
not definitive. Do not draw conclusions solely from the visual distance between
points on this map.
"""

METHODS_OVERLAP_SCORING = """
**Cross-band overlap score:** For each example, the fraction of its 10 nearest
neighbors (by cosine similarity) that belong to a different safety band. Score is
in [0, 1]. Zero means all neighbors share the same band; one means all neighbors
are from different bands. This score measures the density of category boundaries
in the neighborhood of each example.

**Nearest cross-band similarity:** The cosine similarity to the nearest neighbor
from a different safety band. High values indicate that the closest out-of-band
neighbor is very close.
"""

METHODS_BOUNDARY_BLUR = """
**Boundary blur score:** A heuristic that estimates how evenly an example's
embedding is attracted to multiple safety band centroids.

Method: For three reference bands (benign, ambiguous, policy-relevant sanitized),
we compute the mean embedding (centroid) of each band's members, normalize it,
and measure cosine similarity from each example to each centroid. These per-band
similarities are normalized to sum to 1 and treated as a probability distribution.
The boundary blur score is the normalized Shannon entropy of this distribution.

- Score near 1.0: the example sits roughly equidistant from all three reference
  band centroids (high entropy, maximally blurry).
- Score near 0.0: the example sits clearly closer to one band than the others
  (low entropy, sharply clustered).

**This is an exploration heuristic.** High blur does not mean a concept is unsafe.
It means the concept does not sit firmly within any single band's geometric region.
Embedding distance does not equal moral distance.
"""

METHODS_LIMITATIONS = """
**Projection distortion.** The 2D map distorts global distances. Treat it as a
neighborhood visualization, not a metric space.

**Model bias.** The embedding model encodes the statistical patterns of its training
corpus. Those patterns include biases about language, domain, and framing. The
neighborhoods reflect those biases.

**Dataset limitations.** The 113 examples were selected to illustrate specific
cases. They are not a representative sample. Category distributions are
intentional, not empirical.

**Editorial categories.** The five safety bands are editorial judgments. A
different thoughtful person might classify some entries differently. The bands
exist to make the visualization readable, not to declare authoritative categories.

**Not a deployed model.** The embeddings used here are from a general-purpose
sentence model, not from any deployed safety system. Conclusions about real
safety systems would require their actual internal representations.
"""

# ---------------------------------------------------------------------------
# Ethics & Limitations page
# ---------------------------------------------------------------------------

ETHICS_INTENDED = """
This tool is intended for:

- **Researchers and students** studying AI safety, content moderation, and the
  technical limitations of embedding-based classification.
- **Safety practitioners** who want to develop intuition for where embedding-based
  systems will struggle.
- **Policy analysts and journalists** who need concrete examples to explain the
  representation overlap problem to non-technical audiences.
- **Educators** building curricula around AI safety, dual-use technology, or the
  social implications of AI systems.
"""

ETHICS_NOT_INTENDED = """
This tool is **not** intended for:

- **Making moderation decisions.** This map is not a classifier. It does not tell
  you whether any specific content is safe or unsafe.
- **Building training datasets.** Do not use this dataset to train safety
  classifiers or to label data for moderation systems.
- **Justifying restrictions or permissions.** Proximity on this map does not imply
  that one concept should be treated like another.
- **Claiming safety system accuracy.** This project does not evaluate any deployed
  safety system and makes no claims about their performance.
- **Reproducing harmful content.** No entry in this dataset provides actionable
  procedural guidance for causing harm.
"""

ETHICS_CONTENT_POLICY = """
Every entry in this dataset was reviewed individually. The content constraints are:

- No actionable synthesis routes, step-by-step attack instructions, or operational
  harm guidance.
- No exploit code, weaponization details, or methods that would provide material
  uplift to someone attempting harm.
- No manipulation playbooks, grooming scripts, or fraud tutorials.
- Abstract risk placeholder entries name categories of restricted content and
  explain why they are excluded - without reproducing the content itself.

If you believe any entry has crossed these lines, please open a GitHub issue. The
dataset is a plain CSV file in `data/safe_examples_seed.csv` and is easy to audit.
"""

ETHICS_NOT_CLASSIFIER = """
This is not a safety classifier.

It does not output a probability that any text is harmful. It does not implement
a moderation policy. It does not represent the internal state of any deployed
AI system. The "safety bands" in this dataset are editorial categories applied to
illustrative examples - they are not ground truth, they are not validated against
any benchmark, and they have not been reviewed by a safety board.

Do not describe this project as a safety tool. Do not use it to make real decisions
about content.
"""

ETHICS_EMBEDDING_BIAS = """
**Embedding space encodes bias.** The all-MiniLM-L6-v2 model was trained on general
text from the internet. It encodes the statistical patterns of that corpus, including
biases about language, framing, domain, and what sounds like what. The neighborhoods
visible in this map reflect those biases as much as they reflect the concepts
themselves.

**Framing changes geometry.** The same information, described using different
vocabulary, will land in a different location. A clinical description of a dangerous
compound lands differently than a casual description of the same compound. The
embedding represents the surface of the text, not its underlying content.

**The taxonomy is not authoritative.** The five safety bands in this project are
a working framework for making the visualization readable. They are not derived from
a published threat model, not validated against empirical data, and not endorsed by
any safety organization.
"""

FOOTER_NOTE = (
    "Built as a careful public interface for thinking about representation overlap "
    "in AI safety. The map is a teaching aid, not a judgment system."
)

# ---------------------------------------------------------------------------
# Preserved legacy strings (referenced by older page code)
# ---------------------------------------------------------------------------

WHAT_THIS_IS = """
An interactive visualization of how concepts cluster in semantic embedding space.
The map was built using a general-purpose sentence embedding model and a hand-curated
dataset of 113 concept descriptions across 10 domains and 5 safety bands.
"""

WHAT_THIS_IS_NOT = """
This is not a safety classifier. It does not tell you whether a concept is safe or
unsafe. It does not reflect the internal representations of any deployed model.
Proximity on this map does not mean the concepts are morally equivalent. Embedding
distance is not moral distance.
"""

EMBEDDING_MODEL_NOTE = """
The embeddings were computed using all-MiniLM-L6-v2 from sentence-transformers,
a general-purpose semantic similarity model. This model was not trained for safety
classification. Its neighborhoods reflect general language statistics.
"""

UMAP_CAVEAT = """
The 2D map is a UMAP projection from 384 dimensions to 2. Information is lost.
Concepts that appear close on this map may be further apart in the actual
embedding space. Concepts that appear far may share a cluster in a different
2D view. Treat the layout as suggestive, not definitive.
"""

POLICY_STATEMENT = """
No entry in this dataset provides actionable procedural guidance for causing harm.
The abstract risk placeholder category names types of harmful content and describes
why they are excluded - without reproducing the content itself.

If you believe any entry has crossed this line, please open a GitHub issue.
"""

TAXONOMY_DISCLAIMER = """
The taxonomy in this project is not authoritative. It is a working framework for
organizing the dataset and making the visualization interpretable. It has not been
reviewed by a safety board, validated against any benchmark, or derived from a
published threat model.
"""

ABOUT_DATASET = """
The dataset was written by hand. Each entry was reviewed individually. The goal was
to illustrate the entanglement problem across representative cases - not to produce
a comprehensive sample of any real query distribution.

Do not use this dataset as a benchmark or as training data for safety classifiers.
"""
