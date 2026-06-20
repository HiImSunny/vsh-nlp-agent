"""
Unsloth backend (GPU, memory-optimized inference).
Uses Unsloth FastLanguageModel to load 4-bit quantized models
for reduced GPU memory and faster inference.

Requires: pip install unsloth
"""
from __future__ import annotations
from typing import List

import torch

from src.backends.base import BaseBackend


class UnsloBackend(BaseBackend):
    def __init__(self, model_path: str, quant: str = "bnb-4bit"):
        from unsloth import FastLanguageModel

        self._FastLanguageModel = FastLanguageModel

        load_kwargs: dict = {
            "model_name": model_path,
            "trust_remote_code": True,
        }
        if quant == "bnb-4bit":
            load_kwargs["load_in_4bit"] = True
        elif quant == "bnb-8bit":
            load_kwargs["load_in_8bit"] = True

        self._model, self._tok = FastLanguageModel.from_pretrained(
            **load_kwargs
        )
        FastLanguageModel.for_inference(self._model)
        self._label_ids: dict[str, int] = {}

    def _label_id(self, label: str) -> int:
        if label not in self._label_ids:
            ids = self._tok.encode(label, add_special_tokens=False)
            self._label_ids[label] = ids[0]
        return self._label_ids[label]

    @torch.inference_mode()
    def score_choices(self, prompt: str, valid_labels: List[str]) -> str:
        inputs = self._tok(prompt, return_tensors="pt").to(
            self._model.device
        )
        outputs = self._model(**inputs)
        last_logits = outputs.logits[0, -1, :]
        scores = {
            label: last_logits[self._label_id(label)].item()
            for label in valid_labels
        }
        return max(scores, key=scores.__getitem__)

    def close(self) -> None:
        del self._model
