"""Shared LibriTTS-R clip helpers for narrator build scripts."""

from __future__ import annotations

import io
from pathlib import Path


def collect_clips(speaker_id: str, cfg: dict) -> list[tuple[float, bytes, str]]:
    from huggingface_hub import hf_hub_download
    import pyarrow.parquet as pq
    import soundfile as sf

    lo = cfg["clip_sec"]["min"]
    hi = cfg["clip_sec"]["max"]
    target = cfg["clip_sec"]["target"]
    clips: list[tuple[float, bytes, str]] = []

    for shard in cfg["subset_shards"]:
        path = hf_hub_download(cfg["dataset"], shard, repo_type="dataset")
        table = pq.read_table(path, columns=["speaker_id", "text_normalized", "audio"])
        for batch in table.to_batches(max_chunksize=64):
            for row in batch.to_pylist():
                if str(row["speaker_id"]) != str(speaker_id):
                    continue
                data = row["audio"].get("bytes")
                if not data:
                    continue
                arr, sr = sf.read(io.BytesIO(data), dtype="float32")
                dur = len(arr) / sr
                if lo <= dur <= hi:
                    clips.append((dur, data, row["text_normalized"][:120]))

    clips.sort(key=lambda x: (abs(x[0] - target), -x[0]))
    return clips


def reader_label(reader_name: str) -> str:
    first = reader_name.strip().split()[0]
    return first.replace(".", "")
