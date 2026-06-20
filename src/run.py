"""Entry point: read /data -> score -> write /output/pred.csv
Usage: python src/run.py [--data-dir DIR] [--output-dir DIR] [--backend BACKEND] [--batch-size N]
"""
from __future__ import annotations
import argparse
import dataclasses
import os
import time


def _ram_summary() -> str:
    """Return a short RAM summary string (host + GPU if available)."""
    parts: list[str] = []
    try:
        with open("/proc/meminfo") as f:
            meminfo = f.read()
        total_kb = 0
        avail_kb = 0
        for line in meminfo.splitlines():
            if line.startswith("MemTotal:"):
                total_kb = int(line.split()[1])
            elif line.startswith("MemAvailable:"):
                avail_kb = int(line.split()[1])
        used_gb = (total_kb - avail_kb) / 1_048_576
        total_gb = total_kb / 1_048_576
        parts.append(f"RAM {used_gb:.1f}/{total_gb:.0f}GB")
    except (OSError, ValueError):
        pass
    try:
        import subprocess
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            timeout=5, text=True,
        )
        for line in out.strip().splitlines():
            used, total = line.split(", ")
            parts.append(f"VRAM {float(used)/1024:.1f}/{float(total)/1024:.0f}GB")
    except Exception:
        pass
    return " | ".join(parts) if parts else ""


from src.config import Config
from src.io_utils import discover_input, write_predictions
from src.scorer import score_batch


def _build_backend(config: Config):
    if config.backend == "stub":
        from src.backends.stub_backend import StubBackend
        return StubBackend()
    if config.backend == "hf":
        from src.backends.hf_backend import HFBackend
        return HFBackend(config.effective_model(), batch_size=config.batch_size)
    if config.backend == "vllm":
        from src.backends.vllm_backend import VLLMBackend
        return VLLMBackend(config.effective_model(), config.quant)
    if config.backend == "unslo":
        from src.backends.unslo_backend import UnsloBackend
        return UnsloBackend(config.effective_model(), config.quant)
    raise ValueError(f"Unknown backend: {config.backend!r}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default=os.environ.get("DATA_DIR", "/data"))
    parser.add_argument("--output-dir", default=os.environ.get("OUTPUT_DIR", "/output"))
    parser.add_argument("--backend", default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    args = parser.parse_args()

    config = Config()
    if args.backend:
        config = dataclasses.replace(config, backend=args.backend)
    if args.batch_size is not None:
        config = dataclasses.replace(config, batch_size=args.batch_size)

    print(f"[1/4] Scanning {args.data_dir} ...")
    records = discover_input(args.data_dir)
    print(f"[1/4] Loaded {len(records)} records  ({_ram_summary()})")

    print(f"[2/4] Loading model {config.effective_model()} (backend={config.backend}, batch_size={config.batch_size}) ...")
    t_load = time.perf_counter()
    backend = _build_backend(config)
    print(f"[2/4] Model loaded in {time.perf_counter() - t_load:.1f}s  ({_ram_summary()})")

    print(f"[3/4] Scoring {len(records)} questions ...")
    t0 = time.perf_counter()
    try:
        results = score_batch(records, backend, config, desc="Scoring")
    finally:
        backend.close()
    elapsed = time.perf_counter() - t0
    qps = len(results) / elapsed if elapsed > 0 else 0
    print(f"[3/4] Scoring done in {elapsed:.1f}s ({qps:.1f} Q/s)  ({_ram_summary()})")

    print(f"[4/4] Writing predictions ...")
    output_path = os.path.join(args.output_dir, "pred.csv")
    write_predictions(output_path, results)
    print(f"[4/4] Wrote {len(results)} predictions to {output_path}")

    print(f"Done! {_ram_summary()}")


if __name__ == "__main__":
    main()