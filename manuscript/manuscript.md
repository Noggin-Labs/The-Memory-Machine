# The Memory Machine: A Hippocampal-Inspired Computational Framework for Studying Pattern Separation and Retrieval from Degraded Cues

**Manuscript status:** Preliminary methods/framework draft  
**Version:** 0.1  
**Study status:** MM-01 protocol is a design draft; no encoder-comparison experiment has been run.  
**Repository:** https://github.com/NCCL-Research/The-Memory-Machine

> **Drafting note:** This document separates implemented software from proposed experiments. Bracketed literature notes identify places where primary sources must be added and checked before submission. No experimental results or biological validation are claimed.

## Abstract

Episodic-memory research motivates computational investigations of how overlapping representations may be distinguished and how stored information may be accessed from incomplete or altered cues. The Memory Machine is an early-stage, modular computational framework intended to support controlled comparisons of binary representations and retrieval procedures. Its current implementation includes a seeded generator for fixed-sparsity binary pattern pairs with stochastic overlap, utilities for generating missing-feature and feature-substitution cues, binary representation metrics, an in-memory representation store, and a transparent Hamming-distance nearest-neighbour baseline. The software is accompanied by unit tests and documentation specifying input conventions, stochastic controls, and interpretation limits. At the present stage, these components provide reproducible experimental infrastructure rather than a validated model of hippocampal function. The planned MM-01 study will compare candidate transformations under controlled input overlap, with information preservation and retrieval performance evaluated alongside representational similarity. Encoder definitions, sampling decisions, and confirmatory analysis procedures remain under specification. This paper documents the framework's current design and implementation boundary and identifies the experiments required before substantive claims about computational memory mechanisms can be evaluated.

**Keywords:** episodic memory; computational neuroscience; hippocampus; pattern separation; pattern completion; binary representations; retrieval; reproducibility

## 1. Introduction

Episodic memory involves the encoding and later retrieval of information about events and their contexts. Computational accounts of hippocampal function have emphasized the problem of distinguishing overlapping experiences and retrieving stored representations when available cues are incomplete or altered. [Add and verify primary sources on hippocampal pattern separation and completion.]

The terms *pattern separation* and *pattern completion* are used here as motivating computational problems, not as properties already demonstrated by this software. In this framework, representational separation concerns changes in similarity between input patterns and their transformed representations. Retrieval from degraded cues concerns whether a procedure can identify the correct stored item or reconstruct target information when only a partial or altered cue is available. These outcomes must be measured independently.

A central methodological risk is to treat reduced similarity between output representations as sufficient evidence of improved separation. A transformation can reduce similarity by discarding information. Consequently, representational similarity must be considered alongside information preservation and retrieval performance. A second risk is to equate selection of the nearest stored item with pattern completion. Nearest-neighbour selection returns an existing identifier; it does not reconstruct absent features or generate a completed representation.

The Memory Machine was developed as a modular software framework in which input generation, encoding, storage, retrieval, and evaluation can be varied independently. This manuscript reports the implemented infrastructure and defines the scope of the first planned computational comparison, MM-01.

### 1.1 Research aims

The framework is intended to support investigation of the following questions:

1. How do candidate transformations alter the similarity structure of sparse binary patterns with controlled input overlap?
2. How much information about the original input is preserved by each transformation?
3. How do candidate retrieval procedures perform when cues contain missing or substituted features?
4. How sensitive are these outcomes to random seeds, parameter choices, and the composition of the memory set?

These are research questions for subsequent experiments. The current implementation does not answer them.

## 2. Framework overview

The software is organized into separable components:

- **Data generation:** construction of sparse binary pattern pairs with controlled stochastic overlap.
- **Cue degradation:** generation of missing-feature and feature-substitution cues.
- **Encoding:** reserved package for candidate transformations; the planned baselines are not yet implemented.
- **Storage:** an in-memory collection of fixed-dimensional boolean representations.
- **Retrieval:** a transparent nearest-neighbour reference procedure.
- **Evaluation:** binary-vector similarity and distance measures.
- **Experiments:** reserved package for configuration, random-state management, and result logging.

The architecture is designed to make computational components replaceable. This modularity is an engineering design choice; it does not imply correspondence between software modules and anatomical structures.

## 3. Implemented methods

### 3.1 Input pattern generation

The input generator creates a pair of binary vectors with a specified number of active features. Let each vector have dimension (N) and exactly (K) active positions. A reference pattern (A) is sampled uniformly from the set of all (K)-element subsets of the (N) feature positions.

For each active feature in (A), the generator independently retains that feature in comparison pattern (B) with probability (p). The remaining active positions in (B) are sampled uniformly without replacement from positions inactive in (A). Thus, both patterns have exactly (K) active features. The realized overlap is recorded as

\[
O(A,B)=\frac{|A\cap B|}{K}.
\]

The parameter (p) is a per-feature retention probability, not a guarantee that the realized overlap equals (p). The implementation records both the requested probability and the realized shared-feature count and overlap.

The MM-01 draft proposes (N=128), (K=16), and (p\in\{0,0.2,0.4,0.6,0.8\}). These values describe the proposed protocol, not completed experimental conditions. The generator also permits custom dimensions and sparsity subject to its validation constraints.

Exactly one random source must be supplied: an integer seed or a caller-provided NumPy generator. A supplied generator is advanced in place; no global NumPy random state is used.

### 3.2 Cue degradation

Two distinct cue-corruption procedures are implemented.

**Missing-feature cues.** Each active feature in the original pattern is independently removed with probability (q). No inactive feature is inserted. The resulting cue may therefore have lower sparsity than the original pattern.

**Feature-substitution cues.** Each active feature is independently selected with probability (q). Every selected active feature is replaced with a uniformly sampled feature that was inactive in the original pattern. Replacement positions are sampled without replacement. This procedure preserves the number of active features while changing feature identity.

For both procedures, (q) is a Bernoulli selection probability; it does not prescribe an exact realized corruption count. The returned metadata records removed and inserted feature indices. Missing-feature and substitution conditions are kept separate because they produce different cue distributions.

These utilities generate controlled inputs only. They do not implement a biological degradation process or a retrieval mechanism.

### 3.3 Storage

The `MemoryStore` component stores representations under caller-supplied, non-empty string identifiers. Representations must be non-empty, one-dimensional boolean arrays. The first inserted representation establishes the dimensionality; later entries must match it. Duplicate identifiers are rejected.

Arrays are copied on insertion and when returned by retrieval or removal methods, preventing external mutation from silently changing stored values. Identifiers retain insertion order. The store is an in-memory data structure, not a model of biological memory storage.

### 3.4 Nearest-neighbour retrieval baseline

For a boolean cue (c) and stored representation (m_i), the baseline calculates Hamming distance:

\[
d_H(c,m_i)=\sum_{j=1}^{N}\mathbb{1}[c_j\ne m_{ij}].
\]

All stored items are ranked in ascending order of this distance. Ties preserve insertion order. A separate function returns every item tied at the minimum distance rather than imposing an arbitrary single winner.

The procedure returns stored identifiers and distances. It does not modify stored representations, fill missing features, or synthesize a reconstructed pattern. It is therefore a nearest-neighbour selection baseline and is not, by itself, an implementation of pattern completion.

### 3.5 Evaluation metrics

The current evaluation module implements three metrics for equal-length, one-dimensional boolean vectors:

- **Hamming distance:** the number of positions with different values.
- **Normalized Hamming distance:** Hamming distance divided by vector length.
- **Jaccard similarity:** the intersection size of the active-feature sets divided by their union size.

The implementation rejects implicit conversion from numeric arrays to boolean arrays. Normalized Hamming distance is undefined for empty vectors and raises an error. Jaccard similarity is defined by convention as 1 when both active sets are empty.

These metrics quantify properties of binary representations. They do not independently measure information preservation, successful retrieval, biological pattern separation, or memory performance. In particular, similarity measures must not be interpreted without considering output sparsity and the information retained by the transformation.

## 4. Software verification and reproducibility

The repository includes unit tests for input generation, cue degradation, metrics, storage, retrieval, and package structure. The latest recorded GitHub Actions test run associated with code commit `25754a9565652b5df881e39d0828351f1263b894` reported 49 tests passing under Python 3.12.

This result is a software-verification statement: the tested functions passed the assertions in the test suite for that code revision and environment. It is not evidence that the framework is scientifically valid, that all possible inputs have been tested, or that any memory hypothesis is supported.

Stochastic functions require explicit seeds or random-number generators. For future experiments, the repository protocol calls for recording the code commit, configuration and its hash, random seeds, software versions, transformation parameters, sample counts, exclusions, raw machine-readable outputs, and analysis-script version.

## 5. MM-01: planned representation-baseline study

MM-01 is a proposed controlled computational study of how candidate transformations alter similarity between sparse binary input patterns with controlled overlap. Its protocol remains a design draft and is not preregistered.

The current draft names four candidate conditions:

1. identity transformation;
2. random projection followed by binary thresholding;
3. competitive k-winner-take-all (k-WTA);
4. random-hash control.

A separate design document proposes possible definitions and defaults for these transformations. Those choices have not been approved as a locked specification, and no encoder has yet been implemented. Before the study is run, the output representation, dimensions, parameterization, random-state handling, and tie-breaking rules must be fixed.

The planned outcomes include realized input overlap, output Hamming distance where applicable, output Jaccard similarity where active-set semantics are meaningful, an independently defined information-preservation measure, and variability across independent random seeds. The experimental unit, sample sizes, number of seeds, and uncertainty-estimation procedure remain undecided.

No encoder comparison or MM-01 experimental result is reported in this manuscript.

## 6. Limitations

The current framework has several important limitations.

First, it uses sparse binary vectors and does not represent the full complexity of episodic experiences, including temporal, contextual, multimodal, and relational structure.

Second, the current implementation does not include an encoder. The proposed transformation families therefore cannot yet be compared empirically.

Third, the nearest-neighbour baseline uses uniform Hamming distance. It does not model feature salience, correlated features, learned associations, or latent-state inference.

Fourth, the current metrics do not establish information preservation. A suitable decoding or reconstruction evaluation must be defined for each candidate representation before differences in similarity can be interpreted.

Fifth, passing unit tests verifies specified software behaviour under tested cases; it does not establish construct validity, biological plausibility, or correspondence with hippocampal computation.

Finally, no experimental results, biological data, human-subject data, or external validation are presented here.

## 7. Planned work

The next development stages are:

1. finalize and version the MM-01 encoder specification;
2. implement identity and candidate transformation baselines with explicit configuration;
3. define information-preservation and retrieval outcomes before comparing encoders;
4. determine experimental units, sample sizes, seed structure, and uncertainty procedures;
5. implement experiment orchestration and provenance-aware result logging;
6. run exploratory checks, revise the protocol, and only then define any confirmatory analysis;
7. report all outcomes, including null or unfavourable results, with the limitations of the computational abstraction.

A later retrieval study will need to distinguish selecting a stored episode from reconstructing a representation. Any claim about pattern completion will require an explicit reconstruction target and evaluation procedure.

## 8. Conclusion

The Memory Machine currently provides a tested software foundation for controlled binary-pattern generation, cue degradation, representation metrics, storage, and a nearest-neighbour retrieval reference. It is an early computational framework, not a validated hippocampal model. MM-01 remains a proposed experiment whose encoder definitions and analysis decisions must be finalized before results can be interpreted. The framework's immediate contribution is to make these computational comparisons explicit, modular, and reproducible.

## References

**Literature review required before submission.** Add verified primary sources for:

- hippocampal pattern separation and pattern completion;
- computational theories of dentate gyrus and CA3 contributions;
- sparse distributed representations and episodic-memory models;
- methodological considerations for representational similarity and information preservation.

Do not retain a citation unless the cited source has been checked directly and supports the associated claim.
