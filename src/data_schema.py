from __future__ import annotations

import re
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# ---------------------------------------------------------------------------
# New schema: SafeExample
# ---------------------------------------------------------------------------

FORBIDDEN_PATTERNS: list[str] = [
    r"\bhow to (make|build|create|synthesize|produce)\b.{0,50}\b(bomb|explosive|weapon|poison|virus|malware|ransomware)\b",
    r"\bsynthesis route\b",
    r"\bsynthesis (step|procedure|protocol)\b",
    r"\bexploit (chain|payload|code)\b",
    r"\bpayload delivery\b",
    r"\bpersistence mechanism\b",
    r"\bevasion technique\b",
    r"\bgrooming script\b",
    r"\bmanipulation (script|playbook|sequence)\b",
    r"\bfraud (script|scheme|tutorial)\b",
    r"\bhow to (launder|evade|bypass) (money|tax|detection|law enforcement)\b",
]

ABSTRACT_PLACEHOLDER_REQUIRED_PHRASE = "abstract placeholder for a disallowed category"


class SafetyBand(str, Enum):
    benign = "benign"
    capability_building = "capability_building"
    ambiguous = "ambiguous"
    policy_relevant_sanitized = "policy_relevant_sanitized"
    abstract_risk_placeholder = "abstract_risk_placeholder"


class Domain(str, Enum):
    biology = "biology"
    cybersecurity = "cybersecurity"
    persuasion = "persuasion"
    physics = "physics"
    AI_agents = "AI_agents"
    governance = "governance"
    education = "education"
    medicine = "medicine"
    climate = "climate"
    law_policy = "law_policy"


class Framing(str, Enum):
    educational = "educational"
    technical = "technical"
    casual = "casual"
    fictional = "fictional"
    policy = "policy"
    reflective = "reflective"
    abstract_placeholder = "abstract_placeholder"


class SafeExample(BaseModel):
    example_id: str = Field(..., pattern=r"^[A-Z]{2}\d{3}$")
    title: str = Field(..., min_length=3, max_length=200)
    content_text: str = Field(..., min_length=20, max_length=1500)
    domain: Domain
    topic: str = Field(..., min_length=2, max_length=100)
    safety_band: SafetyBand
    framing: Framing
    safe_summary: str = Field(..., min_length=10, max_length=500)
    why_interesting: str = Field(..., min_length=10, max_length=500)
    allowed_for_demo: bool
    notes: Optional[str] = Field(default="", max_length=400)

    @field_validator("content_text")
    @classmethod
    def content_text_no_urls(cls, v: str) -> str:
        if re.search(r"https?://|www\.", v, re.IGNORECASE):
            raise ValueError("content_text must not contain URLs")
        return v

    @field_validator("content_text")
    @classmethod
    def content_text_no_harmful_patterns(cls, v: str) -> str:
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError(
                    f"content_text matches a forbidden operational-detail pattern. "
                    f"Pattern: {pattern!r}. Rewrite to remove procedural specifics."
                )
        return v

    @model_validator(mode="after")
    def abstract_placeholder_rules(self) -> SafeExample:
        if self.safety_band == SafetyBand.abstract_risk_placeholder:
            if self.framing != Framing.abstract_placeholder:
                raise ValueError(
                    "abstract_risk_placeholder entries must use framing='abstract_placeholder'."
                )
            if ABSTRACT_PLACEHOLDER_REQUIRED_PHRASE not in self.content_text.lower():
                raise ValueError(
                    f"abstract_risk_placeholder entries must contain the phrase "
                    f"'{ABSTRACT_PLACEHOLDER_REQUIRED_PHRASE}' in content_text."
                )
        return self

    @model_validator(mode="after")
    def abstract_placeholder_allowed_for_demo(self) -> SafeExample:
        if self.safety_band == SafetyBand.abstract_risk_placeholder:
            if not self.allowed_for_demo:
                raise ValueError(
                    "abstract_risk_placeholder entries should have allowed_for_demo=True; "
                    "they exist specifically to populate the boundary region of the map."
                )
        return self

    model_config = {"str_strip_whitespace": True}


class SafeExampleDataset:
    def __init__(self, entries: list[SafeExample]) -> None:
        self.entries = entries

    def by_band(self, band: SafetyBand) -> list[SafeExample]:
        return [e for e in self.entries if e.safety_band == band]

    def by_domain(self, domain: Domain) -> list[SafeExample]:
        return [e for e in self.entries if e.domain == domain]

    def by_id(self, example_id: str) -> Optional[SafeExample]:
        for e in self.entries:
            if e.example_id == example_id:
                return e
        return None

    def ids(self) -> list[str]:
        return [e.example_id for e in self.entries]

    def band_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for e in self.entries:
            counts[e.safety_band.value] = counts.get(e.safety_band.value, 0) + 1
        return counts

    def domain_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for e in self.entries:
            counts[e.domain.value] = counts.get(e.domain.value, 0) + 1
        return counts

    def allowed_for_demo_entries(self) -> list[SafeExample]:
        return [e for e in self.entries if e.allowed_for_demo]


# ---------------------------------------------------------------------------
# Legacy schema kept for backward compatibility with older pipeline references.
# New code should use SafeExample and SafeExampleDataset.
# ---------------------------------------------------------------------------

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
