"""Deterministic hash-based backend -- no GPU, for unit tests."""
from __future__ import annotations
from typing import List
from src.backends.base import BaseBackend


class StubBackend(BaseBackend):
    def score_choices(self, prompt: str, valid_labels: List[str]) -> str:
        return valid_labels[hash(prompt) % len(valid_labels)]
