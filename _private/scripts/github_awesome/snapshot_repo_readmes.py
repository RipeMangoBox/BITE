#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT_MD = ROOT / "awesome_repo_search_results.final.md"
DEFAULT_SNAPSHOT_ROOT = ROOT / "readme_snapshots"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
)
REPO_PATTERN = re.compile(r"(?<![\w./-])([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(?![\w./-])")


def find_vault_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError(f"Could not locate vault root from {start}")


VAULT_ROOT = find_vault_root(ROOT)


@dataclass
class SnapshotRecord:
    repo: str
    repo_url: str
    description: str
    stars: int
    default_branch: str
    repo_pushed_at: str
    repo_updated_at: str
    snapshot_fetched_at: str
    readme_source_url: str
    readme_source_last_modified: str
    readme_source_etag: str
    readme_sha256: str
    snapshot_dir: str
    snapshot_path: str
    metadata_path: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_star_count(text: str) -> int:
    text = text.strip().lower().replace(",", "")
    if not text:
        return 0
    text = text.removesuffix("stars").strip()
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


def extract_repo_candidates(text: str) -> list[str]:
    seen: set[str] = set()
    repos: list[str] = []
    for repo in REPO_PATTERN.findall(text):
        if repo in seen:
            continue
        seen.add(repo)
        repos.append(repo)
    return repos


def repo_dir_name(repo: str) -> str:
    owner, name = repo.split("/", 1)
    return f"{owner}__{name}"


def fetch_commit_feed_updated(session: requests.Session, repo: str, branch: str) -> str:
    feed_url = f"https://github.com/{repo}/commits/{branch}.atom"
    resp = session.get(feed_url, timeout=40)
    if resp.status_code != 200:
        return ""
    match = re.search(r"<updated>([^<]+)</updated>", resp.text)
    return match.group(1) if match else ""


def fetch_repo_info_from_html(session: requests.Session, repo: str) -> dict[str, Any] | None:
    page_url = f"https://github.com/{repo}"
    resp = session.get(page_url, timeout=40)
    if resp.status_code != 200:
        return None

    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    default_branch_match = re.search(r'"defaultBranch":"([^"]+)"', html)
    default_branch = default_branch_match.group(1) if default_branch_match else "HEAD"

    description = ""
    for attrs in ({"property": "og:description"}, {"name": "description"}):
        meta = soup.find("meta", attrs=attrs)
        content = normalize_space(meta.get("content", "")) if meta else ""
        if content:
            suffix = f" - {repo}"
            if content.endswith(suffix):
                content = content[: -len(suffix)].rstrip()
            description = content
            break

    stars = 0
    for link in soup.select('a[href$="/stargazers"]'):
        text = normalize_space(link.get_text(" ", strip=True))
        stars = parse_star_count(text)
        if stars:
            break

    pushed_at = fetch_commit_feed_updated(session, repo, default_branch)

    return {
        "html_url": page_url,
        "description": description,
        "stargazers_count": stars,
        "default_branch": default_branch,
        "pushed_at": pushed_at,
        "updated_at": pushed_at,
    }


def fetch_repo_info(session: requests.Session, repo: str) -> dict[str, Any] | None:
    resp = session.get(f"https://api.github.com/repos/{repo}", timeout=40)
    if resp.status_code == 200:
        return resp.json()
    return fetch_repo_info_from_html(session, repo)


def fetch_readme(session: requests.Session, repo: str, branch: str) -> tuple[str, str, requests.Response | None]:
    candidates = ["README.md", "readme.md", "README.MD", "README.rst", "README"]
    branches: list[str] = []
    for candidate_branch in (branch, "HEAD"):
        if candidate_branch and candidate_branch not in branches:
            branches.append(candidate_branch)
    for candidate_branch in branches:
        for name in candidates:
            url = f"https://raw.githubusercontent.com/{repo}/{candidate_branch}/{name}"
            resp = session.get(url, timeout=40)
            if resp.status_code == 200 and resp.text.strip():
                return resp.text, url, resp
    return "", "", None


def markdown_linkify(text: str, valid_repos: set[str]) -> str:
    output = text
    for repo in sorted(valid_repos, key=len, reverse=True):
        output = output.replace(f"`{repo}`", f"[`{repo}`](https://github.com/{repo})")
    return output


def build_snapshot_markdown(record: SnapshotRecord, readme_text: str) -> str:
    lines = [
        "---",
        f'title: {yaml_quote(f"README Snapshot - {record.repo}")}',
        f"created: {record.snapshot_fetched_at}",
        f"updated: {record.snapshot_fetched_at}",
        "type: github_awesome_readme_snapshot",
        "tags:",
        "  - github-awesome",
        "  - readme-snapshot",
        "  - status/generated",
        f"repo: {yaml_quote(record.repo)}",
        f"repo_url: {yaml_quote(record.repo_url)}",
        f"default_branch: {yaml_quote(record.default_branch)}",
        f"repo_pushed_at: {yaml_quote(record.repo_pushed_at)}",
        f"repo_updated_at: {yaml_quote(record.repo_updated_at)}",
        f"snapshot_fetched_at: {yaml_quote(record.snapshot_fetched_at)}",
        f"readme_source_url: {yaml_quote(record.readme_source_url)}",
        f"readme_source_last_modified: {yaml_quote(record.readme_source_last_modified)}",
        f"readme_source_etag: {yaml_quote(record.readme_source_etag)}",
        f"readme_sha256: {yaml_quote(record.readme_sha256)}",
        "---",
        "",
        f"# {record.repo} README Snapshot",
        "",
        "> [!abstract] Snapshot Metadata",
        f"> Repo: [`{record.repo}`]({record.repo_url})",
        f"> Repo pushed at: `{record.repo_pushed_at or 'Unknown'}`",
        f"> Snapshot fetched at: `{record.snapshot_fetched_at}`",
        f"> README source: [raw README]({record.readme_source_url})",
    ]
    if record.readme_source_last_modified:
        lines.append(f"> README last modified: `{record.readme_source_last_modified}`")
    if record.readme_source_etag:
        lines.append(f"> README etag: `{record.readme_source_etag}`")
    lines.extend(
        [
            f"> README sha256: `{record.readme_sha256}`",
            "",
            "## Upstream README",
            "",
            readme_text.rstrip(),
            "",
        ]
    )
    return "\n".join(lines)


def build_index_markdown(
    source_md: Path,
    snapshot_root: Path,
    records: list[SnapshotRecord],
) -> str:
    created = datetime.now().strftime("%Y-%m-%dT%H:%M")
    lines = [
        "---",
        'title: "GitHub Awesome README Snapshots"',
        f"created: {created}",
        f"updated: {created}",
        "type: github_awesome_readme_snapshots",
        "tags:",
        "  - github-awesome",
        "  - readme-snapshot",
        "  - status/generated",
        "---",
        "",
        "# GitHub Awesome README Snapshots",
        "",
        f"> 来源结果笔记: [[{note_link_target(source_md)}]]",
        f"> 快照清单: `{(snapshot_root / 'manifest.json').relative_to(VAULT_ROOT).as_posix()}`",
        f"> 生成时间: {created}",
        "",
        "## 说明",
        "",
        "- 每个仓库一个固定目录，便于后续增量检查。",
        "- `repo_pushed_at` 表示 GitHub 仓库最近 push 时间，可用于判断快照是否过期。",
        "- `snapshot_fetched_at` 表示本地快照抓取时间。",
        "- `metadata.json` 保存后续更新判断所需的全部字段。",
        "",
        "## 快照索引",
        "",
        "| Repo | README Snapshot | Repo Pushed | Snapshot Fetched |",
        "|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            "| "
            f"[`{record.repo}`]({record.repo_url}) | "
            f"[[{note_link_target(Path(record.snapshot_path))}|README]] | "
            f"`{record.repo_pushed_at}` | "
            f"`{record.snapshot_fetched_at}` |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-md", type=Path, default=DEFAULT_INPUT_MD)
    parser.add_argument("--snapshot-root", type=Path, default=DEFAULT_SNAPSHOT_ROOT)
    parser.add_argument("--update-md-links", action="store_true")
    args = parser.parse_args()

    input_md = args.input_md.resolve()
    snapshot_root = args.snapshot_root.resolve()
    ensure_dir(snapshot_root)

    text = input_md.read_text(encoding="utf-8")
    repo_candidates = extract_repo_candidates(text)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github+json",
        }
    )

    valid_repos: list[str] = []
    records: list[SnapshotRecord] = []
    fetched_at = utc_now_iso()

    for repo in repo_candidates:
        repo_info = fetch_repo_info(session, repo)
        if not repo_info:
            continue

        valid_repos.append(repo)
        branch = repo_info.get("default_branch") or "main"
        readme_text, readme_url, readme_resp = fetch_readme(session, repo, branch)
        if not readme_text:
            continue

        repo_dir = snapshot_root / repo_dir_name(repo)
        ensure_dir(repo_dir)

        readme_path = repo_dir / "README.snapshot.md"
        metadata_path = repo_dir / "metadata.json"

        record = SnapshotRecord(
            repo=repo,
            repo_url=repo_info.get("html_url") or f"https://github.com/{repo}",
            description=repo_info.get("description") or "",
            stars=int(repo_info.get("stargazers_count") or 0),
            default_branch=branch,
            repo_pushed_at=repo_info.get("pushed_at") or "",
            repo_updated_at=repo_info.get("updated_at") or "",
            snapshot_fetched_at=fetched_at,
            readme_source_url=readme_url,
            readme_source_last_modified=(readme_resp.headers.get("Last-Modified") if readme_resp else "") or "",
            readme_source_etag=(readme_resp.headers.get("ETag") if readme_resp else "") or "",
            readme_sha256=hashlib.sha256(readme_text.encode("utf-8")).hexdigest(),
            snapshot_dir=str(repo_dir),
            snapshot_path=str(readme_path),
            metadata_path=str(metadata_path),
        )

        readme_path.write_text(
            build_snapshot_markdown(record, readme_text),
            encoding="utf-8",
        )
        metadata_path.write_text(
            json.dumps(asdict(record), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        records.append(record)

    records.sort(key=lambda item: item.repo.lower())

    manifest = {
        "source_md": str(input_md),
        "snapshot_root": str(snapshot_root),
        "generated_at": fetched_at,
        "repo_count": len(records),
        "repos": [asdict(record) for record in records],
    }
    (snapshot_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (snapshot_root / "index.md").write_text(
        build_index_markdown(input_md, snapshot_root, records),
        encoding="utf-8",
    )

    if args.update_md_links and valid_repos:
        linked_text = markdown_linkify(text, set(valid_repos))
        input_md.write_text(linked_text, encoding="utf-8")

    print(f"snapshot_root={snapshot_root}")
    print(f"repo_count={len(records)}")
    print(f"index_md={snapshot_root / 'index.md'}")
    print(f"manifest_json={snapshot_root / 'manifest.json'}")


if __name__ == "__main__":
    main()
