from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseBackend(ABC):
    @abstractmethod
    def score_choices(self, prompt: str, valid_labels: List[str]) -> str:
        """Return the letter (e.g. 'A') with highest likelihood."""
        ...
    
    def score_batch(
        self, prompts: List[str], labels_list: List[List[str]]
    ) -> List[str]:
        """Default: fall back to per-item score_choices."""
        return [
            self.score_choices(p, lbls)
            for p, lbls in zip(prompts, labels_list)
        ]

    def close(self) -> None:
        pass
