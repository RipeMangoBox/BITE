"""Discover local ICLR 2026 PDFs and write a verified JSONL manifest.

This script is intentionally read-only for source PDF files. It computes
sha256/size, aligns rows with the resmax manifest when available, deduplicates
by sha256, and writes discovery docs under _private/iclr26_batch/.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = REPO_ROOT / "_private" / "resmax_downloads" / "manifest.jsonl"
DEFAULT_OUTPUT = REPO_ROOT / "_private" / "iclr26_batch" / "manifests" / "discovered_pdfs.jsonl"
DEFAULT_REPORT = REPO_ROOT / "_private" / "iclr26_batch" / "reports" / "pdf_discovery_report.md"
DEFAULT_README = REPO_ROOT / "_private" / "iclr26_batch" / "README.md"

SEARCH_ROOTS = [
    REPO_ROOT / "_private" / "resmax_downloads" / "pdfs" / "ICLR_2026",
    REPO_ROOT / "_private" / "huggingface" / "resmax",
    REPO_ROOT / "_private" / "mineru_comparison",
    REPO_ROOT / "paperPDFs",
]


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _source_for_path(path: Path) -> str:
    s = path.as_posix()
    if "_private/resmax_downloads/" in s:
        return "resmax"
    if "_private/huggingface/" in s:
        return "huggingface"
    if "paperPDFs/" in s:
        return "manual"
    return "unknown"


def _title_guess(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"__ICLR_2026_[A-Za-z0-9_\\-]+$", "", stem)
    stem = re.sub(r"__[0-9a-f]{8,64}$", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"_+", " ", stem).strip()
    return stem or path.stem


def _read_resmax_manifest(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            if raw.get("conf_year") != "ICLR_2026":
                continue
            rows.append(raw)
    return rows


def _verified_row_from_manifest(raw: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    output_pdf = raw.get("output_pdf") or ""
    if not output_pdf:
        return None, "missing_output_pdf"
    path = (REPO_ROOT / output_pdf).resolve()
    if not path.exists() or not path.is_file():
        return None, "missing_pdf"
    size = path.stat().st_size
    expected_size = int(raw.get("size_bytes") or 0)
    if expected_size and size != expected_size:
        return None, "size_mismatch"
    sha = _sha256(path)
    expected_sha = raw.get("sha256") or ""
    if expected_sha and sha != expected_sha:
        return None, "sha256_mismatch"
    return {
        "sha256": sha,
        "size_bytes": size,
        "path": _rel(path),
        "title_guess": raw.get("title") or _title_guess(path),
        "openreview_forum_id": raw.get("openreview_forum_id") or "",
        "source": "resmax",
        "status": "discovered",
        "conf_year": raw.get("conf_year") or "ICLR_2026",
        "manifest_paper_id": raw.get("paper_id") or "",
        "pdf_url": raw.get("pdf_url") or raw.get("downloaded_url") or "",
        "manifest_status": raw.get("status") or "",
        "updated_at": raw.get("updated_at") or "",
    }, "verified"


def discover() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows_by_sha: dict[str, dict[str, Any]] = {}
    duplicate_paths: dict[str, list[str]] = {}
    stats: dict[str, Any] = {
        "resmax_manifest_rows_iclr26": 0,
        "resmax_verified": 0,
        "manifest_skip_reasons": Counter(),
        "scanned_unmatched_pdfs": 0,
        "unmatched_added": 0,
        "deduplicated_sha_count": 0,
        "search_roots": [_rel(p) for p in SEARCH_ROOTS],
    }

    manifest_rows = _read_resmax_manifest(DEFAULT_MANIFEST)
    stats["resmax_manifest_rows_iclr26"] = len(manifest_rows)
    manifest_paths: set[Path] = set()
    for raw in manifest_rows:
        if raw.get("output_pdf"):
            manifest_paths.add((REPO_ROOT / raw["output_pdf"]).resolve())
        row, reason = _verified_row_from_manifest(raw)
        if not row:
            stats["manifest_skip_reasons"][reason] += 1
            continue
        sha = row["sha256"]
        if sha in rows_by_sha:
            duplicate_paths.setdefault(sha, []).append(row["path"])
            continue
        rows_by_sha[sha] = row
        stats["resmax_verified"] += 1

    for root in SEARCH_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.pdf"):
            path = path.resolve()
            if path in manifest_paths:
                continue
            if "ICLR_2026" not in path.as_posix() and "paperPDFs" not in path.as_posix():
                continue
            stats["scanned_unmatched_pdfs"] += 1
            sha = _sha256(path)
            if sha in rows_by_sha:
                duplicate_paths.setdefault(sha, []).append(_rel(path))
                continue
            rows_by_sha[sha] = {
                "sha256": sha,
                "size_bytes": path.stat().st_size,
                "path": _rel(path),
                "title_guess": _title_guess(path),
                "openreview_forum_id": "",
                "source": _source_for_path(path),
                "status": "discovered",
                "conf_year": "ICLR_2026" if "ICLR_2026" in path.as_posix() else "",
                "manifest_paper_id": "",
                "pdf_url": "",
                "manifest_status": "",
                "updated_at": "",
            }
            stats["unmatched_added"] += 1

    for sha, paths in duplicate_paths.items():
        if sha in rows_by_sha:
            rows_by_sha[sha]["duplicate_paths"] = paths
    rows = sorted(
        rows_by_sha.values(),
        key=lambda r: (
            0 if r.get("source") == "resmax" else 1,
            (r.get("title_guess") or "").lower(),
            r.get("path") or "",
        ),
    )
    stats["deduplicated_sha_count"] = len(rows)
    stats["by_source"] = Counter(r.get("source") or "unknown" for r in rows)
    stats["with_openreview_forum_id"] = sum(1 for r in rows if r.get("openreview_forum_id"))
    stats["manifest_skip_reasons"] = dict(stats["manifest_skip_reasons"])
    stats["by_source"] = dict(stats["by_source"])
    return rows, stats


def write_outputs(rows: list[dict[str, Any]], stats: dict[str, Any], output: Path, report: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    now = datetime.now(timezone.utc).isoformat()
    report.parent.mkdir(parents=True, exist_ok=True)
    by_source = stats.get("by_source", {})
    skip_reasons = stats.get("manifest_skip_reasons", {})
    lines = [
        "# ICLR 2026 PDF Discovery Report",
        "",
        f"- generated_at: `{now}`",
        f"- output_manifest: `{_rel(output)}`",
        f"- resmax_manifest: `{_rel(DEFAULT_MANIFEST)}`",
        f"- deduplicated_verified_pdfs: `{len(rows)}`",
        f"- with_openreview_forum_id: `{stats.get('with_openreview_forum_id', 0)}`",
        "",
        "## Search Roots",
        "",
    ]
    for root in stats.get("search_roots", []):
        exists = (REPO_ROOT / root).exists()
        lines.append(f"- `{root}` ({'exists' if exists else 'missing'})")
    lines += [
        "",
        "## Counts",
        "",
        f"- resmax_manifest_rows_iclr26: `{stats.get('resmax_manifest_rows_iclr26', 0)}`",
        f"- resmax_verified: `{stats.get('resmax_verified', 0)}`",
        f"- scanned_unmatched_pdfs: `{stats.get('scanned_unmatched_pdfs', 0)}`",
        f"- unmatched_added: `{stats.get('unmatched_added', 0)}`",
        f"- deduplicated_sha_count: `{stats.get('deduplicated_sha_count', 0)}`",
        "",
        "## By Source",
        "",
    ]
    for source, count in sorted(by_source.items()):
        lines.append(f"- {source}: `{count}`")
    lines += ["", "## Manifest Skips", ""]
    if skip_reasons:
        for reason, count in sorted(skip_reasons.items()):
            lines.append(f"- {reason}: `{count}`")
    else:
        lines.append("- none")
    lines += [
        "",
        "## Batch Selection Implication",
        "",
        "Batch selection must use rows with `conf_year=ICLR_2026`, existing verified PDF size/sha256, and a non-empty `openreview_forum_id`.",
        "The original PDF files were not moved or renamed.",
        "",
    ]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    DEFAULT_README.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_README.write_text(
        "\n".join([
            "# ICLR 2026 Batch Workspace",
            "",
            "This directory stores generated manifests, contracts, verification reports, and review checklists for the local ICLR 2026 batch pipeline.",
            "",
            "Current discovery artifacts:",
            "",
            f"- PDF discovery manifest: `{_rel(output)}`",
            f"- PDF discovery report: `{_rel(report)}`",
            "",
            "Source of truth remains PostgreSQL. Markdown and vault files are review exports only.",
            "",
        ]),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    rows, stats = discover()
    write_outputs(rows, stats, Path(args.output), Path(args.report))
    print(json.dumps({
        "output": _rel(Path(args.output)),
        "report": _rel(Path(args.report)),
        "deduplicated_verified_pdfs": len(rows),
        "with_openreview_forum_id": stats.get("with_openreview_forum_id", 0),
        "by_source": stats.get("by_source", {}),
        "manifest_skip_reasons": stats.get("manifest_skip_reasons", {}),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
