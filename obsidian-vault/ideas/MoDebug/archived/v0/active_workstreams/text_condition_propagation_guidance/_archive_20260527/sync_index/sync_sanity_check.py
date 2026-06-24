#!/usr/bin/env python3
"""Read-only sanity checks for fetched trace run directories."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


RUN_DIR_RE = re.compile(
    r"^\d{8}_\d{6}_[A-Za-z0-9][A-Za-z0-9-]*(?:_[A-Za-z0-9][A-Za-z0-9-]*)+$"
)
TIMESTAMP_PREFIX_RE = re.compile(r"^\d{8}_\d{6}_")

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

STANDARD_MANIFEST_NAMES = {"forward_manifest.jsonl", "delta_manifest.jsonl"}


@dataclass
class Issue:
    level: str
    path: Path
    message: str


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def display(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def iter_dirs(root: Path) -> Iterator[Path]:
    yield root
    for dirpath, dirnames, _filenames in os.walk(root, followlinks=False):
        dirnames[:] = sorted(
            name
            for name in dirnames
            if not (Path(dirpath) / name).is_symlink()
        )
        for dirname in dirnames:
            yield Path(dirpath) / dirname


def find_run_dirs(root: Path) -> tuple[list[Path], list[Path]]:
    run_dirs: list[Path] = []
    malformed_timestamp_dirs: list[Path] = []
    for directory in iter_dirs(root):
        name = directory.name
        if RUN_DIR_RE.match(name):
            run_dirs.append(directory)
        elif TIMESTAMP_PREFIX_RE.match(name):
            malformed_timestamp_dirs.append(directory)
    return sorted(set(run_dirs)), sorted(set(malformed_timestamp_dirs))


def iter_jsonl_files(run_dir: Path) -> Iterator[Path]:
    for dirpath, dirnames, filenames in os.walk(run_dir, followlinks=False):
        dirnames[:] = sorted(
            name
            for name in dirnames
            if not (Path(dirpath) / name).is_symlink()
        )
        for filename in sorted(filenames):
            if filename.endswith(".jsonl"):
                yield Path(dirpath) / filename


def classify_record(record: dict[str, object], manifest_path: Path) -> tuple[str, list[str], str]:
    if "forward_npz_path" in record:
        return "forward", FORWARD_FIELDS, str(record.get("forward_npz_path") or "")
    if "delta_npz_path" in record:
        return "delta", DELTA_FIELDS, str(record.get("delta_npz_path") or "")
    if "forward" in manifest_path.name:
        return "forward", FORWARD_FIELDS, ""
    if "delta" in manifest_path.name:
        return "delta", DELTA_FIELDS, ""
    return "unknown", [], ""


def resolve_manifest_path(
    raw_path: str,
    root: Path,
    run_dir: Path,
    allow_run_relative: bool,
) -> tuple[Path | None, str | None]:
    if not raw_path:
        return None, "empty NPZ path"
    candidate = Path(raw_path)
    if candidate.is_absolute():
        resolved = candidate.resolve(strict=False)
        if not is_relative_to(resolved, root):
            return None, f"absolute path escapes fetched root: {raw_path}"
        return resolved, None

    root_candidate = (root / candidate).resolve(strict=False)
    if not is_relative_to(root_candidate, root):
        return None, f"relative path escapes fetched root: {raw_path}"
    if root_candidate.exists():
        return root_candidate, None

    if allow_run_relative:
        run_candidate = (run_dir / candidate).resolve(strict=False)
        if not is_relative_to(run_candidate, root):
            return None, f"run-relative path escapes fetched root: {raw_path}"
        if run_candidate.exists():
            return run_candidate, None

    return root_candidate, None


def check_manifest(
    manifest_path: Path,
    root: Path,
    run_dir: Path,
    allow_run_relative: bool,
) -> tuple[list[Issue], int]:
    issues: list[Issue] = []
    rows = 0

    if manifest_path.name not in STANDARD_MANIFEST_NAMES:
        issues.append(Issue("WARN", manifest_path, "non-standard manifest filename"))
    if manifest_path.parent != run_dir:
        issues.append(Issue("ERROR", manifest_path, "manifest is not directly under the run directory"))

    try:
        handle = manifest_path.open("r", encoding="utf-8")
    except OSError as exc:
        return [Issue("ERROR", manifest_path, f"cannot read manifest: {exc}")], 0

    with handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            rows += 1
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                issues.append(Issue("ERROR", manifest_path, f"line {line_no}: JSON error: {exc.msg}"))
                continue
            if not isinstance(record, dict):
                issues.append(Issue("ERROR", manifest_path, f"line {line_no}: JSON value is not an object"))
                continue

            kind, required_fields, npz_path = classify_record(record, manifest_path)
            if kind == "unknown":
                issues.append(
                    Issue("ERROR", manifest_path, f"line {line_no}: cannot classify as forward or delta")
                )
                continue

            missing = [field for field in required_fields if field not in record]
            if missing:
                issues.append(
                    Issue("ERROR", manifest_path, f"line {line_no}: missing fields: {','.join(missing)}")
                )

            run_id = str(record.get("run_id") or "")
            if run_id and run_id != run_dir.name:
                issues.append(
                    Issue("WARN", manifest_path, f"line {line_no}: run_id differs from run dir: {run_id}")
                )

            resolved_path, path_error = resolve_manifest_path(
                npz_path,
                root=root,
                run_dir=run_dir,
                allow_run_relative=allow_run_relative,
            )
            if path_error:
                issues.append(Issue("ERROR", manifest_path, f"line {line_no}: {path_error}"))
                continue
            if resolved_path is None or not resolved_path.exists():
                issues.append(
                    Issue("ERROR", manifest_path, f"line {line_no}: NPZ path does not exist: {npz_path}")
                )
            elif resolved_path.suffix != ".npz":
                issues.append(
                    Issue("WARN", manifest_path, f"line {line_no}: NPZ path has non-.npz suffix: {npz_path}")
                )

    return issues, rows


def check_root(root: Path, allow_run_relative: bool) -> tuple[list[Issue], dict[str, int]]:
    issues: list[Issue] = []
    counts = {"run_dirs": 0, "manifest_files": 0, "manifest_rows": 0}
    run_dirs, malformed_dirs = find_run_dirs(root)

    for directory in malformed_dirs:
        issues.append(Issue("ERROR", directory, "timestamp-prefixed directory does not match run dir regex"))

    if not run_dirs:
        issues.append(Issue("ERROR", root, "no run directories found"))
        return issues, counts

    for run_dir in run_dirs:
        counts["run_dirs"] += 1
        manifests = list(iter_jsonl_files(run_dir))
        if not manifests:
            issues.append(Issue("ERROR", run_dir, "no JSONL manifests found"))
            continue
        for manifest_path in manifests:
            counts["manifest_files"] += 1
            manifest_issues, row_count = check_manifest(
                manifest_path,
                root=root,
                run_dir=run_dir,
                allow_run_relative=allow_run_relative,
            )
            counts["manifest_rows"] += row_count
            issues.extend(manifest_issues)

    return issues, counts


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check fetched trace run directories without writing files.")
    parser.add_argument("--root", required=True, type=Path, help="Fetched artifact root to check.")
    parser.add_argument("--dry-run", action="store_true", help="Print read-only mode marker.")
    parser.add_argument(
        "--allow-run-relative",
        action="store_true",
        help="Also accept NPZ paths relative to the enclosing run directory.",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] = sys.argv[1:]) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}", file=sys.stderr)
        return 2

    issues, counts = check_root(root, allow_run_relative=args.allow_run_relative)
    if args.dry_run:
        print("dry_run=true")
    print(f"root={root}")
    print(
        "run_dirs={run_dirs} manifest_files={manifest_files} manifest_rows={manifest_rows}".format(
            **counts
        )
    )

    error_count = sum(1 for issue in issues if issue.level == "ERROR")
    warn_count = sum(1 for issue in issues if issue.level == "WARN")
    for issue in issues:
        print(f"{issue.level}: {display(issue.path, root)}: {issue.message}")
    print(f"errors={error_count} warnings={warn_count}")
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
