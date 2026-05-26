import pytest
from pydantic import ValidationError

from src.data_schema import Category, ConceptDataset, ConceptEntry, TensionType


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


def test_valid_entry_parses():
    e = ConceptEntry(**valid_entry())
    assert e.id == "CB001"
    assert e.category == Category.clearly_benign


def test_invalid_id_format():
    with pytest.raises(ValidationError):
        ConceptEntry(**valid_entry(id="invalid"))


def test_invalid_category():
    with pytest.raises(ValidationError):
        ConceptEntry(**valid_entry(category="not_a_category"))


def test_invalid_tension_type():
    with pytest.raises(ValidationError):
        ConceptEntry(**valid_entry(tension_type="bad_type"))


def test_description_too_short():
    with pytest.raises(ValidationError):
        ConceptEntry(**valid_entry(description="Short."))


def test_description_no_urls():
    with pytest.raises(ValidationError):
        ConceptEntry(**valid_entry(description="See https://example.com for more information about this topic."))


def test_dataset_by_category():
    entries = [
        ConceptEntry(**valid_entry(id="CB001", category=Category.clearly_benign)),
        ConceptEntry(**valid_entry(id="DU001", category=Category.dual_use)),
        ConceptEntry(**valid_entry(id="DU002", category=Category.dual_use)),
    ]
    dataset = ConceptDataset(entries=entries)
    benign = dataset.by_category(Category.clearly_benign)
    dual = dataset.by_category(Category.dual_use)
    assert len(benign) == 1
    assert len(dual) == 2


def test_dataset_by_id():
    entries = [ConceptEntry(**valid_entry(id="CB001"))]
    dataset = ConceptDataset(entries=entries)
    found = dataset.by_id("CB001")
    assert found is not None
    assert found.id == "CB001"
    assert dataset.by_id("CB999") is None


def test_dataset_category_counts():
    entries = [
        ConceptEntry(**valid_entry(id="CB001", category=Category.clearly_benign)),
        ConceptEntry(**valid_entry(id="CB002", category=Category.clearly_benign)),
        ConceptEntry(**valid_entry(id="DU001", category=Category.dual_use)),
    ]
    dataset = ConceptDataset(entries=entries)
    counts = dataset.category_counts()
    assert counts["clearly_benign"] == 2
    assert counts["dual_use"] == 1


def test_all_categories_are_valid_enums():
    for cat in Category:
        assert cat.value in {
            "clearly_benign",
            "dual_use",
            "context_dependent",
            "sensitive_legitimate",
            "out_of_scope_abstract",
        }


def test_all_tension_types_are_valid_enums():
    for t in TensionType:
        assert t.value in {
            "none",
            "context_resolves",
            "domain_lens",
            "protective_vs_enabling",
            "abstraction_gap",
            "creative_cover",
        }
