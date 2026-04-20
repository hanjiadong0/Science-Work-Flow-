from __future__ import annotations

import json
from collections import Counter
from collections import defaultdict
from dataclasses import asdict
from datetime import UTC
from datetime import datetime
from pathlib import Path
from typing import Callable

from .agents import AgentAdapter
from .agents import StubScientificAgent
from .metrics import compute_metrics
from .models import ExperimentReport
from .models import ExperimentSpec
from .models import RunResult
from .models import StressCondition
from .models import TaskCase
from .taxonomy import classify_failures


def run_experiment(
    spec: ExperimentSpec,
    tasks: list[TaskCase],
    agent: AgentAdapter | None = None,
) -> ExperimentReport:
    agent = agent or StubScientificAgent()
    runs: list[RunResult] = []

    for task in tasks:
        workflows = [workflow for workflow in spec.workflows if workflow in task.supported_workflows]
        stress_tests = _stress_plan(spec, task)
        for workflow_name in workflows:
            for model_name in spec.models:
                for grounding_mode in spec.grounding_modes:
                    for stress_test in stress_tests:
                        steps, final_output = agent.run(
                            task=task,
                            model_name=model_name,
                            grounding_mode=grounding_mode,
                            workflow_name=workflow_name,
                            stress_test=stress_test,
                        )
                        metrics = compute_metrics(task, final_output, workflow_name, stress_test)
                        failures = classify_failures(task, workflow_name, metrics)
                        runs.append(
                            RunResult(
                                task_id=task.id,
                                task_name=task.name,
                                task_type=task.task_type,
                                model_name=model_name,
                                grounding_mode=grounding_mode,
                                workflow=workflow_name,
                                stress_test=stress_test.id,
                                metrics=metrics,
                                failures=failures,
                                final_output=final_output,
                                steps=steps,
                            )
                        )

    summary = summarize_runs(runs)
    return ExperimentReport(
        experiment_id=spec.id,
        experiment_name=spec.name,
        generated_at=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        source_config=spec.source_path,
        summary=summary,
        runs=runs,
    )


def write_report(report: ExperimentReport, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    return output_path


def summarize_runs(runs: list[RunResult]) -> dict:
    metric_names = list(runs[0].metrics.keys()) if runs else []
    average_metrics = {
        metric_name: round(sum(run.metrics[metric_name] for run in runs) / len(runs), 6)
        for metric_name in metric_names
    } if runs else {}

    failure_counts = Counter()
    for run in runs:
        failure_counts.update(run.failures)

    return {
        "total_runs": len(runs),
        "average_metrics": average_metrics,
        "by_model": _group_metrics(runs, lambda run: run.model_name),
        "by_grounding_mode": _group_metrics(runs, lambda run: run.grounding_mode),
        "by_workflow": _group_metrics(runs, lambda run: run.workflow),
        "by_stress_test": _group_metrics(runs, lambda run: run.stress_test),
        "failure_counts": dict(sorted(failure_counts.items())),
    }


def format_summary(report: ExperimentReport) -> str:
    lines = [
        f"Experiment: {report.experiment_name}",
        f"Runs: {report.summary['total_runs']}",
        "Average metrics:",
    ]
    for metric_name, value in report.summary["average_metrics"].items():
        lines.append(f"  - {metric_name}: {value:.3f}")
    lines.append("Failure counts:")
    for failure_name, count in report.summary["failure_counts"].items():
        lines.append(f"  - {failure_name}: {count}")
    return "\n".join(lines)


def _stress_plan(spec: ExperimentSpec, task: TaskCase) -> list[StressCondition]:
    baseline = StressCondition(id="baseline", description="No perturbation.", severity="none", effect_size=0.0)
    applicable = [baseline]
    for stress_test in spec.stress_tests:
        if not stress_test.applies_to or task.task_type in stress_test.applies_to:
            applicable.append(stress_test)
    return applicable


def _group_metrics(
    runs: list[RunResult],
    key_fn: Callable[[RunResult], str],
) -> dict[str, dict[str, float]]:
    grouped: dict[str, list[RunResult]] = defaultdict(list)
    for run in runs:
        grouped[key_fn(run)].append(run)

    output: dict[str, dict[str, float]] = {}
    for group_name, group_runs in grouped.items():
        metric_names = group_runs[0].metrics.keys()
        output[group_name] = {
            "runs": float(len(group_runs)),
        }
        for metric_name in metric_names:
            output[group_name][metric_name] = round(
                sum(run.metrics[metric_name] for run in group_runs) / len(group_runs),
                6,
            )
    return dict(sorted(output.items()))
