#!/usr/bin/env python3
"""Incrementally download BITE evidence layers from a Hugging Face dataset.

Modes:
  text   — analysis notes + indexes only (~43 MB)
  assets — figures and tables only (~1.8 GB)
  all    — everything (default)
"""

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


def _ensure_manifest(local_root: Path, rel_path: str, repo_id: str, repo_type: str, revision: str | None) -> Path:
    """Download a manifest from HF if it doesn't exist locally."""
    target = local_root / rel_path
    if target.exists():
        return target
    downloaded = hf_hub_download(
        repo_id=repo_id,
        repo_type=repo_type,
        filename=rel_path,
        revision=revision,
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(Path(downloaded).read_bytes())
    return target


def _download_and_extract_shard(
    shard_path: str,
    shard_info: dict,
    repo_id: str,
    repo_type: str,
    revision: str | None,
    local_root: Path,
) -> None:
    """Download a single shard, verify checksum, and extract."""
    downloaded = hf_hub_download(
        repo_id=repo_id,
        repo_type=repo_type,
        filename=shard_path,
        revision=revision,
    )
    shard = Path(downloaded)
    if shard.stat().st_size != shard_info["size"] or sha256_file(shard) != shard_info["sha256"]:
        raise RuntimeError(f"shard checksum mismatch: {shard_path}")
    with tarfile.open(shard, "r") as tar:
        tar.extractall(local_root)
    print(shard_path)


def sync_text_layer(
    repo_id: str,
    repo_type: str,
    local_root: Path,
    revision: str | None,
    dry_run: bool,
) -> None:
    """Download and extract the text layer (analysis/ + index/)."""
    text_manifest_rel = "manifests/paperbite_text_shards_manifest.jsonl"
    manifest_path = _ensure_manifest(local_root, text_manifest_rel, repo_id, repo_type, revision)

    shard_rows = {row["path"]: row for row in load_manifest(manifest_path)}
    if not shard_rows:
        print("no text shards found in manifest")
        return

    needed = []
    for row in shard_rows.values():
        shard_path = local_root / "media/text_shards" / Path(row["path"]).name
        if not shard_path.exists() or shard_path.stat().st_size != row["size"]:
            needed.append(row)
        elif sha256_file(shard_path) != row["sha256"]:
            needed.append(row)

    print(f"text shards needed: {len(needed)}")
    if dry_run:
        for row in needed:
            print(f"  {row['path']}  ({row['size'] / 1024 / 1024:.0f} MB)")
        return

    for row in needed:
        _download_and_extract_shard(row["path"], row, repo_id, repo_type, revision, local_root)

    # Quick sanity: check a known marker exists
    if not (local_root / "analysis" / "README.md").exists():
        print("warning: analysis/README.md not found after extraction — text layer may be incomplete")


def sync_asset_layer(
    repo_id: str,
    repo_type: str,
    local_root: Path,
    revision: str | None,
    dry_run: bool,
) -> None:
    """Download and extract the asset layer (figures, tables)."""
    manifest_rel = "manifests/paperbite_assets_manifest.jsonl"
    shard_manifest_rel = "manifests/paperbite_asset_shards_manifest.jsonl"

    manifest_path = _ensure_manifest(local_root, manifest_rel, repo_id, repo_type, revision)
    shard_manifest_path = _ensure_manifest(local_root, shard_manifest_rel, repo_id, repo_type, revision)

    shard_rows = {row["path"]: row for row in load_manifest(shard_manifest_path)}

    needed = []
    for row in load_manifest(manifest_path):
        target = local_root / row["path"]
        if not target.exists() or target.stat().st_size != row["size"]:
            needed.append(row)
        elif sha256_file(target) != row["sha256"]:
            needed.append(row)

    needed_shards = sorted({row["shard"] for row in needed})
    print(f"asset files needed: {len(needed)}")
    print(f"asset shards needed: {len(needed_shards)}")
    if dry_run:
        for shard in needed_shards[:50]:
            print(f"  {shard}")
        return

    for shard_rel in needed_shards:
        shard_info = shard_rows.get(shard_rel)
        if shard_info is None:
            raise RuntimeError(f"missing shard manifest row: {shard_rel}")
        _download_and_extract_shard(shard_rel, shard_info, repo_id, repo_type, revision, local_root)

    # Verify extracted files
    bad = []
    for row in needed:
        target = local_root / row["path"]
        if not target.exists() or target.stat().st_size != row["size"] or sha256_file(target) != row["sha256"]:
            bad.append(row["path"])
    if bad:
        raise RuntimeError(f"asset checksum mismatch after extraction: {bad[:10]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-id", default="RipeMangoBox/PaperBite-Assets")
    parser.add_argument("--repo-type", default="dataset")
    parser.add_argument("--revision", default=None)
    parser.add_argument("--local-dir", default="obsidian-vault")
    parser.add_argument("--mode", default="all", choices=["text", "assets", "all"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    local_root = Path(args.local_dir)
    mode = args.mode

    if mode in ("text", "all"):
        sync_text_layer(args.repo_id, args.repo_type, local_root, args.revision, args.dry_run)

    if mode in ("assets", "all"):
        sync_asset_layer(args.repo_id, args.repo_type, local_root, args.revision, args.dry_run)

    return 0


if __name__ == "__main__":
    os.environ.setdefault("HF_ENDPOINT", "https://huggingface.co")
    os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")
    raise SystemExit(main())
