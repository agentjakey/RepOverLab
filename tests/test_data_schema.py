import pytest
from pydantic import ValidationError

from src.data_schema import (
    Category,
    ConceptDataset,
    ConceptEntry,
    Domain,
    Framing,
    SafeExample,
    SafeExampleDataset,
    SafetyBand,
    TensionType,
)


# ---------------------------------------------------------------------------
# SafeExample helpers
# ---------------------------------------------------------------------------

def valid_safe_entry(**kwargs) -> dict:
    base = {
        "example_id": "BL001",
        "title": "How CRISPR gene editing works",
        "content_text": (
            "CRISPR-Cas9 is a molecular tool that allows precise editing of DNA sequences "
            "in living organisms. Scientists use guide RNA to direct the Cas9 protein to a "
            "specific genomic location where it makes a cut. The cell then repairs the cut "
            "using natural repair mechanisms. This technology has applications in medicine, "
            "agriculture, and basic research."
        ),
        "domain": Domain.biology,
        "topic": "CRISPR gene editing",
        "safety_band": SafetyBand.benign,
        "framing": Framing.educational,
        "safe_summary": "An overview of CRISPR-Cas9 gene editing mechanisms and applications.",
        "why_interesting": "Sits at the boundary between legitimate science education and biosecurity.",
        "allowed_for_demo": True,
        "notes": "",
    }
    base.update(kwargs)
    return base


def test_valid_safe_entry_parses():
    e = SafeExample(**valid_safe_entry())
    assert e.example_id == "BL001"
    assert e.safety_band == SafetyBand.benign
    assert e.domain == Domain.biology
    assert e.framing == Framing.educational
    assert e.allowed_for_demo is True


def test_invalid_example_id_format():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(example_id="invalid"))


def test_invalid_example_id_lowercase():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(example_id="bl001"))


def test_invalid_safety_band():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(safety_band="not_a_band"))


def test_invalid_framing():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(framing="bad_framing"))


def test_invalid_domain():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(domain="not_a_domain"))


def test_content_text_too_short():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(content_text="Too short."))


def test_content_text_rejects_urls():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(
            content_text="See https://example.com for more on this topic. " * 3
        ))


def test_content_text_rejects_www_urls():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(
            content_text="Visit www.example.com for detailed synthesis instructions. " * 3
        ))


def test_content_text_rejects_synthesis_route():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(
            content_text=(
                "The synthesis route for this compound involves the following steps "
                "and requires laboratory access to complete the procedure successfully."
            )
        ))


def test_content_text_rejects_exploit_chain():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(
            content_text=(
                "This exploit chain allows attackers to escalate privileges by combining "
                "three separate vulnerabilities in sequence across systems and networks."
            )
        ))


def test_content_text_rejects_grooming_script():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(
            content_text=(
                "This grooming script was used by perpetrators to build trust with victims "
                "over several months before the abuse began in the reported cases."
            )
        ))


def test_abstract_placeholder_requires_correct_framing():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(
            safety_band=SafetyBand.abstract_risk_placeholder,
            framing=Framing.educational,
            content_text=(
                "This is an abstract placeholder for a disallowed category of content. "
                "No operational details are included in this entry for demonstration purposes."
            ),
        ))


def test_abstract_placeholder_requires_phrase():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(
            safety_band=SafetyBand.abstract_risk_placeholder,
            framing=Framing.abstract_placeholder,
            content_text=(
                "This entry represents a restricted category. No details are provided "
                "and no operational guidance is given in this demonstration entry."
            ),
        ))


def test_abstract_placeholder_valid():
    e = SafeExample(**valid_safe_entry(
        example_id="OS001",
        safety_band=SafetyBand.abstract_risk_placeholder,
        framing=Framing.abstract_placeholder,
        allowed_for_demo=True,
        content_text=(
            "This is an abstract placeholder for a disallowed category involving operational "
            "weapons synthesis instructions. No operational details are included. This entry "
            "exists to show that restricted content clusters exist in embedding space."
        ),
    ))
    assert e.safety_band == SafetyBand.abstract_risk_placeholder


def test_abstract_placeholder_must_be_allowed_for_demo():
    with pytest.raises(ValidationError):
        SafeExample(**valid_safe_entry(
            safety_band=SafetyBand.abstract_risk_placeholder,
            framing=Framing.abstract_placeholder,
            allowed_for_demo=False,
            content_text=(
                "This is an abstract placeholder for a disallowed category involving operational "
                "weapons synthesis instructions. No operational details are included."
            ),
        ))


def test_allowed_for_demo_bool_true():
    e = SafeExample(**valid_safe_entry(allowed_for_demo=True))
    assert e.allowed_for_demo is True


def test_allowed_for_demo_bool_false():
    e = SafeExample(**valid_safe_entry(allowed_for_demo=False))
    assert e.allowed_for_demo is False


# ---------------------------------------------------------------------------
# SafeExampleDataset helpers
# ---------------------------------------------------------------------------

def _make_entry(example_id: str, band: SafetyBand, domain: Domain) -> SafeExample:
    return SafeExample(**valid_safe_entry(example_id=example_id, safety_band=band, domain=domain))


def test_dataset_band_counts():
    entries = [
        _make_entry("BL001", SafetyBand.benign, Domain.biology),
        _make_entry("BL002", SafetyBand.benign, Domain.biology),
        _make_entry("CY001", SafetyBand.capability_building, Domain.cybersecurity),
    ]
    ds = SafeExampleDataset(entries)
    counts = ds.band_counts()
    assert counts["benign"] == 2
    assert counts["capability_building"] == 1


def test_dataset_by_band():
    entries = [
        _make_entry("BL001", SafetyBand.benign, Domain.biology),
        _make_entry("CY001", SafetyBand.capability_building, Domain.cybersecurity),
        _make_entry("CY002", SafetyBand.capability_building, Domain.cybersecurity),
    ]
    ds = SafeExampleDataset(entries)
    assert len(ds.by_band(SafetyBand.benign)) == 1
    assert len(ds.by_band(SafetyBand.capability_building)) == 2


def test_dataset_by_domain():
    entries = [
        _make_entry("BL001", SafetyBand.benign, Domain.biology),
        _make_entry("BL002", SafetyBand.benign, Domain.biology),
        _make_entry("CY001", SafetyBand.capability_building, Domain.cybersecurity),
    ]
    ds = SafeExampleDataset(entries)
    assert len(ds.by_domain(Domain.biology)) == 2
    assert len(ds.by_domain(Domain.cybersecurity)) == 1


def test_dataset_by_id():
    entries = [_make_entry("BL001", SafetyBand.benign, Domain.biology)]
    ds = SafeExampleDataset(entries)
    found = ds.by_id("BL001")
    assert found is not None
    assert found.example_id == "BL001"
    assert ds.by_id("XX999") is None


def test_dataset_ids():
    entries = [
        _make_entry("BL001", SafetyBand.benign, Domain.biology),
        _make_entry("CY001", SafetyBand.capability_building, Domain.cybersecurity),
    ]
    ds = SafeExampleDataset(entries)
    assert ds.ids() == ["BL001", "CY001"]


def test_dataset_allowed_for_demo():
    e1 = SafeExample(**valid_safe_entry(example_id="BL001", allowed_for_demo=True))
    e2 = SafeExample(**valid_safe_entry(example_id="BL002", allowed_for_demo=False))
    ds = SafeExampleDataset([e1, e2])
    allowed = ds.allowed_for_demo_entries()
    assert len(allowed) == 1
    assert allowed[0].example_id == "BL001"


def test_all_safety_bands_valid():
    expected = {"benign", "capability_building", "ambiguous", "policy_relevant_sanitized", "abstract_risk_placeholder"}
    assert {b.value for b in SafetyBand} == expected


def test_all_framings_valid():
    expected = {"educational", "technical", "casual", "fictional", "policy", "reflective", "abstract_placeholder"}
    assert {f.value for f in Framing} == expected


def test_all_domains_valid():
    expected = {
        "biology", "cybersecurity", "persuasion", "physics", "AI_agents",
        "governance", "education", "medicine", "climate", "law_policy",
    }
    assert {d.value for d in Domain} == expected


# ---------------------------------------------------------------------------
# Legacy ConceptEntry (backward compat)
# ---------------------------------------------------------------------------

def valid_entry(**kwargs) -> dict:
    base = {
        "id": "CB001",
        "name": "How photosynthesis works",
        "short_name": "Photosynthesis",
        "description": "Plants convert sunlight into chemical energy through photosynthesis.",
        "category": Category.clearly_benign,
        "tension_type": TensionType.none,
        "legitimate_use_note": "",
    }
    base.update(kwargs)
    return base


def test_legacy_valid_entry_parses():
    e = ConceptEntry(**valid_entry())
    assert e.id == "CB001"
    assert e.category == Category.clearly_benign


def test_legacy_invalid_id_format():
    with pytest.raises(ValidationError):
        ConceptEntry(**valid_entry(id="invalid"))


def test_legacy_invalid_category():
    with pytest.raises(ValidationError):
        ConceptEntry(**valid_entry(category="not_a_category"))


def test_legacy_dataset_by_category():
    entries = [
        ConceptEntry(**valid_entry(id="CB001", category=Category.clearly_benign)),
        ConceptEntry(**valid_entry(id="DU001", category=Category.dual_use)),
        ConceptEntry(**valid_entry(id="DU002", category=Category.dual_use)),
    ]
    dataset = ConceptDataset(entries=entries)
    assert len(dataset.by_category(Category.clearly_benign)) == 1
    assert len(dataset.by_category(Category.dual_use)) == 2
