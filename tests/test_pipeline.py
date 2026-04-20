from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cambagent_eval.config import load_experiment
from cambagent_eval.config import load_tasks
from cambagent_eval.pipeline import run_experiment


EXPERIMENT = ROOT / "configs" / "experiments" / "baseline.json"


class PipelineTests(unittest.TestCase):
    def test_dry_run_report_has_expected_shape(self) -> None:
        spec = load_experiment(EXPERIMENT)
        tasks = load_tasks(spec)
        report = run_experiment(spec, tasks)

        self.assertEqual(20, report.summary["total_runs"])
        self.assertIn("average_metrics", report.summary)
        self.assertIn("failure_counts", report.summary)
        self.assertIn("reasoning_output_mismatch", report.summary["failure_counts"])


if __name__ == "__main__":
    unittest.main()
