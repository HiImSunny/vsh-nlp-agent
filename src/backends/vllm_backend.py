"""
vLLM backend (production, GPU).
Uses guided_choice so output is always a valid label letter.
Compatible with vLLM >=0.4.0 (handles API changes across versions).

Requires: pip install vllm
"""
from __future__ import annotations
from typing import List

from src.backends.base import BaseBackend


class VLLMBackend(BaseBackend):
    def __init__(self, model_path: str, quant: str = "none"):
        from vllm import LLM, SamplingParams

        self._LLM = LLM
        self._SamplingParams = SamplingParams

        # GuidedDecodingParams is in different locations across vLLM versions.
        # Try multiple import paths for compatibility.
        self._GuidedDecodingParams = None
        for mod_path in (
            "vllm.sampling_params",
            "vllm",
            "vllm.entrypoints.openai.serving_engine",
        ):
            try:
                mod = __import__(mod_path, fromlist=["GuidedDecodingParams"])
                cls = getattr(mod, "GuidedDecodingParams", None)
                if cls is not None:
                    self._GuidedDecodingParams = cls
                    break
            except ImportError:
                continue

        kwargs: dict = {"model": model_path, "trust_remote_code": True}
        if quant != "none":
            kwargs["quantization"] = quant
        self._llm = self._LLM(**kwargs)

    def score_choices(self, prompt: str, valid_labels: List[str]) -> str:
        if self._GuidedDecodingParams is not None:
            guided = self._GuidedDecodingParams(choice=valid_labels)
            params = self._SamplingParams(
                max_tokens=1, temperature=0.0, guided_decoding=guided
            )
        else:
            # Fallback: pass guided_choice directly to SamplingParams
            params = self._SamplingParams(
                max_tokens=1,
                temperature=0.0,
                guided_choice=valid_labels,
            )
        outputs = self._llm.generate([prompt], params)
        return outputs[0].outputs[0].text.strip()

    def close(self) -> None:
        del self._llm
