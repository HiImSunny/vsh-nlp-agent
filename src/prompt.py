"""
answer_index_to_letter(idx) -> str   # 0->"A", 10->"K"
build_choice_labels(n) -> ["A","B",...] up to K
build_prompt(record, max_context_chars, max_passage_chars) -> str
  Vietnamese MCQA template; truncate MIDDLE of question if too long.
  NEVER truncate choices.
"""
from __future__ import annotations
from typing import List

MAX_CHOICES = 11
_MARKER = " [...] "


def answer_index_to_letter(idx: int) -> str:
    if not 0 <= idx < MAX_CHOICES:
        raise ValueError(f"idx {idx} out of range")
    return chr(ord("A") + idx)


def build_choice_labels(n: int) -> List[str]:
    if not 1 <= n <= MAX_CHOICES:
        raise ValueError(f"n={n} must be 1-{MAX_CHOICES}")
    return [chr(ord("A") + i) for i in range(n)]


def _trunc_middle(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    keep = (max_chars - len(_MARKER)) // 2
    return text[:keep] + _MARKER + text[-keep:]


_TPL = (
    "Đây là câu hỏi trắc nghiệm. "
    "Chọn đáp án đúng bằng cách trả lời CHỈ bằng một chữ cái.\n\n"
    "Câu hỏi: {question}\n\n{choices_block}\nĐáp án:"
)


def build_prompt(
    record,
    max_context_chars: int = 8000,
    max_passage_chars: int = 6000,
) -> str:
    question = _trunc_middle(record.question, max_passage_chars)
    labels = build_choice_labels(len(record.choices))
    choices_block = "\n".join(
        f"{l}. {c}" for l, c in zip(labels, record.choices)
    )
    prompt = _TPL.format(question=question, choices_block=choices_block)
    if len(prompt) > max_context_chars:
        overhead = len(prompt) - len(question)
        question = _trunc_middle(
            record.question, max(0, max_context_chars - overhead)
        )
        prompt = _TPL.format(question=question, choices_block=choices_block)
    return prompt
