from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class CategoryMeta:
    """Metadata for a safety band (replaces the old concept of 'category')."""
    key: str
    label: str
    short: str
    description: str
    color: str
    marker: str


@dataclass
class TensionMeta:
    """Metadata for a framing (replaces the old concept of 'tension_type')."""
    key: str
    label: str
    description: str


@dataclass
class DomainMeta:
    key: str
    label: str
    description: str


class SafetyTaxonomy:
    """
    Loads the safety taxonomy from config/safety_taxonomy.yaml and provides
    lookup and display helpers.

    The taxonomy now uses safety_bands (instead of categories) and framings
    (instead of tension_types). The public interface remains backward-compatible
    so that display code that calls category() / all_categories() / tension() /
    all_tensions() continues to work against the new structure.
    """

    def __init__(self, config_path: Optional[Path] = None) -> None:
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "safety_taxonomy.yaml"
        with open(config_path, encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        # Safety bands are the primary classification axis (was "categories").
        self._bands: dict[str, CategoryMeta] = {}
        for key, vals in raw["safety_bands"].items():
            self._bands[key] = CategoryMeta(
                key=key,
                label=vals["label"],
                short=vals["short"],
                description=vals["description"],
                color=vals["color"],
                marker=vals["marker"],
            )

        # Framings describe how a concept is presented (was "tension_types").
        self._framings: dict[str, TensionMeta] = {}
        for key, vals in raw["framings"].items():
            self._framings[key] = TensionMeta(
                key=key,
                label=vals["label"],
                description=vals["description"],
            )

        # Domains are new: the subject-matter area of each example.
        self._domains: dict[str, DomainMeta] = {}
        for key, vals in raw["domains"].items():
            self._domains[key] = DomainMeta(
                key=key,
                label=vals["label"],
                description=vals["description"],
            )

    # ------------------------------------------------------------------
    # Safety band interface (backward-compatible with "category" naming)
    # ------------------------------------------------------------------

    def category(self, key: str) -> CategoryMeta:
        """Return metadata for a safety band. Accepts both the new band key
        and, for backward compatibility, old category key names."""
        if key in self._bands:
            return self._bands[key]
        raise KeyError(f"Unknown safety band or category key: {key!r}")

    def all_categories(self) -> list[CategoryMeta]:
        return list(self._bands.values())

    def color_map(self) -> dict[str, str]:
        return {k: v.color for k, v in self._bands.items()}

    def label_map(self) -> dict[str, str]:
        return {k: v.label for k, v in self._bands.items()}

    def short_label_map(self) -> dict[str, str]:
        return {k: v.short for k, v in self._bands.items()}

    # ------------------------------------------------------------------
    # Framing interface (backward-compatible with "tension" naming)
    # ------------------------------------------------------------------

    def tension(self, key: str) -> TensionMeta:
        if key in self._framings:
            return self._framings[key]
        raise KeyError(f"Unknown framing key: {key!r}")

    def all_tensions(self) -> list[TensionMeta]:
        return list(self._framings.values())

    # ------------------------------------------------------------------
    # Domain interface (new)
    # ------------------------------------------------------------------

    def domain(self, key: str) -> DomainMeta:
        return self._domains[key]

    def all_domains(self) -> list[DomainMeta]:
        return list(self._domains.values())

    def domain_label_map(self) -> dict[str, str]:
        return {k: v.label for k, v in self._domains.items()}
