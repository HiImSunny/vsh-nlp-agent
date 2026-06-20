"""
Prepare MCQA data for FPT AI Studio fine-tuning (Alpaca format).

Usage:
  # Buoc 1: Chay inference tren FPT GPU container de lay pred.csv
  MCQA_BACKEND=vllm MCQA_MODEL_ID=Qwen/Qwen3.5-4B-Instruct \
    python src/run.py --data-dir /data --output-dir /output

  # Buoc 2: Chuyen doi public test + pseudo-labels thanh Alpaca format
  python scripts/prepare_finetune_data.py \
    --input public-test_1780368312.json \
    --labels /output/pred.csv \
    --output data/finetune_train.json

Alpaca format: [{"instruction": "...", "input": "...", "output": "..."}]
"""
from __future__ import annotations
import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def load_questions(path: str) -> list[dict]:
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def load_labels(path: str) -> dict[str, str]:
    labels = {}
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            labels[row["qid"]] = row["answer"].strip().upper()
    return labels


def convert_to_alpaca(
    questions: list[dict],
    labels: dict[str, str] | None = None,
) -> list[dict]:
    """Convert MCQA questions to Alpaca format.

    If labels is provided, uses them as pseudo-labels (from inference).
    Otherwise sets output to "" for unlabeled data (not useful for training).
    """
    alpaca_data: list[dict] = []
    for q in questions:
        qid = q["qid"]
        question = q["question"]
        choices = q["choices"]

        labels_list = [chr(ord("A") + i) for i in range(len(choices))]
        choices_text = "\n".join(
            f"{l}. {c}" for l, c in zip(labels_list, choices)
        )
        instruction = (
            "ÄÃ¢y lÃ  cÃ¢u há»i tráº¯c nghiá»‡m tiáº¿ng Viá»‡t. "
            "Chá»n Ä‘Ã¡p Ã¡n Ä‘Ãºng báº±ng cÃ¡ch tráº£ lá»i CHá»ˆ báº±ng má»™t chá»¯ cÃ¡i."
        )
        input_text = f"CÃ¢u há»i: {question}\n\n{choices_text}\nÄÃ¡p Ã¡n:"

        output = labels.get(qid, "") if labels else ""
        if output and output not in labels_list:
            print(f"  [WARN] {qid}: output '{output}' not in {labels_list}")

        alpaca_data.append(
            {
                "instruction": instruction,
                "input": input_text,
                "output": output,
            }
        )
    return alpaca_data


def save_alpaca(data: list[dict], output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    n_with = sum(1 for d in data if d["output"])
    print(f"Saved {len(data)} examples to {output_path}")
    print(f"  Co nhan (output!=): {n_with}")
    print(f"  Khong nhan (output=): {len(data) - n_with}")


def main():
    parser = argparse.ArgumentParser(
        description="Chuyen MCQA JSON + pred.csv -> Alpaca format cho FPT fine-tuning"
    )
    parser.add_argument(
        "--input", required=True, help="File JSON cau hoi (MCQA format)"
    )
    parser.add_argument(
        "--labels",
        default=None,
        help="File CSV tu inference (qid,answer), dung lam pseudo-labels",
    )
    parser.add_argument(
        "--output",
        default="data/finetune_train.json",
        help="File JSON output (Alpaca format)",
    )
    args = parser.parse_args()

    questions = load_questions(args.input)
    print(f"Doc {len(questions)} cau hoi tu {args.input}")

    labels = load_labels(args.labels) if args.labels else None
    if labels:
        print(f"Doc {len(labels)} pseudo-labels tu {args.labels}")

    alpaca_data = convert_to_alpaca(questions, labels)
    save_alpaca(alpaca_data, args.output)


if __name__ == "__main__":
    main()
