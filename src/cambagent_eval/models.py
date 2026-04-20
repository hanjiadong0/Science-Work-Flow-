from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(slots=True)
class StressCondition:
    id: str
    description: str = ""
    severity: str = "medium"
    applies_to: list[str] = field(default_factory=list)
    effect_size: float = 0.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StressCondition":
        return cls(
            id=str(data.get("id", data.get("name", "unnamed_stress"))),
            description=str(data.get("description", "")),
            severity=str(data.get("severity", "medium")),
            applies_to=[str(item) for item in data.get("applies_to", [])],
            effect_size=float(data.get("effect_size", 0.0)),
        )


@dataclass(slots=True)
class TaskCase:
    id: str
    name: str
    task_type: str
    default_workflow: str
    supported_workflows: list[str]
    prompt: str
    ground_truth: dict[str, float]
    expected_tools: list[str] = field(default_factory=list)
    domain_context: list[str] = field(default_factory=list)
    priors: dict[str, list[float]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskCase":
        default_workflow = str(data["default_workflow"])
        supported_workflows = [str(item) for item in data.get("supported_workflows", [default_workflow])]
        ground_truth = {str(key): float(value) for key, value in data["ground_truth"].items()}
        priors = {
            str(key): [float(bound) for bound in value]
            for key, value in data.get("priors", {}).items()
        }
        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            task_type=str(data["task_type"]),
            default_workflow=default_workflow,
            supported_workflows=supported_workflows,
            prompt=str(data["prompt"]),
            ground_truth=ground_truth,
            expected_tools=[str(item) for item in data.get("expected_tools", [])],
            domain_context=[str(item) for item in data.get("domain_context", [])],
            priors=priors,
            metadata=dict(data.get("metadata", {})),
        )


@dataclass(slots=True)
class ExperimentSpec:
    id: str
    name: str
    description: str
    task_files: list[str]
    models: list[str]
    grounding_modes: list[str]
    workflows: list[str]
    stress_tests: list[StressCondition] = field(default_factory=list)
    report_path: str = "outputs/report.json"
    source_path: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExperimentSpec":
        return cls(
            id=str(data["id"]),
            name=str(data.get("name", data["id"])),
            description=str(data.get("description", "")),
            task_files=[str(item) for item in data.get("task_files", [])],
            models=[str(item) for item in data.get("models", [])],
            grounding_modes=[str(item) for item in data.get("grounding_modes", [])],
            workflows=[str(item) for item in data.get("workflows", [])],
            stress_tests=[StressCondition.from_dict(item) for item in data.get("stress_tests", [])],
            report_path=str(data.get("report_path", "outputs/report.json")),
        )


@dataclass(slots=True)
class TraceStep:
    index: int
    kind: str
    summary: str
    tool_name: str | None = None
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RunResult:
    task_id: str
    task_name: str
    task_type: str
    model_name: str
    grounding_mode: str
    workflow: str
    stress_test: str
    metrics: dict[str, float]
    failures: list[str]
    final_output: dict[str, Any]
    steps: list[TraceStep]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ExperimentReport:
    experiment_id: str
    experiment_name: str
    generated_at: str
    source_config: str
    summary: dict[str, Any]
    runs: list[RunResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "experiment_name": self.experiment_name,
            "generated_at": self.generated_at,
            "source_config": self.source_config,
            "summary": self.summary,
            "runs": [run.to_dict() for run in self.runs],
        }

