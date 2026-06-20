"""
Prepare MCQA data for FPT AI Studio fine-tuning (Alpaca format).
Usage:
  # Generate pseudo-labels + convert to Alpaca
  python scripts/prepare_finetune_data.py --input public-test_1780368312.json --output data/finetune_train.json

  # Convert existing labeled data to Alpaca
  python scripts/prepare_finetune_data.py --input labeled_data.json --output data/finetune_train.json

Alpaca format: [{"instruction": "...", "input": "...", "output": "..."}]
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
from typing import List

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.prompt import build_prompt, MAX_CHOICES


def load_questions(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def convert_to_alpaca(
    questions: list[dict],
    labels: dict[str, str] | None = None,
) -> list[dict]:
    """Convert MCQA questions to Alpaca format.

    If labels is provided, uses them as ground truth.
    Otherwise sets output to "" for unlabeled data.
    """
    alpaca_data: list[dict] = []
    for q in questions:
        qid = q["qid"]
        question = q["question"]
        choices = q["choices"]

        # Build instruction (generic prompt template)
        labels_list = [chr(ord("A") + i) for i in range(len(choices))]
        choices_text = "\n".join(
            f"{l}. {c}" for l, c in zip(labels_list, choices)
        )
        instruction = (
            "Đây là câu hỏi trắc nghiệm tiếng Việt. "
            "Chọn đáp án đúng bằng cách trả lời CHỈ bằng một chữ cái."
        )
        input_text = f"Câu hỏi: {question}\n\n{choices_text}\nĐáp án:"

        output = labels.get(qid, "") if labels else ""
        if output:
            output = output.upper().strip()

        alpaca_data.append(
            {
                "instruction": instruction,
                "input": input_text,
                "output": output,
            }
        )
    return alpaca_data


def generate_pseudo_labels(
    questions: list[dict], model_id: str = "Qwen/Qwen3.5-4B-Instruct"
) -> dict[str, str]:
    """Run inference to generate pseudo-labels for unlabeled data."""
    print(f"Generating pseudo-labels using {model_id}...")
    print("Note: This requires GPU. Run this on FPT AI Factory, not locally.")

    # We just record the model to use; actual inference happens on FPT
    return {}


def save_alpaca(data: list[dict], output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} examples to {output_path}")
    print(f"With output: {sum(1 for d in data if d['output'])} examples")
    print(f"Without output: {sum(1 for d in data if not d['output'])} examples")


def main():
    parser = argparse.ArgumentParser(
        description="Prepare MCQA data for FPT AI Studio fine-tuning"
    )
    parser.add_argument(
        "--input", required=True, help="Input JSON file (MCQA format)"
    )
    parser.add_argument(
        "--labels",
        default=None,
        help="Optional: CSV with qid,answer columns (ground truth)",
    )
    parser.add_argument(
        "--output",
        default="data/finetune_train.json",
        help="Output JSON file (Alpaca format)",
    )
    args = parser.parse_args()

    questions = load_questions(args.input)
    print(f"Loaded {len(questions)} questions from {args.input}")

    # Load labels if provided
    labels: dict[str, str] | None = None
    if args.labels:
        import csv

        labels = {}
        with open(args.labels, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                labels[row["qid"]] = row["answer"]
        print(f"Loaded {len(labels)} labels from {args.labels}")

    alpaca_data = convert_to_alpaca(questions, labels)
    save_alpaca(alpaca_data, args.output)

    if not labels:
        print("\n[INFO] No labels provided. To generate pseudo-labels:")
        print("  1. Run inference on FPT AI Factory GPU Container:")
        print(
            "     MCQA_BACKEND=vllm MCQA_MODEL_ID=Qwen/Qwen3.5-9B-Instruct \\"
        )
        print("     python src/run.py --data-dir /data --output-dir /output")
        print("  2. Then pass the pred.csv as --labels to this script")


if __name__ == "__main__":
    main()
