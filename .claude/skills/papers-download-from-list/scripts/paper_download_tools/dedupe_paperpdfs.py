#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[4]
DEFAULT_ROOT = REPO_ROOT / "obsidian-vault/paperPDFs"


def compute_hash(path: Path, block_size: int = 1 << 20) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        while True:
            chunk = f.read(block_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def is_preferred_path(path: Path) -> bool:
    name = path.name
    if not name.lower().endswith(".pdf"):
        return False
    if len(name) < 9 or not name[:4].isdigit() or name[4] != "_":
        return False
    parent = path.parent.name
    return bool(parent and "_" in parent and any(part.isdigit() and len(part) == 4 for part in parent.split("_")))


def choose_canonical(paths: list[Path]) -> Path:
    preferred = [p for p in paths if is_preferred_path(p)]
    candidates = preferred or paths
    return sorted(candidates, key=lambda p: (len(p.parts), str(p)))[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Remove duplicate PDF files under obsidian-vault/paperPDFs by content hash.")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="PDF root directory. Defaults to obsidian-vault/paperPDFs.")
    parser.add_argument("--dry-run", action="store_true", help="Report duplicates without deleting files.")
    args = parser.parse_args()

    root = Path(args.root).expanduser()
    if not root.is_absolute():
        root = REPO_ROOT / root

    print(f"Scanning PDFs under: {root}")
    pdfs = sorted(root.rglob("*.pdf")) if root.is_dir() else []
    print(f"Total PDFs found: {len(pdfs)}")

    groups: dict[tuple[int, str], list[Path]] = {}
    for pdf in pdfs:
        try:
            key = (pdf.stat().st_size, compute_hash(pdf))
        except OSError:
            continue
        groups.setdefault(key, []).append(pdf)

    duplicates = [group for group in groups.values() if len(group) > 1]
    print(f"Duplicate groups detected: {len(duplicates)}")

    deleted = 0
    for group in duplicates:
        canonical = choose_canonical(group)
        print("\n[GROUP]")
        for pdf in group:
            mark = "*" if pdf == canonical else " "
            print(f" {mark} {pdf}")
        for pdf in group:
            if pdf == canonical:
                continue
            if args.dry_run:
                continue
            try:
                pdf.unlink()
                deleted += 1
                print(f"  [DEL] {pdf}")
            except OSError as exc:
                print(f"  [ERROR] failed to delete {pdf}: {exc}")

    print(f"Done. Deleted={deleted}, dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
