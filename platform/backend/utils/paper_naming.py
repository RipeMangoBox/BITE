"""Shared paper title and filename normalization."""

from __future__ import annotations

import re


def clean_paper_title(title: str | None, title_sanitized: str | None = None) -> str:
    """Readable English title without importer hashes or duplicated venue slugs."""
    raw = (title or title_sanitized or "Untitled").strip()
    raw = re.sub(r"\s+", " ", raw).strip()

    sanitized = (title_sanitized or "").replace("_", " ").strip()
    candidates = [raw, sanitized]
    best = raw
    for cand in candidates:
        cand = re.sub(r"\s+", " ", cand).strip()
        cand = re.sub(r"\s+[0-9a-f]{8,}$", "", cand, flags=re.IGNORECASE).strip()
        cand = re.sub(r"\s+ICLR\s+20\d{2}\b.*$", "", cand, flags=re.IGNORECASE).strip()
        if cand and len(cand) < len(best):
            best = cand
    return best or raw


def paper_file_slug(title: str | None, title_sanitized: str | None = None, max_len: int = 140) -> str:
    """English filename slug: acronym + full cleaned title, joined by underscores."""
    clean = clean_paper_title(title, title_sanitized)
    clean = re.sub(
        r"\b((?:[A-Za-z]\.){2,})(?=\s|$)",
        lambda m: m.group(1).replace(".", ""),
        clean,
    )
    slug = re.sub(r"[^A-Za-z0-9]+", "_", clean).strip("_")
    return slug[:max_len] or "Untitled"
