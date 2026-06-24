from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PAPER_ANALYSIS_DIR = REPO_ROOT / "obsidian-vault/analysis"
LOG_PATH = REPO_ROOT / "obsidian-vault/paper_list.csv"


ABSTRACT_HEADER_RX = re.compile(r"^> \[!abstract\].*$", re.M)
TITLE_IN_FM_RX = re.compile(r"(?im)^title\s*:\s*(.+)$")
LINKS_LINE_RX = re.compile(r"^> - \*\*Links\*\*:\s*(.*)$", re.M)


def _norm_title(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def _extract_md_title(md_text: str, md_path: Path) -> str:
    if md_text.startswith("---"):
        end = md_text.find("\n---", 3)
        if end != -1:
            fm = md_text[3:end]
            m = TITLE_IN_FM_RX.search(fm)
            if m:
                return m.group(1).strip().strip("\"'").strip()
    stem = re.sub(r"^\d{4}_", "", md_path.stem)
    return stem.replace("_", " ").strip()


def _extract_abstract_block(md_text: str) -> tuple[int, int, str] | None:
    m = ABSTRACT_HEADER_RX.search(md_text)
    if not m:
        return None
    start = m.start()
    after = md_text[start:]
    lines = after.splitlines(keepends=True)
    acc: list[str] = []
    end_rel = 0
    for line in lines:
        if line.startswith(">"):
            acc.append(line)
            end_rel += len(line)
        else:
            break
    end = start + end_rel
    return start, end, "".join(acc)


@dataclass(frozen=True)
class LogRow:
    title: str
    link: str  # project_link_or_github_link


def _parse_log() -> list[LogRow]:
    rows: list[LogRow] = []
    with LOG_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = (row.get("paper_title") or row.get("title") or "").strip()
            link = (row.get("project_link_or_github_link") or row.get("project_link") or row.get("github") or "").strip()
            if not title:
                continue
            rows.append(LogRow(title=title, link=link))
    return rows


def _best_log_match(rows: list[LogRow], md_title: str) -> tuple[float, LogRow] | None:
    nmd = _norm_title(md_title)
    best: tuple[float, LogRow] | None = None
    for r in rows:
        nt = _norm_title(r.title)
        if not nmd or not nt:
            continue
        score = 0.92 if (nmd in nt or nt in nmd) else SequenceMatcher(None, nmd, nt).ratio()
        if best is None or score > best[0]:
            best = (score, r)
    if best and best[0] >= 0.78:
        return best
    return None


def _label_for_link(url: str) -> str:
    return "GitHub" if "github.com" in url.lower() else "Project"


def _has_project_or_github_in_block(block_text: str) -> bool:
    low = block_text.lower()
    return ("project" in low) or ("github" in low)


def _inject_link_into_block(block_text: str, label: str, url: str) -> str:
    url = url.strip()
    if not url or url == "-" or url.isdigit():
        return block_text

    link_md = f"[{label}]({url})"

    m = LINKS_LINE_RX.search(block_text)
    if m:
        existing = m.group(1).strip()
        if url in existing or link_md in existing:
            return block_text
        sep = " | " if existing else ""
        new_line = f"> - **Links**: {existing}{sep}{link_md}"
        return block_text.replace(m.group(0), new_line, 1)

    lines = block_text.splitlines()
    if not lines:
        return block_text
    insert_line = f"> - **Links**: {link_md}"
    out = "\n".join([lines[0], insert_line, *lines[1:]])
    return out + ("\n" if block_text.endswith("\n") else "")


def main() -> int:
    if not LOG_PATH.exists():
        raise FileNotFoundError(f"Missing log file: {LOG_PATH}")

    rows = _parse_log()

    md_files: list[Path] = []
    for p in PAPER_ANALYSIS_DIR.rglob("*.md"):
        if "emergentmind_paper_analysis" in str(p).lower():
            continue
        md_files.append(p)

    updated: list[tuple[Path, str, str, float]] = []
    skipped_no_match: list[tuple[Path, str]] = []
    skipped_no_link: list[tuple[Path, str, str]] = []

    for p in md_files:
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = p.read_text(encoding="utf-8", errors="ignore")

        blk = _extract_abstract_block(text)
        if not blk:
            continue
        start, end, block_text = blk

        if _has_project_or_github_in_block(block_text):
            continue

        title_guess = _extract_md_title(text, p)
        match = _best_log_match(rows, title_guess)
        if not match:
            skipped_no_match.append((p, title_guess))
            continue
        score, row = match

        url = (row.link or "").strip()
        if not url or url == "-" or url.isdigit():
            skipped_no_link.append((p, title_guess, row.link))
            continue

        label = _label_for_link(url)
        new_block = _inject_link_into_block(block_text, label, url)
        if new_block == block_text:
            continue

        p.write_text(text[:start] + new_block + text[end:], encoding="utf-8")
        updated.append((p, label, url, score))

    print(f"Updated files: {len(updated)}")
    for p, label, url, score in updated[:250]:
        print(f"- {p.relative_to(REPO_ROOT)} | +{label}: {url} | match {score:.2f}")
    print(f"Skipped (no match): {len(skipped_no_match)}")
    for p, t in skipped_no_match[:100]:
        print(f"- {p.relative_to(REPO_ROOT)} | title: {t}")
    print(f"Skipped (no link in log): {len(skipped_no_link)}")
    for p, t, l in skipped_no_link[:100]:
        print(f"- {p.relative_to(REPO_ROOT)} | title: {t} | log_link: {l}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
