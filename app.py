"""
Representation Overlap Lab
A map for thinking, not a judge.
"""
import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"

st.set_page_config(
    page_title="Representation Overlap Lab",
    page_icon=str(ROOT / "assets" / "logo.svg"),
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = ROOT / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


@st.cache_data(show_spinner="Loading artifacts...")
def load_artifacts():
    import sys
    sys.path.insert(0, str(ROOT))
    from src.artifact_io import load_all_artifacts
    return load_all_artifacts(ARTIFACTS_DIR)


@st.cache_data
def load_taxonomy():
    import sys
    sys.path.insert(0, str(ROOT))
    from src.safety_taxonomy import SafetyTaxonomy
    return SafetyTaxonomy()


def artifacts_ready() -> bool:
    required = [
        "demo_examples.csv",
        "semantic_embeddings.npy",
        "similarity_semantic.npy",
        "map_coordinates.csv",
        "overlap_scores.csv",
        "artifact_metadata.json",
    ]
    return all((ARTIFACTS_DIR / f).exists() for f in required)


def render_not_ready():
    st.markdown("## Setup required")
    st.markdown(
        "The precomputed artifacts have not been generated yet. "
        "Run the following command from the project root, then refresh this page."
    )
    st.code("python scripts/export_demo_artifacts.py", language="bash")
    st.markdown(
        "This generates synthetic demo embeddings and takes about 10 seconds. "
        "No model download is required. For real sentence-transformer embeddings, "
        "pass `--use-model`."
    )
    st.stop()


def render_synthetic_banner(is_synthetic: bool):
    if is_synthetic:
        st.markdown(
            '<div class="synthetic-banner">'
            "<b>Demo mode.</b> These embeddings are synthetic - geometrically structured "
            "to show cluster relationships, but not derived from real language model "
            "representations. Run <code>python scripts/export_demo_artifacts.py --use-model</code> "
            "for real semantic embeddings."
            "</div>",
            unsafe_allow_html=True,
        )


def page_map(artifacts: dict, taxonomy):
    import sys
    sys.path.insert(0, str(ROOT))
    from src.plotting import build_map_figure, build_overlap_histogram
    from src.recommender import get_neighbors
    from src import ethics_copy as copy

    merged = artifacts["merged"]
    sim = artifacts["similarity"]
    examples = artifacts["examples"]
    meta = artifacts["metadata"]

    render_synthetic_banner(meta.get("is_synthetic", True))

    col_map, col_detail = st.columns([3, 1.2])

    with col_map:
        st.markdown("## The Map")
        st.markdown(
            f'<p class="caption">{copy.MAP_CAPTION}</p>',
            unsafe_allow_html=True,
        )

    with st.sidebar:
        st.markdown("### Filter")

        all_cats = taxonomy.all_categories()
        selected_cats = []
        for cat in all_cats:
            checked = st.checkbox(
                cat.label,
                value=True,
                key=f"filter_{cat.key}",
                help=cat.description,
            )
            if checked:
                selected_cats.append(cat.key)

        st.markdown("---")
        overlap_min = st.slider(
            "Min overlap score",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.05,
            help="Show only concepts with overlap score >= this value.",
        )

        highlight_high = st.checkbox(
            "Highlight high-overlap concepts",
            value=True,
            help="Show concepts with overlap score >= 0.6 in a distinct marker shape.",
        )

        st.markdown("---")
        tension_types = ["all"] + [t.key for t in taxonomy.all_tensions()]
        tension_labels = {"all": "All tension types"} | {
            t.key: t.label for t in taxonomy.all_tensions()
        }
        selected_tension = st.selectbox(
            "Tension type",
            options=tension_types,
            format_func=lambda k: tension_labels.get(k, k),
        )

        st.markdown("---")
        st.markdown(
            '<p class="caption">'
            "Categories are editorial - the model does not know them. "
            "Diamonds mark high-overlap concepts."
            "</p>",
            unsafe_allow_html=True,
        )

    filter_df = merged.copy()
    if selected_cats:
        filter_df = filter_df[filter_df["category"].isin(selected_cats)]
    if overlap_min > 0:
        filter_df = filter_df[filter_df["overlap_score"] >= overlap_min]
    if selected_tension != "all":
        filter_df = filter_df[filter_df["tension_type"] == selected_tension]

    fig = build_map_figure(
        filter_df,
        selected_id=st.session_state.get("selected_id"),
        highlight_high_overlap=highlight_high,
        filter_categories=selected_cats if selected_cats else None,
        overlap_threshold=overlap_min,
    )

    with col_map:
        clicked = st.plotly_chart(
            fig,
            use_container_width=True,
            key="main_map",
            on_select="rerun",
            selection_mode="points",
        )

        if clicked and clicked.get("selection") and clicked["selection"].get("points"):
            point = clicked["selection"]["points"][0]
            curve_data = fig.data[point.get("curve_number", 0)]
            if hasattr(curve_data, "customdata") and curve_data.customdata is not None:
                idx = point.get("point_index", 0)
                if idx < len(curve_data.customdata):
                    st.session_state["selected_id"] = str(curve_data.customdata[idx])

    with col_detail:
        selected_id = st.session_state.get("selected_id")

        if selected_id and selected_id in merged["id"].values:
            row = merged[merged["id"] == selected_id].iloc[0]
            cat_meta = taxonomy.category(row["category"])
            tension_meta = taxonomy.tension(row["tension_type"])

            st.markdown(
                f'<div class="concept-card">'
                f'<div class="concept-name">{row["name"]}</div>'
                f'<div class="category-badge" style="background:{cat_meta.color}22;color:{cat_meta.color};">'
                f"{cat_meta.label}"
                f"</div>"
                f'<div class="description">{row["description"]}</div>'
                f'<div class="tension-label">Tension: {tension_meta.label}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )

            if row.get("legitimate_use_note"):
                st.markdown(
                    f'<div class="callout info">'
                    f"<b>Legitimate use:</b> {row['legitimate_use_note']}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"**Overlap score:** {row['overlap_score']:.2f}  "
                f"{'(high overlap)' if row['overlap_score'] >= 0.6 else ''}"
            )

            st.markdown("**Nearest neighbors**")
            st.markdown(
                f'<p class="caption">{copy.SIMILARITY_CAVEAT}</p>',
                unsafe_allow_html=True,
            )

            neighbors = get_neighbors(
                concept_id=selected_id,
                examples_df=examples,
                similarity_matrix=sim,
                k=10,
                top_n=5,
            )

            for nb in neighbors:
                nb_cat = taxonomy.category(nb.category)
                bar_width = int(nb.similarity * 100)
                same_marker = "" if nb.same_category else " *"
                st.markdown(
                    f'<div class="neighbor-row">'
                    f'<div style="flex:1;">'
                    f'<span style="font-size:0.82rem;color:#1A1A1A;">{nb.short_name}{same_marker}</span><br>'
                    f'<span style="font-size:0.72rem;color:{nb_cat.color};">{nb_cat.short}</span>'
                    f"</div>"
                    f'<div style="width:80px;">'
                    f'<div class="neighbor-sim-bar" style="width:{bar_width}%;background:{nb_cat.color};"></div>'
                    f'<span style="font-size:0.7rem;color:#7A7A7A;">{nb.similarity:.3f}</span>'
                    f"</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            st.markdown(
                '<p class="caption">* different category than selected concept</p>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="callout">'
                "<b>Click any point on the map</b> to see its description, "
                "category, tension type, and five nearest neighbors."
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p class="caption">'
                "Overlap score: fraction of a concept's 10 nearest neighbors "
                "that belong to a different category."
                "</p>",
                unsafe_allow_html=True,
            )

    with st.expander("Overlap score distribution by category"):
        hist = build_overlap_histogram(merged)
        st.plotly_chart(hist, use_container_width=True)
        st.markdown(
            '<p class="caption">'
            + copy.OVERLAP_SCORE_EXPLAINER
            + "</p>",
            unsafe_allow_html=True,
        )


def page_examples(artifacts: dict, taxonomy):
    from src import ethics_copy as copy

    meta = artifacts["metadata"]
    render_synthetic_banner(meta.get("is_synthetic", True))

    st.markdown("## Guided Examples")
    st.markdown(
        copy.GUIDED_EXAMPLE_INTRO,
        unsafe_allow_html=False,
    )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    for title, body in [
        (copy.CASE_1_TITLE, copy.CASE_1_BODY),
        (copy.CASE_2_TITLE, copy.CASE_2_BODY),
        (copy.CASE_3_TITLE, copy.CASE_3_BODY),
    ]:
        st.markdown(f"### {title}")
        st.markdown(body)
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


def page_data(artifacts: dict, taxonomy):
    from src import ethics_copy as copy

    meta = artifacts["metadata"]
    examples = artifacts["examples"]
    render_synthetic_banner(meta.get("is_synthetic", True))

    st.markdown("## The Dataset")
    st.markdown(copy.ABOUT_DATASET)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total concepts", len(examples))
    with col2:
        n_dual = len(examples[examples["category"].isin(["dual_use", "context_dependent"])])
        st.metric("Dual-use or context-dependent", n_dual)
    with col3:
        n_out = len(examples[examples["category"] == "out_of_scope_abstract"])
        st.metric("Out-of-scope (abstract)", n_out)

    st.markdown("---")

    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        search = st.text_input("Search concepts", placeholder="e.g. encryption, clinical, fire")
    with col_filter2:
        all_cat_options = ["All categories"] + sorted(examples["category"].unique().tolist())
        cat_filter = st.selectbox("Filter by category", all_cat_options)

    display_df = examples.copy()
    if search:
        mask = (
            display_df["name"].str.contains(search, case=False, na=False)
            | display_df["description"].str.contains(search, case=False, na=False)
            | display_df["short_name"].str.contains(search, case=False, na=False)
        )
        display_df = display_df[mask]
    if cat_filter != "All categories":
        display_df = display_df[display_df["category"] == cat_filter]

    label_map = taxonomy.label_map()
    display_df = display_df.copy()
    display_df["Category"] = display_df["category"].map(label_map)
    display_df["Tension"] = display_df["tension_type"].str.replace("_", " ")

    st.dataframe(
        display_df[["id", "short_name", "Category", "Tension", "description"]].rename(
            columns={
                "id": "ID",
                "short_name": "Concept",
                "description": "Description",
            }
        ),
        use_container_width=True,
        hide_index=True,
        height=500,
    )

    st.markdown(
        f'<p class="caption">Showing {len(display_df)} of {len(examples)} concepts.</p>',
        unsafe_allow_html=True,
    )

    with st.expander("Category distribution"):
        import plotly.graph_objects as go

        cat_counts = examples["category"].value_counts()
        colors = {k: taxonomy.color_map()[k] for k in cat_counts.index if k in taxonomy.color_map()}
        fig = go.Figure(
            go.Bar(
                x=[label_map.get(c, c) for c in cat_counts.index],
                y=cat_counts.values,
                marker_color=[colors.get(c, "#888888") for c in cat_counts.index],
                opacity=0.85,
            )
        )
        fig.update_layout(
            paper_bgcolor="#FAFAF8",
            plot_bgcolor="#FAFAF8",
            xaxis_title="",
            yaxis_title="Count",
            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(size=12, family="system-ui, sans-serif"),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="callout ethics">'
        + copy.POLICY_STATEMENT
        + "</div>",
        unsafe_allow_html=True,
    )


def page_about(artifacts: dict):
    from src import ethics_copy as copy

    meta = artifacts["metadata"]

    st.markdown("## About this project")
    st.markdown(copy.WHAT_THIS_IS)

    st.markdown("---")
    st.markdown("### What this is not")
    st.markdown(
        '<div class="callout ethics">' + copy.WHAT_THIS_IS_NOT + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### The categories")
    st.markdown(copy.CATEGORIES_EXPLAINER)

    st.markdown("---")
    st.markdown("### The embedding model")
    st.markdown(copy.EMBEDDING_MODEL_NOTE)

    st.markdown("---")
    st.markdown("### The 2D projection")
    st.markdown(copy.UMAP_CAVEAT)

    st.markdown("---")
    st.markdown("### Content policy")
    st.markdown(
        '<div class="callout ethics">' + copy.POLICY_STATEMENT + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### Taxonomy disclaimer")
    st.markdown(copy.TAXONOMY_DISCLAIMER)

    st.markdown("---")
    st.markdown("### Artifact metadata")
    st.json(meta)


def page_reading():
    from src import ethics_copy as copy

    st.markdown("## Further Reading")
    st.markdown(copy.READING_INTRO)

    entries = [
        {
            "title": "Representation Engineering: A Top-Down Approach to AI Transparency",
            "authors": "Zou et al., 2023",
            "annotation": (
                "Introduces representation engineering as a framework for understanding "
                "and controlling AI behavior through linear representations. Directly relevant "
                "to why embedding geometry matters for safety."
            ),
        },
        {
            "title": "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning",
            "authors": "Anthropic, 2023",
            "annotation": (
                "Anthropic's work on sparse autoencoders and feature decomposition. "
                "Shows that model internals are more entangled than clean feature boundaries "
                "would suggest - the representational version of the overlap problem."
            ),
        },
        {
            "title": "Risks from Learned Optimization in Advanced Machine Learning Systems",
            "authors": "Hubinger et al., 2019",
            "annotation": (
                "Classic mesa-optimization paper. The concern about deceptive alignment "
                "connects to why surface-level similarity (including embedding similarity) "
                "does not imply value alignment."
            ),
        },
        {
            "title": "Language Models are Few-Shot Learners (GPT-3)",
            "authors": "Brown et al., 2020",
            "annotation": (
                "The paper that made the dual-use nature of language models a mainstream "
                "concern. The capabilities that make models useful are the same ones that "
                "make safety classification hard."
            ),
        },
        {
            "title": "Universal and Transferable Adversarial Attacks on Aligned Language Models",
            "authors": "Zou et al., 2023",
            "annotation": (
                "Demonstrates that safety training can be bypassed through input perturbations "
                "that shift the activation trajectory. Directly illustrates why representation "
                "space boundaries are not stable."
            ),
        },
        {
            "title": "Content Moderation at Scale: The Human Side of AI Safety",
            "authors": "Roberts, 2019 (Behind the Screen)",
            "annotation": (
                "Documents the human cost of content moderation work and the real-world "
                "complexity of applying rules at scale. A necessary counterweight to purely "
                "technical framings of the safety problem."
            ),
        },
        {
            "title": "On the Dangers of Stochastic Parrots",
            "authors": "Bender, Gebru, McMillan-Major, Shmitchell, 2021",
            "annotation": (
                "Raises concerns about what large language models encode and reproduce. "
                "Relevant to understanding what semantic embedding spaces actually contain "
                "and whose knowledge they reflect."
            ),
        },
        {
            "title": "AI Safety and the Age of Dislocation",
            "authors": "Paul Christiano, alignment forum posts",
            "annotation": (
                "Christiano's public writing on alignment strategy provides context for "
                "why representation-level analysis matters in the longer arc of AI safety work."
            ),
        },
        {
            "title": "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
            "authors": "Reimers and Gurevych, 2019",
            "annotation": (
                "The technical foundation for the embedding model used in this project. "
                "Understanding how the model was trained clarifies what its neighborhoods "
                "actually reflect."
            ),
        },
        {
            "title": "UMAP: Uniform Manifold Approximation and Projection",
            "authors": "McInnes, Healy, Melville, 2018",
            "annotation": (
                "The algorithm used for 2D projection. Understanding UMAP's assumptions - "
                "especially that it can distort global distances while preserving local "
                "neighborhoods - is important for interpreting the map correctly."
            ),
        },
    ]

    for entry in entries:
        st.markdown(
            f'<div class="reading-entry">'
            f'<div class="reading-title">{entry["title"]}</div>'
            f'<div style="font-size:0.78rem;color:#7A7A7A;margin-bottom:0.2rem;">{entry["authors"]}</div>'
            f'<div class="reading-annotation">{entry["annotation"]}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )


def main():
    if "selected_id" not in st.session_state:
        st.session_state["selected_id"] = None

    with st.sidebar:
        st.markdown(
            '<h1 style="font-family:Georgia,serif;font-size:1.1rem;margin-bottom:0.1rem;">'
            "Representation Overlap Lab"
            "</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="tagline">A map for thinking, not a judge.</p>',
            unsafe_allow_html=True,
        )
        st.markdown("---")

        page = st.radio(
            "Navigate",
            options=["The Map", "Guided Examples", "The Dataset", "About & Limitations", "Further Reading"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown(
            '<p class="caption">'
            "This does not decide what is allowed. "
            "It helps show why the boundary is hard."
            "</p>",
            unsafe_allow_html=True,
        )

    if not artifacts_ready():
        render_not_ready()
        return

    try:
        artifacts = load_artifacts()
        taxonomy = load_taxonomy()
    except Exception as e:
        st.error(f"Failed to load artifacts: {e}")
        st.info("Run `python scripts/export_demo_artifacts.py` and refresh.")
        st.stop()
        return

    if page == "The Map":
        page_map(artifacts, taxonomy)
    elif page == "Guided Examples":
        page_examples(artifacts, taxonomy)
    elif page == "The Dataset":
        page_data(artifacts, taxonomy)
    elif page == "About & Limitations":
        page_about(artifacts)
    elif page == "Further Reading":
        page_reading()


if __name__ == "__main__":
    main()
