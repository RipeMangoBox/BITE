---
name: papers-download-from-list
status: active-local-download
description: Uses colocated paper download tools to download, verify, and repair local PDFs from `obsidian-vault/paper_list.csv` rows so that `obsidian-vault/paperPDFs/` stays complete and deduplicated. Use when candidate rows are in `state=Wait` and should become `Downloaded` before the formal analysis chain.
---

# Paper PDF Download and Repair Tools

## What this skill does

Connects `obsidian-vault/paper_list.csv` candidate rows to local PDFs by
orchestrating utilities in the colocated paper download tools directory:

- read candidate papers from `obsidian-vault/paper_list.csv`;
- download missing PDFs into `obsidian-vault/paperPDFs/...`;
- repair common download errors (bad links, wrong version downloads);
- deduplicate, verify download integrity, and mark entries that remain missing for manual follow-up.

In the pipeline

**papers-collect-from-web → papers-download-from-list → formal analysis chain (`scripts/run_local_paper_analysis.py`) → papers-build-index → papers-query-knowledge-base / research-brainstorm-from-kb**,

this skill is responsible for the **Download + Repair** stage.

## Directory and scripts

Script directory (relative to this skill directory):

- `paper_download_tools/check_pdfs_against_log.py`
- `paper_download_tools/download_wait_papers.py`
- `paper_download_tools/dedupe_paperpdfs.py`
- `paper_download_tools/search_download_by_info.py`

## Recommended workflow

Typical execution order (from candidate list to clean PDF set):

1. **Prerequisite: queue exists**
   - Source: `obsidian-vault/paper_list.csv` with `state=Wait` rows.
   - Required columns:
     `state,importance,paper_title,venue,project_link_or_github_link,paper_link,sort,pdf_path`

2. **Batch download `Wait` entries**
   - Example command:
   - ```bash
     python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/download_wait_papers.py" \
       --source "obsidian-vault/paper_list.csv" \
       --out-root "obsidian-vault/paperPDFs"
     ```
   - Behavior:
     - reads rows with `state=Wait`;
     - infers supported PDF URLs from direct `.pdf`, arXiv, and OpenReview links;
     - downloads PDFs into corresponding `obsidian-vault/paperPDFs/...` paths;
     - preflights the local file before success;
     - updates the row to `Downloaded` on success and records `pdf_path`;
     - leaves unsupported or failed rows as `Wait` for manual repair.

3. **Check missing and broken files**
   - ```bash
     python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/check_pdfs_against_log.py"
     ```
   - Behavior:
     - verifies `pdf_path` references in `paper_list.csv`;
     - moves rows with missing PDFs back to `Wait`;
     - promotes rows with found PDFs only to `Downloaded`, never to `analysised` or `checked`.

4. **Deduplicate and clean up**
   - ```bash
     python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/dedupe_paperpdfs.py" \
       --root "obsidian-vault/paperPDFs"
     ```
   - Behavior:
     - finds duplicate downloads of the same paper (by hash/filename/log info);
     - merges/keeps one PDF copy and standardizes references in log.

5. **Manual-spec fallback**
   - For a small manually curated JSON spec list, use:
   - ```bash
     python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/search_download_by_info.py" \
       --spec-file "<paper-specs.json>" \
       --log-path "obsidian-vault/paper_list.csv"
     ```
   - This fallback also writes successful rows as `Downloaded`.

## When to use vs other skills

- **Collect**: use `papers-collect-from-web` to extract candidates and links from conference/topic pages.
- **Download**: use this `papers-download-from-list` skill to convert `paper_list.csv` candidate links into local `obsidian-vault/paperPDFs/` files.
- **Analyze**: use the formal local analysis chain (`scripts/run_local_paper_analysis.py`) to parse PDFs/MinerU outputs into structured `obsidian-vault/analysis/*.md`.
- **Classify / Index**: use `papers-build-index` to rebuild `obsidian-vault/index` indexes.
- **Integrate / Query**: use `papers-query-knowledge-base` to retrieve, compare, and cite across the full KB.
- **Reflect / Ideate**: use `research-brainstorm-from-kb` to distill outputs into research ideas under `obsidian-vault/ideas/`.

## Triggers (examples)

- "Download all `Wait` PDFs from `obsidian-vault/paper_list.csv`."
- "Check which candidate papers failed to download and repair wrong downloads."
- "Clean duplicate/broken PDFs under `obsidian-vault/paperPDFs/`, then continue analysis."
