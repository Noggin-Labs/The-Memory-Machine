# MM-01 input generator

The first implementation milestone provides a seeded generator for the
128-feature, 16-active input specification in MM-01_PROTOCOL_DRAFT.md.

Example:

    from memory_machine.data import make_overlapping_pair

    pair = make_overlapping_pair(retention_probability=0.4, seed=2026)
    print(pair.shared_active, pair.realized_overlap)

The returned PatternPair contains boolean NumPy arrays named reference and
comparison, the requested retention probability, the realized shared-active
count, and the realized overlap fraction.

For custom configurations, pass n_features and n_active. The current
construction requires 2 * n_active <= n_features so the comparison can
always be filled from features inactive in the reference at p=0.

Supply exactly one random source: an integer seed or an existing
numpy.random.Generator via rng. No global NumPy random state is used.
A supplied generator is advanced in place.

This module implements input-pair generation only. It does not implement
the four proposed transformations and does not establish a biological
pattern-separation effect.
