# ResearchFlow Platform

`platform/` contains experimental service code that is not part of the current
default local ResearchFlow workflow. The Python package name remains `backend`,
so local commands should run with `PYTHONPATH=platform` when explicitly working
on this code.

| Path | Purpose |
|---|---|
| `backend/` | FastAPI routes, DB models, ingestion, parsing, analysis, export, MCP, and worker code |
| `frontend/` | Optional Next.js web interface for experimental service browsing and operations |
| `alembic/` | Migration history for the experimental service schema |
| `config/` | Optional public source registry; private fixtures and generated config stay ignored |

The core research workflow starts from `.claude/skills/` and the root README.
Do not route normal paper-analysis tasks through `platform/` unless the user
explicitly asks to work on service code.
