# Proposal Mapping

This repository scaffold maps the lab proposal into concrete code and files.

## Goal

The proposal asks for a structured evaluation framework for LLM-based scientific workflows, with astrophysical inference as the testbed.

Implemented here:

- a reusable experiment specification format in `configs/experiments/`
- task definitions for precision and inference benchmarks in `configs/tasks/`
- a runner that compares workflows, models, grounding modes, and stress tests

## Core Setup

The proposal separates:

- single-step tool-based computations
- multi-step reasoning and planning workflows

Implemented here:

- `one_shot` traces in [workflows.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/workflows.py)
- `deep_research` traces in [workflows.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/workflows.py)

## Ablations

The proposal calls for three main ablations:

1. Backbone model effects
2. Retrieval and domain grounding
3. Multi-step reasoning robustness under stress

Implemented here:

- `models` in [baseline.json](/c:/Users/Anwender/Science-Work-Flow-/configs/experiments/baseline.json)
- `grounding_modes` in [baseline.json](/c:/Users/Anwender/Science-Work-Flow-/configs/experiments/baseline.json)
- `stress_tests` in [baseline.json](/c:/Users/Anwender/Science-Work-Flow-/configs/experiments/baseline.json)

## Evaluation Strategy

The proposal emphasizes:

- numerical accuracy
- posterior consistency
- stability under perturbations
- error propagation
- qualitative failure cases

Implemented here:

- quantitative metrics in [metrics.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/metrics.py)
- qualitative taxonomy in [taxonomy.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/taxonomy.py)

## Immediate Gaps

This scaffold does not yet include:

- a live CMBAgent integration
- real retrieval against a scientific corpus
- actual CAMB or MCMC execution
- benchmark datasets or plotting pipelines

Those are the natural next implementation layers on top of the structure created here.

