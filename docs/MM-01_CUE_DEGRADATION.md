# MM-01 Cue Degradation Utilities

**Status:** implementation specification for exploratory software infrastructure. These utilities do not constitute a biological model or evidence of memory retrieval.

## Two distinct cue-corruption conditions

The data layer implements two deliberately separate operations:

1. **Missing-feature cue:** each active feature in the original pattern is independently removed with probability (p). No inactive feature is inserted, so cue sparsity can decrease.
2. **Feature-substitution cue:** each active feature is independently selected with probability (p), then replaced by a uniformly sampled feature that was inactive in the original pattern. Sampling is without replacement. The cue retains the original active-feature count, but feature identity changes.

The parameter (p) is a Bernoulli selection probability. It does not guarantee an exact number or fraction of changed features in an individual cue. The returned metadata records the actual removed and inserted indices.

## Reproducibility and validation

Both functions require exactly one random source: an integer `seed` or a caller-supplied `numpy.random.Generator`. A seed creates a local generator; a supplied generator is advanced in place. Inputs must be non-empty, one-dimensional boolean arrays. Probabilities must be finite and lie in ([0,1]).

## API

```python
from memory_machine.data.cues import (
    make_missing_feature_cue,
    make_substituted_cue,
)

missing = make_missing_feature_cue(
    pattern, drop_probability=0.25, seed=10
)
substituted = make_substituted_cue(
    pattern, substitution_probability=0.25, seed=10
)
```

Each call returns a `CueDegradation` object containing the cue, mode, probability, and exact edit indices.

## Interpretation limits

Missing-feature cues and feature-substitution cues are different experimental conditions and should not be pooled without an explicit rationale. A retrieval system may respond differently to reduced cue sparsity and altered feature identity. These utilities only generate controlled binary inputs; they do not implement hippocampal retrieval, establish pattern completion, or demonstrate biological equivalence.
