# tts-voice-cast

Shared voice reference library for **dots.tts** and **TADA**: one speaker, many intonation clips (book narration and dialogue).

**One repo, two engines.** WAVs and `manifest.json` are engine-neutral. Each engine only needs a thin adapter (`to-tada-presets.py` / `to-dots-presets.py`) and one merge command (`merge-engine-presets.py`) to write voices into its own `presets.json` while keeping dialogue/book examples.

## Cast overview (default download)

| Group | Characters | Intonations | Libre license |
|-------|------------|-------------|---------------|
| **Expressive (EmoV)** | Nova (F), Leo (M) | **5 each** | **CC BY 4.0** — free to use & redistribute |
| **Named narrators** | Nora, Owen, LJ | 1–2 | CC BY / public domain |
| **Catalog** | 18 LibriTTS-R | 1 each | CC BY 4.0 |

**Optional (not downloaded by default):** Mia (Hume demo, 17 emotions) — `free_license: false`, unclear redistribution terms. Enable with `VOICE_CAST_INCLUDE_HUME_DEMO=1`.

> **Note:** `free_license` means **legally libre** (CC BY, public domain) — **not** “paid voices”. Nova and Leo are free; you do not pay anyone to use them (attribution required for CC BY).

## Layout

```
manifest.json              # generated full cast
manifest-expressive.json   # Leo + Nova (libre)
manifest-hume-demo.json    # Mia (optional, restricted)
scripts/download-all.sh
adapters/to-dots-presets.py
adapters/to-tada-presets.py
adapters/merge-engine-presets.py   # universal merge into engine presets.json
```

## Quick start

```bash
pip install -r requirements-build.txt   # optional; download-all.sh auto-installs
./scripts/download-all.sh
```

Include Hume demo voices:

```bash
VOICE_CAST_INCLUDE_HUME_DEMO=1 ./scripts/download-all.sh
```

## Engine integration

Submodule: `vendor/voice-cast` in [tada](https://github.com/easably/tada) and [dots-tts](https://github.com/easably/dots-tts).

**TADA** (keeps `dialogue_examples` / `book_examples` in `presets.json`):

```bash
python3 adapters/merge-engine-presets.py \
  --engine tada \
  --presets /path/to/tada/presets.json \
  --legacy-aliases
```

**dots.tts**:

```bash
python3 adapters/merge-engine-presets.py \
  --engine dots \
  --presets /path/to/dots-tts/presets.json
```

Export voices only (stdout):

```bash
python3 adapters/to-tada-presets.py --free-license-only --legacy-aliases
python3 adapters/to-dots-presets.py --free-license-only
```

## Licenses

See [LICENSE-SOURCES.md](LICENSE-SOURCES.md) and [plans/free-license-voices.md](plans/free-license-voices.md).
