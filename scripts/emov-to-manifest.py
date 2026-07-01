#!/usr/bin/env python3
"""Emit expressive character blocks for manifest-expressive.json from emov-characters.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "emov-characters.json").read_text(encoding="utf-8"))
    characters = []
    for char in data["characters"]:
        presets = []
        for _emotion, meta in char["emotions"].items():
            presets.append(
                {
                    "id": meta["id"],
                    "label": f"{char['label']} · {meta['intonation']}",
                    "intonation": meta["intonation"],
                    "emotion": meta["emotion"],
                    "description": meta["description"],
                    "recording_quality": "studio_clean",
                    "narration_recommended": True,
                    "file": f"{meta['id']}.wav",
                }
            )
        block = {
            "id": char["id"],
            "label": char["label"],
            "language": "en",
            "gender": char["gender"],
            "source": char["source"],
            "cast_role": "expressive",
            "free_license": char.get("free_license", False),
            "license": char.get("license"),
            "presets": presets,
        }
        characters.append(block)
    json.dump({"characters": characters}, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    import sys

    main()
