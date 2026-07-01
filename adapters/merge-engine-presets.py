#!/usr/bin/env python3
"""Merge voice-cast voices into an engine presets.json (keeps dialogue/book examples)."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = {
    "tada": ROOT / "adapters/to-tada-presets.py",
    "dots": ROOT / "adapters/to-dots-presets.py",
}
EXAMPLE_KEYS = ("dialogue_examples", "book_examples")


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge voice-cast into engine presets.json")
    parser.add_argument("--engine", choices=["tada", "dots"], required=True)
    parser.add_argument(
        "--presets",
        type=Path,
        required=True,
        help="Path to presets.json (voices merged in; examples preserved)",
    )
    parser.add_argument(
        "--include-restricted",
        action="store_true",
        help="Include Hume demo voices (free_license=false). Default: libre voices only.",
    )
    parser.add_argument(
        "--legacy-aliases",
        action="store_true",
        help="TADA only: append narrator_* / character_* ids for older clients",
    )
    args = parser.parse_args()

    adapter = ADAPTERS[args.engine]
    if not adapter.is_file():
        raise SystemExit(f"Missing adapter: {adapter}")

    manifest = ROOT / "manifest.json"
    if not manifest.is_file():
        env = os.environ.copy()
        if args.include_restricted:
            env["VOICE_CAST_INCLUDE_HUME_DEMO"] = "1"
        subprocess.run([sys.executable, str(ROOT / "scripts/generate-manifest.py")], check=True, env=env)

    cmd = [sys.executable, str(adapter)]
    if not args.include_restricted:
        cmd.append("--free-license-only")
    if args.legacy_aliases and args.engine == "tada":
        cmd.append("--legacy-aliases")

    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    voices = json.loads(proc.stdout)

    presets_path = args.presets.resolve()
    if presets_path.is_file():
        existing = json.loads(presets_path.read_text(encoding="utf-8"))
    else:
        existing = {}

    out = {"voices": voices}
    for key in EXAMPLE_KEYS:
        if key in existing:
            out[key] = existing[key]

    presets_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {presets_path} — {len(voices)} voices ({args.engine})")


if __name__ == "__main__":
    main()
