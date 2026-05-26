from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from src.safety_taxonomy import SafetyTaxonomy

TAXONOMY = SafetyTaxonomy()
COLOR_MAP = TAXONOMY.color_map()
LABEL_MAP = TAXONOMY.label_map()

CATEGORY_ORDER = [
    "benign",
    "capability_building",
    "ambiguous",
    "policy_relevant_sanitized",
    "abstract_risk_placeholder",
]

MARKER_SYMBOL_MAP = {
    "benign": "circle",
    "capability_building": "circle",
    "ambiguous": "diamond",
    "policy_relevant_sanitized": "circle",
    "abstract_risk_placeholder": "diamond",
}

DOMAIN_SYMBOL_MAP = {
    "biology": "circle",
    "cybersecurity": "square",
    "persuasion": "diamond",
    "physics": "triangle-up",
    "AI_agents": "cross",
    "governance": "hexagon",
    "education": "star",
    "medicine": "circle-open",
    "climate": "triangle-down",
    "law_policy": "diamond-open",
}


def _cat_col(df: pd.DataFrame) -> str:
    return "safety_band" if "safety_band" in df.columns else "category"

def _id_col(df: pd.DataFrame) -> str:
    return "id" if "id" in df.columns else "example_id"

def _label_col(df: pd.DataFrame) -> str:
    return "title" if "title" in df.columns else "name"

def _short_col(df: pd.DataFrame) -> str:
    return "topic" if "topic" in df.columns else "short_name"

def _framing_col(df: pd.DataFrame) -> str:
    return "framing" if "framing" in df.columns else "tension_type"

def _domain_col(df: pd.DataFrame) -> Optional[str]:
    return "domain" if "domain" in df.columns else None

def _summary_col(df: pd.DataFrame) -> Optional[str]:
    return "safe_summary" if "safe_summary" in df.columns else None


def build_map_figure(
    df: pd.DataFrame,
    selected_id: Optional[str] = None,
    highlight_high_overlap: bool = False,
    filter_categories: Optional[list[str]] = None,
    overlap_threshold: float = 0.0,
    symbol_by_domain: bool = False,
) -> go.Figure:
    """
    Build the main 2D concept map scatter figure.
    df must contain: id/example_id, title/name, topic/short_name,
    safety_band/category, framing/tension_type, x, y, overlap_score.
    """
    cat_col = _cat_col(df)
    id_col = _id_col(df)
    short_col = _short_col(df)
    framing_col = _framing_col(df)
    domain_col = _domain_col(df)
    summary_col = _summary_col(df)

    if filter_categories:
        plot_df = df[df[cat_col].isin(filter_categories)].copy()
    else:
        plot_df = df.copy()

    if overlap_threshold > 0:
        plot_df = plot_df[plot_df["overlap_score"] >= overlap_threshold].copy()

    fig = go.Figure()

    for cat in CATEGORY_ORDER:
        cat_df = plot_df[plot_df[cat_col] == cat]
        if cat_df.empty:
            continue

        is_high_overlap = cat_df["overlap_score"] >= 0.6

        for high in [False, True]:
            subset = cat_df[is_high_overlap == high]
            if subset.empty:
                continue

            size = 13 if (high and highlight_high_overlap) else 10
            opacity = 0.95 if (high and highlight_high_overlap) else 0.82
            line_width = 1.5 if high and highlight_high_overlap else 0.8
            line_color = "#1A1A1A" if high and highlight_high_overlap else "rgba(0,0,0,0.3)"

            if symbol_by_domain and domain_col:
                symbol_list = [
                    DOMAIN_SYMBOL_MAP.get(str(row.get(domain_col, "")), "circle")
                    for _, row in subset.iterrows()
                ]
            elif high and highlight_high_overlap:
                symbol_list = "diamond"
            else:
                symbol_list = MARKER_SYMBOL_MAP.get(cat, "circle")

            hover_text = []
            for _, row in subset.iterrows():
                parts = [f"<b>{row[short_col]}</b>"]
                parts.append(f"Band: {LABEL_MAP.get(row[cat_col], row[cat_col])}")
                if domain_col and pd.notna(row.get(domain_col)):
                    parts.append(f"Domain: {str(row[domain_col]).replace('_', ' ')}")
                parts.append(f"Framing: {str(row[framing_col]).replace('_', ' ')}")
                if summary_col and pd.notna(row.get(summary_col)):
                    summary = str(row[summary_col])[:90]
                    if len(str(row.get(summary_col, ""))) > 90:
                        summary += "..."
                    parts.append(f"<i>{summary}</i>")
                parts.append(f"Overlap: {row['overlap_score']:.2f}")
                hover_text.append("<br>".join(parts))

            is_selected = (
                subset[id_col] == selected_id
                if selected_id
                else pd.Series([False] * len(subset), index=subset.index)
            )

            fig.add_trace(
                go.Scatter(
                    x=subset["x"],
                    y=subset["y"],
                    mode="markers",
                    name=LABEL_MAP.get(cat, cat),
                    legendgroup=cat,
                    showlegend=(not high),
                    marker=dict(
                        color=COLOR_MAP.get(cat, "#888888"),
                        size=[15 if sel else size for sel in is_selected],
                        opacity=[1.0 if sel else opacity for sel in is_selected],
                        symbol=symbol_list,
                        line=dict(
                            width=[2.5 if sel else line_width for sel in is_selected],
                            color=["#000000" if sel else line_color for sel in is_selected],
                        ),
                    ),
                    text=hover_text,
                    hovertemplate="%{text}<extra></extra>",
                    customdata=subset[id_col].values,
                )
            )

    fig.update_layout(
        paper_bgcolor="#FAFAF8",
        plot_bgcolor="#FAFAF8",
        font=dict(family="system-ui, sans-serif", size=12, color="#1A1A1A"),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01,
            bgcolor="rgba(250,250,248,0.9)",
            bordercolor="#E0DDD8",
            borderwidth=1,
            font=dict(size=11),
        ),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(0,0,0,0.04)",
            zeroline=False, showticklabels=False, title="",
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(0,0,0,0.04)",
            zeroline=False, showticklabels=False, title="",
        ),
        margin=dict(l=10, r=10, t=30, b=10),
        hoverlabel=dict(
            bgcolor="#FFFFFF", bordercolor="#E0DDD8", font=dict(size=12),
        ),
        dragmode="pan",
    )

    return fig


def build_affinity_heatmap(affinity_df: pd.DataFrame) -> go.Figure:
    """Heatmap of cross-band mean similarity."""
    cats = CATEGORY_ORDER
    short = {k: TAXONOMY.short_label_map()[k] for k in cats if k in TAXONOMY.short_label_map()}
    z = np.zeros((len(cats), len(cats)))

    for _, row in affinity_df.iterrows():
        if row["category_a"] in cats and row["category_b"] in cats:
            i = cats.index(row["category_a"])
            j = cats.index(row["category_b"])
            z[i][j] = row["mean_similarity"]

    labels = [short.get(c, c) for c in cats]

    fig = go.Figure(
        go.Heatmap(
            z=z, x=labels, y=labels,
            colorscale=[[0.0, "#F2F0EB"], [0.5, "#9B7EBD"], [1.0, "#4E8098"]],
            zmin=0, zmax=1,
            text=[[f"{val:.2f}" if val > 0 else "" for val in row] for row in z],
            texttemplate="%{text}",
            showscale=True,
            colorbar=dict(title="Mean cosine similarity", thickness=12, len=0.8),
        )
    )
    fig.update_layout(
        paper_bgcolor="#FAFAF8", plot_bgcolor="#FAFAF8",
        font=dict(family="system-ui, sans-serif", size=11),
        xaxis=dict(side="bottom"),
        margin=dict(l=10, r=10, t=30, b=10),
    )
    return fig


def build_overlap_histogram(df: pd.DataFrame) -> go.Figure:
    """Histogram of overlap scores by safety band."""
    cat_col = _cat_col(df)
    fig = go.Figure()
    for cat in CATEGORY_ORDER:
        cat_df = df[df[cat_col] == cat]
        if cat_df.empty:
            continue
        fig.add_trace(
            go.Histogram(
                x=cat_df["overlap_score"],
                name=LABEL_MAP.get(cat, cat),
                marker_color=COLOR_MAP.get(cat, "#888888"),
                opacity=0.75,
                xbins=dict(start=0, end=1, size=0.1),
            )
        )
    fig.update_layout(
        barmode="overlay",
        paper_bgcolor="#FAFAF8", plot_bgcolor="#FAFAF8",
        font=dict(family="system-ui, sans-serif", size=11),
        xaxis_title="Overlap score", yaxis_title="Count",
        legend=dict(font=dict(size=10)),
        margin=dict(l=10, r=10, t=10, b=40),
    )
    return fig


def build_blur_bar(blur_df: pd.DataFrame) -> go.Figure:
    """
    Horizontal bar chart of boundary blur scores, sorted descending.
    blur_df must have: topic/short_name, safety_band/category, boundary_blur_score.
    """
    cat_col = _cat_col(blur_df)
    short_col = _short_col(blur_df)
    # nlargest selects top-30; re-sort ascending so largest bar appears at chart top
    df = blur_df.nlargest(30, "boundary_blur_score").sort_values(
        "boundary_blur_score", ascending=True
    )

    colors = [COLOR_MAP.get(c, "#888888") for c in df[cat_col]]
    labels = df[short_col].str[:40]

    fig = go.Figure(
        go.Bar(
            x=df["boundary_blur_score"],
            y=labels,
            orientation="h",
            marker_color=colors,
            opacity=0.85,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Blur score: %{x:.3f}<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        paper_bgcolor="#FAFAF8", plot_bgcolor="#FAFAF8",
        font=dict(family="system-ui, sans-serif", size=11),
        xaxis=dict(title="Boundary blur score", range=[0, 1]),
        yaxis=dict(autorange="reversed" if False else True),
        margin=dict(l=10, r=20, t=10, b=40),
        height=max(300, len(df) * 22),
    )
    return fig


def build_centroid_sim_bar(row: pd.Series) -> go.Figure:
    """
    Bar chart of per-band centroid similarities for a single example.
    """
    sim_cols = {
        "Benign": "sim_to_benign",
        "Ambiguous": "sim_to_ambiguous",
        "Policy/Sanitized": "sim_to_policy_relevant_sanitized",
    }
    labels, values, colors = [], [], []
    band_colors = {
        "Benign": COLOR_MAP.get("benign", "#4E8098"),
        "Ambiguous": COLOR_MAP.get("ambiguous", "#D4A853"),
        "Policy/Sanitized": COLOR_MAP.get("policy_relevant_sanitized", "#C47C5A"),
    }
    for label, col in sim_cols.items():
        if col in row.index and pd.notna(row[col]):
            labels.append(label)
            values.append(float(row[col]))
            colors.append(band_colors[label])

    if not labels:
        return go.Figure()

    fig = go.Figure(
        go.Bar(
            x=labels, y=values,
            marker_color=colors, opacity=0.85,
            hovertemplate="<b>%{x}</b><br>Similarity: %{y:.3f}<extra></extra>",
        )
    )
    fig.update_layout(
        paper_bgcolor="#FAFAF8", plot_bgcolor="#FAFAF8",
        font=dict(family="system-ui, sans-serif", size=11),
        yaxis=dict(title="Cosine similarity", range=[0, 1]),
        xaxis=dict(title=""),
        margin=dict(l=10, r=10, t=10, b=30),
        height=220,
        showlegend=False,
    )
    return fig
