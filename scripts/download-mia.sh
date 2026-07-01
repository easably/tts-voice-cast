#!/usr/bin/env bash
# Download Mia reference clips from the official HumeAI/tada Hugging Face Space.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${ROOT}/samples/en"
BASE_URL="https://huggingface.co/spaces/HumeAI/tada/resolve/main/samples/en"

HUME_MIA_FILES=(
  fb_ears_emo_adoration_freeform.wav
  fb_ears_emo_amazement_freeform.wav
  fb_ears_emo_amusement_freeform.wav
  fb_ears_emo_anger_freeform.wav
  fb_ears_emo_confusion_freeform.wav
  fb_ears_emo_contentment_freeform.wav
  fb_ears_emo_disappointment_freeform.wav
  fb_ears_emo_disgust_freeform.wav
  fb_ears_emo_embarassment_freeform.wav
  fb_ears_emo_fear_freeform.wav
  fb_ears_emo_guilt_freeform.wav
  fb_ears_emo_interest_freeform.wav
  fb_ears_emo_neutral_freeform.wav
  fb_ears_emo_pride_freeform.wav
  fb_ears_emo_relief_freeform.wav
  fb_ears_emo_sadness_freeform.wav
  fb_ears_emo_serenity_freeform.wav
  ljspeech.wav
)

mkdir -p "${DEST}"

download_if_missing() {
  local file="$1"
  local target="${DEST}/${file}"
  if [ -s "${target}" ]; then
    echo "skip ${file}"
    return 0
  fi
  echo "download ${file}"
  curl -fsSL "${BASE_URL}/${file}" -o "${target}"
}

for file in "${HUME_MIA_FILES[@]}"; do
  download_if_missing "${file}"
done

echo "Mia samples ready in ${DEST}"
