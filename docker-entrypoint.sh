#!/usr/bin/env bash
# docker-entrypoint.sh — run MCQA pipeline inside container
set -euo pipefail

exec python src/run.py \
    --data-dir   "${DATA_DIR:-/data}" \
    --output-dir "${OUTPUT_DIR:-/output}" \
    "$@"
