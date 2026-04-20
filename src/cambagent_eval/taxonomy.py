from __future__ import annotations

from .models import TaskCase


def classify_failures(task: TaskCase, workflow_name: str, metrics: dict[str, float]) -> list[str]:
    failures: list[str] = []

    if metrics["hallucinated_tool_calls"] > 0:
        failures.append("hallucinated_tool_call")
    if metrics["physical_validity"] < 1.0:
        failures.append("physically_inconsistent_output")
    if metrics["numerical_accuracy"] < 0.9 and metrics["hallucinated_tool_calls"] == 0:
        failures.append("silent_numerical_error")
    if metrics["confidence_calibration_gap"] > 0.2:
        failures.append("reasoning_output_mismatch")
    if workflow_name == "deep_research" and (
        metrics["error_propagation_risk"] > 0.08 or len(failures) >= 2
    ):
        failures.append("error_propagation")

    if not failures:
        failures.append("no_detected_failure")
    return failures

