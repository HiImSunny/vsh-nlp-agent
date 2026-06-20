# PROGRESS — Vietnamese MCQA HackAIthon 2026 (Bảng C)

> Auto-updated each commit. Legend: ✅ done · 🔄 in progress · ⏳ pending · ❌ blocked

---

## Phase 0 — Setup & Design
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Read rules PDF, understand scoring | ✅ | 2026-06-20 | Accuracy ~70-80pt, Speed 10pt, Creativity 10pt |
| Probe dataset (`public-test_1780368312.json`) | ✅ | 2026-06-20 | 463 Q, choices 2-11, max qlen 8712 chars |
| Write AGENTS.md memory file | ✅ | 2026-06-20 | All project context persisted |
| Design spec approved | ✅ | 2026-06-20 | `docs/superpowers/specs/2026-06-20-mcqa-system-design.md` |
| Git repo initialized | ✅ | 2026-06-20 | First commit with scaffold |

## Phase 1 — Core Implementation (TDD)
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Test suite (13 tests) | ✅ | 2026-06-20 | All GREEN with StubBackend |
| `src/config.py` | ✅ | 2026-06-20 | Frozen dataclass, ENV overrides |
| `src/io_utils.py` | ✅ | 2026-06-20 | Auto-detect CSV/JSON, normalize choices |
| `src/prompt.py` | ✅ | 2026-06-20 | Vietnamese template, middle-truncation |
| `src/backends/stub_backend.py` | ✅ | 2026-06-20 | Hash-based, no GPU needed |
| `src/backends/hf_backend.py` | ✅ | 2026-06-20 | HF transformers, CPU fallback |
| `src/backends/vllm_backend.py` | ✅ | 2026-06-20 | vLLM + guided_choice (cloud GPU) |
| `src/backends/unslo_backend.py` | ✅ | 2026-06-20 | Unsloth 4-bit (GPU, memory-efficient) |
| `src/scorer.py` | ✅ | 2026-06-20 | score_batch() |
| `src/run.py` | ✅ | 2026-06-20 | CLI entrypoint |
| `scripts/benchmark.py` | ✅ | 2026-06-20 | Accuracy + speed measurement |
| `scripts/make_report.py` | ✅ | 2026-06-20 | Bilingual Vi/En PDF report |
| `scripts/make_slides.py` | ✅ | 2026-06-20 | Bilingual Vi/En PPTX slides |

## Phase 1b — FPT AI Factory Integration
| Task | Status | Date | Notes |
|------|--------|------|-------|
| `scripts/prepare_finetune_data.py` | ✅ | 2026-06-20 | MCQA -> Alpaca format |
| `scripts/generate_synthetic_data.py` | ✅ | 2026-06-20 | 65 synthetic Vi MCQA examples |
| `notebooks/cloud_run.ipynb` | ✅ | 2026-06-20 | Updated for FPT AI Notebook |
| `docs/fpt_gpu_container_guide.md` | ✅ | 2026-06-20 | Step-by-step GPU Container |
| `docs/fpt_ai_notebook_guide.md` | ✅ | 2026-06-20 | Step-by-step AI Notebook |
| `docs/fpt_finetune_guide.md` | ✅ | 2026-06-20 | Step-by-step fine-tuning pipeline |

## Phase 2 — pred.csv v1 (portal submission)
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Install deps on FPT GPU Container | ⏳ | — | See `docs/fpt_gpu_container_guide.md` |
| Run on `public-test_1780368312.json` | ⏳ | — | ~463 questions, ~$3-6 on H200 |
| Upload pred.csv to portal | ⏳ | — | **Deadline: before 23/6/2026** |
| Iterate & re-upload (improve score) | ⏳ | — | Multiple submissions allowed |

## Phase 3 — Dockerize & Push
| Task | Status | Date | Notes |
|------|--------|------|-------|
| `docker build` locally | ⏳ | — | Dockerfile ready |
| Push image to Docker Hub | ⏳ | — | **Deadline: within 72h after round 1 close** |
| Push to GitHub + README reproduce steps | ⏳ | — | Same deadline |
| PDF method doc (`scripts/make_report.py`) | ✅ | 2026-06-20 | Script ready, run after benchmarking |

## Phase 4 — Fine-tuning (FPT AI Studio)
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Generate synthetic training data | ✅ | 2026-06-20 | 65 questions in `data/synthetic_train.json` |
| Run inference on public test (pseudo-labels) | ⏳ | — | Need GPU on FPT |
| Upload data to FPT Data Hub | ⏳ | — | See `docs/fpt_finetune_guide.md` |
| Create fine-tuning pipeline | ⏳ | — | Qwen3.5-4B-Instruct, LoRA |
| Download fine-tuned model | ⏳ | — | |
| Final inference on private test (2000Q) | ⏳ | — | **Deadline: 26/6/2026** |

## Phase 5 — Presentation (top-6 only)
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Slide deck (`scripts/make_slides.py`) | ✅ | 2026-06-20 | Script ready |
| Rehearsal | ⏳ | — | **Deadline: 15/7/2026** |

---

## Submission Log
| When | Version | Portal Score | Notes |
|------|---------|-------------|-------|
| — | v0 (stub) | — | placeholder |

---

## Key Contacts / Links
- Portal: http://hackaithon.vsds.vn
- Email: hackaithon@vsds.vn
- Docker Hub repo: (TBD)
- GitHub repo: (TBD)
- FPT AI Factory: https://ai.fptcloud.com
