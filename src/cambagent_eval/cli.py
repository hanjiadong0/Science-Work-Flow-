from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import load_experiment
from .config import load_tasks
from .config import validate_experiment
from .models import ExperimentReport
from .pipeline import format_summary
from .pipeline import run_experiment
from .pipeline import write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cambagent-eval",
        description="Scaffolded evaluation runner for scientific-agent experiments.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate an experiment config.")
    validate_parser.add_argument("experiment", help="Path to an experiment JSON file.")

    dry_run_parser = subparsers.add_parser("dry-run", help="Execute the deterministic offline dry run.")
    dry_run_parser.add_argument("experiment", help="Path to an experiment JSON file.")
    dry_run_parser.add_argument(
        "--output",
        help="Optional override for the report output path.",
    )

    summarize_parser = subparsers.add_parser("summarize", help="Print a summary from a generated report.")
    summarize_parser.add_argument("report", help="Path to a report JSON file.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        spec = load_experiment(args.experiment)
        tasks = load_tasks(spec)
        problems = validate_experiment(spec, tasks)
        if problems:
            for problem in problems:
                print(f"[invalid] {problem}")
            return 1
        print(f"[valid] {spec.name}: {len(tasks)} task(s), {len(spec.stress_tests)} stress test(s)")
        return 0

    if args.command == "dry-run":
        spec = load_experiment(args.experiment)
        tasks = load_tasks(spec)
        problems = validate_experiment(spec, tasks)
        if problems:
            for problem in problems:
                print(f"[invalid] {problem}")
            return 1
        report = run_experiment(spec, tasks)
        output_path = Path(args.output).resolve() if args.output else Path(spec.report_path)
        write_report(report, output_path)
        print(format_summary(report))
        print(f"Report written to: {output_path}")
        return 0

    if args.command == "summarize":
        report_path = Path(args.report).resolve()
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        report = ExperimentReport(
            experiment_id=payload["experiment_id"],
            experiment_name=payload["experiment_name"],
            generated_at=payload["generated_at"],
            source_config=payload["source_config"],
            summary=payload["summary"],
            runs=[],
        )
        print(format_summary(report))
        return 0

    parser.print_help()
    return 1
