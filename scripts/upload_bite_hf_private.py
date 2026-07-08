#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

from huggingface_hub import HfApi


REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = REPO_ROOT / "obsidian-vault"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create/update a private Hugging Face dataset repo for BITE analysis, assets, and paper_list.csv."
    )
    parser.add_argument("--repo-id", required=True, help="HF repo id, e.g. org-or-user/bite-process-private")
    parser.add_argument("--vault-root", default=str(VAULT_ROOT))
    parser.add_argument("--repo-type", default="dataset", choices=["dataset"])
    parser.add_argument("--num-workers", type=int, default=8)
    parser.add_argument("--stage-dir", default=str(REPO_ROOT / "_private" / "hf_stage" / "bite-process-private"))
    parser.add_argument("--all-assets", action="store_true", help="Upload every file under assets/ instead of only note-referenced assets.")
    parser.add_argument("--with-shards", action="store_true", help="Also build PaperBite-compatible tar shards and manifests for fast sync.")
    parser.add_argument("--asset-shard-size-mb", type=int, default=256, help="Approximate unpacked asset bytes per shard when --with-shards is used.")
    parser.add_argument("--reset-repo", action="store_true", help="Delete and recreate the target dataset repo before upload.")
    parser.add_argument("--public", action="store_true", help="Create a public repo instead of the default private repo.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def readme(repo_id: str, private: bool) -> str:
    visibility = "private" if private else "public"
    return f"""---
pretty_name: BITE Process Evidence Vault
viewer: false
---

# BITE Process Evidence Vault

This {visibility} dataset repository stores the shareable BITE evidence layer:

- `analysis/`: Obsidian Markdown paper analysis notes
- `assets/`: figure/table assets referenced by analysis notes
- `paper_list.csv`: canonical paper queue and metadata
- `manifests/` and `media/*_shards/`: optional tar shards for fast first sync

Generated from `{REPO_ROOT}` on {datetime.now().isoformat(timespec="minutes")}.

Suggested local sync:

```bash
python3 scripts/sync_assets_from_hf.py \\
  --repo-id {repo_id} \\
  --repo-type dataset \\
  --local-dir obsidian-vault \\
  --mode all \\
  --sync-paper-list \\
  --overwrite-paper-list
```
"""


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def note_referenced_assets(vault_root: Path) -> set[str]:
    refs: set[str] = set()
    for note in sorted((vault_root / "analysis").glob("*/*.md")):
        text = note.read_text(encoding="utf-8", errors="ignore")
        refs.update(re.findall(r"!\[\[(assets/figures/papers/[^\]]+)\]\]", text))
    return refs


def hardlink_or_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        try:
            if dst.stat().st_size == src.stat().st_size and int(dst.stat().st_mtime) == int(src.stat().st_mtime):
                return
        except OSError:
            pass
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def prepare_stage(vault_root: Path, stage_root: Path, *, all_assets: bool) -> dict[str, int]:
    stage_root.mkdir(parents=True, exist_ok=True)
    for name in ("analysis", "assets", "manifests", "media"):
        target = stage_root / name
        if target.exists():
            shutil.rmtree(target)
    paper_target = stage_root / "paper_list.csv"
    if paper_target.exists():
        paper_target.unlink()

    analysis_files = 0
    for src in sorted((vault_root / "analysis").glob("*/*.md")):
        rel = src.relative_to(vault_root)
        hardlink_or_copy(src, stage_root / rel)
        analysis_files += 1

    asset_files = 0
    if all_assets:
        asset_sources = [
            src
            for src in sorted((vault_root / "assets").rglob("*"))
            if src.is_file() and ".cache" not in src.relative_to(vault_root / "assets").parts
        ]
    else:
        asset_sources = []
        missing: list[str] = []
        for rel_text in sorted(note_referenced_assets(vault_root)):
            src = vault_root / rel_text
            if src.exists():
                asset_sources.append(src)
            else:
                missing.append(rel_text)
        if missing:
            raise FileNotFoundError(f"missing referenced assets: {missing[:10]}")

    for src in asset_sources:
        rel = src.relative_to(vault_root)
        hardlink_or_copy(src, stage_root / rel)
        asset_files += 1

    hardlink_or_copy(vault_root / "paper_list.csv", stage_root / "paper_list.csv")
    return {
        "analysis_files": analysis_files,
        "asset_files": asset_files,
        "paper_list_files": 1,
        "total_files": analysis_files + asset_files + 1,
    }


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def make_tar(tar_path: Path, root: Path, members: list[Path]) -> dict[str, object]:
    tar_path.parent.mkdir(parents=True, exist_ok=True)
    if tar_path.exists():
        tar_path.unlink()
    unpacked_size = 0
    prefixes: list[str] = []
    with tarfile.open(tar_path, "w") as tar:
        for src in members:
            rel = src.relative_to(root).as_posix()
            tar.add(src, arcname=rel, recursive=False)
            unpacked_size += src.stat().st_size
            prefix = "/".join(rel.split("/")[:3]) if rel.startswith("assets/figures/papers/") else rel.split("/", 1)[0]
            if prefix not in prefixes:
                prefixes.append(prefix)
    return {
        "path": tar_path.relative_to(root).as_posix(),
        "size": tar_path.stat().st_size,
        "sha256": sha256_file(tar_path),
        "file_count": len(members),
        "unpacked_size": unpacked_size,
        "members_prefixes": prefixes[:128],
    }


def chunk_by_size(paths: list[Path], max_unpacked_size: int) -> list[list[Path]]:
    chunks: list[list[Path]] = []
    current: list[Path] = []
    current_size = 0
    for path in paths:
        size = path.stat().st_size
        if current and current_size + size > max_unpacked_size:
            chunks.append(current)
            current = []
            current_size = 0
        current.append(path)
        current_size += size
    if current:
        chunks.append(current)
    return chunks


def build_shards(stage_root: Path, *, asset_shard_size_mb: int) -> dict[str, int]:
    manifests_root = stage_root / "manifests"
    text_members = [p for p in (stage_root / "analysis").glob("*/*.md") if p.is_file()]
    if (stage_root / "index").exists():
        text_members.extend(p for p in (stage_root / "index").rglob("*") if p.is_file())
    text_members = sorted(text_members)
    text_rows: list[dict[str, object]] = []
    if text_members:
        text_rows.append(make_tar(stage_root / "media" / "text_shards" / "bite_text.tar", stage_root, text_members))
    write_jsonl(manifests_root / "paperbite_text_shards_manifest.jsonl", text_rows)

    asset_members = sorted(p for p in (stage_root / "assets").rglob("*") if p.is_file())
    max_unpacked_size = max(1, asset_shard_size_mb) * 1024 * 1024
    asset_rows: list[dict[str, object]] = []
    asset_shard_rows: list[dict[str, object]] = []
    for index, members in enumerate(chunk_by_size(asset_members, max_unpacked_size)):
        shard_rel = f"media/assets_shards/assets_papers_{index:04d}.tar"
        shard_row = make_tar(stage_root / shard_rel, stage_root, members)
        asset_shard_rows.append(shard_row)
        for member in members:
            asset_rows.append({
                "path": member.relative_to(stage_root).as_posix(),
                "size": member.stat().st_size,
                "sha256": sha256_file(member),
                "shard": shard_rel,
            })
    write_jsonl(manifests_root / "paperbite_assets_manifest.jsonl", asset_rows)
    write_jsonl(manifests_root / "paperbite_asset_shards_manifest.jsonl", asset_shard_rows)
    return {
        "text_shards": len(text_rows),
        "asset_shards": len(asset_shard_rows),
        "asset_manifest_rows": len(asset_rows),
        "shard_files": len(text_rows) + len(asset_shard_rows) + 3,
    }


def main() -> int:
    args = parse_args()
    vault_root = Path(args.vault_root).expanduser().resolve()
    for required in ("analysis", "assets", "paper_list.csv"):
        if not (vault_root / required).exists():
            raise FileNotFoundError(f"missing required upload target: {vault_root / required}")

    private = not args.public
    print(f"repo_id: {args.repo_id}")
    print(f"repo_type: {args.repo_type}")
    print(f"private: {private}")
    print(f"vault_root: {vault_root}")
    print(f"asset_mode: {'all assets' if args.all_assets else 'note-referenced assets only'}")
    print("include: analysis/**, staged assets/**, paper_list.csv")
    stage_root = Path(args.stage_dir).expanduser().resolve()
    stage_counts = prepare_stage(vault_root, stage_root, all_assets=args.all_assets)
    print(f"stage_root: {stage_root}")
    print(f"stage_counts: {stage_counts}")
    shard_counts: dict[str, int] = {}
    if args.with_shards:
        shard_counts = build_shards(stage_root, asset_shard_size_mb=args.asset_shard_size_mb)
        print(f"shard_counts: {shard_counts}")
    if args.dry_run:
        print("[DRY-RUN] no HF API calls made")
        return 0

    os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")
    api = HfApi()
    who = api.whoami()
    print(f"authenticated_as: {who.get('name') or who}")
    if args.reset_repo:
        api.delete_repo(repo_id=args.repo_id, repo_type=args.repo_type, missing_ok=True)
    api.create_repo(repo_id=args.repo_id, repo_type=args.repo_type, private=private, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
        f.write(readme(args.repo_id, private))
        readme_path = Path(f.name)
    try:
        api.upload_file(
            repo_id=args.repo_id,
            repo_type=args.repo_type,
            path_or_fileobj=str(readme_path),
            path_in_repo="README.md",
            commit_message="Update BITE dataset README",
        )
    finally:
        readme_path.unlink(missing_ok=True)

    api.upload_large_folder(
        repo_id=args.repo_id,
        repo_type=args.repo_type,
        folder_path=stage_root,
        private=private,
        allow_patterns=["analysis/**", "assets/**", "paper_list.csv", "manifests/**", "media/**"],
        ignore_patterns=[".cache/**", "**/.cache/**"],
        num_workers=args.num_workers,
        print_report=True,
        print_report_every=60,
    )
    print("[OK] upload complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
