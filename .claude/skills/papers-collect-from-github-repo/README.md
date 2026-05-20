# papers-collect-from-github-repo

## Overview

Collects paper candidates from **any GitHub repository** — awesome lists, survey companion repos, lab paper lists, conference accepted-paper repos, benchmark leaderboards, or any repo with a structured paper list — and outputs rows aligned with `obsidian-vault/paper_list.csv`.

Because each repo uses a different structure (Markdown tables, bullet lists, mixed HTML, multi-file docs, etc.), this skill does **not** ship fixed parsing scripts. Instead, the agent analyzes each repo's format on the fly and writes a one-off parser.

## Supported source types

- Awesome / curated lists (e.g. `Foruck/Awesome-Human-Motion`)
- Survey companion repos (e.g. `ChenHsing/Awesome-Video-Diffusion-Models`)
- Lab / group publication pages on GitHub
- Conference accepted paper lists
- Benchmark / leaderboard repos with paper references
- Any repo with structured paper entries

## Output format (CSV columns)

```
state,importance,paper_title,venue,project_link_or_github_link,paper_link,sort,pdf_path
```

- `state` defaults to `Wait`
- `importance` and `pdf_path` are left blank during collection
- `sort` inherits section headings from the source, using `_` separators (for example `Motion_Generation`)
- See `obsidian-vault/paper_list.csv` for reference examples

## Typical usage

```
1. "Collect papers from https://github.com/Foruck/Awesome-Human-Motion, only motion generation related."
2. "Focus on Motion Customization, Long Video / Film Generation, and Video Generation with 3D/Physical Prior under https://github.com/showlab/Awesome-Video-Diffusion?tab=readme-ov-file#motion-customization; generate a paper list and save to 'obsidian-vault/paper_list.csv'."
3. "Collect papers from https://github.com/ChenHsing/Awesome-Video-Diffusion-Models, focus on controllable generation."
4. "Extract ICLR 2026 accepted papers from https://github.com/xxx/iclr2026-papers."
```

The agent will:
1. Fetch the raw README (or specified doc files)
2. Analyze its format
3. Write a one-off parser
4. Append new candidates to `paper_list.csv`

## Processing artifacts (optional)

One-off parsing scripts and raw source snapshots may be saved under:

```
obsidian-vault/analysis/processing/github_awesome/<repo_slug>/
```

These are for debugging reference only and are not required for the workflow.

## Relationship to papers-collect-from-web

- **This skill** (`papers-collect-from-github-repo`): optimized for GitHub repos — fetches raw Markdown, understands repo structure, handles multi-file layouts
- **`papers-collect-from-web`**: optimized for arbitrary web pages (conference sites, lab homepages, Google Scholar results, etc.) — fetches rendered HTML, uses link-based extraction
