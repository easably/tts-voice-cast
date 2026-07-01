#!/usr/bin/env python3
"""Assemble manifest.json from expressive cast, named narrators, and LibriTTS catalog."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _catalog_character(entry: dict) -> dict:
    sp = str(entry["speaker_id"])
    label = entry.get("label") or entry.get("reader_name", f"Speaker {sp}")
    first = label.split()[0].replace(".", "")
    char_id = f"libri_{sp}"
    wav = f"libri_{sp}_neutral.wav"
    return {
        "id": char_id,
        "label": first,
        "language": "en",
        "gender": entry["gender"],
        "source": "libritts-r",
        "cast_role": "narrator",
        "catalog": True,
        "libritts_speaker_id": sp,
        "reader_name": entry.get("reader_name", label),
        "presets": [
            {
                "id": f"libri_{sp}_neutral",
                "label": f"{first} · neutral",
                "intonation": "neutral",
                "emotion": "neutral",
                "description": f"Audiobook read — LibriTTS-R speaker {sp} ({entry.get('reader_name', label)}).",
                "recording_quality": "audiobook_clean",
                "narration_recommended": True,
                "file": wav,
            }
        ],
    }


def _named_narrator(entry: dict) -> dict:
    char = {
        "id": entry["id"],
        "label": entry["label"],
        "language": "en",
        "gender": entry["gender"],
        "source": entry["source"],
        "cast_role": "narrator",
        "presets": [],
    }
    if entry.get("reader_name"):
        char["reader_name"] = entry["reader_name"]
    if entry.get("libritts_speaker_id"):
        char["libritts_speaker_id"] = str(entry["libritts_speaker_id"])

    for preset in entry["presets"]:
        pid = preset["id"]
        if entry.get("source") == "ljspeech":
            wav = preset.get("file", "ljspeech.wav")
        else:
            wav = f"{pid}.wav"
        intonation = preset.get("intonation", "neutral")
        char["presets"].append(
            {
                "id": pid,
                "label": f"{entry['label']} · {intonation}",
                "intonation": intonation,
                "emotion": "neutral",
                "description": preset.get("description")
                or f"{entry['label']} — {intonation} audiobook reference.",
                "recording_quality": preset.get("recording_quality", "audiobook_clean"),
                "narration_recommended": True,
                "file": wav,
            }
        )
    return char


def main() -> None:
    expressive = json.loads((ROOT / "manifest-expressive.json").read_text(encoding="utf-8"))
    narrators = json.loads((ROOT / "narrators.json").read_text(encoding="utf-8"))
    catalog = json.loads((ROOT / "catalog-speakers.json").read_text(encoding="utf-8"))

    characters = list(expressive["characters"])
    for entry in narrators["narrators"]:
        characters.append(_named_narrator(entry))
    for entry in catalog["speakers"]:
        characters.append(_catalog_character(entry))

    manifest = {
        "version": 1,
        "sample_prefix": "samples/en",
        "balance": {
            "expressive_female": 15,
            "expressive_male": 5,
            "catalog_female": catalog["target_female"],
            "catalog_male": catalog["target_male"],
            "note": catalog.get("balance_note", ""),
        },
        "characters": characters,
    }
    out = ROOT / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(characters)} characters)")


if __name__ == "__main__":
    main()
