from __future__ import annotations

import json
from pathlib import Path

from .models import ExperimentSpec
from .models import TaskCase


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_experiment(path: str | Path) -> ExperimentSpec:
    experiment_path = Path(path).resolve()
    spec = ExperimentSpec.from_dict(_load_json(experiment_path))
    spec.source_path = str(experiment_path)
    spec.task_files = [
        str(_resolve_relative_path(experiment_path.parent, task_file))
        for task_file in spec.task_files
    ]
    spec.report_path = str(_resolve_relative_path(experiment_path.parent, spec.report_path))
    return spec


def load_tasks(spec: ExperimentSpec) -> list[TaskCase]:
    return [TaskCase.from_dict(_load_json(Path(task_file))) for task_file in spec.task_files]


def validate_experiment(spec: ExperimentSpec, tasks: list[TaskCase]) -> list[str]:
    problems: list[str] = []
    if not spec.models:
        problems.append("Experiment is missing models.")
    if not spec.grounding_modes:
        problems.append("Experiment is missing grounding modes.")
    if not spec.workflows:
        problems.append("Experiment is missing workflows.")
    if not tasks:
        problems.append("Experiment does not reference any task files.")

    for task in tasks:
        if task.default_workflow not in task.supported_workflows:
            problems.append(
                f"Task '{task.id}' default workflow '{task.default_workflow}' is not supported."
            )
        if not set(task.supported_workflows).intersection(spec.workflows):
            problems.append(
                f"Task '{task.id}' has no workflow overlap with experiment workflows."
            )
        if set(task.priors) != set(task.ground_truth):
            problems.append(
                f"Task '{task.id}' priors do not cover the same parameters as ground truth."
            )
    return problems


def _resolve_relative_path(base_dir: Path, candidate: str) -> Path:
    path = Path(candidate)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()

