---
name: research-workflow
status: active-router
mode: local-file-workflow
description: >
  Unified entry for the research pipeline. Maps current work to one stage
  (import-local-pdfs/collect/download/analyze/build/query/ideate/focus/review/audit/export),
  recommends the right existing skill/command, supports step-by-step and
  end-to-end guidance, and keeps stage boundaries clear without duplicating
  underlying capabilities. Note: question-bank and pdfs-compress have been
  retired; their functions are covered by brainstorm and the download/analyze
  pipeline respectively.
---

# Research Workflow Entry

Use this as the single entry for local research workflow orchestration.
Route to file-based skills and their `obsidian-vault/` outputs.

It does **not** replace underlying skills. It routes to them with a clear stage model.

## Stage model

KB build chain:
- collect / import local PDFs → download when needed → analyze → (optional build)
- note: there is no dedicated library-sync skill. If the user already has PDFs,
  ask for the PDF folder path and register/copy them into the local vault layout.

KB usage chain:
- query (including comparison requests) → ideate → focus → review

Support chain:
- audit / export / code-context

## Purpose

- Provide one understandable entry point for the full workflow.
- Support both:
  - **step-by-step** execution (specify a stage)
  - **end-to-end** guidance (auto-detect next stage)
- Clarify each stage's input/output contract.
- Avoid overlap: orchestration here, execution in existing stage skills.

## Stage mapping (reuse existing skills)

- import local PDFs
  - Ask the user for the PDF folder path, category/sort hint, and venue/year
    hint. Use the local vault layout and `paper_list.csv` convention.
- collect
  - `papers-collect-from-web`
  - `papers-collect-from-github-repo`
- download
  - `papers-download-from-list`
- analyze
  - default route: `scripts/run_local_paper_analysis.py` formal analysis chain
    (MinerU parse/reuse → chunk anchor extraction → main analysis JSON →
    section writers → deterministic vault export with figures/tables)
  - `paper-report` supplies the deep-report writing contract for single-paper
    reports and formula derivation
  - note: after analyze, you can go directly to query; run build only if you need refreshed indexes
- build
  - `papers-build-index` (refreshes both `obsidian-vault/index/index.jsonl` for agents and Obsidian navigation pages)
- query
  - `papers-query-knowledge-base` (also handles comparison and code-context requests)
- ideate
  - `research-brainstorm-from-kb`
- focus
  - `idea-focus-coach` (can be used independently; does not depend on ideate output)
- review
  - `reviewer-stress-test` (can be used independently; does not depend on focus output)
- audit
  - `papers-audit-metadata-consistency`
- export
  - `notes-export-share-version`

## Input contract by stage

- import local PDFs: PDF folder path; optional category/sort and venue/year hints
- collect: URLs or GitHub repo URL + venue/year + include/exclude
- download: triage/log file path
- analyze: local PDF path, existing MinerU output directory, or `Downloaded` queue
- build: no extra input (defaults to current repository)
- query: task description/keywords (optional changed files, mode=brief/deep; comparison requests also route here)
- ideate: research problem statement
- focus: initial idea + goal preferences (can come from ideate or be independent input)
- review: idea / roadmap / full paper (can come from focus or be independent input)
- audit: no extra input (scan current obsidian-vault/analysis)
- export: note path to export

## Output contract by stage

For each stage, return:

1. Current stage
2. Input requirements
3. Recommended execution (skill or command template)
4. Output paths
5. Suggested next stage

## Typical usage

### 1) I don't know what to run next

- Describe what you are currently doing
- The workflow will identify the stage and recommend the right skill

### 2) I only want one stage

- Specify the stage name
- Run the corresponding skill

### 3) End-to-end pass

- Start from auto
- Execute stage by stage
- At each stage, verify outputs exist before advancing

## Non-goals

- Do not replace execution logic of any underlying skill
- Do not auto-chain multiple stages (after each stage, suggest next step and let the user decide whether to continue)

## State Convention

`paper_list.csv` paper states follow a unified convention. See `STATE_CONVENTION.md`:

```
Main pipeline: Wait → Downloaded → checked
Out-of-band states: Skip (manually skipped), Missing (download failed)
```
