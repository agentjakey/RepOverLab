from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class CategoryMeta:
    key: str
    label: str
    short: str
    description: str
    color: str
    marker: str


@dataclass
class TensionMeta:
    key: str
    label: str
    description: str


class SafetyTaxonomy:
    def __init__(self, config_path: Optional[Path] = None) -> None:
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "safety_taxonomy.yaml"
        with open(config_path, encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        self._categories: dict[str, CategoryMeta] = {}
        for key, vals in raw["categories"].items():
            self._categories[key] = CategoryMeta(
                key=key,
                label=vals["label"],
                short=vals["short"],
                description=vals["description"],
                color=vals["color"],
                marker=vals["marker"],
            )

        self._tensions: dict[str, TensionMeta] = {}
        for key, vals in raw["tension_types"].items():
            self._tensions[key] = TensionMeta(
                key=key,
                label=vals["label"],
                description=vals["description"],
            )

    def category(self, key: str) -> CategoryMeta:
        return self._categories[key]

    def tension(self, key: str) -> TensionMeta:
        return self._tensions[key]

    def all_categories(self) -> list[CategoryMeta]:
        return list(self._categories.values())

    def all_tensions(self) -> list[TensionMeta]:
        return list(self._tensions.values())

    def color_map(self) -> dict[str, str]:
        return {k: v.color for k, v in self._categories.items()}

    def label_map(self) -> dict[str, str]:
        return {k: v.label for k, v in self._categories.items()}

    def short_label_map(self) -> dict[str, str]:
        return {k: v.short for k, v in self._categories.items()}
