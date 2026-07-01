# tts-voice-cast

Shared voice reference library for **dots.tts** and **TADA**: one speaker, many intonation clips (book narration and dialogue).

## Layout

```
manifest.json           # engine-neutral cast metadata
samples/en/             # WAV files (downloaded, not committed)
scripts/download-mia.sh # Hume TADA Space — Mia (17 emotions)
scripts/build-leo.py    # EmoV-DB speaker sam — Leo (5 emotions)
scripts/download-all.sh # both
adapters/to-dots-presets.py
adapters/to-tada-presets.py   # future
```

## Quick start

```bash
./scripts/download-all.sh
# Mia: ~10 MB from Hugging Face (no token)
# Leo: needs pip install huggingface_hub soundfile
```

## dots.tts integration

Submodule at `vendor/voice-cast` in [dots-tts](https://github.com/easably/dots-tts). Docker build runs `download-all.sh` and copies `samples/en/` into the app image.

Regenerate `presets.json` voices:

```bash
python3 adapters/to-dots-presets.py > /path/to/dots-tts/presets.voices.json
# merge dialogue_examples / book_examples from existing presets.json
```

## Licenses

See [LICENSE-SOURCES.md](LICENSE-SOURCES.md).
