#!/usr/bin/env bash
# Download cast reference WAVs (Leo + Nova + narrators + catalog by default).
# Optional Hume demo (Mia): VOICE_CAST_INCLUDE_HUME_DEMO=1 ./scripts/download-all.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"
SCRIPTS="${ROOT}/scripts"

if [ "${VOICE_CAST_INCLUDE_HUME_DEMO:-0}" = "1" ]; then
  chmod +x "${SCRIPTS}/download-mia.sh"
  "${SCRIPTS}/download-mia.sh"
else
  echo "Skipping Hume demo (Mia). Set VOICE_CAST_INCLUDE_HUME_DEMO=1 to include."
fi

if ! python3 -c "import soundfile, huggingface_hub, pyarrow" 2>/dev/null; then
  python3 -m pip install -q soundfile huggingface_hub pyarrow
fi

export PYTHONPATH="${SCRIPTS}${PYTHONPATH:+:${PYTHONPATH}}"

python3 "${SCRIPTS}/build-emov-characters.py"
python3 "${SCRIPTS}/build-narrator-samples.py"
python3 "${SCRIPTS}/build-narrator-catalog.py"
VOICE_CAST_INCLUDE_HUME_DEMO="${VOICE_CAST_INCLUDE_HUME_DEMO:-0}" python3 "${SCRIPTS}/generate-manifest.py"

echo "All voice-cast samples ready under ${ROOT}/samples/en"
