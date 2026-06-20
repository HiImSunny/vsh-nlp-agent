# FPT Fine-tuning Pipeline -- Huong dan chi tiet

Dung credit **$70 (AI Studio)** de fine-tune Qwen3.5-4B.
Muc tieu: tang accuracy bang **semi-supervised learning** -- dung pseudo-labels tu chinh model.

## Nguyen ly

1. Chay inference model tot nhat (Qwen3.5-9B) tren 463 cau public test -> lay **pseudo-labels**
2. Dung pseudo-labels do fine-tune model nho hon (Qwen3.5-4B) bang LoRA
3. Model fine-tuned co the hieu format MCQA tieng Viet tot hon

## Buoc 1: Tao pseudo-labels

```bash
# Chay inference bang vLLM tren FPT GPU Container / AI Notebook
# Dung model LON nhat co the (Qwen3.5-9B) de lay pseudo-labels chat luong cao
MCQA_BACKEND=vllm MCQA_MODEL_ID=Qwen/Qwen3.5-9B \
  python src/run.py --data-dir /data --output-dir /output

# Ket qua: /output/pred.csv (463 dong qid,answer)
```

## Buoc 2: Chuyen doi sang Alpaca format

```bash
# Chuyen public test + pseudo-labels -> Alpaca format
python scripts/prepare_finetune_data.py \
  --input public-test_1780368312.json \
  --labels /output/pred.csv \
  --output data/finetune_train.json
```

## Buoc 3: Upload du lieu len Data Hub

1. Vao https://ai.fptcloud.com -> **Data Hub**
2. Click "Create Data Connection"
3. Upload file `data/finetune_train.json`
4. Dat ten: `mcqa_pseudo_train`
5. Copy dataset ID

## Buoc 4: Tao Fine-tuning Pipeline

1. Vao https://ai.fptcloud.com -> **Model Fine-tuning** -> "Create Pipeline"

### 4a. Select Base Model
- Model source: **Hugging Face**
- Model name: `Qwen/Qwen3.5-4B`
- Trainer: **Built-in trainer** (SFT)

### 4b. Dataset
- Dataset format: **Alpaca**
- Dataset: chon `mcqa_pseudo_train` tu Data Hub
- Split: Train (80%) / Eval (20%)

### 4c. Hyperparameters
| Tham so | Gia tri | Ghi chu |
|---------|---------|---------|
| Epochs | 3-5 | It epoch de tranh overfit vao pseudo-labels sai |
| Learning rate | 2e-4 | LoRA learning rate |
| LoRA rank | 16 | Can bang toc do va chat luong |
| LoRA alpha | 32 | |
| Max seq length | 2048 | Du cho cau hoi + choices |
| Batch size | 4 | Dieu chinh theo VRAM |

### 4d. Infrastructure
- GPU: **1x H200** (re nhat)
- Volume: 20GB

## Buoc 5: Train & Lay model

1. Click "Start" -> ~15-30 phut -> ~$3-6
2. Model duoc luu vao **Model Hub**
3. Vao Model Hub -> Download model ve
4. Hoac dung **Interactive Session** de test thu

## Buoc 6: Dung fine-tuned model cho inference

```bash
# Chay inference bang fine-tuned model
MCQA_BACKEND=hf MCQA_MODEL_PATH=/path/to/finetuned/model \
  python src/run.py --data-dir /data --output-dir /output
```

## Luu y

- **Pseudo-labels tu Qwen3.5-9B co the sai** (~10-20% error rate). Fine-tuning van co the giup model nho hon hoc format va cai thien accuracy tong the.
- **463 examples** la du cho LoRA fine-tuning (khong can nhieu)
- Co the chay **nhieu vong**: fine-tune -> inference -> fine-tune lai voi pseudo-labels moi (self-training)
- LoRA chi ton ~2-4GB VRAM, phu hop H200 (141GB)
- **Quan trong**: chi fine-tune sau khi da co ket qua baseline (submission dau tien) de so sanh
