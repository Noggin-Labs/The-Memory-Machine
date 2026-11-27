"""Controlled cue degradation for episodic-memory experiments."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

BinaryPattern = NDArray[np.bool_]


@dataclass(frozen=True, slots=True)
class CueDegradation:
    """A degraded cue and metadata describing exactly what was changed."""

    cue: BinaryPattern
    mode: str
    corruption_probability: float
    removed_active_indices: tuple[int, ...]
    inserted_inactive_indices: tuple[int, ...]

    @property
    def n_removed(self) -> int:
        """Number of active features removed from the original pattern."""
        return len(self.removed_active_indices)

    @property
    def n_inserted(self) -> int:
        """Number of inactive features inserted into the cue."""
        return len(self.inserted_inactive_indices)

    @property
    def realized_corruption_fraction(self) -> float:
        """Changed-feature count divided by original active-feature count.

        For substitutions, each replacement changes two bit positions, so the
        returned fraction can be as high as 2.0. Missing-feature corruption
        changes one bit position per removed active feature.
        """
        # Recover original sparsity from cue sparsity and the recorded edits.
        original_active = int(self.cue.sum()) + self.n_removed - self.n_inserted
        if original_active == 0:
            return 0.0
        return (self.n_removed + self.n_inserted) / original_active


def _validate_pattern(pattern: ArrayLike) -> BinaryPattern:
    values = np.asarray(pattern)
    if values.ndim != 1:
        raise ValueError("pattern must be one-dimensional")
    if values.dtype != np.bool_:
        raise TypeError("pattern must have boolean dtype")
    if values.size == 0:
        raise ValueError("pattern must not be empty")
    return values.copy()


def _get_rng(
    *, seed: int | None, rng: np.random.Generator | None
) -> np.random.Generator:
    if (seed is None) == (rng is None):
        raise ValueError("supply exactly one of seed or rng")
    if seed is not None:
        if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)):
            raise TypeError("seed must be an integer")
        return np.random.default_rng(seed)
    if not isinstance(rng, np.random.Generator):
        raise TypeError("rng must be a numpy.random.Generator")
    return rng


def _validate_probability(probability: float) -> float:
    value = float(probability)
    if not np.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError("probability must be finite and in [0, 1]")
    return value


def make_missing_feature_cue(
    pattern: ArrayLike,
    *,
    drop_probability: float,
    seed: int | None = None,
    rng: np.random.Generator | None = None,
) -> CueDegradation:
    """Independently remove each active feature with probability p.

    The resulting cue has no inserted features and may have lower sparsity
    than the original pattern. The probability is a per-active-feature
    Bernoulli probability, not a guaranteed realized fraction.
    """
    original = _validate_pattern(pattern)
    probability = _validate_probability(drop_probability)
    generator = _get_rng(seed=seed, rng=rng)

    active = np.flatnonzero(original)
    removed = active[generator.random(active.size) < probability]
    cue = original.copy()
    cue[removed] = False
    return CueDegradation(
        cue=cue,
        mode="missing",
        corruption_probability=probability,
        removed_active_indices=tuple(int(i) for i in removed),
        inserted_inactive_indices=(),
    )


def make_substituted_cue(
    pattern: ArrayLike,
    *,
    substitution_probability: float,
    seed: int | None = None,
    rng: np.random.Generator | None = None,
) -> CueDegradation:
    """Replace selected active features with uniformly sampled inactive ones.

    Each original active feature is independently selected for replacement
    with probability p. Replacements are sampled without replacement from
    features inactive in the original pattern. The cue therefore preserves
    the original number of active features while changing feature identity.
    """
    original = _validate_pattern(pattern)
    probability = _validate_probability(substitution_probability)
    generator = _get_rng(seed=seed, rng=rng)

    active = np.flatnonzero(original)
    inactive = np.flatnonzero(~original)
    if inactive.size == 0 and probability > 0.0:
        raise ValueError("substitution requires at least one inactive feature")

    removed = active[generator.random(active.size) < probability]
    inserted = (
        generator.choice(inactive, size=removed.size, replace=False)
        if removed.size
        else np.array([], dtype=np.int64)
    )
    cue = original.copy()
    cue[removed] = False
    cue[inserted] = True
    return CueDegradation(
        cue=cue,
        mode="substitution",
        corruption_probability=probability,
        removed_active_indices=tuple(int(i) for i in removed),
        inserted_inactive_indices=tuple(int(i) for i in inserted),
    )
