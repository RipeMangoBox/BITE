# ResearchFlow Skills

This directory is the maintained skill library for ResearchFlow agents. Each
skill is a `SKILL.md` file that tells an agent how to perform one bounded part
of the research workflow.

If your tool expects Codex-compatible skill paths, generate local aliases from
the repository root:

```bash
python3 scripts/setup_shared_skills.py
```

## Workflow

```text
collect candidate papers / import local PDFs
  -> download when needed
  -> MinerU parse
  -> analyze
  -> build index
  -> query / ideate / focus / review / export
```

## Current Status

The current default workflow is local-file based. The skills below operate on
`obsidian-vault/` and related local logs. Archived legacy skills live under
`_private/.archives/` for audit only and are not part of the default route.

| Skill | Status | Guidance |
|---|---|---|
| `research-workflow` | active router | Start here when the next stage is unclear. |
| `papers-collect-from-web` | active local collect | Collect candidate rows from web pages. |
| `papers-collect-from-github-repo` | active local collect | Collect candidate rows from GitHub paper lists. |
| `papers-download-from-list` | active local download | Download and repair PDFs into `obsidian-vault/paperPDFs`. |
| `papers-build-index` | local index | Regenerates `obsidian-vault/index` from local notes. |
| `papers-query-knowledge-base` | active local query | Search and compare papers from local notes and indexes. |
| `papers-audit-metadata-consistency` | local audit | Audits local exported notes and logs. |
| `paper-report` | active deep report | Use for deep single-paper reports. |
| `rf-obsidian-markdown` | Markdown convention | Applies to generated/local Markdown output. |
| `notes-export-share-version` | export utility | Creates shareable Markdown from local notes. |

## Entry Point

- **research-workflow**
  - Routes a request to one stage among local PDF import, collect, download,
    analyze, build, query, ideate, focus, review, audit, and export.
  - Use this first when you are not sure which skill should handle the next
    step.

## Paper Pipeline

- **papers-collect-from-web**
  - Collect candidate papers from non-GitHub web pages such as conference pages,
    lab pages, proceedings, and paper lists.
- **papers-collect-from-github-repo**
  - Collect candidate papers from GitHub repositories, including awesome lists,
    survey companion repos, lab paper lists, accepted-paper repos, and benchmark
    repos.
- **papers-download-from-list**
  - Download, verify, repair, and deduplicate PDFs from a curated triage list.
- **Local PDF folder import**
  - No dedicated library-sync skill is maintained. If you already have PDFs,
    provide the folder path to `research-workflow` or directly to the agent.
  - The agent should copy/register PDFs under `obsidian-vault/paperPDFs/` and
    align any batch rows with `obsidian-vault/paper_list.csv`.
- **Batch analysis from a paper list**
  - Provide `obsidian-vault/paper_list.csv` or a similar paper list to
    `research-workflow`.
  - Default batch size is 25 papers.
  - Default parallelism is 4 agents for 4 batches.
  - After completed batches, refresh `obsidian-vault/index/` automatically.
- **papers-audit-metadata-consistency**
  - Check title, venue, year, link, PDF reference, and note-structure
    consistency across generated analysis notes.
- **papers-build-index**
  - Rebuild `obsidian-vault/index/index.jsonl` and human navigation pages from
    analysis note frontmatter.

## Query, Ideation, and Review

- **papers-query-knowledge-base**
  - Query papers by title, task, technique tag, venue, year, or method. Uses
    `obsidian-vault/index/index.jsonl` as the fast filter layer when present, then
    reads matching analysis notes for evidence.
- **research-brainstorm-from-kb**
  - Generate research directions grounded in the local paper knowledge base.
- **idea-focus-coach**
  - Narrow a broad research idea into a scoped, executable plan.
- **reviewer-stress-test**
  - Challenge an idea, roadmap, or paper draft from a strict reviewer
    perspective and surface repair paths.

## Reports, Markdown, and Export

- **paper-report**
  - Generate a seven-section paper report: overview, background, core
    contribution, framework, formulas, experiments, and lineage.
- **scripts/run_local_paper_analysis.py**
  - Formal single-paper analysis chain for the default local workflow. It
    produces `_private/local_analysis_runs/**` artifacts and exports
    figure/table-aware notes into `obsidian-vault/analysis/`.
- **rf-obsidian-markdown**
  - Apply Obsidian-friendly Markdown conventions to generated notes.
- **notes-export-share-version**
  - Convert internal notes into share-ready Markdown.

## Utilities

- **code-context-paper-retrieval**
  - Legacy compatibility alias. Prefer `papers-query-knowledge-base` with a
    code-context request.
- **skill-fit-guard**
  - Diagnose recurring skill mismatch after a skill call and suggest whether the
    skill should be revised.
- **write-daily-log**
  - Generate or update a structured daily research log from current artifacts
    and decisions.
- **domain-fork**
  - Adapt the ResearchFlow workflow to another professional domain.

## Choosing a Skill

| Need | Skill |
|---|---|
| Unsure which stage you are in | `research-workflow` |
| Import a local PDF folder | Provide the folder path to `research-workflow` or the agent |
| Collect candidates from web pages | `papers-collect-from-web` |
| Collect candidates from a GitHub paper list | `papers-collect-from-github-repo` |
| Download PDFs from candidate rows | `papers-download-from-list` |
| Generate a deep single-paper report | `paper-report` |
| Rebuild the local index | `papers-build-index` |
| Audit metadata consistency | `papers-audit-metadata-consistency` |
| Search, summarize, or compare papers | `papers-query-knowledge-base` |
| Generate research ideas | `research-brainstorm-from-kb` |
| Focus an idea into a plan | `idea-focus-coach` |
| Run reviewer-style pressure tests | `reviewer-stress-test` |
| Export share-ready Markdown | `notes-export-share-version` |
