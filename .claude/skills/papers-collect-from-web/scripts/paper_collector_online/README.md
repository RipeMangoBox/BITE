---
created: 1970-01-01T08:00
updated: 2026-03-17T19:54
---
# paper_collector_online

Append paper candidates to `obsidian-vault/paper_list.csv` by fetching web
pages, saving HTML locally, and extracting paper links.

## Quick start

```bash
python3 ".claude/skills/papers-collect-from-web/scripts/paper_collector_online/collect_from_urls.py" \
  --venue-time "ICLR 2026" \
  --urls "https://example.com/papers.html" "https://another.example.org/list" \
  --include "motion;diffusion" \
  --exclude "workshop;dataset" \
  --append
```

## Output columns

`state,importance,paper_title,venue,project_link_or_github_link,paper_link,sort,pdf_path`

Notes:
- `state` defaults to `Wait`.
- `importance`, `sort`, and `pdf_path` are left blank for later stages.

## Where HTML is stored

Default:

`paperSources/<venue_time>_<timestamp>/...`
