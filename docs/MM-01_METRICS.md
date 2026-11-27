# MM-01 binary representation metrics

This module provides representation-level metrics for equal-length binary
vectors:

- **Hamming distance**: count of positions with different values.
- **Normalized Hamming distance**: Hamming distance divided by vector length.
- **Jaccard similarity**: intersection-over-union of active feature sets.

The functions require one-dimensional NumPy-compatible arrays with boolean
dtype and identical shapes. They deliberately reject implicit numeric-to-bool
conversion so that invalid encodings are not silently accepted.

For two empty active sets, Jaccard similarity is defined by convention as
1.0. Normalized Hamming distance is undefined for empty vectors and raises
ValueError.

These metrics describe binary representations only. They do not, by
themselves, establish information preservation, successful retrieval,
biological pattern separation, or memory performance. Apply Jaccard only
when active-set semantics are meaningful; apply Hamming only to equal-length
binary outputs.
