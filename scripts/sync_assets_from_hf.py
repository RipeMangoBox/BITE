#!/usr/bin/env python3
"""Incrementally download optional PaperBite assets from a Hugging Face dataset."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tarfile
from pathlib import Path

from huggingface_hub import hf_hub_download


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", default="RipeMangoBox/PaperBite-Assets")
    parser.add_argument("--repo-type", default="dataset")
    parser.add_argument("--manifest", default="manifests/paperbite_assets_manifest.jsonl")
    parser.add_argument("--shard-manifest", default="manifests/paperbite_asset_shards_manifest.jsonl")
    parser.add_argument("--revision", default=None)
    parser.add_argument("--local-dir", default=".")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    local_root = Path(args.local_dir)
    manifest_path = local_root / args.manifest
    shard_manifest_path = local_root / args.shard_manifest
    for rel_path, target_path in (
        (args.manifest, manifest_path),
        (args.shard_manifest, shard_manifest_path),
    ):
        if target_path.exists():
            continue
        downloaded_manifest = hf_hub_download(
            repo_id=args.repo_id,
            repo_type=args.repo_type,
            filename=rel_path,
            revision=args.revision,
        )
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(Path(downloaded_manifest).read_bytes())

    shard_rows = {row["path"]: row for row in load_manifest(shard_manifest_path)}
    needed = []
    for row in load_manifest(manifest_path):
        target = local_root / row["path"]
        if not target.exists() or target.stat().st_size != row["size"]:
            needed.append(row)
            continue
        if sha256_file(target) != row["sha256"]:
            needed.append(row)

    needed_shards = sorted({row["shard"] for row in needed})
    print(f"needed assets: {len(needed)}")
    print(f"needed shards: {len(needed_shards)}")
    if args.dry_run:
        for shard in needed_shards[:50]:
            print(shard)
        return 0

    for shard in needed_shards:
        shard_info = shard_rows.get(shard)
        if shard_info is None:
            raise RuntimeError(f"missing shard manifest row: {shard}")
        downloaded_shard = hf_hub_download(
            repo_id=args.repo_id,
            repo_type=args.repo_type,
            filename=shard,
            revision=args.revision,
        )
        shard_path = Path(downloaded_shard)
        if shard_path.stat().st_size != shard_info["size"] or sha256_file(shard_path) != shard_info["sha256"]:
            raise RuntimeError(f"shard checksum mismatch: {shard}")
        with tarfile.open(shard_path, "r") as tar:
            tar.extractall(local_root)
        print(shard)

    bad = []
    for row in needed:
        target = local_root / row["path"]
        if not target.exists() or target.stat().st_size != row["size"] or sha256_file(target) != row["sha256"]:
            bad.append(row["path"])
    if bad:
        raise RuntimeError(f"asset checksum mismatch after extraction: {bad[:10]}")

    return 0


if __name__ == "__main__":
    os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")
    raise SystemExit(main())
