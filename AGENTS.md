# AGENTS.md — Project Memory

> Persistent notes for any AI agent working on this repo. Read this first.
> Last verified against source files: 2026-06-20.

## What this project is

We are competing in **Vietnamese Student HackAIthon 2026 — Bảng C (INNOVATOR)**.

- Official framing (PDF): *"sử dụng các mô hình ngôn ngữ lớn để thiết kế AI Agent xử lý đa tác vụ"* (use LLMs to design a multi-task AI Agent).
- Concrete Round-1 deliverable: a **Vietnamese multiple-choice question-answering (MCQA)** system, packaged as a **Docker container**, that reads questions and writes predicted answers. Scored on **accuracy + inference speed + creativity of optimization**.
- Org: Trung ương Hội Sinh viên Việt Nam / VSDS. Site: http://hackaithon.vsds.vn. Contact: hackaithon@vsds.vn.

## The hard I/O contract (DO NOT DEVIATE)

From the official rules (PDF, Bảng C, "Yêu cầu đầu ra"):

- **Entry-point** reads `public_test.csv` **or** `private_test.csv` from `/data`.
- Writes `pred.csv` to `/output` with exactly two columns: **`qid,answer`** where answer is a letter (`A/B/C/D...`).
- Delivery = **Docker container on Docker Hub** + **GitHub repo** with reproduce steps that run inside the container.
- Plus a **method write-up document** (format free) showing creativity/effectiveness of the optimization strategy.

> NOTE: the PDF literally says `(A/B/C/D)`, but the dataset has up to **11 choices** (see below). Answer letters must therefore span **A-K**. This A-D vs A-K discrepancy is the single most important ambiguity to resolve with the organizers / handle defensively. Map choice index 0->A, 1->B, ... 9->J, 10->K.

> NOTE: the contract says input is a `.csv` (`public_test.csv`/`private_test.csv`), but the sample data we were given is `.json`. The container must be robust to the actual file format mounted at `/data` at evaluation time. Treat the on-disk format as discovered-at-runtime, not assumed.

## Allowed models (STRICT - only these)

LLM (pick from):
- **Qwen3.5 Series**, models **<= 9B params** only.
- **Gemma-4 Series**.

Embedding / Rerank (allowed - enables RAG/retrieval):
- **BGE-m3**
- **Qwen-Rerank**

Using any other base model risks disqualification. Quantization/distillation of the above is the optimization lever.

## The data (verified by probe)

Sample file: `public-test_1780368312.json` (~1.0 MB).

- JSON **array of 463 objects**. Keys per object: exactly `qid`, `question`, `choices`.
- **No `answer` field** - this is the unlabeled public test set (we must produce labels; no ground truth to self-score against locally).
- `choices` is always a list. **Choice-count distribution: {2:3, 3:6, 4:318, 5:1, 10:134, 11:1}.** -> NOT fixed 4. Most are 4, but **134 questions have 10 choices**, one has 11. Answer space is A-K.
- `choices` are **raw text** (no "A."/"B." prefix embedded).
- `qid`: `test_0001` ... `test_0463` (note: the submission sample skips test_0002 -> qids are not guaranteed contiguous; always echo the qid from input).
- `question` length: min 12 / mean ~1370 / **max 8712 chars** -> some long reading-comprehension passages. Context length & truncation strategy matters.

Submission template: `submission_1780332147.csv`
```
qid,answer
test_0001,A
test_0003,B
test_0004,C
test_0005,D
```
(Only A-D shown in the tiny sample, but real answers extend to K.)

Private test (final eval): **2000 questions**, hidden, same format.

## Scoring (Vong 2, from PDF)

Total = 100 points (NOTE: a PDF inconsistency - Accuracy formula multiplies by 70 but its points column says "80 diem". Accuracy is clearly the dominant component; resolve exact weight with organizers if possible):
1. **Accuracy** - `a / num_private_sample * 100% * 70` (a = #correct). Dominant.
2. **Inference time** - fastest team gets 10 pts; others `y/x * 100% * 10` (x = fastest team's time, y = this team's time). -> **lower latency = more points**; speed is explicitly scored.
3. **Idea / optimization creativity** - 10 pts (judged).

Implication: maximize accuracy first, but the latency term means we cannot just pick the biggest model and slowest decoding. Model size, quantization, batching, and context-truncation all trade against the speed score.

## Timeline (Bang C)

- **02/6-23/6/2026**: registration.
- **Within 72h after Round 1 close**: submit all required deliverables (Docker + GitHub + write-up) or auto-disqualified.
- **26/6/2026**: submit final tuned Docker; org evaluates on the 2000-question private test.
- **26/6-03/7/2026**: org scores, picks top 6.
- **15/7/2026 (planned)**: Round 3 - online, **max 8 minutes** live presentation + live demo + Q&A.

Prizes Bang C: 1st = 20,000,000 VND; 2nd = 15M; 3rd = 10M; 3x consolation = 5M.

## User & working preferences

- User is Vietnamese; communicates in Vietnamese. Deliverables the user explicitly asked for: a detailed execution plan, onboarding/"things I need to understand" material, a **report script**, a **PDF**, **presentation slides**, an **end-to-end tracking file**, and **git**.
- Global rules in effect (from ~/.claude/rules/ecc): TDD with 80% coverage target, security checklist before commits, code-review after writing code, conventional-commit messages, prefer small files (<800 lines), immutability, research-before-build (gh search / Context7 / Exa).
- Working in `superpowers:brainstorming` flow: **no implementation/scaffolding until a design is presented and the user approves it** (HARD-GATE).

## Environment facts (this machine)

- Project dir: `D:\Code Project\Python Coding\Vietnamese Student HackAIThon` (Windows).
- Python 3.14; console needs `PYTHONIOENCODING=utf-8 python -X utf8` to print Vietnamese (cp1252 default).
- PDF libs available: `pymupdf` (fitz), `pdfplumber`, `pypdf`. The Read tool's PDF path needs `pdftoppm` which is NOT installed - extract PDF text with pymupdf instead.
- A GateGuard "Fact-Forcing" PreToolUse hook fires on the first Bash call / first Write each session: state the user request + what the action produces before running it.
- No git repo yet. No source code yet - greenfield build.

## Open questions to resolve (before/with the user)

1. A-D vs A-K answer space - confirm organizers accept letters beyond D for 10/11-choice items.
2. Exact accuracy weight (70 vs 80) - does not block design.
3. GPU availability for local dev & for the eval environment (drives model size & quantization choices).
4. Online vs offline model weights inside the container at eval time (must likely bake weights into the image -> image size vs allowed).
5. Whether to invest in a RAG/retrieval path (BGE-m3 + Qwen-Rerank are allowed) or rely on long-context direct prompting.
