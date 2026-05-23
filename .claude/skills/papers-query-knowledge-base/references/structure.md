# obsidian-vault/index & obsidian-vault/analysis — Paths and schema

For tooling, scripts, or Agent skill that need exact paths and frontmatter fields. Paths are relative to the repository root that contains `obsidian-vault/index/`, `obsidian-vault/analysis/`, and `obsidian-vault/paperPDFs/`.

## Root paths

- `obsidian-vault/index/` — index layer
- `obsidian-vault/analysis/` — analysis notes
- `obsidian-vault/paperPDFs/` — PDFs (linked from analysis only)

Use the matching absolute repository path for your machine when invoking from another workspace.

## obsidian-vault/index layout

| Path | Description |
| ------ | ------ |
| `obsidian-vault/index/README.md` | Public placeholder explaining generated index files; tracked and not overwritten |
| `obsidian-vault/index/paper_index.md` | Generated home: links to _AllPapers, by_topic, by_method, by_dataset, by_venue, by_year |
| `obsidian-vault/index/_AllPapers.md` | All papers grouped by topic, then venue/year |
| `obsidian-vault/index/by_topic/topic_index.md` | List of coarse top-level topics |
| `obsidian-vault/index/by_topic/<topic>.md` | Papers for one coarse topic |
| `obsidian-vault/index/by_method/method_index.md` | List of normalized method families |
| `obsidian-vault/index/by_method/<method>.md` | Papers mapped to this method family |
| `obsidian-vault/index/by_dataset/dataset_index.md` | List of all datasets |
| `obsidian-vault/index/by_dataset/<dataset>.md` | Papers that use or report this dataset |
| `obsidian-vault/index/by_venue/venue_index.md` | List of all venues |
| `obsidian-vault/index/by_venue/<venue>.md` | Papers for one venue, grouped by year |
| `obsidian-vault/index/by_year/year_index.md` | List of all years |
| `obsidian-vault/index/by_year/<year>.md` | Papers for one year |
| `obsidian-vault/index/domain/T__<name>.md` | Generated task/domain graph pages |
| `obsidian-vault/index/domain/_overview.md` | Generated domain/task/dataset overview |
| `obsidian-vault/index/dataset/D__<name>.md` | Generated dataset graph pages |

Topic, method-family, dataset, venue, and year filenames are sanitized (e.g. spaces -> single space, unsafe chars -> underscore). Exact method names remain in `index.jsonl` under `methods`; method navigation uses the lower-cardinality `method_groups` field.

## obsidian-vault/index page frontmatter

- `type: paper-index`
- `dimension: all | topic | method | dataset | venue | year`
- Optional: `topic:`, `method:`, `dataset:`, `venue:`, `year:`
- `generated: <ISO date>`

## obsidian-vault/analysis note frontmatter

- **Strong indexing signal**: `pdf_ref` (path like `obsidian-vault/paperPDFs/.../file.pdf` or `paperPDFs/.../file.pdf`). Notes can still be indexed when other clear paper evidence exists, such as `type: paper`, title/venue/year, method/dataset metadata rows, or venue/year path hints.
- **Display/navigation**: title, venue, year, tags, aliases
- **Research/citation**: core_operator, primary_logic (optional; string or multi-line scalar)
- **Optional**: created, updated, status, note

Tags are flat lists of short English slugs/phrases. Do not write `category`, `modalities`, or `frontier` frontmatter fields in new analysis notes.

## obsidian-vault/analysis note body structure

- Quick Links & TL;DR (Summary, Key Performance)
- Part I / Part II / Part III headings follow `analysis_language` in `AGENTS.md`
  - `zh`: `## Part I：问题与挑战`, `## Part II：方法与洞察`, `## Part III：证据与局限`, `### 核心直觉`
  - `en`: `## Part I: Problem & Challenge`, `## Part II: Method & Insight`, `## Part III: Evidence & Limits`, `### The "Aha!" Moment`
- Legacy notes may still use older mixed headings such as `The "Skill" Signature` or `Technical Deep Dive`
- Local Reading (link/embed to PDF)

## Relationship

- obsidian-vault/index pages **link to** obsidian-vault/analysis notes via `[[obsidian-vault/analysis/.../file.md|...]]` and to PDFs via `[[obsidian-vault/paperPDFs/.../file.pdf|PDF]]`.
- obsidian-vault/analysis notes are **not** modified by the collection build; they are only read (frontmatter + path) to build the index.
- Generated index files are local artifacts. In the public repository, an empty
  `index.jsonl` after a fresh clone is expected until paper rows or analysis
  notes are added.
