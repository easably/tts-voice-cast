#!/usr/bin/env python3
"""Generate TADA voice entries from manifest.json (stdout: JSON array)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"

LEGACY_ALIASES = {
    "narrator_neutral": ("mia_neutral", "Narrator — neutral"),
    "narrator_calm": ("mia_calm", "Narrator — calm"),
    "host_excited": ("mia_amused", "Host — amused"),
    "character_sad": ("mia_sad", "Character — sad"),
    "character_angry": ("mia_angry", "Character — angry"),
    "character_curious": ("mia_curious", "Character — curious"),
    "character_amazed": ("mia_amazed", "Character — amazed"),
    "character_fear": ("mia_fearful", "Character — fearful"),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Export TADA presets from voice-cast manifest")
    parser.add_argument(
        "--commercial-only",
        action="store_true",
        help="Only voices with commercial_safe=true (CC-BY / public domain)",
    )
    parser.add_argument(
        "--legacy-aliases",
        action="store_true",
        help="Append legacy narrator_* / character_* ids for older API clients",
    )
    args = parser.parse_args()

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    prefix = data.get("sample_prefix", "samples/en")
    voices: list[dict] = [
        {
            "id": "zero",
            "label": "Zero-shot",
            "description": "No voice reference — generic synthesis.",
            "recording_quality": "generic",
            "narration_recommended": False,
            "sample": None,
            "emotion": "neutral",
        }
    ]
    by_id: dict[str, dict] = {}

    for character in data.get("characters", []):
        if args.commercial_only and not character.get("commercial_safe"):
            continue

        char_id = character["id"]
        char_label = character.get("label", char_id)

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
                "sample": f"{prefix}/{preset['file']}",
            }
            if character.get("cast_role"):
                entry["cast_role"] = character["cast_role"]
            if character.get("catalog"):
                entry["catalog"] = True
            if character.get("commercial_safe") is not None:
                entry["commercial_safe"] = character["commercial_safe"]
            if character.get("license"):
                entry["license"] = character["license"]
            if preset.get("hint"):
                entry["hint"] = preset["hint"]
            voices.append(entry)
            by_id[entry["id"]] = entry

    if args.legacy_aliases:
        for legacy_id, (target_id, label) in LEGACY_ALIASES.items():
            if target_id in by_id:
                voices.append({**by_id[target_id], "id": legacy_id, "label": label})

    if not args.commercial_only:
        voices.append(
            {
                "id": "ljspeech",
                "label": "Classic (LJ Speech)",
                "description": "Reference from the public LJ Speech dataset.",
                "recording_quality": "legacy",
                "narration_recommended": False,
                "commercial_safe": True,
                "license": "public-domain",
                "hint": "Older studio recording — prefer Nova/Leo for commercial work.",
                "sample": f"{prefix}/ljspeech.wav",
                "emotion": "neutral",
            }
        )

    json.dump(voices, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
