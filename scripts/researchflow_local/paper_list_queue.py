from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from scripts.researchflow_local.venue_slug import normalize_conf_year_slug


PDF_MAGIC = b"%PDF"
MISSING_VALUES = {"", "unknown", "null", "none", "n/a"}


@dataclass(frozen=True)
class RowPreflight:
    ok: bool
    failure_kind: str
    reason: str
    pdf_path: Path | None
    conf_year: str


def row_value(row: dict[str, str], *names: str) -> str:
    for name in names:
        value = str(row.get(name) or "").strip()
        if value:
            return value
    return ""


def venue_to_conf_year(venue: str) -> str:
    text = str(venue or "").strip()
    if not text or text.lower() in MISSING_VALUES:
        return ""
    text = re.sub(r"\s+", " ", text)
    text = text.replace("&", "and")
    parts = text.split()
    if len(parts) >= 2 and re.fullmatch(r"\d{4}", parts[-1]):
        return normalize_conf_year_slug("_".join(parts[:-1] + [parts[-1]]))
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*_\d{4}", text):
        return normalize_conf_year_slug(text)
    return ""


def resolve_row_pdf_path(
    row: dict[str, str],
    *,
    repo_root: Path,
    search_roots: list[Path] | None = None,
) -> Path | None:
    raw = row_value(row, "pdf_path", "pdf", "path")
    if not raw:
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = repo_root / path
    if path.exists():
        return path.resolve()

    conf_year = venue_to_conf_year(row_value(row, "venue", "conference"))
    filename = path.name
    for root in search_roots or []:
        root = root.expanduser()
        candidates = []
        if conf_year:
            candidates.append(root / conf_year / filename)
        candidates.append(root / filename)
        for candidate in candidates:
            if candidate.exists():
                return candidate.resolve()
        if root.exists() and filename:
            for candidate in root.rglob(filename):
                if candidate.exists():
                    return candidate.resolve()
    return path.resolve()


def is_readable_pdf(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing pdf: {path}"
    if not path.is_file():
        return False, f"not a file: {path}"
    try:
        with path.open("rb") as handle:
            head = handle.read(8)
    except OSError as exc:
        return False, f"unreadable pdf: {path}: {exc}"
    if not head.startswith(PDF_MAGIC):
        return False, f"not a PDF file: {path}"
    return True, ""


def validate_paper_list_row(
    row: dict[str, str],
    *,
    repo_root: Path,
    search_roots: list[Path] | None = None,
) -> RowPreflight:
    pdf_path = resolve_row_pdf_path(row, repo_root=repo_root, search_roots=search_roots)
    if pdf_path is None:
        return RowPreflight(False, "missing_pdf", "missing pdf_path", None, "")

    pdf_ok, pdf_reason = is_readable_pdf(pdf_path)
    if not pdf_ok:
        return RowPreflight(False, "missing_pdf", pdf_reason, pdf_path, "")

    conf_year = venue_to_conf_year(row_value(row, "venue", "conference"))
    if not conf_year:
        return RowPreflight(False, "missing_venue_year", "venue must include a 4-digit year", pdf_path, "")

    return RowPreflight(True, "", "", pdf_path, conf_year)


def classify_child_failure(record: dict[str, object]) -> str:
    stderr = str(record.get("stderr_tail") or "")
    stdout = str(record.get("stdout_tail") or "")
    error = str(record.get("error") or "")
    text = "\n".join([error, stderr, stdout]).lower()
    if "missing pdf" in text or "pdf not found" in text:
        return "missing_pdf"
    if "vault export requires an existing pdf" in text or "not a pdf file" in text:
        return "missing_pdf"
    if "validation" in text and ("vault" in text or "note" in text):
        return "analysis_mismatch"
    if "mineru timed out" in text or "cuda out of memory" in text or "outofmemory" in text:
        return "too_large"
    if "mineru failed" in text or "no existing mineru output" in text:
        return "parse_failed"
    return "analysis_failed"
