"""Utilities for constructing controlled sparse binary pattern pairs."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

BinaryPattern = NDArray[np.bool_]


@dataclass(frozen=True, slots=True)
class PatternPair:
    """A pair of fixed-sparsity binary patterns and its realized overlap."""

    reference: BinaryPattern
    comparison: BinaryPattern
    target_retention_probability: float
    shared_active: int
    realized_overlap: float


def make_overlapping_pair(
    *,
    n_features: int = 128,
    n_active: int = 16,
    retention_probability: float,
    seed: int | None = None,
    rng: np.random.Generator | None = None,
) -> PatternPair:
    """Generate fixed-sparsity binary patterns with stochastic controlled overlap.

    Each active feature in the reference is independently retained with
    probability p. Remaining active positions are sampled uniformly without
    replacement from features inactive in the reference.

    Supply exactly one of seed or rng. A seed creates a local Generator;
    a supplied Generator is advanced in place.
    """
    if isinstance(n_features, bool) or not isinstance(n_features, int):
        raise TypeError("n_features must be an integer")
    if isinstance(n_active, bool) or not isinstance(n_active, int):
        raise TypeError("n_active must be an integer")
    if n_features < 2:
        raise ValueError("n_features must be at least 2")
    if n_active < 1 or n_active > n_features // 2:
        raise ValueError("n_active must be between 1 and n_features // 2")

    probability = float(retention_probability)
    if not np.isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError("retention_probability must be finite and in [0, 1]")

    if (seed is None) == (rng is None):
        raise ValueError("supply exactly one of seed or rng")
    if seed is not None:
        if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)):
            raise TypeError("seed must be an integer")
        generator = np.random.default_rng(seed)
    else:
        if not isinstance(rng, np.random.Generator):
            raise TypeError("rng must be a numpy.random.Generator")
        generator = rng

    reference_indices = generator.choice(n_features, size=n_active, replace=False)
    reference = np.zeros(n_features, dtype=np.bool_)
    reference[reference_indices] = True

    retained = reference_indices[generator.random(n_active) < probability]
    n_to_sample = n_active - len(retained)
    inactive_indices = np.flatnonzero(~reference)
    added = generator.choice(inactive_indices, size=n_to_sample, replace=False)

    comparison = np.zeros(n_features, dtype=np.bool_)
    comparison[retained] = True
    comparison[added] = True

    shared = int(np.count_nonzero(reference & comparison))
    return PatternPair(
        reference=reference,
        comparison=comparison,
        target_retention_probability=probability,
        shared_active=shared,
        realized_overlap=shared / n_active,
    )
