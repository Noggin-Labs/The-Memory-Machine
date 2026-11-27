import numpy as np
import pytest

from memory_machine.evaluation.metrics import (
    hamming_distance,
    jaccard_similarity,
    normalized_hamming_distance,
)


def test_identical_patterns_have_zero_hamming_distance():
    a = np.array([True, False, True], dtype=np.bool_)
    assert hamming_distance(a, a.copy()) == 0
    assert normalized_hamming_distance(a, a.copy()) == 0.0


def test_hamming_distance_counts_different_positions():
    a = np.array([True, False, True, False], dtype=np.bool_)
    b = np.array([True, True, False, False], dtype=np.bool_)
    assert hamming_distance(a, b) == 2
    assert normalized_hamming_distance(a, b) == 0.5


def test_jaccard_similarity_uses_active_set_intersection_over_union():
    a = np.array([True, True, False, False], dtype=np.bool_)
    b = np.array([False, True, True, False], dtype=np.bool_)
    assert jaccard_similarity(a, b) == pytest.approx(1 / 3)


def test_jaccard_similarity_of_two_empty_sets_is_one():
    empty = np.zeros(4, dtype=np.bool_)
    assert jaccard_similarity(empty, empty) == 1.0


@pytest.mark.parametrize(
    ("a", "b", "error"),
    [
        (np.array([True]), np.array([True, False]), ValueError),
        (np.array([[True, False]]), np.array([[True, False]]), ValueError),
        (np.array([1, 0]), np.array([1, 0]), TypeError),
    ],
)
def test_metrics_reject_invalid_inputs(a, b, error):
    with pytest.raises(error):
        hamming_distance(a, b)


def test_normalized_hamming_rejects_empty_patterns():
    empty = np.array([], dtype=np.bool_)
    with pytest.raises(ValueError):
        normalized_hamming_distance(empty, empty)
