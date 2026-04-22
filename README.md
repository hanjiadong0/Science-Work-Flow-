# Cambagent Proposal Scaffold

This repository is now intentionally minimal. It keeps only the evaluation scaffold that comes directly from `Cambagent_lab_proposal.pdf`, plus the two local agent folders you wanted to test: `external/cmbagent` and `external/OpenGauss`.

## What Stays

- `Cambagent_lab_proposal.pdf`
- one baseline experiment in `configs/experiments/baseline.json`
- proposal task files in `configs/tasks/`
- proposal trial configs in `configs/experiments/trials/`
- one proposal notebook: `notebooks/01_lab_proposal_experiment.ipynb`
- the minimal runner in `src/cambagent_eval/`
- proposal docs in `docs/`

## Main Files

- `docs/proposal_explainer.md`
- `docs/proposal_mapping.md`
- `docs/trial_evaluation_modes.md`
- `docs/open_agents_quickstart.md`
- `external/cmbagent`
- `external/OpenGauss`

## Run The Proposal Scaffold

Validate the baseline config:

```powershell
python -m cambagent_eval validate configs\experiments\baseline.json
```

Run the baseline dry run:

```powershell
python -m cambagent_eval dry-run configs\experiments\baseline.json
```

Open the single notebook:

```powershell
jupyter lab notebooks\01_lab_proposal_experiment.ipynb
```

## Open The Two Agents

The shortest instructions for both agents are in `docs/open_agents_quickstart.md`.

The shared Python environment for both agents is `.venv-agents`, and the current OpenGauss Lean experiment project is exposed inside this repo at `projects\LeanCourse25` while still pointing to your real clone `C:\Users\Anwender\LEANCOURSE\LeanCourse25` with remote `git@github.com:hanjiadong0/LeanCourse25.git`.
