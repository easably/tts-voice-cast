#!/usr/bin/env python3
"""Build neutral audiobook narrator clips from LibriTTS-R (+ LJSpeech alias)."""

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
CONFIG = ROOT / "narrators.json"
MAX_SEC = 12.0


def _resample_24k_mono(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg required to resample narrator clips")
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-i",
            str(src),
            "-ac",
            "1",
            "-ar",
            "24000",
            "-t",
            str(MAX_SEC),
            str(dst),
        ],
        check=True,
        capture_output=True,
    )


def _duration_sec(path: Path) -> float:
    import soundfile as sf

    info = sf.info(str(path))
    return info.frames / info.samplerate


def _collect_libritts_clips(speaker_id: str, cfg: dict) -> list[tuple[float, bytes, str]]:
    return collect_clips(speaker_id, cfg)


def build() -> None:
    try:
        import soundfile  # noqa: F401
    except ImportError as exc:
        raise SystemExit("Install: pip install soundfile pyarrow huggingface_hub") from exc

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    DEST.mkdir(parents=True, exist_ok=True)

    for narrator in cfg["narrators"]:
        char_id = narrator["id"]
        if narrator.get("source") == "ljspeech":
            src = DEST / narrator["presets"][0].get("file", "ljspeech.wav")
            for preset in narrator["presets"]:
                out = DEST / f"{preset['id']}.wav"
                if out.is_file() and _duration_sec(out) >= 3:
                    print(f"skip {out.name} (exists)")
                    continue
                if not src.is_file():
                    print(f"warn: {src.name} missing — run download-mia.sh first", file=sys.stderr)
                    continue
                _resample_24k_mono(src, out)
                print(f"wrote {out.name} from {src.name} ({_duration_sec(out):.1f}s)")
            continue

        speaker = str(narrator["libritts_speaker_id"])
        print(f"collecting LibriTTS-R speaker {speaker} ({narrator.get('reader_name', '')}) ...")
        clips = _collect_libritts_clips(speaker, cfg)
        if len(clips) < len(narrator["presets"]):
            raise SystemExit(
                f"Not enough clips for {char_id} (speaker {speaker}): "
                f"need {len(narrator['presets'])}, found {len(clips)}"
            )

        for preset in narrator["presets"]:
            out = DEST / f"{preset['id']}.wav"
            if out.is_file() and _duration_sec(out) >= 3:
                print(f"skip {out.name} (exists)")
                continue
            pick = int(preset.get("pick", 0))
            dur, data, text = clips[pick]
            tmp = DEST / f".tmp_{preset['id']}.wav"
            import soundfile as sf

            arr, sr = sf.read(io.BytesIO(data), dtype="float32")
            sf.write(str(tmp), arr, sr)
            try:
                _resample_24k_mono(tmp, out)
                print(f"wrote {out.name} ({_duration_sec(out):.1f}s) — {text[:55]}...")
            finally:
                tmp.unlink(missing_ok=True)

    print("Narrator samples ready.")


if __name__ == "__main__":
    build()
