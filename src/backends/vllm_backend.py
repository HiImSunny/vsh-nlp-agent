"""
vLLM backend (production, GPU).
Uses guided_choice so output is always a valid label letter.
Requires: pip install vllm
"""
from __future__ import annotations
from typing import List

from src.backends.base import BaseBackend


class VLLMBackend(BaseBackend):
    def __init__(self, model_path: str, quant: str = "none"):
        from vllm import LLM, SamplingParams
        from vllm.sampling_params import GuidedDecodingParams

        self._SamplingParams = SamplingParams
        self._GuidedDecodingParams = GuidedDecodingParams
        kwargs: dict = {"model": model_path, "trust_remote_code": True}
        if quant != "none":
            kwargs["quantization"] = quant
        self._llm = LLM(**kwargs)

    def score_choices(self, prompt: str, valid_labels: List[str]) -> str:
        guided = self._GuidedDecodingParams(choice=valid_labels)
        params = self._SamplingParams(
            max_tokens=1, temperature=0.0, guided_decoding=guided
        )
        outputs = self._llm.generate([prompt], params)
        return outputs[0].outputs[0].text.strip()

    def close(self) -> None:
        del self._llm
