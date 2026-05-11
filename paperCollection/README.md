# paperCollection

Current collection indexes are intentionally empty until the full ICLR 5k+
reanalysis is regenerated from PostgreSQL.

`obsidian-vault/` is the canonical human navigation export for 00_Home,
per-paper reports, and dataset/method/domain indexes. `paperCollection/` is a
secondary generated compatibility surface for lightweight JSON/navigation only.
Do not treat old `by_task/`, `by_technique/`, or `_AllPapers.md` outputs as
current.

For programmatic queries, use backend API: `POST /api/v1/search/hybrid`.

Legacy generated indexes were retired to
`_private/archives/past_versions/2026-05-09-current-analysis-retired-before-iclr5k-rerun/`.
