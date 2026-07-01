# Source licenses and attribution

## Mia (`fb_ears_*`)

- **Origin:** [HumeAI/tada Hugging Face Space](https://huggingface.co/spaces/HumeAI/tada/tree/main/samples/en)
- **Use:** Demo / R&D voice cast (17 emotions). Verify [Hume](https://hume.ai) terms before commercial redistribution.
- **Commercial alternative:** use **Nova** + **Leo** (EmoV-DB, CC BY 4.0).
- **Attribution:** Hume AI TADA demo samples.

## Leo (`leo_*.wav`) / Nova (`nova_*.wav`)

- **Origin:** [EmoV-DB](https://openslr.org/115/) via Hugging Face `erminga/emo-tts`.
  - Leo — speaker **sam** (male)
  - Nova — speaker **bea** (female)
- **License:** **CC BY 4.0** — commercial use allowed with attribution.
- **Attribution:** Adigwe et al., EmoV-DB: A emotional voices database (2018).
- **Note:** Studio-quality acted emotions; 5 intonations per speaker (neutral, amused, angry, disgusted, sleepy). Best **commercial-safe** expressive cast today.

## Mia (`fb_ears_*`, `mia_*` via Hume filenames)

- **Origin:** [LibriTTS-R](https://openslr.org/141/) via `mythicinfinity/libritts_r` (dev-clean).
- **Speakers:** 84 (Christie Nowak, female), 251 (Mark Nelson, male).
- **License:** **CC BY 4.0** — commercial use allowed with attribution.
- **Attribution:** Koizumi et al., LibriTTS-R (Interspeech 2023); Zen et al., LibriTTS (2019).

## LibriTTS catalog (`libri_*_neutral.wav`)

- **Origin:** LibriTTS-R dev-clean — 18 additional narrators (7 female, 11 male).
- **Balance:** Skewed male because expressive cast has more female emotions (Mia 15 vs Leo 5).
- **License:** **CC BY 4.0** — same as LibriTTS-R.
- **Speaker list:** see `catalog-speakers.json`.

## LJ (`lj_neutral.wav`)

- **Origin:** [LJ Speech](https://keithito.com/LJ-Speech-Dataset/) mirror via Hume TADA Space (`ljspeech.wav`).
- **License:** Public domain (US).
- **Note:** Slightly dated studio; very flat, neutral delivery — good for long-form narration tests.

## LJ Speech (`ljspeech.wav`, optional)

- **Origin:** Public domain [LJ Speech](https://keithito.com/LJ-Speech-Dataset/) via Hume Space mirror.
- **Note:** Legacy timbre; prefer Mia/Leo for book work.
