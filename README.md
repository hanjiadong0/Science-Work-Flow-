# Cambagent Eval Scaffold

This repository is a starter implementation of the lab proposal in [Cambagent_lab_proposal.pdf](/c:/Users/Anwender/Science-Work-Flow-/Cambagent_lab_proposal.pdf). It turns the proposal into a runnable Python scaffold for evaluating LLM-based scientific agents across:

- tool-grounded precision tasks
- research-driven inference tasks
- workflow variants (`one_shot` and `deep_research`)
- ablations over model size, retrieval grounding, and stress conditions

The current version is intentionally lightweight and dependency-friendly. It ships with a deterministic stub agent so we can exercise the evaluation loop offline before wiring in a real CMBAgent or OpenAI-backed adapter.

## Repo Layout

- `src/cambagent_eval/`: core package
- `configs/`: experiment and task specifications
- `docs/`: architecture notes and proposal-to-repo mapping
- `tests/`: smoke tests for config loading, the pipeline, and the CLI
- `outputs/`: generated reports

## Quick Start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .[dev]
python -m cambagent_eval validate configs\experiments\baseline.json
python -m cambagent_eval dry-run configs\experiments\baseline.json
```

If you want to avoid installing extras right away, the scaffold itself only uses the Python standard library.

## What Is Implemented

- experiment specs with model, grounding, workflow, and stress-test matrices
- task specs for precision and inference benchmarks
- a stub scientific agent with deterministic behavior for offline dry runs
- metric computation for numerical accuracy, tool-use accuracy, calibration, stability, and physical validity
- a basic failure taxonomy aligned with the proposal
- JSON report generation and CLI summaries

## Suggested Next Steps

1. Replace the stub adapter in [agents.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/agents.py) with a real CMBAgent or API-backed adapter.
2. Add benchmark datasets and real astrophysical task instances under `configs/tasks/` or a future `data/` directory.
3. Extend the grounding layer to use a curated domain corpus for the retrieval-augmented ablation.
4. Add plotting and statistical analysis for paper-quality experiment summaries.

