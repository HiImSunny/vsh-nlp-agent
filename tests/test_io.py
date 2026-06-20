"""TDD RED: test discover_input and write_predictions."""
import csv
from pathlib import Path
import pytest
from src.io_utils import discover_input, write_predictions, Record

FIXTURE = Path("tests/fixtures/sample_3q.json")


def test_load_json():
    records = discover_input(FIXTURE.parent)
    assert len(records) == 3
    assert records[0].qid == "test_0001"
    assert isinstance(records[0].choices, list)
    assert len(records[0].choices) == 4


def test_load_csv_json_choices(tmp_path):
    csv_file = tmp_path / "public_test.csv"
    csv_file.write_text(
        'qid,question,choices\ntest_0001,Q1,"[""A"",""B""]"\n',
        encoding="utf-8",
    )
    records = discover_input(tmp_path)
    assert records[0].choices == ["A", "B"]


def test_load_csv_pipe_choices(tmp_path):
    csv_file = tmp_path / "public_test.csv"
    csv_file.write_text(
        "qid,question,choices\ntest_0001,Q1,A|B|C\n", encoding="utf-8"
    )
    records = discover_input(tmp_path)
    assert records[0].choices == ["A", "B", "C"]


def test_write_predictions(tmp_path):
    out = tmp_path / "pred.csv"
    write_predictions(out, [("test_0001", "A"), ("test_0003", "C")])
    rows = list(
        csv.reader(out.read_text(encoding="utf-8").splitlines())
    )
    assert rows[0] == ["qid", "answer"]
    assert rows[1] == ["test_0001", "A"]
    assert rows[2] == ["test_0003", "C"]
