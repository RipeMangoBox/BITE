---
name: papers-batch-analyze
description: Batch-analyzes papers from a user-provided CSV or `obsidian-vault/paper_list.csv` by splitting the list into safe per-batch CSVs, spawning parallel worker agents, writing analysis notes under `obsidian-vault/analysis/`, and refreshing `obsidian-vault/index/` after all completed batches. Use when the user asks to analyze many papers from `paper_list.csv` or run a local batch paper analysis workflow.
---

# Batch Paper Analysis

Use this skill to manage batch analysis from `paper_list.csv`. The managing
agent coordinates batching and workers; the splitter script only creates batch
CSV files and a manifest. It must not run LLM analysis.

## Inputs

- Default source: `obsidian-vault/paper_list.csv`
- User override: any user-provided CSV path
- Default batch size: `25`
- Default parallelism: `4` worker agents processing `4` batches at a time
- Output batches: `obsidian-vault/batches/<run_id>/batch_0001.csv`, etc.

Expected CSV columns:

```csv
state,importance,paper_title,venue,project_link_or_github_link,paper_link,sort,pdf_path
```

Column notes:

| Column | Meaning |
| --- | --- |
| `state` | Pipeline state. Analyze rows that are ready, normally `Downloaded`; skip `checked`, `Skip`, `Missing`, and blank states unless the user says otherwise. |
| `importance` | Optional priority label such as `S/A/B/C`. Preserve it. |
| `paper_title` | Paper title used for reporting and fallback naming. |
| `venue` | Venue label, usually `CVPR 2025`, `ICLR 2026`, or `arXiv YYYY`. |
| `project_link_or_github_link` | Project page, GitHub repo, or `N/A`. |
| `paper_link` | Paper page such as arXiv/OpenReview/proceedings. |
| `sort` | Source section/category label. |
| `pdf_path` | Local PDF path. Prefer this exact path when analyzing. |

## Backward Compatibility

Use `paper_list.csv` terminology in this skill. If
`obsidian-vault/paper_list.csv` is missing but an old
`obsidian-vault/analysis/paper_list.csv` exists, do not blindly overwrite.
Tell the user you found the legacy log and propose a reviewed copy/convert step:

```bash
cp obsidian-vault/analysis/paper_list.csv obsidian-vault/paper_list.csv
```

Before using the copied file, review the header and a few rows to confirm the
columns match the expected `paper_list.csv` schema.

## Manager Workflow

1. Resolve the source CSV:
   - Use the user-provided path if supplied.
   - Otherwise use `obsidian-vault/paper_list.csv`.
   - If only legacy `paper_list.csv` exists, follow the reviewed migration
     step above before batching.
2. Create batches:

```bash
python3 .claude/skills/papers-batch-analyze/scripts/split_paper_list.py \
  --source obsidian-vault/paper_list.csv \
  --batch-size 25
```

The command prints the run directory and writes `manifest.json`.

3. Spawn up to 4 worker agents at a time. Each worker receives exactly one
   `batch_XXXX.csv`, the run directory, and these instructions:
   - Read only rows in its batch.
  - For each ready row, analyze the local PDF at `pdf_path` using the formal
    analysis chain (`scripts/run_local_paper_analysis.py`) and
    `rf-obsidian-markdown` rules. Reuse existing MinerU outputs when available.
    Do not add MinerU paths to `paper_list.csv`; pass `--mineru-output-root`
    and, when known, `--mineru-batch-id` so the runner can locate the one
    normalized paper directory for that PDF. If no unique MinerU output is
    found and preprocessed MinerU is required, record the row as failed.
   - Unless the user explicitly overrides it, use the runner's current formal
     defaults: main reasoning enabled with `--reasoning-effort max`,
     chunk/writer thinking disabled, and serialized section writers for
     prompt-cache reuse. Do not raise `--section-workers` above `1` during
     production batches unless the user asks for a latency/cost A/B test.
   - Use the current frontmatter schema: no `category`; `aliases` must be short
     English/model aliases; no `modalities`; no `frontier`.
  - For the formal local analysis runner, keep default token limits for normal
     papers and rely on its adaptive token budget for long/high-density papers:
     long papers raise part/main budgets, while writer stays at 8192.
   - Write one Markdown note per paper under `obsidian-vault/analysis/`, with
     `pdf_ref` pointing to the analyzed PDF.
   - Write a batch result file:
     `obsidian-vault/batches/<run_id>/results/batch_XXXX_results.json`
     containing `batch`, `processed`, `written_md`, `skipped`, and `failures`.
   - Do not edit the source `paper_list.csv` while workers run. Record status
     changes in the batch result file; the manager may consolidate reviewed
     status updates after all workers finish.
   - Do not edit another batch file or another worker's result file.
4. Failure isolation:
   - A failed paper is recorded in that batch result and does not block other
     papers in the same batch.
   - A failed batch does not block other batches.
   - After a failure, keep partial successful `.md` outputs and report the
     failed rows with reasons.
5. Script-only parallel mode:
   - If agent stability is a concern, prefer four independent
     `scripts/run_paper_list_analysis.py` processes instead of worker agents.
   - Use `--shard-index 0..3 --shard-count 4`, distinct `--run-id`, and distinct
     `--analysis-output-root` values so work directories and result logs do not
     collide.
   - Defer detection and repair until after all shards finish; inspect
     `obsidian-vault/batches/<run_id>/results.jsonl`, `summary.json`, and each
     child run `.state`.
6. After all completed batches finish, automatically run `papers-build-index`
   via the index builder:

```bash
python3 .claude/skills/papers-build-index/scripts/build_paper_index.py
```

Manual index refresh remains possible by invoking `papers-build-index` later.

## Completion Report

Report:

- Source CSV and run directory
- Batch count, completed batches, failed batches
- Number of Markdown notes written
- Index refresh command and result
- Any rows that still need manual review
