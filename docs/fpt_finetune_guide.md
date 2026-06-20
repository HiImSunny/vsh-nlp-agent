# FPT Fine-tuning Pipeline -- Huong dan chi tiet

Dung credit **$70 (AI Studio)** de fine-tune Qwen3.5-4B tren du lieu MCQA tieng Viet.
Muc tieu: tang accuracy bang cach day model hieu ro hon ve MCQA tieng Viet.

## Buoc 1: Chuan bi du lieu

### 1a. Du lieu synthetic (da co)
File `data/synthetic_train.json`: **65 cau hoi** MCQA tieng Viet da co nhan.
Dinh dang Alpaca:
```json
{
  "instruction": "Đây là câu hỏi trắc nghiệm tiếng Việt...",
  "input": "Câu hỏi: Thủ đô của Việt Nam là gì?\n\nA. Hà Nội\nB. TP.HCM\nC. Đà Nẵng\nD. Huế\nĐáp án:",
  "output": "A"
}
```

### 1b. Tao pseudo-labels tu public test (khuyen nghi)
Truoc khi fine-tune, nen chay inference tren 463 cau public test
de lay pseudo-labels lam them du lieu train:

```bash
# Chay inference bang vLLM (tren GPU Container hoac AI Notebook)
MCQA_BACKEND=vllm MCQA_MODEL_ID=Qwen/Qwen3.5-9B-Instruct \
  python src/run.py --data-dir /data --output-dir /output

# Chuyen doi sang Alpaca format (co nhan)
python scripts/prepare_finetune_data.py \
  --input public-test_1780368312.json \
  --labels /output/pred.csv \
  --output data/public_pseudo_train.json
```

Gop chung voi synthetic:
```bash
python -c "
import json
with open('data/synthetic_train.json') as f: a = json.load(f)
with open('data/public_pseudo_train.json') as f: b = json.load(f)
combined = a + [x for x in b if x['output']]  # chi lay co nhan
with open('data/combined_train.json', 'w') as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)
print(f'Combined: {len(combined)} examples')
"
```

## Buoc 2: Upload du lieu len Data Hub

1. Vao https://ai.fptcloud.com -> **Data Hub**
2. Click "Create Data Connection"
3. Upload file `data/combined_train.json` (hoac `data/synthetic_train.json`)
4. Dat ten: `mcqa_train_data`
5. Copy dataset ID de dung sau

## Buoc 3: Tao Fine-tuning Pipeline

1. Vao https://ai.fptcloud.com -> **Model Fine-tuning**
2. Click "Create Pipeline"

### 3a. Select Base Model
- Model source: **Hugging Face**
- Model name: `Qwen/Qwen3.5-4B-Instruct`
- Trainer: **Built-in trainer** (SFT)

### 3b. Dataset
- Dataset format: **Alpaca**
- Dataset: chon `mcqa_train_data` tu Data Hub
- Split: Train (80%) / Eval (20%) tu dong

### 3c. Hyperparameters (goi y)
| Tham so | Gia tri | Ghi chu |
|---------|---------|---------|
| Epochs | 3 | Khong nen qua nhieu, tranh overfit |
| Learning rate | 2e-4 | LoRA learning rate |
| LoRA rank | 16 | Can bang toc do va chat luong |
| LoRA alpha | 32 | |
| Max seq length | 2048 | Du cho cau hoi + choices |
| Batch size | 4 | Dieu chinh theo VRAM |

### 3d. Infrastructure
- GPU: **1x H200** (phe nhat)
- Volume: 20G (du cho ~500 cau)

## Buoc 4: Train

1. Review config, click "Start"
2. Thoi gian uoc tinh: ~15-30 phut cho 65-500 examples
3. Chi phi: ~$3-6 (trong credit $70)
4. Theo doi trong Pipeline Management

## Buoc 5: Lay model da fine-tune

1. Sau khi hoan thanh, model duoc luu vao **Model Hub**
2. Vao Model Hub, chon model -> "Download" hoac "Create Version"
3. De su dung cho inference, dung Interactive Session:
   - Vao **Interactive Session**
   - Tao session, chon fine-tuned model
   - Test thu voi cau hoi MCQA

## Buoc 6: Dung fine-tuned model cho inference

Sau khi co model ID tu Model Hub:

```bash
# Chay inference bang fine-tuned model
MCQA_BACKEND=hf \
MCQA_MODEL_ID=Qwen/Qwen3.5-4B-Instruct \
MCQA_MODEL_PATH=/path/to/finetuned/model \
  python src/run.py --data-dir /data --output-dir /output
```

## Luu y

- **65 examples la it**: Co the chua du de cai thien accuracy dang ke
- **Tao them pseudo-labels** tu public test (463 cau) se giup nhieu hon
- Neu co the, tim them Vietnamese MCQ datasets online de fine-tune
- LoRA fine-tuning chi ton ~2-4GB VRAM, phu hop voi H200 141GB
- Co the chay nhieu epoch (5-10) neu dung du lieu it de model hoc ky hon
