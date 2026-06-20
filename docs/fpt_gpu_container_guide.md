# FPT GPU Container -- Huong dan chi tiet

## Buoc 1: Tao GPU Container

1. Vao https://ai.fptcloud.com -> GPU Container
2. Click "Create Container"
3. Chon template: **vllm-openai** (co san vLLM + CUDA)
4. Cau hinh:
   - GPU: **1x H200** ($6.6/h, credit $10 => ~1.5 tieng)
   - Volume: 20GB (du)
   - Thoi gian: chon khoang thoi gian can thiet
5. Environment Variables (quan trong):
   - `MODEL=Qwen/Qwen3.5-4B-Instruct` (hoac Qwen3.5-9B-Instruct)
   - `HF_TOKEN=hf_...` (token HuggingFace cua ban, can de download model)
6. SSH public key: them key de SSH vao container

## Buoc 2: Ket noi vao Container

Container tao xong se co:
- Dia chi IP
- Port SSH (thuong 22)
- Ket noi: `ssh root@<IP> -p <port>`

## Buoc 3: Clone repo va chay inference

```bash
# Trong container
git clone https://github.com/YOUR_USERNAME/mcqa-hackaithon.git
cd mcqa-hackaithon

# Cai them dependency
pip install -q transformers accelerate tqdm

# Tao thu muc data, copy file public-test vao
mkdir -p /data /output
# Upload file public-test_1780368312.json vao /data

# Chay inference (dung luon vLLM co san trong template)
MCQA_BACKEND=vllm MCQA_MODEL_ID=Qwen/Qwen3.5-4B-Instruct \
  python src/run.py --data-dir /data --output-dir /output

# Ket qua o /output/pred.csv
```

## Buoc 4: Lay ket qua

Dung SCP de download:
```bash
scp -P <port> root@<IP>:/output/pred.csv .
```

Hoac mount volume va download tu FPT console.

## Backend options

| Bien moi truong | Gia tri | Ghi chu |
|-----------------|---------|---------|
| MCQA_BACKEND | vllm | **Nhanh nhat**, can GPU |
| MCQA_BACKEND | hf | Transformers, cham hon |
| MCQA_BACKEND | unslo | Unsloth, tiet kiem VRAM |
| MCQA_MODEL_ID | Qwen/Qwen3.5-4B-Instruct | 4B params, nhanh |
| MCQA_MODEL_ID | Qwen/Qwen3.5-9B-Instruct | 9B params, chinh xac hon |
| MCQA_MODEL_ID | Qwen/Qwen3.5-0.8B-Instruct | Sieu nhe, thu nghiem |
