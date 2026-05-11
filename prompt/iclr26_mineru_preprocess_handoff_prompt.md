# ICLR 2026 MinerU Raw Artifact Handoff Prompt

你正在接力 ResearchFlow 的 ICLR 2026 PDF 预处理任务。目标是运行 MinerU CLI 并保存原始产物；不要把 PostgreSQL 当成 MinerU 原始产物存储。

## Hard Constraints

- 原始 MinerU 产物写入 `_private/iclr26_batch/mineru_outputs/<batch_id>/<openreview_forum_id>/`。
- PostgreSQL 只允许作为后续可选索引/状态层；它不是 `.md`、`content_list.json`、布局 PDF、图片等原始产物的存储位置。
- `paperAnalysis/`、`paperCollection/`、`obsidian-vault/` 是导出视角，不要写它们。
- 只能运行 `researchflow-backend/scripts/run_iclr26_mineru_raw_batch.py` 做本任务。
- 不要运行 `researchflow-backend/scripts/preprocess_iclr26_mineru_batch.py`，除非人工明确要求追加 DB L2 索引。
- 禁止运行 `researchflow-backend/scripts/run_iclr26_batch.py`。
- 禁止运行 `IngestWorkflow.run_for_existing_paper()`、analysis_agent、writer_agent、export_vault。
- 如果后续人工要求 DB L2 索引，L2 必须是 MinerU-only：`model_name=mineru_only`、`parsers_used=['mineru']`、`formula_source=mineru`。
- `ALLOW_LLM_IMAGE_UPLOAD=false`。
- 每个 agent 只处理分配给自己的一个 batch，避免并发写同一批 paper。

## Common Command Template

```bash
cd /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/researchflow-backend

ALLOW_LLM_IMAGE_UPLOAD=false PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/rf_pycache \
conda run -n RF python scripts/run_iclr26_mineru_raw_batch.py \
  --batch-manifest ../_private/iclr26_batch/manifests/batch_000X_pdfs.jsonl \
  --batch-id iclr26_000X \
  --output-root ../_private/iclr26_batch/mineru_outputs \
  --resume
```

将 `000X` 替换为你的 batch 编号。

## Batch Assignments

### batch_0001

- contract: `_private/iclr26_batch/contracts/batch_0001.md`
- manifest: `_private/iclr26_batch/manifests/batch_0001_pdfs.jsonl`
- raw artifact output: `_private/iclr26_batch/mineru_outputs/iclr26_0001/`
- progress output: `_private/iclr26_batch/reports/mineru_raw_batch_0001_progress.jsonl`
- summary output: `_private/iclr26_batch/reports/mineru_raw_batch_0001_summary.json`

Command:

```bash
cd /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/researchflow-backend

ALLOW_LLM_IMAGE_UPLOAD=false PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/rf_pycache \
conda run -n RF python scripts/run_iclr26_mineru_raw_batch.py --batch-manifest ../_private/iclr26_batch/manifests/batch_0001_pdfs.jsonl --batch-id iclr26_0001 --output-root ../_private/iclr26_batch/mineru_outputs --resume
```

### batch_0002

- contract: `_private/iclr26_batch/contracts/batch_0002.md`
- manifest: `_private/iclr26_batch/manifests/batch_0002_pdfs.jsonl`
- raw artifact output: `_private/iclr26_batch/mineru_outputs/iclr26_0002/`
- progress output: `_private/iclr26_batch/reports/mineru_raw_batch_0002_progress.jsonl`
- summary output: `_private/iclr26_batch/reports/mineru_raw_batch_0002_summary.json`

Command:

```bash
cd /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/researchflow-backend

ALLOW_LLM_IMAGE_UPLOAD=false PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/rf_pycache \
conda run -n RF python scripts/run_iclr26_mineru_raw_batch.py --batch-manifest ../_private/iclr26_batch/manifests/batch_0002_pdfs.jsonl --batch-id iclr26_0002 --output-root ../_private/iclr26_batch/mineru_outputs --resume
```

### batch_0003

- contract: `_private/iclr26_batch/contracts/batch_0003.md`
- manifest: `_private/iclr26_batch/manifests/batch_0003_pdfs.jsonl`
- raw artifact output: `_private/iclr26_batch/mineru_outputs/iclr26_0003/`
- progress output: `_private/iclr26_batch/reports/mineru_raw_batch_0003_progress.jsonl`
- summary output: `_private/iclr26_batch/reports/mineru_raw_batch_0003_summary.json`

Command:

```bash
cd /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/researchflow-backend

ALLOW_LLM_IMAGE_UPLOAD=false PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/rf_pycache \
conda run -n RF python scripts/run_iclr26_mineru_raw_batch.py --batch-manifest ../_private/iclr26_batch/manifests/batch_0003_pdfs.jsonl --batch-id iclr26_0003 --output-root ../_private/iclr26_batch/mineru_outputs --resume
```

### batch_0004

- contract: `_private/iclr26_batch/contracts/batch_0004.md`
- manifest: `_private/iclr26_batch/manifests/batch_0004_pdfs.jsonl`
- raw artifact output: `_private/iclr26_batch/mineru_outputs/iclr26_0004/`
- progress output: `_private/iclr26_batch/reports/mineru_raw_batch_0004_progress.jsonl`
- summary output: `_private/iclr26_batch/reports/mineru_raw_batch_0004_summary.json`

Command:

```bash
cd /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/researchflow-backend

ALLOW_LLM_IMAGE_UPLOAD=false PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/rf_pycache \
conda run -n RF python scripts/run_iclr26_mineru_raw_batch.py --batch-manifest ../_private/iclr26_batch/manifests/batch_0004_pdfs.jsonl --batch-id iclr26_0004 --output-root ../_private/iclr26_batch/mineru_outputs --resume
```

## Success Criteria

- summary JSON has `failed_count = 0` or every failure is explicitly listed with reason.
- each successful paper has raw MinerU artifacts under `_private/iclr26_batch/mineru_outputs/<batch_id>/<openreview_forum_id>/`.
- each successful paper has at least one `.md` and one `*content_list*.json` in that raw output directory.
- no `run_iclr26_batch.py` process was started.
- no L4/report/export was generated by this preprocessing task.

If a PDF cannot produce valid raw MinerU artifacts after one retry, leave it in the summary as failed and stop that paper; do not use PyMuPDF fallback.
