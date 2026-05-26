from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd

from src.similarity import neighbors_for_concept


@dataclass
class NeighborResult:
    example_id: str
    title: str
    topic: str
    safety_band: str
    domain: str
    framing: str
    safe_summary: str
    similarity: float
    same_band: bool


def _id_col(df: pd.DataFrame) -> str:
    return "id" if "id" in df.columns else "example_id"


def _col(df: pd.DataFrame, *candidates: str, default: str = "") -> str:
    """Return the first column name that exists in df."""
    for c in candidates:
        if c in df.columns:
            return c
    return default


def get_neighbors(
    example_id: str,
    examples_df: pd.DataFrame,
    similarity_matrix: np.ndarray,
    k: int = 10,
    top_n: int = 5,
    cross_band_only: bool = False,
) -> list[NeighborResult]:
    """
    Return the top-N nearest neighbors for a given example ID.

    If cross_band_only=True, only return neighbors whose safety_band
    differs from the source example's safety_band.
    """
    id_col = _id_col(examples_df)
    id_list = list(examples_df[id_col])
    if example_id not in id_list:
        return []

    idx = id_list.index(example_id)

    band_col = _col(examples_df, "safety_band", "category")
    title_col = _col(examples_df, "title", "name")
    topic_col = _col(examples_df, "topic", "short_name")
    domain_col = _col(examples_df, "domain")
    framing_col = _col(examples_df, "framing", "tension_type")
    summary_col = _col(examples_df, "safe_summary", "description")

    source_band = str(examples_df.iloc[idx].get(band_col, ""))

    neighbor_indices, neighbor_scores = neighbors_for_concept(
        concept_idx=idx,
        similarity_matrix=similarity_matrix,
        k=len(examples_df) - 1,
        exclude_self=True,
    )

    results = []
    for j, score in zip(neighbor_indices, neighbor_scores):
        row = examples_df.iloc[int(j)]
        nb_band = str(row.get(band_col, ""))
        if cross_band_only and nb_band == source_band:
            continue
        results.append(
            NeighborResult(
                example_id=str(row.get(id_col, "")),
                title=str(row.get(title_col, "")),
                topic=str(row.get(topic_col, "")),
                safety_band=nb_band,
                domain=str(row.get(domain_col, "")),
                framing=str(row.get(framing_col, "")),
                safe_summary=str(row.get(summary_col, "")),
                similarity=float(round(score, 4)),
                same_band=(nb_band == source_band),
            )
        )
        if len(results) >= top_n:
            break

    return results
