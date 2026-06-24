---
name: papers-collect-from-web
status: active-local-collect
description: "Collects paper candidates from non-GitHub web URLs — conference sites, lab homepages, proceedings pages, Google Scholar results, blog posts with paper lists, etc. Fetches and stores pages locally, then appends rows to `obsidian-vault/paper_list.csv`. Use when the user provides web URLs (not GitHub repos) + keyword constraints + venue/year and wants candidates added to the unified log. For GitHub repos, use `papers-collect-from-github-repo` instead."
---

# Paper Collector (Online / Web)

Fetch web pages to local storage, extract paper candidates, and append them to `obsidian-vault/paper_list.csv`.

Use this skill for **non-GitHub web sources**: conference sites, lab homepages, proceedings pages (ACL Anthology, IEEE Xplore, etc.), Google Scholar results, blog posts with paper lists, etc.

For **GitHub repositories** (awesome lists, survey repos, lab paper repos, conference paper repos), use `papers-collect-from-github-repo` instead — it handles raw Markdown and multi-file repo structures better.

## Scope

- **Input**: one or more web URLs + include/exclude keyword constraints + target venue/year label.
- **Output**:
  - saved source pages under `paperSources/<run_id>/...`
  - new rows appended to `obsidian-vault/paper_list.csv`

## Output format (CSV columns, same as paper_list.csv)

```
state,importance,paper_title,venue,project_link_or_github_link,paper_link,sort,pdf_path
```

Defaults:
- **state**: `Wait` (newly collected) or `Skip` (manually marked skip)
- **importance**: empty (user fills later)
- **venue**: user-provided label such as `ICLR 2026`
- **sort**: leave blank if unknown; user can fill per item later
- **pdf_path**: empty (filled later by `papers-download-from-list`)

> State convention is defined in `STATE_CONVENTION.md`: main pipeline `Wait → Downloaded → checked`; out-of-band states `Skip` / `Missing`.

## Workflow

1. Ask user for:
   - URLs (one or many)
   - include keywords (optional) and exclude keywords (optional)
   - venue/time label (for example `ICLR 2026`)
   - whether to overwrite or append if rows already exist for this venue
2. Run collector script (preferred default):
   - `python3 ".claude/skills/papers-collect-from-web/scripts/paper_collector_online/collect_from_urls.py" --venue-time "ICLR 2026" --urls "<URL1>" "<URL2>" --include "motion;diffusion" --exclude "workshop;dataset" --append`
3. Verify generated rows:
   - columns present and in correct order
   - dedup applied by normalized paper link against existing `paper_list.csv`
   - links are well-formed (no surrounding punctuation)
4. If extraction quality is poor for a URL:
   - rerun with tighter keywords, or
   - run per-source URLs separately, or
   - manually provide a short snippet list and extend script patterns only if needed.

## Rules and heuristics (defaults)

- **Fetch**: store HTML as-is (no JS rendering).
- **Dedup**: by normalized `paper link` (for example normalize arXiv pdf/abs).
- **Project link**: best-effort heuristic; may be empty.
- **Keywords**: match against title + nearby anchor text (case-insensitive).
- **Safety**: respect reasonable timeouts; do not brute-force crawl.

## Notes

- This skill intentionally does **not** download PDFs. It only appends candidate rows to `paper_list.csv` for later processing.
- Output format is unified with `papers-collect-from-github-repo` — both write to `paper_list.csv`.
- Repository root is the folder containing `obsidian-vault/analysis/` and `obsidian-vault/paperPDFs/`.

## Relationship to papers-collect-from-github-repo

- **This skill** (`papers-collect-from-web`): optimized for arbitrary web pages — fetches rendered HTML, uses link-based extraction, stores source HTML locally
- **`papers-collect-from-github-repo`**: optimized for GitHub repos — fetches raw Markdown, understands repo structure, handles multi-file layouts, writes one-off parsers
