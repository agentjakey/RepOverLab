import numpy as np
import pytest

from src.similarity import (
    cosine_similarity_matrix,
    neighbors_for_concept,
    top_k_neighbors,
)


def normalized_random(n: int, d: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    vecs = rng.normal(0, 1, (n, d)).astype(np.float32)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs / norms


def test_similarity_matrix_shape():
    vecs = normalized_random(10, 32)
    sim = cosine_similarity_matrix(vecs)
    assert sim.shape == (10, 10)


def test_similarity_matrix_diagonal_is_one():
    vecs = normalized_random(8, 32)
    sim = cosine_similarity_matrix(vecs)
    diag = np.diag(sim)
    np.testing.assert_allclose(diag, np.ones(8), atol=1e-5)


def test_similarity_matrix_symmetric():
    vecs = normalized_random(10, 32)
    sim = cosine_similarity_matrix(vecs)
    np.testing.assert_allclose(sim, sim.T, atol=1e-5)


def test_similarity_values_in_range():
    vecs = normalized_random(15, 64)
    sim = cosine_similarity_matrix(vecs)
    assert float(sim.min()) >= 0.0
    assert float(sim.max()) <= 1.0 + 1e-5


def test_identical_vectors_have_similarity_one():
    vec = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
    vecs = np.repeat(vec, 3, axis=0)
    sim = cosine_similarity_matrix(vecs)
    np.testing.assert_allclose(sim, np.ones((3, 3)), atol=1e-5)


def test_top_k_neighbors_shape():
    vecs = normalized_random(20, 32)
    sim = cosine_similarity_matrix(vecs)
    indices, scores = top_k_neighbors(sim, k=5)
    assert indices.shape == (20, 5)
    assert scores.shape == (20, 5)


def test_top_k_neighbors_excludes_self():
    vecs = normalized_random(10, 32)
    sim = cosine_similarity_matrix(vecs)
    indices, _ = top_k_neighbors(sim, k=5, exclude_self=True)
    for i in range(10):
        assert i not in indices[i]


def test_top_k_neighbors_sorted_descending():
    vecs = normalized_random(10, 32)
    sim = cosine_similarity_matrix(vecs)
    _, scores = top_k_neighbors(sim, k=5)
    for row in scores:
        assert list(row) == sorted(row, reverse=True)


def test_neighbors_for_concept_returns_k_results():
    vecs = normalized_random(12, 32)
    sim = cosine_similarity_matrix(vecs)
    indices, scores = neighbors_for_concept(0, sim, k=6)
    assert len(indices) == 6
    assert len(scores) == 6


def test_neighbors_for_concept_scores_in_range():
    vecs = normalized_random(12, 32)
    sim = cosine_similarity_matrix(vecs)
    _, scores = neighbors_for_concept(0, sim, k=6)
    assert all(0.0 <= s <= 1.0 + 1e-5 for s in scores)


def test_zero_vector_handled_gracefully():
    vecs = np.zeros((3, 8), dtype=np.float32)
    sim = cosine_similarity_matrix(vecs)
    assert sim.shape == (3, 3)
    assert not np.any(np.isnan(sim))
