"""
Representation Overlap Lab
A map for thinking, not a judge.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"

st.set_page_config(
    page_title="Representation Overlap Lab",
    layout="wide",
    initial_sidebar_state="expanded",
)

_css_path = ROOT / "assets" / "style.css"
if _css_path.exists():
    with open(_css_path, encoding="utf-8") as _f:
        st.markdown(f"<style>{_f.read()}</style>", unsafe_allow_html=True)


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


REQUIRED_ARTIFACTS = [
    "demo_examples.csv",
    "semantic_embeddings.npy",
    "similarity_semantic.npy",
    "map_coordinates.csv",
    "overlap_scores.csv",
    "artifact_metadata.json",
]

PAGES = [
    "Home",
    "Overlap Map",
    "Boundary Blur Explorer",
    "Compare Examples",
    "Methods",
    "Ethics & Limitations",
]


def artifacts_ready() -> bool:
    return all((ARTIFACTS_DIR / f).exists() for f in REQUIRED_ARTIFACTS)


def show_not_ready():
    st.markdown("## Setup required")
    st.markdown(
        "The precomputed artifacts have not been generated yet. "
        "Run the following command from the project root, then refresh this page."
    )
    st.code("python scripts/export_demo_artifacts.py", language="bash")
    st.markdown(
        "This computes embeddings and UMAP projections and takes about 60 seconds "
        "on first run (model download included). "
        "To skip the model and use synthetic demo embeddings, pass `--synthetic`."
    )
    st.stop()


def show_synthetic_banner(is_synthetic: bool):
    if is_synthetic:
        st.markdown(
            '<div class="synthetic-banner">'
            "<b>Demo mode:</b> These embeddings are synthetic, not derived from a real "
            "language model. Run <code>python scripts/export_demo_artifacts.py</code> "
            "for real semantic embeddings."
            "</div>",
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _render_concept_card(row: pd.Series, taxonomy):
    """Render a concept card using the new schema columns with old-name fallback."""
    band = str(row.get("safety_band", row.get("category", "")))
    try:
        cat = taxonomy.category(band)
        cat_label = cat.label
        cat_color = cat.color
    except (KeyError, TypeError):
        cat_label = band
        cat_color = "#888888"

    title = str(row.get("title", row.get("name", "")))
    topic = str(row.get("topic", row.get("short_name", "")))
    summary = str(row.get("safe_summary", row.get("description", "")))

    domain_label = ""
    domain_raw = row.get("domain")
    if domain_raw and pd.notna(domain_raw):
        try:
            domain_label = taxonomy.domain(str(domain_raw)).label
        except KeyError:
            domain_label = str(domain_raw).replace("_", " ")

    framing_label = ""
    framing_raw = row.get("framing", row.get("tension_type"))
    if framing_raw and pd.notna(framing_raw):
        try:
            framing_label = taxonomy.tension(str(framing_raw)).label
        except KeyError:
            framing_label = str(framing_raw).replace("_", " ")

    overlap_val = float(row.get("overlap_score", 0))

    st.markdown(
        f'<div class="concept-card">'
        f'<div class="concept-name">{title}</div>'
        f'<div class="category-badge" style="background:{cat_color}22;color:{cat_color};">'
        f"{cat_label}</div><br>"
        f'<div class="description">{summary}</div>'
        f'<div class="tension-label">Topic: {topic}</div>'
        f'<div class="tension-label">Domain: {domain_label}</div>'
        f'<div class="tension-label">Framing: {framing_label}</div>'
        f'<div class="tension-label">Overlap score: {overlap_val:.2f}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def _render_neighbors(neighbors, taxonomy):
    for nb in neighbors:
        try:
            nb_cat = taxonomy.category(nb.safety_band)
            nb_color = nb_cat.color
            nb_short = nb_cat.short
        except (KeyError, TypeError):
            nb_color = "#888888"
            nb_short = nb.safety_band

        bar_pct = int(nb.similarity * 100)
        marker = "" if nb.same_band else " *"
        st.markdown(
            f'<div class="neighbor-row">'
            f'<div style="flex:1;">'
            f'<span style="font-size:0.82rem;color:#1A1A1A;">{nb.topic}{marker}</span><br>'
            f'<span style="font-size:0.72rem;color:{nb_color};">{nb_short}</span>'
            f"</div>"
            f'<div style="width:80px;">'
            f'<div class="neighbor-sim-bar" style="width:{bar_pct}%;background:{nb_color};"></div>'
            f'<span style="font-size:0.7rem;color:#7A7A7A;">{nb.similarity:.3f}</span>'
            f"</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    cross = [nb for nb in neighbors if not nb.same_band]
    if cross:
        st.markdown(
            '<p class="caption">* from a different safety band</p>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Page: Home
# ---------------------------------------------------------------------------

def page_home(artifacts: dict):
    from src import ethics_copy as copy

    meta = artifacts["metadata"]
    merged = artifacts["merged"]

    show_synthetic_banner(meta.get("is_synthetic", False))

    st.markdown("## Representation Overlap Lab")
    st.markdown(
        '<p class="subtitle">Why safety boundaries are not always cleanly separable.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="tagline">A map for thinking, not a judge.</p>',
        unsafe_allow_html=True,
    )

    st.markdown(copy.HOME_INTRO)

    st.markdown(
        '<div class="callout">' + copy.HOME_WHAT_IS_OVERLAP + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### How to use this lab")
    st.markdown(copy.HOME_HOW_TO_USE)

    st.markdown("---")
    st.markdown(f'<p class="caption">{copy.HOME_QUICK_STATS_LABEL}</p>', unsafe_allow_html=True)

    n = len(merged)
    n_high = int((merged["overlap_score"] >= 0.6).sum())
    n_domains = merged["domain"].nunique() if "domain" in merged.columns else "?"
    model = meta.get("embedding_model", "unknown")
    proj = meta.get("projection_method", "unknown").upper()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Concepts", n)
    c2.metric("High-overlap (>= 0.6)", n_high)
    c3.metric("Domains", n_domains)
    c4.metric("Projection", proj)

    st.markdown(
        f'<p class="caption">Embedding model: {model}</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="callout info">'
        f"<b>{copy.HOME_JUDGE_NOTE}</b>"
        "</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Page: Overlap Map
# ---------------------------------------------------------------------------

def page_map(artifacts: dict, taxonomy):
    from src.plotting import build_map_figure, build_overlap_histogram, build_centroid_sim_bar
    from src.recommender import get_neighbors
    from src import ethics_copy as copy

    merged = artifacts["merged"]
    sim = artifacts["similarity"]
    examples = artifacts["examples"]
    example_ids = examples["id"].tolist()
    meta = artifacts["metadata"]

    show_synthetic_banner(meta.get("is_synthetic", False))

    with st.sidebar:
        st.markdown("### Filters")

        all_cats = taxonomy.all_categories()
        selected_cats = []
        for cat in all_cats:
            if st.checkbox(cat.label, value=True, key=f"map_cat_{cat.key}", help=cat.description):
                selected_cats.append(cat.key)

        st.markdown("---")
        overlap_min = st.slider(
            "Min overlap score",
            min_value=0.0, max_value=1.0, value=0.0, step=0.05,
            key="map_overlap_min",
            help="Show only concepts with overlap score >= this value.",
        )
        highlight_high = st.checkbox(
            "Highlight high-overlap (>= 0.6)", value=True, key="map_highlight",
        )
        st.markdown("---")

        framing_opts = ["all"] + [t.key for t in taxonomy.all_tensions()]
        framing_labels = {"all": "All framings"} | {t.key: t.label for t in taxonomy.all_tensions()}
        selected_framing = st.selectbox(
            "Framing", options=framing_opts,
            format_func=lambda k: framing_labels.get(k, k),
            key="map_framing",
        )

        domain_opts = ["all"] + [d.key for d in taxonomy.all_domains()]
        domain_labels = {"all": "All domains"} | {d.key: d.label for d in taxonomy.all_domains()}
        selected_domain = st.selectbox(
            "Domain", options=domain_opts,
            format_func=lambda k: domain_labels.get(k, k),
            key="map_domain",
        )

        symbol_by_domain = st.checkbox(
            "Symbol by domain", value=False, key="map_sym_domain",
            help="Use distinct marker shapes for each domain instead of each band.",
        )

        st.markdown("---")
        st.markdown(
            '<p class="caption">Categories are editorial. '
            "The embedding model does not know them.</p>",
            unsafe_allow_html=True,
        )

    # Build filtered dataframe for the plot
    plot_df = merged.copy()
    if selected_cats:
        plot_df = plot_df[plot_df["safety_band"].isin(selected_cats)]
    if selected_framing != "all" and "framing" in plot_df.columns:
        plot_df = plot_df[plot_df["framing"] == selected_framing]
    if selected_domain != "all" and "domain" in plot_df.columns:
        plot_df = plot_df[plot_df["domain"] == selected_domain]

    fig = build_map_figure(
        plot_df,
        selected_id=st.session_state.get("selected_id"),
        highlight_high_overlap=highlight_high,
        filter_categories=selected_cats if selected_cats else None,
        overlap_threshold=overlap_min,
        symbol_by_domain=symbol_by_domain,
    )

    col_map, col_detail = st.columns([3, 1.2])

    with col_map:
        st.markdown("## The Map")
        st.markdown(
            f'<p class="caption">{copy.MAP_CAPTION}</p>',
            unsafe_allow_html=True,
        )
        clicked = st.plotly_chart(
            fig,
            use_container_width=True,
            key="main_map",
            on_select="rerun",
            selection_mode="points",
        )
        # Extract selected point ID from Plotly click event
        if (
            clicked
            and isinstance(clicked, dict)
            and clicked.get("selection")
            and clicked["selection"].get("points")
        ):
            point = clicked["selection"]["points"][0]
            curve_idx = point.get("curve_number", 0)
            pt_idx = point.get("point_index", 0)
            if curve_idx < len(fig.data):
                curve = fig.data[curve_idx]
                cd = getattr(curve, "customdata", None)
                if cd is not None and pt_idx < len(cd):
                    st.session_state["selected_id"] = str(cd[pt_idx])

    with col_detail:
        selected_id = st.session_state.get("selected_id")

        if selected_id and selected_id in merged["id"].values:
            row = merged[merged["id"] == selected_id].iloc[0]

            _render_concept_card(row, taxonomy)

            overlap_val = float(row["overlap_score"])
            st.markdown(
                f"**Overlap score:** {overlap_val:.2f}"
                + (" (high)" if overlap_val >= 0.6 else "")
            )
            if "boundary_blur_score" in row.index and pd.notna(row.get("boundary_blur_score")):
                st.markdown(f"**Boundary blur:** {float(row['boundary_blur_score']):.2f}")

            # Centroid similarities mini-chart
            centroid_cols = [
                "sim_to_benign",
                "sim_to_ambiguous",
                "sim_to_policy_relevant_sanitized",
            ]
            if any(c in row.index and pd.notna(row.get(c)) for c in centroid_cols):
                st.markdown("**Band centroid similarities**")
                sim_bar = build_centroid_sim_bar(row)
                if sim_bar.data:
                    st.plotly_chart(
                        sim_bar, use_container_width=True,
                        key=f"centroid_{selected_id}",
                    )

            # Nearest-neighbor tabs
            st.markdown("**Nearest neighbors**")
            tab_all, tab_cross = st.tabs(["All", "Cross-band only"])

            with tab_all:
                st.markdown(
                    f'<p class="caption">{copy.SIMILARITY_CAVEAT}</p>',
                    unsafe_allow_html=True,
                )
                if selected_id in example_ids:
                    nbrs = get_neighbors(
                        example_id=selected_id,
                        examples_df=examples,
                        similarity_matrix=sim,
                        k=10,
                        top_n=5,
                        cross_band_only=False,
                    )
                    _render_neighbors(nbrs, taxonomy)

            with tab_cross:
                st.markdown(
                    f'<p class="caption">{copy.CROSS_BAND_NOTE}</p>',
                    unsafe_allow_html=True,
                )
                if selected_id in example_ids:
                    nbrs_cross = get_neighbors(
                        example_id=selected_id,
                        examples_df=examples,
                        similarity_matrix=sim,
                        k=10,
                        top_n=5,
                        cross_band_only=True,
                    )
                    if not nbrs_cross:
                        st.markdown(
                            '<p class="caption">No cross-band neighbors in top-10.</p>',
                            unsafe_allow_html=True,
                        )
                    else:
                        _render_neighbors(nbrs_cross, taxonomy)

        else:
            st.markdown(
                '<div class="callout">'
                "<b>Click any point on the map</b> to see its content, "
                "safety band, domain, and nearest neighbors."
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p class="caption">'
                "Overlap score: fraction of a concept's 10 nearest neighbors "
                "that belong to a different safety band."
                "</p>",
                unsafe_allow_html=True,
            )

    with st.expander("Overlap score distribution by band"):
        hist_fig = build_overlap_histogram(merged)
        st.plotly_chart(hist_fig, use_container_width=True, key="overlap_hist")
        st.markdown(copy.OVERLAP_SCORE_EXPLAINER)


# ---------------------------------------------------------------------------
# Page: Boundary Blur Explorer
# ---------------------------------------------------------------------------

def page_blur(artifacts: dict, taxonomy):
    from src.plotting import build_blur_bar, build_centroid_sim_bar
    from src import ethics_copy as copy

    merged = artifacts["merged"]
    meta = artifacts["metadata"]

    show_synthetic_banner(meta.get("is_synthetic", False))

    st.markdown("## Boundary Blur Explorer")
    st.markdown(copy.BLUR_INTRO)

    if "boundary_blur_score" not in merged.columns:
        st.markdown(
            '<div class="callout warning">' + copy.BLUR_NO_DATA_MSG + "</div>",
            unsafe_allow_html=True,
        )
        return

    blur_df = merged.dropna(subset=["boundary_blur_score"]).copy()
    topic_col = "topic" if "topic" in blur_df.columns else "short_name"

    # Top-30 bar chart
    top30 = blur_df.nlargest(30, "boundary_blur_score")
    st.markdown("### Top-30 by boundary blur score")
    bar_fig = build_blur_bar(top30)
    st.plotly_chart(bar_fig, use_container_width=True, key="blur_bar")

    st.markdown("---")

    # Full sortable table
    st.markdown("### All concepts sorted by blur score")
    label_map = taxonomy.label_map()

    display_cols = ["id", topic_col, "safety_band", "boundary_blur_score", "overlap_score"]
    if "domain" in blur_df.columns:
        display_cols.insert(3, "domain")

    display = blur_df[display_cols].copy()
    display["Band"] = display["safety_band"].map(label_map)
    display = display.sort_values("boundary_blur_score", ascending=False)

    rename = {
        "id": "ID",
        topic_col: "Concept",
        "safety_band": "_drop_band",
        "boundary_blur_score": "Blur",
        "overlap_score": "Overlap",
    }
    if "domain" in display.columns:
        rename["domain"] = "Domain"

    display = display.rename(columns=rename)
    show_cols = ["ID", "Concept", "Band", "Blur", "Overlap"]
    if "Domain" in display.columns:
        show_cols.insert(3, "Domain")
    display["Blur"] = display["Blur"].round(3)
    display["Overlap"] = display["Overlap"].round(3)

    st.dataframe(
        display[show_cols],
        use_container_width=True,
        hide_index=True,
        height=400,
    )

    st.markdown("---")

    # Per-concept centroid similarity chart
    centroid_cols = ["sim_to_benign", "sim_to_ambiguous", "sim_to_policy_relevant_sanitized"]
    has_centroid = any(c in merged.columns for c in centroid_cols)

    if has_centroid:
        st.markdown("### Centroid similarities for a concept")
        sorted_ids = blur_df.sort_values("boundary_blur_score", ascending=False)["id"].tolist()
        id_to_label = {
            row["id"]: row[topic_col]
            for _, row in blur_df.iterrows()
        }

        sel_id = st.selectbox(
            "Select a concept",
            options=sorted_ids,
            format_func=lambda x: id_to_label.get(x, x),
            key="blur_concept_sel",
        )

        if sel_id:
            sel_row = merged[merged["id"] == sel_id].iloc[0]
            sim_fig = build_centroid_sim_bar(sel_row)
            if sim_fig.data:
                st.plotly_chart(sim_fig, use_container_width=True, key=f"centroid_{sel_id}")
            blur_val = float(sel_row["boundary_blur_score"])
            ov_val = float(sel_row["overlap_score"])
            st.markdown(
                f'<p class="caption">Blur: {blur_val:.3f} | Overlap: {ov_val:.3f}</p>',
                unsafe_allow_html=True,
            )

    with st.expander("How the blur score is computed"):
        st.markdown(copy.BLUR_METHODOLOGY_NOTE)


# ---------------------------------------------------------------------------
# Page: Compare Examples
# ---------------------------------------------------------------------------

def page_compare(artifacts: dict, taxonomy):
    from src import ethics_copy as copy

    merged = artifacts["merged"]
    examples = artifacts["examples"]
    sim_matrix = artifacts["similarity"]
    meta = artifacts["metadata"]

    show_synthetic_banner(meta.get("is_synthetic", False))

    st.markdown("## Compare Examples")
    st.markdown(copy.COMPARE_INTRO)

    topic_col = "topic" if "topic" in merged.columns else "short_name"
    all_ids = examples["id"].tolist()
    id_to_label = {
        row["id"]: row.get(topic_col, row["id"])
        for _, row in merged.iterrows()
    }

    col_a, col_b = st.columns(2)
    with col_a:
        id_a = st.selectbox(
            "Example A",
            options=all_ids,
            format_func=lambda x: id_to_label.get(x, x),
            key="compare_a",
        )
    with col_b:
        remaining = [i for i in all_ids if i != id_a]
        default_b_idx = min(1, len(remaining) - 1)
        id_b = st.selectbox(
            "Example B",
            options=remaining,
            format_func=lambda x: id_to_label.get(x, x),
            key="compare_b",
            index=default_b_idx,
        )

    if not id_a or not id_b:
        return

    idx_a = all_ids.index(id_a)
    idx_b = all_ids.index(id_b)
    sim_val = float(sim_matrix[idx_a, idx_b])

    st.markdown("---")
    st.metric("Cosine similarity", f"{sim_val:.4f}")

    row_a = merged[merged["id"] == id_a].iloc[0]
    row_b = merged[merged["id"] == id_b].iloc[0]
    band_a = str(row_a.get("safety_band", row_a.get("category", "")))
    band_b = str(row_b.get("safety_band", row_b.get("category", "")))

    if band_a == band_b:
        st.markdown(
            f'<div class="callout info">{copy.COMPARE_SAME_BAND_NOTE}</div>',
            unsafe_allow_html=True,
        )
    else:
        note = copy.COMPARE_DIFF_BAND_NOTE.format(sim=sim_val)
        st.markdown(
            f'<div class="callout warning">{note}</div>',
            unsafe_allow_html=True,
        )

    if sim_val >= 0.75:
        interp = copy.COMPARE_HIGH_SIM_INTERP
    elif sim_val >= 0.5:
        interp = copy.COMPARE_MED_SIM_INTERP
    else:
        interp = copy.COMPARE_LOW_SIM_INTERP

    st.markdown(f'<p class="caption">{interp}</p>', unsafe_allow_html=True)

    st.markdown("---")
    card_a, card_b = st.columns(2)
    with card_a:
        st.markdown("**Example A**")
        _render_concept_card(row_a, taxonomy)
    with card_b:
        st.markdown("**Example B**")
        _render_concept_card(row_b, taxonomy)


# ---------------------------------------------------------------------------
# Page: Methods
# ---------------------------------------------------------------------------

def page_methods(artifacts: dict):
    from src import ethics_copy as copy

    meta = artifacts["metadata"]

    st.markdown("## Methods")
    st.markdown(copy.METHODS_INTRO)

    st.markdown("### Dataset")
    st.markdown(copy.METHODS_DATASET)

    st.markdown("### Embedding model")
    st.markdown(copy.METHODS_EMBEDDING)

    st.markdown("### 2D projection")
    st.markdown(copy.METHODS_PROJECTION)

    st.markdown("### Overlap scoring")
    st.markdown(copy.METHODS_OVERLAP_SCORING)

    st.markdown("### Boundary blur score")
    st.markdown(copy.METHODS_BOUNDARY_BLUR)

    st.markdown("### Limitations")
    st.markdown(
        '<div class="callout">' + copy.METHODS_LIMITATIONS + "</div>",
        unsafe_allow_html=True,
    )

    with st.expander("Artifact metadata"):
        st.json(meta)


# ---------------------------------------------------------------------------
# Page: Ethics & Limitations
# ---------------------------------------------------------------------------

def page_ethics():
    from src import ethics_copy as copy

    st.markdown("## Ethics & Limitations")
    st.markdown(
        '<div class="callout ethics">'
        "<b>This is not a safety classifier. Read this page before drawing conclusions.</b>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Intended uses")
    st.markdown(copy.ETHICS_INTENDED)

    st.markdown("### Not intended for")
    st.markdown(
        '<div class="callout warning">' + copy.ETHICS_NOT_INTENDED + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Content policy")
    st.markdown(
        '<div class="policy-box">' + copy.ETHICS_CONTENT_POLICY + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Not a classifier")
    st.markdown(
        '<div class="callout ethics">' + copy.ETHICS_NOT_CLASSIFIER + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Embedding space and bias")
    st.markdown(copy.ETHICS_EMBEDDING_BIAS)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    from src import ethics_copy as copy

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
            options=PAGES,
            label_visibility="collapsed",
            key="nav",
        )

        st.markdown("---")
        st.markdown(
            f'<p class="caption">{copy.FOOTER_NOTE}</p>',
            unsafe_allow_html=True,
        )

    if not artifacts_ready():
        show_not_ready()
        return

    try:
        artifacts = load_artifacts()
        taxonomy = load_taxonomy()
    except Exception as exc:
        st.error(f"Failed to load artifacts: {exc}")
        st.info("Run `python scripts/export_demo_artifacts.py` and refresh.")
        st.stop()
        return

    if page == "Home":
        page_home(artifacts)
    elif page == "Overlap Map":
        page_map(artifacts, taxonomy)
    elif page == "Boundary Blur Explorer":
        page_blur(artifacts, taxonomy)
    elif page == "Compare Examples":
        page_compare(artifacts, taxonomy)
    elif page == "Methods":
        page_methods(artifacts)
    elif page == "Ethics & Limitations":
        page_ethics()


if __name__ == "__main__":
    main()
