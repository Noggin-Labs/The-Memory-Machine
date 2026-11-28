# The Memory Machine

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24475098.svg)](https://doi.org/10.5281/zenodo.24475098)
[![Tests](https://github.com/NCCL-Research/The-Memory-Machine/actions/workflows/tests.yml/badge.svg)](https://github.com/NCCL-Research/The-Memory-Machine/actions/workflows/tests.yml)

A cognitive science and computational neuroscience research project investigating episodic memory, hippocampal pattern separation, pattern completion, and memory retrieval through computational modelling and controlled experiments.

## Research status

This repository is in an early software-development and protocol-design stage. The current manuscript and MM-01 protocol are preliminary. The software components currently implemented are infrastructure and computational baselines; they are not confirmatory evidence for biological pattern separation, pattern completion, or biological equivalence.

## Scope

- Pattern separation: distinguishing overlapping input episodes.
- Pattern completion: evaluating retrieval from incomplete or altered cues.
- Episodic retrieval under interference.
- Capacity, robustness, and representational information preservation.

The model is an experimental computational framework, not a claim that a simplified simulation reproduces the hippocampus.

## Current implementation

- **Data:** fixed-sparsity binary pattern-pair generation with stochastic overlap and recorded realized overlap.
- **Cue degradation:** separate missing-feature and feature-substitution conditions, with explicit random sources and edit metadata.
- **Evaluation:** binary Hamming distance, normalized Hamming distance, and Jaccard similarity.
- **Storage:** an in-memory store for fixed-dimensional boolean representations.
- **Retrieval:** a transparent nearest-neighbour baseline ranked by Hamming distance, returning all minimum-distance ties.

Encoding baselines and a fuller retrieval/reconstruction model remain under development. Proposed encoder definitions are documented separately and have not yet been treated as a locked experimental specification.

## Manuscript

The preliminary methods/framework manuscript is in [`manuscript/manuscript.md`](manuscript/manuscript.md). It distinguishes implemented software from proposed experiments and contains explicit literature-review placeholders; it is not a submission-ready paper.

## Development

Install the project and development dependencies with:

    python -m pip install -e ".[dev]"
    python -m pytest

A GitHub Actions workflow runs the test suite on pushes to `main` and pull requests. The current implementation test suite has **49 passing tests** on Python 3.12 (GitHub Actions run associated with commit `25754a9565652b5df881e39d0828351f1263b894`).

## Reproducibility and interpretation

Stochastic components require explicit seeds or random-number generators. Experiments should save configurations and machine-readable outputs. Results must distinguish implementation checks from evidence about memory encoding or retrieval.

Separation metrics must be reported alongside information-preservation and retrieval measures. A lower output similarity alone is not evidence of a better memory representation. Nearest-neighbour selection is not, by itself, pattern completion.

## Status

Preliminary research draft. Software infrastructure has initial test coverage; encoding mechanisms, retrieval/reconstruction mechanisms, experiment design, and confirmatory analyses remain to be specified and evaluated.
