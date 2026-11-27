# MM-01 Encoding Baselines: Decision Draft

**Status:** proposed design choices only. Not preregistered, not confirmatory, and not evidence that any transformation is biologically plausible.

The current protocol names four candidate transformations but does not yet define them sufficiently for reproducible implementation. This document makes the unresolved choices explicit and proposes a conservative software-comparison setup. The proposals should be reviewed before they are treated as the MM-01 specification.

## Shared comparison contract

- Input: boolean vector with 128 features and exactly 16 active features.
- Output: boolean vector with 128 features for all four baselines, allowing Hamming distance to be calculated on a common dimensionality.
- Each stochastic encoder is instantiated once per encoder seed and then held fixed across all patterns in that replicate. Do not redraw its weights or hash assignments for each input.
- All random state must be explicit and recorded.
- Record output active count and output sparsity for every encoded pattern.
- Report output similarity together with an information-preservation measure. A lower output similarity alone is not evidence of useful separation.
- Identity is a reference condition, not a trainable model.

## Candidate definitions and proposed defaults

| Baseline | Proposed definition | Proposed defaults | Important limitation |
|---|---|---|---|
| Identity | Return the input unchanged. | 128 input bits, 128 output bits. | Establishes the untransformed reference. |
| Random projection | Multiply the centered input vector by a fixed dense Gaussian matrix, then threshold each score at zero. | (W_{ij} \sim \mathcal{N}(0,1/128)); center each input bit by 16/128; 128 output units. | Output activity will generally not remain 16/128; thresholding changes representation density. |
| Competitive k-WTA | Apply fixed random linear scores and activate the 16 highest-scoring output units. | Same input centering and Gaussian score matrix convention as random projection; k=16; deterministic index-order tie break. | Enforces output sparsity but does not itself establish biological competition. |
| Random-hash control | Assign each input feature to one output bucket using a fixed seeded random mapping; output bucket is active if any active input feature maps there. | 128 input features, 128 buckets, one fixed assignment per encoder seed. | Hash collisions can reduce output active count; collision rate must be reported. |

These are not assumed to be equally informative or biologically equivalent. They are computational baselines with different representational properties.

## Required implementation decisions before locking

1. Confirm the proposed output dimension of 128.
2. Confirm the centering convention for projection and k-WTA.
3. Confirm that projection and k-WTA share the same random score matrix within an encoder replicate, or specify why they should not.
4. Confirm k=16 for k-WTA.
5. Confirm random-hash bucket count and whether a single feature-to-bucket assignment is shared across all input patterns in a replicate.
6. Define the information-preservation metric before interpreting separation scores.
7. Specify encoder seeds, number of pattern pairs per condition, and uncertainty procedure in the experiment protocol.

## Analysis safeguards

- Compare output sparsity across methods; do not interpret raw Hamming or Jaccard values without reporting density.
- For binary outputs with different densities, include both Hamming distance and active-set Jaccard similarity, with their definitions stated.
- Treat random projection thresholding and hash collisions as possible sources of information loss.
- Do not select a method because it maximizes separation alone. Retrieval accuracy and information preservation must be evaluated alongside it.
- Keep exploratory parameter selection separate from any later confirmatory evaluation.

## Decision status

No encoder has been implemented from these proposals. The existing data, cue, storage, and metric modules are infrastructure only. The MM-01 protocol should be updated only after these choices and the remaining sample-size and uncertainty decisions are explicitly settled.
