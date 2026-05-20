from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


REPO_ROOT = Path(__file__).resolve().parents[4]
VAULT_DIR = REPO_ROOT / "obsidian-vault"
ANALYSIS_DIR = VAULT_DIR / "analysis"
PAPER_LIST_CSV = VAULT_DIR / "paper_list.csv"
INDEX_DIR = VAULT_DIR / "index"

FRONTMATTER_BOUNDARY = re.compile(r"^---\s*$")
KEY_LINE = re.compile(r"^([A-Za-z0-9_\-]+):(?:\s*(.*))?$")
VENUE_YEAR = re.compile(r"\b([A-Za-z][A-Za-z0-9_.-]*)[_ -]((?:19|20)\d{2})\b")
NON_PAPER_NOTE_NAMES = {"readme.md", "_index.md"}
NON_PAPER_NOTE_PREFIXES = ("quality_report_",)
NON_PAPER_NOTE_DIRS = {"test", "_test", "tests", "_tests"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build obsidian-vault/index from obsidian-vault/paper_list.csv and obsidian-vault/analysis frontmatter."
    )
    parser.add_argument("--dry-run", action="store_true", help="Read inputs and print counts without writing index files.")
    return parser.parse_args()


@dataclass
class Paper:
    title: str
    analysis_path: str = ""
    pdf_ref: str = ""
    venue: str = ""
    year: str = ""
    topics: List[str] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)
    datasets: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    core_operator: str = ""
    primary_logic: str = ""
    source: str = ""
    paper_link: str = ""
    project_link: str = ""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_frontmatter_bounds(lines: List[str]) -> Optional[Tuple[int, int]]:
    if not lines or not FRONTMATTER_BOUNDARY.match(lines[0]):
        return None
    for i in range(1, len(lines)):
        if FRONTMATTER_BOUNDARY.match(lines[i]):
            return 0, i
    return None


def parse_inline_list(raw: str) -> Optional[List[str]]:
    s = raw.strip()
    if not (s.startswith("[") and s.endswith("]")):
        return None
    inner = s[1:-1].strip()
    if not inner:
        return []
    try:
        return [x.strip().strip("\"'") for x in next(csv.reader([inner], skipinitialspace=True)) if x.strip()]
    except csv.Error:
        return None


def parse_frontmatter(md_text: str) -> Dict[str, object]:
    lines = md_text.splitlines()
    bounds = parse_frontmatter_bounds(lines)
    if not bounds:
        return {}

    _, end_idx = bounds
    fm_lines = lines[1:end_idx]
    data: Dict[str, object] = {}
    i = 0
    while i < len(fm_lines):
        raw = fm_lines[i]
        m = KEY_LINE.match(raw)
        if not m:
            i += 1
            continue

        key = m.group(1)
        rest = (m.group(2) or "").rstrip()

        if rest == "" and i + 1 < len(fm_lines) and fm_lines[i + 1].lstrip().startswith("- "):
            items: List[str] = []
            i += 1
            while i < len(fm_lines) and fm_lines[i].lstrip().startswith("- "):
                items.append(fm_lines[i].lstrip()[2:].strip().strip("\"'"))
                i += 1
            data[key] = [x for x in items if x]
            continue

        if rest in ("|", ">"):
            block: List[str] = []
            i += 1
            while i < len(fm_lines):
                li = fm_lines[i]
                if li.startswith("  "):
                    block.append(li[2:])
                    i += 1
                elif li.strip() == "":
                    block.append("")
                    i += 1
                else:
                    break
            data[key] = "\n".join(block).rstrip()
            continue

        val = rest.strip().strip("\"'")
        inline = parse_inline_list(val)
        data[key] = inline if inline is not None else val
        i += 1

    return data


def split_delimited(text: str, delimiters: Set[str]) -> List[str]:
    out: List[str] = []
    buf: List[str] = []
    quote = ""
    depth = 0
    pairs = {"(": ")", "[": "]", "{": "}", "（": "）", "【": "】", "《": "》"}
    closing = set(pairs.values())
    for ch in text:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in ("'", '"'):
            quote = ch
            buf.append(ch)
            continue
        if ch in pairs:
            depth += 1
            buf.append(ch)
            continue
        if ch in closing and depth > 0:
            depth -= 1
            buf.append(ch)
            continue
        if ch in delimiters and depth == 0:
            out.append("".join(buf))
            buf = []
            continue
        buf.append(ch)
    out.append("".join(buf))
    return out


def split_values(value: object, *, comma_split: bool = True) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        raw = [str(x) for x in value]
    else:
        text = str(value).strip()
        if not text:
            return []
        inline = parse_inline_list(text)
        if inline is not None:
            raw = inline
        elif comma_split:
            raw = split_delimited(text, {",", ";", "；"})
        else:
            raw = split_delimited(text, {";", "；"})

    out: List[str] = []
    seen = set()
    for item in raw:
        s = str(item).strip().strip("\"'")
        if s.startswith("#"):
            s = s[1:]
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def first_present(row: Dict[str, str], names: Iterable[str]) -> str:
    lower = {k.lower().strip(): v for k, v in row.items()}
    for name in names:
        val = lower.get(name.lower())
        if val and val.strip():
            return val.strip()
    return ""


def normalize_title(title: str) -> str:
    title = unicodedata.normalize("NFKC", title)
    return re.sub(r"\s+", " ", title).strip().lower()


def repo_rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def normalize_pdf_ref(value: object) -> str:
    ref = str(value or "").strip()
    if not ref:
        return ""
    if ref.startswith("obsidian-vault/paperPDFs/"):
        return ref
    if ref.startswith("paperPDFs/"):
        return f"obsidian-vault/{ref}"
    return ref


def infer_venue_year(*values: object) -> Tuple[str, str]:
    for value in values:
        text = str(value or "")
        match = VENUE_YEAR.search(text)
        if match:
            return match.group(1).replace(".", ""), match.group(2)
    return "", ""


def clean_scalar(value: object) -> str:
    return str(value or "").strip().strip("\"'")


def clean_generated_dirs() -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    for dirname in ("by_dataset", "by_method", "by_topic", "by_venue", "by_year"):
        dir_path = INDEX_DIR / dirname
        dir_path.mkdir(parents=True, exist_ok=True)
        for md in dir_path.glob("*.md"):
            md.unlink()


def sanitize_filename(name: str, max_len: int = 120) -> str:
    s = re.sub(r"[<>:\"/\\|?*\x00-\x1F]", "_", name.strip())
    s = re.sub(r"\s+", " ", s).rstrip(". ")
    if not s:
        s = "Unknown"
    return s[:max_len].rstrip()


def note_link(path: str, title: str = "") -> str:
    return f"[[{path}|{title}]]" if title else f"[[{path}]]"


def is_probably_csv_absent() -> bool:
    return not PAPER_LIST_CSV.exists()


def load_csv_inventory() -> List[Paper]:
    if is_probably_csv_absent():
        return []

    papers: List[Paper] = []
    with PAPER_LIST_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = first_present(row, ("title", "paper_title", "name"))
            if not title:
                continue
            pdf_ref = normalize_pdf_ref(first_present(row, ("pdf_ref", "pdf", "pdf_path")))
            venue = first_present(row, ("venue", "conference", "journal"))
            year = first_present(row, ("year", "publication_year"))
            if not venue or not year:
                inferred_venue, inferred_year = infer_venue_year(venue, pdf_ref, title)
                venue = venue or inferred_venue
                year = year or inferred_year
            papers.append(
                Paper(
                    title=title,
                    analysis_path=first_present(row, ("analysis_path", "analysis", "note_path", "md_path")),
                    pdf_ref=pdf_ref,
                    venue=venue,
                    year=year,
                    topics=split_values(first_present(row, ("topic", "topics", "task", "category"))),
                    methods=split_values(first_present(row, ("method", "methods", "technique", "techniques"))),
                    datasets=split_values(first_present(row, ("dataset", "datasets", "benchmark", "benchmarks"))),
                    tags=split_values(first_present(row, ("tags", "tag"))),
                    paper_link=first_present(row, ("paper_link", "url", "link", "openreview", "arxiv")),
                    project_link=first_present(row, ("project_link", "project_link_or_github_link", "github", "code")),
                    source="paper_list.csv",
                )
            )
    return papers


def clean_wikilinks(text: str) -> str:
    text = re.sub(r"!\[\[[^\]]+\]\]", " ", text)
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    return text


def extract_table_values(md_text: str, field_name: str, *, limit: int = 20) -> List[str]:
    pattern = re.compile(rf"^\|\s*{re.escape(field_name)}\s*\|\s*(.*?)\s*\|", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(md_text)
    if not match:
        return []
    cell = clean_wikilinks(match.group(1))
    cell = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", cell)
    cell = re.sub(r"#[A-Za-z0-9_\-/]+", lambda m: m.group(0)[1:], cell)
    return split_values(cell, comma_split=True)[:limit]


def extract_first_heading(md_text: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", md_text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_links(md_text: str) -> Tuple[str, str]:
    paper_link = ""
    project_link = ""
    for label, url in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", md_text):
        lower = label.lower()
        if not paper_link and any(key in lower for key in ("paper", "openreview", "arxiv", "pdf")):
            paper_link = url
        if not project_link and any(key in lower for key in ("project", "github", "code")):
            project_link = url
    return paper_link, project_link


def should_index_analysis_note(md_path: Path, fm: Dict[str, object], md_text: str) -> bool:
    relative_parts = md_path.relative_to(ANALYSIS_DIR).parts
    if any(part.lower() in NON_PAPER_NOTE_DIRS for part in relative_parts[:-1]):
        return False
    name = md_path.name.lower()
    if name in NON_PAPER_NOTE_NAMES:
        return False
    if any(name.startswith(prefix) for prefix in NON_PAPER_NOTE_PREFIXES):
        return False
    note_type = clean_scalar(fm.get("type")).lower()
    paper_markers = (
        clean_scalar(fm.get("pdf_ref")),
        clean_scalar(fm.get("core_operator")),
        clean_scalar(fm.get("primary_logic")),
        clean_scalar(fm.get("venue")),
        clean_scalar(fm.get("year")),
        clean_scalar(fm.get("paper_level")),
        extract_table_values(md_text, "Method", limit=1),
        extract_table_values(md_text, "Dataset", limit=1),
    )
    if note_type and note_type != "paper":
        return any(bool(x) for x in paper_markers)
    if note_type == "paper":
        return True
    if any(bool(x) for x in paper_markers):
        return True
    return len(relative_parts) > 1 and bool(infer_venue_year(*relative_parts)[1])


def load_analysis_notes() -> List[Paper]:
    if not ANALYSIS_DIR.exists():
        return []

    papers: List[Paper] = []
    for md_path in sorted(ANALYSIS_DIR.rglob("*.md")):
        text = read_text(md_path)
        fm = parse_frontmatter(text)
        if not should_index_analysis_note(md_path, fm, text):
            continue
        title = clean_scalar(fm.get("title")) or extract_first_heading(text) or md_path.stem.replace("_", " ")
        if not title:
            continue

        tags = split_values(fm.get("tags"))
        topics = split_values(fm.get("topics")) or [t for t in tags if t.startswith("topic/")]
        category = split_values(fm.get("category"))
        if not topics and category:
            topics = category
        if not topics:
            rel_parts = md_path.relative_to(ANALYSIS_DIR).parts
            if len(rel_parts) > 2 and not infer_venue_year(rel_parts[0])[1]:
                topics = [rel_parts[0]]
            elif len(rel_parts) > 1:
                topics = [rel_parts[0]]

        methods = split_values(fm.get("methods") or fm.get("method"))
        datasets = split_values(fm.get("datasets") or fm.get("dataset"))
        if not methods:
            methods = extract_table_values(text, "Method", limit=6)
        if not datasets:
            datasets = extract_table_values(text, "Dataset", limit=20)
        pdf_ref = normalize_pdf_ref(fm.get("pdf_ref"))
        venue = clean_scalar(fm.get("venue"))
        year = clean_scalar(fm.get("year"))
        if not venue or not year:
            inferred_venue, inferred_year = infer_venue_year(repo_rel(md_path), pdf_ref, title)
            venue = venue or inferred_venue
            year = year or inferred_year
        paper_link, project_link = extract_links(text)
        paper_link = clean_scalar(
            fm.get("paper_link") or fm.get("url") or fm.get("link") or fm.get("openreview") or fm.get("arxiv")
        ) or paper_link
        project_link = clean_scalar(
            fm.get("project_link") or fm.get("project_link_or_github_link") or fm.get("github") or fm.get("code")
        ) or project_link

        papers.append(
            Paper(
                title=title,
                analysis_path=repo_rel(md_path),
                pdf_ref=pdf_ref,
                venue=venue,
                year=year,
                topics=topics,
                methods=methods,
                datasets=datasets,
                tags=tags,
                core_operator=clean_scalar(fm.get("core_operator")),
                primary_logic=clean_scalar(fm.get("primary_logic") or fm.get("paradigm")),
                paper_link=paper_link,
                project_link=project_link,
                source="analysis",
            )
        )
    return papers


def merge_values(base: List[str], extra: List[str]) -> List[str]:
    out: List[str] = []
    seen = set()
    for val in [*base, *extra]:
        s = val.strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def merge_papers(csv_papers: List[Paper], analysis_papers: List[Paper]) -> List[Paper]:
    if not csv_papers:
        return sorted(analysis_papers, key=lambda p: (str(p.year), p.venue.lower(), p.title.lower()))

    analysis_by_title = {normalize_title(p.title): p for p in analysis_papers}
    analysis_by_path = {p.analysis_path: p for p in analysis_papers if p.analysis_path}
    matched_paths: Set[str] = set()
    matched_titles: Set[str] = set()

    merged: List[Paper] = []
    for base in csv_papers:
        ana = None
        if base.analysis_path:
            ana = analysis_by_path.get(base.analysis_path)
        if ana is None:
            ana = analysis_by_title.get(normalize_title(base.title))
        if ana is None:
            merged.append(base)
            continue

        matched_paths.add(ana.analysis_path)
        matched_titles.add(normalize_title(ana.title))
        base.analysis_path = base.analysis_path or ana.analysis_path
        base.pdf_ref = base.pdf_ref or ana.pdf_ref
        base.venue = base.venue or ana.venue
        base.year = base.year or ana.year
        base.topics = merge_values(base.topics, ana.topics)
        base.methods = merge_values(base.methods, ana.methods)
        base.datasets = merge_values(base.datasets, ana.datasets)
        base.tags = merge_values(base.tags, ana.tags)
        base.core_operator = base.core_operator or ana.core_operator
        base.primary_logic = base.primary_logic or ana.primary_logic
        base.paper_link = base.paper_link or ana.paper_link
        base.project_link = base.project_link or ana.project_link
        base.source = "paper_list.csv+analysis"
        merged.append(base)

    for ana in analysis_papers:
        if ana.analysis_path in matched_paths or normalize_title(ana.title) in matched_titles:
            continue
        merged.append(ana)

    return sorted(merged, key=lambda p: (str(p.year), p.venue.lower(), p.title.lower()))


def year_json_value(year: str) -> object:
    s = str(year).strip()
    return int(s) if re.fullmatch(r"\d{4}", s) else s


def build_jsonl(papers: List[Paper]) -> str:
    lines: List[str] = []
    for p in papers:
        row = {
            "title": p.title,
            "analysis_path": p.analysis_path,
            "pdf_ref": p.pdf_ref,
            "venue": p.venue,
            "year": year_json_value(p.year),
            "topics": p.topics,
            "methods": p.methods,
            "datasets": p.datasets,
            "tags": p.tags,
            "core_operator": p.core_operator,
            "primary_logic": p.primary_logic,
            "paper_link": p.paper_link,
            "project_link": p.project_link,
            "source": p.source,
        }
        lines.append(json.dumps(row, ensure_ascii=False, sort_keys=True))
    return ("\n".join(lines) + "\n") if lines else ""


def paper_bullet(paper: Paper) -> str:
    label = f"{paper.title}"
    suffix = " ".join(x for x in (paper.venue, str(paper.year)) if x)
    if suffix:
        label = f"{label} ({suffix})"
    if paper.analysis_path:
        head = note_link(paper.analysis_path, label)
    else:
        head = label
    parts = [head]
    if paper.pdf_ref:
        parts.append(note_link(paper.pdf_ref, "PDF"))
    if paper.topics:
        parts.append("topics: " + ", ".join(paper.topics))
    if paper.methods:
        parts.append("methods: " + ", ".join(paper.methods[:3]))
    if paper.datasets:
        parts.append("datasets: " + ", ".join(paper.datasets[:3]))
    return "- " + " · ".join(parts)


def frontmatter(title: str, dimension: str, now: str) -> List[str]:
    return [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        "type: paper-index",
        f"dimension: {dimension}",
        "tags:",
        "  - obsidian-vault/index",
        f"generated: {now}",
        "---",
        "",
    ]


def build_all_papers(papers: List[Paper], now: str) -> str:
    lines = frontmatter("All Papers", "all", now)
    lines.extend(["# All Papers", ""])
    for paper in papers:
        lines.append(paper_bullet(paper))
    lines.append("")
    return "\n".join(lines)


def group_by_dimension(papers: List[Paper], attr: str) -> Dict[str, List[Paper]]:
    grouped: Dict[str, List[Paper]] = {}
    for paper in papers:
        values = getattr(paper, attr)
        if isinstance(values, list):
            keys = values
        else:
            keys = [str(values)] if str(values).strip() else []
        for key in keys:
            clean = str(key).strip()
            if clean:
                grouped.setdefault(clean, []).append(paper)
    return grouped


def write_dimension(
    dirname: str, dimension: str, grouped: Dict[str, List[Paper]], now: str, *, min_count: int = 1
) -> None:
    base = INDEX_DIR / dirname
    keys = [key for key in sorted(grouped.keys(), key=lambda x: x.lower()) if len(grouped[key]) >= min_count]
    index_lines = frontmatter(f"{dimension.title()} Index", dimension, now)
    index_lines.extend([f"# {dimension.title()} Index", ""])
    if min_count > 1:
        index_lines.extend([f"Only values linked to at least {min_count} papers are listed here.", ""])
    for key in keys:
        index_lines.append(f"- {note_link(f'obsidian-vault/index/{dirname}/{sanitize_filename(key)}.md', key)} ({len(grouped[key])})")
    index_lines.append("")
    write_text(base / "_Index.md", "\n".join(index_lines))

    for key in keys:
        lines = frontmatter(f"{dimension.title()}: {key}", dimension, now)
        lines.extend([f"# {dimension.title()}: {key}", ""])
        for paper in sorted(grouped[key], key=lambda p: (str(p.year), p.venue.lower(), p.title.lower())):
            lines.append(paper_bullet(paper))
        lines.append("")
        write_text(base / f"{sanitize_filename(key)}.md", "\n".join(lines))


def build_home_index(papers: List[Paper], now: str) -> str:
    lines = frontmatter("ResearchFlow Paper Index", "home", now)
    lines.extend(
        [
            "# ResearchFlow Paper Index",
            "",
            "This directory is generated by `papers-build-index` from `obsidian-vault/paper_list.csv` and `obsidian-vault/analysis/` frontmatter.",
            "",
            "## Entry Points",
            "",
            f"- {note_link('obsidian-vault/index/_AllPapers.md', 'All papers')}",
            f"- {note_link('obsidian-vault/index/by_topic/_Index.md', 'By topic')}",
            f"- {note_link('obsidian-vault/index/by_method/_Index.md', 'By method')}",
            f"- {note_link('obsidian-vault/index/by_dataset/_Index.md', 'By dataset')}",
            f"- {note_link('obsidian-vault/index/by_venue/_Index.md', 'By venue')}",
            f"- {note_link('obsidian-vault/index/by_year/_Index.md', 'By year')}",
            "",
            "## Counts",
            "",
            f"- papers: {len(papers)}",
            f"- generated: {now}",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    csv_papers = load_csv_inventory()
    analysis_papers = load_analysis_notes()
    papers = merge_papers(csv_papers, analysis_papers)

    if not args.dry_run:
        clean_generated_dirs()
        write_text(INDEX_DIR / "index.jsonl", build_jsonl(papers))
        write_text(INDEX_DIR / "_AllPapers.md", build_all_papers(papers, now))
        write_text(INDEX_DIR / "_Index.md", build_home_index(papers, now))

        write_dimension("by_dataset", "dataset", group_by_dimension(papers, "datasets"), now, min_count=2)
        write_dimension("by_method", "method", group_by_dimension(papers, "methods"), now)
        write_dimension("by_topic", "topic", group_by_dimension(papers, "topics"), now)
        write_dimension("by_venue", "venue", group_by_dimension(papers, "venue"), now)
        write_dimension("by_year", "year", group_by_dimension(papers, "year"), now)

    print(f"[OK] papers: {len(papers)}")
    print(f"[OK] source paper_list.csv: {len(csv_papers)}")
    print(f"[OK] source analysis notes: {len(analysis_papers)}")
    print(f"[OK] output: {INDEX_DIR}")
    if args.dry_run:
        print("[OK] dry-run: no files written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
