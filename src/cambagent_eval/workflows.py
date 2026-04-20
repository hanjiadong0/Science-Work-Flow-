from __future__ import annotations

from .models import StressCondition
from .models import TaskCase
from .models import TraceStep


def build_trace(
    workflow_name: str,
    task: TaskCase,
    used_tools: list[str],
    grounding_mode: str,
    stress_test: StressCondition,
    confidence: float,
) -> list[TraceStep]:
    if workflow_name == "deep_research":
        return _build_deep_research_trace(task, used_tools, grounding_mode, stress_test, confidence)
    return _build_one_shot_trace(task, used_tools, grounding_mode, stress_test, confidence)


def _build_one_shot_trace(
    task: TaskCase,
    used_tools: list[str],
    grounding_mode: str,
    stress_test: StressCondition,
    confidence: float,
) -> list[TraceStep]:
    tool_name = used_tools[0] if used_tools else None
    notes = [
        f"Grounding mode: {grounding_mode}",
        f"Stress test: {stress_test.id}",
        f"Expected tools: {', '.join(task.expected_tools) or 'none'}",
    ]
    return [
        TraceStep(
            index=1,
            kind="interpret",
            summary="Parse the precision task and map requested outputs to solver parameters.",
            notes=notes,
        ),
        TraceStep(
            index=2,
            kind="tool_call",
            summary="Execute the primary scientific computation.",
            tool_name=tool_name,
            notes=[f"Domain context items available: {len(task.domain_context)}"],
        ),
        TraceStep(
            index=3,
            kind="report",
            summary="Return parameter estimates with a compact confidence statement.",
            notes=[f"Reported confidence: {confidence:.3f}"],
        ),
    ]


def _build_deep_research_trace(
    task: TaskCase,
    used_tools: list[str],
    grounding_mode: str,
    stress_test: StressCondition,
    confidence: float,
) -> list[TraceStep]:
    retrieval_note = (
        "Domain notes were incorporated before inference."
        if grounding_mode != "plain"
        else "No external grounding was injected."
    )
    inference_tool = used_tools[1] if len(used_tools) > 1 else (used_tools[0] if used_tools else None)
    return [
        TraceStep(
            index=1,
            kind="plan",
            summary="Break the research task into planning, retrieval, inference, and synthesis stages.",
            notes=[f"Stress test: {stress_test.id}"],
        ),
        TraceStep(
            index=2,
            kind="retrieve",
            summary="Gather domain priors or literature cues that constrain the analysis.",
            tool_name=used_tools[0] if used_tools else None,
            notes=[retrieval_note],
        ),
        TraceStep(
            index=3,
            kind="infer",
            summary="Run the inference chain and inspect uncertainty-sensitive outputs.",
            tool_name=inference_tool,
            notes=[f"Domain context items available: {len(task.domain_context)}"],
        ),
        TraceStep(
            index=4,
            kind="synthesize",
            summary="Explain the posterior in natural language and flag potential failure modes.",
            notes=[f"Reported confidence: {confidence:.3f}"],
        ),
    ]

