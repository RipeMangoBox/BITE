# System Architecture

ResearchFlow uses a local-first three-layer architecture.

```text
┌─────────────────────────────────────────────────────────┐
│  Output layer        obsidian-vault/ideas/              │
│                      ideas, plans, review notes         │
├─────────────────────────────────────────────────────────┤
│  Index layer         obsidian-vault/index/              │
│                      JSONL index + navigation pages     │
├─────────────────────────────────────────────────────────┤
│  Evidence layer      obsidian-vault/analysis/           │
│                      structured notes + logs            │
│                      obsidian-vault/paperPDFs/          │
│                      source PDFs                        │
└─────────────────────────────────────────────────────────┘
```

## Evidence layer

- `obsidian-vault/paperPDFs/` stores source PDFs.
- `obsidian-vault/analysis/` stores per-paper structured analysis notes and
  logs.
- This is the primary evidence surface that agents should read.

## Index layer

- `obsidian-vault/index/` stores generated retrieval indexes and navigation
  pages.
- At scale, agents should start from `index.jsonl`, filter candidates, then
  read matching analysis notes.

## Output layer

- `obsidian-vault/ideas/` stores brainstorm notes, focused plans, reviewer
  critiques, and daily logs.
- This layer is downstream of evidence and index, not a substitute for them.

## Working rule

When the vault is large, use:

```text
index.jsonl -> filter -> matching analysis notes -> downstream ideas
```
