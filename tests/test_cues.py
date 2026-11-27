import numpy as np
import pytest

from memory_machine.data.cues import (
    make_missing_feature_cue,
    make_substituted_cue,
)


def test_missing_cue_only_removes_active_features():
    pattern = np.array([True, False, True, False, True], dtype=np.bool_)
    result = make_missing_feature_cue(pattern, drop_probability=1.0, seed=4)
    np.testing.assert_array_equal(result.cue, [False, False, False, False, False])
    assert result.mode == "missing"
    assert result.n_removed == 3
    assert result.n_inserted == 0


def test_substitution_preserves_sparsity_and_changes_identity():
    pattern = np.array([True, False, True, False, False], dtype=np.bool_)
    result = make_substituted_cue(pattern, substitution_probability=1.0, seed=4)
    assert int(result.cue.sum()) == int(pattern.sum())
    assert result.n_removed == result.n_inserted == 2
    assert not np.any(result.cue & pattern)
    assert result.mode == "substitution"


def test_zero_probability_returns_identical_copy():
    pattern = np.array([True, False, True], dtype=np.bool_)
    missing = make_missing_feature_cue(pattern, drop_probability=0.0, seed=1)
    substituted = make_substituted_cue(
        pattern, substitution_probability=0.0, seed=1
    )
    np.testing.assert_array_equal(missing.cue, pattern)
    np.testing.assert_array_equal(substituted.cue, pattern)
    assert missing.cue is not pattern
    assert substituted.cue is not pattern


def test_seed_reproducibility():
    pattern = np.array([True, False, True, False, False], dtype=np.bool_)
    a = make_substituted_cue(pattern, substitution_probability=0.5, seed=7)
    b = make_substituted_cue(pattern, substitution_probability=0.5, seed=7)
    np.testing.assert_array_equal(a.cue, b.cue)
    assert a.removed_active_indices == b.removed_active_indices
    assert a.inserted_inactive_indices == b.inserted_inactive_indices


def test_supplied_generator_is_advanced():
    pattern = np.array([True, False, True, False, False], dtype=np.bool_)
    rng = np.random.default_rng(9)
    state_before = repr(rng.bit_generator.state)
    make_missing_feature_cue(pattern, drop_probability=0.5, rng=rng)
    assert repr(rng.bit_generator.state) != state_before


@pytest.mark.parametrize("function, keyword", [
    (make_missing_feature_cue, "drop_probability"),
    (make_substituted_cue, "substitution_probability"),
])
def test_invalid_probability_rejected(function, keyword):
    for value in (-0.1, 1.1, float("nan"), float("inf")):
        with pytest.raises(ValueError):
            function(np.array([True, False], dtype=np.bool_), **{keyword: value}, seed=1)


def test_substitution_rejects_pattern_without_inactive_features():
    pattern = np.ones(4, dtype=np.bool_)
    with pytest.raises(ValueError):
        make_substituted_cue(
            pattern, substitution_probability=0.5, seed=1
        )
    unchanged = make_substituted_cue(
        pattern, substitution_probability=0.0, seed=1
    )
    np.testing.assert_array_equal(unchanged.cue, pattern)


def test_realized_corruption_fraction_uses_original_active_count():
    pattern = np.array([True, False, True, False], dtype=np.bool_)
    missing = make_missing_feature_cue(pattern, drop_probability=1.0, seed=2)
    substituted = make_substituted_cue(
        pattern, substitution_probability=1.0, seed=2
    )
    assert missing.realized_corruption_fraction == 1.0
    assert substituted.realized_corruption_fraction == 2.0


def test_pattern_validation():
    with pytest.raises(ValueError):
        make_missing_feature_cue(np.ones((2, 2), dtype=np.bool_),
                                 drop_probability=0.5, seed=1)
    with pytest.raises(TypeError):
        make_missing_feature_cue([1, 0, 1], drop_probability=0.5, seed=1)


def test_exactly_one_random_source_required():
    pattern = np.array([True, False], dtype=np.bool_)
    with pytest.raises(ValueError):
        make_missing_feature_cue(pattern, drop_probability=0.5)
    with pytest.raises(ValueError):
        make_missing_feature_cue(
            pattern, drop_probability=0.5, seed=1,
            rng=np.random.default_rng(1)
        )
