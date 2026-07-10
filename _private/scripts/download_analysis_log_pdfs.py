#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import difflib
import json
import re
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, urljoin, urlparse

import requests


REPO_ROOT = Path(__file__).resolve().parents[2]
GLOBAL_LOG = REPO_ROOT / "paperAnalysis" / "analysis_log.csv"
PROCESSING_ROOT = REPO_ROOT / "paperAnalysis" / "processing" / "github_awesome"
COLLECT_LOG_ROOT = REPO_ROOT / "_private" / "PaperBite" / "github_awesome" / "collect_logs"
REPORT_ROOT = REPO_ROOT / "_private" / "PaperBite" / "github_awesome" / "download_reports"
QUEUE_PRIORITY_PATH = REPO_ROOT / "_private" / "PaperBite" / "github_awesome" / "collect_priority_queue.md"
UNIFIED_INDEX_PATH = REPO_ROOT / "paperAnalysis" / "processing" / "unified_paper_index.csv"
UNIFIED_DUPLICATES_PATH = REPO_ROOT / "paperAnalysis" / "processing" / "unified_paper_duplicates.csv"

CSV_FIELDS = [
    "state",
    "importance",
    "paper_title",
    "venue",
    "project_link_or_github_link",
    "paper_link",
    "sort",
    "pdf_path",
]

LOG_STATES_WITH_LOCAL_FILE = {"Downloaded", "checked"}
TARGET_STATES = {"Wait", "Missing", "Downloaded", "checked"}
SKIP_STATES = {"Skip"}
DEFAULT_IMPORTANCE = "Unrated"
DEFAULT_PROJECT_LINK = "N/A"
DEFAULT_PAPER_LINK = "N/A"
DEFAULT_SORT = "Uncategorized"
DEFAULT_VENUE = "Unknown"
MIN_PDF_BYTES = 5_000
THREAD_TIMEOUT = 90
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
}
ARXIV_ID_RE = re.compile(r"(?P<id>\d{4}\.\d{4,5})(?:v\d+)?")
OPENREVIEW_ID_RE = re.compile(r"openreview\.net/(?:forum|pdf)\?id=([^&#]+)", re.I)
DOI_ARXIV_RE = re.compile(r"doi\.org/10\.48550/arxiv\.([0-9]{4}\.[0-9]{4,5})", re.I)
YEAR_RE = re.compile(r"\b((?:19|20)\d{2})\b")
PDF_URL_PATTERNS = [
    re.compile(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']', re.I),
    re.compile(r'<meta[^>]+property=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']', re.I),
    re.compile(r'"citation_pdf_url"\s*:\s*"([^"]+)"', re.I),
    re.compile(r'"pdfUrl"\s*:\s*"([^"]+)"', re.I),
    re.compile(r'"pdf_url"\s*:\s*"([^"]+)"', re.I),
    re.compile(r'"pdfPath"\s*:\s*"([^"]+)"', re.I),
    re.compile(r"href=[\"']([^\"']+\.pdf(?:\?[^\"']*)?)[\"']", re.I),
]


@dataclass(frozen=True)
class LogSpec:
    batch: str
    repo: str
    target_log: Path
    collect_log: Path | None = None


@dataclass
class LoadedLog:
    spec: LogSpec
    rows: list[dict[str, str]]
    created_from_collect: bool = False
    collect_sync_updates: int = 0


@dataclass
class ExistingPdfRecord:
    title: str
    paper_link: str
    pdf_path: str
    source_log: str
    state: str


@dataclass
class RowRef:
    log_path: Path
    row_index: int


@dataclass
class DownloadTask:
    key: str
    title: str
    canonical_pdf_path: str
    candidate_urls: list[str]
    row_refs: list[RowRef] = field(default_factory=list)
    link_keys: set[str] = field(default_factory=set)
    title_keys: set[str] = field(default_factory=set)


@dataclass
class DownloadOutcome:
    key: str
    success: bool
    reason: str
    pdf_path: str
    source_url: str = ""
    reused_existing: bool = False
    downloaded: bool = False
    dry_run: bool = False


def lower_repo_slug(repo: str) -> str:
    return repo.replace("/", "__").lower()


def target_log_for_repo(repo: str) -> Path:
    if repo.lower() == "foruck/awesome-human-motion":
        return GLOBAL_LOG
    return PROCESSING_ROOT / lower_repo_slug(repo) / "analysis_log.csv"


def collect_log_for_repo(repo: str) -> Path | None:
    target_slug = lower_repo_slug(repo)
    for path in sorted(COLLECT_LOG_ROOT.glob("*.auto.csv")):
        file_slug = path.name[: -len(".auto.csv")].lower()
        if file_slug == target_slug:
            return path
    return None


def build_log_spec(selector: str, repo: str) -> LogSpec:
    return LogSpec(
        batch=selector,
        repo=repo,
        target_log=target_log_for_repo(repo),
        collect_log=collect_log_for_repo(repo),
    )


def load_priority_repo_map() -> dict[str, str]:
    if not QUEUE_PRIORITY_PATH.exists():
        return {}
    mapping: dict[str, str] = {}
    for raw_line in QUEUE_PRIORITY_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("| P"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 4:
            continue
        priority = parts[0]
        repo = parts[3].strip("`")
        if priority and repo:
            mapping[priority] = repo
    return mapping


def build_batch_specs() -> dict[str, list[LogSpec]]:
    batch1_repos = [
        "BradyFU/Awesome-Multimodal-Large-Language-Models",
        "MrNeRF/awesome-3D-gaussian-splatting",
        "showlab/Awesome-Video-Diffusion",
        "atfortes/Awesome-LLM-Reasoning",
        "horseee/Awesome-Efficient-LLM",
        "jonyzhang2023/awesome-embodied-vla-va-vln",
        "weitianxin/Awesome-Agentic-Reasoning",
    ]
    batch2_repos = [
        "knightnemo/Awesome-World-Models",
        "jxzhangjhu/Awesome-LLM-RAG",
        "justimyhxu/awesome-3D-generation",
        "mayuelala/Awesome-Controllable-Video-Generation",
        "ga642381/speech-trident",
        "HITsz-TMG/Awesome-Large-Multimodal-Reasoning-Models",
    ]
    batch3_repos = [
        "weihaox/awesome-digital-human",
        "soraproducer/awesome-human-interaction-motion-generation",
        "Zilize/awesome-text-to-motion",
        "worldbench/awesome-3d-4d-world-models",
    ]

    selectors: dict[str, list[LogSpec]] = {
        "P0": [build_log_spec("P0", "Foruck/Awesome-Human-Motion")],
        "P1": [build_log_spec("P1", repo) for repo in batch1_repos],
        "P2": [build_log_spec("P2", repo) for repo in batch2_repos],
        "B1": [build_log_spec("B1", repo) for repo in batch1_repos],
        "B2": [build_log_spec("B2", repo) for repo in batch2_repos],
        "B3": [build_log_spec("B3", repo) for repo in batch3_repos],
    }

    for priority, repo in load_priority_repo_map().items():
        if priority in selectors:
            continue
        selectors[priority] = [build_log_spec(priority, repo)]

    return selectors


def rel_path(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def normalize_text(text: str) -> str:
    text = normalize_spaces(text).lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "", text)


def normalize_title_key(title: str) -> str:
    key = normalize_text(title)
    return f"title:{key}" if key else ""


def normalize_paper_link(url: str) -> str:
    url = normalize_spaces(url).rstrip(").,;")
    if not url or url.upper() == "N/A":
        return ""
    doi_match = DOI_ARXIV_RE.search(url)
    if doi_match:
        return f"https://arxiv.org/abs/{doi_match.group(1)}"
    arxiv_match = ARXIV_ID_RE.search(url) if "arxiv.org" in url.lower() else None
    if arxiv_match:
        return f"https://arxiv.org/abs/{arxiv_match.group('id')}"
    openreview_match = OPENREVIEW_ID_RE.search(url)
    if openreview_match:
        return f"https://openreview.net/forum?id={openreview_match.group(1)}"
    return url


def extract_year(text: str) -> str:
    match = YEAR_RE.search(text or "")
    return match.group(1) if match else "UnknownYear"


def infer_arxiv_year(url: str) -> str:
    match = ARXIV_ID_RE.search(url or "")
    if not match:
        return ""
    prefix = match.group("id").split(".", 1)[0]
    if len(prefix) != 4:
        return ""
    return f"20{prefix[:2]}"


def canonicalize_venue(row: dict[str, str]) -> str:
    venue = normalize_spaces(row.get("venue", "")) or DEFAULT_VENUE
    paper_link = row.get("paper_link", "")
    venue_lower = venue.lower()
    arxiv_year = infer_arxiv_year(paper_link)

    if "arxiv" in venue_lower:
        return f"arXiv {extract_year(venue) if extract_year(venue) != 'UnknownYear' else arxiv_year}".strip()

    noisy_markers = ("homepage", "project page", "produced by", "http://", "https://")
    if arxiv_year and any(marker in venue_lower for marker in noisy_markers):
        return f"arXiv {arxiv_year}"

    return venue


def sanitize_title_for_filename(title: str, max_len: int = 160) -> str:
    value = (title or "").strip()
    value = value.replace("\u2013", "-").replace("\u2014", "-")
    value = re.sub(r"\s+", " ", value)
    value = value.replace(" ", "_").replace("-", "_")
    value = re.sub(r"[<>:\"/\\\\|?*\x00-\x1F,]", "_", value)
    value = re.sub(r"_+", "_", value).strip("_. ")
    if not value:
        value = "Untitled"
    if len(value) > max_len:
        value = value[:max_len].rstrip("_")
    return value


def sanitize_venue_dir(venue: str) -> str:
    value = (venue or "").strip() or DEFAULT_VENUE
    value = value.replace("\u2013", "-").replace("\u2014", "-")
    value = value.replace(" ", "_")
    value = re.sub(r"[<>:\"/\\\\|?*\x00-\x1F,]", "_", value)
    value = re.sub(r"_+", "_", value).strip("_. ")
    return value or DEFAULT_VENUE


def sanitize_sort_dir(sort_value: str) -> str:
    value = normalize_spaces(sort_value) or DEFAULT_SORT
    value = value.replace("/", "_").replace("\\", "_")
    value = re.sub(r"[<>:\"|?*\x00-\x1F]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_. ")
    return value or DEFAULT_SORT


def build_pdf_path(row: dict[str, str]) -> str:
    sort_value = sanitize_sort_dir(row.get("sort", ""))
    venue_value = normalize_spaces(row.get("venue", "")) or DEFAULT_VENUE
    title_value = normalize_spaces(row.get("paper_title", "")) or "Untitled"
    year = extract_year(venue_value)
    filename = f"{year}_{sanitize_title_for_filename(title_value)}.pdf"
    return f"paperPDFs/{sort_value}/{sanitize_venue_dir(venue_value)}/{filename}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in CSV_FIELDS})


def ensure_row_defaults(row: dict[str, str]) -> None:
    row["state"] = normalize_spaces(row.get("state", "")) or "Wait"
    row["importance"] = normalize_spaces(row.get("importance", "")) or DEFAULT_IMPORTANCE
    row["paper_title"] = normalize_spaces(row.get("paper_title", ""))
    row["venue"] = canonicalize_venue(row)
    row["project_link_or_github_link"] = normalize_spaces(
        row.get("project_link_or_github_link", "")
    ) or DEFAULT_PROJECT_LINK
    row["paper_link"] = normalize_spaces(row.get("paper_link", "")) or DEFAULT_PAPER_LINK
    row["sort"] = normalize_spaces(row.get("sort", "")) or DEFAULT_SORT
    row["pdf_path"] = normalize_spaces(row.get("pdf_path", "")) or build_pdf_path(row)


def value_quality(value: str) -> int:
    cleaned = normalize_spaces(value)
    if not cleaned:
        return 0
    if cleaned in {"Unknown", "N/A", "UnknownYear", DEFAULT_VENUE}:
        return 1
    return 2


def row_link_key(row: dict[str, str]) -> str:
    normalized = normalize_paper_link(row.get("paper_link", ""))
    return f"link:{normalized}" if normalized else ""


def row_title_key(row: dict[str, str]) -> str:
    return normalize_title_key(row.get("paper_title", ""))


def build_source_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    lookup: dict[str, dict[str, str]] = {}
    for row in rows:
        for key in (row_link_key(row), row_title_key(row)):
            if key:
                lookup[key] = row
    return lookup


def sync_rows_from_collect(target_rows: list[dict[str, str]], collect_rows: list[dict[str, str]]) -> int:
    lookup = build_source_lookup(collect_rows)
    updates = 0
    for row in target_rows:
        candidate = None
        for key in (row_link_key(row), row_title_key(row)):
            if key and key in lookup:
                candidate = lookup[key]
                break
        if candidate is None:
            continue
        for field in CSV_FIELDS:
            if field == "state":
                if row.get(field, "").strip() in {"", "Wait"} and candidate.get(field, "").strip():
                    row[field] = candidate[field]
                    updates += 1
                continue
            target_value = row.get(field, "")
            source_value = candidate.get(field, "")
            if value_quality(source_value) > value_quality(target_value):
                row[field] = source_value
                updates += 1
    return updates


def pdf_bytes_look_valid(data: bytes) -> bool:
    if len(data) < MIN_PDF_BYTES:
        return False
    return b"%PDF" in data[:1024]


def pdf_file_looks_valid(path: Path) -> bool:
    try:
        if not path.is_file() or path.stat().st_size < MIN_PDF_BYTES:
            return False
        with path.open("rb") as f:
            head = f.read(1024)
        return b"%PDF" in head
    except OSError:
        return False


def prefer_checked_state(state: str) -> bool:
    return state == "checked"


def advance_state_for_ready_pdf(row: dict[str, str]) -> None:
    if prefer_checked_state(row.get("state", "")):
        return
    if row.get("state") in SKIP_STATES:
        return
    row["state"] = "Downloaded"


def candidate_urls_from_row(row: dict[str, str]) -> list[str]:
    urls: list[str] = []
    for value in (row.get("paper_link", ""), row.get("project_link_or_github_link", "")):
        value = normalize_spaces(value)
        if not value or value.upper() == "N/A":
            continue
        if value.startswith("http"):
            urls.append(value)
    out: list[str] = []
    seen: set[str] = set()
    for url in urls:
        if url not in seen:
            out.append(url)
            seen.add(url)
    return out


def iter_special_url_variants(url: str) -> list[str]:
    variants: list[str] = []
    seen: set[str] = set()

    def add(candidate: str) -> None:
        candidate = normalize_spaces(candidate)
        if not candidate or candidate in seen:
            return
        seen.add(candidate)
        variants.append(candidate)

    add(url)
    lower = url.lower()
    parsed = urlparse(url)

    if "arxiv.org" in lower:
        arxiv_match = ARXIV_ID_RE.search(url)
        if arxiv_match:
            arxiv_id = arxiv_match.group("id")
            add(f"https://arxiv.org/pdf/{arxiv_id}.pdf")
            add(f"https://arxiv.org/abs/{arxiv_id}")
    elif parsed.netloc == "arxiv.org" and ARXIV_ID_RE.search(parsed.path):
        arxiv_id = ARXIV_ID_RE.search(parsed.path).group("id")  # type: ignore[union-attr]
        add(f"https://arxiv.org/pdf/{arxiv_id}.pdf")

    doi_match = DOI_ARXIV_RE.search(url)
    if doi_match:
        add(f"https://arxiv.org/pdf/{doi_match.group(1)}.pdf")

    openreview_match = OPENREVIEW_ID_RE.search(url)
    if openreview_match:
        openreview_id = openreview_match.group(1)
        add(f"https://openreview.net/pdf?id={openreview_id}")
        add(f"https://openreview.net/forum?id={openreview_id}")

    if "openaccess.thecvf.com" in lower and parsed.path.endswith(".html"):
        add(url.replace("/html/", "/content/").replace(".html", ".pdf"))

    if "aclanthology.org" in lower and not lower.endswith(".pdf"):
        add(url.rstrip("/") + ".pdf")

    if "dl.acm.org/doi/" in lower and "/doi/pdf/" not in lower:
        add(url.replace("/doi/", "/doi/pdf/"))

    if "ieeexplore.ieee.org" in lower:
        arnumber = re.search(r"/document/(\d+)", url)
        if arnumber:
            add(f"https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber={arnumber.group(1)}")

    if "nature.com" in lower and not lower.endswith(".pdf"):
        add(url.rstrip("/") + ".pdf")

    if "link.springer.com/article/" in lower:
        doi_part = parsed.path.split("/article/", 1)[1]
        add(f"https://link.springer.com/content/pdf/{doi_part}.pdf")

    return variants


def extract_pdf_candidates(base_url: str, html: str) -> list[str]:
    candidates: list[str] = []
    seen: set[str] = set()

    def add(candidate: str) -> None:
        candidate = normalize_spaces(candidate)
        if not candidate:
            return
        candidate = candidate.replace("\\/", "/")
        if candidate.startswith("//"):
            parsed = urlparse(base_url)
            candidate = f"{parsed.scheme}:{candidate}"
        candidate = urljoin(base_url, candidate)
        if candidate in seen:
            return
        seen.add(candidate)
        candidates.append(candidate)

    for pattern in PDF_URL_PATTERNS:
        for match in pattern.finditer(html):
            add(next(group for group in match.groups() if group))

    arxiv_match = ARXIV_ID_RE.search(html)
    if arxiv_match:
        add(f"https://arxiv.org/pdf/{arxiv_match.group('id')}.pdf")

    openreview_match = OPENREVIEW_ID_RE.search(html)
    if openreview_match:
        add(f"https://openreview.net/pdf?id={openreview_match.group(1)}")

    doi_match = DOI_ARXIV_RE.search(html)
    if doi_match:
        add(f"https://arxiv.org/pdf/{doi_match.group(1)}.pdf")

    return candidates


def search_arxiv_pdf_by_title(title: str) -> str:
    title = normalize_spaces(title)
    if not title:
        return ""
    session = requests.Session()
    queries = [f'ti:"{title}"', title]
    for query in queries:
        url = (
            "https://export.arxiv.org/api/query?search_query="
            f"{quote(query)}&start=0&max_results=5"
        )
        try:
            response = session.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            root = ET.fromstring(response.content)
        except Exception:
            continue
        best_score = 0.0
        best_pdf = ""
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            raw_title = entry.findtext("{http://www.w3.org/2005/Atom}title", default="")
            normalized_entry_title = normalize_spaces(raw_title)
            score = difflib.SequenceMatcher(
                None,
                normalize_text(title),
                normalize_text(normalized_entry_title),
            ).ratio()
            entry_id = entry.findtext("{http://www.w3.org/2005/Atom}id", default="")
            arxiv_match = ARXIV_ID_RE.search(entry_id)
            if score > best_score and arxiv_match:
                best_score = score
                best_pdf = f"https://arxiv.org/pdf/{arxiv_match.group('id')}.pdf"
        if best_score >= 0.82 and best_pdf:
            return best_pdf
    return ""


def fetch_response(url: str, session: requests.Session) -> requests.Response:
    response = session.get(url, headers=HEADERS, timeout=THREAD_TIMEOUT, allow_redirects=True)
    response.raise_for_status()
    return response


def write_pdf_bytes(dest: Path, data: bytes) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = dest.with_suffix(dest.suffix + ".part")
    with tmp_path.open("wb") as f:
        f.write(data)
    tmp_path.replace(dest)


def compress_pdf_if_needed(path: Path, max_mb: int = 20) -> str:
    if not path.is_file():
        return ""
    if path.stat().st_size <= max_mb * 1024 * 1024:
        return ""
    if shutil.which("gs") is None:
        return "ghostscript_missing"

    def run_compress(setting: str, suffix: str) -> Path | None:
        output = path.with_name(f"{path.stem}.{suffix}.pdf")
        cmd = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS=/{setting}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output}",
            str(path),
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except Exception:
            return None
        if not pdf_file_looks_valid(output):
            output.unlink(missing_ok=True)
            return None
        return output

    original_size = path.stat().st_size
    for setting, suffix in (("ebook", "ebook"), ("screen", "screen")):
        compressed = run_compress(setting, suffix)
        if compressed is None:
            continue
        if compressed.stat().st_size < original_size:
            compressed.replace(path)
            return f"compressed:{setting}"
        compressed.unlink(missing_ok=True)
    return "compress_no_gain"


def download_pdf_from_response(response: requests.Response, dest: Path) -> tuple[bool, str]:
    content_type = response.headers.get("Content-Type", "").lower()
    data = response.content
    if "application/pdf" not in content_type and not pdf_bytes_look_valid(data):
        return False, f"not_pdf:{content_type or 'unknown'}"
    try:
        write_pdf_bytes(dest, data)
    except Exception as exc:
        return False, f"write_failed:{type(exc).__name__}"
    if not pdf_file_looks_valid(dest):
        dest.unlink(missing_ok=True)
        return False, "invalid_pdf_signature"
    compress_note = compress_pdf_if_needed(dest)
    return True, compress_note or "downloaded"


def download_pdf_from_url(url: str, dest: Path, session: requests.Session) -> tuple[bool, str]:
    try:
        response = fetch_response(url, session)
    except Exception as exc:
        return False, f"request_failed:{type(exc).__name__}"
    return download_pdf_from_response(response, dest)


def try_candidate_once(
    current: str,
    dest: Path,
    session: requests.Session,
) -> tuple[bool, str, str, list[str]]:
    try:
        response = fetch_response(current, session)
    except Exception as exc:
        return False, current, f"request_failed:{type(exc).__name__}", []

    ok, note = download_pdf_from_response(response, dest)
    if ok:
        return True, current, note, []

    content_type = response.headers.get("Content-Type", "").lower()
    if "html" in content_type or "text" in content_type:
        return False, current, note, extract_pdf_candidates(response.url, response.text)
    return False, current, note, []


def try_download_candidate(
    title: str,
    candidate_url: str,
    dest: Path,
    session: requests.Session,
) -> tuple[bool, str, str]:
    attempted: set[str] = set()
    queue: list[str] = iter_special_url_variants(candidate_url)

    while queue:
        current = queue.pop(0)
        if current in attempted:
            continue
        attempted.add(current)

        ok, source_url, note, extracted = try_candidate_once(current, dest, session)
        if ok:
            return True, source_url, note

        for extracted_url in extracted:
            if extracted_url not in attempted:
                queue.append(extracted_url)

    fallback_pdf = search_arxiv_pdf_by_title(title)
    if fallback_pdf and fallback_pdf not in attempted:
        ok, note = download_pdf_from_url(fallback_pdf, dest, session)
        if ok:
            return True, fallback_pdf, note
        return False, fallback_pdf, note

    return False, "", "all_candidates_failed"


def execute_download_task(task: DownloadTask, dry_run: bool) -> DownloadOutcome:
    dest = REPO_ROOT / task.canonical_pdf_path
    if pdf_file_looks_valid(dest):
        return DownloadOutcome(
            key=task.key,
            success=True,
            reason="already_present",
            pdf_path=task.canonical_pdf_path,
            source_url="",
            reused_existing=True,
            dry_run=dry_run,
        )

    if dry_run:
        chosen_url = task.candidate_urls[0] if task.candidate_urls else search_arxiv_pdf_by_title(task.title)
        success = bool(chosen_url)
        return DownloadOutcome(
            key=task.key,
            success=success,
            reason="dry_run_ok" if success else "dry_run_no_candidate",
            pdf_path=task.canonical_pdf_path,
            source_url=chosen_url,
            dry_run=True,
        )

    session = requests.Session()
    for candidate_url in task.candidate_urls:
        ok, source_url, reason = try_download_candidate(task.title, candidate_url, dest, session)
        if ok:
            return DownloadOutcome(
                key=task.key,
                success=True,
                reason=reason,
                pdf_path=task.canonical_pdf_path,
                source_url=source_url,
                downloaded=True,
            )

    fallback_pdf = search_arxiv_pdf_by_title(task.title)
    if fallback_pdf:
        ok, note = download_pdf_from_url(fallback_pdf, dest, session)
        if ok:
            return DownloadOutcome(
                key=task.key,
                success=True,
                reason=note,
                pdf_path=task.canonical_pdf_path,
                source_url=fallback_pdf,
                downloaded=True,
            )
        return DownloadOutcome(
            key=task.key,
            success=False,
            reason=note,
            pdf_path=task.canonical_pdf_path,
            source_url=fallback_pdf,
        )

    return DownloadOutcome(
        key=task.key,
        success=False,
        reason="no_resolved_pdf_source",
        pdf_path=task.canonical_pdf_path,
    )


def prepare_loaded_logs(selected_batches: list[str]) -> tuple[list[LoadedLog], list[dict[str, str]]]:
    specs_by_batch = build_batch_specs()
    loaded: list[LoadedLog] = []
    missing: list[dict[str, str]] = []

    for batch in selected_batches:
        for spec in specs_by_batch[batch]:
            target_exists = spec.target_log.exists()
            collect_exists = spec.collect_log.exists() if spec.collect_log else False

            if not target_exists and not collect_exists:
                missing.append(
                    {
                        "batch": spec.batch,
                        "repo": spec.repo,
                        "reason": "missing_processing_and_collect_log",
                        "target_log": rel_path(spec.target_log),
                    }
                )
                continue

            created_from_collect = False
            rows: list[dict[str, str]]
            if target_exists:
                rows = read_csv_rows(spec.target_log)
            else:
                rows = read_csv_rows(spec.collect_log)  # type: ignore[arg-type]
                created_from_collect = True

            collect_sync_updates = 0
            if collect_exists:
                collect_rows = read_csv_rows(spec.collect_log)  # type: ignore[arg-type]
                collect_sync_updates = sync_rows_from_collect(rows, collect_rows)

            for row in rows:
                ensure_row_defaults(row)

            loaded.append(
                LoadedLog(
                    spec=spec,
                    rows=rows,
                    created_from_collect=created_from_collect,
                    collect_sync_updates=collect_sync_updates,
                )
            )
    return loaded, missing


def canonicalize_pdf_paths(loaded_logs: list[LoadedLog], dry_run: bool) -> dict[str, int]:
    rewrites: dict[str, int] = defaultdict(int)
    for loaded in loaded_logs:
        log_key = rel_path(loaded.spec.target_log)
        for row in loaded.rows:
            current_rel = normalize_spaces(row.get("pdf_path", ""))
            canonical_rel = build_pdf_path(row)
            if not current_rel:
                row["pdf_path"] = canonical_rel
                rewrites[log_key] += 1
                continue
            if current_rel == canonical_rel:
                continue
            current_abs = REPO_ROOT / current_rel
            canonical_abs = REPO_ROOT / canonical_rel
            if not dry_run and pdf_file_looks_valid(current_abs) and not pdf_file_looks_valid(canonical_abs):
                canonical_abs.parent.mkdir(parents=True, exist_ok=True)
                current_abs.replace(canonical_abs)
            row["pdf_path"] = canonical_rel
            rewrites[log_key] += 1
    return rewrites


def scan_existing_pdf_index() -> tuple[dict[str, ExistingPdfRecord], dict[str, ExistingPdfRecord]]:
    link_index: dict[str, ExistingPdfRecord] = {}
    title_index: dict[str, ExistingPdfRecord] = {}
    log_paths = [GLOBAL_LOG, *sorted(PROCESSING_ROOT.glob("*/analysis_log.csv"))]
    for log_path in log_paths:
        if not log_path.exists():
            continue
        try:
            rows = read_csv_rows(log_path)
        except Exception:
            continue
        for row in rows:
            pdf_rel = normalize_spaces(row.get("pdf_path", ""))
            if not pdf_rel:
                continue
            pdf_abs = REPO_ROOT / pdf_rel
            if not pdf_file_looks_valid(pdf_abs):
                continue
            record = ExistingPdfRecord(
                title=row.get("paper_title", ""),
                paper_link=row.get("paper_link", ""),
                pdf_path=pdf_rel,
                source_log=rel_path(log_path),
                state=row.get("state", ""),
            )
            if row_link_key(row):
                link_index.setdefault(row_link_key(row), record)
            if row_title_key(row):
                title_index.setdefault(row_title_key(row), record)
    return link_index, title_index


def build_download_tasks(
    loaded_logs: list[LoadedLog],
    link_index: dict[str, ExistingPdfRecord],
    title_index: dict[str, ExistingPdfRecord],
    stats: dict[str, dict[str, int]],
) -> list[DownloadTask]:
    groups: dict[str, DownloadTask] = {}
    group_by_link: dict[str, str] = {}
    group_by_title: dict[str, str] = {}
    log_lookup = {loaded.spec.target_log: loaded for loaded in loaded_logs}

    for loaded in loaded_logs:
        log_key = rel_path(loaded.spec.target_log)
        stats[log_key]["rows_total"] += len(loaded.rows)
        if loaded.created_from_collect:
            stats[log_key]["created_from_collect"] += 1
        stats[log_key]["collect_sync_updates"] += loaded.collect_sync_updates

        for row_index, row in enumerate(loaded.rows):
            if row.get("state") in SKIP_STATES:
                stats[log_key]["skipped"] += 1
                continue

            pdf_abs = REPO_ROOT / row["pdf_path"]
            if pdf_file_looks_valid(pdf_abs):
                advance_state_for_ready_pdf(row)
                record = ExistingPdfRecord(
                    title=row["paper_title"],
                    paper_link=row["paper_link"],
                    pdf_path=row["pdf_path"],
                    source_log=log_key,
                    state=row["state"],
                )
                if row_link_key(row):
                    link_index[row_link_key(row)] = record
                if row_title_key(row):
                    title_index[row_title_key(row)] = record
                stats[log_key]["already_present"] += 1
                continue

            existing = None
            for key in (row_link_key(row), row_title_key(row)):
                if key and key in link_index:
                    existing = link_index[key]
                    break
                if key and key in title_index:
                    existing = title_index[key]
                    break
            if existing is not None and pdf_file_looks_valid(REPO_ROOT / existing.pdf_path):
                row["pdf_path"] = existing.pdf_path
                advance_state_for_ready_pdf(row)
                stats[log_key]["reused_from_global_index"] += 1
                continue

            if row.get("state") not in TARGET_STATES:
                stats[log_key]["ignored_non_target_state"] += 1
                continue

            link_key = row_link_key(row)
            title_key = row_title_key(row)
            primary_key = link_key or title_key or f"row:{log_key}:{row_index}"
            group_key = primary_key
            if link_key and link_key in group_by_link:
                group_key = group_by_link[link_key]
            elif title_key and title_key in group_by_title:
                group_key = group_by_title[title_key]

            if group_key not in groups:
                groups[group_key] = DownloadTask(
                    key=group_key,
                    title=row["paper_title"],
                    canonical_pdf_path=row["pdf_path"],
                    candidate_urls=candidate_urls_from_row(row),
                )
            task = groups[group_key]
            task.row_refs.append(RowRef(loaded.spec.target_log, row_index))
            if link_key:
                task.link_keys.add(link_key)
                group_by_link[link_key] = group_key
            if title_key:
                task.title_keys.add(title_key)
                group_by_title[title_key] = group_key
            for url in candidate_urls_from_row(row):
                if url not in task.candidate_urls:
                    task.candidate_urls.append(url)

    # Keep canonical path stable inside each dedupe group.
    for task in groups.values():
        if not task.canonical_pdf_path:
            first_ref = task.row_refs[0]
            first_row = log_lookup[first_ref.log_path].rows[first_ref.row_index]
            task.canonical_pdf_path = first_row["pdf_path"]

    return list(groups.values())


def write_loaded_logs(loaded_logs: list[LoadedLog], dry_run: bool) -> None:
    if dry_run:
        return
    for loaded in loaded_logs:
        write_csv_rows(loaded.spec.target_log, loaded.rows)


def better_row(lhs: dict[str, str], rhs: dict[str, str]) -> dict[str, str]:
    def score(row: dict[str, str]) -> tuple[int, int, int]:
        state = row.get("state", "")
        pdf_ok = int(pdf_file_looks_valid(REPO_ROOT / row.get("pdf_path", "")))
        state_rank = {"checked": 4, "Downloaded": 3, "Wait": 2, "Missing": 1, "Skip": 0}.get(state, 0)
        link_rank = int(row.get("paper_link", "").upper() != "N/A")
        return (pdf_ok, state_rank, link_rank)

    return lhs if score(lhs) >= score(rhs) else rhs


def build_unified_index() -> dict[str, int]:
    log_paths = [GLOBAL_LOG, *sorted(PROCESSING_ROOT.glob("*/analysis_log.csv"))]
    groups: dict[str, list[tuple[Path, dict[str, str]]]] = {}
    link_to_group: dict[str, str] = {}
    title_to_group: dict[str, str] = {}

    for log_path in log_paths:
        if not log_path.exists():
            continue
        try:
            rows = read_csv_rows(log_path)
        except Exception:
            continue
        for row in rows:
            ensure_row_defaults(row)
            link_key = row_link_key(row)
            title_key = row_title_key(row)
            group_key = link_key or title_key
            if link_key and link_key in link_to_group:
                group_key = link_to_group[link_key]
            elif title_key and title_key in title_to_group:
                group_key = title_to_group[title_key]
            if not group_key:
                continue
            groups.setdefault(group_key, []).append((log_path, row))
            if link_key:
                link_to_group[link_key] = group_key
            if title_key:
                title_to_group[title_key] = group_key

    unified_rows: list[dict[str, str]] = []
    duplicate_rows: list[dict[str, str]] = []
    duplicate_group_count = 0

    for group_key, members in sorted(groups.items()):
        canonical_row = members[0][1]
        for _path, row in members[1:]:
            canonical_row = better_row(canonical_row, row)
        duplicate_group_count += int(len(members) > 1)
        source_logs = []
        for log_path, row in members:
            source_logs.append(rel_path(log_path))
            duplicate_rows.append(
                {
                    "dedupe_key": group_key,
                    "source_log": rel_path(log_path),
                    "state": row["state"],
                    "paper_title": row["paper_title"],
                    "venue": row["venue"],
                    "paper_link": row["paper_link"],
                    "pdf_path": row["pdf_path"],
                }
            )
        canonical_pdf_abs = REPO_ROOT / canonical_row["pdf_path"]
        unified_rows.append(
            {
                "dedupe_key": group_key,
                "paper_title": canonical_row["paper_title"],
                "venue": canonical_row["venue"],
                "paper_link": canonical_row["paper_link"],
                "pdf_path": canonical_row["pdf_path"],
                "pdf_exists": "yes" if pdf_file_looks_valid(canonical_pdf_abs) else "no",
                "state": canonical_row["state"],
                "source_count": str(len(set(source_logs))),
                "row_count": str(len(members)),
                "source_logs": ";".join(sorted(set(source_logs))),
            }
        )

    UNIFIED_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with UNIFIED_INDEX_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "dedupe_key",
                "paper_title",
                "venue",
                "paper_link",
                "pdf_path",
                "pdf_exists",
                "state",
                "source_count",
                "row_count",
                "source_logs",
            ],
        )
        writer.writeheader()
        writer.writerows(unified_rows)

    with UNIFIED_DUPLICATES_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["dedupe_key", "source_log", "state", "paper_title", "venue", "paper_link", "pdf_path"],
        )
        writer.writeheader()
        writer.writerows(duplicate_rows)

    return {
        "unified_rows": len(unified_rows),
        "duplicate_groups": duplicate_group_count,
        "duplicate_rows": len(duplicate_rows),
    }


def batched(items: list[DownloadTask], batch_size: int) -> Iterable[list[DownloadTask]]:
    for start in range(0, len(items), batch_size):
        yield items[start : start + batch_size]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download PDFs for repo-local/global 8-column analysis_log.csv files and refresh unified dedupe index."
    )
    parser.add_argument(
        "--batches",
        default="P0,P1,P2",
        help=(
            "Comma-separated selectors to process. "
            "Historical batch presets: P0,P1,P2,B1,B2,B3. "
            "Queue-priority selectors from collect_priority_queue: P3..P17."
        ),
    )
    parser.add_argument("--workers", type=int, default=8, help="Concurrent download workers.")
    parser.add_argument(
        "--flush-every",
        type=int,
        default=24,
        help="Write logs after each completed chunk of this many unique paper tasks.",
    )
    parser.add_argument(
        "--limit-groups",
        type=int,
        default=0,
        help="Only process the first N unique paper tasks after dedupe. Useful for validation.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Resolve and plan without writing files.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requested_batches = [part.strip().upper() for part in args.batches.split(",") if part.strip()]
    specs_by_batch = build_batch_specs()
    invalid = [batch for batch in requested_batches if batch not in specs_by_batch]
    if invalid:
        raise SystemExit(f"Unknown batches: {', '.join(invalid)}")

    started_at = time.strftime("%Y%m%d_%H%M%S")
    report_dir = REPORT_ROOT / started_at
    report_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] preparing logs for batches: {', '.join(requested_batches)}")
    loaded_logs, missing_specs = prepare_loaded_logs(requested_batches)
    if not loaded_logs:
        raise SystemExit("No collected logs were available for the requested batches.")

    path_rewrites = canonicalize_pdf_paths(loaded_logs, dry_run=args.dry_run)
    write_loaded_logs(loaded_logs, dry_run=args.dry_run)

    stats: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for log_path, count in path_rewrites.items():
        stats[log_path]["pdf_path_canonicalized"] += count
    link_index, title_index = scan_existing_pdf_index()
    tasks = build_download_tasks(loaded_logs, link_index, title_index, stats)
    total_unique_tasks = len(tasks)
    if args.limit_groups > 0:
        tasks = tasks[: args.limit_groups]

    print(
        f"[INFO] loaded {len(loaded_logs)} logs; "
        f"missing/uncollected repos: {len(missing_specs)}; "
        f"unique download tasks after dedupe: {total_unique_tasks}"
    )
    if args.limit_groups > 0:
        print(f"[INFO] limiting this run to the first {len(tasks)} unique tasks")

    chunk_size = max(args.workers, args.flush_every)
    for chunk_index, chunk in enumerate(batched(tasks, chunk_size), start=1):
        print(f"[INFO] processing chunk {chunk_index} with {len(chunk)} tasks")
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(execute_download_task, task, args.dry_run): task for task in chunk}
            for future in concurrent.futures.as_completed(futures):
                task = futures[future]
                outcome = future.result()
                for loaded in loaded_logs:
                    log_key = rel_path(loaded.spec.target_log)
                    row_indices = [
                        ref.row_index
                        for ref in task.row_refs
                        if ref.log_path == loaded.spec.target_log
                    ]
                    if not row_indices:
                        continue
                    for row_index in row_indices:
                        row = loaded.rows[row_index]
                        row["pdf_path"] = outcome.pdf_path
                        if outcome.success:
                            advance_state_for_ready_pdf(row)
                            if outcome.reused_existing:
                                stats[log_key]["reused_from_task_dest"] += 1
                            elif outcome.downloaded:
                                stats[log_key]["downloaded_now"] += 1
                            elif outcome.dry_run:
                                stats[log_key]["dry_run_resolvable"] += 1
                        else:
                            if row.get("state") not in {"checked", "Skip"}:
                                row["state"] = "Missing"
                            stats[log_key]["marked_missing"] += 1
                if outcome.success and not args.dry_run:
                    record = ExistingPdfRecord(
                        title=task.title,
                        paper_link="",
                        pdf_path=outcome.pdf_path,
                        source_log="runtime",
                        state="Downloaded",
                    )
                    for key in task.link_keys:
                        link_index[key] = record
                    for key in task.title_keys:
                        title_index[key] = record

        write_loaded_logs(loaded_logs, dry_run=args.dry_run)

    unified_summary = build_unified_index()

    report = {
        "started_at": started_at,
        "dry_run": args.dry_run,
        "batches": requested_batches,
        "workers": args.workers,
        "total_loaded_logs": len(loaded_logs),
        "total_unique_tasks_before_limit": total_unique_tasks,
        "total_unique_tasks_this_run": len(tasks),
        "missing_specs": missing_specs,
        "log_stats": {log_path: dict(values) for log_path, values in stats.items()},
        "unified_index": unified_summary,
    }
    report_path = report_dir / "summary.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[INFO] unified index written to: {rel_path(UNIFIED_INDEX_PATH)}")
    print(f"[INFO] duplicate report written to: {rel_path(UNIFIED_DUPLICATES_PATH)}")
    print(f"[INFO] run summary written to: {rel_path(report_path)}")
    print("[INFO] per-log stats:")
    for log_path, values in sorted(report["log_stats"].items()):
        print(f"  - {log_path}: {values}")
    if missing_specs:
        print("[WARN] missing/uncollected repos:")
        for item in missing_specs:
            print(f"  - {item['batch']} {item['repo']}: {item['reason']}")


if __name__ == "__main__":
    main()
