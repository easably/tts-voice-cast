# Source licenses and attribution

## Field: `free_license`

- **`true`** — CC BY 4.0 or public domain. Free to use and redistribute (attribution where required).
- **`false`** — demo-only or unclear terms. **Excluded from default download and preset export.**

This is **not** about payment. Nova and Leo are libre; you do not pay for them.

## Mia (`fb_ears_*`, optional)

- **Origin:** [HumeAI/tada Hugging Face Space](https://huggingface.co/spaces/HumeAI/tada/tree/main/samples/en)
- **Use:** Internal demo / R&D (17 emotions). `free_license: false` — verify [Hume](https://hume.ai) terms before redistribution.
- **Libre alternative:** **Nova** + **Leo** (EmoV-DB, CC BY 4.0).
- **Attribution:** Hume AI TADA demo samples.
- **Enable:** `VOICE_CAST_INCLUDE_HUME_DEMO=1 ./scripts/download-all.sh`

## Leo (`leo_*.wav`) / Nova (`nova_*.wav`)

- **Origin:** [EmoV-DB](https://openslr.org/115/) via Hugging Face `erminga/emo-tts`.
  - Leo — speaker **sam** (male)
  - Nova — speaker **bea** (female)
- **License:** **CC BY 4.0** — libre use with attribution.
- **Attribution:** Adigwe et al., EmoV-DB: A emotional voices database (2018).
- **Note:** 5 intonations per speaker (neutral, amused, angry, disgusted, sleepy).

## Nora / Owen (`nora_*.wav`, `owen_*.wav`)

- **Origin:** [LibriTTS-R](https://openslr.org/141/) via `mythicinfinity/libritts_r` (dev-clean).
- **Speakers:** 84 (Christie Nowak, female), 251 (Mark Nelson, male).
- **License:** **CC BY 4.0**
- **Attribution:** Koizumi et al., LibriTTS-R (Interspeech 2023); Zen et al., LibriTTS (2019).

## LibriTTS catalog (`libri_*_neutral.wav`)

- **Origin:** LibriTTS-R dev-clean — 18 additional narrators (7 female, 11 male).
- **License:** **CC BY 4.0**
- **Speaker list:** see `catalog-speakers.json`.

## LJ (`lj_neutral.wav`)

- **Origin:** [LJ Speech](https://keithito.com/LJ-Speech-Dataset/) mirror via Hume TADA Space (`ljspeech.wav`).
- **License:** Public domain (US).
- **Note:** Slightly dated studio; flat neutral delivery.
