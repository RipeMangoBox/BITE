from __future__ import annotations

import re


def normalize_conf_year_slug(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    text = re.sub(r"\s+", "_", text)
    text = text.replace("-", "_")
    match = re.fullmatch(r"(.+?)_((?:19|20)\d{2})", text)
    if not match:
        return text
    venue, year = match.groups()
    venue = re.sub(r"_+", "_", venue).strip("_")
    if venue.lower() == "arxiv":
        return f"arxiv_{year}"
    if re.fullmatch(r"(?i)(.+?)_?workshops?", venue):
        venue = re.sub(r"(?i)_?workshops?$", "W", venue)
    return f"{venue.upper()}_{year}"
