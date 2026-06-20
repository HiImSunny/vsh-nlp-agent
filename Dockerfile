# ─────────────────────────────────────────────────────────────────────────────
# HackAIthon 2026 Bảng C — Vietnamese MCQA Docker image
# Build: docker build -t mcqa-hackaithon .
# Run:   docker run --gpus all \
#          -v /path/to/data:/data:ro \
#          -v /path/to/output:/output \
#          mcqa-hackaithon
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install vLLM (GPU path); skip if building CPU-only image
# Uncomment for GPU image with vLLM:
# RUN pip install --no-cache-dir vllm

# Install Unsloth (GPU, memory-efficient); skip if building CPU-only image
# Uncomment for GPU image with Unsloth:
# RUN pip install --no-cache-dir unsloth

# Copy application source
COPY src/ src/
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# ── Model weights ────────────────────────────────────────────────────────────
# Bake weights into image so the container works offline at eval time.
# Set MCQA_MODEL_PATH env to the baked path.
#
# Option A: copy pre-downloaded weights
# COPY weights/ /weights/
# ENV MCQA_MODEL_PATH=/weights/qwen3.5-4b
#
# Option B: download at build time (needs internet during docker build)
# ARG MODEL_ID=Qwen/Qwen3.5-4B-Instruct
# RUN python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
#                AutoTokenizer.from_pretrained('$MODEL_ID'); \
#                AutoModelForCausalLM.from_pretrained('$MODEL_ID')"
# ENV MCQA_MODEL_ID=${MODEL_ID}

# Default environment
ENV MCQA_BACKEND=vllm
ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./docker-entrypoint.sh"]
