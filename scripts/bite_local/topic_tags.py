"""Obsidian topic tag helpers for the local-file workflow."""

from __future__ import annotations

import re
from typing import Any, Iterable


_NON_TAG_RE = re.compile(r"[^a-z0-9_/-]+")
_MULTI_SEP_RE = re.compile(r"[_/]+")


def obsidian_tag_slug(value: object) -> str:
    """Normalize a label or id into one Obsidian tag path segment."""
    text = str(value or "").strip().lower()
    text = text.replace("&", " and ")
    text = text.replace("+", " and ")
    text = text.replace("-", "_")
    text = text.replace("/", " ")
    text = re.sub(r"\s+", "_", text)
    text = _NON_TAG_RE.sub("_", text)
    text = _MULTI_SEP_RE.sub("_", text).strip("_/")
    return text or "other_unclear"


def format_topic_tag(*segments: object, namespace: str = "topic") -> str:
    """Build a hierarchical Obsidian tag such as #topic/root/subtopic."""
    clean = [obsidian_tag_slug(namespace)]
    clean.extend(obsidian_tag_slug(segment) for segment in segments if str(segment or "").strip())
    return "#" + "/".join(clean)


def _first_nonempty(*values: object) -> str:
    for value in values:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def topic_tags_from_assignment(info: dict[str, Any] | None) -> list[str]:
    """Return root + child tags from a fine-topic assignment row."""
    info = info or {}
    root = _first_nonempty(info.get("root_id"), info.get("root_label"))
    subtopic = _first_nonempty(info.get("subtopic_id"), info.get("subtopic_label"))
    tags: list[str] = []
    if root:
        tags.append(format_topic_tag(root))
    if root and subtopic and obsidian_tag_slug(root) != obsidian_tag_slug(subtopic):
        tags.append(format_topic_tag(root, subtopic))
    elif subtopic:
        tags.append(format_topic_tag(subtopic))
    return tags


def topic_tags_from_names(names: Iterable[object], *, fallback: str = "other_unclear") -> list[str]:
    """Return stable #topic/... tags from taxonomy/facet names."""
    tags: list[str] = []
    seen: set[str] = set()
    for name in names:
        text = str(name or "").strip()
        if not text:
            continue
        tag = format_topic_tag(text)
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)
    if not tags and fallback:
        tags.append(format_topic_tag(fallback))
    return tags


def format_topic_tags(tags: Iterable[str], *, limit: int = 5) -> str:
    """Render a table-cell-safe, space-separated tag list."""
    out: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        text = str(tag or "").strip()
        if not text:
            continue
        if not text.startswith("#"):
            text = format_topic_tag(text)
        if text in seen:
            continue
        seen.add(text)
        out.append(text)
        if len(out) >= limit:
            break
    return " ".join(out) if out else format_topic_tag("other_unclear")
