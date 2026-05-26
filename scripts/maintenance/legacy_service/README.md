# Legacy Service Maintenance Scripts

This directory documents local-only Python scripts written for the retired
service-mode ResearchFlow implementation backed by the hidden `platform/`
tree and a service database. The script files themselves are ignored by Git.
They are not part of the current local-file analysis chain described in
`.claude/skills/README.md`.

Use these only for historical maintenance or migration work when the ignored
script files, `platform/`, and the target database/schema are present locally.
Most scripts mutate database rows or service-derived artifacts; prefer
`--dry-run` or read the script header before any write run.

## How To Run

Run scripts by direct path from the repository root so their local
`_platform_path.py` helper can add `platform/` to `sys.path`:

```bash
python scripts/maintenance/legacy_service/<script>.py --help
```

Some archived docstrings still show their original root-level or
`python -m scripts.<name>` command. Treat those as historical examples; use the
direct path above from this archive location.

## Archived Groups

- `backfill_*.py`, `cleanup_overtagged_facets.py`, `infer_method_lineage.py`,
  `regenerate_paper_report.py`: service database graph/profile/report
  backfills.
- `promote_venue_papers.py`, `smoke_full_ingest.py`,
  `reanalyze_and_compare.py`: service ingest validation and reanalysis helpers.
- `audit_kb_quality.py`, `dedup_papers.py`, `import_baselines.py`,
  `inject_analysis_repair_for_two_papers.py`, `patch_schema_for_pipeline.py`:
  one-off database audit, repair, schema, and seed-data utilities.

The active local workflow keeps its maintained runners and vault maintenance
tools in `scripts/` and `scripts/paper_analysis_maintenance/`.
