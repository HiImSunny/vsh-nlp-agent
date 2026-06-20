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
| Git repo initialized | ✅ | 2026-06-20 | 3 commits |

## Phase 1 — Core Implementation (TDD) ✅ DONE
| Task | Status | Date | Notes |
|------|--------|------|-------|
| 13 test suite | ✅ | 2026-06-20 | All GREEN with StubBackend |
| `src/config.py` | ✅ | 2026-06-20 | Frozen dataclass, ENV overrides |
| `src/io_utils.py` | ✅ | 2026-06-20 | Auto-detect CSV/JSON, normalize choices |
| `src/prompt.py` | ✅ | 2026-06-20 | Vietnamese template, middle-truncation |
| `src/backends/` (stub, hf, vllm, unslo) | ✅ | 2026-06-20 | 4 backends |
| `src/scorer.py` + `src/ensemble.py` | ✅ | 2026-06-20 | score_batch, majority vote |
| `src/run.py` | ✅ | 2026-06-20 | CLI entrypoint |
| `scripts/benchmark.py` | ✅ | 2026-06-20 | Accuracy + speed measurement |
| `scripts/make_report.py` | ✅ | 2026-06-20 | Bilingual Vi/En PDF report |
| `scripts/make_slides.py` | ✅ | 2026-06-20 | Bilingual Vi/En PPTX slides |
| FPT GPU Container guide | ✅ | 2026-06-20 | `docs/fpt_gpu_container_guide.md` |
| FPT AI Notebook guide | ✅ | 2026-06-20 | `docs/fpt_ai_notebook_guide.md` |
| FPT Fine-tuning guide | ✅ | 2026-06-20 | `docs/fpt_finetune_guide.md` - pseudo-label approach |

## Phase 2 — pred.csv v1 (portal submission) 🔜 NEXT
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Chay inference tren FPT GPU Container | ⏳ | — | Qwen3.5-4B hoac 9B, see `docs/` |
| Upload pred.csv len portal | ⏳ | — | **Deadline: before 23/6/2026** |
| Iterate & improve | ⏳ | — | Multiple submissions allowed |

## Phase 3 — Dockerize & Push
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Build Docker + push Docker Hub | ⏳ | — | **72h after round 1 close** |
| Push to GitHub + reproduce steps | ⏳ | — | Same deadline |
| PDF method doc (`scripts/make_report.py`) | ⏳ | — | Run after benchmarking |

## Phase 4 — Fine-tuning (Optional, post-baseline)
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Run inference (Qwen3.5-9B) -> pseudo-labels | ⏳ | — | Can GPU tren FPT |
| Chuyen doi -> Alpaca format | ⏳ | — | `scripts/prepare_finetune_data.py` |
| Upload + fine-tune tren FPT AI Studio | ⏳ | — | LoRA, $70 credit |
| Final inference private test (2000Q) | ⏳ | — | **Deadline: 26/6/2026** |

## Phase 5 — Presentation (top-6)
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
- FPT AI Factory: https://ai.fptcloud.com
