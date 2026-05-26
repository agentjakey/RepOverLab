from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from src.similarity import neighbors_for_concept


@dataclass
class NeighborResult:
    concept_id: str
    name: str
    short_name: str
    category: str
    tension_type: str
    similarity: float
    same_category: bool


def get_neighbors(
    concept_id: str,
    examples_df: pd.DataFrame,
    similarity_matrix: np.ndarray,
    k: int = 10,
    top_n: int = 5,
) -> list[NeighborResult]:
    """
    Given a concept ID, return its top-N nearest neighbors with metadata.
    """
    id_list = list(examples_df["id"])
    if concept_id not in id_list:
        return []

    idx = id_list.index(concept_id)
    source_category = examples_df.iloc[idx]["category"]

    neighbor_indices, neighbor_scores = neighbors_for_concept(
        concept_idx=idx,
        similarity_matrix=similarity_matrix,
        k=max(k, top_n),
        exclude_self=True,
    )

    results = []
    for pos, (j, score) in enumerate(zip(neighbor_indices, neighbor_scores)):
        if pos >= top_n:
            break
        row = examples_df.iloc[int(j)]
        results.append(
            NeighborResult(
                concept_id=row["id"],
                name=row["name"],
                short_name=row["short_name"],
                category=row["category"],
                tension_type=row["tension_type"],
                similarity=float(round(score, 4)),
                same_category=(row["category"] == source_category),
            )
        )
    return results
