---
name: papers-collect-from-github-repo
status: active-local-collect
description: "Collects paper candidates from any GitHub repository README or docs — awesome lists, survey companion repos, lab paper lists, conference accepted-paper repos, benchmark leaderboards, etc. Agent fetches the README (or specified doc), analyzes its format, writes a one-off parser, and outputs rows aligned with paper_list.csv. No pre-built scripts — agent adapts to each repo's format on the fly."
---

# Papers Collect From GitHub Repo

## Purpose

Extract paper candidates from **any GitHub repository** and output rows aligned with `obsidian-vault/paper_list.csv`.

Supported repo types (non-exhaustive):

| Type | Example |
|------|---------|
| Awesome / curated list | `Foruck/Awesome-Human-Motion` |
| Survey companion repo | `ChenHsing/Awesome-Video-Diffusion-Models` (CSUR) |
| Lab / group paper list | `showlab/showlab.github.io` |
| Conference accepted papers | `ICLR/ICLR-2026-accepted-papers` |
| Benchmark / leaderboard repo | `open-compass/opencompass` |
| Topic-specific collection | `soraproducer/Awesome-Human-Interaction-Motion-Generation` |
| Any repo with a structured paper list in README or docs | — |

Because repo formats vary widely (Markdown tables, bullet lists, mixed HTML, nested docs, multiple files, etc.), this skill **does not include fixed scripts**. The agent writes one-off parsing logic for each target.

## Input

User provides:
- **GitHub repo URL**: e.g. `https://github.com/Foruck/Awesome-Human-Motion`
- **target file** (optional): defaults to `README.md`; can be a specific path like `docs/papers.md` or a directory to scan
- **include/exclude keywords** (optional): e.g. include `motion generation`, exclude `survey`
- **target category** (optional): e.g. `Motion_Generation_Text_Speech_Music_Driven`
- **venue/year hint** (optional): e.g. `CVPR 2025` — used as default when venue cannot be parsed

## Output Format

Output must align with the column format of `obsidian-vault/paper_list.csv`:

```
state,importance,paper_title,venue,project_link_or_github_link,paper_link,sort,pdf_path
```

Field notes:

| Column | Initial default | Description |
|----|-------------|------|
| state | `Wait` | Later can be changed manually to `Skip`, or remain `Wait` for download |
| importance | empty | Later manually labeled as S/A/B/C |
| paper_title | parsed from repo | paper title |
| venue | parsed from repo, fallback `Unknown` | e.g., `CVPR 2025`, `ICLR 2026`; if only on open platforms, use `arXiv YYYY` |
| project_link_or_github_link | project page or GitHub link | prefer project page; if confirmed no open source, use `N/A` |
| paper_link | arXiv / OpenReview link | prefer arXiv abs link |
| sort | section/category heading in source | join words with `_`, e.g. `Motion_Generation` |
| pdf_path | empty | filled later by `papers-download-from-list` |

See `obsidian-vault/paper_list.csv` in the repository for examples.

## Workflow

### 1. Fetch Source Content

- Determine what to fetch:
  - Single README: `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/README.md`
  - Specific file: user-specified path within the repo
  - Multiple files: if repo organizes papers across multiple `.md` files (e.g. `papers/2025.md`, `papers/2026.md`), fetch all relevant files
- Optionally save raw content to `obsidian-vault/analysis/processing/github_awesome/<repo_slug>/` for debugging
  - Note: the `github_awesome` directory name is kept for backward compatibility; it stores artifacts from all GitHub repo sources, not just awesome lists

### 2. Analyze Format

Agent reads the content and determines structure:
- Markdown table, bullet list, nested sections, or mixed format?
- Single file or multi-file organization?
- Where paper titles appear and how links are organized?
- Whether venue metadata is inline, in section headings, or in separate columns?
- Whether the repo uses badges, emoji markers, or other conventions?

### 3. Write One-Off Parser

Based on the structure analysis, the agent writes a one-off Python script (or processes directly in conversation) to extract paper information.

Script requirements:
- Output CSV with the same column order as `paper_list.csv`
- Handle common link patterns: arXiv abs/pdf, OpenReview, GitHub project page, conference proceedings (ACL Anthology, IEEE Xplore, etc.)
- Parse venues from text patterns like `(CVPR 2025)` / `[ICLR 2026]` / section headings like `## NeurIPS 2025`
- Deduplicate repeated appearances of the same paper

### 4. Filter and Deduplicate

- Apply user include/exclude keyword filtering
- Deduplicate against existing `paper_list.csv` entries (fuzzy match by `paper_title`)
- Report number of newly added candidate rows

### 5. Append to paper_list.csv

- Append new rows to `obsidian-vault/paper_list.csv`
- Do not modify existing rows
- Report to user: number of new candidates and source sections

### 6. Completeness Check and Suggestion

After append, scan newly added rows for missing fields:

| Missing field | Detection condition | Completion method | Fallback |
|---------|---------|---------|------------|
| venue | empty or `Unknown` | lookup by paper_link via arXiv metadata / Semantic Scholar API | if unpublished at venue but public: `arXiv YYYY` (e.g., `arXiv 2025`) |
| paper_link | empty | search arXiv / Google Scholar by paper_title | if not found: keep empty |
| project_link_or_github_link | empty | search GitHub / Papers With Code by paper_title | if confirmed no open source: `N/A` |
| sort | empty | infer from source section heading or ask user | keep empty for manual fill |

Then report and suggest:

> "Added N new candidates: X missing venue, Y missing paper_link, Z missing project_link. Do you want multi-source completion? (complete all / venue only / links only / skip)"

After user confirmation:
- **complete all**: use arXiv API, Semantic Scholar, Google Scholar, Papers With Code in sequence
- **specific fields only**: search only matching sources
- **skip**: keep current state for later manual handling

Constraints for completion:
- Keep at least 3 seconds between searches (respect API rate limits)
- Match search results to `paper_title`; only auto-fill when similarity > 0.8, otherwise mark `[needs confirmation]`
- Write completion results back to matching rows in `paper_list.csv`

## Environment Detection

If Python scripts are needed, follow Environment Detection rules from `code-context-paper-retrieval`:
- prioritize environment detection from codebase `environment/environment.yml` / `environment/requirements.txt` etc.
- if unresolved, proactively ask user

## Constraints

- No prebuilt parser scripts; each repo format is adapted live
- One-off scripts may be saved to `obsidian-vault/analysis/processing/github_awesome/<repo_slug>/parse_<timestamp>.py` for future reference
- Do not auto-download PDFs (that is `papers-download-from-list`)
- Do not auto-generate analysis notes; that belongs to the formal analysis
  chain (`scripts/run_local_paper_analysis.py`) or the batch analysis manager.

## Typical Usage

> "Collect papers from https://github.com/Foruck/Awesome-Human-Motion, only motion generation related"

> "Organize papers from https://github.com/ChenHsing/Awesome-Video-Diffusion-Models into paper_list.csv, focus on controllable generation sections"

> "Collect ICLR 2026 accepted papers from https://github.com/xxx/iclr2026-papers"

> "Extract papers from https://github.com/xxx/lab-publications, filter by 2025-2026"
