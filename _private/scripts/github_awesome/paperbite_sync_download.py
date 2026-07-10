#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import itertools
import os
import re
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, quote, urljoin, urlparse, urlunparse

import requests


SCRIPT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_ROOT.parents[2]
PRIVATE_PAPERBITE_ROOT = REPO_ROOT / "_private" / "PaperBite"
PAPERBITE_ROOT = REPO_ROOT / "PaperBite"
GLOBAL_ROOT = PAPERBITE_ROOT / "_global"
SOURCES_ROOT = PAPERBITE_ROOT / "sources"
PAPERS_ROOT = PAPERBITE_ROOT / "papers"
WIKI_ROOT = PAPERBITE_ROOT / "wiki"

DEFAULT_CSVS = [
    SCRIPT_ROOT / "collect_logs" / "ChenHsing__Awesome-Video-Diffusion-Models.auto.csv",
    SCRIPT_ROOT / "collect_logs" / "weitianxin__Awesome-Agentic-Reasoning.auto.csv",
]

RUNNER_NAME = "paperbite_sync_download_v1"
SCHEMA_VERSION = "2"
PARSER_VERSION = "1"
USER_AGENT = "Mozilla/5.0 (compatible; PaperBiteSync/1.0; +https://github.com)"

PAPER_REGISTRY_FIELDS = [
    "paper_id",
    "title",
    "venue",
    "year",
    "canonical_paper_link",
    "canonical_code_link",
    "category",
    "pdf_path",
    "pdf_sha256",
    "analysis_path",
    "analysis_level",
    "schema_version",
    "first_seen_at",
    "last_seen_at",
    "status",
    "notes",
]

SOURCE_MEMBERSHIP_FIELDS = [
    "paper_id",
    "source_repo",
    "source_item_id",
    "source_section",
    "first_seen_commit",
    "last_seen_commit",
    "membership_status",
    "first_seen_at",
    "last_seen_at",
]

PDF_REGISTRY_FIELDS = [
    "paper_id",
    "pdf_path",
    "pdf_sha256",
    "file_size_bytes",
    "source_url",
    "downloaded_at",
    "last_verified_at",
    "status",
    "notes",
]

ALIASES_FIELDS = [
    "paper_id",
    "alias_type",
    "alias_value",
    "source_repo",
    "first_seen_at",
    "notes",
]

SYNC_RUN_FIELDS = [
    "run_id",
    "source_repo",
    "started_at",
    "finished_at",
    "base_commit",
    "new_commit",
    "parser_version",
    "status",
    "added_count",
    "removed_count",
    "changed_count",
    "rescan_required",
    "notes",
]

SOURCE_ITEMS_FIELDS = [
    "source_item_id",
    "source_repo",
    "state",
    "importance",
    "paper_title",
    "venue",
    "project_link_or_github_link",
    "paper_link",
    "sort",
    "pdf_path",
    "paper_id",
    "item_type",
    "updated_at",
]

REVIEW_QUEUE_FIELDS = [
    "source_item_id",
    "paper_id",
    "filter_result",
    "review_status",
    "paper_status",
    "score",
    "decision_reason",
    "manual_override",
    "reviewed_at",
    "notes",
]

PAPER_HOST_HINTS = (
    "arxiv.org",
    "openreview.net",
    "openaccess.thecvf.com",
    "thecvf.com",
    "aclanthology.org",
    "pmlr.press",
    "proceedings.mlr.press",
    "proceedings.neurips.cc",
    "papers.nips.cc",
    "doi.org",
    "dl.acm.org",
    "ieeexplore.ieee.org",
    "ecva.net",
    "springer.com",
    "nature.com",
    "science.org",
    "sciencedirect.com",
)

NON_PAPER_VENUE_PREFIXES = ("software",)

STATUS_PRIORITY = {
    "downloaded": 4,
    "analysis_ready": 3,
    "missing_pdf": 2,
    "waiting_pdf": 1,
    "registered": 0,
}

ANALYSIS_LEVEL_PRIORITY = {"none": 0, "brief": 1, "full": 2}


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def sanitize_component(text: str, fallback: str) -> str:
    value = normalize_spaces(text).replace(" ", "_")
    value = value.replace("\u2013", "-").replace("\u2014", "-")
    value = re.sub(r"[<>:\"/\\|?*\x00-\x1f]", "_", value)
    value = re.sub(r"_+", "_", value).strip("_. ")
    return value or fallback


def normalize_title_key(title: str) -> str:
    value = normalize_spaces(title).lower()
    value = re.sub(r"[^a-z0-9]+", "", value)
    return value


def extract_year(text: str) -> str:
    match = re.search(r"\b((?:19|20)\d{2})\b", text or "")
    return match.group(1) if match else ""


def infer_arxiv_year(url: str) -> str:
    match = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{2})([0-9]{2})\.[0-9]{4,5}", url or "", re.I)
    if not match:
        return ""
    return f"20{match.group(1)}"


def extract_year_from_row(row: dict[str, str]) -> str:
    year = extract_year(row.get("venue", ""))
    if year:
        return year
    return infer_arxiv_year(row.get("paper_link", ""))


def venue_is_final(venue: str) -> bool:
    low = normalize_spaces(venue).lower()
    if not low:
        return False
    return not low.startswith(("arxiv", "unknown", "software", "technical report", "corr"))


def level_max(lhs: str, rhs: str) -> str:
    lhs_n = lhs if lhs in ANALYSIS_LEVEL_PRIORITY else "none"
    rhs_n = rhs if rhs in ANALYSIS_LEVEL_PRIORITY else "none"
    return lhs_n if ANALYSIS_LEVEL_PRIORITY[lhs_n] >= ANALYSIS_LEVEL_PRIORITY[rhs_n] else rhs_n


def status_max(lhs: str, rhs: str) -> str:
    lhs_n = lhs if lhs in STATUS_PRIORITY else "registered"
    rhs_n = rhs if rhs in STATUS_PRIORITY else "registered"
    return lhs_n if STATUS_PRIORITY[lhs_n] >= STATUS_PRIORITY[rhs_n] else rhs_n


def min_iso(lhs: str, rhs: str) -> str:
    if lhs == "N/A":
        return rhs
    if rhs == "N/A":
        return lhs
    return lhs if lhs <= rhs else rhs


def max_iso(lhs: str, rhs: str) -> str:
    if lhs == "N/A":
        return rhs
    if rhs == "N/A":
        return lhs
    return lhs if lhs >= rhs else rhs


def canonicalize_arxiv_url(url: str) -> str:
    arxiv_id = extract_arxiv_id(url)
    if not arxiv_id:
        return normalize_url(url)
    return f"https://arxiv.org/abs/{arxiv_id}"


def extract_arxiv_id(url: str) -> str:
    match = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})(?:v\d+)?", url or "", re.I)
    return match.group(1) if match else ""


def extract_openreview_id(url: str) -> str:
    if "openreview.net" not in (url or "").lower():
        return ""
    parsed = urlparse(url)
    query_id = parse_qs(parsed.query).get("id", [""])[0]
    if query_id:
        return query_id
    match = re.search(r"/forum\?id=([^&#]+)|/pdf\?id=([^&#]+)", url or "", re.I)
    if not match:
        return ""
    return match.group(1) or match.group(2) or ""


def extract_doi(url: str) -> str:
    value = (url or "").strip()
    if not value:
        return ""
    match = re.search(r"(10\.\d{4,9}/[^?#\s]+)", value, re.I)
    if not match:
        return ""
    doi = match.group(1).rstrip(").,;")
    return doi.lower()


def normalize_url(url: str) -> str:
    value = (url or "").strip()
    if not value or value.upper() == "N/A":
        return "N/A"
    arxiv_id = extract_arxiv_id(value)
    if arxiv_id:
        return f"https://arxiv.org/abs/{arxiv_id}"
    openreview_id = extract_openreview_id(value)
    if openreview_id:
        return f"https://openreview.net/forum?id={openreview_id}"
    doi = extract_doi(value)
    if doi and ("doi.org" in value.lower() or "/doi/" in value.lower()):
        return f"https://doi.org/{doi}"
    parsed = urlparse(value)
    path = parsed.path.rstrip("/") or "/"
    query = parsed.query if openreview_id else ""
    return urlunparse((parsed.scheme.lower() or "https", parsed.netloc.lower(), path, "", query, ""))


def build_hash_paper_id(title: str, year: str) -> str:
    base = f"{normalize_title_key(title)}|{year or 'unknown'}"
    digest = hashlib.sha256(base.encode("utf-8")).hexdigest()[:8]
    return f"hash:{digest}"


def paper_id_priority(paper_id: str) -> int:
    if paper_id.startswith("arxiv:"):
        return 4
    if paper_id.startswith("doi:"):
        return 3
    if paper_id.startswith("openreview:"):
        return 2
    return 1


def preferred_paper_id(row: dict[str, str]) -> tuple[str, list[str]]:
    link = row.get("paper_link", "")
    ids: list[str] = []
    arxiv_id = extract_arxiv_id(link)
    if arxiv_id:
        ids.append(f"arxiv:{arxiv_id}")
    doi = extract_doi(link)
    if doi:
        ids.append(f"doi:{doi}")
    openreview_id = extract_openreview_id(link)
    if openreview_id:
        ids.append(f"openreview:{openreview_id}")
    if ids:
        return ids[0], ids
    return build_hash_paper_id(row.get("paper_title", ""), extract_year_from_row(row)), []


def build_analysis_path(category: str, venue: str, paper_id: str) -> str:
    category_dir = sanitize_component(category, "Uncategorized")
    venue_dir = sanitize_component(venue, "UnknownVenue")
    filename = sanitize_component(paper_id.replace(":", "__"), "paper") + ".md"
    return f"PaperBite/papers/{category_dir}/{venue_dir}/{filename}"


def build_source_repo_id(csv_path: Path) -> str:
    name = csv_path.name.removesuffix(".auto.csv")
    owner, repo = github_owner_repo_from_csv(csv_path)
    if owner and repo:
        return f"{sanitize_component(owner.lower(), 'owner')}__{sanitize_component(repo.lower(), 'repo')}"
    return sanitize_component(name.lower(), "source_repo")


def github_owner_repo_from_csv(csv_path: Path) -> tuple[str, str]:
    name = csv_path.name.removesuffix(".auto.csv")
    if "__" not in name:
        return "", ""
    owner, repo = name.split("__", 1)
    return owner, repo


def build_source_url(csv_path: Path) -> str:
    owner, repo = github_owner_repo_from_csv(csv_path)
    if owner and repo:
        return f"https://github.com/{owner}/{repo}"
    return "N/A"


def build_source_item_id(csv_path: Path, row: dict[str, str]) -> str:
    raw = "||".join(
        [
            csv_path.name,
            row.get("paper_title", ""),
            row.get("paper_link", ""),
            row.get("venue", ""),
            row.get("sort", ""),
        ]
    )
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"srcitem:{digest}"


def row_is_paper(row: dict[str, str]) -> bool:
    if (row.get("state", "") or "").strip().lower() == "skip":
        return False
    venue_low = normalize_spaces(row.get("venue", "")).lower()
    if any(venue_low.startswith(prefix) for prefix in NON_PAPER_VENUE_PREFIXES):
        return False
    link = (row.get("paper_link", "") or "").lower()
    if link.endswith(".pdf"):
        return True
    return any(host in link for host in PAPER_HOST_HINTS) or "arxiv.org" in link


def choose_title(existing: str, incoming: str) -> str:
    if existing == "N/A":
        return incoming
    if incoming == "N/A":
        return existing
    if normalize_title_key(existing) == normalize_title_key(incoming):
        return incoming if len(incoming) >= len(existing) else existing
    return existing


def choose_venue(existing: str, incoming: str) -> str:
    if existing == "N/A":
        return incoming
    if incoming == "N/A":
        return existing
    if venue_is_final(incoming) and not venue_is_final(existing):
        return incoming
    if venue_is_final(existing) and not venue_is_final(incoming):
        return existing
    return incoming if len(incoming) >= len(existing) else existing


def link_score(url: str, paper_id: str) -> int:
    value = normalize_url(url)
    if value == "N/A":
        return 0
    score = 1
    if paper_id.startswith("arxiv:") and extract_arxiv_id(value):
        score += 10
    if paper_id.startswith("doi:") and extract_doi(value):
        score += 10
    if paper_id.startswith("openreview:") and extract_openreview_id(value):
        score += 10
    for idx, host in enumerate(
        [
            "arxiv.org",
            "doi.org",
            "openreview.net",
            "openaccess.thecvf.com",
            "aclanthology.org",
            "pmlr.press",
            "proceedings.neurips.cc",
            "papers.nips.cc",
        ],
        start=1,
    ):
        if host in value:
            score += 20 - idx
            break
    return score


def choose_link(existing: str, incoming: str, paper_id: str) -> str:
    existing_n = normalize_url(existing)
    incoming_n = normalize_url(incoming)
    if existing_n == "N/A":
        return incoming_n
    if incoming_n == "N/A":
        return existing_n
    return incoming_n if link_score(incoming_n, paper_id) >= link_score(existing_n, paper_id) else existing_n


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def ensure_csv(path: Path, fieldnames: list[str]) -> None:
    if path.exists():
        return
    ensure_dir(path.parent)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{key: value.strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def write_csv_rows(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    ensure_dir(path.parent)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "N/A") or "N/A" for field in fieldnames})


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def absolute_repo_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def response_is_pdf(response: requests.Response) -> bool:
    content_type = response.headers.get("Content-Type", "").lower()
    if "application/pdf" in content_type:
        return True
    try:
        prefix = response.content[:16]
    except Exception:
        return False
    return b"%PDF-" in prefix


def extract_doi_from_html(text: str) -> str:
    match = re.search(r'<meta[^>]+name=["\']citation_doi["\'][^>]+content=["\']([^"\']+)["\']', text, re.I)
    if match:
        return match.group(1).strip().lower()
    match = re.search(r"(10\.\d{4,9}/[^\"'\s<>]+)", text, re.I)
    if not match:
        return ""
    return match.group(1).strip().rstrip(").,;").lower()


def extract_pdf_candidates_from_html(base_url: str, text: str) -> list[str]:
    candidates: list[str] = []

    meta_patterns = [
        r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+property=["\']og:pdf["\'][^>]+content=["\']([^"\']+)["\']',
    ]
    for pattern in meta_patterns:
        for match in re.finditer(pattern, text, re.I):
            candidates.append(urljoin(base_url, match.group(1).strip()))

    href_patterns = [
        r'href=["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']',
        r'href=["\']([^"\']*openreview\.net/pdf\?id=[^"\']+)["\']',
        r'href=["\']([^"\']*arxiv\.org/(?:abs|pdf)/[^"\']+)["\']',
    ]
    for pattern in href_patterns:
        for match in re.finditer(pattern, text, re.I):
            candidates.append(urljoin(base_url, match.group(1).strip()))

    for match in re.finditer(r"(https?://[^\"'\s<>]+\.pdf(?:\?[^\"'\s<>]*)?)", text, re.I):
        candidates.append(match.group(1).strip())

    for match in re.finditer(r"(https?://[^\"'\s<>]+openreview\.net/pdf\?id=[^\"'\s<>]+)", text, re.I):
        candidates.append(match.group(1).strip())

    for match in re.finditer(r"(https?://[^\"'\s<>]+arxiv\.org/(?:abs|pdf)/[^\"'\s<>]+)", text, re.I):
        candidates.append(match.group(1).strip())

    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        normalized = normalize_url(candidate)
        if normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(candidate)
    return deduped


def direct_pdf_candidate(url: str) -> str:
    value = normalize_url(url)
    if value == "N/A":
        return ""
    if value.lower().endswith(".pdf"):
        return value
    arxiv_id = extract_arxiv_id(value)
    if arxiv_id:
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    openreview_id = extract_openreview_id(value)
    if openreview_id:
        return f"https://openreview.net/pdf?id={openreview_id}"
    return ""


def try_common_paths(session: requests.Session, base_url: str, timeout: int) -> str:
    if not base_url or base_url == "N/A":
        return ""
    parsed = urlparse(base_url)
    if not parsed.scheme or not parsed.netloc:
        return ""
    root = f"{parsed.scheme}://{parsed.netloc}"
    for candidate in [
        f"{root}/paper.pdf",
        f"{root}/papers/paper.pdf",
        f"{root}/static/paper.pdf",
        f"{root}/static/pdfs/paper.pdf",
        f"{root}/assets/paper.pdf",
    ]:
        try:
            response = session.get(candidate, headers={"User-Agent": USER_AGENT}, timeout=timeout, allow_redirects=True)
        except Exception:
            continue
        if response.ok and response_is_pdf(response):
            return response.url
    return ""


def search_arxiv_by_title(session: requests.Session, title: str, timeout: int) -> str:
    query = quote(title.replace('"', ""))
    url = f"http://export.arxiv.org/api/query?search_query=ti:%22{query}%22&max_results=1"
    try:
        response = session.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    except Exception:
        return ""
    if not response.ok:
        return ""
    match = re.search(r"<id>https?://arxiv.org/abs/([0-9.]+v?\d*)</id>", response.text)
    if not match:
        return ""
    arxiv_id = re.sub(r"v\d+$", "", match.group(1))
    return f"https://arxiv.org/pdf/{arxiv_id}.pdf"


def crossref_search(session: requests.Session, title: str, timeout: int) -> str:
    url = f"https://api.crossref.org/works?query.title={quote(title)}&rows=1"
    try:
        response = session.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    except Exception:
        return ""
    if not response.ok:
        return ""
    try:
        items = response.json().get("message", {}).get("items", [])
    except Exception:
        return ""
    if not items:
        return ""
    doi = items[0].get("DOI", "")
    return doi.lower() if doi else ""


def resolve_pdf_url(
    session: requests.Session,
    title: str,
    paper_link: str,
    project_link: str,
    timeout: int,
) -> tuple[str, str]:
    queue: deque[tuple[str, str]] = deque()
    for label, url in [
        ("paper_link", paper_link),
        ("paper_direct", direct_pdf_candidate(paper_link)),
        ("project_link", project_link),
        ("project_direct", direct_pdf_candidate(project_link)),
    ]:
        normalized = normalize_url(url)
        if normalized != "N/A":
            queue.append((url, label))

    seen: set[str] = set()

    while queue:
        url, reason = queue.popleft()
        normalized = normalize_url(url)
        if normalized == "N/A" or normalized in seen:
            continue
        seen.add(normalized)

        direct = direct_pdf_candidate(url)
        if direct and normalize_url(direct) not in seen:
            queue.appendleft((direct, f"{reason}:direct"))

        try:
            response = session.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout, allow_redirects=True)
        except Exception:
            continue

        if response.ok and response_is_pdf(response):
            return response.url, reason

        text = response.text if "html" in response.headers.get("Content-Type", "").lower() else ""
        if text:
            for candidate in extract_pdf_candidates_from_html(response.url, text):
                queue.append((candidate, f"{reason}:html"))
            doi = extract_doi_from_html(text)
            if doi:
                queue.append((f"https://doi.org/{doi}", f"{reason}:doi"))

    common_path = try_common_paths(session, project_link, timeout)
    if common_path:
        return common_path, "project_common_path"

    arxiv_pdf = search_arxiv_by_title(session, title, timeout)
    if arxiv_pdf:
        return arxiv_pdf, "title_arxiv_search"

    doi = crossref_search(session, title, timeout)
    if doi:
        return f"https://doi.org/{doi}", "title_crossref_search"

    return "", "not_found"


def download_pdf(
    session: requests.Session,
    pdf_url: str,
    target_path: Path,
    timeout: int,
) -> tuple[bool, str]:
    ensure_dir(target_path.parent)
    temp_path = target_path.with_suffix(target_path.suffix + ".part")
    try:
        response = session.get(pdf_url, headers={"User-Agent": USER_AGENT}, timeout=timeout, allow_redirects=True, stream=True)
    except Exception as exc:
        return False, f"request_failed:{exc}"

    if not response.ok:
        return False, f"http_{response.status_code}"

    with temp_path.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 128):
            if chunk:
                handle.write(chunk)

    with temp_path.open("rb") as handle:
        prefix = handle.read(16)
    if b"%PDF-" not in prefix:
        temp_path.unlink(missing_ok=True)
        return False, "not_pdf"

    os.replace(temp_path, target_path)
    return True, normalize_url(response.url)


def interleave_tasks(tasks: list[dict[str, str]]) -> list[dict[str, str]]:
    by_source: dict[str, deque[dict[str, str]]] = defaultdict(deque)
    for task in tasks:
        by_source[task["source_repo"]].append(task)
    ordered: list[dict[str, str]] = []
    source_cycle = [key for key in by_source]
    while source_cycle:
        next_cycle: list[str] = []
        for source_repo in source_cycle:
            if by_source[source_repo]:
                ordered.append(by_source[source_repo].popleft())
            if by_source[source_repo]:
                next_cycle.append(source_repo)
        source_cycle = next_cycle
    return ordered


def create_default_row(fieldnames: list[str], **values: str) -> dict[str, str]:
    row = {field: "N/A" for field in fieldnames}
    row.update({key: (value if value not in {"", None} else "N/A") for key, value in values.items()})
    return row


def load_registry_maps() -> tuple[
    dict[str, dict[str, str]],
    dict[tuple[str, str, str], dict[str, str]],
    dict[str, dict[str, str]],
    dict[tuple[str, str, str], dict[str, str]],
    dict[tuple[str, str], str],
    dict[tuple[str, str], str],
]:
    paper_registry = {
        row["paper_id"]: row
        for row in read_csv_rows(GLOBAL_ROOT / "paper_registry.csv")
        if row.get("paper_id")
    }
    source_membership = {
        (row["paper_id"], row["source_repo"], row["source_item_id"]): row
        for row in read_csv_rows(GLOBAL_ROOT / "source_membership.csv")
        if row.get("paper_id")
    }
    pdf_registry = {
        row["paper_id"]: row
        for row in read_csv_rows(GLOBAL_ROOT / "pdf_registry.csv")
        if row.get("paper_id")
    }
    aliases = {
        (row["paper_id"], row["alias_type"], row["alias_value"]): row
        for row in read_csv_rows(GLOBAL_ROOT / "aliases.csv")
        if row.get("paper_id")
    }

    alias_lookup: dict[tuple[str, str], str] = {}
    for row in aliases.values():
        alias_lookup[(row["alias_type"], row["alias_value"])] = row["paper_id"]

    title_year_lookup: dict[tuple[str, str], str] = {}
    for paper_id, row in paper_registry.items():
        title_key = normalize_title_key(row.get("title", ""))
        year = row.get("year", "")
        if title_key and year and (title_key, year) not in title_year_lookup:
            title_year_lookup[(title_key, year)] = paper_id
    return paper_registry, source_membership, pdf_registry, aliases, alias_lookup, title_year_lookup


def rebuild_title_year_lookup(paper_registry: dict[str, dict[str, str]]) -> dict[tuple[str, str], str]:
    result: dict[tuple[str, str], str] = {}
    for paper_id, row in paper_registry.items():
        title_key = normalize_title_key(row.get("title", ""))
        year = row.get("year", "")
        if title_key and year:
            result[(title_key, year)] = paper_id
    return result


def add_alias(
    aliases: dict[tuple[str, str, str], dict[str, str]],
    alias_lookup: dict[tuple[str, str], str],
    paper_id: str,
    alias_type: str,
    alias_value: str,
    source_repo: str,
    timestamp: str,
    notes: str,
) -> None:
    if not alias_value or alias_value == "N/A":
        return
    key = (paper_id, alias_type, alias_value)
    if key in aliases:
        return
    row = create_default_row(
        ALIASES_FIELDS,
        paper_id=paper_id,
        alias_type=alias_type,
        alias_value=alias_value,
        source_repo=source_repo,
        first_seen_at=timestamp,
        notes=notes or "N/A",
    )
    aliases[key] = row
    alias_lookup[(alias_type, alias_value)] = paper_id


def rename_paper_id(
    old_id: str,
    new_id: str,
    paper_registry: dict[str, dict[str, str]],
    source_membership: dict[tuple[str, str, str], dict[str, str]],
    pdf_registry: dict[str, dict[str, str]],
    aliases: dict[tuple[str, str, str], dict[str, str]],
    alias_lookup: dict[tuple[str, str], str],
    timestamp: str,
    source_repo: str,
) -> None:
    if old_id == new_id or old_id not in paper_registry:
        return

    existing = paper_registry.pop(old_id)
    existing["paper_id"] = new_id
    existing["analysis_path"] = build_analysis_path(existing["category"], existing["venue"], new_id)

    if new_id in paper_registry:
        merged = paper_registry[new_id]
        merged["title"] = choose_title(merged["title"], existing["title"])
        merged["venue"] = choose_venue(merged["venue"], existing["venue"])
        merged["year"] = merged["year"] if merged["year"] != "N/A" else existing["year"]
        merged["canonical_paper_link"] = choose_link(merged["canonical_paper_link"], existing["canonical_paper_link"], new_id)
        merged["canonical_code_link"] = merged["canonical_code_link"] if merged["canonical_code_link"] != "N/A" else existing["canonical_code_link"]
        merged["category"] = merged["category"] if merged["category"] != "N/A" else existing["category"]
        merged["pdf_path"] = merged["pdf_path"] if merged["pdf_path"] != "N/A" else existing["pdf_path"]
        merged["pdf_sha256"] = merged["pdf_sha256"] if merged["pdf_sha256"] != "N/A" else existing["pdf_sha256"]
        merged["analysis_path"] = merged["analysis_path"] if merged["analysis_path"] != "N/A" else existing["analysis_path"]
        merged["analysis_level"] = level_max(merged["analysis_level"], existing["analysis_level"])
        merged["first_seen_at"] = min_iso(merged["first_seen_at"], existing["first_seen_at"])
        merged["last_seen_at"] = max_iso(merged["last_seen_at"], existing["last_seen_at"])
        merged["status"] = status_max(merged["status"], existing["status"])
        merged["notes"] = merged["notes"] if merged["notes"] != "N/A" else existing["notes"]
    else:
        paper_registry[new_id] = existing

    moved_membership: dict[tuple[str, str, str], dict[str, str]] = {}
    for key, row in list(source_membership.items()):
        if row["paper_id"] != old_id:
            continue
        source_membership.pop(key)
        row["paper_id"] = new_id
        moved_membership[(row["paper_id"], row["source_repo"], row["source_item_id"])] = row
    source_membership.update(moved_membership)

    if old_id in pdf_registry:
        row = pdf_registry.pop(old_id)
        row["paper_id"] = new_id
        if new_id not in pdf_registry:
            pdf_registry[new_id] = row

    for key, row in list(aliases.items()):
        if row["paper_id"] != old_id:
            continue
        aliases.pop(key)
        row["paper_id"] = new_id
        aliases[(row["paper_id"], row["alias_type"], row["alias_value"])] = row
        alias_lookup[(row["alias_type"], row["alias_value"])] = new_id

    add_alias(aliases, alias_lookup, new_id, "legacy_paper_id", old_id, source_repo, timestamp, "upgraded_from_hash")


def ensure_layout(csv_paths: list[Path]) -> None:
    for path in [PAPERBITE_ROOT, GLOBAL_ROOT, SOURCES_ROOT, PAPERS_ROOT, WIKI_ROOT]:
        ensure_dir(path)

    ensure_csv(GLOBAL_ROOT / "paper_registry.csv", PAPER_REGISTRY_FIELDS)
    ensure_csv(GLOBAL_ROOT / "source_membership.csv", SOURCE_MEMBERSHIP_FIELDS)
    ensure_csv(GLOBAL_ROOT / "pdf_registry.csv", PDF_REGISTRY_FIELDS)
    ensure_csv(GLOBAL_ROOT / "sync_runs.csv", SYNC_RUN_FIELDS)
    ensure_csv(GLOBAL_ROOT / "aliases.csv", ALIASES_FIELDS)

    schema_version_path = GLOBAL_ROOT / "schema_version.yaml"
    if not schema_version_path.exists():
        schema_version_path.write_text(
            "analysis_schema: 2\nparser_version: 1\n",
            encoding="utf-8",
        )

    filter_policy_path = GLOBAL_ROOT / "filter_policy.yaml"
    if not filter_policy_path.exists():
        filter_policy_path.write_text(
            "\n".join(
                [
                    "global:",
                    "  hard_filter:",
                    "    year_min: 2022",
                    "    venue_allow:",
                    "      tier1: [CVPR, ICCV, ECCV, NeurIPS, ICML, ICLR, ACL, EMNLP]",
                    "      tier2: [AAAI, IJCAI, WACV, BMVC, MM, ICRA, IROS, CoRL]",
                    "  soft_signals:",
                    "    weights:",
                    "      has_code: 3",
                    "      venue_tier1: 5",
                    "      venue_tier2: 2",
                    "      recency_bonus: 2",
                    "    threshold_brief: 4",
                    "    threshold_full_candidate: 7",
                    "  per_sync_budget:",
                    "    max_new_brief: 30",
                    "    max_new_full_candidates: 10",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    registry_path = GLOBAL_ROOT / "registry.yaml"
    if not registry_path.exists():
        lines = ["registries:"]
        for csv_path in csv_paths:
            source_repo = build_source_repo_id(csv_path)
            source_url = build_source_url(csv_path)
            lines.extend(
                [
                    f"  - id: {source_repo}",
                    f"    url: {source_url}",
                    "    domain: github_awesome",
                    "    priority: P0",
                    "    enabled: true",
                ]
            )
        registry_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    wiki_index = WIKI_ROOT / "index.md"
    if not wiki_index.exists():
        wiki_index.write_text(
            "# PaperBite\n\n> Auto-generated canonical index root.\n",
            encoding="utf-8",
        )


def ensure_source_layout(csv_path: Path) -> Path:
    source_repo = build_source_repo_id(csv_path)
    source_dir = SOURCES_ROOT / source_repo
    ensure_dir(source_dir)
    ensure_dir(source_dir / "snapshots")
    ensure_csv(source_dir / "source_items.csv", SOURCE_ITEMS_FIELDS)
    ensure_csv(source_dir / "review_queue.csv", REVIEW_QUEUE_FIELDS)

    meta_path = source_dir / "meta.yaml"
    meta_path.write_text(
        "\n".join(
            [
                f"source_repo: {source_repo}",
                f"source_url: {build_source_url(csv_path)}",
                f"collect_log: {repo_relative(csv_path)}",
                "source_type: github_awesome_collect_log",
                "enabled: true",
                f"updated_at: {now_iso()}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return source_dir


def ensure_paper_registry_row(
    paper_registry: dict[str, dict[str, str]],
    paper_id: str,
    row: dict[str, str],
    canonical_pdf_path: str,
    timestamp: str,
) -> tuple[dict[str, str], bool]:
    created = paper_id not in paper_registry
    if created:
        paper_registry[paper_id] = create_default_row(
            PAPER_REGISTRY_FIELDS,
            paper_id=paper_id,
            title=row.get("paper_title", "N/A"),
            venue=row.get("venue", "N/A"),
            year=extract_year_from_row(row) or "N/A",
            canonical_paper_link=normalize_url(row.get("paper_link", "")),
            canonical_code_link=normalize_url(row.get("project_link_or_github_link", "")),
            category=row.get("sort", "N/A"),
            pdf_path=canonical_pdf_path,
            pdf_sha256="N/A",
            analysis_path=build_analysis_path(row.get("sort", "Uncategorized"), row.get("venue", "UnknownVenue"), paper_id),
            analysis_level="none",
            schema_version=SCHEMA_VERSION,
            first_seen_at=timestamp,
            last_seen_at=timestamp,
            status="waiting_pdf",
            notes=f"managed_by={RUNNER_NAME}",
        )
        return paper_registry[paper_id], True

    current = paper_registry[paper_id]
    current["title"] = choose_title(current["title"], row.get("paper_title", "N/A"))
    current["venue"] = choose_venue(current["venue"], row.get("venue", "N/A"))
    current["year"] = current["year"] if current["year"] != "N/A" else (extract_year_from_row(row) or "N/A")
    current["canonical_paper_link"] = choose_link(current["canonical_paper_link"], row.get("paper_link", "N/A"), paper_id)
    current["canonical_code_link"] = choose_link(current["canonical_code_link"], row.get("project_link_or_github_link", "N/A"), paper_id)
    current["category"] = current["category"] if current["category"] != "N/A" else row.get("sort", "N/A")
    current["pdf_path"] = current["pdf_path"] if current["pdf_path"] != "N/A" else canonical_pdf_path
    current["analysis_path"] = current["analysis_path"] if current["analysis_path"] != "N/A" else build_analysis_path(current["category"], current["venue"], paper_id)
    current["last_seen_at"] = timestamp
    current["schema_version"] = SCHEMA_VERSION
    return current, False


def ensure_pdf_registry_row(
    pdf_registry: dict[str, dict[str, str]],
    paper_id: str,
    pdf_path: str,
    source_url: str,
    timestamp: str,
) -> dict[str, str]:
    if paper_id not in pdf_registry:
        pdf_registry[paper_id] = create_default_row(
            PDF_REGISTRY_FIELDS,
            paper_id=paper_id,
            pdf_path=pdf_path,
            pdf_sha256="N/A",
            file_size_bytes="0",
            source_url=normalize_url(source_url),
            downloaded_at="N/A",
            last_verified_at=timestamp,
            status="pending",
            notes="awaiting_download",
        )
    row = pdf_registry[paper_id]
    row["pdf_path"] = row["pdf_path"] if row["pdf_path"] != "N/A" else pdf_path
    row["source_url"] = row["source_url"] if row["source_url"] != "N/A" else normalize_url(source_url)
    row["last_verified_at"] = timestamp
    return row


def update_pdf_status_from_file(
    paper_registry: dict[str, dict[str, str]],
    pdf_registry: dict[str, dict[str, str]],
    paper_id: str,
    timestamp: str,
) -> bool:
    if paper_id not in paper_registry:
        return False
    pdf_path = paper_registry[paper_id]["pdf_path"]
    if pdf_path == "N/A":
        return False
    absolute_path = absolute_repo_path(pdf_path)
    if not absolute_path.exists() or absolute_path.stat().st_size <= 0:
        return False
    sha = sha256_file(absolute_path)
    paper_registry[paper_id]["pdf_sha256"] = sha
    paper_registry[paper_id]["status"] = "downloaded"

    pdf_row = pdf_registry.setdefault(
        paper_id,
        create_default_row(
            PDF_REGISTRY_FIELDS,
            paper_id=paper_id,
            pdf_path=pdf_path,
            pdf_sha256="N/A",
            file_size_bytes="0",
            source_url=paper_registry[paper_id]["canonical_paper_link"],
            downloaded_at="N/A",
            last_verified_at=timestamp,
            status="pending",
            notes="adopted_existing_file",
        ),
    )
    pdf_row["pdf_path"] = pdf_path
    pdf_row["pdf_sha256"] = sha
    pdf_row["file_size_bytes"] = str(absolute_path.stat().st_size)
    pdf_row["downloaded_at"] = pdf_row["downloaded_at"] if pdf_row["downloaded_at"] != "N/A" else timestamp
    pdf_row["last_verified_at"] = timestamp
    pdf_row["status"] = "downloaded"
    pdf_row["notes"] = "canonical_pdf"
    return True


def run_once(csv_paths: list[Path], max_downloads: int | None, dry_run: bool, timeout: int) -> dict[str, dict[str, int]]:
    started_at = now_iso()
    ensure_layout(csv_paths)
    paper_registry, source_membership, pdf_registry, aliases, alias_lookup, title_year_lookup = load_registry_maps()
    sync_runs = read_csv_rows(GLOBAL_ROOT / "sync_runs.csv")

    per_source_stats: dict[str, dict[str, int]] = {}
    csv_rows_map: dict[Path, list[dict[str, str]]] = {}
    source_items_map: dict[str, list[dict[str, str]]] = {}
    paper_contexts: dict[str, list[dict[str, object]]] = defaultdict(list)

    for csv_path in csv_paths:
        ensure_source_layout(csv_path)
        source_repo = build_source_repo_id(csv_path)
        stats = per_source_stats.setdefault(
            source_repo,
            {
                "tracked_rows": 0,
                "non_paper_rows": 0,
                "new_papers": 0,
                "row_updates": 0,
                "downloaded_now": 0,
                "reused_existing": 0,
                "failed": 0,
            },
        )
        rows = read_csv_rows(csv_path)
        csv_rows_map[csv_path] = rows
        source_items: list[dict[str, str]] = []
        timestamp = now_iso()

        for row in rows:
            source_item_id = build_source_item_id(csv_path, row)
            item_type = "paper" if row_is_paper(row) else "non_paper"
            paper_id = "N/A"

            if item_type == "paper":
                stats["tracked_rows"] += 1
                preferred_id, explicit_ids = preferred_paper_id(row)
                title_year_key = (normalize_title_key(row.get("paper_title", "")), extract_year_from_row(row) or "N/A")

                existing_id = ""
                for explicit_id in explicit_ids:
                    if explicit_id in paper_registry:
                        existing_id = explicit_id
                        break
                    alias_hit = alias_lookup.get(("legacy_paper_id", explicit_id))
                    if alias_hit:
                        existing_id = alias_hit
                        break

                if not existing_id:
                    link_key = normalize_url(row.get("paper_link", ""))
                    existing_id = alias_lookup.get(("paper_link", link_key), "")

                if not existing_id and title_year_key[0] and title_year_key[1] != "N/A":
                    existing_id = title_year_lookup.get(title_year_key, "")

                paper_id = existing_id or preferred_id

                if existing_id and existing_id.startswith("hash:") and paper_id_priority(preferred_id) > paper_id_priority(existing_id):
                    rename_paper_id(
                        existing_id,
                        preferred_id,
                        paper_registry,
                        source_membership,
                        pdf_registry,
                        aliases,
                        alias_lookup,
                        timestamp,
                        source_repo,
                    )
                    title_year_lookup = rebuild_title_year_lookup(paper_registry)
                    paper_id = preferred_id

                canonical_pdf_path = paper_registry.get(paper_id, {}).get("pdf_path", "N/A")
                candidate_pdf_path = row.get("pdf_path", "N/A") or "N/A"
                if canonical_pdf_path == "N/A":
                    canonical_pdf_path = candidate_pdf_path
                elif canonical_pdf_path != candidate_pdf_path:
                    canonical_absolute = absolute_repo_path(canonical_pdf_path)
                    candidate_absolute = absolute_repo_path(candidate_pdf_path)
                    if not canonical_absolute.exists() and candidate_absolute.exists():
                        canonical_pdf_path = candidate_pdf_path

                paper_row, created = ensure_paper_registry_row(paper_registry, paper_id, row, canonical_pdf_path, timestamp)
                if created:
                    stats["new_papers"] += 1
                title_year_lookup[(normalize_title_key(paper_row["title"]), paper_row["year"])] = paper_id

                if row.get("pdf_path", "N/A") != paper_row["pdf_path"]:
                    row["pdf_path"] = paper_row["pdf_path"]
                    stats["row_updates"] += 1

                add_alias(
                    aliases,
                    alias_lookup,
                    paper_id,
                    "paper_link",
                    normalize_url(row.get("paper_link", "")),
                    source_repo,
                    timestamp,
                    "source_paper_link",
                )
                add_alias(
                    aliases,
                    alias_lookup,
                    paper_id,
                    "title_year",
                    f"{normalize_title_key(row.get('paper_title', ''))}|{extract_year_from_row(row) or 'N/A'}",
                    source_repo,
                    timestamp,
                    "normalized_title_year",
                )
                fallback_hash = build_hash_paper_id(row.get("paper_title", ""), extract_year_from_row(row))
                if fallback_hash != paper_id:
                    add_alias(
                        aliases,
                        alias_lookup,
                        paper_id,
                        "legacy_paper_id",
                        fallback_hash,
                        source_repo,
                        timestamp,
                        "fallback_hash_alias",
                    )
                if normalize_title_key(row.get("paper_title", "")) != normalize_title_key(paper_row["title"]):
                    add_alias(
                        aliases,
                        alias_lookup,
                        paper_id,
                        "title",
                        row.get("paper_title", "N/A"),
                        source_repo,
                        timestamp,
                        "source_title_alias",
                    )

                source_membership[(paper_id, source_repo, source_item_id)] = create_default_row(
                    SOURCE_MEMBERSHIP_FIELDS,
                    paper_id=paper_id,
                    source_repo=source_repo,
                    source_item_id=source_item_id,
                    source_section=row.get("sort", "N/A"),
                    first_seen_commit="collect_log:auto",
                    last_seen_commit="collect_log:auto",
                    membership_status="active",
                    first_seen_at=source_membership.get((paper_id, source_repo, source_item_id), {}).get("first_seen_at", timestamp),
                    last_seen_at=timestamp,
                )

                ensure_pdf_registry_row(
                    pdf_registry,
                    paper_id,
                    paper_row["pdf_path"],
                    paper_row["canonical_paper_link"],
                    timestamp,
                )
                update_pdf_status_from_file(paper_registry, pdf_registry, paper_id, timestamp)

                paper_contexts[paper_id].append(
                    {
                        "row": row,
                        "source_repo": source_repo,
                        "paper_link": row.get("paper_link", "N/A"),
                        "project_link": row.get("project_link_or_github_link", "N/A"),
                        "title": row.get("paper_title", "N/A"),
                    }
                )
            else:
                stats["non_paper_rows"] += 1

            source_items.append(
                create_default_row(
                    SOURCE_ITEMS_FIELDS,
                    source_item_id=source_item_id,
                    source_repo=source_repo,
                    state=row.get("state", "N/A"),
                    importance=row.get("importance", "N/A"),
                    paper_title=row.get("paper_title", "N/A"),
                    venue=row.get("venue", "N/A"),
                    project_link_or_github_link=normalize_url(row.get("project_link_or_github_link", "")),
                    paper_link=normalize_url(row.get("paper_link", "")),
                    sort=row.get("sort", "N/A"),
                    pdf_path=row.get("pdf_path", "N/A"),
                    paper_id=paper_id,
                    item_type=item_type,
                    updated_at=timestamp,
                )
            )

        source_items_map[source_repo] = source_items

    download_tasks: list[dict[str, str]] = []
    for paper_id, contexts in paper_contexts.items():
        if update_pdf_status_from_file(paper_registry, pdf_registry, paper_id, now_iso()):
            for context in contexts:
                row = context["row"]
                source_repo = str(context["source_repo"])
                if row.get("state") != "Downloaded":
                    row["state"] = "Downloaded"
                    per_source_stats[source_repo]["row_updates"] += 1
                    per_source_stats[source_repo]["reused_existing"] += 1
            continue

        if not any(str(context["row"].get("state", "")) == "Wait" for context in contexts):
            continue

        primary = contexts[0]
        download_tasks.append(
            {
                "paper_id": paper_id,
                "source_repo": str(primary["source_repo"]),
                "title": str(primary["title"]),
                "paper_link": str(primary["paper_link"]),
                "project_link": str(primary["project_link"]),
                "pdf_path": paper_registry[paper_id]["pdf_path"],
            }
        )

    ordered_tasks = interleave_tasks(download_tasks)
    if max_downloads is not None:
        ordered_tasks = ordered_tasks[:max_downloads]

    if not dry_run and ordered_tasks:
        session = requests.Session()
        for task in ordered_tasks:
            paper_id = task["paper_id"]
            pdf_url, reason = resolve_pdf_url(
                session,
                task["title"],
                task["paper_link"],
                task["project_link"],
                timeout,
            )
            if not pdf_url:
                paper_registry[paper_id]["status"] = "missing_pdf"
                pdf_registry[paper_id]["status"] = "failed"
                pdf_registry[paper_id]["notes"] = f"resolve_failed:{reason}"
                pdf_registry[paper_id]["last_verified_at"] = now_iso()
                for context in paper_contexts[paper_id]:
                    per_source_stats[str(context["source_repo"])]["failed"] += 1
                continue

            target_path = absolute_repo_path(task["pdf_path"])
            ok, note = download_pdf(session, pdf_url, target_path, timeout)
            if not ok:
                paper_registry[paper_id]["status"] = "missing_pdf"
                pdf_registry[paper_id]["status"] = "failed"
                pdf_registry[paper_id]["notes"] = note
                pdf_registry[paper_id]["last_verified_at"] = now_iso()
                for context in paper_contexts[paper_id]:
                    per_source_stats[str(context["source_repo"])]["failed"] += 1
                continue

            timestamp = now_iso()
            sha = sha256_file(target_path)
            paper_registry[paper_id]["pdf_sha256"] = sha
            paper_registry[paper_id]["status"] = "downloaded"

            pdf_registry[paper_id]["pdf_path"] = repo_relative(target_path)
            pdf_registry[paper_id]["pdf_sha256"] = sha
            pdf_registry[paper_id]["file_size_bytes"] = str(target_path.stat().st_size)
            pdf_registry[paper_id]["source_url"] = note
            pdf_registry[paper_id]["downloaded_at"] = timestamp
            pdf_registry[paper_id]["last_verified_at"] = timestamp
            pdf_registry[paper_id]["status"] = "downloaded"
            pdf_registry[paper_id]["notes"] = f"downloaded_from:{note}"

            for context in paper_contexts[paper_id]:
                row = context["row"]
                source_repo = str(context["source_repo"])
                if row.get("state") != "Downloaded":
                    row["state"] = "Downloaded"
                    per_source_stats[source_repo]["row_updates"] += 1
                row["pdf_path"] = repo_relative(target_path)
                per_source_stats[source_repo]["downloaded_now"] += 1

    for csv_path, rows in csv_rows_map.items():
        write_csv_rows(csv_path, list(rows[0].keys()) if rows else ["state", "importance", "paper_title", "venue", "project_link_or_github_link", "paper_link", "sort", "pdf_path"], rows)

    for source_repo, rows in source_items_map.items():
        write_csv_rows(SOURCES_ROOT / source_repo / "source_items.csv", SOURCE_ITEMS_FIELDS, rows)

    write_csv_rows(
        GLOBAL_ROOT / "paper_registry.csv",
        PAPER_REGISTRY_FIELDS,
        [paper_registry[key] for key in sorted(paper_registry)],
    )
    write_csv_rows(
        GLOBAL_ROOT / "source_membership.csv",
        SOURCE_MEMBERSHIP_FIELDS,
        [
            source_membership[key]
            for key in sorted(source_membership, key=lambda item: (item[1], item[0], item[2]))
        ],
    )
    write_csv_rows(
        GLOBAL_ROOT / "pdf_registry.csv",
        PDF_REGISTRY_FIELDS,
        [pdf_registry[key] for key in sorted(pdf_registry)],
    )
    write_csv_rows(
        GLOBAL_ROOT / "aliases.csv",
        ALIASES_FIELDS,
        [
            aliases[key]
            for key in sorted(aliases, key=lambda item: (item[0], item[1], item[2]))
        ],
    )

    finished_at = now_iso()
    for csv_path in csv_paths:
        source_repo = build_source_repo_id(csv_path)
        stats = per_source_stats[source_repo]
        sync_runs.append(
            create_default_row(
                SYNC_RUN_FIELDS,
                run_id=f"{dt.datetime.now().strftime('%Y%m%dT%H%M%S')}_{source_repo}",
                source_repo=source_repo,
                started_at=started_at,
                finished_at=finished_at,
                base_commit="collect_log:auto",
                new_commit="collect_log:auto",
                parser_version=f"{RUNNER_NAME}:{PARSER_VERSION}",
                status="completed",
                added_count=str(stats["new_papers"]),
                removed_count="0",
                changed_count=str(stats["row_updates"]),
                rescan_required="false",
                notes=(
                    f"tracked_rows={stats['tracked_rows']};"
                    f"non_paper_rows={stats['non_paper_rows']};"
                    f"downloaded_now={stats['downloaded_now']};"
                    f"reused_existing={stats['reused_existing']};"
                    f"failed={stats['failed']}"
                ),
            )
        )
    write_csv_rows(GLOBAL_ROOT / "sync_runs.csv", SYNC_RUN_FIELDS, sync_runs)

    return per_source_stats


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync collect logs into canonical PaperBite registries and downloads.")
    parser.add_argument("--csv", action="append", default=[], help="Collect log CSV path. Can be passed multiple times.")
    parser.add_argument("--continuous", action="store_true", help="Continuously poll and process the target CSVs.")
    parser.add_argument("--poll-seconds", type=int, default=900, help="Sleep seconds between continuous rounds.")
    parser.add_argument("--max-rounds", type=int, default=0, help="Stop after N rounds in continuous mode. 0 means unlimited.")
    parser.add_argument("--max-downloads", type=int, default=0, help="Max unique papers to download per round. 0 means no limit.")
    parser.add_argument("--timeout", type=int, default=60, help="HTTP timeout in seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Build/update registries without downloading PDFs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    csv_paths = [Path(path).resolve() for path in (args.csv or DEFAULT_CSVS)]
    missing = [path for path in csv_paths if not path.exists()]
    if missing:
        raise SystemExit(f"Missing CSVs: {missing}")

    rounds = itertools.count(1)
    while True:
        round_idx = next(rounds)
        stats = run_once(
            csv_paths=csv_paths,
            max_downloads=None if args.max_downloads <= 0 else args.max_downloads,
            dry_run=args.dry_run,
            timeout=args.timeout,
        )
        total_downloaded = sum(item["downloaded_now"] for item in stats.values())
        total_failed = sum(item["failed"] for item in stats.values())
        total_reused = sum(item["reused_existing"] for item in stats.values())
        print(
            f"[Round {round_idx}] downloaded_now={total_downloaded} reused_existing={total_reused} failed={total_failed}"
        )
        for source_repo, item in stats.items():
            print(
                "  "
                + f"{source_repo}: tracked={item['tracked_rows']} new_papers={item['new_papers']} "
                + f"downloaded_now={item['downloaded_now']} reused_existing={item['reused_existing']} failed={item['failed']}"
            )

        if not args.continuous:
            break
        if args.max_rounds > 0 and round_idx >= args.max_rounds:
            break
        time.sleep(max(args.poll_seconds, 1))


if __name__ == "__main__":
    main()
