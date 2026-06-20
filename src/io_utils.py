"""
discover_input(data_dir) -> list[Record]
  Scan for *test*.csv > *test*.json > *.csv > *.json
  Auto-detect format, normalise choices to list[str]

write_predictions(output_path, [(qid, letter), ...]) -> None
  Write qid,answer CSV
"""
from __future__ import annotations
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass(frozen=True)
class Record:
    qid: str
    question: str
    choices: List[str]


def _normalise_choices(raw) -> List[str]:
    if isinstance(raw, list):
        return [str(c) for c in raw]
    if isinstance(raw, str):
        s = raw.strip()
        if s.startswith("["):
            return [str(c) for c in json.loads(s)]
        return [c.strip() for c in s.split("|")]
    raise ValueError(f"Cannot parse choices: {raw!r}")


def _records_from_json(path: Path) -> List[Record]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array in {path}")
    return [
        Record(
            qid=str(o["qid"]),
            question=str(o["question"]),
            choices=_normalise_choices(o["choices"]),
        )
        for o in data
    ]


def _records_from_csv(path: Path) -> List[Record]:
    records = []
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            records.append(
                Record(
                    qid=str(row["qid"]),
                    question=str(row["question"]),
                    choices=_normalise_choices(row["choices"]),
                )
            )
    return records


def _find_test_file(data_dir: Path) -> Path:
    for pattern in ("*test*.csv", "*test*.json", "*.csv", "*.json"):
        matches = sorted(data_dir.glob(pattern))
        if matches:
            return matches[0]
    raise FileNotFoundError(f"No input file found in {data_dir}")


def discover_input(data_dir) -> List[Record]:
    p = Path(data_dir)
    f = _find_test_file(p)
    if f.suffix.lower() == ".json":
        return _records_from_json(f)
    return _records_from_csv(f)


def write_predictions(
    output_path, results: List[Tuple[str, str]]
) -> None:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["qid", "answer"])
        for qid, answer in results:
            w.writerow([qid, answer])
