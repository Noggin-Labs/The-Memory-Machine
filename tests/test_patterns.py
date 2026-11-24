import numpy as np
import pytest

from memory_machine.data.patterns import make_overlapping_pair


def test_default_dimensions_and_exact_sparsity():
    pair = make_overlapping_pair(retention_probability=0.4, seed=7)
    assert pair.reference.shape == pair.comparison.shape == (128,)
    assert pair.reference.dtype == pair.comparison.dtype == np.bool_
    assert int(pair.reference.sum()) == int(pair.comparison.sum()) == 16


def test_zero_retention_is_disjoint():
    pair = make_overlapping_pair(retention_probability=0.0, seed=11)
    assert pair.shared_active == 0
    assert pair.realized_overlap == 0.0
    assert not np.any(pair.reference & pair.comparison)


def test_full_retention_is_identical():
    pair = make_overlapping_pair(retention_probability=1.0, seed=11)
    assert pair.shared_active == 16
    assert pair.realized_overlap == 1.0
    np.testing.assert_array_equal(pair.reference, pair.comparison)


def test_seed_reproducibility():
    a = make_overlapping_pair(retention_probability=0.6, seed=123)
    b = make_overlapping_pair(retention_probability=0.6, seed=123)
    np.testing.assert_array_equal(a.reference, b.reference)
    np.testing.assert_array_equal(a.comparison, b.comparison)
    assert a.shared_active == b.shared_active


def test_different_seeds_can_change_pair():
    a = make_overlapping_pair(retention_probability=0.5, seed=1)
    b = make_overlapping_pair(retention_probability=0.5, seed=2)
    assert not (np.array_equal(a.reference, b.reference) and
                np.array_equal(a.comparison, b.comparison))


def test_supplied_generator_is_accepted_and_advanced():
    rng = np.random.default_rng(5)
    a = make_overlapping_pair(retention_probability=0.5, rng=rng)
    b = make_overlapping_pair(retention_probability=0.5, rng=rng)
    assert not np.array_equal(a.reference, b.reference)


@pytest.mark.parametrize("p", [-0.01, 1.01, float("nan"), float("inf")])
def test_invalid_probability_rejected(p):
    with pytest.raises(ValueError):
        make_overlapping_pair(retention_probability=p, seed=1)


def test_exactly_one_random_source_required():
    with pytest.raises(ValueError):
        make_overlapping_pair(retention_probability=0.5)
    with pytest.raises(ValueError):
        make_overlapping_pair(retention_probability=0.5, seed=1,
                              rng=np.random.default_rng(1))


def test_invalid_dimensions_rejected():
    with pytest.raises(ValueError):
        make_overlapping_pair(n_features=128, n_active=65,
                              retention_probability=0.5, seed=1)
    with pytest.raises(ValueError):
        make_overlapping_pair(n_features=10, n_active=0,
                              retention_probability=0.5, seed=1)
    with pytest.raises(TypeError):
        make_overlapping_pair(n_features=128.0,
                              retention_probability=0.5, seed=1)
