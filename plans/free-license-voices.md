# Libre (free-license) expressive cast

For redistribution and audiobooks without license risk, use **Nova** (female) and **Leo** (male) from EmoV-DB — same speaker across 5 intonations each, clean studio recordings.

| Field | Meaning |
|-------|---------|
| `free_license: true` | CC BY 4.0 or public domain — OK to use and ship in your product |
| `free_license: false` | Terms unclear or demo-only — exclude by default |

**Mia** (17 Hume demo emotions) is higher quality but **not** libre — kept in `manifest-hume-demo.json`, skipped unless `VOICE_CAST_INCLUDE_HUME_DEMO=1`.

## Export libre voices only

```bash
python3 adapters/to-tada-presets.py --free-license-only --legacy-aliases
python3 adapters/to-dots-presets.py --free-license-only
```

## Merge into engine repo

```bash
python3 adapters/merge-engine-presets.py --engine tada --presets ../tada/presets.json --legacy-aliases
python3 adapters/merge-engine-presets.py --engine dots --presets ../dots-tts/presets.json
```
