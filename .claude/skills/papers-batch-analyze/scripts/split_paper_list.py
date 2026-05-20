#!/usr/bin/env python3
"""Split paper_list.csv into per-batch CSV files.

This script only prepares deterministic batch inputs and a manifest. It does
not run paper analysis or call any LLM.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_SOURCE = Path("obsidian-vault/paper_list.csv")
DEFAULT_BATCH_SIZE = 25
DEFAULT_BATCH_ROOT = Path("obsidian-vault/batches")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        default=str(DEFAULT_SOURCE),
        help="Input CSV path. Defaults to obsidian-vault/paper_list.csv.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Rows per batch. Defaults to 25.",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Optional output run directory. Defaults to obsidian-vault/batches/<run_id>.",
    )
    return parser.parse_args()


def make_run_dir(out_dir: str | None) -> tuple[str, Path]:
    if out_dir:
        run_dir = Path(out_dir)
        return run_dir.name, run_dir
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return run_id, DEFAULT_BATCH_ROOT / run_id


def read_rows(source: Path) -> tuple[list[str], list[dict[str, str]]]:
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit(f"Input CSV has no header: {source}")
        return list(reader.fieldnames), list(reader)


def write_batch(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    source = Path(args.source)
    if args.batch_size <= 0:
        raise SystemExit("--batch-size must be positive")
    if not source.is_file():
        raise SystemExit(f"Input CSV not found: {source}")

    fieldnames, rows = read_rows(source)
    run_id, run_dir = make_run_dir(args.out_dir)
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "results").mkdir()

    batch_paths: list[str] = []
    for batch_number, start in enumerate(range(0, len(rows), args.batch_size), start=1):
        batch_rows = rows[start : start + args.batch_size]
        batch_path = run_dir / f"batch_{batch_number:04d}.csv"
        write_batch(batch_path, fieldnames, batch_rows)
        batch_paths.append(str(batch_path))

    manifest = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(source),
        "batch_size": args.batch_size,
        "total_rows": len(rows),
        "batch_count": len(batch_paths),
        "batches": batch_paths,
    }
    manifest_path = run_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"[OK] run_dir: {run_dir}")
    print(f"[OK] manifest: {manifest_path}")
    print(f"[OK] total_rows: {len(rows)}")
    print(f"[OK] batch_count: {len(batch_paths)}")


if __name__ == "__main__":
    main()
