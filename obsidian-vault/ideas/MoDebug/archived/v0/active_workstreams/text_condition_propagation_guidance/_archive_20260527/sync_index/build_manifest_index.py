#!/usr/bin/env python3
"""Build a file tree and manifest index for fetched trace artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator


FORWARD_FIELDS = [
    "run_id",
    "sample_id",
    "model",
    "model_family",
    "condition_id",
    "condition_text",
    "paired_condition_id",
    "z_kind",
    "z_id",
    "f_name",
    "f_space",
    "forward_npz_path",
    "motion_artifact_path",
    "role",
    "used_for",
    "limitations",
]

DELTA_FIELDS = [
    "run_id",
    "sample_id",
    "model",
    "condition_pair",
    "z_kind",
    "z_id",
    "f_name",
    "metric_name",
    "metric_value",
    "delta_npz_path",
    "role",
    "used_for",
    "limitations",
]

TSV_COLUMNS = [
    "manifest_kind",
    "manifest_path",
    "line_no",
    "run_dir",
    "run_id",
    "sample_id",
    "model",
    "model_family",
    "condition_id",
    "paired_condition_id",
    "condition_pair",
    "z_kind",
    "z_id",
    "f_name",
    "f_space",
    "metric_name",
    "metric_value",
    "npz_path",
    "role",
    "used_for",
    "limitations",
    "status",
]

GENERATED_NAMES = {"file_tree.md", "manifest_index.tsv"}
TRACE_MANIFEST_NAMES = {
    "forward_manifest.jsonl",
    "delta_manifest.jsonl",
    "delta_guard_manifest.jsonl",
    "skipped_forward_manifest.jsonl",
}
NON_ISSUE_STATUSES = {"ok", "skipped"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def clean_cell(value: object) -> str:
    if value is None:
        return ""
    return str(value).replace("\t", " ").replace("\n", " ").replace("\r", " ")


def iter_jsonl_files(root: Path) -> Iterator[Path]:
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = sorted(
            name
            for name in dirnames
            if not (Path(dirpath) / name).is_symlink()
        )
        for filename in sorted(filenames):
            if filename in TRACE_MANIFEST_NAMES:
                yield Path(dirpath) / filename


def classify_record(record: dict[str, object]) -> tuple[str, list[str], str]:
    if record.get("status") == "skipped" and "skip_reason" in record:
        missing = [field for field in FORWARD_FIELDS if field not in record]
        return "skipped_forward", missing, clean_cell(record.get("forward_npz_path"))
    if "forward_npz_path" in record:
        missing = [field for field in FORWARD_FIELDS if field not in record]
        return "forward", missing, clean_cell(record.get("forward_npz_path"))
    if "delta_npz_path" in record:
        missing = [field for field in DELTA_FIELDS if field not in record]
        return "delta", missing, clean_cell(record.get("delta_npz_path"))
    return "unknown", ["forward_npz_path|delta_npz_path"], ""


def nearest_run_dir(path: Path, root: Path) -> str:
    for parent in [path.parent, *path.parents]:
        if parent == root.parent:
            break
        name = parent.name
        if len(name) >= 16 and name[8] == "_" and name[15] == "_":
            return relative(parent, root)
    return ""


def manifest_rows(manifest_path: Path, root: Path) -> Iterator[dict[str, str]]:
    manifest_rel = relative(manifest_path, root)
    try:
        handle = manifest_path.open("r", encoding="utf-8")
    except OSError as exc:
        yield {
            "manifest_kind": "unreadable",
            "manifest_path": manifest_rel,
            "line_no": "0",
            "run_dir": nearest_run_dir(manifest_path, root),
            "status": f"unreadable:{exc}",
        }
        return

    with handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                yield {
                    "manifest_kind": "parse_error",
                    "manifest_path": manifest_rel,
                    "line_no": str(line_no),
                    "run_dir": nearest_run_dir(manifest_path, root),
                    "status": f"json_error:{exc.msg}",
                }
                continue
            if not isinstance(record, dict):
                yield {
                    "manifest_kind": "parse_error",
                    "manifest_path": manifest_rel,
                    "line_no": str(line_no),
                    "run_dir": nearest_run_dir(manifest_path, root),
                    "status": "json_value_not_object",
                }
                continue

            kind, missing, npz_path = classify_record(record)
            status = "ok" if not missing else "missing:" + ",".join(missing)
            row = {column: "" for column in TSV_COLUMNS}
            row.update(
                {
                    "manifest_kind": kind,
                    "manifest_path": manifest_rel,
                    "line_no": str(line_no),
                    "run_dir": nearest_run_dir(manifest_path, root),
                    "npz_path": npz_path,
                    "status": status,
                }
            )
            for column in TSV_COLUMNS:
                if column in record:
                    row[column] = clean_cell(record[column])
            yield row


def iter_tree_lines(root: Path, max_depth: int, max_entries: int) -> Iterator[str]:
    count = 0

    def walk(directory: Path, prefix: str, depth: int) -> Iterator[str]:
        nonlocal count
        if count >= max_entries:
            return
        try:
            with os.scandir(directory) as entries:
                sorted_entries = sorted(
                    entries,
                    key=lambda item: (
                        not item.is_dir(follow_symlinks=False),
                        item.name.lower(),
                    ),
                )
        except OSError as exc:
            yield f"{prefix}- [unreadable] {directory.name}: {exc}"
            return

        for entry in sorted_entries:
            if count >= max_entries:
                return
            if entry.name in GENERATED_NAMES:
                continue
            entry_path = Path(entry.path)
            is_link = entry_path.is_symlink()
            is_dir = entry.is_dir(follow_symlinks=False)
            suffix = "/" if is_dir else ""
            target = ""
            if is_link:
                try:
                    target = f" -> {os.readlink(entry_path)}"
                except OSError:
                    target = " -> [unreadable]"
            yield f"{prefix}- {entry.name}{suffix}{target}"
            count += 1
            if is_dir and not is_link and depth < max_depth:
                yield from walk(entry_path, prefix + "  ", depth + 1)

    yield from walk(root, "", 0)
    if count >= max_entries:
        yield f"- ... truncated after {max_entries} entries"


def write_file_tree(root: Path, output_path: Path, max_depth: int, max_entries: int) -> None:
    generated_at = utc_now()
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("---\n")
        handle.write('title: "Fetched Trace File Tree"\n')
        handle.write("generated_by: build_manifest_index.py\n")
        handle.write(f'generated_at: "{generated_at}"\n')
        handle.write(f'source_root: "{root.as_posix()}"\n')
        handle.write("---\n\n")
        handle.write("# Fetched Trace File Tree\n\n")
        handle.write(f"- generated_by: `build_manifest_index.py`\n")
        handle.write(f"- generated_at: `{generated_at}`\n")
        handle.write(f"- source_root: `{root.as_posix()}`\n")
        handle.write(f"- max_depth: `{max_depth}`\n")
        handle.write(f"- max_entries: `{max_entries}`\n\n")
        handle.write("```text\n")
        handle.write(f"{root.name}/\n")
        for line in iter_tree_lines(root, max_depth=max_depth, max_entries=max_entries):
            handle.write(f"  {line}\n")
        handle.write("```\n")


def write_manifest_index(root: Path, output_path: Path) -> dict[str, int]:
    counts = {"manifest_files": 0, "rows": 0, "ok": 0, "issues": 0}
    generated_at = utc_now()
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("# generated_by\tbuild_manifest_index.py\n")
        handle.write(f"# generated_at\t{generated_at}\n")
        handle.write(f"# source_root\t{root.as_posix()}\n")
        writer = csv.DictWriter(
            handle,
            fieldnames=TSV_COLUMNS,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        for manifest_path in iter_jsonl_files(root):
            counts["manifest_files"] += 1
            for row in manifest_rows(manifest_path, root):
                writer.writerow({column: clean_cell(row.get(column, "")) for column in TSV_COLUMNS})
                counts["rows"] += 1
                if row.get("status") in NON_ISSUE_STATUSES:
                    counts["ok"] += 1
                else:
                    counts["issues"] += 1
    return counts


def count_manifest_rows(root: Path) -> dict[str, int]:
    counts = {"manifest_files": 0, "rows": 0, "ok": 0, "issues": 0}
    for manifest_path in iter_jsonl_files(root):
        counts["manifest_files"] += 1
        for row in manifest_rows(manifest_path, root):
            counts["rows"] += 1
            if row.get("status") in NON_ISSUE_STATUSES:
                counts["ok"] += 1
            else:
                counts["issues"] += 1
    return counts


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate file_tree.md and manifest_index.tsv for a fetched trace root."
    )
    parser.add_argument("--root", required=True, type=Path, help="Fetched artifact root to scan.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for file_tree.md and manifest_index.tsv. Required unless --dry-run.",
    )
    parser.add_argument("--max-depth", type=int, default=5, help="Maximum tree depth.")
    parser.add_argument("--max-entries", type=int, default=2000, help="Maximum tree entries.")
    parser.add_argument("--dry-run", action="store_true", help="Scan and report counts without writing.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    output_dir = args.output_dir.resolve() if args.output_dir else None

    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}", file=sys.stderr)
        return 2
    if args.max_depth < 0 or args.max_entries < 1:
        print("ERROR: --max-depth must be >= 0 and --max-entries must be >= 1", file=sys.stderr)
        return 2

    if args.dry_run:
        counts = count_manifest_rows(root)
        print("dry_run=true")
        print(f"root={root}")
        print(f"output_dir={output_dir or '[not set]'}")
        print(f"manifest_files={counts['manifest_files']}")
        print(f"manifest_rows={counts['rows']}")
        print(f"ok_rows={counts['ok']}")
        print(f"issue_rows={counts['issues']}")
        return 0 if counts["issues"] == 0 else 1

    if output_dir is None:
        print("ERROR: --output-dir is required unless --dry-run", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    tree_path = output_dir / "file_tree.md"
    index_path = output_dir / "manifest_index.tsv"
    write_file_tree(root, tree_path, max_depth=args.max_depth, max_entries=args.max_entries)
    counts = write_manifest_index(root, index_path)

    print(f"wrote {tree_path}")
    print(f"wrote {index_path}")
    print(
        "manifest_files={manifest_files} manifest_rows={rows} ok_rows={ok} issue_rows={issues}".format(
            **counts
        )
    )
    return 0 if counts["issues"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
