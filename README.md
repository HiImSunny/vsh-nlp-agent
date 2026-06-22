# vsh-nlp-agent — Vietnamese MCQA System (HackAIthon 2026)

> HackAIthon 2026 — Bảng C (INNOVATOR)  
> Team: Duy Khang  
> Model chính (Final submission): **Qwen/Qwen3.5-9B + bnb-4bit + CLS** — **55.0 điểm trên portal**

---

## Mục lục | Table of Contents

- [Tiếng Việt](#tiếng-việt)
  - [Giới thiệu](#giới-thiệu)
  - [Kết quả thí nghiệm](#kết-quả-thí-nghiệm)
  - [Cách chạy lại kết quả](#cách-chạy-lại-kết-quả)
  - [Docker](#docker)
  - [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [English](#english)
  - [Introduction](#introduction)
  - [Experiment Results](#experiment-results)
  - [Reproduce Results](#reproduce-results)
  - [Docker](#docker-1)
  - [Directory Structure](#directory-structure)

---

# Tiếng Việt

## Giới thiệu

Hệ thống trả lời câu hỏi trắc nghiệm tiếng Việt (MCQA) sử dụng mô hình ngôn ngữ lớn nguồn mở. Đầu vào là file CSV/JSON chứa câu hỏi và lựa chọn, đầu ra là file `pred.csv` với hai cột `qid,answer` (A-K).

**Phương pháp chính:** *Constrained Likelihood Scoring (CLS)* — chỉ cần 1 forward pass qua model để lấy logits tại vị trí cuối cùng, argmax = đáp án. Nhanh gấp 50-100 lần so với sinh văn bản tự do (generation).

## Kết quả thí nghiệm

Chạy trên **NVIDIA L4 (22GB VRAM)** qua Lightning.ai.

| Model | Phương pháp | Lượng tử | Thời gian (463 câu) | Điểm portal |
|-------|------------|---------|-------------------|-------------|
| **Qwen3.5-9B** ✅ | **CLS** | **bnb-4bit** | **179s (2.6 Q/s)** | **55.0** |
| Gemma-4-E4B-it (fixed) | CLS | fp16 | 90s (5.1 Q/s) | 51.4 |
| Qwen3.5-4B | CLS | fp16 | 227s (2.0 Q/s) | ~53.6 |
| Qwen3.5-9B | Generation | bnb-4bit | 1950s (0.24 Q/s) | 28.73 |

## Cách chạy lại kết quả

### Yêu cầu

- GPU 16GB+ VRAM (tối thiểu)
- Python 3.11+
- Docker (tùy chọn)

### 1. Clone repo

```bash
git clone https://github.com/HiImSunny/vsh-nlp-agent.git
cd vsh-nlp-agent
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
pip install bitsandbytes  # cho 4-bit quantization
```

### 3. Chạy inference (Qwen3.5-9B — model nộp final)

```bash
# Môi trường
export MCQA_BACKEND=hf
export MCQA_MODEL_ID=Qwen/Qwen3.5-9B
export MCQA_QUANT=bnb-4bit
export MCQA_BATCH_SIZE=4
export PYTHONPATH=.

# Chạy
python src/run.py --data-dir /path/to/data --output-dir /path/to/output
```

Kết quả sẽ được ghi vào `/path/to/output/pred.csv`.

### 4. Chạy các model khác

```bash
# Qwen3.5-4B (không lượng tử)
export MCQA_MODEL_ID=Qwen/Qwen3.5-4B
export MCQA_QUANT=none
python src/run.py --data-dir /path/to/data --output-dir /path/to/output

# Gemma-4-E4B-it
export MCQA_MODEL_ID=google/gemma-4-E4B-it
export MCQA_QUANT=none
python src/run.py --data-dir /path/to/data --output-dir /path/to/output
```

### 5. Tùy chỉnh

| Biến môi trường | Mô tả | Giá trị mặc định |
|----------------|-------|-----------------|
| `MCQA_BACKEND` | Backend inference (hf / vllm / unslo) | hf |
| `MCQA_MODEL_ID` | HuggingFace model ID | Qwen/Qwen3.5-9B |
| `MCQA_QUANT` | Lượng tử hóa (none / bnb-4bit) | bnb-4bit |
| `MCQA_BATCH_SIZE` | Batch size | 4 |
| `MCQA_MAX_CONTEXT_CHARS` | Context budget (ký tự) | 8000 |
| `MCQA_MAX_PASSAGE_CHARS` | Passage budget (ký tự) | 6000 |

## Docker

### Build

```bash
docker build -t hiimsunny/vsh-nlp-agent:latest .
```

### Chạy

```bash
docker run --gpus all \
  -v /path/to/data:/data:ro \
  -v /path/to/output:/output \
  hiimsunny/vsh-nlp-agent:latest
```

### Pull từ Docker Hub

```bash
docker pull hiimsunny/vsh-nlp-agent:latest
```

## Cấu trúc thư mục

```
vsh-nlp-agent/
├── src/
│   ├── backends/          # 4 backends: stub, hf, vllm, unslo
│   ├── config.py          # Config với ENV overrides
│   ├── io_utils.py        # Đọc CSV/JSON + ghi pred.csv
│   ├── prompt.py          # Prompt template + middle-truncation
│   ├── scorer.py          # score_batch
│   └── run.py             # Entry point
├── scripts/
│   ├── make_report.py     # Tạo PDF method report
│   └── make_slides.py     # Tạo PPTX slides
├── tests/                 # Pytest suite (13 tests)
├── docs/report/           # Method PDF output
├── notebooks/             # Cloud notebook
├── Dockerfile             # Docker image
├── docker-entrypoint.sh   # Docker entrypoint
├── requirements.txt       # Python dependencies
└── README.md
```

---

# English

## Introduction

Vietnamese Multiple-Choice QA system using open-source LLMs. Input is CSV/JSON with questions and choices; output is `pred.csv` with `qid,answer` columns (A-K).

**Core method:** *Constrained Likelihood Scoring (CLS)* — single forward pass through the LLM, extract logits at the last position, argmax = answer. 50-100x faster than free-text generation.

## Experiment Results

Run on **NVIDIA L4 (22GB VRAM)** via Lightning.ai.

| Model | Method | Quantization | Time (463 questions) | Portal Score |
|-------|--------|-------------|---------------------|-------------|
| **Qwen3.5-9B** ✅ | **CLS** | **bnb-4bit** | **179s (2.6 Q/s)** | **55.0** |
| Gemma-4-E4B-it (fixed) | CLS | fp16 | 90s (5.1 Q/s) | 51.4 |
| Qwen3.5-4B | CLS | fp16 | 227s (2.0 Q/s) | ~53.6 |
| Qwen3.5-9B | Generation | bnb-4bit | 1950s (0.24 Q/s) | 28.73 |

## Reproduce Results

### Requirements

- GPU 16GB+ VRAM (minimum)
- Python 3.11+
- Docker (optional)

### 1. Clone

```bash
git clone https://github.com/HiImSunny/vsh-nlp-agent.git
cd vsh-nlp-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install bitsandbytes
```

### 3. Run inference (Qwen3.5-9B — final submission)

```bash
export MCQA_BACKEND=hf
export MCQA_MODEL_ID=Qwen/Qwen3.5-9B
export MCQA_QUANT=bnb-4bit
export MCQA_BATCH_SIZE=4
export PYTHONPATH=.

python src/run.py --data-dir /path/to/data --output-dir /path/to/output
```

Output is written to `/path/to/output/pred.csv`.

### 4. Run other models

```bash
# Qwen3.5-4B (no quantization)
export MCQA_MODEL_ID=Qwen/Qwen3.5-4B
export MCQA_QUANT=none
python src/run.py --data-dir /path/to/data --output-dir /path/to/output

# Gemma-4-E4B-it
export MCQA_MODEL_ID=google/gemma-4-E4B-it
export MCQA_QUANT=none
python src/run.py --data-dir /path/to/data --output-dir /path/to/output
```

### 5. Configuration

| ENV variable | Description | Default |
|-------------|-------------|---------|
| `MCQA_BACKEND` | Inference backend (hf / vllm / unslo) | hf |
| `MCQA_MODEL_ID` | HuggingFace model ID | Qwen/Qwen3.5-9B |
| `MCQA_QUANT` | Quantization (none / bnb-4bit) | bnb-4bit |
| `MCQA_BATCH_SIZE` | Batch size | 4 |
| `MCQA_MAX_CONTEXT_CHARS` | Max context length (chars) | 8000 |
| `MCQA_MAX_PASSAGE_CHARS` | Max passage length (chars) | 6000 |

## Docker

### Build

```bash
docker build -t hiimsunny/vsh-nlp-agent:latest .
```

### Run

```bash
docker run --gpus all \
  -v /path/to/data:/data:ro \
  -v /path/to/output:/output \
  hiimsunny/vsh-nlp-agent:latest
```

### Pull from Docker Hub

```bash
docker pull hiimsunny/vsh-nlp-agent:latest
```

## Directory Structure

```
vsh-nlp-agent/
├── src/
│   ├── backends/          # 4 backends: stub, hf, vllm, unslo
│   ├── config.py          # Config with ENV overrides
│   ├── io_utils.py        # CSV/JSON reader + pred.csv writer
│   ├── prompt.py          # Vietnamese prompt template
│   ├── scorer.py          # Score batching
│   └── run.py             # CLI entrypoint
├── scripts/
│   ├── make_report.py     # PDF method report generator
│   └── make_slides.py     # PPTX slides generator
├── tests/                 # 13 pytest tests
├── docs/report/           # Generated method PDF
├── notebooks/             # Cloud notebook
├── Dockerfile             # Docker build
├── docker-entrypoint.sh   # Docker entrypoint
├── requirements.txt       # Python deps
└── README.md
```

---

**Method report PDF:** `docs/report/method_report.pdf`  
**GitHub:** https://github.com/HiImSunny/vsh-nlp-agent  
**Docker Hub:** https://hub.docker.com/r/hiimsunny/vsh-nlp-agent
