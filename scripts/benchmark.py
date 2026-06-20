"""
Benchmark accuracy + speed on a labeled dev set.
Usage: python scripts/benchmark.py --data-dir data/dev --labels data/dev/labels.csv
"""
from __future__ import annotations
import argparse
import csv
import dataclasses
import time

from src.config import Config
from src.io_utils import discover_input
from src.scorer import score_batch
from src.run import _build_backend


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument(
        "--labels",
        required=True,
        help="CSV with qid,answer columns",
    )
    parser.add_argument("--backend", default="stub")
    parser.add_argument(
        "--output", default=None, help="Write pred.csv to this path"
    )
    args = parser.parse_args()

    config = Config()
    config = dataclasses.replace(config, backend=args.backend)

    # Load ground truth
    gt: dict[str, str] = {}
    with open(args.labels, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            gt[row["qid"]] = row["answer"].strip().upper()

    records = [
        r for r in discover_input(args.data_dir) if r.qid in gt
    ]
    backend = _build_backend(config)

    print(f"Scoring {len(records)} questions with {config.backend}...")
    t0 = time.perf_counter()
    results = score_batch(records, backend, config)
    elapsed = time.perf_counter() - t0
    backend.close()

    correct = sum(1 for qid, ans in results if gt.get(qid) == ans)
    total = len(results)
    acc = correct / total * 100 if total else 0
    qpm = total / elapsed * 60 if elapsed > 0 else 0

    print(f"| Metric | Value |")
    print(f"|--------|-------|")
    print(f"| Accuracy | {acc:.1f}% ({correct}/{total}) |")
    print(f"| Elapsed | {elapsed:.1f}s |")
    print(f"| Throughput | {qpm:.0f} Q/min |")

    if args.output:
        from src.io_utils import write_predictions

        from pathlib import Path

        write_predictions(args.output, results)
        print(f"Predictions written to {args.output}")


if __name__ == "__main__":
    main()
