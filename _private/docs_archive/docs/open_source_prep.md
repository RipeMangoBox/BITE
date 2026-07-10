# Open Source Prep Report

Date: 2026-05-15
Branch: `feat/filter-report-obsidian-fixes-current`

## Scope

This audit reviewed the current working tree for public-release readiness. It
did not modify paper analysis Markdown/PDF content, vault exports, `_private`,
local storage, cache contents, or generated analysis data.

## Changes Made

- Root `.gitignore` now excludes local trash, root-level PDFs, dated local
  research drafts, and the current root scratch notes.
- `researchflow-backend/.gitignore` now excludes local deploy env variants,
  the server-specific OSS mirror helper, and a generated local test result.
- `researchflow-backend/.dockerignore` now excludes env files, Git metadata,
  caches, local storage, exports, backups, vault/analysis/PDF data, `_private`,
  secret files, and private keys from Docker build context.
- `docs/server_status.md` was replaced with a public-safe template. The prior
  working copy exposed a real public IP, hostname, SSH key path, topology, and
  private operational details.
- `researchflow-backend/DEPLOY.md`, `METADATA_ACQUISITION.md`, and
  `.env.production` now use placeholders instead of provider-key shaped values,
  host-local proxy endpoints, or point-in-time server measurements.
- `.obsidian/` now keeps the public default vault configuration with the
  checked-in Blue Topaz theme and sanitized workspace state.
- `.claude/scheduled_tasks.lock` was removed from the tracked public surface
  and future `.claude/*.lock` runtime files are ignored.

## Suggested Submit Group

Submit these if their code owner confirms the behavior:

- `docs/deploy.md`
- `docs/server_status.md`
- `docs/open_source_prep.md`
- `.gitignore`
- `researchflow-backend/.gitignore`
- `researchflow-backend/.dockerignore`
- `researchflow-backend/.env.deploy` after confirming it should remain a
  tracked template and after rotating any previously exposed credentials
- `researchflow-backend/.env.production` as a template, if the project wants
  both deploy and production env examples
- `researchflow-backend/.env.example`
- `researchflow-backend/METADATA_ACQUISITION.md`
- `researchflow-backend/Dockerfile`
- `researchflow-backend/docker-compose.yml`
- `researchflow-backend/docker-compose.prod.yml`
- `researchflow-backend/uv.lock` if the project adopts `uv` lockfile commits
- Local/offline analysis tests and one-off batch tooling should remain under
  `_private/` unless promoted as generic supported tooling.

## Must Exclude From Public Commit

- `.trash/`
- Root-level local research drafts:
  `2026-05-10_motion-paradigm-shift-strategic-analysis.md`,
  `2026-05-10_xhs-motion-blogger-landscape.md`,
  `2026-05-10_xhs-motion-social-landscape.md`,
  `2026-05-11_visual-prior-assisted-text-to-motion.md`,
  `2026-05-12_fine-grained-text-motion-alignment-design.md`,
  `ChinaMM.md`, `T_Math_Reasoning.md`
- Root-level PDFs, including `332 Submission.pdf`
- `researchflow-backend/.env`
- `researchflow-backend/storage/`
- `.claude/*.lock`
- `paperAnalysis/`, `paperPDFs/`, `obsidian-vault/`, `_private/`
- Local one-off smoke/test runners and generated results under
  `researchflow-backend/scripts/` unless rewritten as generic supported tooling
- Generated caches such as `__pycache__/`, `.pytest_cache/`, build artifacts,
  and local backups

## Sensitive Points Requiring Manual Confirmation

1. `researchflow-backend/.env.deploy` is currently sanitized in the working
   tree, but the diff shows that the previous tracked version contained a real
   database password and a Kimi-style API key. Rotate those credentials and
   rewrite public release history before pushing to any public remote.
2. `researchflow-backend/DEPLOY.md` has been template-sanitized, but it still
   contains operational guidance and dated architecture assumptions. Backend
   owners should confirm it matches the current deployment contract.
3. `.mcp.json` is tracked and contains a concrete MCP endpoint. It was outside
   the allowed write scope for this pass; sanitize or exclude it before public
   release.
4. Batch handoff prompts and local/offline analysis runners have been moved
   under `_private/`. Keep them excluded from public commits unless they are
   rewritten as generic supported tooling.
5. Existing tracked files may still contain local MinerU fallback or planning
   paths, especially around parse/deploy workflows. These are not API secrets,
   but they are internal assumptions. Review before publishing as supported
   tooling.
6. `docs/deploy.md`, `.env.example`, Dockerfile, and docker-compose files now
   use placeholders or provider endpoints rather than live keys, but the
   deployment behavior changes should be reviewed by the code owner.

## Verification Commands

Run these before staging:

```bash
git status --short
git status --ignored --short .trash '332 Submission.pdf' '2026-05-10_motion-paradigm-shift-strategic-analysis.md' researchflow-backend/storage
# Also run a sensitive-token scan for real API keys, private keys, concrete
# infrastructure endpoints, and user-specific absolute paths before staging.
```
