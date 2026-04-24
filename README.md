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
- `docs/data_science_bridge.md`
- `docs/trial_evaluation_modes.md`
- `docs/open_agents_quickstart.md`
- `references/clear/README.md`
- `references/lean/README.md`
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

## Connect This Repo To Your Data Science Study Repo

To make your study experience reusable here:

- keep the study repo for notes, EDA habits, metric intuition, and method summaries
- use this repo for repeatable experiment configs, evaluation runs, and reports
- add your study repo as a local link under `projects\` so both repos sit in one workflow

The concrete mapping is documented in:

- `docs\data_science_bridge.md`
- `projects\README.md`

Current local study link:

- `projects\DataScienceRoot`
- `projects\DataScienceSS2026`
- `projects\NLPStudyRoot`
- `projects\DataScienceStudyLab`

## Build The Agent Structure Report

Do not use `latexmk` on this machine unless you separately install Perl.
Use the included PowerShell script instead:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_agent_structure_report.ps1
```

The script now prefers `latexmk` when Perl is available and falls back to a
two-pass `pdflatex` build otherwise. It also auto-detects a local Strawberry
Perl extraction under your user profile if the current shell has not picked up
`perl` on PATH yet.

This builds:

- `docs\cmbagent_opengauss_agent_structure_report.pdf`

If MiKTeX says this is a new installation or that updates have not been checked
yet, open MiKTeX Console once, finish its setup/update step, and then rerun the
script.

## Open The Two Agents

The shortest instructions for both agents are in `docs/open_agents_quickstart.md`.

The shared Python environment for both agents is `.venv-agents`, and the current OpenGauss Lean experiment project is exposed inside this repo at `projects\LeanCourse25` while still pointing to your real clone `C:\Users\Anwender\LEANCOURSE\LeanCourse25` with remote `git@github.com:hanjiadong0/LeanCourse25.git`.

## VS Code LaTeX Build

This workspace now includes:

- `.vscode\settings.json`
- `scripts\latexmk-local.cmd`

These force LaTeX Workshop to use the local MiKTeX `latexmk.exe` together with
the extracted Strawberry Perl path, so VS Code does not depend on a stale
global `PATH` when building or cleaning.
