<p align="center">
  <img src="./assets/LOGO.png" alt="ResearchFlow logo" width="280"/>
</p>

<h1 align="center">ResearchFlow</h1>

<p align="center"><strong>Structured Paper Analysis and Research Memory for Knowledge-Grounded Research Agents</strong></p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README_CN.md">中文</a>
</p>

<p align="center">
  <img alt="Semi-automated" src="https://img.shields.io/badge/Semi--automated-Research%20Workflow-1f6feb?style=flat-square"/>
  <img alt="Markdown first" src="https://img.shields.io/badge/Markdown--first-Local%20Files-0f766e?style=flat-square"/>
  <img alt="Knowledge base" src="https://img.shields.io/badge/Local-Knowledge%20Base-0891b2?style=flat-square"/>
  <img alt="MinerU powered" src="https://img.shields.io/badge/MinerU-PDF%20Parsing-0891b2?style=flat-square"/>
  <img alt="Claude Code compatible" src="https://img.shields.io/badge/Claude%20Code-compatible-d97706?style=flat-square"/>
  <img alt="Codex CLI compatible" src="https://img.shields.io/badge/Codex%20CLI-compatible-7c3aed?style=flat-square"/>
  <img alt="Obsidian optional" src="https://img.shields.io/badge/Obsidian-optional-475569?style=flat-square"/>
  <img alt="MIT license" src="https://img.shields.io/badge/License-MIT-111827?style=flat-square"/>
</p>

> 🔥 **ResearchFlow Community** | **[💬 WeChat / ResearchFlow WeChat Group](./WECHAT.md)**

---

> 🧠 **Knowledge first, not execution first.** Many AI research tools focus on
> helping you run experiments or draft papers. ResearchFlow focuses on the
> upstream question: **when an agent makes a research decision, does it have
> enough structured, searchable paper evidence in hand?**
>
> 🧩 **Turn structured paper analysis into reusable research memory.**
> ResearchFlow organizes paper PDFs and paper lists into a local knowledge base:
> structured analysis notes, lightweight indexes, Obsidian-friendly navigation
> pages, and downstream idea or review notes.
>
> 🪶 **Local-first with low lock-in.** The default workflow is **local files
> only**: PDFs, Markdown notes, JSONL indexes, and idea notes all live under
> `obsidian-vault/`. Normal use does not require an API server, database, or
> service deployment.

💡 _ResearchFlow is a methodology and local knowledge workflow, not a closed
platform. The valuable artifact is the research memory you keep accumulating._

## 🔭 Current Goals

- [X] Release a stronger paper analysis template for structured, comparable,
  and reusable paper understanding.
- [ ] Improve automation from candidate papers to a maintained index.
- [ ] Release a high-quality paper analysis knowledge base for
  human-in-the-loop research.
- [ ] Improve structured metadata for retrieval, filtering, and cross-paper
  comparison.

## 🎯 More Than A Prompt: A Knowledge Pipeline

Give ResearchFlow a research direction, and it helps you build the knowledge
base step by step:

```text
collect candidate papers / import local PDFs
  -> download when needed
  -> MinerU PDF parse
  -> structured paper analysis
  -> index
  -> query / ideate / review / export
```

### Formal Analysis Chain

- MinerU parses each PDF once; existing extraction is reused when available.
- Parsed Markdown is chunked, then chunk-level anchor extraction collects
  grounded evidence instead of summarizing the full paper at once.
- Main analysis merges anchors, compact paper context, and figure/table data
  into verified JSON.
- Section writers generate the seven report sections from verified evidence.
- Vault export, figure placement, index refresh, and audit steps are
  deterministic local checks where applicable.

For stage-by-stage details, reasoning settings, validation rules, and measured
cost/latency, see [Formal Local Analysis Chain](docs/formal-analysis-chain.md).

You can use it in four common modes:

| Mode     | Purpose                                                                                   | Typical entry                                                                   |
| -------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Build    | Collect candidates, download PDFs, analyze papers, and refresh the index                  | `research-workflow`                                                           |
| Query    | Retrieve papers by topic, task, method, venue, year, title, or technique tags             | `papers-query-knowledge-base`                                                 |
| Decision | Compare methods before choosing baselines, changing a design, or writing related work     | `papers-query-knowledge-base`                                                 |
| Idea     | Generate, focus, and stress-test research directions grounded in the local knowledge base | `research-brainstorm-from-kb`, `idea-focus-coach`, `reviewer-stress-test` |

ResearchFlow is useful when you want to:

- Build a topic-specific paper knowledge base from web pages, GitHub paper
  lists, or local PDF folders.
- Convert PDFs into structured notes with comparable fields, evidence anchors,
  formulas, tables, figure/table metadata, and reading-order context.
- Compare methods before selecting baselines, writing related work, or changing
  a research design.
- Generate research ideas, focus them into executable plans, and stress-test
  them from a reviewer perspective.
- Export share-ready Markdown or browse the knowledge base in Obsidian.

## 🏗️ Three-Layer Architecture

```text
┌─────────────────────────────────────────────────────────┐
│  Output layer        obsidian-vault/ideas/              │
│                      ideas, plans, review notes          │
├─────────────────────────────────────────────────────────┤
│  Index layer         obsidian-vault/index/              │
│                      JSONL index + Obsidian pages        │
├─────────────────────────────────────────────────────────┤
│  Evidence layer      obsidian-vault/analysis/           │
│                      structured notes + logs             │
│                      obsidian-vault/paperPDFs/           │
│                      source PDFs                         │
└─────────────────────────────────────────────────────────┘
```

- `obsidian-vault/paperPDFs/` stores the source PDFs.
- `obsidian-vault/analysis/` stores per-paper analysis notes and logs. This is
  the main evidence layer agents should read.
- `obsidian-vault/index/` stores generated retrieval indexes and
  navigation pages. At scale, agents should start from `index.jsonl`, filter
  candidates, then read matching analysis notes.
- `obsidian-vault/ideas/` stores downstream research outputs such as brainstorm
  notes, focused plans, reviewer critiques, and daily logs.
- Obsidian is optional. It is only a browsing and backlink layer; the repository
  still works as a normal local folder.

## 🤖 Agent Compatibility

ResearchFlow intentionally stays plain: folders, Markdown, JSONL, CSV, and
`SKILL.md`. The same research memory can therefore be shared by multiple agents:

- Claude Code / Cursor can read `.claude/skills` directly.
- Codex CLI can use `scripts/setup_shared_skills.py` to generate local aliases.
- Other agents that can read files can read `obsidian-vault/index/index.jsonl`
  and `obsidian-vault/analysis/` directly, without special integration.

## 🚀 Quick Start

ResearchFlow is used across macOS, Windows, and Linux. The default analysis
workflow does not require OS-specific tools such as `jq`, `curl`, or `make`.
PDF helper libraries such as Poppler and Ghostscript are already declared in the
Conda environment, so the README does not list OS-specific installation steps.

### 1. Create the conda environment

```bash
git clone https://github.com/<your-username>/ResearchFlow.git
cd ResearchFlow

conda env create -f environment/environment.yml
conda activate researchflow
```

### 2. Configure model and parser access

Most local operations work without a checked-in config file. When you need to
set model keys, model names, or parser overrides, create a repo-root `.env` and
use [environment/.env.example](environment/.env.example) as a reference. Do not
put secrets into `.env.example`.

Common OpenAI-compatible variables:

```dotenv
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
```

### 3. Install or configure MinerU

MinerU is the recommended parser for formal paper analysis. Ask the agent to
install, configure, and verify MinerU for your machine instead of following a
long manual setup in the README.

Minimal verification: `mineru --help` should run, or `.env` should set
`MINERU_CLI_PATH` to the MinerU executable.

### 4. Prepare agent skills

Claude Code and Cursor can read `.claude/skills` directly. For Codex-compatible
skill paths, generate local aliases:

```bash
python3 scripts/setup_shared_skills.py
```

Then start from the workflow skill:

```text
/research-workflow
I want to build a knowledge base for controllable motion generation from PDFs.
Please tell me the next step and the expected outputs.
```

The default workflow does not require starting any service. Use the local
folders under `obsidian-vault/` as the working state.

## 📖 Usage Examples

Build a topic knowledge base from scratch:

```text
/research-workflow
I want to build a knowledge base for text-driven reactive motion generation.
Start by collecting candidate papers and tell me which skill to use at each stage.
```

Collect candidate papers from a GitHub paper list:

```text
/papers-collect-from-github-repo
Collect papers related to controllable human motion generation from this GitHub repository: <URL>
Keep only items related to diffusion, controllability, real-time generation, or long-form motion.
Write a candidate list suitable for the downstream download workflow.
```

Import PDFs from a local folder:

```text
/research-workflow
I already have PDFs under /path/to/pdf-folder.
Please register them under obsidian-vault/paperPDFs/ using category Motion_Generation,
venue CVPR, and year 2026, then tell me which paper to analyze first.
```

Download PDFs from a curated candidate list:

```text
/papers-download-from-list
Download the papers that are still marked as Wait in the current candidate list.
Report successful downloads, failures, and skipped items.
```

Generate a deep report for a prepared PDF:

```text
/paper-report
Generate a deep report for obsidian-vault/paperPDFs/<Category>/<Venue_Year>/<Paper>.pdf.
Save the report under obsidian-vault/analysis/ with source anchors preserved.
```

Run the formal local analysis chain directly when you need the actual pipeline
artifacts and figure/table-aware vault export:

```bash
python3 scripts/run_local_paper_analysis.py \
  --pdf "obsidian-vault/paperPDFs/<Category>/<Venue_Year>/<Paper>.pdf" \
  --conf-year "<Venue_Year>" \
  --export-vault
```

If MinerU output already exists, reuse it instead of reparsing:

```bash
python3 scripts/run_local_paper_analysis.py \
  --mineru-output "<mineru_output_dir>" \
  --paper-pdf "obsidian-vault/paperPDFs/<Category>/<Venue_Year>/<Paper>.pdf" \
  --conf-year "<Venue_Year>" \
  --export-vault
```

For a normalized MinerU cache, keep one paper output per directory and let the
runner discover it from the PDF stem:

```bash
python3 scripts/run_local_paper_analysis.py \
  --pdf "obsidian-vault/paperPDFs/<Category>/<Venue_Year>/<Paper>.pdf" \
  --conf-year "<Venue_Year>" \
  --mineru-output-root "<mineru_output_root>" \
  --require-existing-mineru-output \
  --export-vault
```

For controlled experiments, keep the real venue/year metadata and redirect only
the Markdown note path with `--vault-note-dir`.

The formal local runner is the default analysis route for pipeline artifacts.

Analyze a batch from a paper list:

```bash
python3 scripts/run_paper_list_analysis.py \
  --source obsidian-vault/paper_list.csv \
  --state Downloaded \
  --limit 25 \
  --mineru-output-root "<mineru_output_root>" \
  --require-existing-mineru-output
```

For larger runs, split the list with `papers-batch-analyze` and run up to four
worker agents in parallel.

For long-running runs where agent disconnection is a bigger risk than automatic
repair, run four script-only shards instead. Each process writes its own queue
results and its own analysis work directory:

```bash
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
for shard in 0 1 2 3; do
  python3 scripts/run_paper_list_analysis.py \
    --source obsidian-vault/paper_list.csv \
    --state Downloaded \
    --run-id "${RUN_ID}_shard${shard}" \
    --shard-index "$shard" \
    --shard-count 4 \
    --analysis-output-root "_private/local_analysis_runs/${RUN_ID}_shard${shard}" \
    --mineru-output-root "_private/iclr26_batch/mineru_outputs" \
    --require-existing-mineru-output \
    > "_private/local_analysis_runs/${RUN_ID}_shard${shard}.log" 2>&1 &
done
wait
```

After the scripts finish, inspect `obsidian-vault/batches/<run_id>/summary.json`
and `results.jsonl`, then run post-hoc repair or index refresh.

Refresh the index manually when needed:

```bash
python3 .claude/skills/papers-build-index/scripts/build_paper_index.py
```

The generated home page is `obsidian-vault/index/paper_index.md`. The tracked
`obsidian-vault/index/README.md` remains a public placeholder and is not
overwritten by the builder.

To verify the index/workflow chain on your machine without using private paper
data:

```bash
python3 scripts/smoke_index_workflow.py
```

Ask a literature question:

```text
/papers-query-knowledge-base
Compare DART, OmniControl, and MoMask for long-horizon controllable generation.
Focus on representation design, control interface, and experimental evidence.
```

Generate an idea grounded in your local knowledge base:

```text
/research-brainstorm-from-kb
I want to study text-driven reactive motion generation.
Propose 3 directions grounded in the papers already analyzed.
```

Narrow an idea into an executable plan:

```text
/idea-focus-coach
My idea is to use a diffusion model for reactive motion generation,
but I am not sure how large the scope should be or what the first experiment should be.
Please narrow it into an executable MVP.
```

Pressure-test an idea:

```text
/reviewer-stress-test
Review my idea from the perspective of an ICLR reviewer:
[paste the idea description or point to a file under obsidian-vault/ideas/]
Focus on novelty, experimental design, and differentiation from SOTA.
```

## ✨ Core Capabilities

The maintained skill library lives in `.claude/skills`.

| Need                                       | Skill                               |
| ------------------------------------------ | ----------------------------------- |
| Decide the next pipeline step              | `research-workflow`               |
| Import PDFs from a local folder            | Provide the folder path to `research-workflow` |
| Collect candidates from web pages          | `papers-collect-from-web`         |
| Collect candidates from GitHub paper lists | `papers-collect-from-github-repo` |
| Download PDFs from a triage list           | `papers-download-from-list`       |
| Generate a deep single-paper report        | `paper-report`                 |
| Rebuild the local index                    | `papers-build-index`              |
| Query or compare papers from local notes   | `papers-query-knowledge-base`     |
| Generate grounded research ideas           | `research-brainstorm-from-kb`     |
| Focus an idea into an executable plan      | `idea-focus-coach`                |
| Run reviewer-style stress tests            | `reviewer-stress-test`            |
| Export share-ready Markdown                | `notes-export-share-version`      |

See [.claude/skills/README.md](.claude/skills/README.md) for the full skill map.

## Repository Structure

```text
ResearchFlow/
├── .claude/skills/                 maintained agent skill library
├── assets/                         public logo and README assets
├── environment/                    conda, dotenv, and local Python tooling files
├── linkedCodebases/                optional links to related local codebases
├── obsidian-vault/
│   ├── paperPDFs/                  source PDFs for analysis
│   ├── analysis/                   structured per-paper analysis notes
│   ├── index/                      generated JSONL index and navigation pages
│   └── ideas/                      ideas, plans, reviews, and logs
├── scripts/                        setup, maintenance, and audit utilities
├── AGENTS.md                       agent-facing local workflow rules
├── README.md                       English entry point
└── README_CN.md                    Chinese entry point
```

Generated corpora, private notes, local credentials, caches, and large research
artifacts should stay out of Git.

## Advanced Config

`<a id="codex-cli-compat"></a>`

<details>
<summary>Codex CLI compatibility</summary>

Claude Code / Cursor does not need this step. Codex CLI does.

The repository does not track `.codex/`. After clone, generate
`.codex/skills` and `.codex/skills-config.json` locally:

```bash
python3 scripts/setup_shared_skills.py
```

Verify aliases without changing them:

```bash
python3 scripts/setup_shared_skills.py --check
```

</details>

`<a id="obsidian-config"></a>`

<details>
<summary>Obsidian setup</summary>

- Obsidian is optional but strongly recommended. It is only a visualization layer.
- Open `obsidian-vault/` as an Obsidian vault if you want graph view,
  backlinks, and manual browsing.
- Do not treat Obsidian pages as a separate source of truth; they are local
  files generated or maintained by the workflow.

</details>

ResearchFlow currently supports the local file workflow through the conda
environment and local commands only.

## Data Hygiene

- Keep `.env` local and commit `environment/.env.example` only.
- Keep PDFs, generated analysis notes, generated indexes, vault pages, caches,
  model outputs, and private experiments out of source history unless you are
  intentionally publishing a curated example.
- Preserve the standard `obsidian-vault/` layout so agents and scripts can find
  the expected inputs and outputs.
- Avoid mixing unrelated paper sets in the same category unless you want
  them retrieved together.
- Run a sensitive-token scan before publishing a fork or release.

## Citation

If ResearchFlow helps your research, please cite the repository directly:

```bibtex
@misc{lin2026researchflow,
  title        = {{ResearchFlow}: A Structured Paper Analysis Framework for Knowledge-Grounded Research},
  author       = {Jingzhong Lin and Ziheng Huang},
  year         = {2026},
  howpublished = {\url{https://github.com/RipeMangoBox/ResearchFlow}},
  note         = {GitHub repository}
}
```

## License

MIT
