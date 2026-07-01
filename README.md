# tts-voice-cast

Shared voice reference library for **dots.tts** and **TADA**: one speaker, many intonation clips (book narration and dialogue).

## Cast overview

| Group | Characters | Intonations | Commercial use |
|-------|------------|-------------|----------------|
| **Expressive (Hume)** | Mia (F) | **17** | Demo only — verify Hume terms |
| **Expressive (EmoV)** | Nova (F), Leo (M) | **5 each** | **CC BY 4.0** — OK for commercial |
| **Named narrators** | Nora, Owen, LJ | 1–2 | CC BY / public domain |
| **Catalog** | 18 LibriTTS-R | 1 each | CC BY 4.0 |

For **one voice × many clean intonations** with **commercial license**: use **Nova** or **Leo** (or Mia for internal demos).

## Layout

```
manifest.json              # generated full cast
manifest-expressive.json   # Mia + Leo + Nova
emov-characters.json       # EmoV-DB build config (Leo, Nova)
scripts/download-all.sh
adapters/to-dots-presets.py
adapters/to-tada-presets.py
```

## Quick start

```bash
pip install -r requirements-build.txt   # optional; download-all.sh auto-installs
./scripts/download-all.sh
```

## TADA integration

```bash
python3 adapters/to-tada-presets.py --legacy-aliases > voices.json
# merge dialogue_examples / book_examples in the engine repo
```

Submodule: `vendor/voice-cast` in [tada](https://github.com/easably/tada) and [dots-tts](https://github.com/easably/dots-tts).

## Licenses

See [LICENSE-SOURCES.md](LICENSE-SOURCES.md) and [plans/commercial-expressive-cast.md](plans/commercial-expressive-cast.md).
