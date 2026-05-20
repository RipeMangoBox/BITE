from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[4]
VAULT_DIR = REPO_ROOT / "obsidian-vault"
ANALYSIS_DIR = VAULT_DIR / "analysis"
PAPER_LIST_CSV = VAULT_DIR / "paper_list.csv"
INDEX_DIR = VAULT_DIR / "index"

FRONTMATTER_BOUNDARY = re.compile(r"^---\s*$")
KEY_LINE = re.compile(r"^([A-Za-z0-9_\-]+):(?:\s*(.*))?$")


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
            raw = re.split(r"[;,]", text)
        else:
            raw = re.split(r"[;]", text)

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
            papers.append(
                Paper(
                    title=title,
                    analysis_path=first_present(row, ("analysis_path", "analysis", "note_path", "md_path")),
                    pdf_ref=normalize_pdf_ref(first_present(row, ("pdf_ref", "pdf", "pdf_path"))),
                    venue=first_present(row, ("venue", "conference", "journal")),
                    year=first_present(row, ("year", "publication_year")),
                    topics=split_values(first_present(row, ("topic", "topics", "task", "category"))),
                    methods=split_values(first_present(row, ("method", "methods", "technique", "techniques"))),
                    datasets=split_values(first_present(row, ("dataset", "datasets", "benchmark", "benchmarks"))),
                    tags=split_values(first_present(row, ("tags", "tag"))),
                    source="paper_list.csv",
                )
            )
    return papers


def extract_table_values(md_text: str, field_name: str) -> List[str]:
    pattern = re.compile(rf"^\|\s*{re.escape(field_name)}\s*\|\s*(.*?)\s*\|", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(md_text)
    if not match:
        return []
    cell = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", match.group(1))
    cell = re.sub(r"#[A-Za-z0-9_\-/]+", lambda m: m.group(0)[1:], cell)
    return split_values(cell, comma_split=False)


def load_analysis_notes() -> List[Paper]:
    if not ANALYSIS_DIR.exists():
        return []

    papers: List[Paper] = []
    for md_path in sorted(ANALYSIS_DIR.rglob("*.md")):
        text = read_text(md_path)
        fm = parse_frontmatter(text)
        has_paper_evidence = bool(
            str(fm.get("type") or "").strip() == "paper"
            or str(fm.get("pdf_ref") or "").strip()
            or str(fm.get("core_operator") or "").strip()
            or str(fm.get("primary_logic") or "").strip()
        )
        if not has_paper_evidence:
            continue
        title = str(fm.get("title") or md_path.stem.replace("_", " ")).strip()
        if not title:
            continue

        tags = split_values(fm.get("tags"))
        topics = split_values(fm.get("topics")) or [t for t in tags if t.startswith("topic/")]
        category = split_values(fm.get("category"))
        if not topics and category:
            topics = category

        methods = split_values(fm.get("methods") or fm.get("method") or fm.get("aliases"))
        datasets = split_values(fm.get("datasets") or fm.get("dataset"))
        if not methods:
            methods = extract_table_values(text, "Method")[:1]
        if not datasets:
            datasets = extract_table_values(text, "Dataset")[:12]

        papers.append(
            Paper(
                title=title,
                analysis_path=repo_rel(md_path),
                pdf_ref=normalize_pdf_ref(fm.get("pdf_ref")),
                venue=str(fm.get("venue") or "").strip(),
                year=str(fm.get("year") or "").strip(),
                topics=topics,
                methods=methods,
                datasets=datasets,
                tags=tags,
                core_operator=str(fm.get("core_operator") or "").strip(),
                primary_logic=str(fm.get("primary_logic") or "").strip(),
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
        base.source = "paper_list.csv+analysis"
        merged.append(base)

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


def write_dimension(dirname: str, dimension: str, grouped: Dict[str, List[Paper]], now: str) -> None:
    if not grouped:
        return

    base = INDEX_DIR / dirname
    keys = sorted(grouped.keys(), key=lambda x: x.lower())
    index_lines = frontmatter(f"{dimension.title()} Index", dimension, now)
    index_lines.extend([f"# {dimension.title()} Index", ""])
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


def build_readme(papers: List[Paper], now: str) -> str:
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
        write_text(INDEX_DIR / "README.md", build_readme(papers, now))

        write_dimension("by_dataset", "dataset", group_by_dimension(papers, "datasets"), now)
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
