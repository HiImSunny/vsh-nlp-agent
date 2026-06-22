# ============================================================================
# HackAIthon 2026 Bang C - Vietnamese MCQA Docker image
# Build:  docker build -t hiimsunny/vsh-nlp-agent:latest .
# Run:    docker run --gpus all \
#           -v /path/to/data:/data:ro \
#           -v /path/to/output:/output \
#           hiimsunny/vsh-nlp-agent:latest
# ============================================================================

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir bitsandbytes

COPY src/ src/
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

ARG MODEL_ID=Qwen/Qwen3.5-9B
RUN python -c "from transformers import AutoTokenizer; from transformers import AutoModelForCausalLM; from transformers import BitsAndBytesConfig; import torch; q = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16, bnb_4bit_use_double_quant=True); AutoTokenizer.from_pretrained('${MODEL_ID}', trust_remote_code=True); AutoModelForCausalLM.from_pretrained('${MODEL_ID}', trust_remote_code=True, quantization_config=q, device_map='auto'); print('Model cached OK')"
ENV MCQA_MODEL_ID=${MODEL_ID}

ENV MCQA_BACKEND=hf
ENV MCQA_QUANT=bnb-4bit
ENV MCQA_BATCH_SIZE=4
ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./docker-entrypoint.sh"]
