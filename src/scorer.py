
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
    # Build all prompts and labels upfront
    prompts: List[str] = []
    labels_list: List[List[str]] = []
    for record in tqdm(records, desc=desc or "Preparing"):
        prompt = build_prompt(
            record, config.max_context_chars, config.max_passage_chars
        )
        valid_labels = build_choice_labels(len(record.choices))
        prompts.append(prompt)
        labels_list.append(valid_labels)

    # Batch inference through backend
    answers = backend.score_batch(prompts, labels_list)
    return [(r.qid, a) for r, a in zip(records, answers)]
