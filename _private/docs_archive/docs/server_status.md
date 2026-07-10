# Production Server Status Template

> This file is safe for the public repository. Do not record real hostnames,
> public IPs, SSH key paths, account names, proxy addresses, passwords, API
> keys, or provider credentials here.

Use this template for private deployment audits by copying it outside the
repository, or by storing the filled version under a private path ignored by
Git.

---

## 1. Access & Topology

| Field | Value |
|-------|-------|
| Public endpoint | `<deployment-host-or-domain>` |
| Hostname | `<redacted>` |
| OS | `<redacted>` |
| Docker | `<redacted>` |
| SSH | `ssh <user>@<host>` |
| Deploy root | `<remote-deploy-root>` |
| Branch on server | `<branch>` |
| Commit on server | `<short-sha>` |

`docker compose ps` snapshot:

```text
api       <status>
worker    <status>
mcp       <status>
caddy     <status>
postgres  <status>
redis     <status>
frontend  <status>
```

Public surface:

| Path | Backend |
|------|---------|
| `/api/*`, `/docs`, `/openapi.json` | `api:8000` |
| `/sse`, `/messages/*` | `mcp:8001` |
| anything else | `frontend:3000` |

---

## 2. Environment Variables

Secrets must stay redacted. Prefer documenting variable names and intent rather
than live values.

```dotenv
POSTGRES_PASSWORD=<redacted>
DATABASE_URL=postgresql+asyncpg://rf:<redacted>@postgres:5432/researchflow
REDIS_URL=redis://redis:6379/0

OBJECT_STORAGE_PROVIDER=<local|oss|cos>
OBJECT_STORAGE_BUCKET=<bucket-name>
OBJECT_STORAGE_REGION=<region>

DEEPSEEK_API_KEY=<redacted>
DEEPSEEK_BASE_URL=<provider-base-url>
DEEPSEEK_MODEL=<model-name>

KIMI_API_KEY=<redacted>
KIMI_BASE_URL=<provider-base-url>
KIMI_MODEL=<model-name>

S2_API_KEY=<redacted>
GITHUB_TOKEN=<redacted>
OPENREVIEW_USERNAME=<redacted>
OPENREVIEW_PASSWORD=<redacted>

HTTPS_PROXY=<redacted>
VENUE_PROXY=<redacted>
NO_PROXY=localhost,postgres,redis,127.0.0.1
```

---

## 3. Database Schema State

| Item | Value |
|------|-------|
| Alembic revision | `<revision>` |
| Table count | `<count>` |
| Papers | `<count>` |
| Analyses | `<count>` |
| Reports | `<count>` |

Record only aggregate counts that are safe to publish.

---

## 4. External Dependencies

| Endpoint | Status | Notes |
|----------|--------|-------|
| LLM provider | `<status>` | Do not include keys or signed URLs. |
| Object storage | `<status>` | Do not include bucket-private URLs. |
| API healthcheck | `<status>` | Use local or placeholder hosts. |

---

## 5. Rollout Checklist

```bash
# Sync code to your deployment target.
rsync -avz --delete \
  --exclude='.venv' \
  --exclude='__pycache__' \
  --exclude='.git' \
  --exclude='storage/' \
  --exclude='.env' \
  --exclude='obsidian-vault/' \
  ./researchflow-backend/ <user>@<host>:<remote-deploy-root>/

# Apply migrations.
ssh <user>@<host> \
  'cd <remote-deploy-root> && docker compose exec -T api bash -c "PYTHONPATH=/app alembic -c alembic/alembic.ini upgrade head"'

# Restart services that need the new code.
ssh <user>@<host> \
  'cd <remote-deploy-root> && docker compose restart api worker mcp'
```

---

## 6. Open Questions / Follow-Ups

1. Verify the public healthcheck path before documenting it as operational.
2. Keep live incident notes and server-specific audit snapshots outside the
   public repository.
