import numpy as np
import pytest

from src.overlap import compute_overlap_scores, cross_category_affinity
from src.similarity import cosine_similarity_matrix


def make_clustered_embeddings(n_per_cat: int = 5, n_cats: int = 3, dim: int = 32, seed: int = 0):
    """
    Generate embeddings where each category is a tight cluster far from others.
    With tight clusters, overlap scores should be near 0.
    """
    rng = np.random.default_rng(seed)
    embeddings = []
    categories = []

    cat_names = [f"cat_{i}" for i in range(n_cats)]
    for i, cat in enumerate(cat_names):
        center = np.zeros(dim, dtype=np.float32)
        center[i * (dim // n_cats)] = 1.0
        for _ in range(n_per_cat):
            noise = rng.normal(0, 0.01, dim).astype(np.float32)
            vec = center + noise
            vec = vec / np.linalg.norm(vec)
            embeddings.append(vec)
            categories.append(cat)

    return np.stack(embeddings), categories


def make_mixed_embeddings(n: int = 10, dim: int = 32, seed: int = 1):
    """All embeddings near the same point - everyone is everyone's neighbor."""
    rng = np.random.default_rng(seed)
    center = np.ones(dim, dtype=np.float32) / np.sqrt(dim)
    embeddings = []
    categories = []
    cat_names = ["cat_a", "cat_b"]
    for i in range(n):
        noise = rng.normal(0, 0.005, dim).astype(np.float32)
        vec = center + noise
        vec = vec / np.linalg.norm(vec)
        embeddings.append(vec)
        categories.append(cat_names[i % 2])
    return np.stack(embeddings), categories


def test_overlap_zero_for_tight_clusters():
    embeddings, categories = make_clustered_embeddings(n_per_cat=8, n_cats=3)
    sim = cosine_similarity_matrix(embeddings)
    scores = compute_overlap_scores(sim, categories, k=6)
    assert scores.max() < 0.3, f"Expected low overlap for tight clusters, got {scores.max():.3f}"


def test_overlap_high_for_mixed_clusters():
    embeddings, categories = make_mixed_embeddings(n=20)
    sim = cosine_similarity_matrix(embeddings)
    scores = compute_overlap_scores(sim, categories, k=8)
    assert scores.mean() > 0.3, f"Expected high overlap for mixed embeddings, got {scores.mean():.3f}"


def test_overlap_scores_in_range():
    embeddings, categories = make_mixed_embeddings(n=15)
    sim = cosine_similarity_matrix(embeddings)
    scores = compute_overlap_scores(sim, categories, k=5)
    assert all(0.0 <= s <= 1.0 for s in scores)


def test_overlap_output_length_matches_input():
    embeddings, categories = make_clustered_embeddings(n_per_cat=4, n_cats=2)
    sim = cosine_similarity_matrix(embeddings)
    scores = compute_overlap_scores(sim, categories, k=3)
    assert len(scores) == len(categories)


def test_cross_category_affinity_returns_dataframe():
    embeddings, categories = make_mixed_embeddings(n=16)
    sim = cosine_similarity_matrix(embeddings)
    df = cross_category_affinity(sim, categories, k=5)
    assert "category_a" in df.columns
    assert "category_b" in df.columns
    assert "mean_similarity" in df.columns
    assert len(df) > 0


def test_cross_category_affinity_no_self_pairs():
    embeddings, categories = make_mixed_embeddings(n=16)
    sim = cosine_similarity_matrix(embeddings)
    df = cross_category_affinity(sim, categories, k=5)
    assert not any(df["category_a"] == df["category_b"])


def test_overlap_with_all_same_category():
    embeddings, _ = make_mixed_embeddings(n=10)
    sim = cosine_similarity_matrix(embeddings)
    categories = ["only_cat"] * 10
    scores = compute_overlap_scores(sim, categories, k=5)
    np.testing.assert_array_equal(scores, np.zeros(10, dtype=np.float32))


def test_overlap_dtype_is_float32():
    embeddings, categories = make_clustered_embeddings()
    sim = cosine_similarity_matrix(embeddings)
    scores = compute_overlap_scores(sim, categories, k=3)
    assert scores.dtype == np.float32
