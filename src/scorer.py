"""score_batch(records, backend, config) -> list[(qid, letter)]"""
from __future__ import annotations
from typing import List, Optional, Tuple

from tqdm import tqdm

from src.backends.base import BaseBackend
from src.config import Config
from src.io_utils import Record
from src.prompt import build_prompt, build_choice_labels

def score_batch(
    records: List[Record],
    backend: BaseBackend,
    config: Config,
    desc: Optional[str] = None,
) -> List[Tuple[str, str]]:
    results: List[Tuple[str, str]] = []
    for record in tqdm(records, desc=desc or "Inferring"):
        prompt = build_prompt(
            record, config.max_context_chars, config.max_passage_chars
        )
        valid_labels = build_choice_labels(len(record.choices))
        answer = backend.score_choices(prompt, valid_labels)
        results.append((record.qid, answer))
    return results