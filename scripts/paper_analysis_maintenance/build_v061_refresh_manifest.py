#!/usr/bin/env python3
"""Build and validate the read-only v06.1 analysis refresh manifest.

This script never reads paper PDFs and never writes analysis notes. Its only
outputs are deterministic JSON/JSONL/CSV reports under the requested run dir.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
VAULT_ROOT = REPO_ROOT / "obsidian-vault"
ANALYSIS_DIR = VAULT_ROOT / "analysis"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "_private/BITE_versions/v06.1/runs/2026-07-13"
CUTOFF = "2026-06-26"

REQUIRED_FIELDS = (
    "title", "type", "paper_level", "venue", "year", "pdf_ref",
    "project_link", "code_link", "aliases", "tags", "core_operator",
    "primary_logic", "claims",
)
CANONICAL_SECTIONS = (
    "概要", "核心方法与创新机理", "实验与关键发现", "定位与知识库关联", "原文 PDF",
)
OLD_SECTIONS = (
    "概述", "背景与动机", "核心创新", "整体框架", "核心模块与公式推导",
    "实验与分析", "方法谱系与知识库定位",
)
EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
SUPPLEMENT_RE = re.compile(r"^#{2,6}\s+.*补充(?:图|图表|实验图|可视化).*$", re.MULTILINE | re.IGNORECASE)
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp", ".tif", ".tiff"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis-dir", type=Path, default=ANALYSIS_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--paths", type=Path, help="Optional newline, JSON, JSONL, or CSV path list to validate.")
    parser.add_argument("--cutoff", default=CUTOFF, help="Old-note cutoff date (YYYY-MM-DD, exclusive).")
    parser.add_argument("--stdout", action="store_true", help="Print summary JSON after writing reports.")
    return parser.parse_args()


def top_level_notes(analysis_dir: Path) -> list[Path]:
    return sorted(p for p in analysis_dir.glob("*/*.md") if p.is_file())


def load_paths(path: Path, analysis_dir: Path) -> list[Path]:
    text = path.read_text(encoding="utf-8-sig")
    suffix = path.suffix.lower()
    values: list[str] = []
    if suffix == ".json":
        obj = json.loads(text)
        rows = obj if isinstance(obj, list) else obj.get("notes", obj.get("paths", []))
        values = [str(x.get("note_path", x.get("path", "")) if isinstance(x, dict) else x) for x in rows]
    elif suffix == ".jsonl":
        for line in text.splitlines():
            if line.strip():
                obj = json.loads(line)
                values.append(str(obj.get("note_path", obj.get("path", "")) if isinstance(obj, dict) else obj))
    elif suffix == ".csv":
        rows = list(csv.DictReader(text.splitlines()))
        values = [str(r.get("note_path") or r.get("path") or "") for r in rows]
    else:
        values = [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    result: list[Path] = []
    for value in values:
        p = Path(value)
        if not p.is_absolute():
            p = REPO_ROOT / p if value.startswith("obsidian-vault/") else analysis_dir / value
        result.append(p.resolve())
    return sorted(set(result))


def git_creation_dates() -> dict[str, str]:
    cmd = ["git", "log", "--diff-filter=A", "--format=@@%aI", "--name-only", "--", "obsidian-vault/analysis"]
    proc = subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    if proc.returncode:
        return {}
    current = ""
    dates: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        if line.startswith("@@"):
            current = line[2:12]
        elif line.endswith(".md") and current:
            # git log is newest-first; overwrite so the final value is earliest.
            dates[line] = current
    return dates


def git_dirty_analysis_paths() -> set[str]:
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--", "obsidian-vault/analysis"],
        cwd=REPO_ROOT, capture_output=True, check=False,
    )
    if proc.returncode:
        return set()
    dirty: set[str] = set()
    entries = proc.stdout.decode("utf-8", errors="surrogateescape").split("\0")
    index = 0
    while index < len(entries):
        line = entries[index]
        index += 1
        if not line:
            continue
        value = line[3:]
        if " -> " in value:
            value = value.rsplit(" -> ", 1)[1]
        elif line[:2] in {"R ", "C ", " R", " C"} and index < len(entries):
            value = entries[index]
            index += 1
        dirty.add(value)
    return dirty


def calibration_sample(records: list[dict[str, Any]], dirty: set[str], size: int = 20) -> list[dict[str, Any]]:
    eligible = [r for r in records if r["note_path"] not in dirty and r.get("exists")]
    chosen: list[dict[str, Any]] = []
    seen: set[str] = set()

    def take(predicate: Any, count: int) -> None:
        for record in eligible:
            path = str(record["note_path"])
            if len([r for r in chosen if predicate(r)]) >= count:
                break
            if path not in seen and predicate(record):
                chosen.append(record)
                seen.add(path)

    take(lambda r: r["priority"] == "P0", 5)
    take(lambda r: r["structure_version"] == "legacy" and r["image_count"] == 12, 8)
    take(lambda r: r["structure_version"] == "legacy" and r["image_count"] != 12, 4)
    take(lambda r: r["structure_version"] == "noncanonical", 2)
    take(lambda r: r["structure_version"] == "v06_canonical" and r["priority"] != "Skip", 1)
    for record in eligible:
        if len(chosen) >= size:
            break
        path = str(record["note_path"])
        if path not in seen and record["priority"] != "Skip":
            chosen.append(record)
            seen.add(path)
    return chosen[:size]


def frontmatter_keys(text: str) -> tuple[set[str], bool]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return set(), False
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return set(), False
    keys = {m.group(1) for line in lines[1:end] if (m := re.match(r"^([A-Za-z0-9_-]+):(?:\s|$)", line))}
    return keys, True


def clean_embed_target(raw: str) -> str:
    target = raw.split("#", 1)[0]
    if "|" in target:
        target = target.split("|", 1)[0]
    return target.strip()


def resolve_embed(target: str) -> Path | None:
    if not target or target.startswith(("http://", "https://")):
        return None
    p = Path(target)
    if p.is_absolute() or target.startswith("../") or target.startswith("obsidian-vault/"):
        return p if p.is_absolute() else REPO_ROOT / p
    return VAULT_ROOT / p


def inspect_note(path: Path, creation_dates: dict[str, str], cutoff: str) -> dict[str, Any]:
    rel = path.relative_to(REPO_ROOT).as_posix() if path.is_relative_to(REPO_ROOT) else str(path)
    if not path.exists():
        return {"note_path": rel, "exists": False, "priority": "P0", "issues": ["missing_note"]}
    text = path.read_text(encoding="utf-8")
    keys, fm_valid = frontmatter_keys(text)
    headings = HEADING_RE.findall(text)
    missing_fields = [key for key in REQUIRED_FIELDS if key not in keys]
    missing_sections = [section for section in CANONICAL_SECTIONS if section not in headings]
    has_core = "> [!tip] 核心洞察" in text
    has_effect = "> [!tip] 效果简介" in text
    canonical = fm_valid and not missing_fields and not missing_sections and has_core and has_effect
    embeds = [clean_embed_target(x) for x in EMBED_RE.findall(text)]
    image_embeds = [x for x in embeds if Path(x).suffix.lower() in IMAGE_EXTS or x.startswith("assets/figures/")]
    pdf_embeds = [x for x in embeds if Path(x).suffix.lower() == ".pdf"]
    broken: list[str] = []
    invalid_prefix: list[str] = []
    for target in embeds:
        resolved = resolve_embed(target)
        if Path(target).is_absolute() or target.startswith(("../", "obsidian-vault/")):
            invalid_prefix.append(target)
        if resolved is not None and not resolved.exists():
            broken.append(target)
    supplemental = SUPPLEMENT_RE.findall(text)
    old_sections = [section for section in OLD_SECTIONS if section in headings]
    creation = creation_dates.get(rel)
    if creation and creation < cutoff:
        source = "pre_cutoff_git_created"
    elif creation:
        source = "post_cutoff_git_created"
    else:
        source = "unknown_creation"
    issues: list[str] = []
    if not fm_valid: issues.append("invalid_frontmatter")
    if missing_fields: issues.append("missing_frontmatter_fields")
    if missing_sections: issues.append("missing_canonical_sections")
    if not pdf_embeds: issues.append("missing_pdf_embed")
    if broken: issues.append("broken_local_embeds")
    if invalid_prefix: issues.append("invalid_embed_prefix")
    if old_sections: issues.append("old_section_structure")
    if len(image_embeds) == 12: issues.append("twelve_image_template")
    if supplemental: issues.append("supplemental_image_heading")
    if "[arXiv](" in text: issues.append("legacy_arxiv_label")
    if not canonical or broken or invalid_prefix or not pdf_embeds:
        priority = "P0" if (not fm_valid or broken or invalid_prefix or not pdf_embeds) else "P1"
    elif supplemental or len(image_embeds) > 6 or "[arXiv](" in text:
        priority = "P2"
    else:
        priority = "Skip"
    if canonical:
        structure_version = "v06_canonical"
    elif old_sections:
        structure_version = "legacy"
    else:
        structure_version = "noncanonical"
    return {
        "note_path": rel, "exists": True, "collection_source": source,
        "git_created": creation, "structure_version": structure_version,
        "canonical": canonical, "frontmatter_valid": fm_valid,
        "missing_fields": missing_fields, "missing_sections": missing_sections,
        "image_count": len(image_embeds), "pdf_embed_count": len(pdf_embeds),
        "supplemental_headings": supplemental, "broken_local_embeds": broken,
        "invalid_embed_prefixes": invalid_prefix, "old_sections": old_sections,
        "priority": priority, "issues": issues,
        "venue_year": path.parent.name,
    }


def write_outputs(records: list[dict[str, Any]], output_dir: Path, mode: str) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = "refresh_manifest" if mode == "full" else "validation_manifest"
    with (output_dir / f"{stem}.jsonl").open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    columns = ("note_path", "exists", "collection_source", "git_created", "structure_version", "canonical",
               "frontmatter_valid", "missing_fields", "missing_sections", "image_count", "pdf_embed_count",
               "supplemental_headings", "broken_local_embeds", "invalid_embed_prefixes", "priority", "issues", "venue_year")
    with (output_dir / f"{stem}.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for record in records:
            row = {k: record.get(k) for k in columns}
            for key, value in row.items():
                if isinstance(value, list): row[key] = json.dumps(value, ensure_ascii=False)
            writer.writerow(row)
    priority = Counter(r["priority"] for r in records)
    structure = Counter(r.get("structure_version", "missing") for r in records)
    source = Counter(r.get("collection_source", "missing") for r in records)
    venue = Counter(r.get("venue_year", "missing") for r in records)
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(), "mode": mode, "total": len(records),
        "canonical": sum(bool(r.get("canonical")) for r in records),
        "with_missing_fields": sum(bool(r.get("missing_fields")) for r in records),
        "with_supplemental_headings": sum(bool(r.get("supplemental_headings")) for r in records),
        "broken_embed_count": sum(len(r.get("broken_local_embeds", [])) for r in records),
        "image_count": sum(int(r.get("image_count", 0)) for r in records),
        "priority_counts": dict(sorted(priority.items())), "structure_counts": dict(sorted(structure.items())),
        "collection_source_counts": dict(sorted(source.items())), "venue_year_counts": dict(sorted(venue.items())),
    }
    (output_dir / f"{stem}_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if mode == "full":
        dirty = git_dirty_analysis_paths()
        sample = calibration_sample(records, dirty)
        (output_dir / "preexisting_dirty_paths.txt").write_text(
            "".join(f"{path}\n" for path in sorted(dirty)), encoding="utf-8"
        )
        (output_dir / "calibration_paths.txt").write_text(
            "".join(f"{record['note_path']}\n" for record in sample), encoding="utf-8"
        )
        (output_dir / "calibration_manifest.json").write_text(
            json.dumps(sample, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        summary["preexisting_dirty_count"] = len(dirty)
        summary["calibration_count"] = len(sample)
        (output_dir / f"{stem}_summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return summary


def main() -> int:
    args = parse_args()
    paths = load_paths(args.paths, args.analysis_dir) if args.paths else top_level_notes(args.analysis_dir)
    dates = git_creation_dates()
    records = [inspect_note(path, dates, args.cutoff) for path in paths]
    summary = write_outputs(records, args.output_dir, "selected" if args.paths else "full")
    if args.stdout:
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if args.paths and any(r["priority"] == "P0" for r in records) else 0


if __name__ == "__main__":
    raise SystemExit(main())
