"""TDD RED: integration test -- run.py on 3-Q fixture -> valid pred.csv."""
import csv
import os
import subprocess
import sys
from pathlib import Path

FIXTURE_DIR = "tests/fixtures"


def test_run_produces_valid_pred_csv(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd())
    result = subprocess.run(
        [
            sys.executable,
            "src/run.py",
            "--data-dir",
            str(FIXTURE_DIR),
            "--output-dir",
            str(tmp_path),
            "--backend",
            "stub",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    pred = tmp_path / "pred.csv"
    assert pred.exists()
    rows = list(
        csv.DictReader(pred.read_text(encoding="utf-8").splitlines())
    )
    assert len(rows) == 3
    for row in rows:
        assert "qid" in row
        assert "answer" in row
        assert row["answer"] in list("ABCDEFGHIJK")
