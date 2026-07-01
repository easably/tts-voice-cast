#!/usr/bin/env bash
# Download all cast reference WAVs (Mia + Leo).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

chmod +x scripts/download-mia.sh
./scripts/download-mia.sh

if ! python3 -c "import soundfile, huggingface_hub" 2>/dev/null; then
  python3 -m pip install -q soundfile huggingface_hub
fi

python3 scripts/build-leo.py --tar

python3 scripts/build-narrator-samples.py

echo "All voice-cast samples ready under ${ROOT}/samples/en"
