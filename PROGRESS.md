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
| Git repo initialized | ✅ | 2026-06-20 | Local only for now |
| Write all skeleton source files | ✅ | 2026-06-20 | TDD RED state — tests exist, impl pending |

## Phase 1 — Core Implementation (TDD)
| Task | Status | Date | Notes |
|------|--------|------|-------|
| `test_io.py` RED | ✅ | 2026-06-20 | 3 tests: JSON, CSV-json-choices, CSV-pipe-choices |
| `test_prompt.py` RED | ✅ | 2026-06-20 | 4 tests: labels 2/4/10/11, template body |
| `test_scorer.py` RED | ✅ | 2026-06-20 | 2 tests: StubBackend valid, batch size |
| `test_run.py` RED | ✅ | 2026-06-20 | 1 integration test: 3-Q fixture → pred.csv |
| Implement `src/config.py` | ✅ | 2026-06-20 | Frozen dataclass, ENV overrides |
| Implement `src/io_utils.py` | ✅ | 2026-06-20 | Auto-detect CSV/JSON, normalize choices |
| Implement `src/prompt.py` | ✅ | 2026-06-20 | Vietnamese template, middle-truncation |
| Implement `src/backends/base.py` | ✅ | 2026-06-20 | ABC |
| Implement `src/backends/stub_backend.py` | ✅ | 2026-06-20 | Hash-based, no GPU needed |
| Implement `src/backends/hf_backend.py` | ⏳ | — | HF transformers, CPU fallback |
| Implement `src/backends/vllm_backend.py` | ⏳ | — | vLLM + guided_choice (cloud GPU) |
| Implement `src/scorer.py` | ✅ | 2026-06-20 | score_batch() |
| Implement `src/run.py` | ✅ | 2026-06-20 | CLI entrypoint |
| All tests GREEN | ⏳ | — | `pytest --cov=src` ≥80% |

## Phase 2 — pred.csv v1 (portal submission)
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Install deps (vllm / hf) on cloud GPU | ⏳ | — | Colab or Kaggle |
| Run on `public-test_1780368312.json` | ⏳ | — | ~463 questions |
| Upload pred.csv to portal | ⏳ | — | **Deadline: before 23/6/2026** |
| Iterate & re-upload (improve score) | ⏳ | — | Multiple submissions allowed |

## Phase 3 — Dockerize & Push
| Task | Status | Date | Notes |
|------|--------|------|-------|
| `docker build` locally | ⏳ | — | |
| Push image to Docker Hub | ⏳ | — | **Deadline: within 72h after round 1 close** |
| Push to GitHub + README reproduce steps | ⏳ | — | Same deadline |
| PDF method doc (`scripts/make_report.py`) | ⏳ | — | Bilingual Vi/En |

## Phase 4 — Final Docker (private 2000Q)
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Benchmark models (Qwen3.5 vs Gemma-4, quant) | ⏳ | — | |
| Tune config for accuracy × speed | ⏳ | — | |
| Submit final Docker | ⏳ | — | **Deadline: 26/6/2026** |

## Phase 5 — Presentation (top-6 only)
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Slide deck (`scripts/make_slides.py`) | ⏳ | — | Bilingual Vi/En, 8 min |
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
