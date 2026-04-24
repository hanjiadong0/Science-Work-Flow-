# Data Science Bridge

This repository can act like the research-execution side of your data science study repo.
Your study repo captures how you learn; this repo captures how you turn that learning into structured experiments.

## Relationship Between The Two Repos

Use your data science study repo for:

- notes on methods, models, metrics, and papers
- small practice notebooks and concept demos
- reusable EDA habits
- summaries of what worked and what failed

Use this repo for:

- experiment definitions in `configs/experiments/`
- benchmark tasks in `configs/tasks/`
- repeatable evaluation logic in `src/cambagent_eval/`
- experiment notebooks in `notebooks/`
- saved outputs and reports in `outputs/`

The practical relationship is:

1. Learn a method in the study repo.
2. Translate that method into an experiment or task here.
3. Run and compare workflows here.
4. Feed results, mistakes, and lessons back into the study repo.

## Transfer Map

Here is the simplest one-to-one mapping.

- problem framing from the study repo -> experiment description in `configs/experiments/*.json`
- dataset assumptions -> task prompt and expected outputs in `configs/tasks/*.json`
- EDA notebook habits -> analysis notebooks in `notebooks/`
- model comparison practice -> `models`, `grounding_modes`, and `workflows`
- evaluation metrics practice -> `src/cambagent_eval/metrics.py`
- error analysis practice -> `src/cambagent_eval/taxonomy.py`
- experiment tracking habits -> JSON reports in `outputs/`

## How To Reuse Your Data Science Experience

Bring these habits directly into this repo:

- define a clear hypothesis before editing configs
- treat each task file as a structured problem statement
- compare one variable at a time when running ablations
- keep notebook exploration separate from reusable pipeline logic
- read failures as data, not just as mistakes
- document why a workflow succeeded or failed

## Recommended Workflow

When you study something in the other repo, convert it here with this pattern:

1. Write the concept in the study repo.
2. Create or edit a task in `configs/tasks/`.
3. Add or clone an experiment in `configs/experiments/`.
4. Inspect the run in `notebooks/01_lab_proposal_experiment.ipynb`.
5. Save the result in `outputs/`.
6. Write a short lesson summary back in the study repo.

## Suggested Linked-Repo Layout

The `projects/` folder already holds local links to external repos. A good setup is:

- `projects/LeanCourse25`
- `projects/DataScienceRoot`
- `projects/DataScienceSS2026`
- `projects/NLPStudyRoot`
- `projects/DataScienceStudyLab`

That keeps this repo as the execution hub while still letting you keep your study repo separate.

## Current Linked Study Repo

This workspace is now linked to:

- `projects/DataScienceRoot` -> `C:\Users\Anwender\Downloads\data science`
- `projects/DataScienceSS2026` -> `C:\Users\Anwender\Downloads\data science\ss 2026`
- `projects/NLPStudyRoot` -> `C:\Users\Anwender\Downloads\data science\ss 2026\NLP`
- `projects/DataScienceStudyLab` -> `C:\Users\Anwender\Downloads\data science\ss 2026\NLP\Lab`

The visible study areas there include:

- biomedical named entity
- reinforcement learning
- value method
- paper-reading material

That means your transfer path is already practical:

- use the full data science root when you want patterns that cut across multiple subjects
- use the parent roots when you need broader semester or NLP context
- reuse notebook habits and experiment framing from the NLP lab
- turn successful study patterns into repeatable configs here
- use this repo to evaluate workflow quality, robustness, and failure modes
- push the lessons back into the course repo after each run

## What To Carry Over First

The highest-value things to transfer from the study repo are:

- experiment design discipline
- metric selection
- notebook storytelling
- ablation thinking
- failure analysis language
- reproducibility habits

If you use those six consistently, your study experience becomes part of the workflow here instead of staying isolated in notes.
