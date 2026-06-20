"""TDD RED: test prompt building."""
import pytest
from src.prompt import (
    answer_index_to_letter,
    build_choice_labels,
    build_prompt,
)
from src.io_utils import Record


def test_labels_2():
    assert build_choice_labels(2) == ["A", "B"]


def test_labels_4():
    assert build_choice_labels(4) == ["A", "B", "C", "D"]


def test_labels_10():
    assert build_choice_labels(10) == list("ABCDEFGHIJ")


def test_labels_11():
    assert build_choice_labels(11) == list("ABCDEFGHIJK")


def test_template_contains_choices():
    r = Record(qid="x", question="Q?", choices=["opt1", "opt2"])
    p = build_prompt(r)
    assert "A. opt1" in p
    assert "B. opt2" in p
    assert "Đáp án:" in p


def test_truncation_keeps_choices():
    long_q = "x" * 10000
    r = Record(qid="x", question=long_q, choices=["opt1", "opt2"])
    p = build_prompt(r, max_context_chars=500, max_passage_chars=300)
    assert "A. opt1" in p
    assert "B. opt2" in p
    assert "[...]" in p
