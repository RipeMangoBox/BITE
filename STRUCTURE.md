# Repository Structure

This file is the public map for top-level directories and files. Private notes,
generated exports, local data, and tool aliases stay out of Git.

## Top-Level Directories

| Path | Purpose | Public policy |
|---|---|---|
| `.claude/` | Maintained ResearchFlow agent skills and skill config | Keep |
| `_private/` | Local architecture notes, experiments, credentials, drafts, and archives | Ignore |
| `assets/` | Public logo/banner assets used by README files | Keep curated assets only |
| `linkedCodebases/` | Placeholder for local symlinks to related codebases | Keep README only |
| `obsidian-vault/` | Generated Obsidian browsing export | Keep README only |
| `obsidian-vault/analysis/` | Generated structured analysis notes and logs | Keep README only |
| `obsidian-vault/index/` | Generated JSONL index and navigation pages | Keep README only |
| `obsidian-vault/ideas/` | Generated or personal idea, focus, review, and log notes | Keep README only |
| `obsidian-vault/paperPDFs/` | Local source PDFs for analysis | Keep README only |
| `scripts/` | Setup, local paper workflow, maintenance, and audit utilities | Keep curated reusable scripts |
| `tests/` | Local/private regression tests, when present | Ignore |

## Top-Level Files

| File | Purpose | Public policy |
|---|---|---|
| `environment/.env.example` | Local environment template without secrets | Keep |
| `.gitattributes` | Git text/binary handling | Keep |
| `.gitignore` | Excludes local data, generated outputs, private notes, and caches | Keep |
| `AGENTS.md` | Agent-facing local workflow rules | Keep |
| `LICENSE` | Project license | Keep |
| `Makefile` | Common local conda commands | Keep |
| `README.md` | English public entry point | Keep |
| `README_CN.md` | Chinese public entry point | Keep |
| `STRUCTURE.md` | This repository map | Keep |
| `environment/environment.yml` | Recommended conda environment | Keep |
| `environment/pyproject.toml` | Python tooling config | Keep |
| `environment/pytest.ini` | Optional pytest defaults for local/private tests | Keep |
| `environment/requirements.txt` | Local workflow pip dependencies | Keep |

ResearchFlow currently supports the local file workflow through the conda
environment and local commands only.

## Layout Rules

- New reusable agent workflow instructions go under `.claude/skills/`.
- Generated research data stays in the placeholder data directories and is not
  committed.
- Local test suites stay out of Git unless a curated public test fixture is
  intentionally added.
- One-off experiments, private deployment notes, local credentials, and large
  source artifacts go under `_private/` or stay outside the repository.
