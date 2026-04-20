from __future__ import annotations

from .models import StressCondition
from .models import TaskCase


def compute_metrics(
    task: TaskCase,
    final_output: dict,
    workflow_name: str,
    stress_test: StressCondition,
) -> dict[str, float]:
    predicted = final_output.get("parameters", {})
    expected_tools = set(task.expected_tools)
    used_tools = set(final_output.get("used_tools", []))
    confidence = float(final_output.get("confidence", 0.5))

    relative_errors: list[float] = []
    for key, truth in task.ground_truth.items():
        predicted_value = float(predicted.get(key, 0.0))
        denominator = max(abs(truth), 1e-9)
        relative_errors.append(abs(predicted_value - truth) / denominator)

    mean_relative_error = sum(relative_errors) / len(relative_errors)
    max_relative_error = max(relative_errors)

    union = expected_tools | used_tools
    tool_use_accuracy = 1.0 if not union else len(expected_tools & used_tools) / len(union)
    hallucinated_tool_calls = float(len(used_tools - expected_tools))
    physical_validity = 1.0 if _within_priors(task, predicted) else 0.0

    numerical_accuracy = max(0.0, 1.0 - mean_relative_error)
    posterior_consistency = max(0.0, 1.0 - ((mean_relative_error + max_relative_error) / 2.0))
    stability_under_perturbation = max(0.0, numerical_accuracy - stress_test.effect_size)
    error_propagation_risk = min(
        1.0,
        max_relative_error * (1.2 if workflow_name == "deep_research" else 0.8),
    )
    confidence_calibration_gap = abs(confidence - numerical_accuracy)

    return {
        "mean_relative_error": round(mean_relative_error, 6),
        "max_relative_error": round(max_relative_error, 6),
        "numerical_accuracy": round(numerical_accuracy, 6),
        "posterior_consistency": round(posterior_consistency, 6),
        "tool_use_accuracy": round(tool_use_accuracy, 6),
        "hallucinated_tool_calls": round(hallucinated_tool_calls, 6),
        "physical_validity": round(physical_validity, 6),
        "stability_under_perturbation": round(stability_under_perturbation, 6),
        "error_propagation_risk": round(error_propagation_risk, 6),
        "confidence_calibration_gap": round(confidence_calibration_gap, 6),
    }


def _within_priors(task: TaskCase, predicted: dict[str, float]) -> bool:
    for key, bounds in task.priors.items():
        value = float(predicted.get(key, 0.0))
        lower, upper = bounds
        if value < lower or value > upper:
            return False
    return True

