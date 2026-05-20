# scripts/

Utility scripts for ResearchFlow.

Most day-to-day work should start from `.claude/skills` and the root README.
Use scripts when you need direct file maintenance, index checks, or advanced
service maintenance.

## Local Workflow Scripts

| Script | Purpose |
|---|---|
| `setup_shared_skills.py` | Create local `.codex/` skill aliases from `.claude/skills` |
| `link_codebase.py` | Create symlinks or junctions under `linkedCodebases/` |
| `auto_download_papers.py` | Download PDFs from triage logs |
| `playwright_download.py` | Headless browser PDF download fallback |
| `update_download_log.py` | Normalize download log format |
| `find_pdfs.py` | Locate PDFs on disk |
| `audit_knowledge_batch.py` | Check analysis file structure |
| `fix_analysis_md_issues.py` | Repair broken frontmatter |
| `fix_missing_venue_year.py` | Fill missing venue/year |
| `review_analysis_mismatch.py` | Compare CSV log rows with Markdown files |
| `run_local_paper_analysis.py` | Formal single-paper analysis chain: MinerU parse/reuse → anchor extraction → main analysis → section writing → vault export with figures/tables |
| `run_paper_list_analysis.py` | Script-only queue runner for rows in `obsidian-vault/paper_list.csv` |
| `smoke_index_workflow.py` | Verify `research-workflow` auto routing and `papers-build-index` behavior on temporary empty and one-note vaults |

## Index Maintenance

| Script | Purpose |
|---|---|
| `maintenance/get_missing_md.py` | Find PDFs without analysis notes |
| `paper_analysis_maintenance/check_part_sections.py` | Audit Part I/II/III headers |
| `paper_analysis_maintenance/fill_project_github_in_abstract.py` | Fill project/GitHub links when available |
| `paper_analysis_maintenance/mark_wait_for_incomplete_parts.py` | Mark incomplete analyses in logs |
| `paper_analysis_maintenance/salad_format_audit.py` | Strict format compliance check |

## Legacy Service Maintenance

Retired service-mode database scripts depend on the hidden `platform/` tree.
They are not part of the public local-file workflow and are ignored unless a
future service implementation deliberately reintroduces them.

Generated logs, caches, service dumps, and one-off run outputs should stay out
of Git.
