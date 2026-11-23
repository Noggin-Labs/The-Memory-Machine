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

## Initial implementation boundary

This commit establishes package structure and a smoke test only. It does not implement or validate a pattern-separation, pattern-completion, or hippocampal model.
