"""
vLLM backend (production, GPU).
Uses guided_choice so output is always a valid label letter.
Compatible with vLLM >=0.4.0 (handles API changes across versions).
Supports batched inference via score_batch().

Requires: pip install vllm
"""
from __future__ import annotations
from typing import List

from tqdm import tqdm
from src.backends.base import BaseBackend


class VLLMBackend(BaseBackend):
    def __init__(self, model_path: str, quant: str = "none"):
        from vllm import LLM, SamplingParams

        self._LLM = LLM
        self._SamplingParams = SamplingParams

        # GuidedDecodingParams import fallback for different vLLM versions
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

    def _make_params(self, valid_labels):
        if self._GuidedDecodingParams is not None:
            guided = self._GuidedDecodingParams(choice=valid_labels)
            return self._SamplingParams(
                max_tokens=1, temperature=0.0, guided_decoding=guided
            )
        return self._SamplingParams(
            max_tokens=1, temperature=0.0, guided_choice=valid_labels,
        )

    def score_choices(self, prompt: str, valid_labels: List[str]) -> str:
        params = self._make_params(valid_labels)
        outputs = self._llm.generate([prompt], params)
        return outputs[0].outputs[0].text.strip()

    def score_batch(
        self, prompts: List[str], labels_list: List[List[str]]
    ) -> List[str]:
        """Batch via vLLM with per-item guided constraints."""
        params_list = [self._make_params(lbls) for lbls in labels_list]
        results: List[str] = []
        for i in tqdm(range(0, len(prompts), 64), desc="vLLM batch", unit="chunk"):
            chunk = prompts[i:i+64]
            chunk_params = params_list[i:i+64]
            outputs = self._llm.generate(chunk, chunk_params)
            results.extend(o.outputs[0].text.strip() for o in outputs)
        return results

    def close(self) -> None:
        del self._llm
