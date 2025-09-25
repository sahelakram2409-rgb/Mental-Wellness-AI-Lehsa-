#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="${PYTHONPATH:-$(pwd)}"
PORT="${PORT:-8000}"
python -m uvicorn app:app --host 0.0.0.0 --port "$PORT" --reload
