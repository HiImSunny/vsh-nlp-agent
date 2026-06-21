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
| Git author config | ✅ | 2026-06-21 | Rewrote history: Duy Khang <duykhang.sunext@gmail.com> |

## Phase 1 — Core Implementation (TDD) ✅ DONE
| Task | Status | Date | Notes |
|------|--------|------|-------|
| 13 test suite | ✅ | 2026-06-20 | All GREEN with StubBackend |
| `src/config.py` | ✅ | 2026-06-20 | Frozen dataclass, ENV overrides |
| `src/io_utils.py` | ✅ | 2026-06-20 | Auto-detect CSV/JSON, normalize choices |
| `src/prompt.py` | ✅ | 2026-06-20 | Vietnamese template, middle-truncation |
| `src/backends/` (stub, hf, vllm, unslo) | ✅ | 2026-06-20 | 4 backends |
| `src/scorer.py` + `src/ensemble.py` | ✅ | 2026-06-20 | score_batch, majority vote. Added tqdm progress bar |
| `src/run.py` | ✅ | 2026-06-20 | CLI entrypoint. Added elapsed time + Q/s reporting |
| `scripts/benchmark.py` | ✅ | 2026-06-20 | Accuracy + speed measurement |
| `scripts/make_report.py` | ✅ | 2026-06-20 | Bilingual Vi/En PDF report |
| `scripts/make_slides.py` | ✅ | 2026-06-20 | Bilingual Vi/En PPTX slides |
| FPT GPU Container guide | ✅ | 2026-06-20 | `docs/fpt_gpu_container_guide.md` |
| FPT AI Notebook guide | ✅ | 2026-06-20 | `docs/fpt_ai_notebook_guide.md` |
| FPT Fine-tuning guide | ✅ | 2026-06-20 | `docs/fpt_finetune_guide.md` - pseudo-label approach |

## Phase 2 — pred.csv v1 (portal submission) 🔜 ACTIVE
| Task | Status | Date | Notes |
|------|--------|------|-------|
| Run Qwen3.5-4B (HF backend) | ✅ | 2026-06-21 | L4, 227.3s, 2.0 Q/s, fp16, batch=4 |
| Run Qwen3.5-9B (HF + bnb-4bit) | ✅ | 2026-06-21 | L4, 178.6s, 2.6 Q/s, batch=1, **55 pts** |
| Run Gemma-4-E4B-it (HF, broken weights) | ✅ | 2026-06-21 | L4, 114.1s, 4.1 Q/s, ~~23.75 pts~~ (weights init random) |
| Run Gemma-4-E4B-it (HF, fixed weights) | ✅ | 2026-06-21 | L4, 90.3s, 5.1 Q/s, **51.4 pts** |
| Fix: Gemma4ForCausalLM -> Gemma4ForConditionalGeneration | ✅ | 2026-06-21 | Weight prefix mismatch: model.language_model.layers vs model.layers |
| Fix: space-prefix labels (" A" not "A") | ✅ | 2026-06-21 | Gemma tokenizer: "A"=236776 (rare) vs " A"=562 (common) |
| Compare model scores | ⏳ | — | Qwen9B(55) > Gemma(51.4) > Qwen4B(?) |
| Submit best model | ⏳ | — | 2 submissions left. Deadline: before 23/6/2026 |

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

## Experiment Log
| When | Model | Backend | Quant | Score | Time | Notes |
|------|-------|---------|-------|-------|------|-------|
| 2026-06-21 | Qwen3.5-4B | hf | none | (overwritten) | 227.3s | L4, fp16, batch=4 |
| 2026-06-21 | Qwen3.5-9B | hf | bnb-4bit | **55.0** | 178.6s | L4, batch=1, 4-bit |
| 2026-06-21 | Gemma-4-E4B-it | hf | none | ~~23.75~~ | 114.1s | Broken: Gemma4ForCausalLM + bare labels |
| 2026-06-21 | Gemma-4-E4B-it | hf | none | **51.4** | 90.3s | Fixed: Gemma4ForConditionalGeneration + space labels |

## Submission Log
| When | Version | Score | Notes |
|------|---------|-------|-------|
| 2026-06-21 | Qwen3.5-4B | (overwritten) | First upload, overwritten by 9B |
| 2026-06-21 | Qwen3.5-9B | **55** | Best so far |
| 2026-06-21 | Gemma-4-E4B-it v1 | **23.75** | Broken weights |
| 2026-06-21 | Gemma-4-E4B-it v2 | **51.4** | Fixed. 2 submissions left |

---

## Key Contacts / Links
- Portal: http://hackaithon.vsds.vn
- Email: hackaithon@vsds.vn
- FPT AI Factory: https://ai.fptcloud.com
