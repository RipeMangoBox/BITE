# ResearchFlow Private Workspace Registry

Updated: 2026-07-09

`_private/` is now a branch-local tracked workspace by default. Its purpose is
to retain traceable project decisions, audits, workflow helpers, and small
evidence artifacts while keeping credentials, browser state, large staging data,
and generated backups ignored.

## Fast Entry Points

| Need | Path |
|---|---|
| Directory policy and current layout | `_private/README.md` |
| BITE / PaperBite architecture and roadmap | `_private/planning/researchflow/` |
| ICLR 2026 topic prioritization | `_private/topic_priority/` |
| ICLR 2026 shortlist selection | `_private/iclr26_selection/` |
| Analysis-chain version history | `_private/version_analysis_chain/` |
| BITE v04/v06 update notes | `_private/BITE_versions/` |
| MinerU and structured-context budget audits | `_private/analysis_audits/` |
| ACM/SIGGRAPH browser download recovery | `_private/acm_download_recovery/` |
| PDF over-compression recovery | `_private/pdf_recovery/` |
| SIGGRAPH wait-state DOI/PDF resolution | `_private/sig_wait_resolve_20260701/` |
| Current small local analysis runs | `_private/local_analysis_runs/` |
| Hugging Face update reports/manifests | `_private/hf_updates/` |
| Release and public-sync audit evidence | `_private/release_audit/`, `_private/merge_audits/` |
| Retired but historically useful material | `_private/obsolete/`, `_private/docs_archive/`, `_private/archives/` |

## Ignored Private Or Bulky Paths

| Path | Reason |
|---|---|
| `_private/aliyun_key/` | SSH key material. |
| `_private/acm_download_recovery/secrets/` | Cookie/exported browser credential material. |
| `_private/browser_profiles/` | Browser profile databases, cookies, cache, and runtime locks. |
| `_private/hf_stage/` | Full local dataset staging mirror, about 5 GB. |
| `_private/hf_updates/**/media/` | Sharded media assets, hundreds of MB. |
| `_private/hf_updates/**/stage/` | Generated staging copy of analysis/index material. |
| `_private/pdf_overcompressed_backup/` | Large PDF backup tree, about 1.4 GB. |
| `_private/pdf_recovery_work/` | Recreated scratch space for PDF recovery runs. |
| `_private/local_obsidian_config/`, `_private/obsidian_config_backups/` | Local app configuration and personal workspace state. |
| `_private/mineru_local/` | Local MinerU config snapshot. |
| `_private/.archives/` | Compressed historical bundles; global archive rules also apply. |

## Layout Rules

- Keep only registry-style entry files at `_private/` root.
- Put related workflow logs next to their scripts and README files.
- Keep path-specific ignore rules in `.gitignore`; do not re-add a blanket
  `_private/` ignore.
- Preserve source anchors in dated audit logs, queues, and reports.
- Before syncing to public `main`, review `_private/` content and exclude
  branch-specific or local-development material.
