#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import fitz
import yaml


ROOT = Path(__file__).resolve().parents[2]
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"
REPORT_DIR = ROOT / "obsidian-vault" / "batches" / "reports"
QUARANTINE_ROOT = ROOT / "_private" / "quarantine" / "mismatched_pdfs"
CSV_FIELDS = [
    "state",
    "importance",
    "paper_title",
    "venue",
    "project_link_or_github_link",
    "paper_link",
    "sort",
    "pdf_path",
]


@dataclass
class AuditRecord:
    kind: str
    status: str
    title: str
    venue: str
    path: str
    observed: str
    similarity: float
    reason: str
    line: int | None = None


def norm_title(text: str) -> str:
    text = str(text or "").lower().replace("&", " and ")
    text = re.sub(r"\barxiv\s*:\s*\S+", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    stopwords = {"a", "an", "the", "for", "with", "of", "and", "to", "in", "on"}
    return " ".join(token for token in text.split() if token not in stopwords)


def title_similarity(left: str, right: str) -> float:
    left_key = norm_title(left)
    right_key = norm_title(right)
    if not left_key or not right_key:
        return 0.0
    return SequenceMatcher(None, left_key, right_key).ratio()


def token_contained(expected: str, observed: str) -> bool:
    expected_tokens = set(norm_title(expected).split())
    observed_tokens = set(norm_title(observed).split())
    if not expected_tokens or not observed_tokens:
        return False
    return len(expected_tokens & observed_tokens) / max(1, len(expected_tokens)) >= 0.72


def resolve_path(raw: str) -> Path:
    path = Path(str(raw or "").strip())
    if not path.is_absolute():
        path = ROOT / path
    return path


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def pdf_title_candidates(path: Path) -> list[str]:
    candidates: list[str] = []
    try:
        with fitz.open(path) as doc:
            metadata_title = re.sub(r"\s+", " ", str((doc.metadata or {}).get("title") or "")).strip()
            if metadata_title:
                candidates.append(metadata_title)
            if doc.page_count:
                text = doc.load_page(0).get_text("text") or ""
                full_page = re.sub(r"\s+", " ", text).strip()
                if full_page:
                    candidates.append(full_page[:3000])
                added = 0
                for raw_line in text.splitlines()[:50]:
                    line = re.sub(r"\s+", " ", raw_line).strip()
                    if len(line) >= 12 and re.search(r"[A-Za-z]", line):
                        candidates.append(line)
                        added += 1
                        if added >= 10:
                            break
    except Exception:
        return candidates
    out: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        key = norm_title(item)
        if key and key not in seen:
            seen.add(key)
            out.append(item)
    return out


def best_title_match(expected: str, candidates: list[str]) -> tuple[bool, str, float]:
    if not expected or not candidates:
        return True, "", 0.0
    scored = sorted(
        ((candidate, title_similarity(expected, candidate), token_contained(expected, candidate)) for candidate in candidates),
        key=lambda item: item[1],
        reverse=True,
    )
    if any(score >= 0.62 or contained for _, score, contained in scored):
        candidate, score, _ = scored[0]
        return True, candidate, round(score, 4)
    candidate, score, _ = scored[0]
    return False, candidate, round(score, 4)


def read_rows() -> tuple[list[dict[str, str]], list[str]]:
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_FIELDS:
            raise SystemExit(f"Unexpected paper_list header: {reader.fieldnames}")
        return [dict(row) for row in reader], list(reader.fieldnames)


def write_rows(rows: list[dict[str, str]], fieldnames: list[str]) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = PAPER_LIST.with_name(f"{PAPER_LIST.name}.bak_{timestamp}")
    shutil.copy2(PAPER_LIST, backup)
    tmp = PAPER_LIST.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(PAPER_LIST)
    return backup


def row_in_scope(row: dict[str, str], *, since_ts: float) -> bool:
    venue = str(row.get("venue") or "").upper()
    if "SIGGRAPH" not in venue:
        return False
    state = str(row.get("state") or "")
    pdf_raw = str(row.get("pdf_path") or "")
    if state == "Downloaded":
        return True
    if not pdf_raw:
        return False
    path = resolve_path(pdf_raw)
    try:
        return path.exists() and path.stat().st_mtime >= since_ts
    except OSError:
        return False


def audit_pdfs(rows: list[dict[str, str]], *, since_ts: float) -> list[AuditRecord]:
    records: list[AuditRecord] = []
    for idx, row in enumerate(rows, start=2):
        if not row_in_scope(row, since_ts=since_ts):
            continue
        title = str(row.get("paper_title") or "").strip()
        venue = str(row.get("venue") or "").strip()
        raw_path = str(row.get("pdf_path") or "").strip()
        if not raw_path:
            records.append(AuditRecord("pdf", "missing", title, venue, "", "", 0.0, "missing_pdf_path", idx))
            continue
        path = resolve_path(raw_path)
        if not path.exists():
            records.append(AuditRecord("pdf", "missing", title, venue, rel(path), "", 0.0, "missing_file", idx))
            continue
        candidates = pdf_title_candidates(path)
        ok, observed, similarity = best_title_match(title, candidates)
        records.append(AuditRecord(
            "pdf",
            "ok" if ok else "mismatch",
            title,
            venue,
            rel(path),
            observed,
            similarity,
            "title_match" if ok else "title_mismatch",
            idx,
        ))
    return records


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    try:
        return yaml.safe_load(text.split("---", 2)[1]) or {}
    except Exception:
        return {}


def audit_markdown_notes(*, since_ts: float) -> list[AuditRecord]:
    records: list[AuditRecord] = []
    for note in sorted((ROOT / "obsidian-vault" / "analysis").glob("*SIGGRAPH*/*.md")):
        try:
            if note.stat().st_mtime < since_ts:
                continue
        except OSError:
            continue
        text = note.read_text(encoding="utf-8", errors="ignore")
        fm = parse_frontmatter(text)
        title = str(fm.get("title") or note.stem.replace("_", " ")).strip()
        venue = str(fm.get("venue") or note.parent.name).strip()
        pdf_ref = str(fm.get("pdf_ref") or "").strip()
        if not pdf_ref:
            records.append(AuditRecord("md", "missing", title, venue, rel(note), "", 0.0, "missing_pdf_ref"))
            continue
        pdf_path = resolve_path(pdf_ref.removeprefix("obsidian-vault/"))
        if not pdf_path.exists():
            pdf_path = ROOT / "obsidian-vault" / pdf_ref
        if not pdf_path.exists():
            records.append(AuditRecord("md", "missing", title, venue, rel(note), rel(pdf_path), 0.0, "missing_pdf_file"))
            continue
        ok, observed, similarity = best_title_match(title, pdf_title_candidates(pdf_path))
        records.append(AuditRecord(
            "md",
            "ok" if ok else "mismatch",
            title,
            venue,
            rel(note),
            observed,
            similarity,
            "title_match" if ok else "note_pdf_title_mismatch",
        ))
    return records


def quarantine_pdf(path: Path) -> str:
    if not path.exists():
        return ""
    target = QUARANTINE_ROOT / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") / rel(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(target))
    return rel(target)


def apply_pdf_updates(rows: list[dict[str, str]], records: list[AuditRecord], *, quarantine: bool) -> dict[str, Any]:
    by_line = {record.line: record for record in records if record.kind == "pdf" and record.status == "mismatch" and record.line}
    updates: list[dict[str, Any]] = []
    for idx, row in enumerate(rows, start=2):
        record = by_line.get(idx)
        if not record:
            continue
        old_path = resolve_path(record.path)
        quarantine_path = quarantine_pdf(old_path) if quarantine else ""
        old_state = row.get("state", "")
        if old_state in {"Downloaded", "checked"}:
            row["state"] = "Wait"
        row["pdf_path"] = ""
        updates.append({
            "line": idx,
            "title": row.get("paper_title", ""),
            "old_state": old_state,
            "new_state": row.get("state", ""),
            "old_pdf_path": record.path,
            "quarantine_path": quarantine_path,
            "observed": record.observed,
        })
    return {"updated_rows": len(updates), "updates": updates}


def write_report(records: list[AuditRecord], summary: dict[str, Any], *, label: str) -> tuple[Path, Path]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    json_path = REPORT_DIR / f"{label}_{timestamp}.json"
    csv_path = REPORT_DIR / f"{label}_{timestamp}.csv"
    payload = {"summary": summary, "records": [asdict(record) for record in records]}
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(AuditRecord("", "", "", "", "", "", 0.0, "")).keys()))
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))
    return json_path, csv_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", default="2026-06-19", help="Audit notes/PDFs modified on or after this date.")
    parser.add_argument("--mode", choices=["pdf", "md", "both"], default="both")
    parser.add_argument("--write-updates", action="store_true", help="Update paper_list rows for mismatched PDFs.")
    parser.add_argument("--no-quarantine", dest="quarantine", action="store_false", help="Do not move mismatched PDF files.")
    parser.set_defaults(quarantine=True)
    args = parser.parse_args()

    since_dt = datetime.fromisoformat(args.since).replace(tzinfo=timezone.utc)
    rows, fieldnames = read_rows()
    records: list[AuditRecord] = []
    if args.mode in {"pdf", "both"}:
        records.extend(audit_pdfs(rows, since_ts=since_dt.timestamp()))
    if args.mode in {"md", "both"}:
        records.extend(audit_markdown_notes(since_ts=since_dt.timestamp()))

    update_info: dict[str, Any] = {}
    backup = ""
    if args.write_updates:
        update_info = apply_pdf_updates(rows, records, quarantine=args.quarantine)
        if update_info.get("updated_rows"):
            backup = rel(write_rows(rows, fieldnames))

    summary = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "since": args.since,
        "mode": args.mode,
        "total": len(records),
        "ok": sum(1 for item in records if item.status == "ok"),
        "mismatch": sum(1 for item in records if item.status == "mismatch"),
        "missing": sum(1 for item in records if item.status == "missing"),
        "paper_list_backup": backup,
        **update_info,
    }
    json_path, csv_path = write_report(records, summary, label="siggraph_pdf_md_consistency")
    print(json.dumps({"json_report": rel(json_path), "csv_report": rel(csv_path), **summary}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
