---
name: papers-download-from-list
status: active-local-download
description: Uses colocated paper download tools to download, verify, and repair local PDFs according to triage logs (e.g., ICLR_2026.txt) so that `obsidian-vault/paperPDFs/` stays complete and deduplicated. Use when you have a curated candidate list under `obsidian-vault/analysis/` and want all corresponding PDFs downloaded/checked before analysis or index rebuild.
---

# Paper PDF Download and Repair Tools

## What this skill does

Connects **online triage lists** to **local PDFs** by orchestrating utilities in the colocated paper download tools directory:

- read candidate papers from `obsidian-vault/analysis/*.txt` (for example `ICLR_2026.txt`);
- download missing PDFs into `obsidian-vault/paperPDFs/...`;
- repair common download errors (bad links, wrong version downloads);
- deduplicate, verify download integrity, and mark entries that remain missing for manual follow-up.

In the pipeline

**papers-collect-from-web → papers-download-from-list → formal analysis chain (`scripts/run_local_paper_analysis.py`) → papers-build-index → papers-query-knowledge-base / research-brainstorm-from-kb**,

this skill is responsible for the **Download + Repair** stage.

## Directory and scripts

Script directory (relative to this skill directory):

- `paper_download_tools/check_paper_downloads.py`
- `paper_download_tools/check_pdfs_against_log.py`
- `paper_download_tools/download_wait_papers.py`
- `paper_download_tools/redownload_correct_pdfs.py`
- `paper_download_tools/fix_wrong_downloads_from_log.py`
- `paper_download_tools/mark_missing_wait.py`
- `paper_download_tools/dedupe_paperpdfs.py`

## Recommended workflow

Typical execution order (from candidate list to clean PDF set):

1. **Prerequisite: triage list exists**
   - `obsidian-vault/analysis/*.txt` triage file with schema:
     - `state | title | venue&time | paper link | project/github link | category`

2. **Batch download `Wait` entries**
   - Example command:
   - ```bash
     python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/download_wait_papers.py" \
       --log "obsidian-vault/analysis/ICLR_2026.txt" \
       --out-root "obsidian-vault/paperPDFs"
     ```
   - Behavior:
     - reads rows with `state=Wait`;
     - infers/creates target subdirectories from `category` and `venue&time`;
     - downloads PDFs into corresponding `obsidian-vault/paperPDFs/...` paths;
     - automatically compresses oversized PDFs (>20MB) using Ghostscript `/ebook` (fallback `/screen`);
     - updates log state to `Downloaded` on success.

3. **Check missing and broken files**
   - ```bash
     python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/check_paper_downloads.py" \
       --log "obsidian-vault/analysis/ICLR_2026.txt" \
       --pdf-root "obsidian-vault/paperPDFs"
     ```
   - ```bash
     python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/check_pdfs_against_log.py" \
       --log "obsidian-vault/analysis/ICLR_2026.txt" \
       --pdf-root "obsidian-vault/paperPDFs"
     ```
   - Behavior:
     - reports rows that have links in log but no local PDF;
     - reports downloaded PDFs that are suspiciously small/corrupt/unreadable for redownload.

4. **Redownload wrong or mismatched PDFs**
   - ```bash
     python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/fix_wrong_downloads_from_log.py" \
       --log "obsidian-vault/analysis/ICLR_2026.txt" \
       --pdf-root "obsidian-vault/paperPDFs"
     ```
   - ```bash
     python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/redownload_correct_pdfs.py" \
       --log "obsidian-vault/analysis/ICLR_2026.txt" \
       --pdf-root "obsidian-vault/paperPDFs"
     ```
   - Behavior:
     - redownloads problematic items using original/fixed links from log;
     - updates log state to mark repaired entries.

5. **Mark long-term missing entries to avoid repeated retries**
   - ```bash
     python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/mark_missing_wait.py" \
       --log "obsidian-vault/analysis/ICLR_2026.txt"
     ```
   - Behavior:
     - for entries that still fail after repeated attempts, update state to `Missing` and keep them in log for later manual addition/retry.

6. **Deduplicate and clean up**
   - ```bash
     python3 ".claude/skills/papers-download-from-list/scripts/paper_download_tools/dedupe_paperpdfs.py" \
       --root "obsidian-vault/paperPDFs"
     ```
   - Behavior:
     - finds duplicate downloads of the same paper (by hash/filename/log info);
     - merges/keeps one PDF copy and standardizes references in log.

## When to use vs other skills

- **Collect**: use `papers-collect-from-web` to extract candidates and links from conference/topic pages.
- **Download**: use this `papers-download-from-list` skill to convert triage links into local `obsidian-vault/paperPDFs/` files.
- **Analyze**: use the formal local analysis chain (`scripts/run_local_paper_analysis.py`) to parse PDFs/MinerU outputs into structured `obsidian-vault/analysis/*.md`.
- **Classify / Index**: use `papers-build-index` to rebuild `obsidian-vault/index` indexes.
- **Integrate / Query**: use `papers-query-knowledge-base` to retrieve, compare, and cite across the full KB.
- **Reflect / Ideate**: use `research-brainstorm-from-kb` to distill outputs into research ideas under `obsidian-vault/ideas/`.

## Triggers (examples)

- "Download all PDFs from this `ICLR_2026.txt` list."
- "Check which candidate papers failed to download and repair wrong downloads."
- "Clean duplicate/broken PDFs under `obsidian-vault/paperPDFs/`, then continue analysis."
