"""Binary-representation metrics used by MM-01."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def _validate_binary_pair(a: ArrayLike, b: ArrayLike) -> tuple[np.ndarray, np.ndarray]:
    """Return validated one-dimensional boolean arrays with matching shapes."""
    left = np.asarray(a)
    right = np.asarray(b)
    if left.ndim != 1 or right.ndim != 1:
        raise ValueError("patterns must be one-dimensional")
    if left.shape != right.shape:
        raise ValueError("patterns must have identical shapes")
    if left.dtype != np.bool_ or right.dtype != np.bool_:
        raise TypeError("patterns must have boolean dtype")
    return left, right


def hamming_distance(a: ArrayLike, b: ArrayLike) -> int:
    """Return the number of bit positions that differ."""
    left, right = _validate_binary_pair(a, b)
    return int(np.count_nonzero(left != right))


def normalized_hamming_distance(a: ArrayLike, b: ArrayLike) -> float:
    """Return differing positions divided by vector length."""
    left, right = _validate_binary_pair(a, b)
    if left.size == 0:
        raise ValueError("normalized Hamming distance is undefined for empty patterns")
    return float(np.count_nonzero(left != right) / left.size)


def jaccard_similarity(a: ArrayLike, b: ArrayLike) -> float:
    """Return intersection-over-union for active features.

    By convention, two empty active sets have Jaccard similarity 1.0.
    """
    left, right = _validate_binary_pair(a, b)
    intersection = int(np.count_nonzero(left & right))
    union = int(np.count_nonzero(left | right))
    if union == 0:
        return 1.0
    return intersection / union
