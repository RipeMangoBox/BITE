#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = REPO_ROOT / "obsidian-vault" / "analysis"

REQUIRED_FRONTMATTER = [
    "title",
    "type",
    "paper_level",
    "venue",
    "year",
    "pdf_ref",
    "aliases",
    "tags",
    "core_operator",
    "primary_logic",
    "claims",
]

REQUIRED_SECTIONS = [
    "概述",
    "背景与动机",
    "核心创新",
    "整体框架",
    "核心模块与公式推导",
    "实验与分析",
    "方法谱系与知识库定位",
    "原文 PDF",
]

DISALLOWED_FRONTMATTER = ["category", "modalities", "frontier"]
PLACEHOLDER_PATTERNS = ["待人工复核", "{{FIG:", "FIG:", "[TODO]"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit ResearchFlow formal analysis-chain note exports.")
    parser.add_argument("--analysis-dir", default=str(ANALYSIS_DIR))
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--out-json", default="")
    parser.add_argument("--out-md", default="")
    return parser.parse_args()


def repo_rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def is_analysis_note(path: Path, analysis_dir: Path) -> bool:
    if path.name.startswith("quality_report_"):
        return False
    if path.name == "README.md":
        return False
    rel = path.relative_to(analysis_dir)
    if len(rel.parts) not in {2, 3}:
        return False
    if any(part.startswith(".") for part in rel.parts):
        return False
    if rel.parts[0].lower() in {"processing", "emergentmind_paper_analysis"}:
        return False
    return bool(re.search(r"\d{4}", "/".join(rel.parts[:-1])))


def split_frontmatter(text: str) -> tuple[list[str], str, bool]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text, False
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1 :]), True
    return [], text, False


def parse_frontmatter(lines: list[str]) -> dict[str, Any]:
    data: dict[str, Any] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            index += 1
            continue
        key = match.group(1)
        value = (match.group(2) or "").strip()
        if value == "" and index + 1 < len(lines) and lines[index + 1].lstrip().startswith("- "):
            items: list[str] = []
            index += 1
            while index < len(lines) and lines[index].lstrip().startswith("- "):
                items.append(lines[index].lstrip()[2:].strip().strip("\"'"))
                index += 1
            data[key] = items
            continue
        if value in {"|", ">"}:
            block: list[str] = []
            index += 1
            while index < len(lines):
                item = lines[index]
                if item.startswith("  "):
                    block.append(item[2:])
                    index += 1
                elif item.strip() == "":
                    block.append("")
                    index += 1
                else:
                    break
            data[key] = "\n".join(block).strip()
            continue
        data[key] = value.strip("\"'")
        index += 1
    return data


def heading_titles(body: str) -> set[str]:
    return {match.group(1).strip() for match in re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)}


def table_rows_with_aliased_wikilinks(text: str) -> list[int]:
    rows: list[int] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and re.search(r"\[\[[^\]]+\|[^\]]+\]\]", stripped):
            rows.append(line_no)
    return rows


def dangling_numeric_refs(text: str) -> list[str]:
    scan = re.sub(r"`[^`\n]*`", "", text)
    scan = re.sub(r"\$\$.*?\$\$", "", scan, flags=re.DOTALL)
    scan = re.sub(r"\$[^$\n]*\$", "", scan)
    refs = sorted(
        set(match.group(1) for match in re.finditer(r"(?<![\w}'!\]])\[(\d{1,3})\]", scan)),
        key=lambda value: int(value),
    )
    if not refs:
        return []
    defined = set(re.findall(r"^\s*\[(\d{1,3})\]:", scan, flags=re.MULTILINE))
    bibliography = set(re.findall(r"^\s*\[(\d{1,3})\]\s+", scan, flags=re.MULTILINE))
    return [ref for ref in refs if ref not in defined and ref not in bibliography]


def file_exists_from_ref(pdf_ref: str) -> bool:
    if not pdf_ref:
        return False
    value = pdf_ref.strip().strip("\"'")
    candidates = [REPO_ROOT / value]
    if value.startswith("obsidian-vault/"):
        candidates.append(REPO_ROOT / value.removeprefix("obsidian-vault/"))
    else:
        candidates.append(REPO_ROOT / "obsidian-vault" / value)
    return any(path.exists() for path in candidates)


def normalized_title(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip("\"'")).lower()


def check_note(path: Path, analysis_dir: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    fm_lines, body, has_frontmatter = split_frontmatter(text)
    fm = parse_frontmatter(fm_lines) if has_frontmatter else {}
    failures: list[str] = []
    warnings: list[str] = []

    missing_frontmatter = [key for key in REQUIRED_FRONTMATTER if key not in fm]
    if not has_frontmatter:
        failures.append("missing YAML frontmatter")
    elif missing_frontmatter:
        failures.append("missing frontmatter keys: " + ", ".join(missing_frontmatter))

    disallowed = [key for key in DISALLOWED_FRONTMATTER if key in fm]
    if disallowed:
        failures.append("disallowed frontmatter keys: " + ", ".join(disallowed))

    if str(fm.get("type", "")).strip("\"'") != "paper":
        failures.append("frontmatter type is not paper")

    year = str(fm.get("year", "")).strip("\"'")
    if not re.fullmatch(r"\d{4}", year):
        failures.append("invalid or missing year")

    title = str(fm.get("title", "")).strip()
    h1_match = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
    if not h1_match:
        failures.append("missing H1 title")
    elif title and normalized_title(title) not in normalized_title(h1_match.group(1)):
        warnings.append("H1 title does not contain frontmatter title")

    aliases = fm.get("aliases")
    if not isinstance(aliases, list) or not aliases:
        failures.append("aliases must be a non-empty YAML list")
    claims = fm.get("claims")
    if not isinstance(claims, list) or not claims:
        failures.append("claims must be a non-empty YAML list")
    tags = fm.get("tags")
    if not isinstance(tags, list) or not tags:
        failures.append("tags must be a non-empty YAML list")

    for scalar_key in ["core_operator", "primary_logic"]:
        value = str(fm.get(scalar_key, "")).strip()
        if len(value) < 20:
            failures.append(f"{scalar_key} is empty or too short")

    pdf_ref = str(fm.get("pdf_ref", "")).strip()
    if not pdf_ref:
        failures.append("missing pdf_ref")
    elif not file_exists_from_ref(pdf_ref):
        failures.append(f"pdf_ref target missing: {pdf_ref}")

    pdf_embed_ref = pdf_ref.strip().strip("\"'")
    if pdf_ref and f"![[{pdf_embed_ref}]]" not in text:
        failures.append("missing matching PDF embed")

    headings = heading_titles(body)
    missing_sections = [section for section in REQUIRED_SECTIONS if section not in headings]
    if missing_sections:
        failures.append("missing required sections: " + ", ".join(missing_sections))

    if "> [!tip] 核心洞察" not in text:
        failures.append("missing core-insight callout")
    if "| 字段 | 内容 |" not in text:
        failures.append("missing metadata info table")

    placeholder_hits = [pattern for pattern in PLACEHOLDER_PATTERNS if pattern in text]
    if placeholder_hits:
        failures.append("placeholder or unresolved marker remains: " + ", ".join(placeholder_hits))

    if re.search(r"!\[[^\]]*\]\((?:\.\./\.\./)?assets/[^)]+\)", text):
        failures.append("legacy markdown image link under assets")
    if re.search(r"!\[\[\.\./\.\./assets/[^\]]+\]\]", text):
        failures.append("legacy relative asset wikilink")

    table_alias_lines = table_rows_with_aliased_wikilinks(text)
    if table_alias_lines:
        failures.append("aliased wikilinks inside markdown table rows: " + ", ".join(map(str, table_alias_lines[:8])))

    dangling_refs = dangling_numeric_refs(text)
    if dangling_refs:
        failures.append("dangling numeric references: " + ", ".join(dangling_refs[:12]))

    if len(text.strip()) < 3000:
        failures.append(f"note appears truncated: {len(text.strip())} chars")

    return {
        "path": repo_rel(path),
        "ok": not failures,
        "failures": failures,
        "warnings": warnings,
        "title": title.strip("\"'"),
        "year": year,
        "pdf_ref": pdf_ref.strip("\"'"),
        "chars": len(text),
    }


def load_notes(analysis_dir: Path) -> list[Path]:
    return [
        path
        for path in sorted(analysis_dir.rglob("*.md"))
        if is_analysis_note(path, analysis_dir)
    ]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Analysis Chain Audit Shard Report",
        "",
        f"- generated: {payload['generated']}",
        f"- shard: {payload['shard_index']} / {payload['shard_count']}",
        f"- checked_notes: {summary['checked_notes']}",
        f"- passed: {summary['passed']}",
        f"- failed: {summary['failed']}",
        f"- warnings: {summary['warnings']}",
        "",
        "## Failure Reasons",
        "",
    ]
    if not summary["failure_reasons"]:
        lines.append("- none")
    else:
        for reason, count in summary["failure_reasons"]:
            lines.append(f"- {count}: {reason}")
    lines.extend(["", "## Failed Notes", ""])
    failed = [item for item in payload["results"] if not item["ok"]]
    if not failed:
        lines.append("- none")
    else:
        for item in failed:
            lines.append(f"- `{item['path']}`")
            for reason in item["failures"]:
                lines.append(f"  - {reason}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    analysis_dir = Path(args.analysis_dir)
    if not analysis_dir.is_absolute():
        analysis_dir = REPO_ROOT / analysis_dir
    if args.shard_count < 1:
        raise SystemExit("--shard-count must be >= 1")
    if args.shard_index < 0 or args.shard_index >= args.shard_count:
        raise SystemExit("--shard-index must be in [0, shard-count)")

    notes = load_notes(analysis_dir)
    shard_notes = [path for index, path in enumerate(notes) if index % args.shard_count == args.shard_index]
    results = [check_note(path, analysis_dir) for path in shard_notes]
    failure_reasons = Counter(reason for item in results for reason in item["failures"])
    payload = {
        "generated": datetime.now().isoformat(timespec="minutes"),
        "analysis_dir": repo_rel(analysis_dir),
        "shard_index": args.shard_index,
        "shard_count": args.shard_count,
        "total_candidate_notes": len(notes),
        "summary": {
            "checked_notes": len(results),
            "passed": sum(1 for item in results if item["ok"]),
            "failed": sum(1 for item in results if not item["ok"]),
            "warnings": sum(len(item["warnings"]) for item in results),
            "failure_reasons": failure_reasons.most_common(),
        },
        "results": results,
    }

    if args.out_json:
        write_json(Path(args.out_json), payload)
    if args.out_md:
        out_md = Path(args.out_md)
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(render_markdown(payload), encoding="utf-8")

    print(
        f"[OK] shard {args.shard_index}/{args.shard_count}: "
        f"{payload['summary']['passed']} passed, {payload['summary']['failed']} failed, "
        f"{len(results)} checked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
