from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class BaseBackend(ABC):
    @abstractmethod
    def score_choices(self, prompt: str, valid_labels: List[str]) -> str:
        """Return the letter (e.g. 'A') with highest likelihood."""
        ...

    def close(self) -> None:
        pass
