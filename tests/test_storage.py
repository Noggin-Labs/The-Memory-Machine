import numpy as np
import pytest

from memory_machine.storage import MemoryStore


def test_add_get_and_insertion_order():
    store = MemoryStore()
    first = np.array([True, False, True], dtype=np.bool_)
    second = np.array([False, True, False], dtype=np.bool_)
    store.add("episode-1", first)
    store.add("episode-2", second)
    assert len(store) == 2
    assert store.dimension == 3
    assert store.ids == ("episode-1", "episode-2")
    np.testing.assert_array_equal(store.get("episode-1"), first)


def test_store_copies_inputs_and_outputs():
    store = MemoryStore()
    original = np.array([True, False, True], dtype=np.bool_)
    store.add("a", original)
    original[:] = False
    retrieved = store.get("a")
    retrieved[:] = False
    np.testing.assert_array_equal(
        store.get("a"), [True, False, True]
    )


def test_duplicate_id_rejected():
    store = MemoryStore()
    store.add("a", np.array([True, False], dtype=np.bool_))
    with pytest.raises(KeyError):
        store.add("a", np.array([False, True], dtype=np.bool_))


def test_dimension_mismatch_rejected_without_mutation():
    store = MemoryStore()
    store.add("a", np.array([True, False], dtype=np.bool_))
    with pytest.raises(ValueError):
        store.add("b", np.array([True, False, True], dtype=np.bool_))
    assert store.ids == ("a",)
    assert len(store) == 1


def test_remove_returns_copy_and_resets_dimension_when_empty():
    store = MemoryStore()
    store.add("a", np.array([True, False], dtype=np.bool_))
    removed = store.remove("a")
    removed[:] = False
    assert len(store) == 0
    assert store.dimension is None
    assert store.ids == ()


def test_clear_resets_store():
    store = MemoryStore()
    store.add("a", np.array([True, False], dtype=np.bool_))
    store.clear()
    assert len(store) == 0
    assert store.dimension is None


def test_unknown_id_rejected():
    store = MemoryStore()
    with pytest.raises(KeyError):
        store.get("missing")
    with pytest.raises(KeyError):
        store.remove("missing")


@pytest.mark.parametrize("memory_id", ["", "   "])
def test_empty_id_rejected(memory_id):
    store = MemoryStore()
    with pytest.raises(ValueError):
        store.add(memory_id, np.array([True], dtype=np.bool_))


def test_invalid_representations_rejected():
    store = MemoryStore()
    with pytest.raises(ValueError):
        store.add("matrix", np.ones((2, 2), dtype=np.bool_))
    with pytest.raises(ValueError):
        store.add("empty", np.array([], dtype=np.bool_))
    with pytest.raises(TypeError):
        store.add("numeric", [1, 0])


def test_non_string_id_rejected():
    store = MemoryStore()
    with pytest.raises(TypeError):
        store.add(1, np.array([True], dtype=np.bool_))
