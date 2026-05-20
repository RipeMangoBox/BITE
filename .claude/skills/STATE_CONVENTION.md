# Paper State Convention

Unified definitions for the `state` column in `paper_list.csv`. All skills must follow this convention.

## State flow

```
Wait → Downloaded → checked
  │        │
  │        ├→ too_large          (PDF exceeds size limit after compression)
  │        └→ analysis_mismatch  (analysis template incomplete after retry)
  │
  ├→ Skip     (user manually excluded)
  └→ Missing  (download failed, PDF unavailable)
```

## Main pipeline states

| state | Meaning | Written by | Next action |
|-------|---------|------------|-------------|
| `Wait` | Newly collected candidate, waiting for download | collect (from-web / from-github-awesome) | Run download |
| `Downloaded` | PDF downloaded to `obsidian-vault/paperPDFs/`, waiting for analysis | download (`papers-download-from-list`) | Run analyze |
| `checked` | Structured analysis completed; `.md` exists in `obsidian-vault/analysis/` | analyze (`scripts/run_local_paper_analysis.py`) | Ready for query / build index |

## Abnormal states (from analyze stage)

| state | Meaning | Written by | Recovery |
|-------|---------|------------|----------|
| `analysis_mismatch` | Analysis generated but required report sections, anchors, or figure/table export are incomplete after one retry | analyze (`scripts/run_local_paper_analysis.py`) | Re-run analyze on this entry, or manually edit the `.md` then set state to `checked` |
| `too_large` | PDF exceeds local parsing limits after compression; skipped | analyze (`scripts/run_local_paper_analysis.py`) | Manually compress or split the PDF, then set state back to `Downloaded` |

## Out-of-band states
![1775910552974](image/STATE_CONVENTION/1775910552974.png)![1775910556384](image/STATE_CONVENTION/1775910556384.png)
| state | Meaning | Written by | Recovery |
|-------|---------|------------|----------|
| `Skip` | Manually filtered out, not processed | User (manual edit) | Set back to `Wait` if reconsidered |
| `Missing` | PDF unavailable after repeated download attempts | download (`papers-download-from-list`) | Retry later, or manually place PDF then set to `Downloaded` |

## Rules

1. Main pipeline moves forward only: `Wait → Downloaded → checked`.
2. `Skip` and `Missing` are set from `Wait`; `too_large` and `analysis_mismatch` are set from `Downloaded`.
3. Only the user may revert a state (e.g. `Missing → Wait`, `too_large → Downloaded`).
4. Downloads automatically compress PDFs > 20 MB before analysis.
5. Each skill only processes entries at its own input state:
   - download processes `Wait`
   - analyze processes `Downloaded`
   - build-collection-index processes `checked`

## Field fallback values

| Field | Fallback | Notes |
|-------|----------|-------|
| venue | `arXiv YYYY` | For works not accepted by a venue but published on open platforms such as arXiv, e.g., `arXiv 2025` |
| project_link_or_github_link | `N/A` | Confirmed no open-source code or project page |
