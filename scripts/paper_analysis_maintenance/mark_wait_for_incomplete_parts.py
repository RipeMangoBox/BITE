import csv
import re
from pathlib import Path

# Infer repository root from this file location:
# scripts/paper_analysis_maintenance/mark_wait_for_incomplete_parts.py -> parents[2] = repo root
ROOT = Path(__file__).resolve().parents[2]
paper_root = ROOT / "obsidian-vault/analysis"
log_path = ROOT / "obsidian-vault/paper_list.csv"

REQUIRED_MARKERS = [
    re.compile(r"(?i)\bPart\s*I\b"),
    re.compile(r"(?i)\bPart\s*II\b"),
    re.compile(r"(?i)\bPart\s*III\b"),
]


def has_all_parts(md_path: Path) -> bool:
    if not md_path.exists():
        return False
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    return all(rx.search(text) for rx in REQUIRED_MARKERS)


def sanitize_title_for_filename(title: str) -> str:
    out = []
    prev_us = False
    for ch in title:
        if ch.isalnum():
            out.append(ch)
            prev_us = False
        else:
            if not prev_us:
                out.append("_")
                prev_us = True
    return "".join(out).strip("_")


def md_path_from_row(row: dict[str, str]) -> Path:
    pdf_path = (row.get("pdf_path") or "").strip()
    if pdf_path.startswith("obsidian-vault/paperPDFs/"):
        rel = Path(pdf_path).relative_to("obsidian-vault/paperPDFs").with_suffix(".md")
        return paper_root / rel

    title = (row.get("paper_title") or row.get("title") or "").strip()
    venue = (row.get("venue") or "").strip()
    category = (row.get("sort") or row.get("category") or "").strip()
    category_dir = category.replace(" ", "_").replace("-", "_")
    venue_dir = venue.replace(" ", "_")
    year = "".join(ch for ch in venue if ch.isdigit()) or "Unknown"
    safe_title = sanitize_title_for_filename(title)
    return paper_root / category_dir / venue_dir / f"{year}_{safe_title}.md"


def main() -> None:
    with log_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if "state" not in fieldnames:
        raise ValueError(f"Missing state column in {log_path}")

    updated = 0
    for row in rows:
        md_path = md_path_from_row(row)
        if not has_all_parts(md_path):
            if row.get("state") != "Wait":
                row["state"] = "Wait"
                updated += 1

    with log_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Updated Wait entries: {updated}")


if __name__ == "__main__":
    main()
