---
name: domain-fork
status: design-only-legacy
description: Migrates ResearchFlow's architecture to a new professional domain (e.g. frontend development, accounting, journalism). Interactive session with the user to map research concepts to domain equivalents, then generates a complete set of adapted skills and folder structure. Explicit trigger only.
---

# Domain Fork

## Purpose

Migrate the core ResearchFlow architecture (collect/import local sources → download when needed → analyze → build index → query → ideate → focus → review) into a user-specified professional domain, and generate a complete domain-adapted skill set plus folder structure in one pass.
This is a design-only legacy workflow. It is not part of the active paper
analysis pipeline.

## Trigger

**Explicit invocation only**. It should not be auto-triggered by description matching.

User must clearly request something like:
- "Fork a frontend development version of ResearchFlow"
- "Migrate ResearchFlow to the accounting domain"
- "Use domain-fork to create a journalism knowledge-base workflow"

## Interactive Flow

After invocation, enter an interactive confirmation flow with **no skipped steps**:

### Step 1: Domain confirmation

Confirm with the user:
- **Target domain**: e.g., "frontend development", "accounting/audit", "news production"
- **Repository name**: suggest `<Domain>Flow` (e.g., `FrontendFlow`, `AccountingFlow`, `JournalismFlow`), user can override
- **Save location**: if not specified, default to `ResearchFlow/<RepoName>/` and prompt:

> "Default output path is ResearchFlow/<RepoName>/. Do you want to change it?"

### Step 2: Concept mapping table

Generate a ResearchFlow → target-domain concept mapping table for user confirmation/edit:

| ResearchFlow concept | Mapped target-domain concept | Notes |
|-------------------|--------------|------|
| paper | (domain equivalent) | e.g., technical article, regulation document, news story |
| PDF | (domain equivalent) | e.g., webpage article, regulation PDF, manuscript document |
| venue | (domain equivalent) | e.g., technical blog/framework version, regulator source, media source |
| obsidian-vault/analysis | (domain equivalent) | e.g., technical notes, regulation interpretation, editorial analysis |
| obsidian-vault/index | (domain equivalent) | e.g., technical index, regulation index, topic index |
| obsidian-vault/paperPDFs | (domain equivalent) | e.g., original articles, source regulations, source manuscripts |
| obsidian-vault/ideas | (domain equivalent) | e.g., project proposals, audit strategies, topic plans |
| core_operator | (domain equivalent) | e.g., core technical strategy, core regulation clause, core news angle |
| primary_logic | (domain equivalent) | e.g., implementation flow, compliance-check flow, editorial flow |
| paper_list.csv | keep | main tracking log, with domain-adjusted columns |
| state: Wait→Downloaded→checked | keep or adapt | state machine may need domain adaptation |

### Step 3: Skill mapping confirmation

Show how ResearchFlow's 17 routed skills map to target-domain skills (the shared Markdown convention skill can be copied separately without renaming):

| ResearchFlow Skill | Target-domain Skill | Keep? | Adjustment |
|-------------------|---------------|---------|---------|
| local source import | `<domain>-import-local-sources` | ✅/❌ | keep when users already have local source files or a source inbox |
| papers-collect-from-web | `<domain>-collect-from-web` | ✅ | source websites become domain-specific |
| papers-collect-from-github-repo | `<domain>-collect-from-curated-list` | ✅/❌ | depends on whether curated lists exist |
| papers-download-from-list | `<domain>-download-from-list` | ✅ | download objects become domain documents |
| scripts/run_local_paper_analysis.py / paper-report | `<domain>-analyze-document` | ✅ | analysis template rewritten for domain |
| papers-audit-metadata-consistency | `<domain>-audit-metadata` | ✅ | metadata fields adjusted for domain |
| papers-build-index | `<domain>-build-index` | ✅ | index dimensions adjusted for domain |
| papers-query-knowledge-base | `<domain>-query-kb` | ✅ | query dimensions adjusted for domain; handles comparison requests |
| code-context-paper-retrieval | `code-context-<domain>-retrieval` | ✅/❌ | keep only for code-related domains |
| research-brainstorm-from-kb | `<domain>-brainstorm-from-kb` | ✅ | ideation dimensions adjusted for domain |
| idea-focus-coach | `<domain>-focus-coach` | ✅ | focus dimensions adjusted for domain |
| reviewer-stress-test | `<domain>-stress-test` | ✅ | review standards adjusted for domain |
| research-workflow | `<domain>-workflow` | ✅ | stage naming adjusted for domain |
| notes-export-share-version | `notes-export-share-version` | ✅ | generic, no change needed |
| skill-fit-guard | `skill-fit-guard` | ✅ | generic, no change needed |
| write-daily-log | `write-daily-log` | ✅/❌ | keep when the target domain needs evidence-based daily summaries |
| domain-fork | `<domain>-fork` | ❌ | usually do not recurse the migration skill into the forked repo |

User may:
- remove unnecessary skills
- rename skills
- adjust mapping relationships

### Step 4: Confirm and generate

After user confirmation, generate in one pass:

1. **Directory structure**

```
<RepoName>/
├── .claude/
│   ├── skills-config.json
│   └── skills/
│       ├── User_README.md
│       ├── README.md
│       ├── STATE_CONVENTION.md
│       └── <all mapped skills>/
├── <AnalysisDir>/          # maps from obsidian-vault/analysis
│   └── tracking_log.csv    # maps from paper_list.csv
├── <CollectionDir>/        # maps from obsidian-vault/index
│   ├── by_<dim1>/
│   ├── by_<dim2>/
│   └── by_<dim3>/
├── <SourceDir>/            # maps from obsidian-vault/paperPDFs
├── <IdeaDir>/              # maps from obsidian-vault/ideas
└── README.md
```

2. **SKILL.md for each skill**: rewritten from corresponding ResearchFlow skill with all domain terminology replaced
3. **skills-config.json**: register all generated skills
4. **STATE_CONVENTION.md**: state transitions adapted for the target domain
5. **User_README.md / README.md**: domain-adapted navigation and instructions
6. **tracking_log.csv**: empty template with domain-adjusted column names
7. **Repository README.md**: domain-adapted overview

## Generation Principles

1. **Structural symmetry**: keep the collect → build → use three-stage architecture
2. **Terminology consistency**: use one consistent term per concept across all skills
3. **Minimum viable generation**: generate only skill definitions (`SKILL.md`), not scripts (agent writes scripts on demand)
4. **State machine continuity**: keep the three-state main flow `Wait → Downloaded → checked`, with optional domain-specific labels
5. **Do not modify ResearchFlow**: domain-fork reads ResearchFlow as template only and must not edit any ResearchFlow file

## Boundaries

- Generate skill definitions and folder structure only; do not generate real content data
- Do not auto-populate `tracking_log.csv` (that happens when users use the new repository)
- Do not copy ResearchFlow `obsidian-vault/analysis` / `obsidian-vault/index` / `obsidian-vault/paperPDFs` data
- Do not copy `.obsidian.zip` (user can copy/adjust it manually if needed)

## Example

User: "Fork a frontend development version"

Step 1 confirmation:
- domain: frontend development
- repo name: FrontendFlow
- path: ResearchFlow/FrontendFlow/

Step 2 mapping:
- paper → technical article/spec document
- PDF → webpage article/PDF spec
- venue → technical blog/framework version/W3C standard
- obsidian-vault/analysis → articleAnalysis
- obsidian-vault/index → articleCollection
- obsidian-vault/paperPDFs → articleSources
- core_operator → core technical strategy
- primary_logic → implementation flow

Step 3 skill mapping:
- `papers-collect-from-web` → `articles-collect-from-web`
- `papers-collect-from-github-repo` → `articles-collect-from-curated-list`
- `code-context-paper-retrieval` → `code-context-article-retrieval` (kept; frontend is code-centric)
- `reviewer-stress-test` → `code-review-stress-test` (mapped to code review perspective)
- ...

Step 4: generate the complete `FrontendFlow/` structure.
