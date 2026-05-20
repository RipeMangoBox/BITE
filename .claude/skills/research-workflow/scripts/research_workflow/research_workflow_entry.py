#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List


REPO_ROOT = Path(__file__).resolve().parents[5]
PAPER_ANALYSIS = REPO_ROOT / "obsidian-vault/analysis"
PAPER_COLLECTION = REPO_ROOT / "obsidian-vault/index"
PAPER_PDFS = REPO_ROOT / "obsidian-vault/paperPDFs"

STAGES = ["collect", "download", "analyze", "build", "query", "ideate"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Unified research workflow entry (advisor): detect/choose stage and print suggested next commands."
    )
    p.add_argument("--stage", choices=STAGES + ["auto"], default="auto")
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


def has_analysis_notes() -> bool:
    if not PAPER_ANALYSIS.exists():
        return False
    return any(PAPER_ANALYSIS.rglob("*.md"))


def detect_stage(preferred_log: Path | None) -> str:
    logs = discover_logs()
    target_logs = [preferred_log] if preferred_log else logs
    target_logs = [p for p in target_logs if p and p.exists()]

    if not target_logs:
        if has_analysis_notes():
            return "query"
        return "collect"

    total_wait = sum(count_wait_entries(p) for p in target_logs)
    if total_wait > 0:
        return "download"

    # query can run directly from obsidian-vault/analysis; build is optional
    return "query"


def stage_spec(stage: str, mode: str, log_hint: str) -> Dict[str, object]:
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
            "outputs": "obsidian-vault/index/README.md, _AllPapers.md, by_topic/, by_method/, by_dataset/, by_venue/, by_year/ (statistics/navigation pages)",
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
    return {
        "inputs": "research question",
        "outputs": "obsidian-vault/ideas/YYYY-MM-DD_<topic>.md",
        "commands": [
            "Use /research-brainstorm-from-kb",
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
    lines.append("- Stage set: collect / download / analyze / build / query / ideate")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    log_path = resolve_log_file(args.log_file)
    log_hint = args.log_file or (log_path.as_posix() if log_path else "")

    stage = args.stage
    if stage == "auto":
        stage = detect_stage(log_path)

    print(render(stage, args.mode, log_hint))


if __name__ == "__main__":
    main()
