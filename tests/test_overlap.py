import numpy as np
import pytest

from src.overlap import (
    compute_overlap_scores,
    compute_nearest_cross_band_sim,
    compute_centroid_sims,
    compute_boundary_blur_score,
    cross_category_affinity,
)
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


# ---------------------------------------------------------------------------
# compute_overlap_scores (existing tests preserved)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# compute_nearest_cross_band_sim
# ---------------------------------------------------------------------------

def test_nearest_cross_band_sim_in_range():
    embeddings, categories = make_mixed_embeddings(n=20)
    sim = cosine_similarity_matrix(embeddings)
    result = compute_nearest_cross_band_sim(sim, categories)
    assert len(result) == len(categories)
    assert float(result.min()) >= 0.0
    assert float(result.max()) <= 1.0 + 1e-5


def test_nearest_cross_band_sim_zero_for_single_band():
    embeddings, _ = make_mixed_embeddings(n=10)
    sim = cosine_similarity_matrix(embeddings)
    categories = ["only_band"] * 10
    result = compute_nearest_cross_band_sim(sim, categories)
    assert float(result.max()) == 0.0


def test_nearest_cross_band_sim_high_for_mixed():
    embeddings, categories = make_mixed_embeddings(n=20)
    sim = cosine_similarity_matrix(embeddings)
    result = compute_nearest_cross_band_sim(sim, categories)
    # All embeddings are near the same point so cross-band sims should be high.
    assert result.mean() > 0.5


def test_nearest_cross_band_sim_dtype():
    embeddings, categories = make_mixed_embeddings(n=10)
    sim = cosine_similarity_matrix(embeddings)
    result = compute_nearest_cross_band_sim(sim, categories)
    assert result.dtype == np.float32


# ---------------------------------------------------------------------------
# compute_centroid_sims
# ---------------------------------------------------------------------------

def test_centroid_sims_returns_dict():
    embeddings, categories = make_mixed_embeddings(n=20)
    result = compute_centroid_sims(embeddings, categories, reference_bands=["cat_a", "cat_b"])
    assert isinstance(result, dict)
    assert "cat_a" in result
    assert "cat_b" in result


def test_centroid_sims_shape():
    embeddings, categories = make_mixed_embeddings(n=20)
    result = compute_centroid_sims(embeddings, categories, reference_bands=["cat_a", "cat_b"])
    for band, arr in result.items():
        assert arr.shape == (20,)
        assert arr.dtype == np.float32


def test_centroid_sims_values_in_range():
    embeddings, categories = make_mixed_embeddings(n=20)
    result = compute_centroid_sims(embeddings, categories, reference_bands=["cat_a", "cat_b"])
    for band, arr in result.items():
        assert float(arr.min()) >= 0.0
        assert float(arr.max()) <= 1.0 + 1e-5


def test_centroid_sims_omits_missing_band():
    embeddings, categories = make_mixed_embeddings(n=20)
    # "cat_z" has no members; should be absent from result.
    result = compute_centroid_sims(
        embeddings, categories, reference_bands=["cat_a", "cat_b", "cat_z"]
    )
    assert "cat_z" not in result
    assert "cat_a" in result


def test_centroid_sims_own_band_higher_for_tight_clusters():
    embeddings, categories = make_clustered_embeddings(n_per_cat=8, n_cats=2, dim=32)
    # cat_0 and cat_1 are far apart
    result = compute_centroid_sims(
        embeddings, categories, reference_bands=["cat_0", "cat_1"]
    )
    # For cat_0 members (first 8), sim_to_cat_0 should exceed sim_to_cat_1.
    for i in range(8):
        assert result["cat_0"][i] > result["cat_1"][i]


# ---------------------------------------------------------------------------
# compute_boundary_blur_score
# ---------------------------------------------------------------------------

def test_boundary_blur_in_range():
    embeddings, categories = make_mixed_embeddings(n=20)
    c_sims = compute_centroid_sims(embeddings, categories, reference_bands=["cat_a", "cat_b"])
    blur = compute_boundary_blur_score(c_sims)
    assert len(blur) == 20
    assert float(blur.min()) >= 0.0
    assert float(blur.max()) <= 1.0 + 1e-5


def test_boundary_blur_dtype():
    embeddings, categories = make_mixed_embeddings(n=20)
    c_sims = compute_centroid_sims(embeddings, categories, reference_bands=["cat_a", "cat_b"])
    blur = compute_boundary_blur_score(c_sims)
    assert blur.dtype == np.float32


def test_boundary_blur_zero_for_single_band():
    embeddings, _ = make_mixed_embeddings(n=10)
    # Only one band in the centroid sims dict.
    c_sims = {"only_band": np.ones(10, dtype=np.float32) * 0.8}
    blur = compute_boundary_blur_score(c_sims)
    np.testing.assert_array_equal(blur, np.zeros(10, dtype=np.float32))


def test_boundary_blur_high_for_equidistant():
    # Construct c_sims where all bands have the same similarity -> max entropy.
    n = 10
    n_bands = 3
    c_sims = {f"band_{i}": np.full(n, 0.5, dtype=np.float32) for i in range(n_bands)}
    blur = compute_boundary_blur_score(c_sims)
    # Equidistant means max entropy -> blur should be near 1.
    assert float(blur.mean()) > 0.95


def test_boundary_blur_low_for_clustered():
    # One band dominates strongly; others are near zero.
    n = 10
    c_sims = {
        "dominant": np.full(n, 0.95, dtype=np.float32),
        "weak_a": np.full(n, 0.05, dtype=np.float32),
        "weak_b": np.full(n, 0.02, dtype=np.float32),
    }
    blur = compute_boundary_blur_score(c_sims)
    # Strong dominance -> low entropy -> low blur.
    assert float(blur.mean()) < 0.3


def test_boundary_blur_empty_dict():
    blur = compute_boundary_blur_score({})
    assert len(blur) == 0
