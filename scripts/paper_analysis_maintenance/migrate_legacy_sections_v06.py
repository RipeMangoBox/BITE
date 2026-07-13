#!/usr/bin/env python3
"""Conservatively regroup complete legacy BITE notes into v06 sections.

The migration only replaces known level-two section headings and concatenates
their untouched payloads. It does not read PDFs, summarize prose, or alter
frontmatter, links, embeds, formulas, tables, and source anchors.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ANALYSIS_DIR = REPO_ROOT / "obsidian-vault" / "analysis"
DEFAULT_RUNS_DIR = REPO_ROOT / "_private" / "BITE_versions" / "v06.1" / "runs"

HEADING_RE = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.MULTILINE)
CANONICAL = (
    "概要",
    "核心方法与创新机理",
    "实验与关键发现",
    "定位与知识库关联",
    "原文 PDF",
)
MAPPING = (
    ("概要", ("概述", "背景与动机")),
    ("核心方法与创新机理", ("核心创新", "整体框架", "核心模块与公式推导")),
    ("实验与关键发现", ("实验与分析",)),
    ("定位与知识库关联", ("方法谱系与知识库定位",)),
    ("原文 PDF", ("原文 PDF", "Local Reading")),
)
LEGACY_HEADINGS = frozenset(name for _, names in MAPPING for name in names)


@dataclass(frozen=True)
class Section:
    heading: str
    payload: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Regroup complete legacy seven-section notes into the v06 canonical structure."
    )
    parser.add_argument("--analysis-dir", type=Path, default=DEFAULT_ANALYSIS_DIR)
    parser.add_argument(
        "--paths-file",
        type=Path,
        help="UTF-8 file containing one note path per line; blank lines and # comments are ignored.",
    )
    parser.add_argument("--write", action="store_true", help="Write notes. Default is dry-run.")
    parser.add_argument(
        "--run-dir",
        type=Path,
        help="Report/backup directory. Defaults to a timestamped directory under v06.1/runs.",
    )
    return parser.parse_args()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_sections(text: str) -> tuple[str, list[Section]]:
    matches = list(HEADING_RE.finditer(text))
    if not matches:
        return text, []
    prelude = text[: matches[0].start()]
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(Section(match.group(1).strip(), text[match.end() : end]))
    return prelude, sections


def migrate(text: str) -> tuple[str | None, str, dict[str, object]]:
    prelude, sections = split_sections(text)
    headings = [section.heading for section in sections]
    details: dict[str, object] = {"headings_before": headings}

    if tuple(headings) == CANONICAL:
        return None, "already_canonical", details
    unknown = [heading for heading in headings if heading not in LEGACY_HEADINGS]
    if unknown:
        details["unknown_headings"] = unknown
        return None, "manual_review_unknown_h2", details

    counts = {heading: headings.count(heading) for heading in LEGACY_HEADINGS}
    duplicates = sorted(heading for heading, count in counts.items() if count > 1)
    if duplicates:
        details["duplicate_headings"] = duplicates
        return None, "manual_review_duplicate_h2", details

    missing_groups = [
        target for target, sources in MAPPING if not any(source in headings for source in sources)
    ]
    # A safe legacy migration needs content for every canonical group. The
    # method group additionally requires all three old method sections so no
    # ambiguous partial template is silently accepted.
    missing_method = [
        source
        for source in ("核心创新", "整体框架", "核心模块与公式推导")
        if source not in headings
    ]
    if missing_groups or missing_method:
        details["missing_groups"] = missing_groups
        details["missing_method_sections"] = missing_method
        return None, "manual_review_incomplete_legacy", details

    by_heading = {section.heading: section.payload for section in sections}
    chunks = [prelude.rstrip()]
    payload_before = "".join(section.payload for section in sections)
    payload_after_parts: list[str] = []
    for target, sources in MAPPING:
        payload = "".join(by_heading[source] for source in sources if source in by_heading)
        payload_after_parts.append(payload)
        chunks.append(f"## {target}{payload}")
    migrated = "\n\n".join(chunks).rstrip() + "\n"

    if "".join(payload_after_parts) != payload_before:
        return None, "internal_error_payload_changed", details
    details["headings_after"] = list(CANONICAL)
    details["payload_sha256"] = sha256(payload_before)
    return migrated, "changed", details


def resolve_candidates(analysis_dir: Path, paths_file: Path | None) -> list[Path]:
    analysis_dir = analysis_dir.resolve()
    if paths_file is None:
        return sorted(path for path in analysis_dir.glob("*/*.md") if path.is_file())

    candidates: list[Path] = []
    for line_number, raw in enumerate(paths_file.read_text(encoding="utf-8").splitlines(), 1):
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        path = Path(value)
        if not path.is_absolute():
            repo_path = (REPO_ROOT / path).resolve()
            analysis_path = (analysis_dir / path).resolve()
            path = repo_path if repo_path.is_relative_to(analysis_dir) else analysis_path
        else:
            path = path.resolve()
        if not path.is_relative_to(analysis_dir):
            raise ValueError(f"line {line_number}: path is outside analysis-dir: {value}")
        if path.parent.parent != analysis_dir or path.suffix != ".md":
            raise ValueError(f"line {line_number}: expected a top-level analysis note: {value}")
        if not path.is_file():
            raise FileNotFoundError(f"line {line_number}: note not found: {value}")
        candidates.append(path)
    return sorted(set(candidates))


def atomic_write(path: Path, text: str) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except BaseException:
        Path(temp_name).unlink(missing_ok=True)
        raise


def main() -> int:
    args = parse_args()
    analysis_dir = args.analysis_dir.resolve()
    stamp = datetime.now().astimezone().strftime("%Y-%m-%d_%H%M%S")
    run_dir = (args.run_dir or DEFAULT_RUNS_DIR / f"structure_migration_{stamp}").resolve()
    if args.write and run_dir.exists():
        raise FileExistsError(f"write-mode run-dir must not already exist: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=True)
    backup_dir = run_dir / "backups"
    report_path = run_dir / "report.jsonl"

    candidates = resolve_candidates(analysis_dir, args.paths_file)
    records: list[dict[str, object]] = []
    changed = 0
    for path in candidates:
        original = path.read_text(encoding="utf-8")
        updated, status, details = migrate(original)
        record: dict[str, object] = {
            "path": str(path),
            "relative_path": str(path.relative_to(analysis_dir)),
            "status": status,
            "before_sha256": sha256(original),
            **details,
        }
        if updated is not None:
            changed += 1
            record["after_sha256"] = sha256(updated)
            if args.write:
                backup = backup_dir / path.relative_to(analysis_dir)
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, backup)
                atomic_write(path, updated)
                if path.read_text(encoding="utf-8") != updated:
                    raise OSError(f"post-write verification failed: {path}")
                record["backup_path"] = str(backup)
                record["status"] = "written"
        records.append(record)

    with report_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    summary = {
        "mode": "write" if args.write else "dry-run",
        "candidates": len(candidates),
        "changed": changed,
        "unchanged_or_manual_review": len(candidates) - changed,
        "report": str(report_path),
        "backup_dir": str(backup_dir) if args.write else None,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
