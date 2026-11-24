# MM-01: Input-overlap and representation baseline study

**Status:** Design draft — not preregistered; no experiment has been run.  
**Project:** The Memory Machine  
**Version:** 0.1-draft

## 1. Purpose

MM-01 is a controlled computational baseline study. It asks how candidate transformations change the similarity structure of sparse binary input patterns with controlled feature overlap.

It is a software experiment about representations. It is **not** evidence that the implementation reproduces hippocampal circuitry, biological pattern separation, episodic memory, or human learning.

## 2. Research question

Under controlled overlap between sparse binary input patterns, how do the candidate transformations differ in:

- output similarity as input overlap changes;
- preservation of information about the original input;
- stability across random seeds?

The first milestone should establish that the input generator and evaluation pipeline behave as specified before interpreting any encoder comparison.

## 3. Input specification

- Input dimensionality: 128 binary features.
- Sparsity: exactly 16 active features per pattern.
- Target input-overlap conditions: `p = [0.0, 0.2, 0.4, 0.6, 0.8]`.
- Each trial begins with a uniformly sampled 16-of-128 reference pattern A.
- For a target p, each active feature in A is independently retained in B with probability p. The remaining active positions in B are sampled uniformly without replacement from features inactive in A, so B also contains exactly 16 active features.
- The realized overlap is recorded for every pair; p is a retention probability, not a guarantee that the realized overlap equals p exactly.
- A and B are generated with an explicit seeded random-number generator. Seeds and generator version must be recorded.

This construction makes p=0 produce disjoint active sets and p=1 produce identical patterns. Intermediate conditions have stochastic realized overlap.

## 4. Candidate transformations

The planned comparison names four conditions. Their mathematical definitions must be fixed before confirmatory runs:

1. **Identity baseline:** return the 128-dimensional input unchanged.
2. **Random projection:** apply a fixed seeded projection matrix. The output dimensionality, matrix distribution, scaling, and any output thresholding must be specified before running.
3. **Competitive k-WTA:** retain the k largest activation values. The activation function, weights, k, tie-breaking rule, and whether weights are shared with the random-projection condition must be specified before running.
4. **Random-hash control:** map inputs using a seeded random hash. The hash family, output dimensionality, collision behaviour, and whether the mapping is pair-independent must be specified before running.

Do not describe these conditions as biologically faithful implementations. They are computational transformations selected for comparison.

## 5. Outcomes

Report at minimum:

- **Input overlap:** shared active features divided by 16, alongside the raw shared-feature count.
- **Output Hamming distance:** number of differing output bits, only for binary outputs with equal dimensionality.
- **Output Jaccard similarity:** intersection-over-union of active output features, only when outputs are represented as sets of active features.
- **Information preservation:** a separately defined measure of whether the original input can be recovered or decoded. Do not infer this from output sparsity or output distance alone.
- **Seed variability:** distribution across independent seeds, not only a single run.

Metrics that are not mathematically applicable to a transformation's output representation must be marked not applicable rather than silently coerced.

## 6. Controls and implementation checks

Before comparing transformations:

- verify every input has shape 128 and exactly 16 active features;
- verify p=0 pairs have zero shared active features and p=1 pairs are identical;
- verify observed overlap is recorded and bounded between 0 and 1;
- verify fixed seeds reproduce identical generated inputs and outputs;
- verify different seeds can produce different stochastic inputs;
- test metric edge cases, including empty active sets if any encoder can produce them;
- keep generator tests separate from encoder evaluation.

## 7. Experimental units and sampling

The independent experimental unit, number of input pairs per condition, number of seeds, and uncertainty-estimation method are **not yet specified**. These must be selected and justified before confirmatory analysis. Do not treat multiple pairs generated from one reference pattern as independent without accounting for their shared structure.

## 8. Analysis plan

Plot and tabulate each outcome by target p and transformation. Include realized input overlap in the analysis so that conclusions are not based only on nominal p. Report per-seed results and aggregate uncertainty using a method appropriate to the chosen sampling structure.

Do not select a preferred transformation based on one metric alone. In particular, lower output similarity is not automatically better if information preservation is poor.

## 9. Reproducibility record

Every run must record:

- code commit;
- configuration file and configuration hash;
- random seed(s) and random-number-generator implementation;
- Python and dependency versions;
- transformation parameters;
- number of generated pairs and exclusions;
- raw machine-readable outputs;
- analysis script version.

No generated results belong in version control until they have been checked and accompanied by this provenance.

## 10. Decisions required before implementation is treated as final

- Define output representation and dimensionality for each transformation.
- Define random-projection matrix distribution and any binarization.
- Define the k-WTA activation and weight-generation process.
- Define the random-hash family and collision handling.
- Choose sample sizes, seed count, and uncertainty procedure.
- Define a valid information-preservation measure for each output type.
- Decide whether the study is exploratory or confirmatory and document that status.

**Current conclusion:** MM-01 is a proposed experiment specification. No result, model advantage, pattern-separation effect, or biological interpretation is claimed.
