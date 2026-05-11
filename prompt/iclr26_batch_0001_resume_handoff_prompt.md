# ICLR 2026 Batch 0001 接力 Prompt

你正在接力 ResearchFlow 的 ICLR 2026 batch `iclr26_0001`。当前任务已按用户要求暂停；不要自动继续跑 batch，除非用户明确要求恢复。

## 用户最新决策

1. 只采纳 `resume` 支持。
2. 不采纳其他优化建议：不要继续实现 output splitting、JSON repair pass、降低 analysis scope、timeout、two-pass mode、single-agent rewrite。
3. 架构暂时保持 `analysis_agent + writer_agent` 双 agent。
4. 对“单 agent 是否能解决 handoff/json 问题”的判断：
   - 单 agent 可以减少 agent-to-agent handoff / blackboard 不一致问题。
   - 但不能根本解决当前 malformed JSON，因为主因是 `analysis_agent` 的长结构化 JSON 输出。
   - 如果单 agent 直接输出 Markdown，会绕过 DeltaCard、EvidenceUnit、GraphAssertion 等 DB 入库与验收门，不是等价替换。

## 强约束

- PostgreSQL 是唯一写入 truth target。
- `paperAnalysis/`、`paperCollection/`、`obsidian-vault/` 是导出/只读视角，不要把它们当 source of truth。
- Formal L2 必须是 MinerU-only：
  - `model_name = mineru_only`
  - `parsers_used = ["mineru"]`
  - `formula_source = mineru`
- DeepSeek/DS 当前为 text-only，不上传图片：
  - `ALLOW_LLM_IMAGE_UPLOAD=false`
- 不要启动 `batch_0002`，直到 `batch_0001` 完成导出并经过人工 Markdown review。
- 如果分析 Markdown 无法写入磁盘，必须停止任务并告知用户。

## 当前状态

- batch_id: `iclr26_0001`
- runner: 已停止
- progress 文件: `_private/iclr26_batch/reports/batch_0001_progress.jsonl`
- selected_total: `25`
- processed_with_progress: `8`
- succeeded_l4_report: `4`
- needs_repair: `4`
- Markdown export: 尚未到达
- Markdown write failure: 未观察到

## PDF 检索结果

已完成 ICLR 2026 PDF 路径检索并写入文档：

- manifest: `_private/iclr26_batch/manifests/discovered_pdfs.jsonl`
- report: `_private/iclr26_batch/reports/pdf_discovery_report.md`
- contract: `_private/iclr26_batch/contracts/batch_0001.md`

关键数字：

- deduplicated verified PDFs: `9971`
- with OpenReview forum id: `5348`
- selected in `batch_0001`: `25`
- skipped because missing PDF in resmax manifest: `123`

## 已处理 8 篇结果

| # | Paper ID | Status | L2 figures | Note |
|---|---|---:|---:|---|
| 1 | `57c6800b-45b0-4c4a-8731-b8eee1acebf8` | needs_repair | 16 | `analysis_agent_output_missing`; invalid JSON |
| 2 | `cb135b08-a5e2-44a9-b03a-d37d42003b03` | succeeded | 24 | L4/report passed |
| 3 | `8a4f9d14-37dd-49dc-bb2c-87f1a8721d8b` | succeeded | 15 | L4/report passed |
| 4 | `4a2eed43-3e9a-417a-b751-ac9d5d426cd2` | succeeded | 49 | L4/report passed |
| 5 | `b25a0a3e-4bdb-45cf-acc7-1682e546f8ce` | needs_repair | 38 | `analysis_agent_output_missing`; invalid JSON |
| 6 | `a3085587-c3c4-47bd-81c4-50f8d9cd2408` | succeeded | 36 | L2 retry succeeded; L4/report passed |
| 7 | `8ac34250-95ad-4d69-ab4b-48b418d3f586` | needs_repair | 20 | `analysis_agent_output_missing`; invalid JSON |
| 8 | `7f7ece6d-c621-4b37-84d0-7b0f3f2ca10c` | needs_repair | 16 | `analysis_agent_output_missing`; invalid JSON |

## 耗时定位

来自暂停报告的 DB agent-run timing：

| Agent | Status | Runs | Avg seconds | Total seconds |
|---|---:|---:|---:|---:|
| `analysis_agent` | failed | 4 | 254.8 | 1019.3 |
| `analysis_agent` | success | 4 | 197.6 | 790.4 |
| `writer_agent` | success | 4 | 46.9 | 187.4 |

结论：耗时大头是 `analysis_agent`，尤其是失败 JSON 输出会在约 4 分钟后才进入 `needs_repair`。

## 已完成代码/文档变更

主要文件：

- `researchflow-backend/scripts/run_iclr26_batch.py`
  - 新增 `--resume`
  - 读取 progress JSONL，跳过已有终态结果
  - 终态状态：`succeeded`、`needs_repair`、`needs_l2_repair`、`quarantined`
  - `--resume` 时复用现有 contract，并校验当前 selected OpenReview id 顺序必须与 contract 一致，避免 batch 选择漂移
- `_private/iclr26_batch/reports/batch_0001_pause_status.md`
  - 已更新为“只采纳 resume，其他建议不采纳”
  - 已写入恢复命令
- `DailySummary/2026-05-10.md`
  - 已写入当天日志，记录 PDF 检索、暂停状态、单 agent 判断、resume 决策

历史上下文中还已有以下相关改动：

- `researchflow-backend/backend/services/parse_service.py`
  - Formal MinerU-only path 不再混入 GROBID
  - metadata 固定为 MinerU-only
  - figure image metadata 增加 `source_path`
- `researchflow-backend/backend/services/agent_runner.py`
  - 已有 JSON parse failure retry 逻辑
- `researchflow-backend/backend/services/ingest_workflow.py`
  - deep ingest 缺少关键 analysis blackboard item 时返回 `needs_repair`
- `researchflow-backend/scripts/discover_iclr26_pdfs.py`
  - 已用于生成 ICLR 2026 PDF discovery manifest/report

## 已验证

语法校验通过：

```bash
PYTHONPYCACHEPREFIX=/tmp/rf_pycache PYTHONNOUSERSITE=1 \
conda run -n RF python -m py_compile researchflow-backend/scripts/run_iclr26_batch.py
```

Resume helper 已确认能识别现有 progress：

```text
progress_rows=8 progress_ids=8 contract_ids=25
```

另一次检查输出：

```text
rows=8 ids=8
statuses=needs_repair,succeeded
```

## 恢复命令

只有当用户明确要求恢复时，才运行：

```bash
cd /home/ripemangobox/Coding/Github/OpenSource/Open_Ready/ResearchFlow/researchflow-backend

DATABASE_URL='postgresql+asyncpg://rf:<password>@127.0.0.1:5432/researchflow' \
ALLOW_LLM_IMAGE_UPLOAD=false PYTHONNOUSERSITE=1 PYTHONPYCACHEPREFIX=/tmp/rf_pycache \
conda run -n RF python scripts/run_iclr26_batch.py \
  --batch-contract ../_private/iclr26_batch/contracts/batch_0001.md \
  --limit 25 --mineru-only --stop-before-human-review --resume
```

预期行为：

- 读取 `_private/iclr26_batch/reports/batch_0001_progress.jsonl`
- 跳过已有 8 个终态 paper
- 继续处理剩余 17 篇
- 结束后执行 export/verify
- 如果任一 paper 出现 `markdown_not_written_to_disk`，脚本会停止并报错

## 接力注意事项

- 不要重跑 discovery，除非用户明确要求。
- 不要清空 progress JSONL。
- 不要手动改 DB 里的 paper analysis/report 状态，除非用户明确要求。
- 不要把 `needs_repair` 的 4 篇强行改成 succeeded。
- 不要启动 `batch_0002`。
- 如果用户只是问状态，汇报当前暂停状态和 resume 命令，不要自动运行。
- 如果用户要求继续，先确认没有残留 runner，再用 `--resume` 命令恢复。
