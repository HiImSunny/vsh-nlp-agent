"""
Optional ensemble (off by default in run.py).
Run multiple backends / prompt variants, majority vote.
"""
from __future__ import annotations
from collections import Counter
from typing import List, Tuple

from src.config import Config
from src.io_utils import Record
from src.scorer import score_batch


def run_ensemble(
    records: List[Record],
    backends,
    config: Config,
) -> List[Tuple[str, str]]:
    all_answers: dict[str, list] = {r.qid: [] for r in records}
    for backend in backends:
        for qid, answer in score_batch(records, backend, config):
            all_answers[qid].append(answer)
    results: List[Tuple[str, str]] = []
    for record in records:
        votes = Counter(all_answers[record.qid])
        results.append((record.qid, votes.most_common(1)[0][0]))
    return results
