# Method Summary -- HackAIthon 2026 Bang C (INNOVATOR)

## Team / Submission

- Competition: HackAIthon 2026 Bang C -- AI Agent da tac vu (MCQA)
- Task: Answer Vietnamese multiple-choice questions, output qid,answer (A-K)
- Deliverable: Docker container + GitHub repo + this method doc

## Core Method: Constrained Likelihood Scoring (CLS)

Instead of generating free text (slow, error-prone), we use a single forward pass:

1. Build prompt: Vietnamese instruction + question + labelled choices
2. Forward pass through LLM
3. Extract logits ONLY for valid label tokens (A through K)
4. Argmax = answer

**Advantages:**
- Always valid output (no parsing errors)
- 1 token generation = extremely fast inference
- Works for any number of choices (2 to 11)

## Architecture

src/
  config.py         -- Config dataclass, ENV overrides
  io_utils.py       -- Auto-detect CSV/JSON, normalise choices
  prompt.py         -- Vietnamese MCQA template, middle-truncation
  backends/
    stub_backend.py   -- Deterministic hash (testing)
    hf_backend.py     -- HuggingFace Transformers (CPU fallback)
    vllm_backend.py   -- vLLM guided_choice (GPU production)
    unslo_backend.py  -- Unsloth 4-bit (GPU memory-efficient)
  scorer.py         -- score_batch: prompt -> score -> collect
  run.py            -- Entry point: /data -> /output/pred.csv

## Models Used

- Qwen3.5-4B-Instruct (primary)
- Qwen3.5-9B-Instruct (if GPU allows)
- Optional: Unsloth 4-bit quantization for memory efficiency

## Optimization

- AWQ quantization (vLLM) / BnB 4-bit (Unsloth)
- Middle-truncation for long passages (keep end of context)
- Context budget: 8000 chars
- Batch inference for throughput

## FPT AI Factory Integration

- Container: GPU Container (vLLM template) or AI Notebook (JupyterLab)
- GPU: NVIDIA H200 (141 GB VRAM)
- Pipeline: git clone -> pip install -> run inference -> download pred.csv
- Fine-tuning (optional): pseudo-labels from inference -> LoRA on Qwen3.5-4B

## Key Results

(To be filled after benchmarking)

## Links

- GitHub: (TBD)
- Docker Hub: (TBD)
