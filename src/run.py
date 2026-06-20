"""
Entry point: read /data -> score -> write /output/pred.csv
Usage: python src/run.py [--data-dir DIR] [--output-dir DIR] [--backend BACKEND]
"""
from __future__ import annotations
import argparse
import dataclasses
import os

from src.config import Config
from src.io_utils import discover_input, write_predictions
from src.scorer import score_batch


def _build_backend(config: Config):
    if config.backend == "stub":
        from src.backends.stub_backend import StubBackend

        return StubBackend()
    if config.backend == "hf":
        from src.backends.hf_backend import HFBackend

        return HFBackend(config.effective_model())
    if config.backend == "vllm":
        from src.backends.vllm_backend import VLLMBackend

        return VLLMBackend(config.effective_model(), config.quant)
    if config.backend == "unslo":
        from src.backends.unslo_backend import UnsloBackend

        return UnsloBackend(config.effective_model(), config.quant)
    raise ValueError(f"Unknown backend: {config.backend!r}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir", default=os.environ.get("DATA_DIR", "/data")
    )
    parser.add_argument(
        "--output-dir", default=os.environ.get("OUTPUT_DIR", "/output")
    )
    parser.add_argument("--backend", default=None)
    args = parser.parse_args()

    config = Config()
    if args.backend:
        config = dataclasses.replace(config, backend=args.backend)

    records = discover_input(args.data_dir)
    print(f"Loaded {len(records)} records from {args.data_dir}")

    backend = _build_backend(config)
    try:
        results = score_batch(records, backend, config)
    finally:
        backend.close()

    output_path = os.path.join(args.output_dir, "pred.csv")
    write_predictions(output_path, results)
    print(f"Wrote {len(results)} predictions to {output_path}")


if __name__ == "__main__":
    main()
