# MM-01 Protocol v0.2 — Recommended specification for review

**Status:** Proposed specification; requires researcher approval before it is locked or described as preregistered.  
**Study type:** Exploratory computational Monte Carlo comparison.  
**No experimental runs or outcome data are reported in this document.**

## 1. Scope and boundary

MM-01 will test how four deterministic binary transformations change the representational similarity of sparse binary input pairs whose feature overlap is controlled probabilistically.

MM-01 will **not** test biological pattern separation, hippocampal function, memory retrieval from degraded cues, or pattern completion. Cue degradation and nearest-neighbour utilities remain available in the software but belong to a later retrieval experiment (provisionally MM-02). Keeping these questions separate avoids claiming retrieval from an experiment that only compares pairwise representations.

## 2. Primary research question

How does each candidate transformation change the relationship between the realized input overlap of a pair and the normalized Hamming distance between its output representations?

### Primary outcome

For each input pair (A,B) and encoder E:

\[
D_E(A,B)=\frac{1}{128}\sum_{j=1}^{128}\mathbb{1}[E(A)_j\ne E(B)_j].
\]

The primary analysis is the curve of mean output normalized Hamming distance against **realized input overlap**, reported separately by encoder. Target retention probability is a design condition, not a substitute for realized overlap.

### Secondary outcomes

1. Output Jaccard similarity, only as a secondary active-set measure, accompanied by output active counts.
2. Output active count and sparsity distributions.
3. Empirical output-collision rate among distinct input patterns in the generated pattern bank.
4. Sensitivity of all outcomes to independent input/encoder seed blocks.

A lower output similarity or higher output distance is not automatically beneficial. It may reflect loss of information or collisions elsewhere in the input space.

## 3. Input generation

- Input dimension: N = 128.
- Active features: K = 16.
- Target retention probabilities: p = {0, 0.2, 0.4, 0.6, 0.8}.
- Each pair is generated independently using the existing fixed-sparsity generator.
- Record the raw shared-active count and realized overlap for every pair.
- The same generated input pairs are passed to all four encoders within a seed block (paired comparison).
- Do not generate a new encoder matrix or hash mapping for every input pair.

The existing generator's stochastic p parameter is not an exact overlap quota. Analysis and plots must use the realized overlap.

## 4. Candidate encoder definitions

All outputs are boolean vectors of length 128. All stochastic encoder parameters are sampled once per seed block and held fixed for that block's entire pattern bank.

### E0 — Identity

\[
E_0(x)=x.
\]

No fitted parameters or randomness.

### E1 — Dense Gaussian projection with zero threshold

Let x be the input vector and let μ = K/N = 0.125. Center the input as x' = x − μ1. Sample a fixed matrix W with independent entries:

\[
W_{ij}\sim\mathcal{N}(0,1/128),\quad W\in\mathbb{R}^{128\times128}.
\]

Calculate z = W x' and output E1(x)_j = 1[z_j > 0]. Use a strict greater-than-zero threshold; exact zeros map to 0. Do not re-sample W between patterns.

### E2 — Competitive k-winner-take-all

Use the same centered input and the same Gaussian score matrix W as E1 within a seed block. Calculate z = W x'. Set exactly k = 16 output positions to 1, selecting the 16 largest scores. Resolve exact ties deterministically by lower output index first. This condition differs from E1 only in its output activation rule.

Sharing W between E1 and E2 makes the comparison of thresholding versus fixed-k selection more controlled. A sensitivity analysis with independent W matrices may be considered later, but is not part of the initial specification.

### E3 — Random feature hash

Sample one fixed mapping h from the 128 input feature indices to 128 output buckets, independently and uniformly with replacement. For each input x, output bucket b is active if at least one active input feature i satisfies h(i)=b:

\[
E_3(x)_b=\mathbb{1}[\exists i:x_i=1\land h(i)=b].
\]

Use the same mapping for every pattern in a seed block. Hash collisions are part of the control's behaviour and must be reported, not corrected after observing results.

These transformations are computational baselines. They are not asserted to be biologically faithful models of dentate gyrus, CA3, or any other neural structure.

## 5. Sampling and seed structure

Use a two-level seed-block design:

- 30 independent seed blocks.
- Within each block, generate 200 independent input pairs at each of the five target p values (1,000 pairs per block).
- This yields 30,000 input pairs in total, each evaluated by all four encoders.
- Within each block, use one independent input-generation seed and one independent encoder-parameter seed. The identity condition is deterministic but is evaluated on the same input pairs.
- Record the exact seeds and generator/library versions.

The 30-block, 200-pair design is a **proposed exploratory Monte Carlo starting point**, not a power-derived sample size and not a biological sample size. After a pilot, estimate Monte Carlo uncertainty for the primary curves. Increase the number of blocks or pairs if the prespecified precision target is not met. Do not reduce sample size because an interim result looks favourable.

## 6. Collision and information-loss diagnostic

Do not label output distance itself as information preservation.

Within each seed block and encoder, construct the set of unique input patterns represented in the generated pattern bank. Compute:

- number of unique input patterns;
- number of unique output patterns;
- number and proportion of unique input patterns whose output is shared by at least one other distinct input pattern;
- pairwise collision probability among distinct input patterns.

A collision means two distinct input patterns map to exactly the same output vector. This is an empirical, finite-pattern-bank diagnostic of non-injectivity, not a complete measure of mutual information and not proof that all non-colliding patterns are recoverable in realistic retrieval settings.

If a later study requires a stronger information-preservation claim, define a separate held-out decoding experiment with a fixed decoder, training protocol, and baseline before collecting confirmatory data. Do not retrofit a decoder after seeing MM-01 outcomes.

## 7. Analysis plan

1. Validate inputs and encoder outputs before calculating metrics.
2. For each seed block, encoder, and target p, report the distribution of realized input overlap, normalized Hamming distance, Jaccard similarity, output active count, and collision diagnostics.
3. Plot output normalized Hamming distance against realized input overlap, with separate curves by encoder.
4. Report block-level means and dispersion. Treat the seed block as the replication unit for uncertainty summaries; pairs within a block are nested Monte Carlo samples, not 200 independent replications of the encoder.
5. Report uncertainty intervals across the 30 independent blocks. State the interval method and provide the block-level values so results can be independently checked.
6. Include target p condition summaries as descriptive secondary analyses; do not substitute target p for realized overlap.
7. Report all four encoders, all five input conditions, and all prespecified outcomes. Do not select only favourable metrics.
8. Do not use the terms “biological pattern separation,” “hippocampal computation,” “memory improvement,” or “pattern completion” as conclusions from this experiment.

### Precision rule

The initial 30 × 200 design is exploratory. Before confirmatory use, select a precision target for the primary curve (for example, a maximum desired half-width for the across-block confidence interval) and justify it from pilot variability. If that target is not met, increase Monte Carlo sampling according to a written rule rather than inspecting which encoder is ahead.

## 8. Software validation gates

Before the first full run, tests must verify:

- every generated input has shape (128,) and exactly 16 active bits;
- realized overlap equals the reported shared count divided by 16;
- p = 0 produces disjoint pairs and p = 1 produces identical pairs;
- all encoders return boolean vectors of shape (128,);
- identity returns an exact copy of the input;
- projection and k-WTA reuse fixed W within a block;
- k-WTA always returns exactly 16 active bits and applies the documented tie rule;
- random hash uses one fixed feature-to-bucket map within a block;
- identical inputs always produce identical outputs within a fixed encoder instance;
- same seeds reproduce the same block, while distinct seeds can change stochastic parameters;
- collision counts are computed only across distinct input patterns;
- no global random state is used.

## 9. Reproducibility and data management

Each run must record the Git commit, complete configuration and hash, input and encoder seeds, Python and dependency versions, encoder parameter summaries or hashes, pair counts, exclusions, raw outputs, analysis code version, and run timestamp.

Store raw data in a machine-readable format with a schema. Store derived summaries separately. Do not overwrite raw outputs. Any exclusion must be recorded with a reason before examining encoder outcomes.

## 10. Decision status and approval checklist

The following is recommended but not yet approved:

- [ ] Approve the strict MM-01 scope: representation comparison only; retrieval deferred to MM-02.
- [ ] Approve the four encoder definitions and shared projection/k-WTA matrix.
- [ ] Approve 30 seed blocks × 200 pairs × 5 target p conditions as an exploratory starting design.
- [ ] Approve the collision diagnostic as a limited information-loss proxy, not a complete information measure.
- [ ] Approve the block-level uncertainty approach and specify the interval method before the full run.
- [ ] Approve the software validation gates.

**Until these decisions are explicitly approved, this document remains a recommended protocol draft, not a locked or preregistered protocol.**
