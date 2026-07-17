#!/usr/bin/env python3
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any, Iterable

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from storymotion.training.human200 import (  # noqa: E402
    HUMAN199_DIM,
    HUMAN200_DIM,
    HUMAN200_FEATURE_CONTRACT,
    HUMAN200_LAYOUT,
    human199_raw_to_human200_raw,
    load_human200_stats,
    sha256_file,
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ids_sha256(sample_ids: list[str]) -> str:
    return hashlib.sha256(("\n".join(sample_ids) + "\n").encode()).hexdigest()


def resolve_feature_path(row: dict[str, Any], root: Path) -> Path:
    value = row.get("motion_feature_path")
    if not value:
        raise KeyError(f"missing motion_feature_path for {row.get('sample_id')}")
    path = Path(str(value))
    return path if path.is_absolute() else root / path


def load_human199(path: str) -> torch.Tensor:
    value: Any
    source = Path(path)
    if source.suffix == ".npy":
        value = np.load(source)
    elif source.suffix == ".pt":
        value = torch.load(source, map_location="cpu", weights_only=False)
    else:
        raise ValueError(f"unsupported human feature file: {source}")
    if isinstance(value, dict):
        value = value.get("motion", value.get("features"))
    tensor = torch.as_tensor(value, dtype=torch.float64)
    if tensor.ndim != 2 or tensor.shape[-1] != HUMAN199_DIM or tensor.shape[0] <= 0:
        raise ValueError(f"expected [T,{HUMAN199_DIM}] at {source}, got {tuple(tensor.shape)}")
    if not torch.isfinite(tensor).all():
        raise ValueError(f"non-finite human199 feature: {source}")
    return tensor


def merge_moments(
    left_count: int,
    left_mean: torch.Tensor,
    left_m2: torch.Tensor,
    right_count: int,
    right_mean: torch.Tensor,
    right_m2: torch.Tensor,
) -> tuple[int, torch.Tensor, torch.Tensor]:
    if right_count <= 0:
        return left_count, left_mean, left_m2
    if left_count <= 0:
        return right_count, right_mean, right_m2
    total = left_count + right_count
    delta = right_mean - left_mean
    mean = left_mean + delta * (right_count / total)
    m2 = left_m2 + right_m2 + delta.square() * (left_count * right_count / total)
    return total, mean, m2


def chunk_moments(task: tuple[int, list[str]]) -> tuple[int, int, torch.Tensor, torch.Tensor, int]:
    chunk_index, paths = task
    count = 0
    mean = torch.zeros(HUMAN200_DIM, dtype=torch.float64)
    m2 = torch.zeros(HUMAN200_DIM, dtype=torch.float64)
    for path in paths:
        human200 = human199_raw_to_human200_raw(load_human199(path))
        frame_count = int(human200.shape[0])
        frame_mean = human200.mean(dim=0)
        frame_m2 = (human200 - frame_mean).square().sum(dim=0)
        count, mean, m2 = merge_moments(count, mean, m2, frame_count, frame_mean, frame_m2)
    return chunk_index, count, mean, m2, len(paths)


def chunks(values: list[str], size: int) -> Iterable[tuple[int, list[str]]]:
    for start in range(0, len(values), size):
        yield start // size, values[start : start + size]


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False) as handle:
        temp_path = Path(handle.name)
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    try:
        if path.exists():
            raise FileExistsError(f"refusing to overwrite immutable human200 statistics: {path}")
        temp_path.replace(path)
    finally:
        temp_path.unlink(missing_ok=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build frame-weighted train-only StoryMotion v8.2 human200 statistics.")
    parser.add_argument("--train-human-manifest", type=Path, required=True)
    parser.add_argument("--human-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-samples", type=int, default=162760)
    parser.add_argument("--num-workers", type=int, default=8)
    parser.add_argument("--chunk-size", type=int, default=256)
    parser.add_argument("--min-std", type=float, default=1.0e-6)
    parser.add_argument("--progress-every-chunks", type=int, default=50)
    parser.add_argument(
        "--reuse-existing",
        action="store_true",
        help="Validate and reuse an immutable existing artifact instead of overwriting it.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.num_workers < 0 or args.chunk_size <= 0 or args.min_std <= 0:
        raise ValueError("num-workers must be non-negative; chunk-size/min-std must be positive")
    # These are small per-sequence reductions. Let the process pool provide
    # parallelism instead of multiplying a BLAS thread pool inside each worker.
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    if args.output.exists():
        if not args.reuse_existing:
            raise FileExistsError(f"refusing to overwrite immutable human200 statistics: {args.output}")
        existing = load_human200_stats(
            args.output,
            expected_train_manifest=args.train_human_manifest,
        )
        source = existing["meta"]["source"]
        if args.expected_samples and int(source["samples"]) != args.expected_samples:
            raise ValueError(
                f"existing statistics cover {source['samples']} samples, expected {args.expected_samples}"
            )
        print(
            json.dumps(
                {
                    "output": str(args.output),
                    "sha256": existing["sha256"],
                    "samples": source["samples"],
                    "frames": source["frames"],
                    "reused": True,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        return
    rows = read_jsonl(args.train_human_manifest)
    if args.expected_samples and len(rows) != args.expected_samples:
        raise ValueError(f"train manifest has {len(rows)} rows, expected {args.expected_samples}")
    sample_ids = [str(row.get("sample_id") or "") for row in rows]
    if not all(sample_ids) or len(sample_ids) != len(set(sample_ids)):
        raise ValueError("train manifest sample IDs must be non-empty and unique")
    wrong_space = [sample_id for sample_id, row in zip(sample_ids, rows) if row.get("feature_space") != "pulpmotion_smpl_rifke"]
    if wrong_space:
        raise ValueError(f"train manifest contains non-RIFKE records: {wrong_space[:5]}")
    feature_root = args.human_root or args.train_human_manifest.parent
    paths = [str(resolve_feature_path(row, feature_root)) for row in rows]
    tasks = list(chunks(paths, args.chunk_size))
    iterator: Iterable[tuple[int, int, torch.Tensor, torch.Tensor, int]]
    if args.num_workers:
        executor = ProcessPoolExecutor(max_workers=args.num_workers)
        iterator = executor.map(chunk_moments, tasks)
    else:
        executor = None
        iterator = map(chunk_moments, tasks)
    count = 0
    mean = torch.zeros(HUMAN200_DIM, dtype=torch.float64)
    m2 = torch.zeros(HUMAN200_DIM, dtype=torch.float64)
    samples = 0
    try:
        for expected_index, result in enumerate(iterator):
            chunk_index, chunk_count, chunk_mean, chunk_m2, chunk_samples = result
            if chunk_index != expected_index:
                raise RuntimeError("parallel statistics chunks were merged out of ordered-row order")
            count, mean, m2 = merge_moments(count, mean, m2, chunk_count, chunk_mean, chunk_m2)
            samples += chunk_samples
            if args.progress_every_chunks > 0 and (expected_index + 1) % args.progress_every_chunks == 0:
                print(json.dumps({"chunks": expected_index + 1, "samples": samples, "frames": count}), flush=True)
    finally:
        if executor is not None:
            executor.shutdown(wait=True, cancel_futures=True)
    if samples != len(rows) or count <= 0:
        raise RuntimeError(f"statistics coverage mismatch: samples={samples}/{len(rows)}, frames={count}")
    variance = (m2 / count).clamp_min(0.0)
    raw_std = torch.sqrt(variance)
    std = raw_std.clamp_min(args.min_std)
    payload = {
        "schema_version": 1,
        "feature_contract": HUMAN200_FEATURE_CONTRACT,
        "layout": HUMAN200_LAYOUT,
        "human_dim": HUMAN200_DIM,
        "normalization": "frame_weighted_population_mean_std",
        "min_std": args.min_std,
        "clamped_std_channels": int((raw_std < args.min_std).sum().item()),
        "source": {
            "split": "train",
            "manifest": str(args.train_human_manifest.resolve()),
            "manifest_sha256": sha256_file(args.train_human_manifest),
            "samples": samples,
            "sample_ids_sha256": ids_sha256(sample_ids),
            "frames": count,
            "ordered_rows": True,
        },
        "builder": {
            "script": str(Path(__file__).resolve()),
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "argv": sys.argv,
            "num_workers": args.num_workers,
            "chunk_size": args.chunk_size,
            "merge": "ordered_contiguous_chunks_chan_welford",
        },
        "mean": mean.tolist(),
        "std": std.tolist(),
    }
    atomic_write_json(args.output, payload)
    print(json.dumps({"output": str(args.output), "sha256": sha256_file(args.output), "samples": samples, "frames": count}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
