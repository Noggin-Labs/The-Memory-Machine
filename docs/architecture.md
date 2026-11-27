# Software architecture

The package separates six concerns so that candidate mechanisms can be compared without coupling their implementations.

| Package | Responsibility |
|---|---|
| data | Generate episodes, control pairwise input overlap, and degrade retrieval cues |
| encoding | Transform input episodes into internal representations |
| storage | Store representations and expose memory collections |
| retrieval | Retrieve or reconstruct an episode from a cue |
| evaluation | Quantify separation, information preservation, and retrieval performance |
| experiments | Manage conditions, random seeds, configurations, and result logging |

## Design constraints

1. Keep encoding, storage, and retrieval independently replaceable.
2. Make stochastic behaviour reproducible through explicit random-number generators or seeds.
3. Evaluate memories in the presence of competing episodes, not only in isolation.
4. Report separation together with information preservation and retrieval performance.
5. Distinguish missing-feature cues from feature substitutions.
6. Keep implementation checks separate from confirmatory scientific results.

## Current implementation boundary

The current software foundation includes:

- stochastic fixed-sparsity binary pattern-pair generation with recorded realized overlap;
- separate missing-feature and feature-substitution cue generators with explicit random sources and edit metadata;
- binary Hamming and Jaccard metrics with documented input and empty-set conventions;
- a minimal in-memory store for fixed-dimensional boolean representations.

These are infrastructure components. They do not implement or validate a pattern-separation, pattern-completion, retrieval, or hippocampal model. Encoding baselines, retrieval mechanisms, information-preservation measures, and confirmatory experiment orchestration remain to be specified and evaluated.
