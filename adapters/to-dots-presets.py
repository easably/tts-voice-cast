#!/usr/bin/env python3
"""Generate dots.tts voice entries from manifest.json (stdout: JSON array)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"

LANG_MAP = {"en": "EN", "zh": "ZH", "ru": "RU"}


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    prefix = data.get("sample_prefix", "samples/en")
    voices: list[dict] = [
        {
            "id": "zero_shot",
            "label": "Zero-shot — random voice",
            "description": "No reference audio — random speaker voice.",
            "cloning_mode": "no_reference",
            "narration_recommended": False,
            "language": "any",
            "sample": None,
            "prompt_text": None,
        }
    ]

    for character in data.get("characters", []):
        char_id = character["id"]
        char_label = character.get("label", char_id)
        lang = LANG_MAP.get(character.get("language", "en"), "EN")

        for preset in character.get("presets", []):
            entry = {
                    "id": preset["id"],
                    "label": preset["label"],
                    "character": char_id,
                    "character_label": char_label,
                    "intonation": preset.get("intonation"),
                    "emotion": preset.get("emotion"),
                    "description": preset.get("description", ""),
                    "recording_quality": preset.get("recording_quality", "studio_clean"),
                    "narration_recommended": preset.get("narration_recommended", True),
                    "cloning_mode": "x_vector",
                    "language": lang,
                    "sample": f"{prefix}/{preset['file']}",
                    "prompt_text": "",
                }
            if character.get("cast_role"):
                entry["cast_role"] = character["cast_role"]
            if character.get("catalog"):
                entry["catalog"] = True
            voices.append(entry)

    json.dump(voices, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
