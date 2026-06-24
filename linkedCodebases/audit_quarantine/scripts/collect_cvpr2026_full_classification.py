#!/usr/bin/env python3
"""Collect and classify CVPR 2026 papers for paper_list.csv.

This is intentionally a one-off collector: the source pages and derived CSVs are
saved under paperSources so the selection can be audited before appending.
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import re
import subprocess
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "paperSources" / "cvpr2026_full_collect_20260612"
PAPER_LIST = ROOT / "obsidian-vault" / "paper_list.csv"

CVF_OPENACCESS_URL = "https://openaccess.thecvf.com/CVPR2026?day=all"
CVPR_ORALS_URL = "https://cvpr.thecvf.com/virtual/2026/events/Oral"
CVPR_PAPERS_URL = "https://cvpr.thecvf.com/virtual/2026/papers.html"
TOP_README_URL = "https://raw.githubusercontent.com/SkalskiP/top-cvpr-2026-papers/master/README.md"
TOP_DATA_URL = "https://raw.githubusercontent.com/SkalskiP/top-cvpr-2026-papers/master/automation/data.csv"
PROGRAM_PDF_URL = "https://media.eventhosts.cc/Conferences/CVPR2026/CVPR_main_conf_2026_15.pdf"
AWARDS_URL = "https://www.newswise.com/articles/cvpr-2026-honors-the-year-s-most-innovative-computer-vision-and-ai-research"


PRIMARY_CATEGORIES = [
    "LLM / Vision-Language / Multimodal LMM",
    "Generative Models / Diffusion / Unified Gen-Understanding",
    "Agentic / Embodied / Planning",
    "Reinforcement Learning",
    "Character Animation / Motion Generation / Understanding",
    "3D Vision / Geometry / Reconstruction",
    "Segmentation / Detection / Tracking",
    "Robotics / Autonomous Driving",
    "Datasets / Benchmarks / Evaluation",
    "Efficiency / Systems / Compression",
    "Safety / Robustness / Privacy",
    "Medical / Scientific Vision",
    "Image Restoration / Computational Imaging",
    "Representation / Self-Supervised / Transfer",
    "Other Vision / Applications",
]


@dataclass
class Paper:
    title: str
    authors: str = ""
    openaccess_html: str = ""
    cvf_pdf: str = ""
    arxiv: str = ""
    supp: str = ""
    bibtex: str = ""
    project_link: str = ""
    code_link: str = ""
    huggingface: str = ""
    youtube: str = ""
    virtual_link: str = ""
    virtual_id: str = ""
    top_topic: str = ""
    top_session: str = ""
    top_highlight: str = ""
    oral_session: str = ""
    final_award: str = ""
    award_candidate: bool = False
    categories: list[str] = field(default_factory=list)
    primary_category: str = ""
    importance: str = ""
    importance_score: int = 0
    importance_reason: str = ""
    selected_reason: str = ""
    source_tags: list[str] = field(default_factory=list)

    @property
    def best_link(self) -> str:
        return self.arxiv or self.openaccess_html or self.cvf_pdf or self.virtual_link

    @property
    def best_project(self) -> str:
        return self.project_link or self.code_link or self.huggingface or self.youtube


def fetch_text(url: str, path: Path, *, binary: bool = False) -> bytes | str:
    if path.exists() and path.stat().st_size > 0:
        return path.read_bytes() if binary else path.read_text(encoding="utf-8", errors="ignore")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, timeout=90, headers=headers)
    response.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    if binary:
        path.write_bytes(response.content)
        return response.content
    path.write_text(response.text, encoding="utf-8")
    return response.text


def normalize_title(title: str) -> str:
    title = html.unescape(title)
    title = title.replace("³", "3").replace("²", "2").replace("×", "x")
    title = title.replace("–", "-").replace("—", "-").replace("‑", "-")
    title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def loose_title(title: str) -> str:
    s = normalize_title(title)
    s = re.sub(r"\b(cvpr|paper|html|pdf)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def contains_any(text: str, terms: Iterable[str]) -> bool:
    low = text.lower()
    return any(term in low for term in terms)


def term_matches(text: str, term: str) -> bool:
    parts = [part for part in re.split(r"[\s\-]+", term.lower()) if part]
    pattern = r"[\s\-]+".join(re.escape(part) for part in parts)
    if term[0].isalnum():
        pattern = r"\b" + pattern
    if term[-1].isalnum():
        pattern = pattern + r"\b"
    return re.search(pattern, text) is not None


def parse_openaccess(html_text: str) -> dict[str, Paper]:
    soup = BeautifulSoup(html_text, "html.parser")
    papers: dict[str, Paper] = {}
    for dt in soup.find_all("dt", class_="ptitle"):
        link = dt.find("a")
        if not link:
            continue
        title = html.unescape(link.get_text(" ", strip=True))
        paper = Paper(title=title)
        paper.openaccess_html = urljoin("https://openaccess.thecvf.com", link.get("href", ""))
        dds = []
        sib = dt.find_next_sibling()
        while sib and sib.name == "dd":
            dds.append(sib)
            sib = sib.find_next_sibling()
        if dds:
            author_links = dds[0].find_all("a")
            paper.authors = ", ".join(a.get_text(" ", strip=True) for a in author_links)
        for dd in dds[1:]:
            for a in dd.find_all("a"):
                label = a.get_text(" ", strip=True).lower()
                href = a.get("href", "")
                if label == "pdf":
                    paper.cvf_pdf = urljoin("https://openaccess.thecvf.com", href)
                elif label == "supp":
                    paper.supp = urljoin("https://openaccess.thecvf.com", href)
                elif label == "arxiv":
                    paper.arxiv = href
            bib = dd.find("div", class_="bibref")
            if bib:
                paper.bibtex = bib.get_text("\n", strip=True)
        paper.source_tags.append("cvf_openaccess")
        papers[normalize_title(title)] = paper
    return papers


def parse_event_cards(html_text: str) -> dict[str, dict[str, str]]:
    soup = BeautifulSoup(html_text, "html.parser")
    out: dict[str, dict[str, str]] = {}
    for card in soup.select(".event-card"):
        title_node = card.select_one(".event-title")
        link = title_node.find("a") if title_node else None
        title = title_node.get_text(" ", strip=True) if title_node else card.get("data-event-title", "")
        if not title:
            continue
        metadata = " | ".join(x.get_text(" ", strip=True) for x in card.select(".meta-pill"))
        speakers = ""
        speaker_node = card.select_one(".event-speakers")
        if speaker_node:
            speakers = speaker_node.get_text(" ", strip=True)
        out[normalize_title(title)] = {
            "title": html.unescape(title),
            "event_id": card.get("data-event-id", ""),
            "event_type": card.get("data-event-type", ""),
            "href": urljoin("https://cvpr.thecvf.com", link.get("href", "")) if link else "",
            "metadata": metadata,
            "speakers": html.unescape(speakers),
        }
    return out


def parse_top_data(csv_text: str) -> dict[str, dict[str, str]]:
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    return {normalize_title(row["title"]): row for row in rows}


def parse_awards(news_html: str) -> dict[str, str]:
    text = html.unescape(re.sub("<[^>]+>", " ", news_html))
    text = re.sub(r"\s+", " ", text)
    known = {
        "Efficiently Reconstructing Dynamic Scenes One D4RT at a Time": "Best Paper",
        "Native and Compact Structured Latents for 3D Generation": "Best Student Paper",
        "NitroGen: An Open Foundation Model for Generalist Gaming Agents": "Best Paper Honorable Mention",
        "SAM 3D: 3Dfy Anything in Images": "Best Paper Honorable Mention",
        "ChordEdit: One-Step Low-Energy Transport for Image Editing": "Best Student Paper Honorable Mention",
    }
    awards = {}
    for title, label in known.items():
        if title in text:
            awards[normalize_title(title)] = label
    return awards


def run_pdftotext(pdf_path: Path, txt_path: Path) -> str:
    if txt_path.exists() and txt_path.stat().st_size > 0:
        return txt_path.read_text(encoding="utf-8", errors="ignore")
    subprocess.run(["pdftotext", str(pdf_path), str(txt_path)], check=True)
    return txt_path.read_text(encoding="utf-8", errors="ignore")


def score_categories(title: str, extra: str = "") -> tuple[list[str], str]:
    text = f"{title} {extra}".lower()
    scores: Counter[str] = Counter()

    def add(category: str, points: int, terms: Iterable[str]) -> None:
        for term in terms:
            if term_matches(text, term):
                scores[category] += points

    add(
        "LLM / Vision-Language / Multimodal LMM",
        4,
        [
            "vision-language",
            "vision language",
            "vlm",
            "mllm",
            "large multimodal",
            "multimodal large",
            "llava",
            "llm",
            "language model",
            "visual reasoning",
            "multimodal reasoning",
            "chain-of-thought",
            "caption",
            "vqa",
            "text-video",
            "text to video",
            "text-to-image",
            "text-to-motion",
            "instruction",
            "prompt",
        ],
    )
    add(
        "Generative Models / Diffusion / Unified Gen-Understanding",
        4,
        [
            "diffusion",
            "flow matching",
            "flow-based",
            "flow model",
            "generative",
            "generation",
            "generate",
            "image editing",
            "video editing",
            "text-to-image",
            "text-to-video",
            "text-to-motion",
            "autoregressive",
            "tokenizer",
            "latent",
            "vae",
            "world model",
            "unified",
            "synthesis",
            "inpainting",
            "restoration",
            "enhancement",
            "super-resolution",
            "neural rendering",
        ],
    )
    add(
        "Agentic / Embodied / Planning",
        4,
        [
            "agent",
            "agentic",
            "embodied",
            "planning",
            "navigation",
            "nav",
            "tool-aware",
            "tool use",
            "vision-language-action",
            "vla",
            "action model",
            "game",
            "gaming",
            "policy",
            "physical ai",
            "active mapping",
            "exploration",
            "manipulation",
        ],
    )
    add(
        "Reinforcement Learning",
        5,
        [
            "reinforcement learning",
            "reward",
            "grpo",
            "policy gradient",
            "rl",
            "preference optimization",
            "ppo",
            "q-learning",
            "bandit",
        ],
    )
    add(
        "Character Animation / Motion Generation / Understanding",
        6,
        [
            "motion generation",
            "motion synthesis",
            "motion understanding",
            "motion editing",
            "motion transfer",
            "motion control",
            "motion prediction",
            "motion capture",
            "motion recovery",
            "motion reconstruction",
            "motion interpolation",
            "motion generation",
            "motion editing",
            "motion synthesis",
            "motion reasoning",
            "motion representation",
            "motion-centric",
            "motion-focused",
            "motion alignment",
            "text-to-motion",
            "language to motion",
            "motion-language",
            "human motion",
            "human reaction",
            "human reconstruction",
            "human mesh",
            "human video",
            "human avatar",
            "digital human",
            "human generation",
            "human-object interaction",
            "human-object interactions",
            "human-human interaction",
            "human-human control",
            "human scene interaction",
            "human-scene interaction",
            "physics-based human-object",
            "physics-grounded human-human",
            "recovering physically plausible human-object",
            "character",
            "animation",
            "image animation",
            "video animation",
            "video character",
            "character video",
            "gesture",
            "co-speech",
            "dance",
            "sign language",
            "gait",
            "locomotion",
            "mocap",
            "human pose",
            "hand pose",
            "body pose",
            "pose-guided video",
            "pose-guided image",
            "pose transfer",
            "body motion",
            "hand motion",
            "whole-body",
            "full-body",
            "talking avatar",
            "head avatar",
            "portrait animation",
            "humanoid",
            "camera motion",
            "camera trajectory",
            "kinematics",
            "mesh recovery",
            "reenact",
            "avatar",
            "portrait animation",
        ],
    )
    add(
        "3D Vision / Geometry / Reconstruction",
        5,
        [
            "3d",
            "4d",
            "gaussian splatting",
            "gaussian",
            "reconstruction",
            "depth",
            "pose estimation",
            "view synthesis",
            "novel view",
            "nerf",
            "radiance field",
            "mesh",
            "point cloud",
            "geometry",
            "geometric",
            "sfm",
            "slam",
            "camera",
            "stereo",
            "surface",
            "scene",
            "occupancy",
            "spatial",
            "asset",
        ],
    )
    add(
        "Segmentation / Detection / Tracking",
        4,
        [
            "segmentation",
            "segment",
            "detection",
            "detect",
            "tracking",
            "tracker",
            "track",
            "correspondence",
            "matting",
            "recognition",
            "re-identification",
            "classification",
            "object",
        ],
    )
    add(
        "Robotics / Autonomous Driving",
        4,
        [
            "robot",
            "robotics",
            "autonomous",
            "driving",
            "lidar",
            "bev",
            "vehicle",
            "traffic",
            "trajectory prediction",
            "manipulation",
            "grasp",
            "tactile",
        ],
    )
    add(
        "Datasets / Benchmarks / Evaluation",
        4,
        [
            "benchmark",
            "dataset",
            "evaluation",
            "evaluating",
            "measure",
            "metrics",
            "taxonomy",
            "large-scale dataset",
        ],
    )
    add(
        "Efficiency / Systems / Compression",
        4,
        [
            "efficient",
            "efficiency",
            "accelerating",
            "compression",
            "quantization",
            "cache",
            "caching",
            "pruning",
            "distillation",
            "lightweight",
            "real-time",
            "edge",
            "scalable",
            "token merging",
        ],
    )
    add(
        "Safety / Robustness / Privacy",
        4,
        [
            "robust",
            "security",
            "privacy",
            "jailbreak",
            "red-team",
            "watermark",
            "adversarial",
            "attack",
            "defense",
            "ood",
            "out-of-distribution",
            "hallucinate",
            "hallucination",
            "uncertainty",
            "fairness",
            "unlearning",
        ],
    )
    add(
        "Medical / Scientific Vision",
        4,
        [
            "medical",
            "clinical",
            "anatomy",
            "tumor",
            "cancer",
            "radiology",
            "microscopy",
            "brain",
            "cell",
            "surgical",
        ],
    )
    add(
        "Image Restoration / Computational Imaging",
        4,
        [
            "imaging",
            "hyperspectral",
            "thermal",
            "infrared",
            "visible image fusion",
            "defocus",
            "speckle",
            "denoise",
            "deblur",
            "low-light",
            "super-resolution",
            "restoration",
            "camera",
            "sensor",
        ],
    )
    add(
        "Representation / Self-Supervised / Transfer",
        4,
        [
            "self-supervised",
            "representation",
            "pretraining",
            "transfer",
            "adaptation",
            "generalization",
            "test-time",
            "concept",
            "embedding",
            "feature",
            "domain",
        ],
    )

    if not scores:
        return ["Other Vision / Applications"], "Other Vision / Applications"

    ordered = [cat for cat, _ in scores.most_common()]
    if "Character Animation / Motion Generation / Understanding" in scores:
        primary = "Character Animation / Motion Generation / Understanding"
    else:
        primary = ordered[0]
    return ordered, primary


def has_oral_signal(paper: Paper) -> bool:
    return any(tag.startswith("cvpr_virtual_oral") for tag in paper.source_tags)


def compute_importance(paper: Paper) -> None:
    score = 0
    reasons = []
    if paper.final_award:
        if paper.final_award == "Best Paper":
            score += 120
        elif paper.final_award == "Best Student Paper":
            score += 110
        else:
            score += 95
        reasons.append(f"final_award:{paper.final_award}")
    if has_oral_signal(paper):
        score += 55
        reasons.append("oral")
    if paper.top_highlight == "Highlight":
        score += 45
        reasons.append("highlight")
    if paper.award_candidate:
        score += 25
        reasons.append("award_candidate")
    if paper.code_link:
        score += 8
        reasons.append("code")
    if paper.project_link or paper.huggingface:
        score += 6
        reasons.append("project_or_hf")
    hot_weights = {
        "LLM / Vision-Language / Multimodal LMM": 25,
        "Generative Models / Diffusion / Unified Gen-Understanding": 23,
        "Agentic / Embodied / Planning": 22,
        "Reinforcement Learning": 18,
        "3D Vision / Geometry / Reconstruction": 22,
        "Character Animation / Motion Generation / Understanding": 30,
        "Datasets / Benchmarks / Evaluation": 10,
        "Efficiency / Systems / Compression": 8,
        "Safety / Robustness / Privacy": 8,
    }
    for cat in paper.categories:
        if cat in hot_weights:
            score += hot_weights[cat]
            reasons.append(f"hot:{cat}")
    if paper.top_topic:
        score += 10
        reasons.append(f"top_repo_topic:{paper.top_topic}")
    paper.importance_score = score
    if score >= 100 or paper.final_award:
        paper.importance = "S"
    elif score >= 65:
        paper.importance = "A"
    elif score >= 35:
        paper.importance = "B"
    else:
        paper.importance = ""
    paper.importance_reason = ";".join(reasons)


def load_existing_keys() -> tuple[set[str], set[str]]:
    title_keys: set[str] = set()
    link_keys: set[str] = set()
    with PAPER_LIST.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            title_keys.add(normalize_title(row.get("paper_title", "")))
            link = row.get("paper_link", "").strip()
            if link:
                link_keys.add(normalize_link(link))
    return title_keys, link_keys


def normalize_link(link: str) -> str:
    link = link.strip()
    link = re.sub(r"[?#].*$", "", link)
    link = link.replace("/pdf/", "/abs/")
    link = re.sub(r"\.pdf$", "", link)
    link = re.sub(r"v\d+$", "", link)
    return link.rstrip("/")


def merge_near_matches(papers: dict[str, Paper], signals: dict[str, dict[str, str]]) -> dict[str, tuple[str, dict[str, str]]]:
    matched: dict[str, tuple[str, dict[str, str]]] = {}
    paper_keys = list(papers)
    loose_to_key = {loose_title(papers[k].title): k for k in paper_keys}
    for key, signal in signals.items():
        if key in papers:
            matched[key] = (key, signal)
            continue
        loose = loose_title(signal.get("title", ""))
        if loose in loose_to_key:
            matched[loose_to_key[loose]] = (key, signal)
            continue
        compact = loose.replace(" ", "")
        found = ""
        for lk, pk in loose_to_key.items():
            if compact and (compact in lk.replace(" ", "") or lk.replace(" ", "") in compact):
                found = pk
                break
        if found:
            matched[found] = (key, signal)
    return matched


def build_rows(papers: list[Paper]) -> list[dict[str, str]]:
    rows = []
    for p in papers:
        sort = (
            "CVPR_2026_full_collect_20260612"
            f" | {p.primary_category}"
            f" | score={p.importance_score}"
            f" | reason={p.selected_reason}"
        )
        rows.append(
            {
                "state": "Wait",
                "importance": p.importance,
                "paper_title": p.title,
                "venue": "CVPR 2026",
                "project_link_or_github_link": p.best_project,
                "paper_link": p.best_link,
                "sort": sort[:500],
                "pdf_path": "",
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--append", action="store_true", help="Append selected rows to obsidian-vault/paper_list.csv")
    parser.add_argument("--limit-non-motion", type=int, default=1000)
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    open_html = fetch_text(CVF_OPENACCESS_URL, OUT_DIR / "cvpr2026_openaccess_all.html")
    oral_html = fetch_text(CVPR_ORALS_URL, OUT_DIR / "cvpr2026_virtual_orals.html")
    papers_html = fetch_text(CVPR_PAPERS_URL, OUT_DIR / "cvpr2026_virtual_papers.html")
    top_readme = fetch_text(TOP_README_URL, OUT_DIR / "top_cvpr_2026_papers_README.md")
    top_csv = fetch_text(TOP_DATA_URL, OUT_DIR / "top_cvpr_2026_papers_data.csv")
    awards_html = fetch_text(AWARDS_URL, OUT_DIR / "cvpr2026_awards_newswise.html")
    program_pdf = fetch_text(PROGRAM_PDF_URL, OUT_DIR / "CVPR_main_conf_2026_15.pdf", binary=True)
    assert isinstance(program_pdf, bytes)
    program_text = run_pdftotext(OUT_DIR / "CVPR_main_conf_2026_15.pdf", OUT_DIR / "CVPR_main_conf_2026_15.txt")

    papers = parse_openaccess(open_html)
    openaccess_count = len(papers)
    oral_signals = parse_event_cards(oral_html)
    paper_page_signals = parse_event_cards(papers_html)
    top_signals = parse_top_data(top_csv)
    awards = parse_awards(awards_html)

    oral_matches = merge_near_matches(papers, oral_signals)
    for paper_key, (_, signal) in oral_matches.items():
        p = papers[paper_key]
        p.oral_session = signal.get("metadata", "")
        p.virtual_link = signal.get("href", "")
        p.virtual_id = signal.get("event_id", "")
        p.source_tags.append("cvpr_virtual_oral")

    matched_oral_signal_keys = {signal_key for signal_key, _ in oral_matches.values()}
    for signal_key, signal in oral_signals.items():
        if signal_key in matched_oral_signal_keys:
            continue
        title = signal.get("title", "")
        if not title:
            continue
        fallback_key = normalize_title(title)
        if fallback_key in papers:
            continue
        papers[fallback_key] = Paper(
            title=title,
            authors=signal.get("speakers", ""),
            virtual_link=signal.get("href", ""),
            virtual_id=signal.get("event_id", ""),
            oral_session=signal.get("metadata", ""),
            source_tags=["cvpr_virtual_oral_unmatched"],
        )

    poster_matches = merge_near_matches(papers, paper_page_signals)
    for paper_key, (_, signal) in poster_matches.items():
        p = papers[paper_key]
        if not p.virtual_link:
            p.virtual_link = signal.get("href", "")
        if not p.virtual_id:
            p.virtual_id = signal.get("event_id", "")
        p.source_tags.append("cvpr_virtual_papers")

    top_matches = merge_near_matches(papers, top_signals)
    for paper_key, (_, signal) in top_matches.items():
        p = papers[paper_key]
        p.top_topic = signal.get("topic", "")
        p.top_session = signal.get("session", "")
        p.top_highlight = signal.get("highlight", "")
        p.code_link = signal.get("code", "")
        p.huggingface = signal.get("huggingface", "")
        p.youtube = signal.get("youtube", "")
        if signal.get("paper", "").startswith("http"):
            if "arxiv.org" in signal["paper"]:
                p.arxiv = p.arxiv or signal["paper"]
            elif not p.project_link:
                p.project_link = signal["paper"]
        p.award_candidate = signal.get("highlight") == "Award Candidate"
        p.source_tags.append("top_cvpr_2026_repo")

    for key, label in awards.items():
        if key in papers:
            papers[key].final_award = label
            papers[key].source_tags.append("cvf_awards_newswise")
        else:
            loose_key = loose_title(key)
            for pk in papers:
                if loose_title(papers[pk].title) == loose_key:
                    papers[pk].final_award = label
                    papers[pk].source_tags.append("cvf_awards_newswise")
                    break

    for p in papers.values():
        extra = " ".join([p.top_topic, p.top_session, p.oral_session, p.authors])
        p.categories, p.primary_category = score_categories(p.title, extra)
        # Top repository topics are human-curated enough to override only when
        # they point to a clear primary bucket and motion is not involved.
        if p.primary_category != "Character Animation / Motion Generation / Understanding":
            topic_map = {
                "3D Vision": "3D Vision / Geometry / Reconstruction",
                "Generative Models": "Generative Models / Diffusion / Unified Gen-Understanding",
                "Vision-Language Models": "LLM / Vision-Language / Multimodal LMM",
                "Agents": "Agentic / Embodied / Planning",
                "Segmentation": "Segmentation / Detection / Tracking",
                "Object Tracking": "Segmentation / Detection / Tracking",
                "Pose Estimation": "3D Vision / Geometry / Reconstruction",
                "Depth Estimation": "3D Vision / Geometry / Reconstruction",
                "Video Understanding": "LLM / Vision-Language / Multimodal LMM",
                "Physical Modeling": "3D Vision / Geometry / Reconstruction",
                "Image-to-Image": "Generative Models / Diffusion / Unified Gen-Understanding",
            }
            if p.top_topic in topic_map:
                p.primary_category = topic_map[p.top_topic]
                if p.primary_category not in p.categories:
                    p.categories.insert(0, p.primary_category)
        compute_importance(p)

    all_papers = sorted(papers.values(), key=lambda p: normalize_title(p.title))
    motion = [p for p in all_papers if p.primary_category == "Character Animation / Motion Generation / Understanding"]
    non_motion = [p for p in all_papers if p.primary_category != "Character Animation / Motion Generation / Understanding"]
    forced_non_motion = [p for p in non_motion if has_oral_signal(p) or p.final_award]
    forced_keys = {normalize_title(p.title) for p in forced_non_motion}
    remaining_non_motion = [p for p in non_motion if normalize_title(p.title) not in forced_keys]
    remaining_non_motion_sorted = sorted(remaining_non_motion, key=lambda p: (-p.importance_score, normalize_title(p.title)))
    fill_count = max(0, args.limit_non_motion - len(forced_non_motion))
    selected_non_motion = sorted(forced_non_motion, key=lambda p: (-p.importance_score, normalize_title(p.title)))
    selected_non_motion += remaining_non_motion_sorted[:fill_count]
    selected = selected_non_motion + sorted(motion, key=lambda p: (-p.importance_score, normalize_title(p.title)))
    selected_keys = {normalize_title(p.title) for p in selected}
    selected_non_motion_keys = {normalize_title(p.title) for p in selected_non_motion}
    for p in selected:
        if p.primary_category == "Character Animation / Motion Generation / Understanding":
            p.selected_reason = "all_category_5_motion"
        elif normalize_title(p.title) in forced_keys:
            forced_reasons = []
            if has_oral_signal(p):
                forced_reasons.append("oral")
            if p.final_award:
                forced_reasons.append("final_award")
            p.selected_reason = "forced_" + "_".join(forced_reasons)
        elif normalize_title(p.title) in selected_non_motion_keys:
            p.selected_reason = f"top_fill_to_{args.limit_non_motion}_non_motion_core"

    title_keys, link_keys = load_existing_keys()
    appendable = []
    skipped = []
    for p in selected:
        title_key = normalize_title(p.title)
        link_key = normalize_link(p.best_link) if p.best_link else ""
        if title_key in title_keys:
            skipped.append({"paper_title": p.title, "reason": "duplicate_title", "paper_link": p.best_link})
            continue
        if link_key and link_key in link_keys:
            skipped.append({"paper_title": p.title, "reason": "duplicate_link", "paper_link": p.best_link})
            continue
        appendable.append(p)

    classification_rows = []
    for p in all_papers:
        classification_rows.append(
            {
                "paper_title": p.title,
                "authors": p.authors,
                "primary_category": p.primary_category,
                "categories": "; ".join(p.categories),
                "importance": p.importance,
                "importance_score": str(p.importance_score),
                "importance_reason": p.importance_reason,
                "selected": "yes" if normalize_title(p.title) in selected_keys else "no",
                "selected_reason": p.selected_reason,
                "oral": "yes" if has_oral_signal(p) else "no",
                "final_award": p.final_award,
                "award_candidate": "yes" if p.award_candidate else "no",
                "oral_session": p.oral_session,
                "top_topic": p.top_topic,
                "top_highlight": p.top_highlight,
                "top_session": p.top_session,
                "openaccess_html": p.openaccess_html,
                "paper_link": p.best_link,
                "cvf_pdf": p.cvf_pdf,
                "project_or_code": p.best_project,
                "source_tags": ";".join(sorted(set(p.source_tags))),
            }
        )

    class_fields = list(classification_rows[0].keys())
    write_csv(OUT_DIR / "cvpr2026_full_classification.csv", classification_rows, class_fields)

    append_rows = build_rows(appendable)
    write_csv(
        OUT_DIR / "cvpr2026_selected_for_append.csv",
        append_rows,
        ["state", "importance", "paper_title", "venue", "project_link_or_github_link", "paper_link", "sort", "pdf_path"],
    )
    write_csv(OUT_DIR / "duplicates_skipped.csv", skipped, ["paper_title", "reason", "paper_link"])

    with (OUT_DIR / "cvpr2026_full_classification.jsonl").open("w", encoding="utf-8") as f:
        for row in classification_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    unmatched_top = sorted(set(top_signals) - {v[0] for v in top_matches.values()})
    summary = {
        "openaccess_papers": openaccess_count,
        "classified_total_papers": len(papers),
        "virtual_oral_unmatched_fallback_rows": len(papers) - openaccess_count,
        "virtual_oral_cards": len(oral_signals),
        "virtual_oral_matched_to_openaccess": len(oral_matches),
        "top_repo_rows": len(top_signals),
        "top_repo_matched_to_openaccess": len(top_matches),
        "top_repo_unmatched_titles": [top_signals[k]["title"] for k in unmatched_top],
        "final_awards_matched": Counter(p.final_award for p in all_papers if p.final_award),
        "category_counts": Counter(p.primary_category for p in all_papers),
        "multi_category_counts": Counter(cat for p in all_papers for cat in p.categories),
        "importance_counts": Counter(p.importance or "blank" for p in all_papers),
        "selected_total_before_existing_dedup": len(selected),
        "selected_non_motion_total": len(selected_non_motion),
        "selected_non_motion_forced_oral_or_award": len(forced_non_motion),
        "selected_non_motion_limit": args.limit_non_motion,
        "selected_motion_all": len(motion),
        "appendable_after_existing_dedup": len(appendable),
        "skipped_existing_duplicates": len(skipped),
        "program_text_contains_oral_session": program_text.count("Oral Session"),
        "top_readme_size": len(top_readme),
        "append_performed": args.append,
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.append and append_rows:
        with PAPER_LIST.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "state",
                    "importance",
                    "paper_title",
                    "venue",
                    "project_link_or_github_link",
                    "paper_link",
                    "sort",
                    "pdf_path",
                ],
            )
            writer.writerows(append_rows)

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
