# The Memory Machine

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24475098.svg)](https://doi.org/10.5281/zenodo.24475098)


A cognitive science and computational neuroscience research project investigating episodic memory, hippocampal pattern separation, pattern completion, and memory retrieval through computational modelling and controlled experiments.

## Research status

This repository is at the initial software-architecture stage. The current manuscript is a preliminary research draft. The initial input-generation checks are not confirmatory evidence for pattern separation, pattern completion, or biological equivalence.

## Scope

- Pattern separation: distinguishing overlapping input episodes.
- Pattern completion: recovering an episode from an incomplete cue.
- Episodic retrieval under interference.
- Capacity, robustness, and representational information preservation.

The model is an experimental computational framework, not a claim that a simplified simulation reproduces the hippocampus.

## Development

The package uses a src layout. Install the project and development dependencies with:

    python -m pip install -e ".[dev]"
    pytest

Core scientific components are intentionally separated into data generation, encoding, storage, retrieval, evaluation, and experiment orchestration. Experimental mechanisms will be added only when their assumptions and evaluation criteria are specified.

## Reproducibility

Experiments should use explicit random seeds, saved configuration, and machine-readable outputs. Results must distinguish input-generator validation from evidence about memory encoding or retrieval.

## Status

Preliminary research draft; implementation and confirmatory experiments are in progress.
