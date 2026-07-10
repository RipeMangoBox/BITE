# _private Directory Guide

`_private/` stores branch-local project history, audits, private workflow helpers,
and local evidence that should not be synchronized to the public `main` worktree
without review.

As of 2026-07-09, `_private/` is no longer ignored as a whole. Small text
artifacts are trackable by default. Secrets, browser state, local app settings,
dataset staging, PDF backups, and generated recovery work remain ignored through
path-specific `.gitignore` rules.

## Current Layout

| Directory | Role | Git policy |
|---|---|---|
| `planning/` | ResearchFlow/BITE architecture, roadmap, RWiki notes, watchlists. | Track |
| `topic_priority/` | ICLR 2026 topic taxonomy, assignments, quality audit dossiers, and selected workflow batches. | Track |
| `iclr26_selection/` | ICLR 2026 candidate selection rules, scripts, shortlist, and audit summary. | Track |
| `version_analysis_chain/` | Analysis-chain version notes and prompt/flow change history. | Track |
| `BITE_versions/` | Versioned BITE release/update notes and modernization audit summaries. | Track small docs; compressed assets follow global archive rules |
| `analysis_audits/` | MinerU/context-budget audit scripts and their 2026-06-26 reports. | Track |
| `acm_download_recovery/` | ACM/SIGGRAPH browser-download workflow notes, queue snapshots, and helper script. | Track docs/queue/script; ignore `secrets/` and generated `reports/` |
| `pdf_recovery/` | 2026-07-02 PDF over-compression recovery scripts, candidate lists, and recovery logs. | Track logs/scripts; ignore large PDF backups and work dirs |
| `sig_wait_resolve_20260701/` | SIGGRAPH wait-state DOI/PDF resolution queue and report artifacts. | Track |
| `local_analysis_runs/` | Small current integrated-analysis run outputs for Hunyuan3D/MaterialMVP checks. | Track |
| `arxiv_sources_hunyuan3d/` | Source markdown snapshots for Hunyuan3D-related local analyses. | Track |
| `release_audit/` | OSS release checklist, MinerU normalization logs, and project-link audit. | Track |
| `merge_audits/` | Branch/public privacy and merge audit notes. | Track |
| `docs_archive/`, `backups/`, `obsolete/`, `archives/` | Historical docs, small backups, retired local notes, and duplicate-analysis cleanup evidence. | Track text evidence; ignore generated assets/PDFs inside test side effects |
| `hf_updates/` | PaperBite Hugging Face update manifests and reports. | Track manifests/reports; ignore bulky `media/` and `stage/` |
| `hf_stage/` | Full local Hugging Face staging mirror. | Ignore |
| `pdf_overcompressed_backup/` | Large backup copy of PDFs replaced during compression recovery. | Ignore |
| `browser_profiles/` | Chrome/Edge profile state used for browser-mediated downloads. | Ignore |
| `aliyun_key/`, `acm_download_recovery/secrets/` | Credentials and cookies. | Ignore |
| `local_obsidian_config/`, `obsidian_config_backups/`, `mineru_local/` | Local machine/app configuration snapshots. | Ignore |

## Cleanup Policy

- Delete only obvious runtime trash: `__pycache__/`, empty logs, temporary
  `tmp_*` candidate files, and generated work directories that can be recreated.
- Preserve dated audit logs, queue snapshots, migration notes, selection rules,
  and retired bundles when they explain a decision or recovery path.
- Keep large raw assets and sensitive local state in place only when useful, but
  keep them ignored.
- Do not sync `_private/` blindly to public `main`; review private content and
  path-specific ignore rules first.
