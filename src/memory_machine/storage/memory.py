"""Simple in-memory storage for encoded episode representations."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

BinaryRepresentation = NDArray[np.bool_]


class MemoryStore:
    """Store fixed-dimensional binary representations under explicit IDs.

    This class is a transparent container, not a retrieval algorithm. Stored
    and returned arrays are copied so callers cannot mutate internal state
    through an input or a retrieved reference.
    """

    def __init__(self) -> None:
        self._items: dict[str, BinaryRepresentation] = {}
        self._dimension: int | None = None

    @staticmethod
    def _validate_id(memory_id: str) -> str:
        if not isinstance(memory_id, str):
            raise TypeError("memory_id must be a string")
        if not memory_id.strip():
            raise ValueError("memory_id must not be empty")
        return memory_id

    @staticmethod
    def _validate_representation(representation: ArrayLike) -> BinaryRepresentation:
        values = np.asarray(representation)
        if values.ndim != 1:
            raise ValueError("representation must be one-dimensional")
        if values.size == 0:
            raise ValueError("representation must not be empty")
        if values.dtype != np.bool_:
            raise TypeError("representation must have boolean dtype")
        return values.copy()

    @property
    def dimension(self) -> int | None:
        """Representation dimensionality, or None while the store is empty."""
        return self._dimension

    @property
    def ids(self) -> tuple[str, ...]:
        """Memory IDs in insertion order."""
        return tuple(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def add(self, memory_id: str, representation: ArrayLike) -> None:
        """Add a representation; duplicate IDs and dimension mismatches fail."""
        key = self._validate_id(memory_id)
        values = self._validate_representation(representation)
        if key in self._items:
            raise KeyError(f"memory ID already exists: {key}")
        if self._dimension is not None and values.size != self._dimension:
            raise ValueError(
                f"representation has dimension {values.size}; "
                f"store dimension is {self._dimension}"
            )
        self._items[key] = values
        if self._dimension is None:
            self._dimension = int(values.size)

    def get(self, memory_id: str) -> BinaryRepresentation:
        """Return a copy of the stored representation."""
        key = self._validate_id(memory_id)
        try:
            return self._items[key].copy()
        except KeyError:
            raise KeyError(f"unknown memory ID: {key}") from None

    def remove(self, memory_id: str) -> BinaryRepresentation:
        """Remove an item and return a copy of its representation."""
        key = self._validate_id(memory_id)
        try:
            removed = self._items.pop(key).copy()
        except KeyError:
            raise KeyError(f"unknown memory ID: {key}") from None
        if not self._items:
            self._dimension = None
        return removed

    def clear(self) -> None:
        """Remove all stored representations."""
        self._items.clear()
        self._dimension = None
