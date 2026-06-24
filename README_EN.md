<p align="center">
  <img src="./assets/paperbite_icon.png" alt="BITE logo" width="240"/>
</p>

<h1 align="center">BITE</h1>

<p align="center"><strong>Bibliographic Intelligence for Thought Emergence</strong></p>

<p align="center"><strong>Let every idea have a <mark>source</mark>, and every judgment have an <mark>anchor</mark>.</strong></p>

<p align="center">
  <a href="README.md">中文</a> |
  <a href="README_EN.md">English</a>
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

> 🔥 **BITE Community** | **[💬 WeChat / BITE WeChat Group](./WECHAT.md)**
>
> 🔥 **News**: BITE's public evidence layer is published on HuggingFace dataset [PaperBite-Assets](https://huggingface.co/datasets/RipeMangoBox/PaperBite-Assets), covering `L0-L3` structured paper assets (Markdown analysis notes + figures + manifests). Incrementally sync with `scripts/sync_assets_from_hf.py`; if you work on AI-related research, it is a strong starting point for building your own evidence vault.

---

<p align="center">
  <img src="./assets/bite-core-slide-3-en.png" alt="BITE core idea in English" width="720"/>
</p>

> **What is BITE?** BITE is a local-first workflow framework for structured paper analysis and research memory, purpose-built for knowledge-grounded research agents. It transforms paper analysis into structured notes and builds a persistent, reusable research memory.

> **Who is this for?** Researchers building paper-grounded knowledge bases,
> agent-assisted literature workflows, or evidence-backed idea generation.

> 🧠 **Knowledge first, not execution first.** Many AI research tools focus on
> helping you run experiments or draft papers. BITE focuses on the
> upstream question: **when an agent makes a research decision, does it have
> enough structured, searchable paper evidence in hand?**
>
> 🧩 **Turn structured paper analysis into reusable research memory.**
> BITE organizes paper PDFs and paper lists into layered local assets:
> source literature, single-paper evidence units, domain knowledge surfaces,
> cross-domain evidence accumulation, and downstream idea or experiment records.
>
> 🪶 **Local-first with low lock-in.** The default workflow is local files only:
> PDFs, Markdown notes, JSONL indexes, and idea notes all live under
> `obsidian-vault/`. Normal use does not require a server, database, or service
> deployment.

💡 _BITE is a methodology and local knowledge workflow, not a closed
platform. What matters is the layered research assets you keep accumulating._

## 🧠 Core Idea

BITE is not centered on idea generation in isolation. The core claim is
that research directions should emerge from an accumulated, structured, and
traceable evidence base, then be stress-tested before execution.

## 🗂️ Asset Levels

<p align="center">
  <img src="./assets/bite-asset-levels.png" alt="BITE asset hierarchy" width="480"/>
</p>

This diagram shows BITE's six-layer asset hierarchy: `L0-L3` (knowledge building, powered by PaperBite), `L4` (emergence), and `L5` (validation).

The table below follows the diagram **from bottom to top**:

| Level | Output | Role |
| --- | --- | --- |
| `L0` | paper PDFs | preserve source literature |
| `L1` | single-paper analysis | extract idea, design, and evidence |
| `L2` | Domain Research Vault | support domain-level induction and deduction |
| `L3` | Cross-Domain Research Vault | support transfer and idea emergence |
| `L4` | Idea Vault | emergence layer |
| `L5` | Experiment Vault | validation layer |

## 🎯 How It Works

Give BITE a research direction, and it helps you build the knowledge
base step by step:

```text
collect candidate papers / import local PDFs
  -> download when needed
  -> integrated analysis chain
     (MinerU parse/reuse -> structured analysis -> vault export)
  -> optional index refresh
  -> query / ideate / review / export
```

You can use it in four common modes:

| Mode | Purpose | Typical entry |
| --- | --- | --- |
| Build | Collect candidates, download or import PDFs, run the integrated analysis chain, and refresh the index when needed | `research-workflow` |
| Query | Retrieve papers by topic, task, method, venue, year, title, or technique tags | `papers-query-knowledge-base` |
| Decision | Compare methods before choosing baselines, changing a design, or writing related work | `papers-query-knowledge-base` |
| Idea | Generate, focus, and stress-test research directions grounded in the local knowledge base | `research-brainstorm-from-kb`, `idea-focus-coach`, `reviewer-stress-test` |

## 🛠️ Environment Setup

### 📦 1. Create the conda environment

```bash
git clone https://github.com/<your-username>/BITE.git
cd BITE
conda env create -f environment/environment.yml
conda activate bite
```

### 🔐 2. Configure model and parser access

Create a repo-root `.env` when you need model keys, model names, or parser
overrides. Use [environment/.env.example](environment/.env.example) as a
reference.

### 📄 3. Install or configure MinerU

MinerU is the PDF parsing component inside BITE's local analysis chain. You no
longer need a separate MinerU batch-preparation phase before analysis:
`scripts/run_local_paper_analysis.py` can call MinerU during analysis, or reuse
existing parse outputs when you already have them. Minimal verification:
`mineru --help` should run, or `.env` should set `MINERU_CLI_PATH`.

## 🧭 Usage

### 🧠 1. Start from the workflow skill

```text
/research-workflow
I want to build a knowledge base for controllable motion generation from PDFs.
Please tell me the next step and the expected outputs.
```

### 📥 2. Optional: Sync public evidence layer

To use BITE's pre-built structured paper assets, sync from HuggingFace by layer:

```bash
pip install huggingface_hub

# Text only: analysis notes + indexes (~43 MB)
python scripts/sync_assets_from_hf.py --mode text

# Assets only: figures and tables (~1.8 GB)
python scripts/sync_assets_from_hf.py --mode assets

# Everything (default)
python scripts/sync_assets_from_hf.py --mode all --dry-run   # preview first
python scripts/sync_assets_from_hf.py                        # full sync

# Explicitly replace your local paper list with the public PaperBite list
python scripts/sync_assets_from_hf.py --mode paper-list --overwrite-paper-list
```

PaperBite shards use vault-relative paths (`analysis/`, `index/`, and
`assets/`) and extract directly under `obsidian-vault/`. This makes them
suitable as a drop-in public evidence vault for BITE. `paper_list.csv` is synced
only when explicitly requested, so your local paper list is not overwritten by
default. The public assets do not include the full original PDF corpus; keep
downloading or importing `paperPDFs/` locally when PDFs are needed.

### ⚙️ 3. Run the integrated local analysis chain

For a single paper, start directly from the PDF. The runner performs MinerU
parse or cache reuse, chunk evidence extraction, main analysis JSON generation,
section writing, figure/table placement, vault export, and structural
validation. Pass `--mineru-output` or `--mineru-output-root` only when you
already have parse outputs to reuse.

```bash
python3 scripts/run_local_paper_analysis.py \
  --pdf "obsidian-vault/paperPDFs/<Venue_Year>/<Paper>.pdf" \
  --conf-year "<Venue_Year>" \
  --export-vault
```

## 📚 Further Reading

- [Asset Architecture](docs/asset-architecture.md)
- [System Architecture](docs/system-architecture.md)
- [Formal Local Analysis Chain](docs/formal-analysis-chain.md)

## 📖 Usage Examples

<details>
<summary>Build a topic knowledge base from scratch</summary>

```text
/research-workflow
I want to build a knowledge base for text-driven reactive motion generation.
Start by collecting candidate papers and tell me which skill to use at each stage.
```

</details>

<details>
<summary>Collect candidate papers from a GitHub paper list</summary>

```text
/papers-collect-from-github-repo
Collect papers related to controllable human motion generation from this GitHub repository: <URL>
Keep only items related to diffusion, controllability, real-time generation, or long-form motion.
Write a candidate list suitable for the downstream download workflow.
```

</details>

<details>
<summary>Run the formal local analysis chain</summary>

Run the full chain directly from a PDF:

```bash
python3 scripts/run_local_paper_analysis.py \
  --pdf "obsidian-vault/paperPDFs/<Venue_Year>/<Paper>.pdf" \
  --conf-year "<Venue_Year>" \
  --export-vault \
  --reasoning-effort max \
  --part-thinking disabled \
  --writer-thinking disabled
```

Reuse existing MinerU output when available:

```bash
python3 scripts/run_local_paper_analysis.py \
  --mineru-output "<mineru_output_dir>" \
  --paper-pdf "obsidian-vault/paperPDFs/<Venue_Year>/<Paper>.pdf" \
  --conf-year "<Venue_Year>" \
  --export-vault
```

For batch analysis, the queue runner calls the same formal chain per row:

```bash
python3 scripts/run_paper_list_analysis.py \
  --source obsidian-vault/paper_list.csv \
  --state Downloaded \
  --jobs 2 \
  --export-vault
```

</details>

## ✨ Core Capabilities

| Need | Skill |
| --- | --- |
| Decide the next pipeline step | `research-workflow` |
| Collect candidates from web pages | `papers-collect-from-web` |
| Collect candidates from GitHub paper lists | `papers-collect-from-github-repo` |
| Download PDFs from a triage list | `papers-download-from-list` |
| Generate a deep single-paper report | `paper-report` |
| Rebuild the local index | `papers-build-index` |
| Query or compare papers from local notes | `papers-query-knowledge-base` |
| Generate grounded research ideas | `research-brainstorm-from-kb` |
| Focus an idea into an executable plan | `idea-focus-coach` |
| Run reviewer-style stress tests | `reviewer-stress-test` |
| Export share-ready Markdown | `notes-export-share-version` |

See [.claude/skills/README.md](.claude/skills/README.md) for the full skill map.

## 🤖 Agent Compatibility

BITE intentionally stays plain: folders, Markdown, JSONL, CSV, and
`SKILL.md`. The same research memory can therefore be shared by multiple agents:

- Claude Code / Cursor can read `.claude/skills` directly.
- Codex CLI can use `scripts/setup_shared_skills.py` to generate local aliases.
- Other agents can read `obsidian-vault/index/index.jsonl` and
  `obsidian-vault/analysis/` directly.

## Advanced Config

<details>
<summary>Codex CLI compatibility</summary>

Claude Code / Cursor does not need this step. Codex CLI does.

```bash
python3 scripts/setup_shared_skills.py
python3 scripts/setup_shared_skills.py --check
```

</details>

<details>
<summary>Obsidian setup</summary>

- Obsidian is optional but recommended as a visualization layer.
- Open `obsidian-vault/` as an Obsidian vault if you want graph view,
  backlinks, and manual browsing.
- Do not treat Obsidian pages as a separate source of truth.

</details>
