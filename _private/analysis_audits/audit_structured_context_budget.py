#!/usr/bin/env python3
"""Audit pre-reference PDF text lengths for structured main-context budgeting."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover
    fitz = None


TARGET_BUCKETS = {
    "CVPR": ("CVPR_2026", "CVPR_2025", "CVPR_2024"),
    "NEURIPS": ("NEURIPS_2025", "NEURIPS_2024", "NEURIPS_2023", "NEURIPS_2022"),
    "SIGGRAPH": ("SIGGRAPH_2025", "SIGGRAPH_2024", "SIGGRAPH_2023", "SIGGRAPH_2022"),
    "ICLR": ("ICLR_2026", "ICLR_2025", "ICLR_2024"),
    "ICCV_ECCV": ("ICCV_2025", "ICCV_2023", "ECCV_2024"),
}

STOP_HEADING_RE = re.compile(
    r"^\s*(?:\d+\.?\s*)?"
    r"("
    r"acknowledg(?:e)?ments?|"
    r"references|bibliography|"
    r"appendix(?:\s+[A-Z0-9][\w.-]*)?.*|"
    r"supplementary(?:\s+material)?.*|"
    r"supplemental(?:\s+material)?.*"
    r")\s*$",
    re.IGNORECASE,
)
TITLE_LIKE_STOP_RE = re.compile(
    r"^\s*("
    r"acknowledg(?:e)?ments?|"
    r"references|bibliography|"
    r"appendix(?:\s+[A-Z0-9][\w.-]*)?.*|"
    r"supplementary(?:\s+material)?.*|"
    r"supplemental(?:\s+material)?.*"
    r")\s*$",
    re.IGNORECASE,
)
NOISE_LINE_RE = re.compile(
    r"^\s*(?:"
    r"arXiv:\S+|"
    r"CVPR\s+\d{4}|"
    r"Proceedings of .*|"
    r"\d+\s*|"
    r"Figure\s+\d+[:.]?\s*|"
    r"Table\s+\d+[:.]?\s*"
    r")\s*$",
    re.IGNORECASE,
)


def pdf_pages(path: Path) -> int | None:
    if fitz is None:
        return None
    try:
        with fitz.open(path) as doc:
            return doc.page_count
    except Exception:
        return None


def extract_text(path: Path, timeout: int) -> str:
    with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
        cmd = ["pdftotext", "-enc", "UTF-8", str(path), tmp.name]
        subprocess.run(cmd, check=True, timeout=timeout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return Path(tmp.name).read_text(errors="ignore")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = []
    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if NOISE_LINE_RE.match(line):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def cutoff_pre_invalid(text: str) -> tuple[str, str | None, int | None]:
    lines = text.splitlines()
    char_pos = 0
    best: tuple[int, str] | None = None
    min_pos = max(4000, int(len(text) * 0.20))
    for line in lines:
        stripped = line.strip()
        if char_pos >= min_pos and (STOP_HEADING_RE.match(stripped) or TITLE_LIKE_STOP_RE.match(stripped)):
            best = (char_pos, stripped)
            break
        char_pos += len(line) + 1
    if best is None:
        return text, None, None
    pos, heading = best
    return text[:pos].rstrip(), heading, pos


def percentile(values: list[int], q: float) -> int:
    if not values:
        return 0
    values = sorted(values)
    if len(values) == 1:
        return values[0]
    idx = (len(values) - 1) * q
    lo = math.floor(idx)
    hi = math.ceil(idx)
    if lo == hi:
        return values[lo]
    return round(values[lo] * (hi - idx) + values[hi] * (idx - lo))


def choose_sample(paths: list[Path], n: int, seed: int) -> list[Path]:
    rng = random.Random(seed)
    paths = sorted(paths)
    if len(paths) <= n:
        return paths
    return sorted(rng.sample(paths, n))


def bucket_for(venue_dir: str) -> str | None:
    for bucket, venues in TARGET_BUCKETS.items():
        if venue_dir in venues:
            return bucket
    return None


def audit(root: Path, sample_per_bucket: int, seed: int, timeout: int) -> tuple[list[dict], dict]:
    by_bucket: dict[str, list[Path]] = defaultdict(list)
    for pdf in root.glob("*/*.pdf"):
        bucket = bucket_for(pdf.parent.name)
        if bucket:
            by_bucket[bucket].append(pdf)

    rows: list[dict] = []
    for bucket in sorted(by_bucket):
        for pdf in choose_sample(by_bucket[bucket], sample_per_bucket, seed + sum(map(ord, bucket))):
            row = {
                "bucket": bucket,
                "venue": pdf.parent.name,
                "path": str(pdf),
                "file": pdf.name,
                "pages": pdf_pages(pdf),
                "status": "ok",
                "text_chars": 0,
                "pre_invalid_chars": 0,
                "cutoff_heading": "",
                "cutoff_found": False,
            }
            try:
                text = normalize_text(extract_text(pdf, timeout=timeout))
                pre, heading, _ = cutoff_pre_invalid(text)
                row.update(
                    {
                        "text_chars": len(text),
                        "pre_invalid_chars": len(pre),
                        "cutoff_heading": heading or "",
                        "cutoff_found": heading is not None,
                    }
                )
                if len(text) < 2000:
                    row["status"] = "low_text"
            except Exception as exc:
                row["status"] = f"error:{type(exc).__name__}"
                row["error"] = str(exc)[:300]
            rows.append(row)

    summary: dict[str, dict] = {}
    for bucket in sorted(by_bucket):
        bucket_rows = [r for r in rows if r["bucket"] == bucket and r["status"] == "ok"]
        values = [int(r["pre_invalid_chars"]) for r in bucket_rows]
        summary[bucket] = {
            "available": len(by_bucket[bucket]),
            "sampled_ok": len(bucket_rows),
            "sampled_total": len([r for r in rows if r["bucket"] == bucket]),
            "cutoff_found": sum(1 for r in bucket_rows if r["cutoff_found"]),
            "min": min(values) if values else 0,
            "p50": percentile(values, 0.50),
            "p75": percentile(values, 0.75),
            "p90": percentile(values, 0.90),
            "p95": percentile(values, 0.95),
            "max": max(values) if values else 0,
        }
    all_values = [int(r["pre_invalid_chars"]) for r in rows if r["status"] == "ok"]
    summary["ALL"] = {
        "available": sum(len(v) for v in by_bucket.values()),
        "sampled_ok": len(all_values),
        "sampled_total": len(rows),
        "cutoff_found": sum(1 for r in rows if r["status"] == "ok" and r["cutoff_found"]),
        "min": min(all_values) if all_values else 0,
        "p50": percentile(all_values, 0.50),
        "p75": percentile(all_values, 0.75),
        "p90": percentile(all_values, 0.90),
        "p95": percentile(all_values, 0.95),
        "max": max(all_values) if all_values else 0,
    }
    return rows, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("obsidian-vault/paperPDFs"))
    parser.add_argument("--sample-per-bucket", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260626)
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--out-prefix", type=Path, default=Path("_private/analysis_audits/structured_context_budget_audit_20260626"))
    args = parser.parse_args()

    rows, summary = audit(args.root, args.sample_per_bucket, args.seed, args.timeout)
    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    csv_path = args.out_prefix.with_suffix(".csv")
    json_path = args.out_prefix.with_suffix(".json")
    md_path = args.out_prefix.with_suffix(".md")

    fieldnames = [
        "bucket",
        "venue",
        "file",
        "pages",
        "status",
        "text_chars",
        "pre_invalid_chars",
        "cutoff_found",
        "cutoff_heading",
        "path",
    ]
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps({"summary": summary, "rows": rows}, indent=2), encoding="utf-8")

    lines = ["# Structured Context Budget Audit", ""]
    lines.append(f"- sample_per_bucket: {args.sample_per_bucket}")
    lines.append(f"- seed: {args.seed}")
    lines.append(f"- pdf_root: `{args.root}`")
    lines.append("")
    lines.append("| bucket | available | ok/total | cutoff found | p50 | p75 | p90 | p95 | max |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for bucket, data in summary.items():
        lines.append(
            f"| {bucket} | {data['available']} | {data['sampled_ok']}/{data['sampled_total']} | "
            f"{data['cutoff_found']} | {data['p50']} | {data['p75']} | {data['p90']} | {data['p95']} | {data['max']} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"wrote {csv_path}")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
