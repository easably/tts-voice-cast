# Commercial-safe expressive cast (CC BY 4.0)

For redistribution and commercial audiobooks, use **Nova** (female) and **Leo** (male) from EmoV-DB — same speaker across 5 intonations each, clean studio recordings without room noise.

| Character | Speaker | Intonations | License |
|-----------|---------|-------------|---------|
| Nova | bea (F) | neutral, amused, angry, disgusted, sleepy | CC BY 4.0 |
| Leo | sam (M) | neutral, amused, angry, disgusted, sleepy | CC BY 4.0 |

**Mia** (17 Hume demo emotions) is higher quality and more intonations but **not** cleared for commercial redistribution — use for internal demos only.

## Export for TADA / dots.tts

```bash
python3 adapters/to-tada-presets.py --commercial-only > voices-commercial.json
python3 adapters/to-tada-presets.py --legacy-aliases > voices-full.json
```

## Future expansion (phase 2)

| Source | Speakers | Emotions | License | Notes |
|--------|----------|----------|---------|-------|
| [ESD](https://github.com/HLTSingapore/Emotional-Speech-Data) | 10 EN | 5 | Academic — verify | Parallel sentences, studio |
| [Expresso](https://huggingface.co/datasets/ylacombe/expresso) | 4 | 7+ read styles | Check paper | whisper, confused, laughing |
| LibriTTS-R narrators | many | 1–2 | CC BY 4.0 | Casting variety, not emotions |

Pipeline: clip picker → 24 kHz mono → `manifest-*.json` → `generate-manifest.py`.
