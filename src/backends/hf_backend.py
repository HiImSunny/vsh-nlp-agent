
"""
HuggingFace Transformers backend (CPU/GPU fallback).
Loads model + tokenizer, gets logits at last position,
picks argmax among valid_labels token ids.

Supports batched inference via score_batch().
"""
from __future__ import annotations
from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from src.backends.base import BaseBackend


class HFBackend(BaseBackend):
    def __init__(self, model_path: str):
        self._tok = AutoTokenizer.from_pretrained(
            model_path, trust_remote_code=True
        )
        if self._tok.pad_token is None:
            self._tok.pad_token = self._tok.eos_token
        self._model = AutoModelForCausalLM.from_pretrained(
            model_path, trust_remote_code=True, torch_dtype=torch.float16
        )
        self._model.eval()
        self._label_ids: dict[str, int] = {}

    def _label_id(self, label: str) -> int:
        if label not in self._label_ids:
            ids = self._tok.encode(label, add_special_tokens=False)
            self._label_ids[label] = ids[0]
        return self._label_ids[label]

    @torch.inference_mode()
    def score_choices(self, prompt: str, valid_labels: List[str]) -> str:
        inputs = self._tok(prompt, return_tensors="pt")
        outputs = self._model(**inputs)
        last_logits = outputs.logits[0, -1, :]
        scores = {
            label: last_logits[self._label_id(label)].item()
            for label in valid_labels
        }
        return max(scores, key=scores.__getitem__)

    @torch.inference_mode()
    def score_batch(
        self, prompts: List[str], labels_list: List[List[str]]
    ) -> List[str]:
        batch = self._tok(
            prompts,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )
        outputs = self._model(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
        )
        logits = outputs.logits

        results: List[str] = []
        for i in range(len(prompts)):
            seq_len = batch["attention_mask"][i].sum().item()
            last_logits = logits[i, seq_len - 1, :]
            valid_labels = labels_list[i]
            scores = {
                label: last_logits[self._label_id(label)].item()
                for label in valid_labels
            }
            results.append(max(scores, key=scores.__getitem__))
        return results

    def close(self) -> None:
        del self._model
