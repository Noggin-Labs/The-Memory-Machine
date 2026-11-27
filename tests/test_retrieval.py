import numpy as np
import pytest

from memory_machine.retrieval import nearest_memories, rank_memories
from memory_machine.storage import MemoryStore


def _store():
    store = MemoryStore()
    store.add("first", np.array([True, False, False], dtype=np.bool_))
    store.add("second", np.array([True, True, False], dtype=np.bool_))
    store.add("third", np.array([False, False, True], dtype=np.bool_))
    return store


def test_rank_memories_orders_by_ascending_hamming_distance():
    ranked = rank_memories(np.array([True, True, False], dtype=np.bool_), _store())
    assert [(m.memory_id, m.distance) for m in ranked] == [
        ("second", 0), ("first", 1), ("third", 3)
    ]


def test_nearest_memories_returns_all_ties_in_insertion_order():
    store = MemoryStore()
    store.add("left", np.array([True, False], dtype=np.bool_))
    store.add("right", np.array([False, True], dtype=np.bool_))
    nearest = nearest_memories(np.array([True, True], dtype=np.bool_), store)
    assert [(m.memory_id, m.distance) for m in nearest] == [
        ("left", 1), ("right", 1)
    ]


def test_empty_store_returns_no_matches():
    empty = MemoryStore()
    cue = np.array([True, False], dtype=np.bool_)
    assert rank_memories(cue, empty) == ()
    assert nearest_memories(cue, empty) == ()


def test_dimension_mismatch_rejected():
    with pytest.raises(ValueError):
        rank_memories(np.array([True, False], dtype=np.bool_), _store())


def test_invalid_cue_rejected():
    store = _store()
    with pytest.raises(ValueError):
        rank_memories(np.ones((2, 2), dtype=np.bool_), store)
    with pytest.raises(ValueError):
        rank_memories(np.array([], dtype=np.bool_), store)
    with pytest.raises(TypeError):
        rank_memories([1, 0, 1], store)


def test_non_store_rejected():
    with pytest.raises(TypeError):
        rank_memories(np.array([True, False], dtype=np.bool_), [])
