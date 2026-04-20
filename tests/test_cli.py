from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cambagent_eval.cli import main


EXPERIMENT = ROOT / "configs" / "experiments" / "baseline.json"


class CliTests(unittest.TestCase):
    def test_validate_command_succeeds(self) -> None:
        exit_code = main(["validate", str(EXPERIMENT)])
        self.assertEqual(0, exit_code)

    def test_dry_run_writes_report(self) -> None:
        report_path = ROOT / "outputs" / "cli_test_report.json"
        if report_path.exists():
            report_path.unlink()

        try:
            exit_code = main(["dry-run", str(EXPERIMENT), "--output", str(report_path)])

            self.assertEqual(0, exit_code)
            data = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(20, data["summary"]["total_runs"])
        finally:
            if report_path.exists():
                report_path.unlink()


if __name__ == "__main__":
    unittest.main()
