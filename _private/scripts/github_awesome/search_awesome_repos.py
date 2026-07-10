#!/usr/bin/env python3

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import math
import re
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote_plus, unquote, urlparse

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
DEFAULT_TASK_FILE = ROOT / "awesome_repo_search_tasks.md"
RUNS_DIR = ROOT / "search_runs"


def find_vault_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError(f"Could not locate vault root from {start}")


VAULT_ROOT = find_vault_root(ROOT)

SEARCH_KEYWORD_LIMIT = 3
PROVISIONAL_TOP_K = 3
MAX_SEARCH_WORKERS = 1
MAX_FETCH_WORKERS = 8

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
)

CORE_DIRECTION_IDS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17}

MANUAL_SEEDS: dict[int, list[str]] = {
    1: [
        "AIDC-AI/Awesome-Unified-Multimodal-Models",
        "OpenEnvision-Lab/Awesome-Multimodal-Modeling",
    ],
    5: [
        "yuelinan/Awesome-Efficient-R1-style-LRMs",
    ],
    6: [
        "haoranD/Awesome-Embodied-AI",
        "DelinQu/awesome-vision-language-action-model",
    ],
    7: [
        "hyp1231/awesome-llm-powered-agent",
        "luo-junyu/Awesome-Agent-Papers",
        "VoltAgent/awesome-ai-agent-papers",
    ],
    8: [
        "worldbench/awesome-3d-4d-world-models",
    ],
    9: [
        "Danielskry/Awesome-RAG",
    ],
    12: [
        "AudioLLMs/Awesome-Audio-LLM",
    ],
    13: [
        "The-Martyr/Awesome-Multimodal-Reasoning",
        "Osilly/Awesome-Interleaving-Reasoning",
    ],
    17: [
        "knightnemo/Awesome-World-Models",
    ],
}

STOPWORDS = {
    "awesome",
    "curated",
    "list",
    "model",
    "models",
    "paper",
    "papers",
    "research",
    "repo",
    "repositories",
    "generation",
    "reasoning",
    "language",
    "large",
    "vision",
    "multimodal",
    "video",
    "llm",
    "mllm",
    "vlm",
    "and",
    "for",
    "the",
    "with",
    "text",
    "to",
    "of",
    "augmented",
}


@dataclass
class DirectionSpec:
    idx: int
    name: str
    known_candidates: list[str]
    keywords: list[str]
    goal: str


@dataclass
class SearchHit:
    repo: str
    query: str
    rank: int
    description: str
    title: str
    topics: list[str]
    search_star_text: str
    search_stars: int
    search_updated_text: str
    search_url: str


@dataclass
class RepoMetrics:
    repo: str
    name: str = ""
    description: str = ""
    homepage: str = ""
    stars: int = 0
    forks: int = 0
    open_issues: int = 0
    archived: bool = False
    default_branch: str = "main"
    html_url: str = ""
    topics: list[str] = field(default_factory=list)
    pushed_at: str = ""
    pushed_date: str = ""
    pushed_days_ago: int = 9999
    readme_url: str = ""
    readme_headings_h2: int = 0
    readme_headings_h3: int = 0
    readme_bullets: int = 0
    readme_tables: int = 0
    readme_research_terms: int = 0
    readme_years: int = 0
    readme_has_toc: bool = False
    readme_size: int = 0


@dataclass
class RankedRepo:
    repo: str
    direction_id: int
    direction_name: str
    score_total: float
    score_research: float
    score_structure: float
    score_recency: float
    score_community: float
    score_discovery: float
    stars: int
    pushed_date: str
    description: str
    reasoning: str
    search_queries: list[str]
    search_ranks: list[int]
    html_url: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def note_link_target(path: Path) -> str:
    try:
        relative = path.relative_to(VAULT_ROOT)
    except ValueError:
        relative = path
    if relative.suffix == ".md":
        relative = relative.with_suffix("")
    return relative.as_posix()


def parse_star_count(text: str) -> int:
    text = text.strip().lower().replace(",", "")
    if not text:
        return 0
    multiplier = 1
    if text.endswith("k"):
        multiplier = 1000
        text = text[:-1]
    elif text.endswith("m"):
        multiplier = 1_000_000
        text = text[:-1]
    try:
        return int(float(text) * multiplier)
    except ValueError:
        return 0


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_task_file(task_path: Path) -> list[DirectionSpec]:
    text = task_path.read_text(encoding="utf-8")
    section_re = re.compile(
        r"## 方向\s+(\d+):\s+(.+?)\n(.*?)(?=\n---\n\n## 方向\s+\d+:|\Z)",
        re.S,
    )
    directions: list[DirectionSpec] = []
    for match in section_re.finditer(text):
        idx = int(match.group(1))
        name = normalize_space(match.group(2))
        body = match.group(3)

        known_candidates: list[str] = []
        known_block = re.search(r"已知候选:\n(.*?)(?:\n\n搜索关键词:|\Z)", body, re.S)
        if known_block:
            known_candidates = re.findall(r"`([^`]+/[^`]+)`", known_block.group(1))

        keywords: list[str] = []
        kw_block = re.search(r"搜索关键词:\n(.*?)(?:\n\n目标:|\Z)", body, re.S)
        if kw_block:
            keywords = re.findall(r"-\s+`([^`]+)`", kw_block.group(1))

        goal_match = re.search(r"目标:\s*(.+)", body)
        goal = normalize_space(goal_match.group(1)) if goal_match else ""

        directions.append(
            DirectionSpec(
                idx=idx,
                name=name,
                known_candidates=known_candidates,
                keywords=keywords,
                goal=goal,
            )
        )

    if not directions:
        raise RuntimeError(f"Failed to parse directions from {task_path}")
    return directions


class GitHubClient:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "application/vnd.github+json",
            }
        )

    def get_text(self, url: str, accept: str | None = None) -> str:
        headers: dict[str, str] = {}
        if accept:
            headers["Accept"] = accept
        resp = self.session.get(url, headers=headers, timeout=40)
        resp.raise_for_status()
        return resp.text

    def get_json(self, url: str, accept: str | None = None) -> Any:
        headers: dict[str, str] = {}
        if accept:
            headers["Accept"] = accept
        resp = self.session.get(url, headers=headers, timeout=40)
        resp.raise_for_status()
        return resp.json()


def find_result_card(link) -> Any:
    node = link
    while node is not None:
        classes = node.get("class") or []
        class_blob = " ".join(classes)
        if "Repositories-module__resultRow" in class_blob or "Result-module__Result" in class_blob:
            return node
        node = node.parent
    return link.parent


def parse_search_results(html: str, query: str, url: str) -> list[SearchHit]:
    soup = BeautifulSoup(html, "html.parser")
    hits: list[SearchHit] = []
    seen: set[str] = set()
    for rank, link in enumerate(soup.select(".search-title a[href^='/']"), start=1):
        href = (link.get("href") or "").strip("/")
        if href.count("/") != 1 or href in seen:
            continue
        seen.add(href)
        card = find_result_card(link)
        card_text = normalize_space(card.get_text(" ", strip=True))
        desc = ""
        desc_node = card.find("p")
        if desc_node:
            desc = normalize_space(desc_node.get_text(" ", strip=True))
        topics = [
            normalize_space(a.get_text(" ", strip=True))
            for a in card.select("a[href*='/topics/']")
        ]
        star_text = ""
        for star_link in card.select("a[href$='/stargazers']"):
            star_text = normalize_space(star_link.get_text(" ", strip=True))
            if star_text:
                break
        search_stars = parse_star_count(star_text)
        updated_text = ""
        updated_match = re.search(
            r"·\s*Updated(?: on)?\s+(.+?)(?:\s+Star|$)",
            card_text,
        )
        if updated_match:
            updated_text = normalize_space(updated_match.group(1))

        hits.append(
            SearchHit(
                repo=href,
                query=query,
                rank=rank,
                description=desc,
                title=normalize_space(link.get_text(" ", strip=True)),
                topics=topics,
                search_star_text=star_text,
                search_stars=search_stars,
                search_updated_text=updated_text,
                search_url=url,
            )
        )
    return hits


def normalize_repo_url(url: str) -> str:
    parsed = urlparse(url)
    if "duckduckgo.com" in parsed.netloc:
        target = unquote(parse_qs(parsed.query).get("uddg", [""])[0])
        if target:
            return normalize_repo_url(target)
    if "github.com" not in parsed.netloc:
        return ""
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 2:
        return ""
    return f"{parts[0]}/{parts[1]}"


def search_candidates_duckduckgo(
    client: GitHubClient,
    spec: DirectionSpec,
    search_keyword_limit: int,
) -> list[SearchHit]:
    queries = spec.keywords[:search_keyword_limit]
    hits: list[SearchHit] = []
    for query in queries:
        ddg_query = f"{query} site:github.com"
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(ddg_query)}"
        html = ""
        last_exc: Exception | None = None
        for attempt in range(3):
            try:
                html = client.get_text(url, "text/html")
                last_exc = None
                break
            except Exception as exc:
                last_exc = exc
                time.sleep(1.2 * (attempt + 1))
        if last_exc is not None:
            print(f"[warn] ddg search failed for {spec.name} / {query}: {last_exc}")
            continue

        soup = BeautifulSoup(html, "html.parser")
        seen: set[str] = set()
        rank = 0
        for a in soup.select("a.result__a"):
            repo = normalize_repo_url(a.get("href") or "")
            if not repo or repo in seen:
                continue
            seen.add(repo)
            rank += 1
            row = a.find_parent("div", class_="result") or a.parent.parent
            snippet_node = row.select_one(".result__snippet") if row else None
            snippet = normalize_space(snippet_node.get_text(" ", strip=True)) if snippet_node else ""
            title = normalize_space(a.get_text(" ", strip=True))
            hits.append(
                SearchHit(
                    repo=repo,
                    query=query,
                    rank=rank,
                    description=snippet,
                    title=title,
                    topics=[],
                    search_star_text="",
                    search_stars=0,
                    search_updated_text="",
                    search_url=url,
                )
            )
        time.sleep(0.8)
    return hits


def search_candidates(
    client: GitHubClient,
    spec: DirectionSpec,
    search_keyword_limit: int,
) -> list[SearchHit]:
    return search_candidates_duckduckgo(client, spec, search_keyword_limit)


def coarse_text_score(text: str, positive_terms: list[str], negative_terms: list[str]) -> float:
    text_l = text.lower()
    score = 0.0
    for term in positive_terms:
        if term in text_l:
            score += 1.0
    for term in negative_terms:
        if term in text_l:
            score -= 1.0
    return score


def direction_search_score(spec: DirectionSpec, hits: list[SearchHit], repo: str) -> float:
    repo_hits = [h for h in hits if h.repo == repo]
    if not repo_hits:
        return 0.0
    query_count = len({h.query for h in repo_hits})
    best_rank = min(h.rank for h in repo_hits)
    avg_stars = max(h.search_stars for h in repo_hits)
    description = " ".join(h.description for h in repo_hits)
    title = " ".join(h.title for h in repo_hits)
    topics = " ".join(" ".join(h.topics) for h in repo_hits)
    text = f"{repo} {title} {description} {topics}"

    positive_terms = [
        "awesome",
        "curated",
        "paper",
        "papers",
        "survey",
        "benchmark",
        "dataset",
        "leaderboard",
        "collection",
        "recent",
    ]
    negative_terms = [
        "framework",
        "sdk",
        "starter",
        "template",
        "course",
        "awesome-selfhosted",
        "roadmap",
    ]
    score = 0.0
    score += query_count * 8.0
    score += max(0, 12 - best_rank * 1.5)
    score += min(24.0, math.log10(avg_stars + 10) * 6.0) if avg_stars else 0.0
    score += coarse_text_score(text, positive_terms, negative_terms) * 2.5
    if repo in spec.known_candidates:
        score += 10.0
    return score


def shortlist_direction_repos(spec: DirectionSpec, hits: list[SearchHit]) -> list[str]:
    candidate_repos = {h.repo for h in hits}
    candidate_repos.update(spec.known_candidates)
    candidate_repos.update(MANUAL_SEEDS.get(spec.idx, []))
    scored = [
        (direction_search_score(spec, hits, repo), repo)
        for repo in candidate_repos
    ]
    scored.sort(reverse=True)
    shortlist = [repo for _, repo in scored[:PROVISIONAL_TOP_K]]
    for repo in spec.known_candidates:
        if repo not in shortlist:
            shortlist.append(repo)
    for repo in MANUAL_SEEDS.get(spec.idx, []):
        if repo not in shortlist:
            shortlist.append(repo)
    return shortlist


def fetch_repo_api(client: GitHubClient, repo: str) -> dict[str, Any]:
    return client.get_json(f"https://api.github.com/repos/{repo}")


def fetch_readme_text(client: GitHubClient, repo: str, branch: str) -> tuple[str, str]:
    filenames = ["README.md", "readme.md", "README.MD", "README.rst", "README"]
    for filename in filenames:
        url = f"https://raw.githubusercontent.com/{repo}/{branch}/{filename}"
        resp = client.session.get(url, timeout=40)
        if resp.status_code == 200 and resp.text.strip():
            return resp.text, url
    return "", ""


def summarize_readme(readme_text: str) -> dict[str, Any]:
    lines = readme_text.splitlines()
    lowered = readme_text.lower()
    return {
        "h2": sum(1 for line in lines if re.match(r"^##\s+", line)),
        "h3": sum(1 for line in lines if re.match(r"^###\s+", line)),
        "bullets": sum(1 for line in lines if re.match(r"^\s*[-*]\s+", line)),
        "tables": sum(1 for line in lines if "|" in line and "---" in line),
        "research_terms": sum(
            lowered.count(term)
            for term in [
                "paper",
                "papers",
                "dataset",
                "datasets",
                "benchmark",
                "benchmarks",
                "survey",
                "leaderboard",
                "method",
                "methods",
                "arxiv",
            ]
        ),
        "years": len(re.findall(r"\b20(1\d|2\d)\b", readme_text)),
        "has_toc": "[toc]" in lowered or "table of contents" in lowered,
        "size": len(readme_text),
    }


def build_repo_metrics(client: GitHubClient, repo: str) -> RepoMetrics:
    api = fetch_repo_api(client, repo)
    pushed_at = api.get("pushed_at") or ""
    pushed_date = ""
    pushed_days_ago = 9999
    if pushed_at:
        pushed_dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        pushed_date = pushed_dt.date().isoformat()
        pushed_days_ago = max(0, (utc_now().date() - pushed_dt.date()).days)

    readme_text, readme_url = fetch_readme_text(client, repo, api.get("default_branch") or "main")
    readme_summary = summarize_readme(readme_text)

    return RepoMetrics(
        repo=repo,
        name=api.get("name") or repo.split("/")[-1],
        description=normalize_space(api.get("description") or ""),
        homepage=api.get("homepage") or "",
        stars=int(api.get("stargazers_count") or 0),
        forks=int(api.get("forks_count") or 0),
        open_issues=int(api.get("open_issues_count") or 0),
        archived=bool(api.get("archived")),
        default_branch=api.get("default_branch") or "main",
        html_url=api.get("html_url") or f"https://github.com/{repo}",
        topics=list(api.get("topics") or []),
        pushed_at=pushed_at,
        pushed_date=pushed_date,
        pushed_days_ago=pushed_days_ago,
        readme_url=readme_url,
        readme_headings_h2=readme_summary["h2"],
        readme_headings_h3=readme_summary["h3"],
        readme_bullets=readme_summary["bullets"],
        readme_tables=readme_summary["tables"],
        readme_research_terms=readme_summary["research_terms"],
        readme_years=readme_summary["years"],
        readme_has_toc=readme_summary["has_toc"],
        readme_size=readme_summary["size"],
    )


def direction_is_core(spec: DirectionSpec) -> bool:
    return spec.idx in CORE_DIRECTION_IDS


def score_community(spec: DirectionSpec, stars: int) -> float:
    if stars <= 0:
        return 0.0
    threshold = 500 if direction_is_core(spec) else 100
    if stars >= threshold * 10:
        return 100.0
    if stars >= threshold * 4:
        return 88.0
    if stars >= threshold * 2:
        return 76.0
    if stars >= threshold:
        return 62.0
    if stars >= max(30, threshold // 2):
        return 42.0
    return 24.0


def score_recency(days_ago: int, archived: bool) -> float:
    if archived:
        return 0.0
    if days_ago <= 30:
        return 100.0
    if days_ago <= 90:
        return 86.0
    if days_ago <= 180:
        return 65.0
    if days_ago <= 365:
        return 42.0
    return 18.0


def score_structure(metrics: RepoMetrics) -> float:
    score = 0.0
    score += min(metrics.readme_headings_h2, 14) * 4.0
    score += min(metrics.readme_headings_h3, 18) * 1.5
    score += min(metrics.readme_bullets, 240) / 8.0
    score += min(metrics.readme_tables, 8) * 3.0
    score += min(metrics.readme_years, 16) * 1.0
    if metrics.readme_has_toc:
        score += 8.0
    if metrics.readme_size > 50_000:
        score += 6.0
    return min(score, 100.0)


def score_research(metrics: RepoMetrics) -> float:
    text = " ".join(
        [
            metrics.repo,
            metrics.description,
            " ".join(metrics.topics),
        ]
    ).lower()
    positive_terms = [
        "awesome",
        "curated",
        "paper",
        "papers",
        "survey",
        "dataset",
        "datasets",
        "benchmark",
        "benchmarks",
        "leaderboard",
        "collection",
        "reasoning",
        "generation",
        "multimodal",
    ]
    negative_terms = [
        "framework",
        "sdk",
        "starter",
        "template",
        "toolkit",
        "boilerplate",
        "course",
        "tutorial",
        "interview",
    ]
    score = 18.0
    score += coarse_text_score(text, positive_terms, negative_terms) * 5.0
    score += min(metrics.readme_research_terms, 24) * 2.0
    if "curated list" in text:
        score += 12.0
    if "awesome" in metrics.repo.lower():
        score += 8.0
    if metrics.readme_years >= 4:
        score += 8.0
    return max(0.0, min(score, 100.0))


def score_discovery(spec: DirectionSpec, hits: list[SearchHit], repo: str) -> float:
    repo_hits = [h for h in hits if h.repo == repo]
    if not repo_hits and repo not in spec.known_candidates:
        return 0.0
    query_count = len({h.query for h in repo_hits})
    best_rank = min((h.rank for h in repo_hits), default=10)
    best_search_stars = max((h.search_stars for h in repo_hits), default=0)
    score = 0.0
    score += min(40.0, query_count * 14.0)
    score += max(0.0, 24.0 - (best_rank - 1) * 3.0)
    score += min(20.0, math.log10(best_search_stars + 10) * 5.0) if best_search_stars else 0.0
    if repo in spec.known_candidates:
        score += 16.0
    return min(score, 100.0)


def build_reasoning(spec: DirectionSpec, metrics: RepoMetrics, component_scores: dict[str, float]) -> str:
    reasons: list[str] = []
    if component_scores["research"] >= 80:
        reasons.append("研究导向强")
    elif component_scores["research"] >= 60:
        reasons.append("研究导向合格")
    else:
        reasons.append("研究导向一般")

    if component_scores["structure"] >= 75:
        reasons.append("README 分类清晰")
    elif component_scores["structure"] >= 50:
        reasons.append("README 有可拆分结构")
    else:
        reasons.append("结构一般")

    if metrics.pushed_days_ago <= 90:
        reasons.append("近 90 天有维护")
    elif metrics.pushed_days_ago <= 180:
        reasons.append("近半年仍有更新")
    else:
        reasons.append("维护活跃度偏弱")

    threshold = 500 if direction_is_core(spec) else 100
    if metrics.stars >= threshold:
        reasons.append(f"社区信号达标 ({metrics.stars}★)")
    else:
        reasons.append(f"社区信号偏弱 ({metrics.stars}★)")

    return "；".join(reasons)


def rank_direction(
    spec: DirectionSpec,
    hits: list[SearchHit],
    repo_metrics: dict[str, RepoMetrics],
) -> list[RankedRepo]:
    ranked: list[RankedRepo] = []
    direction_repos = {
        repo for repo in repo_metrics if repo in shortlist_direction_repos(spec, hits)
    }
    for repo in direction_repos:
        metrics = repo_metrics[repo]
        research = score_research(metrics)
        structure = score_structure(metrics)
        recency = score_recency(metrics.pushed_days_ago, metrics.archived)
        community = score_community(spec, metrics.stars)
        discovery = score_discovery(spec, hits, repo)
        total = (
            research * 0.30
            + structure * 0.22
            + recency * 0.20
            + community * 0.18
            + discovery * 0.10
        )

        repo_hits = [h for h in hits if h.repo == repo]
        ranked.append(
            RankedRepo(
                repo=repo,
                direction_id=spec.idx,
                direction_name=spec.name,
                score_total=round(total, 2),
                score_research=round(research, 2),
                score_structure=round(structure, 2),
                score_recency=round(recency, 2),
                score_community=round(community, 2),
                score_discovery=round(discovery, 2),
                stars=metrics.stars,
                pushed_date=metrics.pushed_date,
                description=metrics.description,
                reasoning=build_reasoning(
                    spec,
                    metrics,
                    {
                        "research": research,
                        "structure": structure,
                        "recency": recency,
                        "community": community,
                        "discovery": discovery,
                    },
                ),
                search_queries=sorted({h.query for h in repo_hits}),
                search_ranks=sorted(h.rank for h in repo_hits),
                html_url=metrics.html_url,
            )
        )

    ranked.sort(key=lambda item: (-item.score_total, -item.stars, item.repo.lower()))
    return ranked[:3]


def render_markdown(
    task_path: Path,
    results: dict[int, list[RankedRepo]],
    directions: list[DirectionSpec],
    run_dir: Path,
) -> str:
    created = datetime.now().strftime("%Y-%m-%dT%H:%M")
    task_link = note_link_target(task_path)
    lines: list[str] = [
        "---",
        'title: "Awesome Repo Search Results"',
        f"created: {created}",
        f"updated: {created}",
        "type: awesome_repo_search_results",
        "tags:",
        "  - github-awesome",
        "  - repo-search",
        "  - status/generated",
        "---",
        "",
        "# Awesome 仓库搜索结果",
        "",
        f"> 任务文件: [[{task_link}]]",
        f"> 运行目录: `{run_dir.relative_to(VAULT_ROOT).as_posix()}`",
        f"> 生成时间: {created}",
        "",
        "## 方法说明",
        "",
        "- 自动解析任务文件中的方向、关键词与已知候选。",
        "- 使用 GitHub 仓库搜索页做候选发现，再用 GitHub 仓库元数据核对 stars 与最近 push 日期。",
        "- 按 `研究导向 / 结构清晰 / 近 90 天维护 / 社区信号` 四项加权排序。",
        "- 对每个方向输出 top 3，并给出一个推荐主库。",
        "",
    ]

    for spec in directions:
        ranked = results.get(spec.idx, [])
        lines.append(f"## 方向 {spec.idx}: {spec.name}")
        lines.append("")
        if not ranked:
            lines.append("- 未能稳定检索到满足条件的候选仓库。")
            lines.append("")
            continue

        for i, repo in enumerate(ranked, start=1):
            desc = repo.description or "暂无描述"
            line = (
                f"{i}. [`{repo.repo}`]({repo.html_url}) — ⭐ {repo.stars} — "
                f"{repo.pushed_date or 'Unknown'} — {desc}"
            )
            lines.append(line)
        lines.append(f"推荐主库: `{ranked[0].repo}`")
        lines.append(f"理由: {ranked[0].reasoning}。{spec.goal}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task-file",
        type=Path,
        default=DEFAULT_TASK_FILE,
        help="Path to the awesome repo search task markdown file.",
    )
    args = parser.parse_args()

    directions = parse_task_file(args.task_file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = RUNS_DIR / timestamp
    ensure_dir(run_dir)

    client = GitHubClient()

    direction_hits: dict[int, list[SearchHit]] = {}
    search_dump: dict[str, Any] = {}
    shortlist_union: set[str] = set()

    for spec in directions:
        hits = search_candidates(client, spec, SEARCH_KEYWORD_LIMIT)
        direction_hits[spec.idx] = hits
        shortlist = shortlist_direction_repos(spec, hits)
        shortlist_union.update(shortlist)
        search_dump[str(spec.idx)] = {
            "direction": spec.name,
            "keywords_used": spec.keywords[:SEARCH_KEYWORD_LIMIT],
            "known_candidates": spec.known_candidates,
            "shortlist": shortlist,
            "hits": [asdict(hit) for hit in hits],
        }
        time.sleep(0.4)

    (run_dir / "search_hits.json").write_text(
        json.dumps(search_dump, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    repo_metrics: dict[str, RepoMetrics] = {}
    with cf.ThreadPoolExecutor(max_workers=MAX_FETCH_WORKERS) as executor:
        future_map = {
            executor.submit(build_repo_metrics, client, repo): repo
            for repo in sorted(shortlist_union)
        }
        for future in cf.as_completed(future_map):
            repo = future_map[future]
            try:
                repo_metrics[repo] = future.result()
            except Exception as exc:
                print(f"[warn] failed to fetch repo metrics for {repo}: {exc}")

    (run_dir / "repo_metrics.json").write_text(
        json.dumps(
            {repo: asdict(metrics) for repo, metrics in sorted(repo_metrics.items())},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    ranked_results: dict[int, list[RankedRepo]] = {}
    ranked_dump: dict[str, Any] = {}
    for spec in directions:
        ranked = rank_direction(spec, direction_hits.get(spec.idx, []), repo_metrics)
        ranked_results[spec.idx] = ranked
        ranked_dump[str(spec.idx)] = {
            "direction": spec.name,
            "results": [asdict(item) for item in ranked],
        }

    (run_dir / "ranked_results.json").write_text(
        json.dumps(ranked_dump, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    markdown = render_markdown(args.task_file, ranked_results, directions, run_dir)
    output_path = run_dir / "awesome_repo_search_results.md"
    output_path.write_text(markdown, encoding="utf-8")
    latest_path = ROOT / "awesome_repo_search_results.latest.md"
    latest_path.write_text(markdown, encoding="utf-8")

    print(f"Generated: {output_path}")
    print(f"Updated latest: {latest_path}")


if __name__ == "__main__":
    main()
