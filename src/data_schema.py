from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Category(str, Enum):
    clearly_benign = "clearly_benign"
    dual_use = "dual_use"
    context_dependent = "context_dependent"
    sensitive_legitimate = "sensitive_legitimate"
    out_of_scope_abstract = "out_of_scope_abstract"


class TensionType(str, Enum):
    none = "none"
    context_resolves = "context_resolves"
    domain_lens = "domain_lens"
    protective_vs_enabling = "protective_vs_enabling"
    abstraction_gap = "abstraction_gap"
    creative_cover = "creative_cover"


class ConceptEntry(BaseModel):
    id: str = Field(..., pattern=r"^[A-Z]{2}\d{3}$")
    name: str = Field(..., min_length=3, max_length=120)
    short_name: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=20, max_length=600)
    category: Category
    tension_type: TensionType
    legitimate_use_note: Optional[str] = Field(default="", max_length=300)

    @field_validator("description")
    @classmethod
    def description_no_urls(cls, v: str) -> str:
        import re
        if re.search(r"https?://|www\.", v, re.IGNORECASE):
            raise ValueError("descriptions must not contain URLs")
        return v

    @field_validator("description")
    @classmethod
    def description_no_harmful_patterns(cls, v: str) -> str:
        forbidden = [
            r"\bstep[- ]by[- ]step\b",
            r"\brecipe\b",
            r"\bsynthesis route\b",
            r"\bhow to make\b.{0,30}\bbomb\b",
        ]
        import re
        for pattern in forbidden:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError(f"description matches a forbidden pattern: {pattern}")
        return v

    model_config = {"str_strip_whitespace": True}


class ConceptDataset(BaseModel):
    entries: list[ConceptEntry]

    def by_category(self, category: Category) -> list[ConceptEntry]:
        return [e for e in self.entries if e.category == category]

    def by_id(self, entry_id: str) -> Optional[ConceptEntry]:
        for e in self.entries:
            if e.id == entry_id:
                return e
        return None

    def ids(self) -> list[str]:
        return [e.id for e in self.entries]

    def category_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for e in self.entries:
            counts[e.category.value] = counts.get(e.category.value, 0) + 1
        return counts
