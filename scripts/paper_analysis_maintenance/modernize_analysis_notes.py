#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = REPO_ROOT / "obsidian-vault" / "analysis"
PAPER_LIST = REPO_ROOT / "obsidian-vault" / "paper_list.csv"
DEFAULT_REPORT_DIR = REPO_ROOT / "_private" / "BITE_versions" / "v06"


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
LINKS_ROW_RE = re.compile(r"^(\|\s*Links\s*\|\s*)(.*?)(\s*\|\s*)$", re.MULTILINE)
IMAGE_RE = re.compile(r"^!\[\[assets/figures/papers/[^\]]+\]\]\s*$")
ITALIC_CAPTION_RE = re.compile(r"^\*(?:Figure|Fig\.?|Table)\s+[^:]{0,80}:.*\*\s*$", re.IGNORECASE)


@dataclass
class PaperRow:
    title: str
    paper_link: str
    project_link: str
    pdf_path: str


@dataclass
class ImageBlock:
    start: int
    end: int
    embed: str
    caption: str
    section: str
    index: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Modernize old BITE analysis notes with deterministic fixes.")
    parser.add_argument("--analysis-dir", default=str(ANALYSIS_DIR))
    parser.add_argument("--paper-list", default=str(PAPER_LIST))
    parser.add_argument("--cutoff", default="2026-06-24", help="Only touch notes with mtime before this date.")
    parser.add_argument("--max-images", type=int, default=6)
    parser.add_argument("--max-caption-chars", type=int, default=360)
    parser.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR))
    parser.add_argument("--write", action="store_true", help="Apply fixes. Default is dry-run.")
    return parser.parse_args()


def normalize_title(value: str) -> str:
    value = value.lower().replace("_", " ").replace("-", " ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def load_paper_rows(path: Path) -> tuple[dict[str, PaperRow], dict[str, PaperRow]]:
    by_title: dict[str, PaperRow] = {}
    by_pdf_stem: dict[str, PaperRow] = {}
    if not path.exists():
        return by_title, by_pdf_stem
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            item = PaperRow(
                title=(row.get("paper_title") or "").strip(),
                paper_link=(row.get("paper_link") or "").strip(),
                project_link=(row.get("project_link_or_github_link") or "").strip(),
                pdf_path=(row.get("pdf_path") or "").strip(),
            )
            title_key = normalize_title(item.title)
            if title_key and title_key not in by_title:
                by_title[title_key] = item
            pdf_stem = Path(item.pdf_path).stem if item.pdf_path else ""
            stem_key = normalize_title(pdf_stem)
            if stem_key and stem_key not in by_pdf_stem:
                by_pdf_stem[stem_key] = item
    return by_title, by_pdf_stem


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, text
    data: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            data[match.group(1)] = match.group(2).strip().strip("\"'")
    return data, "\n".join(lines[end + 1 :])


def h1_title(body: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def find_paper_row(path: Path, text: str, by_title: dict[str, PaperRow], by_pdf_stem: dict[str, PaperRow]) -> PaperRow | None:
    fm, body = split_frontmatter(text)
    candidates = [
        path.stem,
        fm.get("title", ""),
        h1_title(body),
    ]
    for value in candidates:
        key = normalize_title(value)
        if key in by_pdf_stem:
            return by_pdf_stem[key]
        if key in by_title:
            return by_title[key]
    return None


def normalized_url(value: str) -> str:
    return value.strip().rstrip("/")


def is_paperish_label(label: str) -> bool:
    return label.strip().lower() in {"paper", "arxiv", "arxiv pdf", "pdf"}


def fix_links(text: str, row: PaperRow | None) -> tuple[str, dict[str, Any]]:
    info: dict[str, Any] = {
        "arxiv_labels_renamed": 0,
        "links_rows_rewritten": 0,
        "paper_arxiv_conflicts": [],
        "paper_list_link_used": False,
    }

    def rewrite_links_row(match: re.Match[str]) -> str:
        prefix, content, suffix = match.group(1), match.group(2), match.group(3)
        links = [(label.strip(), url.strip()) for label, url in LINK_RE.findall(content)]
        if not links:
            return match.group(0)

        paper_urls = [url for label, url in links if label.strip().lower() == "paper"]
        arxiv_urls = [url for label, url in links if label.strip().lower() == "arxiv"]
        csv_paper = row.paper_link if row and row.paper_link else ""
        if paper_urls and arxiv_urls:
            distinct = sorted({normalized_url(url) for url in paper_urls + arxiv_urls})
            if len(distinct) > 1:
                info["paper_arxiv_conflicts"].append({"paper": paper_urls[:3], "arxiv": arxiv_urls[:3]})

        paper_url = csv_paper or (paper_urls[0] if paper_urls else "") or (arxiv_urls[0] if arxiv_urls else "")
        if csv_paper:
            info["paper_list_link_used"] = True

        out: list[tuple[str, str]] = []
        seen_urls: set[str] = set()
        if paper_url:
            out.append(("paper", paper_url))
            seen_urls.add(normalized_url(paper_url))

        for label, url in links:
            if is_paperish_label(label):
                continue
            clean_label = label.strip()
            if clean_label.lower() in {"project", "code", "github"}:
                clean_label = "Code" if clean_label.lower() in {"code", "github"} else "Project"
            url_key = normalized_url(url)
            if not url or url_key in seen_urls:
                continue
            out.append((clean_label, url))
            seen_urls.add(url_key)

        rewritten = " · ".join(f"[{label}]({url})" for label, url in out)
        if rewritten != content:
            info["links_rows_rewritten"] += 1
        return f"{prefix}{rewritten}{suffix}"

    new_text = LINKS_ROW_RE.sub(rewrite_links_row, text)

    def rename_arxiv_label(match: re.Match[str]) -> str:
        label, url = match.group(1), match.group(2)
        if label.strip().lower() == "arxiv":
            info["arxiv_labels_renamed"] += 1
            return f"[paper]({url})"
        return match.group(0)

    new_text = LINK_RE.sub(rename_arxiv_label, new_text)
    return new_text, info


def current_section(line: str, section: str) -> str:
    match = re.match(r"^##\s+(.+?)\s*$", line)
    return match.group(1).strip() if match else section


def collect_image_blocks(lines: list[str]) -> list[ImageBlock]:
    blocks: list[ImageBlock] = []
    section = ""
    index = 0
    i = 0
    while i < len(lines):
        section = current_section(lines[i], section)
        if not IMAGE_RE.match(lines[i].strip()):
            i += 1
            continue
        start = i
        end = i + 1
        caption = ""
        if end < len(lines) and ITALIC_CAPTION_RE.match(lines[end].strip()):
            caption = lines[end]
            end += 1
        index += 1
        blocks.append(ImageBlock(start=start, end=end, embed=lines[i], caption=caption, section=section, index=index))
        i = end
    return blocks


def block_slot(block: ImageBlock) -> str:
    section = block.section
    caption = block.caption
    if "实验" in section or "发现" in section or "结果" in section or "Table" in caption:
        return "experiment"
    if "背景" in section or "动机" in section or "概要" in section or "概述" in section:
        return "motivation"
    if "方法" in section or "创新" in section or "框架" in section or "机理" in section or "模块" in section:
        return "method"
    return "other"


def selected_image_indices(blocks: list[ImageBlock], max_images: int) -> set[int]:
    if max_images <= 0 or len(blocks) <= max_images:
        return {block.index for block in blocks}
    quotas = {"motivation": 1, "method": 2, "experiment": 3}
    selected: list[int] = []
    for slot, quota in quotas.items():
        for block in blocks:
            if block.index in selected:
                continue
            if block_slot(block) == slot:
                selected.append(block.index)
                if sum(1 for idx in selected if block_slot(next(b for b in blocks if b.index == idx)) == slot) >= quota:
                    break
    for block in blocks:
        if len(selected) >= max_images:
            break
        if block.index not in selected:
            selected.append(block.index)
    return set(selected[:max_images])


def escape_caption_reserved_chars(line: str) -> str:
    parts = re.split(r"(`[^`\n]*`|\$[^$\n]*\$)", line)
    return "".join(
        part if part.startswith(("`", "$")) else re.sub(r"(?<!\\)<", r"\\<", part)
        for part in parts
    )


def compact_caption(line: str, max_chars: int) -> str:
    if max_chars <= 0 or len(line) <= max_chars:
        return line
    stripped = line.strip()
    if not (stripped.startswith("*") and stripped.endswith("*")):
        return line[:max_chars].rstrip() + "..."
    inner = stripped[1:-1]
    return "*" + inner[: max(0, max_chars - 5)].rstrip() + "...*"


def fix_images(text: str, max_images: int, max_caption_chars: int) -> tuple[str, dict[str, Any]]:
    lines = text.splitlines()
    blocks = collect_image_blocks(lines)
    keep = selected_image_indices(blocks, max_images)
    remove_lines: set[int] = set()
    captions_compacted = 0
    captions_escaped = 0
    block_by_start = {block.start: block for block in blocks}
    for block in blocks:
        if block.index not in keep:
            remove_lines.update(range(block.start, block.end))
            if block.end < len(lines) and not lines[block.end].strip():
                remove_lines.add(block.end)
            continue
        if block.caption:
            fixed = escape_caption_reserved_chars(block.caption)
            if fixed != block.caption:
                captions_escaped += 1
            compacted = compact_caption(fixed, max_caption_chars)
            if compacted != fixed:
                captions_compacted += 1
            lines[block.start + 1] = compacted

    if not remove_lines and not captions_compacted and not captions_escaped:
        return text, {
            "image_count_before": len(blocks),
            "image_count_after": len(blocks),
            "images_removed": 0,
            "captions_compacted": 0,
            "captions_escaped": 0,
        }

    out = [line for index, line in enumerate(lines) if index not in remove_lines]
    after_count = len([block for block in blocks if block.index in keep])
    return "\n".join(out), {
        "image_count_before": len(blocks),
        "image_count_after": after_count,
        "images_removed": len(blocks) - after_count,
        "captions_compacted": captions_compacted,
        "captions_escaped": captions_escaped,
        "removed_blocks": [
            {
                "index": block.index,
                "section": block.section,
                "caption": block.caption[:160],
            }
            for block in blocks
            if block.index not in keep
        ],
        "unused": bool(block_by_start) and False,
    }


def candidate_notes(analysis_dir: Path, cutoff: datetime) -> list[Path]:
    cutoff_ts = cutoff.timestamp()
    return [
        path
        for path in sorted(analysis_dir.glob("*/*.md"))
        if path.is_file() and path.stat().st_mtime < cutoff_ts
    ]


def main() -> int:
    args = parse_args()
    analysis_dir = Path(args.analysis_dir)
    paper_list = Path(args.paper_list)
    cutoff = datetime.fromisoformat(args.cutoff)
    by_title, by_pdf_stem = load_paper_rows(paper_list)
    notes = candidate_notes(analysis_dir, cutoff)

    changed: list[dict[str, Any]] = []
    unchanged = 0
    for path in notes:
        original = path.read_text(encoding="utf-8", errors="ignore")
        row = find_paper_row(path, original, by_title, by_pdf_stem)
        text, link_info = fix_links(original, row)
        text, image_info = fix_images(text, args.max_images, args.max_caption_chars)
        if text == original:
            unchanged += 1
            continue
        item = {
            "path": path.relative_to(REPO_ROOT).as_posix(),
            "paper_list_match": row.title if row else "",
            "link_info": link_info,
            "image_info": image_info,
        }
        changed.append(item)
        if args.write:
            path.write_text(text + ("\n" if original.endswith("\n") else ""), encoding="utf-8")

    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    payload = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "mode": "write" if args.write else "dry-run",
        "cutoff": args.cutoff,
        "checked_notes": len(notes),
        "changed_notes": len(changed),
        "unchanged_notes": unchanged,
        "max_images": args.max_images,
        "max_caption_chars": args.max_caption_chars,
        "summary": {
            "links_rows_rewritten": sum(item["link_info"]["links_rows_rewritten"] for item in changed),
            "arxiv_labels_renamed": sum(item["link_info"]["arxiv_labels_renamed"] for item in changed),
            "paper_arxiv_conflicts": sum(len(item["link_info"]["paper_arxiv_conflicts"]) for item in changed),
            "images_removed": sum(item["image_info"]["images_removed"] for item in changed),
            "captions_compacted": sum(item["image_info"]["captions_compacted"] for item in changed),
            "captions_escaped": sum(item["image_info"]["captions_escaped"] for item in changed),
        },
        "changed": changed,
    }
    json_path = report_dir / f"modernize_analysis_notes_{ts}.json"
    md_path = report_dir / f"modernize_analysis_notes_{ts}.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Modernize Analysis Notes Report",
        "",
        f"- generated: {payload['generated']}",
        f"- mode: {payload['mode']}",
        f"- cutoff: {payload['cutoff']}",
        f"- checked_notes: {payload['checked_notes']}",
        f"- changed_notes: {payload['changed_notes']}",
        f"- unchanged_notes: {payload['unchanged_notes']}",
        f"- max_images: {payload['max_images']}",
        f"- max_caption_chars: {payload['max_caption_chars']}",
        "",
        "## Summary",
        "",
    ]
    for key, value in payload["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Changed Notes", ""])
    for item in changed[:500]:
        lines.append(f"- `{item['path']}`: links={item['link_info']['links_rows_rewritten']}, arxiv_labels={item['link_info']['arxiv_labels_renamed']}, images_removed={item['image_info']['images_removed']}, captions_compacted={item['image_info']['captions_compacted']}")
    if len(changed) > 500:
        lines.append(f"- ... {len(changed) - 500} more; see JSON report")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"[OK] mode: {payload['mode']}")
    print(f"[OK] checked: {len(notes)}")
    print(f"[OK] changed: {len(changed)}")
    print(f"[OK] report: {md_path}")
    print(f"[OK] json: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
