# SIG/SIGA/TOG Coverage Summary 2026-06-29

Goal: make `obsidian-vault/paper_list.csv` cover accepted SIGGRAPH,
SIGGRAPH Asia, and TOG-related technical papers from 2022 onward.

## Imported Sources

- SIGGRAPH 2022, 2023, 2024 and SIGGRAPH Asia 2022, 2023, 2024:
  `paperSources/siggraph_full_collect_20260624/merge_report.json`.
  Source records: 1525.
- SIGGRAPH 2025:
  existing `paper_list.csv` rows are primarily anchored to
  `https://s2025.conference-schedule.org/` official schedule links.
- SIGGRAPH Asia 2025 Conference track:
  `paperSources/sig_coverage_20260629/crossref_siga2025_conference_papers.jsonl`.
  Selection: Crossref records with DOI prefix `10.1145/3757377.*` and
  container title `Proceedings of the SIGGRAPH Asia 2025 Conference Papers`.
  Source records: 201.
- SIGGRAPH Asia 2025 Journal/TOG-related track:
  `paperSources/sig_coverage_20260629/kesen_siga2025Papers.md`, fetched
  through Jina Reader from Ke-Sen Huang's SIGGRAPH Asia 2025 papers page.
  The page states ACM permission and defines `SIG/TOG`, `SIG`, and `TOG`.
  Imported only `SIG/TOG` and `TOG` markers by default because the `SIG`
  conference track is already covered by the ACM proceedings DOI family.
- SIGGRAPH 2026:
  `paperSources/sig_coverage_20260629/sig2026_snippet_2026-07-20.html`
  through `sig2026_snippet_2026-07-23.html`, official Linklings schedule
  snippets under the Technical Paper filter. Parsed rows with `ssid` matching
  `papers_*` or `paperstog_*`.
- ACM TOG volume/issue audit:
  `scripts/local_maintenance/append_tog_issues_crossref.py --dry-run` queried
  Crossref for ACM TOG ISSN `0730-0301` and volume/issue pairs 41(4), 41(6),
  42(4), 42(6), 43(4), 43(6), 44(4), 44(6), 45(4), and 45(6). The dry run was
  intentionally not committed because many remaining candidates use short
  Crossref titles such as model names, while existing SIG/SIGA rows often use
  full titles with subtitles.

## Current Counts

After this run, `paper_list.csv` has:

- SIGGRAPH 2022: 313
- SIGGRAPH 2023: 242
- SIGGRAPH 2024: 279
- SIGGRAPH 2025: 416
- SIGGRAPH 2026: 343
- SIGGRAPH Asia 2022: 206
- SIGGRAPH Asia 2023: 223
- SIGGRAPH Asia 2024: 267
- SIGGRAPH Asia 2025: 317

## Known Caveats

- SIGGRAPH 2026 schedule has 345 paper rows: 309 `papers_*` and 36
  `paperstog_*`. Six titles already existed locally, so 339 rows were added.
- The SIGGRAPH 2026 conditional PDF has 317 `papers_*` IDs. Sixteen PDF IDs
  were not present in the schedule snippets and were not added because the PDF
  contains IDs without titles. The mismatch is recorded in
  `append_siggraph2026_schedule_report.json`.
- Five pre-existing normalized-title duplicates remain in SIGGRAPH 2025 rows.
  They predate this run and were not removed.
- Independent TOG rows are not used as the primary completeness measure for
  SIG/SIGA accepted-paper coverage here. Most TOG issue records already match
  existing SIG/SIGA rows by title, DOI, or short-title containment. Remaining
  short-title candidates require safer alias-aware reconciliation before
  appending.
