# FPT AI Notebook -- Huong dan chi tiet

## Buoc 1: Tao AI Notebook

1. Vao https://ai.fptcloud.com -> AI Notebook
2. Click "Launch Notebook"
3. Chon cau hinh:
   - GPU: **1x H200** ($6.6/h, credit $10 => ~1.5 tieng)
   - Volume: 20GB
4. Choose image: Python 3.11 + CUDA
5. Launch (cho vai phut de khoi tao)

## Buoc 2: Mo JupyterLab

Sau khi notebook READY, click "Open" de mo JupyterLab.
Day la moi truong giong Colab nhung co GPU that.

## Buoc 3: Upload file va chay

### 3a. Upload data file
- Keo file `public-test_1780368312.json` vao JupyterLab
- Hoac dung terminal trong JupyterLab de download:
```bash
mkdir -p /data /output
# Neu co link Google Drive
# gdown --id <FILE_ID> -O /data/
```

### 3b. Clone repo
Mo Terminal trong JupyterLab:
```bash
git clone https://github.com/YOUR_USERNAME/mcqa-hackaithon.git
cd mcqa-hackaithon
pip install -q transformers accelerate tqdm
# Neu dung vLLM:
# pip install -q vllm
```

### 3c. Chay notebook
Mo file `notebooks/cloud_run.ipynb` trong JupyterLab
Chay tung cell -> ket qua o /output/pred.csv

## Buoc 4: Download ket qua

Trong JupyterLab, click chuot phai vao /output/pred.csv -> Download

## Luu y credit

- H200: $6.6/h
- Credit $10 => ~1.5 tieng
- **Stop notebook khi khong dung** de tranh ton credit
- FPT tinh phi theo thoi gian thuc (per-minute billing)
