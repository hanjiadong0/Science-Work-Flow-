from __future__ import annotations

import hashlib
from abc import ABC
from abc import abstractmethod
from typing import Any

from .models import StressCondition
from .models import TaskCase
from .models import TraceStep
from .workflows import build_trace


class AgentAdapter(ABC):
    @abstractmethod
    def run(
        self,
        task: TaskCase,
        model_name: str,
        grounding_mode: str,
        workflow_name: str,
        stress_test: StressCondition,
    ) -> tuple[list[TraceStep], dict[str, Any]]:
        raise NotImplementedError


class StubScientificAgent(AgentAdapter):
    """Deterministic offline agent used to exercise the evaluation loop."""

    def run(
        self,
        task: TaskCase,
        model_name: str,
        grounding_mode: str,
        workflow_name: str,
        stress_test: StressCondition,
    ) -> tuple[list[TraceStep], dict[str, Any]]:
        quality = self._estimate_quality(task, model_name, grounding_mode, workflow_name, stress_test)
        used_tools = self._select_tools(task, quality, grounding_mode, workflow_name)
        parameters = self._predict_parameters(task, model_name, grounding_mode, workflow_name, stress_test, quality)
        confidence = max(0.05, min(0.99, quality + 0.08 * self._signed_noise(task.id, model_name, "confidence")))
        steps = build_trace(workflow_name, task, used_tools, grounding_mode, stress_test, confidence)

        final_output = {
            "parameters": parameters,
            "used_tools": used_tools,
            "confidence": round(confidence, 3),
            "summary": self._summary_text(task, workflow_name, grounding_mode, stress_test),
        }
        return steps, final_output

    def _estimate_quality(
        self,
        task: TaskCase,
        model_name: str,
        grounding_mode: str,
        workflow_name: str,
        stress_test: StressCondition,
    ) -> float:
        quality = 0.58
        model_name_lower = model_name.lower()
        if "frontier" in model_name_lower or "large" in model_name_lower:
            quality += 0.18
        if grounding_mode != "plain":
            quality += 0.10
        if workflow_name == task.default_workflow:
            quality += 0.04
        quality -= stress_test.effect_size
        quality += 0.05 * self._signed_noise(task.id, model_name, grounding_mode, workflow_name, stress_test.id)
        return max(0.08, min(0.97, quality))

    def _predict_parameters(
        self,
        task: TaskCase,
        model_name: str,
        grounding_mode: str,
        workflow_name: str,
        stress_test: StressCondition,
        quality: float,
    ) -> dict[str, float]:
        parameters: dict[str, float] = {}
        error_scale = max(0.015, 0.32 - (quality * 0.26) + (stress_test.effect_size * 0.35))
        for key, truth in task.ground_truth.items():
            noise = self._signed_noise(task.id, model_name, grounding_mode, workflow_name, stress_test.id, key)
            predicted = truth * (1 + noise * error_scale)
            if stress_test.id == "missing_data" and task.task_type == "research_inference" and key == "eccentricity":
                predicted += 0.04
            if stress_test.id == "parameter_misconfiguration" and task.task_type == "tool_precision" and key == "omega_b":
                predicted -= 0.006
            parameters[key] = round(predicted, 6)
        return parameters

    def _select_tools(
        self,
        task: TaskCase,
        quality: float,
        grounding_mode: str,
        workflow_name: str,
    ) -> list[str]:
        tools = list(task.expected_tools)
        if not tools:
            return tools

        if grounding_mode == "plain" and quality < 0.65:
            tools[-1] = "hallucinated_solver"
        elif grounding_mode != "plain" and workflow_name == "deep_research" and "paper_index" not in tools:
            tools.insert(0, "paper_index")
        return tools

    def _summary_text(
        self,
        task: TaskCase,
        workflow_name: str,
        grounding_mode: str,
        stress_test: StressCondition,
    ) -> str:
        return (
            f"Simulated {workflow_name} run for '{task.name}' with "
            f"{grounding_mode} grounding under the '{stress_test.id}' condition."
        )

    def _signed_noise(self, *parts: str) -> float:
        digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
        bucket = int(digest[:8], 16) / 0xFFFFFFFF
        return (bucket * 2.0) - 1.0

