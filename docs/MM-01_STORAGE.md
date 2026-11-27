# Memory Storage Interface

**Status:** foundational software infrastructure. This module is not a cognitive or biological memory model.

## Contract

`MemoryStore` is a minimal in-memory container for fixed-dimensional boolean representations.

- Every item has a caller-supplied, non-empty string ID.
- Representations must be non-empty, one-dimensional NumPy-compatible boolean arrays.
- The first stored representation establishes the store dimensionality.
- Later representations must have the same dimensionality.
- Duplicate IDs are rejected rather than silently overwritten.
- Input arrays are copied on insertion; output arrays are copied on retrieval and removal.
- IDs are exposed in insertion order.
- Removing the last item or clearing the store resets its dimensionality.

## Example

```python
import numpy as np
from memory_machine.storage import MemoryStore

store = MemoryStore()
store.add("episode-001", np.array([True, False, True], dtype=np.bool_))
retrieved = store.get("episode-001")
```

## Scope boundary

The store does not rank memories, calculate similarity, perform pattern completion, infer latent states, or model hippocampal anatomy. Retrieval is intentionally kept in a separate package so storage and retrieval implementations can be varied independently.
