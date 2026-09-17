#!/usr/bin/env bash
# Start the demo from any working directory.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

install=false
case "${1:-}" in
  --install) install=true ;;
  -h|--help)
    echo "Usage: ./start.sh [--install]"
    echo "Creates .venv and installs missing dependencies. --install refreshes dependencies."
    echo "Options: HOST=127.0.0.1 PORT=8000 PYTHON=python3"
    exit 0 ;;
  "") ;;
  *) echo "Unknown option: $1 (see --help)" >&2; exit 2 ;;
esac
if (( $# > 1 )); then
  echo "Too many arguments (see --help)." >&2
  exit 2
fi

export HOST="${HOST:-127.0.0.1}"
export PORT="${PORT:-8000}"
if [[ ! "$PORT" =~ ^[0-9]{1,5}$ ]] || (( 10#$PORT < 1 || 10#$PORT > 65535 )); then
  echo "PORT must be an integer between 1 and 65535." >&2
  exit 2
fi
PORT=$((10#$PORT))

if [[ ! -x .venv/bin/python ]]; then
  echo "Creating .venv (Python 3.11+ required)..."
  if command -v uv >/dev/null 2>&1; then
    uv venv --python "${PYTHON:-3.11}" .venv
  else
    "${PYTHON:-python3}" -m venv .venv
  fi
  install=true
fi

.venv/bin/python -c 'import sys; sys.exit("Python 3.11+ is required; recreate .venv with a supported Python." if sys.version_info < (3, 11) else 0)'
if ! .venv/bin/python -c 'import pandemic_prep_dash.main' >/dev/null 2>&1; then
  install=true
fi
if [[ "$install" == true ]]; then
  echo "Installing demo dependencies..."
  if command -v uv >/dev/null 2>&1; then
    uv pip install --python .venv/bin/python -e .
  else
    if ! .venv/bin/python -m pip --version >/dev/null 2>&1; then
      .venv/bin/python -m ensurepip --upgrade
    fi
    .venv/bin/python -m pip install -e .
  fi
fi

echo "Demo: http://${HOST}:${PORT}"
echo "Stop with Ctrl+C. Workflow state resets when the server stops."
exec .venv/bin/python -m uvicorn pandemic_prep_dash.main:app --host "$HOST" --port "$PORT" --workers 1
