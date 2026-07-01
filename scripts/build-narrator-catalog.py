#!/usr/bin/env python3
"""Build one neutral clip per LibriTTS-R catalog speaker."""

from __future__ import annotations

import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from libritts_clips import collect_clips

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "samples/en"
CONFIG = ROOT / "catalog-speakers.json"
MAX_SEC = 12.0


def _resample_24k_mono(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg required")
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-ac", "1", "-ar", "24000", "-t", str(MAX_SEC), str(dst)],
        check=True,
        capture_output=True,
    )


def _duration_sec(path: Path) -> float:
    import soundfile as sf

    info = sf.info(str(path))
    return info.frames / info.samplerate


def build() -> None:
    try:
        import soundfile as sf  # noqa: F401
    except ImportError as exc:
        raise SystemExit("Install: pip install soundfile pyarrow huggingface_hub") from exc

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    DEST.mkdir(parents=True, exist_ok=True)
    missing: list[str] = []

    for speaker in cfg["speakers"]:
        sp = str(speaker["speaker_id"])
        out = DEST / f"libri_{sp}_neutral.wav"
        if out.is_file() and _duration_sec(out) >= 3:
            print(f"skip {out.name} (exists)")
            continue
        print(f"catalog speaker {sp} ({speaker.get('reader_name', '')}) ...")
        clips = collect_clips(sp, cfg)
        if not clips:
            missing.append(sp)
            continue
        dur, data, text = clips[0]
        tmp = DEST / f".tmp_libri_{sp}.wav"
        import soundfile as sf

        arr, sr = sf.read(io.BytesIO(data), dtype="float32")
        sf.write(str(tmp), arr, sr)
        try:
            _resample_24k_mono(tmp, out)
            print(f"wrote {out.name} ({_duration_sec(out):.1f}s) — {text[:50]}...")
        finally:
            tmp.unlink(missing_ok=True)

    if missing:
        raise SystemExit(f"Missing catalog clips for speakers: {', '.join(missing)}")
    print(f"Catalog samples ready ({len(cfg['speakers'])} speakers).")


if __name__ == "__main__":
    build()
