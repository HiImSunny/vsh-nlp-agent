"""TDD RED: test score_batch with StubBackend."""
from src.backends.stub_backend import StubBackend
from src.config import Config
from src.io_utils import Record
from src.prompt import build_choice_labels
from src.scorer import score_batch

RECORDS = [
    Record(
        qid="test_0001",
        question="Q1?",
        choices=["A", "B", "C", "D"],
    ),
    Record(qid="test_0003", question="Q2?", choices=["X", "Y"]),
]


def test_stub_returns_valid_label():
    backend = StubBackend()
    config = Config()
    results = score_batch(RECORDS, backend, config)
    for qid, answer in results:
        record = next(r for r in RECORDS if r.qid == qid)
        valid = build_choice_labels(len(record.choices))
        assert answer in valid


def test_batch_size_equals_record_count():
    backend = StubBackend()
    config = Config()
    results = score_batch(RECORDS, backend, config)
    assert len(results) == len(RECORDS)
