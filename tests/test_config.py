from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cambagent_eval.config import load_experiment
from cambagent_eval.config import load_tasks
from cambagent_eval.config import validate_experiment


EXPERIMENT = ROOT / "configs" / "experiments" / "baseline.json"


class ConfigTests(unittest.TestCase):
    def test_baseline_experiment_loads_cleanly(self) -> None:
        spec = load_experiment(EXPERIMENT)
        tasks = load_tasks(spec)
        problems = validate_experiment(spec, tasks)

        self.assertEqual([], problems)
        self.assertEqual(2, len(tasks))
        self.assertTrue(spec.report_path.endswith("lab_proposal_baseline_report.json"))


if __name__ == "__main__":
    unittest.main()
