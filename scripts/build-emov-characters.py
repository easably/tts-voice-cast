#!/usr/bin/env python3
"""Build expressive reference clips from EmoV-DB (CC BY 4.0) for configured characters."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "samples/en"
CONFIG = ROOT / "emov-characters.json"
REPO = "erminga/emo-tts"
MIN_SEC = 3.5
MAX_SEC = 12.0


def _duration_sec(wav_path: Path) -> float:
    import soundfile as sf

    return sf.info(str(wav_path)).frames / sf.info(str(wav_path)).samplerate


def _resample_24k_mono(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(src), "-ac", "1", "-ar", "24000", "-t", str(MAX_SEC), str(dst)],
            check=True,
            capture_output=True,
        )
        return

    import numpy as np
    import soundfile as sf

    audio, sr = sf.read(str(src), dtype="float32", always_2d=True)
    mono = audio.mean(axis=1)
    if sr != 24000:
        import torch
        import torchaudio

        t = torch.from_numpy(mono).unsqueeze(0)
        mono = torchaudio.functional.resample(t, sr, 24000).squeeze(0).numpy()
    mono = mono[: int(MAX_SEC * 24000)]
    sf.write(str(dst), mono, 24000)


def _pick_wav_from_tar(tar_path: Path) -> Path:
    with tarfile.open(tar_path, "r:gz") as archive:
        members = [m for m in archive.getmembers() if m.isfile() and m.name.lower().endswith(".wav")]
        if not members:
            raise RuntimeError(f"No WAV in {tar_path.name}")
        members.sort(key=lambda m: m.size or 0, reverse=True)
        for member in members:
            extracted = archive.extractfile(member)
            if extracted is None:
                continue
            tmp = Path(tempfile.mkstemp(suffix=".wav")[1])
            tmp.write_bytes(extracted.read())
            try:
                if _duration_sec(tmp) >= MIN_SEC:
                    return tmp
            except Exception:
                pass
            tmp.unlink(missing_ok=True)
        member = members[0]
        extracted = archive.extractfile(member)
        tmp = Path(tempfile.mkstemp(suffix=".wav")[1])
        tmp.write_bytes(extracted.read())
        return tmp


def build_character(char: dict) -> None:
    from huggingface_hub import hf_hub_download

    speaker = char["speaker"]
    char_id = char["id"]
    print(f"=== EmoV-DB {char_id} (speaker {speaker}) ===")

    for emotion, meta in char["emotions"].items():
        filename = f"{meta['id']}.wav"
        out = DEST / filename
        if out.is_file() and _duration_sec(out) >= MIN_SEC:
            print(f"skip {filename} (exists)")
            continue
        tar_name = f"EmoV-DB/{speaker}_{emotion}.tar.gz"
        print(f"download {tar_name} ...")
        tar_path = Path(hf_hub_download(repo_id=REPO, filename=tar_name, repo_type="dataset"))
        clip = _pick_wav_from_tar(tar_path)
        try:
            _resample_24k_mono(clip, out)
            print(f"wrote {out.name} ({_duration_sec(out):.1f}s)")
        finally:
            if clip.parent == Path(tempfile.gettempdir()) or "/tmp" in str(clip):
                clip.unlink(missing_ok=True)


def main() -> None:
    try:
        import soundfile  # noqa: F401
    except ImportError as exc:
        raise SystemExit("Install: pip install soundfile huggingface_hub") from exc

    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    DEST.mkdir(parents=True, exist_ok=True)
    for char in data["characters"]:
        build_character(char)
    print("EmoV-DB expressive characters ready.")


if __name__ == "__main__":
    main()
