#!/usr/bin/env python3
"""Backfill missing paper/project/code links in paper_list.csv and notes.

The script is intentionally conservative:
- only fills empty/N/A values in paper_list.csv;
- only uses links observed in local analysis notes, local run manifests, or PDF
  first-page text/annotations;
- writes audit files before applying changes.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


REPO_ROOT = Path(__file__).resolve().parents[2]
PAPER_LIST = REPO_ROOT / "obsidian-vault" / "paper_list.csv"
ANALYSIS_DIR = REPO_ROOT / "obsidian-vault" / "analysis"
VAULT_ROOT = REPO_ROOT / "obsidian-vault"
RUNS_DIR = REPO_ROOT / "_private" / "local_analysis_runs"
OUT_DIR = REPO_ROOT / "obsidian-vault" / "batches" / "link_completion_20260610"

URL_RE = re.compile(r"https?://[^\s)\]}>\"'，。；;]+", re.I)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", re.I)
LINKS_ROW_RE = re.compile(r"(?m)^(\|\s*Links\s*\|\s*)(.*?)(\s*\|)\s*$")
VENUE_ROW_RE = re.compile(r"(?m)^(\|\s*(?:会议/期刊|Venue)\s*\|.*\|\s*)$")
FM_SCALAR_RE = re.compile(r"(?m)^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):\s*(?P<value>.*)$")
STOPWORDS = {
    "a",
    "an",
    "the",
    "of",
    "for",
    "and",
    "or",
    "to",
    "via",
    "with",
    "in",
    "on",
    "from",
    "by",
    "using",
    "through",
    "towards",
    "toward",
    "learning",
    "model",
    "models",
    "diffusion",
    "generation",
}
PAPER_HOST_MARKERS = (
    "arxiv.org",
    "openreview.net",
    "openaccess.thecvf.com",
    "doi.org",
    "dl.acm.org",
    "ieeexplore.ieee.org",
    "proceedings.mlr.press",
    "proceedings.neurips.cc",
    "aclanthology.org",
    "aaai.org",
    "ojs.aaai.org",
    "jmlr.org",
    "cvf.com",
    "thecvf.com",
)
PROJECT_CONTEXT = re.compile(
    r"\b(project|homepage|home page|website|demo|code|github|repo|repository|implementation|source)\b",
    re.I,
)


try:
    import fitz  # type: ignore
except Exception:  # pragma: no cover
    fitz = None


@dataclass
class LinkCandidate:
    kind: str
    url: str
    source: str
    evidence: str
    confidence: float
    note_path: str = ""
    line: int = 0


@dataclass
class NoteInfo:
    path: Path
    title: str = ""
    pdf_ref: str = ""
    openreview_forum_id: str = ""
    project_link: str = ""
    code_link: str = ""
    paper_links: list[LinkCandidate] = field(default_factory=list)
    source_links: list[LinkCandidate] = field(default_factory=list)


def clean_url(url: str) -> str:
    value = (url or "").strip().strip("<>")
    while value and value[-1] in ".,;:!?，。；)]}>":
        value = value[:-1]
    return value


def host_of(url: str) -> str:
    try:
        return urlsplit(url).netloc.lower().replace("www.", "")
    except ValueError:
        return ""


def path_parts(url: str) -> list[str]:
    try:
        return [part for part in urlsplit(url).path.split("/") if part]
    except ValueError:
        return []


def is_empty(value: str) -> bool:
    return (value or "").strip().lower() in {"", "n/a", "na", "none", "null", "-", "--"}


def normalize_title(text: str) -> str:
    text = re.sub(r"\$[^$]*\$", " ", text or "")
    text = re.sub(r"\bet\s+al\.?\b", " ", text, flags=re.I)
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def title_tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", (text or "").lower())
        if len(token) > 2 and token not in STOPWORDS
    }


def titles_compatible(a: str, b: str) -> tuple[bool, str]:
    na = normalize_title(a)
    nb = normalize_title(b)
    if not na or not nb:
        return False, "missing_title"
    if na == nb:
        return True, "title_exact"
    if len(na) >= 28 and na in nb:
        return True, "note_title_contained"
    if len(nb) >= 28 and nb in na:
        return True, "row_title_contained"
    ta = title_tokens(a)
    tb = title_tokens(b)
    if len(ta) >= 4 and len(tb) >= 4:
        overlap = len(ta & tb)
        denom = min(len(ta), len(tb))
        if denom and overlap / denom >= 0.86:
            return True, f"token_overlap_{overlap}_{denom}"
    return False, "title_mismatch"


def canonical_paper_url(url: str) -> str:
    url = clean_url(url)
    try:
        parsed = urlsplit(url)
    except ValueError:
        return url
    host = parsed.netloc.lower().replace("www.", "")
    path = parsed.path.rstrip("/")
    if host == "arxiv.org":
        match = re.search(r"/(?:abs|pdf)/([^/]+?)(?:\.pdf)?$", path)
        if match:
            arxiv_id = re.sub(r"v\d+$", "", match.group(1), flags=re.I)
            return f"https://arxiv.org/abs/{arxiv_id}"
    if host == "openreview.net":
        match = re.search(r"(?:^|&)id=([^&]+)", parsed.query)
        if match:
            return f"https://openreview.net/forum?id={match.group(1)}"
    return urlunsplit((parsed.scheme.lower(), host, path, parsed.query, "")).rstrip("/")


def is_paper_url(url: str) -> bool:
    url = clean_url(url)
    host = host_of(url)
    path = ""
    query = ""
    try:
        parsed = urlsplit(url)
        path = parsed.path.lower()
        query = parsed.query.lower()
    except ValueError:
        return False
    if host == "arxiv.org":
        return bool(re.search(r"^/(abs|pdf)/[0-9]{4}\.[0-9]{4,5}(v\d+)?(?:\.pdf)?$", path))
    if host == "openreview.net":
        return path == "/forum" and bool(re.search(r"(?:^|&)id=[^&]+", query))
    if host == "openaccess.thecvf.com":
        return path.endswith(("_paper.html", "_paper.pdf", ".pdf")) and "/content/" in path
    if host == "doi.org":
        doi = path.strip("/")
        return doi.startswith("10.") and not re.search(r"\b[xyn]{3,}\b", doi)
    if host == "dl.acm.org":
        doi = path.removeprefix("/doi/")
        return doi.startswith("10.") and not re.search(r"\b[xyn]{3,}\b", doi)
    if host == "ieeexplore.ieee.org":
        return "/document/" in path
    if host in {"proceedings.mlr.press", "proceedings.neurips.cc", "aclanthology.org", "jmlr.org"}:
        return len(path.strip("/")) > 4
    if any(marker in host for marker in ("aaai.org", "ojs.aaai.org")):
        return len(path.strip("/")) > 4 and not path.rstrip("/").endswith(("/aaai", "/"))
    return path.endswith(".pdf") and any(marker in path for marker in ("paper", "proceedings", "content"))


def is_code_repo(url: str) -> bool:
    host = host_of(url)
    if host not in {"github.com", "gitlab.com", "bitbucket.org"}:
        return False
    parts = path_parts(url)
    return len(parts) >= 2 and parts[0].lower() not in {
        "features",
        "marketplace",
        "topics",
        "collections",
        "orgs",
        "search",
    }


def is_generic_or_dependency_url(url: str) -> bool:
    host = host_of(url)
    parts = path_parts(url)
    if host in {"github.com", "gitlab.com", "bitbucket.org"} and len(parts) < 2:
        return True
    if host in {
        "github.com",
        "gitlab.com",
        "bitbucket.org",
        "blender.org",
        "www.blender.org",
        "python.org",
        "pytorch.org",
        "huggingface.co",
    } and len(parts) == 0:
        return True
    return False


def is_project_url(url: str, context: str = "") -> bool:
    host = host_of(url)
    if is_generic_or_dependency_url(url):
        return False
    if is_paper_url(url):
        return False
    if is_code_repo(url):
        return True
    if host.endswith("github.io") or "huggingface.co" in host:
        return True
    return bool(PROJECT_CONTEXT.search(context))


def classify_markdown_link(label: str, url: str, context: str = "") -> str:
    label_l = (label or "").lower()
    url_l = (url or "").lower()
    if "code" in label_l or "github" in label_l or "repo" in label_l or is_code_repo(url):
        return "code" if is_code_repo(url) else ""
    if "project" in label_l or "homepage" in label_l or "website" in label_l or "demo" in label_l:
        return "project" if is_project_url(url, context) else ""
    if "paper" in label_l or "arxiv" in label_l or "openreview" in label_l or "doi" in label_l or "pdf" in label_l:
        return "paper" if is_paper_url(url) else ""
    if is_paper_url(url):
        return "paper"
    if is_project_url(url, context):
        return "code" if is_code_repo(url) else "project"
    return ""


def yaml_value(value: str) -> str:
    value = (value or "").strip()
    if not value or value.lower() in {"null", "none"}:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    return value.strip()


def frontmatter(text: str) -> tuple[str, str, str]:
    if not text.startswith("---\n"):
        return "", text, ""
    end = text.find("\n---", 4)
    if end == -1:
        return "", text, ""
    return text[:4], text[4:end], text[end:]


def parse_frontmatter_scalars(text: str) -> dict[str, str]:
    _, fm, _ = frontmatter(text)
    result: dict[str, str] = {}
    for match in FM_SCALAR_RE.finditer(fm):
        result[match.group("key").strip()] = yaml_value(match.group("value"))
    return result


def line_number(text: str, offset: int) -> int:
    return text[:offset].count("\n") + 1


def parse_note(path: Path) -> NoteInfo:
    text = path.read_text(encoding="utf-8", errors="ignore")
    scalars = parse_frontmatter_scalars(text)
    rel_note = str(path.relative_to(REPO_ROOT))
    info = NoteInfo(
        path=path,
        title=scalars.get("title", ""),
        pdf_ref=scalars.get("pdf_ref", ""),
        openreview_forum_id=scalars.get("openreview_forum_id", ""),
        project_link=scalars.get("project_link", ""),
        code_link=scalars.get("code_link", ""),
    )
    if info.project_link and not is_empty(info.project_link):
        info.source_links.append(LinkCandidate("project", clean_url(info.project_link), "note_frontmatter", "project_link", 0.99, rel_note))
    if info.code_link and not is_empty(info.code_link):
        info.source_links.append(LinkCandidate("code", clean_url(info.code_link), "note_frontmatter", "code_link", 0.99, rel_note))
    if info.openreview_forum_id:
        info.paper_links.append(
            LinkCandidate(
                "paper",
                f"https://openreview.net/forum?id={info.openreview_forum_id}",
                "note_frontmatter",
                "openreview_forum_id",
                0.98,
                rel_note,
            )
        )

    for current_line, line in enumerate(text.splitlines(), start=1):
        if not re.match(r"^\|\s*Links\s*\|", line, flags=re.I):
            continue
        for match in MD_LINK_RE.finditer(line):
            label, raw_url = match.groups()
            url = clean_url(raw_url)
            kind = classify_markdown_link(label, url, line)
            if not kind:
                continue
            if kind == "paper" and label.strip().lower() != "paper":
                continue
            candidate = LinkCandidate(
                kind=kind,
                url=canonical_paper_url(url) if kind == "paper" else url,
                source="note_links_row",
                evidence=label,
                confidence=0.98 if label.lower() in {"paper", "code", "project"} else 0.94,
                note_path=rel_note,
                line=current_line,
            )
            if kind == "paper":
                info.paper_links.append(candidate)
            else:
                info.source_links.append(candidate)
    info.paper_links = dedupe_links(info.paper_links)
    info.source_links = dedupe_links(info.source_links)
    return info


def dedupe_links(candidates: list[LinkCandidate]) -> list[LinkCandidate]:
    best: dict[tuple[str, str], LinkCandidate] = {}
    for item in candidates:
        url = clean_url(item.url)
        if not url:
            continue
        key = (item.kind, canonical_paper_url(url) if item.kind == "paper" else url.rstrip("/"))
        current = best.get(key)
        if current is None or item.confidence > current.confidence:
            item.url = key[1]
            best[key] = item
    return sorted(best.values(), key=lambda item: (item.confidence, item.kind == "code"), reverse=True)


def note_rel_pdf_keys(note: NoteInfo) -> list[str]:
    value = note.pdf_ref.strip().replace("\\", "/")
    if value.startswith("obsidian-vault/"):
        value = value[len("obsidian-vault/") :]
    keys = []
    if value:
        keys.append(value.lower())
        keys.append(Path(value).name.lower())
    return keys


def row_pdf_keys(row: dict[str, str]) -> list[str]:
    value = (row.get("pdf_path") or row.get("path") or "").strip().replace("\\", "/")
    if value.startswith(str(REPO_ROOT)):
        try:
            value = str(Path(value).relative_to(REPO_ROOT))
        except ValueError:
            pass
    if value.startswith("obsidian-vault/"):
        value = value[len("obsidian-vault/") :]
    keys = []
    if value:
        keys.append(value.lower())
        keys.append(Path(value).name.lower())
    return keys


def load_paper_list(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = []
        for line_no, row in enumerate(reader, start=2):
            row["_line_no"] = str(line_no)
            rows.append(row)
    return fieldnames, rows


def write_paper_list(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    clean_rows = [{key: value for key, value in row.items() if key != "_line_no"} for row in rows]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(clean_rows)


def build_note_indexes(notes: list[NoteInfo]) -> tuple[dict[str, list[NoteInfo]], dict[str, list[NoteInfo]]]:
    title_index: dict[str, list[NoteInfo]] = {}
    pdf_index: dict[str, list[NoteInfo]] = {}
    for note in notes:
        key = normalize_title(note.title)
        if key:
            title_index.setdefault(key, []).append(note)
        for pdf_key in note_rel_pdf_keys(note):
            pdf_index.setdefault(pdf_key, []).append(note)
    return title_index, pdf_index


def match_note(row: dict[str, str], title_index: dict[str, list[NoteInfo]], pdf_index: dict[str, list[NoteInfo]], notes: list[NoteInfo]) -> tuple[NoteInfo | None, str]:
    row_title = row.get("paper_title") or row.get("title") or ""
    title_key = normalize_title(row_title)
    if title_key:
        exact = title_index.get(title_key, [])
        if len(exact) == 1:
            return exact[0], "title_exact"
        if len(exact) > 1:
            pdf_matches = candidates_by_pdf(row, exact)
            if len(pdf_matches) == 1:
                return pdf_matches[0], "title_exact_pdf_disambiguated"
    for pdf_key in row_pdf_keys(row):
        matches = pdf_index.get(pdf_key, [])
        if len(matches) == 1 and titles_compatible(matches[0].title, row_title)[0]:
            return matches[0], "pdf_title_compatible"
        compatible = [note for note in matches if titles_compatible(note.title, row_title)[0]]
        if len(compatible) == 1:
            return compatible[0], "pdf_disambiguated_by_title"
    compatible = []
    for note in notes:
        ok, reason = titles_compatible(note.title, row_title)
        if ok:
            compatible.append((note, reason))
    if len(compatible) == 1:
        return compatible[0][0], compatible[0][1]
    if len(compatible) > 1:
        pdf_matches = candidates_by_pdf(row, [item[0] for item in compatible])
        if len(pdf_matches) == 1:
            return pdf_matches[0], "fuzzy_pdf_disambiguated"
        return None, "ambiguous_title"
    return None, "no_matching_note"


def candidates_by_pdf(row: dict[str, str], candidates: list[NoteInfo]) -> list[NoteInfo]:
    row_keys = set(row_pdf_keys(row))
    return [note for note in candidates if row_keys & set(note_rel_pdf_keys(note))]


def first_page_text(pdf_path: Path) -> str:
    try:
        proc = subprocess.run(
            ["pdftotext", "-f", "1", "-l", "1", "-layout", str(pdf_path), "-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=25,
        )
    except Exception:
        return ""
    return proc.stdout or ""


def first_page_annotations(pdf_path: Path) -> list[str]:
    if fitz is None:
        return []
    urls: list[str] = []
    try:
        doc = fitz.open(pdf_path)
        if doc.page_count:
            page = doc[0]
            for link in page.get_links():
                uri = str(link.get("uri") or "")
                if uri.startswith("http"):
                    urls.append(uri)
        doc.close()
    except Exception:
        return urls
    return urls


def row_pdf_path(row: dict[str, str]) -> Path | None:
    value = (row.get("pdf_path") or row.get("path") or "").strip()
    if not value:
        return None
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path if path.exists() else None


def pdf_first_page_candidates(row: dict[str, str]) -> tuple[list[LinkCandidate], list[LinkCandidate]]:
    pdf_path = row_pdf_path(row)
    if not pdf_path:
        return [], []
    text = first_page_text(pdf_path)
    urls = [clean_url(url) for url in URL_RE.findall(text)]
    urls.extend(clean_url(url) for url in first_page_annotations(pdf_path))
    paper: list[LinkCandidate] = []
    source: list[LinkCandidate] = []
    for url in urls:
        if not url:
            continue
        context_index = text.find(url)
        context = text[max(0, context_index - 120) : context_index + len(url) + 120] if context_index != -1 else ""
        if is_paper_url(url):
            paper.append(LinkCandidate("paper", canonical_paper_url(url), "pdf_first_page", context.strip()[:220], 0.9))
        elif is_project_url(url, context):
            kind = "code" if is_code_repo(url) else "project"
            source.append(LinkCandidate(kind, url, "pdf_first_page", context.strip()[:220], 0.88))
    return dedupe_links(paper), dedupe_links(source)


def best_source_link(candidates: list[LinkCandidate]) -> LinkCandidate | None:
    candidates = [
        item
        for item in candidates
        if item.kind in {"code", "project"}
        and not is_paper_url(item.url)
        and not is_generic_or_dependency_url(item.url)
        and (item.kind != "code" or is_code_repo(item.url))
        and (item.kind != "project" or is_project_url(item.url, item.evidence))
    ]
    if not candidates:
        return None
    # paper_list uses one field; prefer repository/code when both exist.
    return sorted(candidates, key=lambda item: (item.kind == "code", item.confidence), reverse=True)[0]


def best_paper_link(candidates: list[LinkCandidate]) -> LinkCandidate | None:
    candidates = [item for item in candidates if item.kind == "paper" and is_paper_url(item.url)]
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: item.confidence, reverse=True)[0]


def rel_to_repo(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except Exception:
        return str(path)


def load_local_run_candidates() -> tuple[dict[str, list[LinkCandidate]], dict[str, list[LinkCandidate]]]:
    paper_by_note: dict[str, list[LinkCandidate]] = {}
    source_by_note: dict[str, list[LinkCandidate]] = {}
    if not RUNS_DIR.exists():
        return paper_by_note, source_by_note
    for manifest_path in RUNS_DIR.rglob("manifest.json"):
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        vault_export = manifest.get("vault_export") or {}
        note_path = str(vault_export.get("note_path") or "")
        if not note_path:
            continue
        try:
            note_rel = str(Path(note_path).resolve().relative_to(REPO_ROOT))
        except Exception:
            note_rel = note_path
        paper_link = clean_url(str(manifest.get("paper_link") or ""))
        if paper_link and is_paper_url(paper_link):
            paper_by_note.setdefault(note_rel, []).append(
                LinkCandidate("paper", canonical_paper_url(paper_link), "local_run_manifest", str(manifest_path.relative_to(REPO_ROOT)), 0.95, note_rel)
            )
        analysis_path = manifest_path.parent / "analysis" / "main_analysis.json"
        if not analysis_path.exists():
            continue
        try:
            analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        metadata = analysis.get("paper_metadata") or {}
        for key, kind in (("code_link", "code"), ("project_link", "project")):
            url = clean_url(str(metadata.get(key) or ""))
            if url and is_project_url(url):
                source_by_note.setdefault(note_rel, []).append(
                    LinkCandidate(kind, url, "local_run_main_analysis", key, 0.93, note_rel)
                )
        for item in analysis.get("source_links") or []:
            if not isinstance(item, dict):
                continue
            url = clean_url(str(item.get("url") or ""))
            label = str(item.get("label") or "")
            kind = classify_markdown_link(label, url)
            if kind in {"code", "project"} and is_project_url(url):
                source_by_note.setdefault(note_rel, []).append(
                    LinkCandidate(kind, url, "local_run_source_links", label, 0.91, note_rel)
                )
    for mapping in (paper_by_note, source_by_note):
        for key, values in list(mapping.items()):
            mapping[key] = dedupe_links(values)
    return paper_by_note, source_by_note


def load_external_project_candidates(paths: list[str]) -> dict[str, tuple[LinkCandidate, str]]:
    external: dict[str, tuple[LinkCandidate, str]] = {}
    for raw_path in paths:
        path = Path(raw_path)
        if not path.is_absolute():
            path = REPO_ROOT / path
        if not path.exists():
            raise SystemExit(f"external project candidate file not found: {path}")
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                line_no = str(row.get("csv_row_number") or row.get("row_number") or "").strip()
                if not line_no:
                    continue
                if (row.get("confidence_label") or "").strip().lower() != "high":
                    continue
                if (row.get("match_method") or "").strip() == "no_unique_analysis_note":
                    continue
                kind = (row.get("source_kind") or row.get("kind") or "").strip().lower()
                if kind not in {"code", "project"}:
                    continue
                url = clean_url(row.get("suggested_link") or row.get("new") or "")
                if not url:
                    continue
                evidence = row.get("source_evidence") or row.get("evidence") or row.get("source_label") or ""
                if kind == "code" and not is_code_repo(url):
                    continue
                if kind == "project" and not is_project_url(url, evidence):
                    continue
                try:
                    confidence = float(row.get("confidence") or 0.91)
                except ValueError:
                    confidence = 0.91
                note_path = (row.get("analysis_md_path") or row.get("note_path") or "").strip()
                candidate = LinkCandidate(
                    kind=kind,
                    url=url,
                    source=f"external:{path.relative_to(REPO_ROOT)}",
                    evidence=evidence,
                    confidence=max(confidence, 0.91),
                    note_path=note_path,
                )
                current = external.get(line_no)
                if current is None or candidate.confidence > current[0].confidence:
                    external[line_no] = (candidate, note_path)
    return external


def load_external_paper_candidates(paths: list[str]) -> dict[str, tuple[LinkCandidate, str]]:
    external: dict[str, tuple[LinkCandidate, str]] = {}
    for raw_path in paths:
        path = Path(raw_path)
        if not path.is_absolute():
            path = REPO_ROOT / path
        if not path.exists():
            raise SystemExit(f"external paper candidate file not found: {path}")
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                line_no = str(row.get("csv_line") or row.get("row_number") or row.get("csv_row_number") or "").strip()
                if not line_no:
                    continue
                url = clean_url(row.get("suggested_paper_link") or row.get("paper_link") or row.get("new") or "")
                if not url or not is_paper_url(url):
                    continue
                try:
                    confidence = float(row.get("confidence") or 0.95)
                except ValueError:
                    confidence = 0.95
                verification = (row.get("verification_status") or row.get("verification") or "").strip().lower()
                if verification == "verified":
                    confidence = max(confidence, 0.96)
                note_path = (row.get("analysis_md_path") or row.get("note_path") or "").strip()
                evidence = row.get("evidence") or row.get("verification") or "external paper-link candidate"
                candidate = LinkCandidate(
                    kind="paper",
                    url=canonical_paper_url(url),
                    source=f"external:{path.relative_to(REPO_ROOT)}",
                    evidence=evidence,
                    confidence=confidence,
                    note_path=note_path,
                )
                current = external.get(line_no)
                if current is None or candidate.confidence > current[0].confidence:
                    external[line_no] = (candidate, note_path)
    return external


def source_relevant_to_title(source: LinkCandidate, title: str) -> bool:
    if source.kind == "project":
        return True
    if source.source == "note_links_row":
        return True
    if source.kind != "code" or not is_code_repo(source.url):
        return False
    title_words = title_tokens(title)
    url_words = title_tokens(" ".join(path_parts(source.url)))
    # Frontmatter code links are LLM-extracted in some old runs. Require at
    # least one non-generic title token in the repository path before applying.
    return bool(title_words & url_words)


def format_md_link(kind: str, url: str) -> str:
    label = {"paper": "paper", "code": "Code", "project": "Project"}[kind]
    return f"[{label}]({url})"


def ensure_links_row(text: str, links: list[LinkCandidate]) -> str:
    additions = []
    for item in links:
        if item.url and item.url not in text:
            additions.append(format_md_link(item.kind, item.url))
    if not additions:
        return text
    addition_text = " · ".join(additions)
    match = LINKS_ROW_RE.search(text)
    if match:
        current = match.group(2).strip()
        if current:
            new_content = f"{current} · {addition_text}"
        else:
            new_content = addition_text
        new_row = f"{match.group(1)}{new_content}{match.group(3)}"
        return text[: match.start()] + new_row + text[match.end() :]
    venue_match = VENUE_ROW_RE.search(text)
    new_row = f"| Links | {addition_text} |"
    if venue_match:
        return text[: venue_match.end()] + "\n" + new_row + text[venue_match.end() :]
    return text


def set_frontmatter_link(text: str, key: str, url: str) -> str:
    prefix, fm, rest = frontmatter(text)
    if not fm:
        return text
    lines = fm.splitlines()
    key_re = re.compile(rf"^{re.escape(key)}:\s*")
    for index, line in enumerate(lines):
        if key_re.match(line):
            current = yaml_value(line.split(":", 1)[1])
            if is_empty(current):
                lines[index] = f"{key}: {url}"
            return prefix + "\n".join(lines) + rest
    insert_at = 0
    for index, line in enumerate(lines):
        if line.startswith("pdf_ref:"):
            insert_at = index + 1
            break
    lines.insert(insert_at, f"{key}: {url}")
    return prefix + "\n".join(lines) + rest


def update_note_text(text: str, paper: LinkCandidate | None, source: LinkCandidate | None) -> str:
    links = []
    if paper:
        links.append(paper)
    if source:
        links.append(source)
    new_text = ensure_links_row(text, links)
    if source:
        fm_key = "code_link" if source.kind == "code" else "project_link"
        new_text = set_frontmatter_link(new_text, fm_key, source.url)
    return new_text


def write_jsonl(path: Path, records: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_csv(path: Path, records: list[dict]) -> None:
    fieldnames = [
        "row_number",
        "column",
        "title",
        "old",
        "new",
        "kind",
        "confidence",
        "source",
        "evidence",
        "note_path",
        "match_method",
        "apply",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow({key: record.get(key, "") for key in fieldnames})


def parse_states(value: str) -> set[str]:
    return {item.strip() for item in value.split(",") if item.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-list", default=str(PAPER_LIST))
    parser.add_argument("--analysis-dir", default=str(ANALYSIS_DIR))
    parser.add_argument("--out-dir", default=str(OUT_DIR))
    parser.add_argument("--states", default="", help="Comma-separated row states to process; empty means all states.")
    parser.add_argument("--min-confidence", type=float, default=0.9)
    parser.add_argument("--include-local-run-source-links", action="store_true")
    parser.add_argument(
        "--external-project-candidates",
        action="append",
        default=[],
        help="CSV candidates from a sidecar project/code-link audit; repeat as needed.",
    )
    parser.add_argument(
        "--external-paper-candidates",
        action="append",
        default=[],
        help="CSV candidates from a sidecar paper-link audit; repeat as needed.",
    )
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    paper_list = Path(args.paper_list)
    analysis_dir = Path(args.analysis_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    states = parse_states(args.states)

    fieldnames, rows = load_paper_list(paper_list)
    notes = [parse_note(path) for path in sorted(analysis_dir.rglob("*.md")) if path.name != "README.md"]
    title_index, pdf_index = build_note_indexes(notes)
    notes_by_rel = {str(note.path.relative_to(REPO_ROOT)): note for note in notes}
    run_paper_by_note, run_source_by_note = load_local_run_candidates()
    external_project = load_external_project_candidates(args.external_project_candidates)
    external_paper = load_external_paper_candidates(args.external_paper_candidates)

    records: list[dict] = []
    skip_reasons: dict[str, int] = {}
    note_updates: dict[Path, tuple[LinkCandidate | None, LinkCandidate | None]] = {}

    for row in rows:
        if states and row.get("state", "") not in states:
            skip_reasons["state_filter"] = skip_reasons.get("state_filter", 0) + 1
            continue
        note, match_method = match_note(row, title_index, pdf_index, notes)
        external_paper_link, external_paper_note_path = external_paper.get(row["_line_no"], (None, ""))
        external_source, external_note_path = external_project.get(row["_line_no"], (None, ""))
        fallback_note_path = external_source.note_path if external_source is not None else ""
        fallback_note_path = external_paper_note_path or external_note_path or fallback_note_path
        if note is None and fallback_note_path:
            note = notes_by_rel.get(fallback_note_path)
            if note is not None:
                match_method = "external_candidate_note_path"
        if note is None:
            skip_reasons[match_method] = skip_reasons.get(match_method, 0) + 1
            continue
        note_rel = str(note.path.relative_to(REPO_ROOT))
        pdf_paper, pdf_source = pdf_first_page_candidates(row)
        paper_candidates = dedupe_links([
            *note.paper_links,
            *run_paper_by_note.get(note_rel, []),
            *pdf_paper,
        ])
        if external_paper_link is not None:
            paper_candidates.append(external_paper_link)
            paper_candidates = dedupe_links(paper_candidates)
        source_candidates = [*note.source_links, *pdf_source]
        if args.include_local_run_source_links:
            source_candidates.extend(run_source_by_note.get(note_rel, []))
        if external_source is not None:
            source_candidates.append(external_source)
        source_candidates = [
            item for item in dedupe_links(source_candidates)
            if source_relevant_to_title(item, row.get("paper_title", ""))
        ]
        paper = best_paper_link(paper_candidates)
        source = best_source_link(source_candidates)
        planned_paper: LinkCandidate | None = None
        planned_source: LinkCandidate | None = None

        if is_empty(row.get("paper_link", "")) and paper and paper.confidence >= args.min_confidence:
            records.append({
                "row_number": row["_line_no"],
                "column": "paper_link",
                "title": row.get("paper_title", ""),
                "old": row.get("paper_link", ""),
                "new": paper.url,
                "kind": paper.kind,
                "confidence": paper.confidence,
                "source": paper.source,
                "evidence": paper.evidence,
                "note_path": note_rel,
                "match_method": match_method,
                "apply": True,
            })
            planned_paper = paper
        elif is_empty(row.get("paper_link", "")):
            skip_reasons["missing_paper_no_confident_candidate"] = skip_reasons.get("missing_paper_no_confident_candidate", 0) + 1

        if is_empty(row.get("project_link_or_github_link", "")) and source and source.confidence >= args.min_confidence:
            records.append({
                "row_number": row["_line_no"],
                "column": "project_link_or_github_link",
                "title": row.get("paper_title", ""),
                "old": row.get("project_link_or_github_link", ""),
                "new": source.url,
                "kind": source.kind,
                "confidence": source.confidence,
                "source": source.source,
                "evidence": source.evidence,
                "note_path": note_rel,
                "match_method": match_method,
                "apply": True,
            })
            planned_source = source
        elif is_empty(row.get("project_link_or_github_link", "")):
            skip_reasons["missing_project_no_confident_candidate"] = skip_reasons.get("missing_project_no_confident_candidate", 0) + 1

        if planned_paper or planned_source:
            old_paper, old_source = note_updates.get(note.path, (None, None))
            note_updates[note.path] = (planned_paper or old_paper, planned_source or old_source)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    write_jsonl(out_dir / "link_completion_candidates.jsonl", records)
    write_csv(out_dir / "link_completion_candidates.csv", records)

    summary = {
        "paper_list": rel_to_repo(paper_list),
        "analysis_dir": rel_to_repo(analysis_dir),
        "apply": args.apply,
        "min_confidence": args.min_confidence,
        "states": sorted(states),
        "candidate_updates": len(records),
        "paper_link_updates": sum(1 for record in records if record["column"] == "paper_link"),
        "project_or_code_updates": sum(1 for record in records if record["column"] == "project_link_or_github_link"),
        "note_update_count": len(note_updates),
        "skip_reasons": skip_reasons,
        "candidates_jsonl": rel_to_repo(out_dir / "link_completion_candidates.jsonl"),
        "candidates_csv": rel_to_repo(out_dir / "link_completion_candidates.csv"),
    }

    if args.apply:
        before_path = out_dir / f"paper_list.before_{timestamp}.csv"
        shutil.copy2(paper_list, before_path)
        row_by_line = {row["_line_no"]: row for row in rows}
        for record in records:
            row_by_line[str(record["row_number"])][record["column"]] = str(record["new"])
        write_paper_list(paper_list, fieldnames, rows)

        md_before_dir = out_dir / f"md_before_{timestamp}"
        md_changed = 0
        for note_path, (paper, source) in note_updates.items():
            text = note_path.read_text(encoding="utf-8", errors="ignore")
            new_text = update_note_text(text, paper, source)
            if new_text == text:
                continue
            rel = note_path.relative_to(REPO_ROOT)
            backup = md_before_dir / rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            backup.write_text(text, encoding="utf-8")
            note_path.write_text(new_text, encoding="utf-8")
            md_changed += 1
        summary["paper_list_before"] = rel_to_repo(before_path)
        summary["md_before_dir"] = rel_to_repo(md_before_dir) if md_changed else ""
        summary["md_changed"] = md_changed

    (out_dir / "link_completion_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
