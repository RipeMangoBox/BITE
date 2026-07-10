#!/usr/bin/env python3
"""Evaluate MinerU markdown body length and exact BITE structured contexts."""

from __future__ import annotations

import csv
import importlib.util
import json
import re
import sys
from pathlib import Path


RUNNER = Path("scripts/run_local_paper_analysis.py")
PDF_AUDIT = Path("_private/analysis_audits/structured_context_mainbody_budget_audit_20260626_n60.csv")
PARSE_PATHS = Path("/tmp/bite_parse_full_paths.txt")
OUT_PREFIX = Path("_private/analysis_audits/mineru_context_precision_audit_20260626_n10")


STOP_HEADING_RE = re.compile(
    r"(?i)\b(acknowledg(?:e)?ments?|references?|bibliography|appendix|supplement(?:ary|al)?)\b"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def load_runner():
    spec = importlib.util.spec_from_file_location("bite_runner", RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {RUNNER}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def find_parse_paths() -> list[Path]:
    if not PARSE_PATHS.exists():
        raise FileNotFoundError(f"{PARSE_PATHS} missing; run find */parse/full.md first")
    return [Path(line.strip()) for line in PARSE_PATHS.read_text().splitlines() if line.strip()]


def match_rows() -> list[dict]:
    parse_index = [(norm(str(path)), path) for path in find_parse_paths()]
    rows = list(csv.DictReader(PDF_AUDIT.open()))
    matched = []
    for row in rows:
        key = norm(Path(row["file"]).stem)[:80]
        hits = [path for haystack, path in parse_index if key and key in haystack]
        if hits:
            row = dict(row)
            row["parse_full_md"] = str(hits[0])
            matched.append(row)
    return matched


def choose_10(matched: list[dict]) -> list[dict]:
    chosen: list[dict] = []
    by_bucket: dict[str, list[dict]] = {}
    seen_paths: set[str] = set()
    for row in matched:
        by_bucket.setdefault(row["bucket"], []).append(row)
    for bucket in ("CVPR", "NEURIPS", "ICCV_ECCV", "ICLR", "SIGGRAPH"):
        rows = sorted(by_bucket.get(bucket, []), key=lambda r: int(r["pre_invalid_chars"]))
        if not rows:
            continue
        deduped = []
        local_seen: set[str] = set()
        for row in rows:
            key = row["parse_full_md"]
            if key not in local_seen:
                deduped.append(row)
                local_seen.add(key)
        rows = deduped
        if len(rows) == 1:
            if rows[0]["parse_full_md"] not in seen_paths:
                chosen.append(rows[0])
                seen_paths.add(rows[0]["parse_full_md"])
            continue
        for row in (rows[len(rows) // 2], rows[-1]):
            if row["parse_full_md"] not in seen_paths:
                chosen.append(row)
                seen_paths.add(row["parse_full_md"])
    if len(chosen) < 10:
        for row in sorted(matched, key=lambda r: int(r["pre_invalid_chars"]), reverse=True):
            if row["parse_full_md"] not in seen_paths:
                chosen.append(row)
                seen_paths.add(row["parse_full_md"])
            if len(chosen) >= 10:
                break
    return chosen[:10]


def cut_main_body_markdown(markdown: str) -> tuple[str, str, int]:
    matches = list(HEADING_RE.finditer(markdown))
    min_pos = max(2000, int(len(markdown) * 0.15))
    candidates: list[tuple[int, str]] = []
    for match in matches:
        heading = match.group(2).strip()
        if match.start() >= min_pos and STOP_HEADING_RE.search(heading):
            candidates.append((match.start(), heading))
    if candidates:
        pos, heading = candidates[0]
        return markdown[:pos].strip(), heading, pos

    # Fallback: exact-ish standalone lines only, not arbitrary inline mentions.
    char_pos = 0
    for line in markdown.splitlines():
        stripped = re.sub(r"^#+\s*", "", line).strip()
        if char_pos >= min_pos and STOP_HEADING_RE.search(stripped) and len(stripped) <= 120:
            return markdown[:char_pos].strip(), stripped, char_pos
        char_pos += len(line) + 1
    return markdown.strip(), "", -1


def section_stats(mod, markdown: str, context: str) -> dict:
    sections = mod.split_markdown_sections(markdown)
    body_sections = [
        s
        for s in sections
        if s.get("heading") not in ("PREAMBLE", "FULL_TEXT")
        and not mod.MAIN_CONTEXT_EXCLUDE_HEADING_RE.search(str(s.get("heading") or ""))
    ]
    key_sections = [
        s for s in body_sections if mod.MAIN_CONTEXT_KEY_HEADING_RE.search(str(s.get("heading") or ""))
    ]
    covered = 0
    key_covered = 0
    truncated_markers = context.count("[... section truncated ...]") + context.count("\n...")
    for section in body_sections:
        text = str(section.get("text") or "")
        probe = re.sub(r"\s+", " ", text[:220]).strip()
        if probe and probe[:80] in re.sub(r"\s+", " ", context):
            covered += 1
    for section in key_sections:
        text = str(section.get("text") or "")
        probe = re.sub(r"\s+", " ", text[:220]).strip()
        if probe and probe[:80] in re.sub(r"\s+", " ", context):
            key_covered += 1
    return {
        "body_sections": len(body_sections),
        "key_sections": len(key_sections),
        "covered_sections_probe": covered,
        "covered_key_sections_probe": key_covered,
        "truncated_markers": truncated_markers,
    }


def main() -> None:
    mod = load_runner()
    chosen = choose_10(match_rows())
    rows = []
    for row in chosen:
        markdown = Path(row["parse_full_md"]).read_text(errors="ignore")
        body, stop_heading, stop_pos = cut_main_body_markdown(markdown)
        structured = mod.main_paper_context(markdown, max_chars=24_000, mode="structured")
        structured36 = mod.main_paper_context(markdown, max_chars=36_000, mode="structured")
        structured48 = mod.main_paper_context(markdown, max_chars=48_000, mode="structured")
        stats24 = section_stats(mod, markdown, structured)
        stats36 = section_stats(mod, markdown, structured36)
        stats48 = section_stats(mod, markdown, structured48)
        out = {
            "bucket": row["bucket"],
            "venue": row["venue"],
            "file": row["file"],
            "parse_full_md": row["parse_full_md"],
            "pdf_pre_invalid_chars": int(row["pre_invalid_chars"]),
            "mineru_markdown_chars": len(markdown),
            "mineru_body_chars": len(body),
            "body_stop_heading": stop_heading,
            "body_stop_pos": stop_pos,
            "structured24_chars": len(structured),
            "structured36_chars": len(structured36),
            "structured48_chars": len(structured48),
            **{f"structured24_{k}": v for k, v in stats24.items()},
            **{f"structured36_{k}": v for k, v in stats36.items()},
            **{f"structured48_{k}": v for k, v in stats48.items()},
        }
        rows.append(out)

    OUT_PREFIX.parent.mkdir(parents=True, exist_ok=True)
    json_path = OUT_PREFIX.with_suffix(".json")
    csv_path = OUT_PREFIX.with_suffix(".csv")
    md_path = OUT_PREFIX.with_suffix(".md")
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    fieldnames = list(rows[0].keys()) if rows else []
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    lines = ["# MinerU Context Precision Audit", ""]
    lines.append("| bucket | file | pdf chars | MinerU body | s24 | s36 | s48 | key covered 24/36/48 | trunc 24/36/48 | stop |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in rows:
        key_cov = f"{r['structured24_covered_key_sections_probe']}/{r['structured24_key_sections']} / {r['structured36_covered_key_sections_probe']}/{r['structured36_key_sections']} / {r['structured48_covered_key_sections_probe']}/{r['structured48_key_sections']}"
        trunc = f"{r['structured24_truncated_markers']} / {r['structured36_truncated_markers']} / {r['structured48_truncated_markers']}"
        lines.append(
            f"| {r['bucket']} | {Path(r['file']).stem[:44]} | {r['pdf_pre_invalid_chars']} | "
            f"{r['mineru_body_chars']} | {r['structured24_chars']} | {r['structured36_chars']} | "
            f"{r['structured48_chars']} | {key_cov} | {trunc} | {r['body_stop_heading'][:40]} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(rows, indent=2, ensure_ascii=False))
    print(f"wrote {csv_path}")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
