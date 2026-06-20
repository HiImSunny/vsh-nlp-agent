"""
Config dataclass -- all overridable via ENV vars.
ENV: MCQA_MODEL_ID, MCQA_MODEL_PATH, MCQA_BACKEND (vllm|hf|stub|unslo),
     MCQA_QUANT (awq|gptq|none|bnb-4bit), MCQA_BATCH_SIZE,
     MCQA_MAX_CONTEXT_CHARS, MCQA_MAX_PASSAGE_CHARS
"""
from __future__ import annotations
import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Config:
    model_id: str = field(
        default_factory=lambda: os.environ.get(
            "MCQA_MODEL_ID", "Qwen/Qwen3.5-4B"
        )
    )
    model_path: str = field(
        default_factory=lambda: os.environ.get("MCQA_MODEL_PATH", "")
    )
    backend: str = field(
        default_factory=lambda: os.environ.get("MCQA_BACKEND", "stub")
    )
    quant: str = field(
        default_factory=lambda: os.environ.get("MCQA_QUANT", "none")
    )
    max_context_chars: int = field(
        default_factory=lambda: int(
            os.environ.get("MCQA_MAX_CONTEXT_CHARS", "8000")
        )
    )
    max_passage_chars: int = field(
        default_factory=lambda: int(
            os.environ.get("MCQA_MAX_PASSAGE_CHARS", "6000")
        )
    )
    batch_size: int = field(
        default_factory=lambda: int(
            os.environ.get("MCQA_BATCH_SIZE", "8")
        )
    )
    max_new_tokens: int = 1  # constrained scoring: 1 token only

    def effective_model(self) -> str:
        return self.model_path if self.model_path else self.model_id
