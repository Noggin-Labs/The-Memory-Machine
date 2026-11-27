# MM-01 Nearest-Neighbour Retrieval Baseline

**Status:** simple computational baseline; not a biological retrieval model.

## Behaviour

The retrieval package provides two functions:

- `rank_memories(cue, store)` returns all stored IDs ranked by ascending Hamming distance.
- `nearest_memories(cue, store)` returns every item tied at the minimum Hamming distance.

Ties preserve insertion order. The functions return identifiers and distances; they do not alter the stored representations, fill missing features, or synthesize a reconstructed episode. An empty store returns no matches. A cue whose dimensionality differs from the store raises an error.

## Why include this baseline?

It provides a transparent reference against which more complex retrieval mechanisms can later be compared. It is not evidence of pattern completion: selecting the closest stored item is not the same operation as reconstructing an episode from an incomplete cue.

## Scope and limitations

Hamming distance treats every bit position equally. It does not account for feature salience, correlated features, temporal structure, or learned associations. Results depend on the representation supplied by the encoder. Retrieval performance must be measured against known target IDs in a separately specified evaluation protocol.
