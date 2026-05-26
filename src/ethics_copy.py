"""
All user-facing microcopy for Representation Overlap Lab.

These strings are intentionally separated from code so they can be reviewed
for tone, accuracy, and care independently of the logic. If you are reading
this to audit the project's claims, this is the right file to start with.
"""

TAGLINE = "A map for thinking, not a judge."

LANDING_INTRO = """
Safety systems for AI models need to draw lines. What counts as harmful? What
is merely sensitive? What is dual-use, context-dependent, or simply adjacent to
something that should be restricted?

The problem is that language does not organize itself the way those lines require.
When you embed a phrase into a vector space, it lands in a neighborhood. Its
neighbors are determined by the statistics of training data - not by intent,
not by context, not by who is asking.

This project makes those neighborhoods visible. It takes a curated set of
concept descriptions and shows you where they fall in semantic space, how they
cluster, and which ones live in genuinely ambiguous territory - close to
multiple categories at once.

This is a map for thinking, not a decision system.
"""

WHAT_THIS_IS = """
An interactive visualization of how concepts cluster in semantic embedding space.
The map was built using a general-purpose sentence embedding model and a
hand-curated dataset of approximately 95 concepts across five categories.
"""

WHAT_THIS_IS_NOT = """
This is not a safety classifier. It does not tell you whether a concept is safe or
unsafe. It does not reflect the internal representations of any deployed model.
Proximity on this map does not mean the concepts are morally equivalent, or that
one should be treated like the other. Embedding distance is not moral distance.

This project should not be used to justify moderation decisions, to build training
datasets, or to claim that any concept is "close enough" to another to warrant
restriction or permission.
"""

CATEGORIES_EXPLAINER = """
The five categories in this project are editorial judgments made by the project
author. A different thoughtful person might draw some lines differently. The
categories exist to make the visualization readable, not to declare final
classifications.

The model that produced these embeddings does not know the categories. It was
trained on general text for semantic similarity. Its neighborhoods reflect the
statistics of that training corpus.
"""

MAP_CAPTION = (
    "Each point is a concept description. "
    "Color encodes category. Diamonds mark high-overlap concepts - "
    "those whose nearest neighbors are mostly from different categories."
)

OVERLAP_SCORE_EXPLAINER = """
The overlap score for a concept is the fraction of its 10 nearest neighbors
that belong to a different category. A score of 0.0 means all neighbors share
the same category. A score of 1.0 means every neighbor is from a different
category. High-overlap concepts are the ones sitting at the edges of what
any classification rule can cleanly describe.
"""

SIMILARITY_CAVEAT = (
    "Closer in embedding space does not mean closer in meaning or intent. "
    "It means the descriptions used similar vocabulary and syntactic structure. "
    "Paraphrase changes geometry."
)

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
No entry in this dataset provides actionable procedural guidance for causing
harm. The "out-of-scope abstract" category names types of harmful content and
describes why they are excluded - without reproducing the content itself.

If you believe any entry has crossed this line, please open a GitHub issue.
The dataset is in a plain CSV file and is easy to audit.
"""

TAXONOMY_DISCLAIMER = """
The taxonomy in this project is not authoritative. It is a working framework
for organizing the dataset and making the visualization interpretable. It has
not been reviewed by a safety board, validated against any benchmark, or
derived from a published threat model.
"""

READING_INTRO = """
These are the papers, essays, and projects that informed this work. Each entry
includes a short note on what it contributes and why it is relevant. This list
is not comprehensive. It is a starting point.
"""

ABOUT_DATASET = """
The dataset was written by hand. Each entry was reviewed individually. The goal
was to illustrate the entanglement problem across representative cases - not to
produce a comprehensive sample of any real query distribution.

Do not use this dataset as a benchmark or as training data for safety classifiers.
"""

GUIDED_EXAMPLE_INTRO = """
Three cases where the entanglement problem is especially visible. Each case is
described in plain language, with the relevant neighborhood shown in the map.
These are not edge cases or adversarial examples. They are representative of
the kinds of decisions that safety systems face in production.
"""

CASE_1_TITLE = "When clinical language and harm language share a neighborhood"
CASE_1_BODY = """
A psychiatrist asking about self-harm assessment methods and someone looking for
specific self-harm guidance will often produce queries that land near each other
in embedding space. Both use clinical vocabulary. Both involve similar mechanisms.
The embedding model cannot read intent, institutional context, or the presence of
a patient in a clinical relationship.

Safety systems that filter on this neighborhood will suppress genuine clinical
work. Systems that allow it may pass harmful guidance. The boundary exists
between these uses, but it does not exist in the geometry.

This does not mean the problem is unsolvable. It means the solution requires
more than an embedding distance threshold. Context, source, and conversational
history all carry information that a single embedding cannot.
"""

CASE_2_TITLE = "When security education and exploitation share vocabulary"
CASE_2_BODY = """
Security researchers, students studying for certifications, and people attempting
unauthorized access all discuss the same technical concepts. How authentication
fails. How traffic can be intercepted. How systems can be probed for weaknesses.

The same sentence could appear in a university course, a penetration testing
report, or an attack planning conversation. The vocabulary is shared. The intent
is not - but intent is not in the embedding.

On this map, security research descriptions land near dual-use knowledge,
near context-dependent concepts, and occasionally near out-of-scope abstract
entries. The overlap is not a failure of the taxonomy. It reflects the actual
structure of the space.
"""

CASE_3_TITLE = "When protective information lives next to enabling information"
CASE_3_BODY = """
Information about domestic violence - how coercive control works, how to recognize
warning signs, how people leave - serves two very different populations. Advocates,
survivors, and researchers need it to protect people. In rare cases, perpetrators
might seek it to understand what behaviors will be recognized.

The same is true for extremism research, trafficking awareness, and abuse
prevention. Protective information is semantically proximate to enabling
information because they describe the same dynamics. The embedding space
does not distinguish the direction of use.

A safety system that restricts protective information to avoid enabling
harm is making a real tradeoff. This visualization helps make that tradeoff
visible rather than invisible.
"""
