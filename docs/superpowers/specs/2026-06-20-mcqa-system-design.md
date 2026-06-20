# Design Spec: Vietnamese MCQA System — HackAIthon 2026 Bang C

**Date:** 2026-06-20  
**Status:** APPROVED

---

## 1. Problem Statement

Build a Vietnamese multiple-choice question-answering (MCQA) system using only allowed small open-source LLMs, packaged as a Docker container that:
- Reads a test file (`public_test.csv` or `private_test.csv`) from `/data`
- Writes `pred.csv` to `/output` with columns `qid,answer` (letter A to K)
- Is scored on **Accuracy** (dominant ~70-80pts) + **Inference speed** (10pts) + **Idea creativity** (10pts)

**Deadline constraints (from portal screenshot + PDF):**
- Before 23/6/2026: submit pred.csv to leaderboard portal (multiple times OK — iterate to climb).
- Within 72h after round 1 closes: Docker Hub + GitHub + PDF method doc.
- 26/6/2026: final Docker for private test (2000 questions).
- 15/7/2026: Slides + 8-min live presentation (top 6 only).

---

## 2. Allowed Models (Strict)

**LLM** (one or more of):
- Qwen3.5 Series, <=9B params
- Gemma-4 Series

**Embedding/Rerank** (optional, for RAG if needed later):
- BGE-m3
- Qwen-Rerank

Any other base model = disqualification risk.

**Compute:** Cloud GPU (Colab / Kaggle / rented GPU).

---

## 3. Data Schema

```
Input (from /data):
  File format: CSV or JSON (auto-detected at runtime)
  Fields: qid (str), question (str), choices (list[str] or JSON-encoded str)

Output (/output/pred.csv):
  qid,answer
  test_0001,A
  test_0003,D
  ...
  Answer letter mapping: index 0->A, 1->B, ..., 10->K

Known dataset (public-test_1780368312.json):
  - 463 questions
  - choice counts: {2:3, 3:6, 4:318, 5:1, 10:134, 11:1}
  - max question length: 8712 chars
  - NO answer field (unlabeled public test)
```

**Critical ambiguity:** PDF says answer = (A/B/C/D) but dataset has up to 11 choices.
Defensive mapping: `chr(ord('A') + choice_index)` handles A..K automatically.

---

## 4. Core Technical Approach

### 4A. Constrained Likelihood Scoring (Core — Huong A)

Instead of generating free text, we score each choice using the model's logits for
a single letter token. The model outputs exactly 1 token for the final answer.

Prompt template (bilingual reasoning in Vietnamese):
```
Day la cau hoi trac nghiem. Chon dap an dung bang cach tra loi chi bang mot chu cai.

Cau hoi: {question}

A. {choices[0]}
B. {choices[1]}
...
{last_label}. {choices[n-1]}

Dap an:
```

Then: extract logits for tokens A, B, ..., last_valid_label only. Argmax = answer.

**Why this wins on both scoring dimensions:**
- Accuracy: no format-parsing errors, always valid output, works for any N choices.
- Speed: 1 forward pass per question, minimal token generation (1 token).

### 4B. Ensemble / Self-Consistency (optional, Huong B — plug in if time allows)

Run 2-3 prompt variants or 2 models, take majority vote.
Implemented in `ensemble.py` but NOT in default v1 entrypoint.

---

## 5. Software Architecture

```
src/
  config.py          # Settings dataclass: model_id, backend, quant, max_len, batch_size
                     # All overridable via ENV vars (MCQA_MODEL, MCQA_BACKEND, etc.)
  io_utils.py        # discover_input(data_dir) -> list[Record]
                     # Auto-detect CSV/JSON, normalize choices field
                     # write_predictions(output_path, list[(qid, letter)])
  prompt.py          # build_prompt(record) -> str
                     # build_choice_labels(n) -> ["A","B",...] up to K
                     # answer_index_to_letter(i) -> str
  backends/
    base.py          # ABC: score_choices(prompt, valid_labels) -> str
    vllm_backend.py  # vLLM + guided_choice + quantization (production, GPU)
    hf_backend.py    # Hugging Face transformers (dev fallback, runs on CPU)
    stub_backend.py  # deterministic (hash-based), for unit tests without GPU
  scorer.py          # score_batch(records, backend, config) -> list[(qid, letter)]
  ensemble.py        # (optional) run_ensemble(records, backends) -> list[(qid, letter)]
  run.py             # ENTRY POINT: /data -> score -> /output/pred.csv

tests/
  test_io.py         # unit: JSON load, CSV load (JSON-choices), CSV (pipe-choices)
  test_prompt.py     # unit: label gen for 2/4/10/11 choices; template renders correctly
  test_scorer.py     # unit: StubBackend returns valid label; batch = 1 result per record
  test_run.py        # integration: run.py on 3-question fixture -> valid pred.csv

scripts/
  benchmark.py       # measure accuracy/speed on labeled dev set, print markdown table
  make_report.py     # generate bilingual Vi/En PDF -> docs/report/method_report.pdf
  make_slides.py     # generate bilingual slide deck -> docs/slides/presentation.pdf

notebooks/
  cloud_run.ipynb    # Colab/Kaggle: pip install vllm, load model, run, save pred.csv

Dockerfile           # base image -> install deps -> copy weights -> entrypoint
docker-entrypoint.sh # exec python src/run.py
requirements.txt     # pinned Python deps
```

---

## 6. I/O Robustness

`discover_input()` logic:
1. Scan `/data` for `*test*.csv` first, then `*test*.json`, then any `.csv`, any `.json`.
2. CSV path: parse header; `choices` column may be JSON-encoded list OR pipe-separated string.
3. JSON path: array of objects with at minimum `qid`, `question`, `choices`.
4. Output: `list[Record]` where `Record.choices` is always `list[str]`.
5. Always echo `Record.qid` verbatim into pred.csv — never renumber.

---

## 7. Context Length Strategy

Max question ~8712 chars + 10 choices ~3000 chars = ~4000 tokens.
- `max_context_chars` in config (default 8000 chars total).
- If question alone exceeds `max_passage_chars` (default 6000): truncate the **middle** of the passage, keep start + end (question stem is usually at the end).
- **Never truncate choices** — they define the answer space.

---

## 8. Performance Targets

| Metric | Target |
|--------|--------|
| Accuracy on public portal | >60% v1, aim >75% after tuning |
| Throughput | >20 questions/min on cloud A100 |
| pred.csv validity (format) | 100% (enforced by constrained scoring) |
| Unit test coverage | >=80% |

---

## 9. Delivery Map

| Deliverable | Mechanism | Due |
|---|---|---|
| pred.csv v1 (portal upload) | run.py on public test | ASAP today |
| Improved pred.csv (iterate) | benchmark + tune | 20-23/6 |
| Docker Hub push | Dockerfile | by 23/6 |
| GitHub + reproduce steps | README.md | by 23/6 |
| PDF method doc (bilingual) | make_report.py | 24-25/6 |
| Final Docker (private 2000Q) | tuned pipeline | 26/6 |
| PROGRESS.md (tracking) | updated each commit | rolling |
| Slide deck (bilingual) | make_slides.py | 10-14/7 |
| Live 8-min demo | rehearsal | 15/7 |

---

## 10. TDD Plan (RED-GREEN-REFACTOR)

1. `test_io.py`: 3 tests (JSON / CSV-JSON-choices / CSV-pipe-choices) — write first, impl second.
2. `test_prompt.py`: 4 tests (label gen 2,4,10,11 choices; template body). 
3. `test_scorer.py`: 2 tests (StubBackend valid label; batch size = record count).
4. `test_run.py`: 1 integration test (3-Q fixture -> pred.csv has 3 valid rows).
Coverage: `pytest --cov=src --cov-report=term-missing`, target >=80%.

---

## 11. Out of Scope (YAGNI for 6 days)

- RAG with BGE-m3/Qwen-Rerank (questions are self-contained passages).
- LoRA fine-tuning (time risk with 6-day window).
- Ensemble enabled by default (code present, off by default).
- Web UI / API server.

---

## 12. Open Questions

1. Do organizers accept letters beyond D for 10/11-choice questions? -> Defensive A-K mapping in place.
2. Accuracy weight: formula says x70 but column says "80 diem" -> does not block design.
3. Does eval environment have internet? -> Bake weights into image to be safe.
