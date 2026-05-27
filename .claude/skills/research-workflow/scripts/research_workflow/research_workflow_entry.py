#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


REPO_ROOT = Path(__file__).resolve().parents[5]
PAPER_ANALYSIS = REPO_ROOT / "obsidian-vault/analysis"
PAPER_COLLECTION = REPO_ROOT / "obsidian-vault/index"
PAPER_PDFS = REPO_ROOT / "obsidian-vault/paperPDFs"
PAPER_LIST_CSV = REPO_ROOT / "obsidian-vault/paper_list.csv"

STAGES = [
    "import-local-pdfs",
    "collect",
    "download",
    "analyze",
    "build",
    "query",
    "ideate",
    "focus",
    "review",
    "audit",
    "export",
]
STAGE_ALIASES = {
    "import": "import-local-pdfs",
    "import-local": "import-local-pdfs",
    "local-pdfs": "import-local-pdfs",
}
NON_PAPER_NOTE_NAMES = {"readme.md", "_index.md"}
NON_PAPER_NOTE_PREFIXES = ("quality_report_",)
NON_PAPER_NOTE_DIRS = {"test", "_test", "tests", "_tests"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Unified research workflow entry (advisor): detect/choose stage and print suggested next commands."
    )
    p.add_argument("--stage", choices=STAGES + sorted(STAGE_ALIASES) + ["auto"], default="auto")
    p.add_argument("--log-file", default="", help="Optional triage/log file or paper_list.csv path")
    p.add_argument("--mode", choices=["brief", "deep"], default="brief", help="Query mode hint")
    return p.parse_args()


def resolve_log_file(log_file: str) -> Path | None:
    if not log_file:
        return None
    p = Path(log_file)
    if not p.is_absolute():
        p = REPO_ROOT / p
    return p if p.exists() else None


def count_wait_entries(log_path: Path) -> int:
    if log_path.suffix.lower() == ".csv":
        return paper_list_summary(log_path)[0].get("wait", 0)

    text = log_path.read_text(encoding="utf-8", errors="ignore")
    c = 0
    for line in text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        parts = [x.strip() for x in line.split("|")]
        if parts and parts[0].lower() == "wait":
            c += 1
    return c


def discover_logs() -> List[Path]:
    if not PAPER_ANALYSIS.exists():
        return []
    logs: List[Path] = []
    for p in PAPER_ANALYSIS.glob("*.txt"):
        if p.name.startswith("missing") or p.name.startswith("paper_analysis_check_task"):
            continue
        logs.append(p)
    return sorted(logs, key=lambda x: x.name.lower())


def paper_list_summary(csv_path: Path = PAPER_LIST_CSV) -> Tuple[Counter, int, int]:
    states: Counter = Counter()
    total = 0
    rows_with_pdf = 0
    if not csv_path.exists():
        return states, total, rows_with_pdf

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = [name or "" for name in (reader.fieldnames or [])]
        lower_fields = {x.strip().lower(): x for x in fieldnames}
        state_field = lower_fields.get("state") or lower_fields.get("status") or ""
        pdf_field = next((x for x in fieldnames if x.strip().lower() in {"pdf_ref", "pdf", "pdf_path"}), "")
        for row in reader:
            if not any(str(v or "").strip() for v in row.values()):
                continue
            total += 1
            state = unicodedata.normalize("NFKC", (row.get(state_field, "") if state_field else "")).strip().lower()
            state = state or "unknown"
            states[state] += 1
            if pdf_field and row.get(pdf_field, "").strip():
                rows_with_pdf += 1
    return states, total, rows_with_pdf


def has_local_pdfs() -> bool:
    return PAPER_PDFS.exists() and any(PAPER_PDFS.rglob("*.pdf"))


def read_prefix(path: Path, chars: int = 16000) -> str:
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        return f.read(chars)


def is_analysis_note(md_path: Path) -> bool:
    relative_parts = md_path.relative_to(PAPER_ANALYSIS).parts
    if any(part.lower() in NON_PAPER_NOTE_DIRS for part in relative_parts[:-1]):
        return False
    name = md_path.name.lower()
    if name in NON_PAPER_NOTE_NAMES:
        return False
    if any(name.startswith(prefix) for prefix in NON_PAPER_NOTE_PREFIXES):
        return False

    text = read_prefix(md_path)
    markers = (
        r"^type:\s*paper\b",
        r"^pdf_ref:\s*\S+",
        r"^core_operator:\s*\S+",
        r"^primary_logic:\s*\S+",
        r"^venue:\s*\S+",
        r"^year:\s*(?:19|20)\d{2}\b",
        r"^###\s+原文PDF\b",
        r"^\|\s*Method\s*\|",
        r"^\|\s*Dataset\s*\|",
    )
    if any(re.search(pattern, text, re.IGNORECASE | re.MULTILINE) for pattern in markers):
        return True

    return len(relative_parts) > 1 and bool(re.search(r"(?:19|20)\d{2}", "/".join(relative_parts[:-1])))


def count_analysis_notes() -> int:
    if not PAPER_ANALYSIS.exists():
        return 0
    return sum(1 for path in PAPER_ANALYSIS.rglob("*.md") if is_analysis_note(path))


def detect_stage(preferred_log: Path | None) -> str:
    states, total_rows, rows_with_pdf = paper_list_summary(PAPER_LIST_CSV)
    analysis_count = count_analysis_notes()
    if preferred_log and preferred_log.suffix.lower() == ".csv":
        states, total_rows, rows_with_pdf = paper_list_summary(preferred_log)

    if states.get("wait", 0) > 0:
        return "download"
    if states.get("downloaded", 0) > 0:
        return "analyze"
    if states.get("checked", 0) > 0:
        return "query"
    if analysis_count > 0:
        return "query"
    if total_rows > 0:
        return "analyze" if rows_with_pdf > 0 else "download"
    if has_local_pdfs():
        return "import-local-pdfs"

    logs = discover_logs()
    target_logs = [preferred_log] if preferred_log else logs
    target_logs = [p for p in target_logs if p and p.exists()]

    if not target_logs:
        return "collect"

    total_wait = sum(count_wait_entries(p) for p in target_logs)
    if total_wait > 0:
        return "download"

    # query can run directly from obsidian-vault/analysis; build is optional
    return "query"


def stage_spec(stage: str, mode: str, log_hint: str) -> Dict[str, object]:
    stage = STAGE_ALIASES.get(stage, stage)
    if stage == "import-local-pdfs":
        return {
            "inputs": "PDF folder path + optional category/sort hint + venue/year hint",
            "outputs": "obsidian-vault/paperPDFs/** + registered obsidian-vault/paper_list.csv rows",
            "commands": [
                "Ask for the source PDF folder and register/copy PDFs into the local vault layout",
                "Use the paper_list.csv state convention so already-local PDFs can enter analyze as Downloaded",
            ],
            "next": "analyze",
        }
    if stage == "collect":
        return {
            "inputs": "URLs or GitHub repo URL + venue/year + include/exclude",
            "outputs": "obsidian-vault/paper_list.csv candidate rows",
            "commands": [
                "Use /papers-collect-from-web or /papers-collect-from-github-repo",
            ],
            "next": "download",
        }
    if stage == "download":
        log = log_hint or "<triage-log>.txt"
        return {
            "inputs": "triage/log file (contains Wait entries)",
            "outputs": "obsidian-vault/paperPDFs/** + log state updates",
            "commands": [
                "Use /papers-download-from-list",
                f'Or run: python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/download_wait_papers.py" --log "{log}" --out-root "obsidian-vault/paperPDFs"',
            ],
            "next": "analyze",
        }
    if stage == "analyze":
        return {
            "inputs": "PDF path, existing MinerU output directory, or Downloaded queue",
            "outputs": "_private/local_analysis_runs/** + obsidian-vault/analysis/**/*.md",
            "commands": [
                'Default single-paper chain: python3 "scripts/run_local_paper_analysis.py" --pdf "<pdf>" --conf-year "<Venue_Year>" --export-vault',
                'Reuse existing MinerU output: python3 "scripts/run_local_paper_analysis.py" --mineru-output "<mineru_output_dir>" --paper-pdf "<pdf>" --conf-year "<Venue_Year>" --export-vault',
                'Downloaded queue: python3 "scripts/run_paper_list_analysis.py" --source "obsidian-vault/paper_list.csv" --state Downloaded --limit 25',
                "Use /paper-report when the user asks for a deep report or formula derivation",
                "Note: after analyze you can go directly to query; run build only if statistics/navigation pages are needed",
            ],
            "next": "query (or optional build)",
        }
    if stage == "build":
        return {
            "inputs": "obsidian-vault/analysis already has structured markdown notes",
            "outputs": "obsidian-vault/index/index.jsonl, _Index.md, _AllPapers.md, by_topic/, by_method/, by_dataset/, by_venue/, by_year/ (statistics/navigation pages)",
            "commands": [
                "Use /papers-build-index",
                'Or run: python3 ".claude/skills/papers-build-index/scripts/build_paper_index.py"',
            ],
            "next": "query",
        }
    if stage == "query":
        return {
            "inputs": "task description/keywords (optional changed files)",
            "outputs": f"retrieval results ({mode}) + paper paths/analysis paths/PDF suggestions",
            "commands": [
                "Use /papers-query-knowledge-base",
                f"Or use /code-context-paper-retrieval (mode={mode})",
            ],
            "next": "ideate",
        }
    if stage == "ideate":
        return {
            "inputs": "research problem statement",
            "outputs": "obsidian-vault/ideas/YYYY-MM-DD_<topic>.md",
            "commands": [
                "Use /research-brainstorm-from-kb",
            ],
            "next": "focus",
        }
    if stage == "focus":
        return {
            "inputs": "initial idea + goal/preferences/scope constraints",
            "outputs": "focused plan or updated obsidian-vault/ideas/** note",
            "commands": [
                "Use /idea-focus-coach",
            ],
            "next": "review",
        }
    if stage == "review":
        return {
            "inputs": "idea, roadmap, or full paper draft",
            "outputs": "strict reviewer diagnostics + repair paths, usually under obsidian-vault/ideas/**",
            "commands": [
                "Use /reviewer-stress-test",
            ],
            "next": "focus (if repair is needed) or export",
        }
    if stage == "audit":
        return {
            "inputs": "no extra input; scans obsidian-vault/analysis",
            "outputs": "obsidian-vault/batches/reports/quality_report_*.md",
            "commands": [
                "Use /papers-audit-metadata-consistency",
            ],
            "next": "fix reported issues, then build or query",
        }
    return {
        "inputs": "note path to export",
        "outputs": "shareable Markdown note with internal knowledge-base traces removed",
        "commands": [
            "Use /notes-export-share-version",
        ],
        "next": "(end)",
    }


def render(stage: str, mode: str, log_hint: str) -> str:
    spec = stage_spec(stage, mode, log_hint)
    lines: List[str] = []
    lines.append("## Research Workflow Entry")
    lines.append("")
    lines.append(f"- Current stage: {stage}")
    lines.append(f"- Input requirements: {spec['inputs']}")
    lines.append(f"- Output paths: {spec['outputs']}")
    lines.append("")
    lines.append("### Recommended actions")
    for i, cmd in enumerate(spec["commands"], start=1):
        lines.append(f"{i}. {cmd}")
    lines.append("")
    lines.append(f"- Suggested next stage: {spec['next']}")
    lines.append("- Stage set: " + " / ".join(STAGES))
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    log_path = resolve_log_file(args.log_file)
    log_hint = args.log_file or (log_path.as_posix() if log_path else "")

    stage = args.stage
    if stage == "auto":
        stage = detect_stage(log_path)
    else:
        stage = STAGE_ALIASES.get(stage, stage)

    print(render(stage, args.mode, log_hint))


if __name__ == "__main__":
    main()
