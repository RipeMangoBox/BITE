#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import difflib
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from typing import Any, Iterable

try:
    import requests
except ImportError as exc:  # pragma: no cover
    raise SystemExit("strict_complete_tier1_logs.py requires the `requests` package.") from exc

from collect_queue_pipeline import (
    COLLECT_LOG_ROOT,
    CSV_FIELDS,
    QUEUE_PATH,
    ROOT,
    IssueRecord,
    iso_now,
    load_issue_history,
    load_queue,
    merge_issue_history,
    normalize_arxiv_url,
    repo_slug,
    render_issues_md,
    save_state,
    ts_now,
    update_queue_file,
    write_csv_rows,
    write_issue_history,
)


REPO_ROOT = ROOT.parents[2]
REPORT_ROOT = ROOT / "strict_reports"
PAPER_ROOT = REPO_ROOT / "paperPDFs"
TIER1_PRIORITIES = {"P1", "P2", "P3", "P4", "P5"}
TIER1_REPOS = {
    "BradyFU/Awesome-Multimodal-Large-Language-Models",
    "showlab/Awesome-Video-Diffusion",
    "jonyzhang2023/awesome-embodied-vla-va-vln",
    "MrNeRF/awesome-3D-gaussian-splatting",
    "knightnemo/Awesome-World-Models",
}
TIMEOUT = 20
USER_AGENT = "ResearchFlowStrictComplete/1.0 (mailto:researchflow@example.com)"
PLACEHOLDER_IMPORTANCE = "Unrated"
PAPER_HOST_HINTS = (
    "arxiv.org",
    "openreview.net",
    "doi.org",
    "ieeexplore.ieee.org",
    "dl.acm.org",
    "aclanthology.org",
    "pmlr.press",
    "openaccess.thecvf.com",
    "proceedings.neurips.cc",
    "papers.nips.cc",
    "ecva.net",
    "springer.com",
    "nature.com",
    "science.org",
    "techrxiv.org",
)
PREPRINT_VENUES = {
    "arxiv",
    "openreview",
    "unknown",
    "doi",
    "ieee",
    "springer",
    "technical report",
    "techrxiv",
}
INVALID_PROJECT_HOSTS = {"img.shields.io"}
NON_PAPER_PAGE_HINTS = {
    "coming soon",
    "blog",
    "project page",
    "model card",
}
GREEK_REPLACEMENTS = {
    "π": "pi",
    "α": "alpha",
    "β": "beta",
    "γ": "gamma",
    "δ": "delta",
    "ε": "epsilon",
    "λ": "lambda",
    "μ": "mu",
    "σ": "sigma",
}
VENUE_PATTERNS: list[tuple[str, str]] = [
    (r"conference on computer vision and pattern recognition|\bcvpr\b", "CVPR"),
    (r"international conference on computer vision|\biccv\b", "ICCV"),
    (r"european conference on computer vision|\beccv\b", "ECCV"),
    (r"advances in neural information processing systems|\bneurips\b|\bnips\b", "NeurIPS"),
    (r"international conference on learning representations|\biclr\b", "ICLR"),
    (r"international conference on machine learning|\bicml\b", "ICML"),
    (r"\baaa?i\b|aaai conference on artificial intelligence", "AAAI"),
    (r"conference on empirical methods in natural language processing|\bemnlp\b", "EMNLP"),
    (r"annual meeting of the association for computational linguistics|\bacl\b", "ACL"),
    (r"north american chapter of the association for computational linguistics|\bnaacl\b", "NAACL"),
    (r"european chapter of the association for computational linguistics|\beacl\b", "EACL"),
    (r"international conference on computational linguistics|\bcoling\b", "COLING"),
    (r"conference on robot learning|\bcorl\b", "CoRL"),
    (r"robotics: science and systems|\brss\b", "RSS"),
    (r"international conference on robotics and automation|\bicra\b", "ICRA"),
    (r"intelligent robots and systems|\biros\b", "IROS"),
    (r"winter conference on applications of computer vision|\bwacv\b", "WACV"),
    (r"british machine vision conference|\bbmvc\b", "BMVC"),
    (r"international conference on 3d vision|\b3dv\b", "3DV"),
    (r"acm international conference on multimedia|acm multimedia|\bacm mm\b", "ACM MM"),
    (r"siggraph asia", "SIGGRAPH Asia"),
    (r"\bsiggraph\b", "SIGGRAPH"),
    (r"transactions on pattern analysis and machine intelligence|\btpami\b|\bpami\b", "TPAMI"),
    (r"international journal of robotics research|\bijrr\b", "IJRR"),
    (r"international journal of computer vision|\bijcv\b", "IJCV"),
    (r"transactions on machine learning research|\btmlr\b", "TMLR"),
    (r"acm transactions on knowledge discovery from data|\btkdd\b", "TKDD"),
    (r"findings of the association for computational linguistics:\s*acl", "ACL Findings"),
    (r"findings of the association for computational linguistics:\s*emnlp", "EMNLP Findings"),
    (r"findings of the association for computational linguistics:\s*naacl", "NAACL Findings"),
    (r"findings of the association for computational linguistics:\s*eacl", "EACL Findings"),
]
ARXIV_ID_RE = re.compile(r"(?P<id>\d{4}\.\d{4,5})(?:v\d+)?")
DOI_RE = re.compile(r"(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)")
URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.I)
META_TAG_RE = re.compile(
    r"<meta[^>]+(?:name|property)=['\"]([^'\"]+)['\"][^>]+content=['\"]([^'\"]*)['\"][^>]*>|"
    r"<meta[^>]+content=['\"]([^'\"]*)['\"][^>]+(?:name|property)=['\"]([^'\"]+)['\"][^>]*>",
    re.I,
)
MANUAL_OVERRIDES: dict[str, dict[str, str]] = {
    "ChartMoE: Mixture of Expert Connector for Advanced Chart Understanding": {
        "venue": "ICLR 2025",
    },
    "Evaluating and Analyzing Relationship Hallucinations in LVLMs": {
        "venue": "ICML 2024",
    },
    "PointCLIP V2: Adapting CLIP for Powerful 3D Open-world Learning": {
        "venue": "ICCV 2023",
    },
    "The Claude 3 Model Family: Opus, Sonnet, Haiku": {
        "venue": "Technical Report 2024",
    },
    "VIMA: General Robot Manipulation with Multimodal Prompts": {
        "venue": "ICML 2023",
    },
    "Write and Paint: Generative Vision-Language Models are Unified Modal Learners": {
        "venue": "ICLR 2023",
    },
    "Benchmarking Large Multimodal Models against Common Corruptions": {
        "venue": "arXiv 2024",
    },
    "HallusionBench: You See What You Think? Or You Think What You See? An Image-Context Reasoning Benchmark Challenging for GPT-4V(ision), LLaVA-1.5, and Other Multi-modality Models": {
        "venue": "CVPR 2024",
    },
    "MathVista: Evaluating Math Reasoning in Visual Contexts with GPT-4V, Bard, and Other Large Multimodal Models": {
        "venue": "ICLR 2024",
    },
    "SEED-Bench: Benchmarking Multimodal LLMs with Generative Comprehension": {
        "venue": "CVPR 2024",
    },
    "Grounding Language Models to Images for Multimodal Inputs and Outputs": {
        "venue": "ICML 2023",
    },
    "3DTrajMaster: Mastering 3D Trajectory for Multi-Entity Motion in Video Generation": {
        "venue": "arXiv 2024",
    },
    "VITA-QinYu: Expressive Spoken Language Model for Role-Playing and Singing": {
        "venue": "Project Page 2026",
        "paper_link": "N/A",
        "state": "Skip",
    },
    "π0.6: a VLA that Learns from Experience": {
        "venue": "Technical Report 2025",
        "paper_link": "https://www.physicalintelligence.company/download/pistar06.pdf",
    },
    "MiniVLA: A Better VLA with a Smaller Footprint": {
        "venue": "Blog 2024",
        "state": "Skip",
    },
    "Genesis: A Generative and Universal Physics Engine for Robotics and Beyond": {
        "venue": "Project Page 2024",
        "state": "Skip",
    },
    "A Path Towards Autonomous Machine Intelligence": {
        "venue": "OpenReview 2022",
    },
    "Safe Reinforcement Learning with World Models": {
        "venue": "ICLR 2024",
    },
    "WOW!: World Models in a Closed-Loop World": {
        "venue": "ICLR 2026",
    },
    "WorldGen: From Text to Traversable and Interactive 3D Worlds": {
        "venue": "arXiv 2025",
    },
    "Probabilistic Adaptation of Black-Box Text-to-Video Models": {
        "venue": "ICLR 2026",
    },
    "Offline Transition Modeling via Contrastive Energy Learning": {
        "venue": "ICML 2024",
    },
    "Policy-conditioned Environment Models are More Generalizable": {
        "venue": "ICML 2024",
    },
    "Scaling Offline Model-Based RL via Jointly-Optimized World-Action Model Pretraining": {
        "venue": "ICLR 2025",
    },
    "Open-World Reinforcement Learning over Long Short-Term Imagination": {
        "venue": "ICLR 2025",
    },
    "Learning Transformer-based World Models with Contrastive Predictive Coding": {
        "venue": "ICLR 2025",
    },
    "Reward-Free Curricula for Training Robust World Models": {
        "venue": "ICLR 2024",
    },
    "Learning Hierarchical World Models with Adaptive Temporal Abstractions from Discrete Latent Dynamics": {
        "venue": "ICLR 2024",
    },
}


@dataclass
class MetadataCandidate:
    source: str
    title: str
    match_score: float
    venue: str
    year: str
    kind: str
    paper_link: str
    doi: str
    details: str


@dataclass
class RepoStats:
    rows: int = 0
    changed_rows: int = 0
    venue_updated: int = 0
    venue_year_filled: int = 0
    paper_link_filled: int = 0
    importance_filled: int = 0
    pdf_path_filled: int = 0
    project_filled: int = 0
    state_changed: int = 0
    unresolved: int = 0
    invalid_candidates: int = 0


class MetadataResolver:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "application/json, text/html;q=0.9, application/xml;q=0.8, */*;q=0.5",
            }
        )
        self.openalex_title_cache: dict[str, Any] = {}
        self.crossref_title_cache: dict[str, Any] = {}
        self.openalex_doi_cache: dict[str, Any] = {}
        self.crossref_doi_cache: dict[str, Any] = {}
        self.page_cache: dict[str, dict[str, Any]] = {}
        self.arxiv_cache: dict[str, dict[str, str] | None] = {}

    def fetch_json(self, url: str) -> Any:
        resp = self.session.get(url, timeout=TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        return resp.json()

    def fetch_text(self, url: str) -> tuple[str, str]:
        resp = self.session.get(url, timeout=TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        resp.encoding = resp.encoding or "utf-8"
        return resp.text, str(resp.url)

    def search_openalex(self, title: str) -> list[dict[str, Any]]:
        key = normalize_lookup_query(title)
        if key in self.openalex_title_cache:
            return self.openalex_title_cache[key]
        queries = build_title_queries(title)
        seen_ids: set[str] = set()
        results: list[dict[str, Any]] = []
        for query in queries:
            url = f"https://api.openalex.org/works?search={quote(query)}&per-page=5"
            try:
                payload = self.fetch_json(url)
            except Exception:
                continue
            for item in payload.get("results", []):
                oid = str(item.get("id") or "")
                if oid and oid in seen_ids:
                    continue
                if oid:
                    seen_ids.add(oid)
                results.append(item)
            if results:
                break
        self.openalex_title_cache[key] = results
        return results

    def search_crossref(self, title: str) -> list[dict[str, Any]]:
        key = normalize_lookup_query(title)
        if key in self.crossref_title_cache:
            return self.crossref_title_cache[key]
        queries = build_title_queries(title)
        results: list[dict[str, Any]] = []
        seen_doi: set[str] = set()
        for query in queries:
            url = f"https://api.crossref.org/works?query.title={quote(query)}&rows=5"
            try:
                payload = self.fetch_json(url)
            except Exception:
                continue
            for item in payload.get("message", {}).get("items", []):
                doi = str(item.get("DOI") or "")
                if doi and doi in seen_doi:
                    continue
                if doi:
                    seen_doi.add(doi)
                results.append(item)
            if results:
                break
        self.crossref_title_cache[key] = results
        return results

    def fetch_openalex_by_doi(self, doi: str) -> dict[str, Any] | None:
        doi = normalize_doi(doi)
        if not doi:
            return None
        if doi in self.openalex_doi_cache:
            return self.openalex_doi_cache[doi]
        try:
            payload = self.fetch_json(f"https://api.openalex.org/works/https://doi.org/{quote(doi, safe='')}")
        except Exception:
            payload = None
        self.openalex_doi_cache[doi] = payload
        return payload

    def fetch_crossref_by_doi(self, doi: str) -> dict[str, Any] | None:
        doi = normalize_doi(doi)
        if not doi:
            return None
        if doi in self.crossref_doi_cache:
            return self.crossref_doi_cache[doi]
        try:
            payload = self.fetch_json(f"https://api.crossref.org/works/{quote(doi, safe='')}")
            item = payload.get("message")
        except Exception:
            item = None
        self.crossref_doi_cache[doi] = item
        return item

    def fetch_page_metadata(self, url: str) -> dict[str, Any]:
        if not url or not url.startswith("http"):
            return {}
        if url in self.page_cache:
            return self.page_cache[url]
        try:
            html, final_url = self.fetch_text(url)
        except Exception:
            self.page_cache[url] = {}
            return {}
        meta: dict[str, str] = {}
        for m in META_TAG_RE.finditer(html):
            key = m.group(1) or m.group(4) or ""
            value = m.group(2) or m.group(3) or ""
            if not key:
                continue
            meta[key.lower()] = unescape(value).strip()
        urls = [clean_url(m.group(0)) for m in URL_RE.finditer(html)]
        arxiv_ids = sorted(set(ARXIV_ID_RE.findall(" ".join(urls + list(meta.values()) + [html[:12000]]))))
        dois = sorted(set(normalize_doi(m.group(1)) for m in DOI_RE.finditer(" ".join(urls + list(meta.values()) + [html[:12000]]))))
        page_text = " ".join([meta.get("og:title", ""), meta.get("og:description", ""), meta.get("description", "")]).strip()
        item = {
            "final_url": final_url,
            "meta": meta,
            "urls": urls,
            "arxiv_ids": arxiv_ids,
            "dois": dois,
            "page_text": page_text,
            "page_year": first_year(" ".join(meta.values()) + " " + final_url),
            "coming_soon": "coming soon" in html.lower() or "coming soon" in page_text.lower(),
        }
        self.page_cache[url] = item
        return item

    def fetch_arxiv_metadata(self, arxiv_id: str) -> dict[str, str] | None:
        arxiv_id = extract_arxiv_id(arxiv_id)
        if not arxiv_id:
            return None
        if arxiv_id in self.arxiv_cache:
            return self.arxiv_cache[arxiv_id]
        try:
            resp = self.session.get(
                f"https://export.arxiv.org/api/query?id_list={quote(arxiv_id)}",
                timeout=TIMEOUT,
                allow_redirects=True,
            )
            resp.raise_for_status()
            root = ET.fromstring(resp.text)
        except Exception:
            self.arxiv_cache[arxiv_id] = None
            return None
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }
        entry = root.find("atom:entry", ns)
        if entry is None:
            self.arxiv_cache[arxiv_id] = None
            return None
        payload = {
            "id": arxiv_id,
            "title": normalize_spaces(entry.findtext("atom:title", default="", namespaces=ns)),
            "published": normalize_spaces(entry.findtext("atom:published", default="", namespaces=ns)),
            "doi": normalize_doi(entry.findtext("arxiv:doi", default="", namespaces=ns) or ""),
            "journal_ref": normalize_spaces(entry.findtext("arxiv:journal_ref", default="", namespaces=ns)),
            "comment": normalize_spaces(entry.findtext("arxiv:comment", default="", namespaces=ns)),
        }
        self.arxiv_cache[arxiv_id] = payload
        return payload


def quote(text: str, safe: str = "") -> str:
    from urllib.parse import quote as url_quote

    return url_quote(text, safe=safe)


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def normalize_lookup_query(text: str) -> str:
    return normalize_title_key(text)


def transliterate(text: str) -> str:
    out = text or ""
    for src, dst in GREEK_REPLACEMENTS.items():
        out = out.replace(src, dst)
    out = unicodedata.normalize("NFKD", out)
    out = out.encode("ascii", "ignore").decode("ascii")
    return out


def normalize_title_key(text: str) -> str:
    text = transliterate(text or "").lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, normalize_title_key(a), normalize_title_key(b)).ratio()


def first_year(text: str) -> str:
    m = re.search(r"\b(19|20)\d{2}\b", text or "")
    return m.group(0) if m else ""


def extract_years(text: str) -> list[str]:
    return re.findall(r"\b(19|20)\d{2}\b", text or "")


def normalize_doi(text: str) -> str:
    value = normalize_spaces(text)
    if not value:
        return ""
    value = value.replace("https://doi.org/", "").replace("http://doi.org/", "").replace("doi:", "")
    m = DOI_RE.search(value)
    return m.group(1).rstrip(").,;") if m else ""


def extract_arxiv_id(text: str) -> str:
    m = ARXIV_ID_RE.search(text or "")
    return m.group("id") if m else ""


def infer_year_from_link(url: str) -> str:
    arxiv_id = extract_arxiv_id(url)
    if arxiv_id:
        return f"20{arxiv_id[:2]}"
    return first_year(url)


def build_title_queries(title: str) -> list[str]:
    cleaned = normalize_spaces(title)
    if not cleaned:
        return []
    queries = [cleaned]
    ascii_text = transliterate(cleaned)
    if ascii_text and ascii_text != cleaned:
        queries.append(ascii_text)
    base = cleaned.split(":", 1)[0].strip()
    if base and base != cleaned:
        queries.append(base)
        ascii_base = transliterate(base)
        if ascii_base and ascii_base != base:
            queries.append(ascii_base)
    deduped: list[str] = []
    seen: set[str] = set()
    for item in queries:
        key = normalize_lookup_query(item)
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def clean_url(url: str) -> str:
    cleaned = html_unescape(url).strip(")>,;\"'")
    return cleaned.replace("&amp;", "&")


def html_unescape(text: str) -> str:
    return unescape(text or "")


def parse_current_venue(venue: str) -> tuple[str, str]:
    venue = normalize_spaces(venue)
    if not venue:
        return "", ""
    m = re.search(r"\b((?:19|20)\d{2})\b", venue)
    if not m:
        return venue, ""
    year = m.group(1)
    base = normalize_spaces(venue.replace(year, ""))
    return base, year


def venue_needs_review(venue: str) -> bool:
    base, year = parse_current_venue(venue)
    return not year or base.lower() in PREPRINT_VENUES


def project_link_invalid(url: str) -> bool:
    if not url or url == "N/A":
        return False
    lowered = url.lower()
    return any(host in lowered for host in INVALID_PROJECT_HOSTS)


def paper_link_looks_actionable(url: str) -> bool:
    lowered = (url or "").lower()
    if not lowered or lowered == "n/a":
        return False
    if lowered.endswith(".pdf") or ".pdf?" in lowered or ".pdf#" in lowered:
        return True
    return any(host in lowered for host in PAPER_HOST_HINTS)


def normalize_paper_link(url: str) -> str:
    if not url or url == "N/A":
        return url
    url = clean_url(url)
    if "arxiv.org/" in url:
        return normalize_arxiv_url(url)
    return url


def detect_page_kind(url: str) -> str:
    lowered = (url or "").lower()
    if "/blog/" in lowered:
        return "blog"
    if "github.com/" in lowered:
        return "github_repo"
    if lowered.endswith(".pdf") or ".pdf?" in lowered or ".pdf#" in lowered:
        return "pdf"
    return "page"


def normalize_venue_name(raw: str, year: str) -> str:
    raw = normalize_spaces(html_unescape(raw))
    if not raw:
        return ""
    lowered = raw.lower()
    if "arxiv" in lowered:
        return f"arXiv {year}".strip()
    if "techrxiv" in lowered:
        return f"TechRxiv {year}".strip()
    if "openreview" in lowered:
        return f"OpenReview {year}".strip()
    for pattern, replacement in VENUE_PATTERNS:
        if re.search(pattern, lowered, re.I):
            return f"{replacement} {year}".strip()
    cleaned = re.sub(r"^\b(19|20)\d{2}\b[\s:,-]*", "", raw).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return f"{cleaned} {year}".strip() if year else cleaned


def build_pdf_path(sort_value: str, venue: str, title: str) -> str:
    category = sanitize_path_component(sort_value or "Uncategorized")
    venue_slug = sanitize_path_component(venue or "Unknown")
    year = first_year(venue)
    title_slug = sanitize_path_component(title, max_len=180)
    filename = f"{year}_{title_slug}.pdf" if year else f"{title_slug}.pdf"
    return (Path("paperPDFs") / category / venue_slug / filename).as_posix()


def sanitize_path_component(text: str, max_len: int = 120) -> str:
    text = transliterate(text or "")
    text = re.sub(r"[^0-9A-Za-z]+", "_", text).strip("_")
    text = re.sub(r"_+", "_", text)
    if not text:
        text = "Unknown"
    if len(text) > max_len:
        text = text[:max_len].rstrip("_")
    return text


def crossref_title(item: dict[str, Any]) -> str:
    titles = item.get("title") or []
    return normalize_spaces(titles[0]) if titles else ""


def crossref_year(item: dict[str, Any]) -> str:
    for key in ("published-print", "published-online", "issued", "created"):
        data = item.get(key) or {}
        parts = data.get("date-parts") or [[]]
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def crossref_raw_venue(item: dict[str, Any]) -> str:
    container = item.get("container-title") or []
    if container and container[0]:
        return normalize_spaces(container[0])
    event = item.get("event") or {}
    if event.get("name"):
        return normalize_spaces(event["name"])
    return normalize_spaces(item.get("publisher") or "")


def openalex_title(item: dict[str, Any]) -> str:
    return normalize_spaces(item.get("display_name") or "")


def openalex_year(item: dict[str, Any]) -> str:
    year = item.get("publication_year")
    return str(year) if year else ""


def openalex_raw_venue(item: dict[str, Any]) -> str:
    primary = item.get("primary_location") or {}
    raw_source_name = normalize_spaces(primary.get("raw_source_name") or "")
    if raw_source_name:
        return raw_source_name
    source = primary.get("source") or {}
    source_name = normalize_spaces(source.get("display_name") or "")
    if source_name:
        return source_name
    for location in item.get("locations") or []:
        raw_source_name = normalize_spaces(location.get("raw_source_name") or "")
        if raw_source_name:
            return raw_source_name
        source = location.get("source") or {}
        source_name = normalize_spaces(source.get("display_name") or "")
        if source_name:
            return source_name
    return ""


def openalex_doi(item: dict[str, Any]) -> str:
    return normalize_doi(item.get("doi") or "")


def doi_to_url(doi: str) -> str:
    doi = normalize_doi(doi)
    return f"https://doi.org/{doi}" if doi else ""


def classify_candidate(venue_raw: str, source_type: str) -> str:
    lowered = (venue_raw or "").lower()
    source_type = (source_type or "").lower()
    if "arxiv" in lowered or source_type in {"preprint"}:
        return "preprint"
    if "techrxiv" in lowered or source_type == "posted-content":
        return "platform"
    if "openreview" in lowered:
        return "platform"
    if source_type in {"journal-article", "proceedings-article", "article", "review"}:
        return "published"
    if venue_raw:
        return "published"
    return "unknown"


def pick_best_openalex(title: str, items: list[dict[str, Any]]) -> dict[str, Any] | None:
    best = None
    best_score = 0.0
    for item in items:
        item_title = openalex_title(item)
        score = similarity(title, item_title)
        if score > best_score:
            best = item
            best_score = score
    if best is None or best_score < 0.84:
        return None
    return best


def pick_best_crossref(title: str, items: list[dict[str, Any]]) -> dict[str, Any] | None:
    best = None
    best_score = 0.0
    for item in items:
        item_title = crossref_title(item)
        score = similarity(title, item_title)
        if score > best_score:
            best = item
            best_score = score
    if best is None or best_score < 0.84:
        return None
    return best


def candidate_from_openalex(item: dict[str, Any], row_title: str) -> MetadataCandidate | None:
    title = openalex_title(item)
    if not title:
        return None
    score = similarity(row_title, title)
    if score < 0.84:
        return None
    year = openalex_year(item)
    venue_raw = openalex_raw_venue(item)
    doi = openalex_doi(item)
    paper_link = doi_to_url(doi) or normalize_paper_link((item.get("primary_location") or {}).get("landing_page_url") or "")
    kind = classify_candidate(venue_raw, str(item.get("type") or ""))
    venue = normalize_venue_name(venue_raw, year)
    return MetadataCandidate(
        source="OpenAlex",
        title=title,
        match_score=score,
        venue=venue,
        year=year,
        kind=kind,
        paper_link=paper_link,
        doi=doi,
        details=venue_raw or str(item.get("type") or ""),
    )


def candidate_from_crossref(item: dict[str, Any], row_title: str) -> MetadataCandidate | None:
    title = crossref_title(item)
    if not title:
        return None
    score = similarity(row_title, title)
    if score < 0.84:
        return None
    year = crossref_year(item)
    venue_raw = crossref_raw_venue(item)
    doi = normalize_doi(item.get("DOI") or "")
    paper_link = doi_to_url(doi) or normalize_paper_link(item.get("URL") or "")
    kind = classify_candidate(venue_raw, str(item.get("type") or ""))
    venue = normalize_venue_name(venue_raw, year)
    return MetadataCandidate(
        source="Crossref",
        title=title,
        match_score=score,
        venue=venue,
        year=year,
        kind=kind,
        paper_link=paper_link,
        doi=doi,
        details=venue_raw or str(item.get("type") or ""),
    )


def candidate_from_page(row: dict[str, str], page: dict[str, Any], link_source: str) -> MetadataCandidate | None:
    if not page:
        return None
    meta = page.get("meta") or {}
    title = normalize_spaces(meta.get("citation_title") or meta.get("og:title") or row["paper_title"])
    year = first_year(
        " ".join(
            [
                meta.get("citation_publication_date", ""),
                meta.get("citation_online_date", ""),
                meta.get("citation_date", ""),
                meta.get("og:description", ""),
                meta.get("description", ""),
                page.get("final_url", ""),
            ]
        )
    ) or page.get("page_year", "")
    venue_raw = normalize_spaces(
        meta.get("citation_conference_title")
        or meta.get("citation_journal_title")
        or meta.get("citation_technical_report_institution")
        or ""
    )
    paper_link = normalize_paper_link(meta.get("citation_pdf_url") or meta.get("citation_abstract_html_url") or "")
    doi = ""
    if page.get("dois"):
        doi = page["dois"][0]
        if not paper_link:
            paper_link = doi_to_url(doi)
    if not paper_link and page.get("arxiv_ids"):
        paper_link = f"https://arxiv.org/abs/{page['arxiv_ids'][0]}"
    if not venue_raw and page.get("arxiv_ids"):
        venue_raw = "arXiv"
    if not venue_raw and page.get("coming_soon"):
        venue_raw = "Project Page"
    if not venue_raw and link_source == "project_link":
        venue_raw = "Project Page"
    if not venue_raw and detect_page_kind(page.get("final_url", "")) == "blog":
        venue_raw = "Blog"
    if not venue_raw and not year:
        return None
    venue = normalize_venue_name(venue_raw, year)
    kind = "published"
    lowered = venue_raw.lower()
    if "project page" in lowered or "blog" in lowered:
        kind = "artifact"
    elif "arxiv" in lowered:
        kind = "preprint"
    return MetadataCandidate(
        source=f"page:{link_source}",
        title=title,
        match_score=similarity(row["paper_title"], title),
        venue=venue,
        year=year,
        kind=kind,
        paper_link=paper_link,
        doi=doi,
        details=page.get("final_url", ""),
    )


def candidate_from_arxiv_meta(meta: dict[str, str], row: dict[str, str]) -> MetadataCandidate | None:
    title = normalize_spaces(meta.get("title") or "")
    if not title:
        return None
    score = similarity(row["paper_title"], title)
    if score < 0.84:
        return None
    published = meta.get("published") or ""
    year = first_year(published)
    journal_ref = meta.get("journal_ref") or ""
    comment = meta.get("comment") or ""
    current_base, _current_year = parse_current_venue(row["venue"])
    raw = journal_ref or comment
    resolved = ""
    if raw:
        candidate_year = first_year(raw) or year
        resolved = normalize_venue_name(raw, candidate_year)
        if current_base and candidate_year and normalize_title_key(current_base) in normalize_title_key(raw):
            resolved = f"{current_base} {candidate_year}"
    if not resolved and year:
        resolved = f"arXiv {year}"
    kind = "published" if resolved and not resolved.lower().startswith(("arxiv", "openreview", "techrxiv")) else "preprint"
    paper_link = f"https://arxiv.org/abs/{meta['id']}"
    return MetadataCandidate(
        source="arXiv API",
        title=title,
        match_score=score,
        venue=resolved,
        year=first_year(resolved) or year,
        kind=kind,
        paper_link=paper_link,
        doi=meta.get("doi") or "",
        details=raw or published,
    )


def choose_final_candidate(
    row: dict[str, str],
    current_venue: str,
    arxiv_candidate: MetadataCandidate | None,
    oa_candidate: MetadataCandidate | None,
    cr_candidate: MetadataCandidate | None,
    page_candidate: MetadataCandidate | None,
) -> tuple[str, list[str], bool]:
    sources_used: list[str] = []
    base, year = parse_current_venue(current_venue)
    current_base_norm = base.lower()
    if page_candidate:
        sources_used.append(page_candidate.source)
    if arxiv_candidate:
        sources_used.append(arxiv_candidate.source)
    if oa_candidate:
        sources_used.append(oa_candidate.source)
    if cr_candidate:
        sources_used.append(cr_candidate.source)

    published_candidates = [c for c in (arxiv_candidate, oa_candidate, cr_candidate) if c and c.kind == "published" and c.venue and c.year]
    if len(published_candidates) >= 2:
        first = published_candidates[0]
        second = published_candidates[1]
        if normalize_title_key(first.venue) == normalize_title_key(second.venue):
            return first.venue, sources_used, False
        if first.doi and second.doi and first.doi == second.doi:
            return first.venue, sources_used, False

    if base and not year:
        for candidate in published_candidates:
            cand_base, cand_year = parse_current_venue(candidate.venue)
            if cand_year and normalize_title_key(cand_base) == normalize_title_key(base):
                return candidate.venue, sources_used, False

    if venue_needs_review(current_venue):
        if published_candidates:
            strong = max(published_candidates, key=lambda item: item.match_score)
            if strong.match_score >= 0.92:
                if cr_candidate and oa_candidate and cr_candidate.doi and oa_candidate.doi and cr_candidate.doi == oa_candidate.doi:
                    return strong.venue, sources_used, False
                if cr_candidate and oa_candidate and normalize_title_key(cr_candidate.venue) == normalize_title_key(oa_candidate.venue):
                    return strong.venue, sources_used, False
                if current_base_norm in PREPRINT_VENUES:
                    return strong.venue, sources_used, False

    if arxiv_candidate and arxiv_candidate.kind == "published" and arxiv_candidate.venue and arxiv_candidate.year:
        if base and not year:
            cand_base, cand_year = parse_current_venue(arxiv_candidate.venue)
            if cand_year and normalize_title_key(cand_base) == normalize_title_key(base):
                return arxiv_candidate.venue, sources_used, False
        if current_base_norm in PREPRINT_VENUES:
            return arxiv_candidate.venue, sources_used, False

    if oa_candidate and oa_candidate.kind in {"preprint", "platform"} and oa_candidate.year:
        if "technical report" in current_base_norm:
            return f"Technical Report {oa_candidate.year}", sources_used, False
        if current_base_norm in {"openreview"}:
            return f"OpenReview {oa_candidate.year}", sources_used, False
        if current_base_norm in {"doi"} and "techrxiv" in oa_candidate.details.lower():
            return f"TechRxiv {oa_candidate.year}", sources_used, False
        return f"arXiv {oa_candidate.year}", sources_used, False

    if arxiv_candidate and arxiv_candidate.year:
        if "technical report" in current_base_norm:
            return f"Technical Report {arxiv_candidate.year}", sources_used, False
        if current_base_norm in {"openreview"}:
            return f"OpenReview {arxiv_candidate.year}", sources_used, False
        return f"arXiv {arxiv_candidate.year}", sources_used, False

    fallback_year = (
        (oa_candidate.year if oa_candidate else "")
        or (cr_candidate.year if cr_candidate else "")
        or (arxiv_candidate.year if arxiv_candidate else "")
        or (page_candidate.year if page_candidate else "")
        or infer_year_from_link(row.get("paper_link", ""))
    )
    if current_base_norm == "openreview" and fallback_year:
        return f"OpenReview {fallback_year}", sources_used, False
    if current_base_norm == "doi" and fallback_year:
        if "techrxiv" in row.get("paper_link", "").lower():
            return f"TechRxiv {fallback_year}", sources_used, False
        return f"DOI {fallback_year}", sources_used, False
    if current_base_norm in {"ieee", "springer", "anthropic"} and fallback_year:
        return f"{base} {fallback_year}".strip(), sources_used, False
    if base and not year and fallback_year and current_base_norm not in PREPRINT_VENUES:
        return f"{base} {fallback_year}".strip(), sources_used, False

    if page_candidate and page_candidate.kind == "artifact" and page_candidate.year:
        return page_candidate.venue, sources_used, True

    if current_venue and year:
        return current_venue, sources_used, False
    return current_venue, sources_used, True


def best_candidate_title_match(candidates: Iterable[MetadataCandidate | None]) -> float:
    scores = [c.match_score for c in candidates if c]
    return max(scores) if scores else 0.0


def resolve_row(
    row: dict[str, str],
    resolver: MetadataResolver,
) -> tuple[dict[str, str], list[IssueRecord], dict[str, int]]:
    issues: list[IssueRecord] = []
    changes = {
        "venue_updated": 0,
        "venue_year_filled": 0,
        "paper_link_filled": 0,
        "importance_filled": 0,
        "pdf_path_filled": 0,
        "project_filled": 0,
        "state_changed": 0,
        "invalid_candidates": 0,
    }

    original = row.copy()
    row = {field: normalize_spaces(row.get(field, "")) for field in CSV_FIELDS}
    row["paper_link"] = normalize_paper_link(row["paper_link"])
    override = MANUAL_OVERRIDES.get(row["paper_title"]) or {}

    if not row["state"]:
        row["state"] = "Wait"
    if not row["importance"]:
        row["importance"] = PLACEHOLDER_IMPORTANCE
        changes["importance_filled"] += 1
    if not row["project_link_or_github_link"] or project_link_invalid(row["project_link_or_github_link"]):
        row["project_link_or_github_link"] = "N/A"
        changes["project_filled"] += 1
    if override.get("paper_link") and row["paper_link"] != override["paper_link"]:
        row["paper_link"] = override["paper_link"]
        changes["paper_link_filled"] += 1
    if override.get("venue") and row["venue"] != override["venue"]:
        old_base, old_year = parse_current_venue(row["venue"])
        new_base, new_year = parse_current_venue(override["venue"])
        if old_base and new_base and normalize_title_key(old_base) == normalize_title_key(new_base) and not old_year and new_year:
            changes["venue_year_filled"] += 1
        else:
            changes["venue_updated"] += 1
        row["venue"] = override["venue"]
    if override.get("state") and row["state"] != override["state"]:
        row["state"] = override["state"]
        changes["state_changed"] += 1

    page_candidate = None
    page_meta = {}
    primary_link = row["paper_link"] if row["paper_link"] and row["paper_link"] != "N/A" else row["project_link_or_github_link"]
    page_source = "paper_link" if row["paper_link"] and row["paper_link"] != "N/A" else "project_link"
    if primary_link and primary_link != "N/A" and not paper_link_looks_actionable(primary_link):
        page_meta = resolver.fetch_page_metadata(primary_link)
        page_candidate = candidate_from_page(row, page_meta, page_source)
        if page_candidate and page_candidate.paper_link and not paper_link_looks_actionable(row["paper_link"]):
            row["paper_link"] = page_candidate.paper_link
            changes["paper_link_filled"] += 1

    if not row["paper_link"]:
        search_page = resolver.fetch_page_metadata(row["project_link_or_github_link"])
        project_page_candidate = candidate_from_page(row, search_page, "project_link")
        if project_page_candidate and project_page_candidate.paper_link:
            row["paper_link"] = project_page_candidate.paper_link
            changes["paper_link_filled"] += 1
            page_candidate = project_page_candidate
        elif row["project_link_or_github_link"] and row["project_link_or_github_link"] != "N/A":
            row["paper_link"] = "N/A"
            changes["paper_link_filled"] += 1

    oa_candidate = None
    cr_candidate = None
    arxiv_candidate = None
    need_review = venue_needs_review(row["venue"]) or row["paper_link"] in {"", "N/A"}
    if need_review:
        arxiv_id = extract_arxiv_id(row["paper_link"])
        if not arxiv_id and page_meta.get("arxiv_ids"):
            arxiv_id = page_meta["arxiv_ids"][0]
        if arxiv_id:
            arxiv_meta = resolver.fetch_arxiv_metadata(arxiv_id)
            if arxiv_meta:
                arxiv_candidate = candidate_from_arxiv_meta(arxiv_meta, row)
        best_oa = pick_best_openalex(row["paper_title"], resolver.search_openalex(row["paper_title"]))
        if best_oa:
            oa_candidate = candidate_from_openalex(best_oa, row["paper_title"])
        doi = ""
        if arxiv_candidate and arxiv_candidate.doi:
            doi = arxiv_candidate.doi
        elif oa_candidate and oa_candidate.doi:
            doi = oa_candidate.doi
        elif page_meta.get("dois"):
            doi = page_meta["dois"][0]
        elif row["paper_link"] and "doi.org/" in row["paper_link"]:
            doi = normalize_doi(row["paper_link"])
        if doi:
            crossref_item = resolver.fetch_crossref_by_doi(doi)
            if crossref_item:
                cr_candidate = candidate_from_crossref(crossref_item, row["paper_title"])
            if not oa_candidate:
                openalex_item = resolver.fetch_openalex_by_doi(doi)
                if openalex_item:
                    oa_candidate = candidate_from_openalex(openalex_item, row["paper_title"])
        need_crossref_title = False
        venue_base, venue_year = parse_current_venue(row["venue"])
        if not venue_year or venue_base.lower() in {"openreview", "doi", "ieee", "springer", "technical report", "unknown"}:
            need_crossref_title = True
        if oa_candidate and oa_candidate.kind == "published":
            need_crossref_title = True
        if cr_candidate is None and need_crossref_title:
            best_cr = pick_best_crossref(row["paper_title"], resolver.search_crossref(row["paper_title"]))
            if best_cr:
                cr_candidate = candidate_from_crossref(best_cr, row["paper_title"])

    resolved_venue, sources_used, unresolved = choose_final_candidate(row, row["venue"], arxiv_candidate, oa_candidate, cr_candidate, page_candidate)
    old_base, old_year = parse_current_venue(row["venue"])
    new_base, new_year = parse_current_venue(resolved_venue)
    if resolved_venue and resolved_venue != row["venue"]:
        if old_base and new_base and normalize_title_key(old_base) == normalize_title_key(new_base) and not old_year and new_year:
            changes["venue_year_filled"] += 1
        else:
            changes["venue_updated"] += 1
        row["venue"] = resolved_venue

    if not row["venue"]:
        if oa_candidate and oa_candidate.year:
            row["venue"] = f"arXiv {oa_candidate.year}"
            changes["venue_updated"] += 1
        elif page_candidate and page_candidate.year:
            row["venue"] = page_candidate.venue
            changes["venue_updated"] += 1

    if not row["paper_link"]:
        row["paper_link"] = "N/A"
        changes["paper_link_filled"] += 1

    if not row["pdf_path"]:
        row["pdf_path"] = build_pdf_path(row["sort"], row["venue"], row["paper_title"])
        changes["pdf_path_filled"] += 1

    if row["paper_link"] == "N/A":
        if page_candidate and page_candidate.kind == "artifact" and row["state"] != "Skip":
            row["state"] = "Skip"
            changes["state_changed"] += 1
        if row["state"] != "Skip":
            issues.append(
                IssueRecord(
                    timestamp=iso_now(),
                    issue_type="missing_paper_link",
                    title=row["paper_title"],
                    status="needs_review",
                    details="未能找到可用论文链接，已使用保守占位或转为非论文候选。",
                    attempted=sources_used or ["project page scan", "OpenAlex title search", "Crossref title search"],
                    resolved=False,
                )
            )

    if not first_year(row["venue"]):
        issue_type = "missing_venue_year"
        if page_candidate and page_candidate.kind == "artifact":
            if row["state"] != "Skip":
                row["state"] = "Skip"
                changes["state_changed"] += 1
            issue_type = "non_paper_candidate"
        issues.append(
            IssueRecord(
                timestamp=iso_now(),
                issue_type=issue_type,
                title=row["paper_title"],
                status="needs_review",
                details=f"venue 仍缺少年份或未能确认最终 venue：{row['venue'] or 'Unknown'}",
                attempted=sources_used or ["OpenAlex title search", "Crossref title search"],
                resolved=False,
            )
        )

    if unresolved and row["state"] != "Skip" and venue_needs_review(row["venue"]) and best_candidate_title_match([oa_candidate, cr_candidate, page_candidate]) < 0.90:
        issues.append(
            IssueRecord(
                timestamp=iso_now(),
                issue_type="low_confidence_venue",
                title=row["paper_title"],
                status="needs_review",
                details=f"venue 保守保留为 `{row['venue']}`，仍建议人工复核。",
                attempted=sources_used or ["OpenAlex title search", "Crossref title search"],
                resolved=False,
            )
        )

    if row["state"] == "Skip":
        changes["invalid_candidates"] += 1

    return row, dedupe_issues(issues), changes


def dedupe_issues(items: list[IssueRecord]) -> list[IssueRecord]:
    seen: set[tuple[str, str, str]] = set()
    out: list[IssueRecord] = []
    for item in items:
        key = (item.issue_type, normalize_title_key(item.title), item.details)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def display_path(path: Path) -> str:
    for base in (ROOT, REPO_ROOT):
        try:
            return str(path.relative_to(base))
        except ValueError:
            continue
    return str(path)


def render_run_summary(path: Path, repo: str, stats: RepoStats, history: list[IssueRecord], output_csv: Path) -> None:
    unresolved = sum(1 for item in history if not item.resolved)
    lines = [
        "---",
        f'title: "Strict Completion Summary - {repo}"',
        f"created: {iso_now()}",
        f"updated: {iso_now()}",
        "type: github_awesome_strict_completion_summary",
        "tags:",
        "  - github-awesome",
        "  - strict-completion",
        f'repo: "{repo}"',
        "---",
        "",
        f"# {repo} 严格补全摘要",
        "",
        f"- 输出 CSV: `{display_path(output_csv)}`",
        f"- 条目数: `{stats.rows}`",
        f"- 变更条目数: `{stats.changed_rows}`",
        f"- venue 更新: `{stats.venue_updated}`",
        f"- venue 年份补齐: `{stats.venue_year_filled}`",
        f"- paper_link 补齐: `{stats.paper_link_filled}`",
        f"- project_link 补齐: `{stats.project_filled}`",
        f"- importance 补齐: `{stats.importance_filled}`",
        f"- pdf_path 补齐: `{stats.pdf_path_filled}`",
        f"- state 调整: `{stats.state_changed}`",
        f"- 识别为非论文/候选异常: `{stats.invalid_candidates}`",
        f"- 累计未解决问题: `{unresolved}`",
        "",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_global_report(path: Path, repo_reports: list[tuple[str, RepoStats, int]]) -> None:
    lines = [
        "---",
        'title: "Tier 1 Strict Completion Report"',
        f"created: {iso_now()}",
        f"updated: {iso_now()}",
        "type: github_awesome_strict_completion_report",
        "tags:",
        "  - github-awesome",
        "  - strict-completion",
        "  - tier1",
        "---",
        "",
        "# Tier 1 严格补全报告",
        "",
        "| Repo | Rows | Changed | Venue Updated | Venue Year Filled | Paper Link Filled | Project Link Filled | Importance Filled | Pdf Path Filled | Unresolved |",
        "|------|------|---------|---------------|-------------------|-------------------|---------------------|-------------------|-----------------|------------|",
    ]
    for repo, stats, unresolved in repo_reports:
        lines.append(
            f"| `{repo}` | {stats.rows} | {stats.changed_rows} | {stats.venue_updated} | {stats.venue_year_filled} | {stats.paper_link_filled} | {stats.project_filled} | {stats.importance_filled} | {stats.pdf_path_filled} | {unresolved} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def select_tasks(queue_path: Path, requested_repos: list[str]) -> tuple[list[str], list[Any]]:
    queue_lines, tasks = load_queue(queue_path)
    tier1 = [task for task in tasks if task.priority in TIER1_PRIORITIES and task.repo in TIER1_REPOS]
    if requested_repos:
        requested = {repo.lower() for repo in requested_repos}
        tier1 = [task for task in tier1 if task.repo.lower() in requested]
    return queue_lines, tier1


def main() -> int:
    ap = argparse.ArgumentParser(description="对 Tier 1 GitHub awesome repo-local CSV 做严格补全与 venue/year 复核。")
    ap.add_argument("--queue", default=str(QUEUE_PATH), help="优先级队列文件路径")
    ap.add_argument("--repo", action="append", default=[], help="只处理指定 repo，可重复传入")
    ap.add_argument("--limit", type=int, default=0, help="每个 repo 只处理前 N 条，用于小范围验证")
    ap.add_argument("--dry-run", action="store_true", help="只输出运行结果，不落盘")
    ap.add_argument("--no-queue-update", action="store_true", help="不回写 collect_priority_queue.md")
    args = ap.parse_args()

    queue_path = Path(args.queue)
    queue_lines, tasks = select_tasks(queue_path, args.repo)
    if not tasks:
        raise SystemExit("未找到可处理的 Tier 1 repo。")

    resolver = MetadataResolver()
    run_stamp = ts_now()
    report_dir = REPORT_ROOT / run_stamp
    if not args.dry_run:
        report_dir.mkdir(parents=True, exist_ok=True)

    repo_reports: list[tuple[str, RepoStats, int]] = []

    for task in tasks:
        slug = repo_slug(task.repo)
        canonical_csv = COLLECT_LOG_ROOT / f"{slug}.auto.csv"
        if not canonical_csv.exists():
            raise SystemExit(f"canonical CSV 不存在: {canonical_csv}")

        rows = read_csv_rows(canonical_csv)
        repo_dir = ROOT / slug
        run_dir = repo_dir / run_stamp
        if not args.dry_run:
            repo_dir.mkdir(parents=True, exist_ok=True)
            run_dir.mkdir(parents=True, exist_ok=True)

        updated_rows: list[dict[str, str]] = []
        current_issues: list[IssueRecord] = []
        stats = RepoStats(rows=len(rows))

        selected_rows = rows[: args.limit] if args.limit and args.limit > 0 else rows
        stats.rows = len(selected_rows)
        for index, row in enumerate(selected_rows, start=1):
            new_row, issues, changes = resolve_row(row, resolver)
            updated_rows.append(new_row)
            current_issues.extend(issues)
            stats.venue_updated += changes["venue_updated"]
            stats.venue_year_filled += changes["venue_year_filled"]
            stats.paper_link_filled += changes["paper_link_filled"]
            stats.importance_filled += changes["importance_filled"]
            stats.pdf_path_filled += changes["pdf_path_filled"]
            stats.project_filled += changes["project_filled"]
            stats.state_changed += changes["state_changed"]
            stats.invalid_candidates += changes["invalid_candidates"]
            if any(changes.values()):
                stats.changed_rows += 1
            if index % 50 == 0 or index == len(selected_rows):
                print(f"[progress] {task.repo}: {index}/{len(selected_rows)}")

        deduped_current_issues = dedupe_issues(current_issues)
        issues_jsonl = repo_dir / "issues.jsonl"
        history = load_issue_history(issues_jsonl) if issues_jsonl.exists() else []
        merged_history = merge_issue_history(history, deduped_current_issues)
        unresolved_total = sum(1 for issue in merged_history if not issue.resolved)
        stats.unresolved = unresolved_total

        if not args.dry_run:
            final_rows = updated_rows + rows[len(selected_rows) :]
            write_csv_rows(run_dir / "collect_output.csv", final_rows)
            write_csv_rows(canonical_csv, final_rows)
            write_issue_history(issues_jsonl, merged_history)
            render_issues_md(repo_dir / "issues.md", task, merged_history, str(run_dir.relative_to(ROOT)))
            render_run_summary(run_dir / "strict_completion_summary.md", task.repo, stats, merged_history, canonical_csv)
            save_state(
                repo_dir / "task_state.json",
                {
                    "repo": task.repo,
                    "priority": task.priority,
                    "direction": task.direction,
                    "selected_at": iso_now(),
                    "source_mode": "strict_completion_tier1",
                    "latest_run": str(run_dir),
                    "row_count": len(updated_rows + rows[len(selected_rows) :]),
                    "issue_count_current_run": len(deduped_current_issues),
                    "issue_count_total": len(merged_history),
                    "canonical_csv": str(canonical_csv),
                },
            )

        total_row_count = len(updated_rows + rows[len(selected_rows) :])
        progress_text = f"✅ 完成（{total_row_count} 条；{unresolved_total} 个未解决问题记录于 `{slug}/issues.md`）"
        if not args.no_queue_update:
            update_queue_file(queue_path, queue_lines, task, progress_text, dry_run=args.dry_run)

        repo_reports.append((task.repo, stats, unresolved_total))
        print(f"[strict] {task.repo}: rows={total_row_count} changed={stats.changed_rows} unresolved={unresolved_total}")

    if not args.dry_run:
        render_global_report(report_dir / "tier1_strict_completion_report.md", repo_reports)

    if args.dry_run:
        print("Dry-run mode enabled; canonical CSV, issues, state, and queue were not modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
