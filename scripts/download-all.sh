#!/usr/bin/env bash
# Download all cast reference WAVs (Mia + Leo + narrators + catalog).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"
SCRIPTS="${ROOT}/scripts"

chmod +x "${SCRIPTS}/download-mia.sh"
"${SCRIPTS}/download-mia.sh"

if ! python3 -c "import soundfile, huggingface_hub, pyarrow" 2>/dev/null; then
  python3 -m pip install -q soundfile huggingface_hub pyarrow
fi

export PYTHONPATH="${SCRIPTS}${PYTHONPATH:+:${PYTHONPATH}}"

python3 "${SCRIPTS}/build-leo.py" --tar
python3 "${SCRIPTS}/build-narrator-samples.py"
python3 "${SCRIPTS}/build-narrator-catalog.py"
python3 "${SCRIPTS}/generate-manifest.py"

echo "All voice-cast samples ready under ${ROOT}/samples/en"
