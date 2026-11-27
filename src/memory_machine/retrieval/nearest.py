"""Transparent nearest-neighbour retrieval baselines."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from memory_machine.evaluation.metrics import hamming_distance
from memory_machine.storage import MemoryStore


@dataclass(frozen=True, slots=True)
class RetrievalMatch:
    """A stored memory ID and its Hamming distance from a cue."""

    memory_id: str
    distance: int


def _validate_cue(cue: ArrayLike) -> np.ndarray:
    values = np.asarray(cue)
    if values.ndim != 1:
        raise ValueError("cue must be one-dimensional")
    if values.size == 0:
        raise ValueError("cue must not be empty")
    if values.dtype != np.bool_:
        raise TypeError("cue must have boolean dtype")
    return values.copy()


def rank_memories(
    cue: ArrayLike,
    store: MemoryStore,
) -> tuple[RetrievalMatch, ...]:
    """Rank all stored representations by ascending Hamming distance.

    Ties preserve the MemoryStore insertion order. This is a nearest-neighbour
    baseline only: it returns stored IDs and distances and does not reconstruct
    missing features or synthesize a new representation.
    """
    query = _validate_cue(cue)
    if not isinstance(store, MemoryStore):
        raise TypeError("store must be a MemoryStore")
    if len(store) == 0:
        return ()
    if store.dimension != query.size:
        raise ValueError(
            f"cue has dimension {query.size}; store dimension is {store.dimension}"
        )

    matches = [
        RetrievalMatch(memory_id=memory_id,
                       distance=hamming_distance(query, store.get(memory_id)))
        for memory_id in store.ids
    ]
    return tuple(sorted(matches, key=lambda match: match.distance))


def nearest_memories(
    cue: ArrayLike,
    store: MemoryStore,
) -> tuple[RetrievalMatch, ...]:
    """Return every memory tied for the minimum Hamming distance.

    Returning all ties avoids silently imposing an arbitrary winner when the
    cue is equally close to multiple stored representations. The empty store
    produces an empty tuple.
    """
    ranked = rank_memories(cue, store)
    if not ranked:
        return ()
    best_distance = ranked[0].distance
    return tuple(match for match in ranked if match.distance == best_distance)
