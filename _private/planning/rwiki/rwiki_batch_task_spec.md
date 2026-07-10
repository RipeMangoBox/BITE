---
created: 2026-04-12
scope: private
purpose: 给 CLI agent 会话的可执行任务 spec
---

# ResearchWiki Batch Task Spec

> 本文件是给 CLI agent（Claude Code / Codex CLI）的执行指令。
> 每个 awesome 仓库一个独立任务块，支持断点续跑。
> 会话上下文快满时，保存进度到 `progress.yaml`，开新会话继续。

---

## 全局约定

### 工作目录

```
ResearchFlow/ResearchWiki/
```

### 输出结构（每个 source）

```
ResearchWiki/sources/<source_id>/
├── snapshots/<commit_sha_or_date>.md   ← README 原文快照
├── source_items.csv                     ← 全量 parse 结果
├── review_queue.csv                     ← 筛选后待审
└── meta.yaml                            ← 运行态元信息
```

### source_items.csv 字段

```csv
item_id,paper_title,venue,year,paper_link,code_link,project_link,source_section,has_code,parse_status,补全_status
```

- `paper_link`：arxiv/openreview/CVF 链接。如果 README 未提供，标记 `parse_status=missing_paper_link`
- `code_link`：GitHub 代码仓库链接
- `project_link`：项目主页
- `has_code`：true/false/unknown
- `parse_status`：`ok` | `missing_paper_link` | `missing_venue` | `ambiguous`
- `补全_status`：`not_needed` | `pending` | `done` | `failed`

### 断点续跑机制

每个 source 的 `meta.yaml` 记录当前进度：

```yaml
source_id: awe_human_motion
last_step: collect          # collect | enrich | filter | download | analyze
last_step_status: done      # done | partial | failed
items_total: 539
items_parsed: 539
items_enriched: 412
items_filtered: 80
items_downloaded: 0
items_analyzed: 0
last_updated: 2026-04-13T02:30
notes: "127 items missing paper_link, enrichment in progress"
```

新会话启动时：读 `meta.yaml`，从 `last_step` 的下一步或 partial 处继续。

---

## Step 定义

### Step 1: collect

1. Fetch awesome 仓库 README（用 WebFetch 或 curl）
2. 保存快照到 `snapshots/<date>.md`
3. 解析 README，提取所有论文条目，写入 `source_items.csv`
4. 每个仓库的 README 格式不同，agent 需要先分析格式再写一次性 parser
5. 标记缺失字段：`missing_paper_link`、`missing_venue` 等

### Step 2: enrich（补全缺失字段）

对 `parse_status != ok` 的条目：

1. 用论文标题搜索 arXiv / Semantic Scholar / Google Scholar
2. 补全 `paper_link`（优先 arxiv）
3. 补全 `venue` + `year`（从论文页面提取）
4. 检查 `code_link` 是否有效（GitHub 404 检测）
5. 更新 `补全_status = done | failed`

**关键**：这一步是最耗时的，需要网络请求。建议：
- 每处理 20 条保存一次 csv
- 失败的标记 `failed` 跳过，不阻塞后续
- 上下文快满时保存进度，记录到 meta.yaml

### Step 3: filter

按 `filter_policy.yaml` 对 `source_items.csv` 全量条目打标，**不删除任何条目**：
1. hard_filter：year_min、venue_whitelist、exclude_keywords → 标记 `filter_result=pass|auto_reject`
2. soft_score：对 pass 的条目打分 → 写入 `score` 列
3. budget_cap：per_sync 限额 → 超出预算的标记 `review_status=deferred`

所有条目（含 auto_reject）都写入 `review_queue.csv`，保留完整记录。
人工审阅时只需关注 `filter_result=pass` 且 `review_status=pending` 的条目，标记 accept/reject/defer。
被 auto_reject 的条目保留在 csv 中，后续可通过 `manual_override=true` 恢复。

### Step 4: download

对 `review_queue.csv` 中 accepted 的条目下载 PDF 到 `paperPDFs/`。

### Step 5: analyze

对已下载的 PDF 执行结构化分析，输出到 `ResearchWiki/papers/`。

---

## 任务清单（按优先级）

### Pilot: awe_human_motion

```yaml
source_id: awe_human_motion
url: https://github.com/Foruck/Awesome-Human-Motion
priority: P0
est_papers: ~539
known_issues:
  - README 格式：按任务分类（Motion Generation, Motion Prediction, ...），每条通常有 paper + code 链接
  - 部分早期论文可能缺 arxiv link
batch: pilot
```

### Batch 1（7 个仓库，并行）

```yaml
- source_id: awe_mllm
  url: https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models
  priority: P1
  est_papers: ~450
  known_issues:
    - 仓库结构复杂，可能有子页面
  batch: 1

- source_id: awe_3dgs
  url: https://github.com/MrNeRF/awesome-3D-gaussian-splatting
  priority: P1
  est_papers: ~509
  known_issues:
    - 可能有外部 paper-list 站点链接
  batch: 1

- source_id: awe_video_diffusion
  url: https://github.com/showlab/Awesome-Video-Diffusion
  priority: P1
  est_papers: ~714
  known_issues:
    - 论文量大，需要严格 budget 控制
  batch: 1

- source_id: awe_llm_reasoning
  url: https://github.com/atfortes/Awesome-LLM-Reasoning
  priority: P1
  est_papers: ~143
  known_issues:
    - 规模较小，可能全量处理
  batch: 1

- source_id: awe_efficient_llm
  url: https://github.com/horseee/Awesome-Efficient-LLM
  priority: P1
  est_papers: ~788
  known_issues:
    - 论文量最大之一，必须严格筛选
  batch: 1

- source_id: awe_embodied_vla
  url: https://github.com/jonyzhang2023/awesome-embodied-vla-va-vln
  priority: P1
  est_papers: 700+
  known_issues:
    - README badge 标注 700+，实际可能更多
  batch: 1

- source_id: awe_agentic_reasoning
  url: https://github.com/weitianxin/Awesome-Agentic-Reasoning
  priority: P1
  est_papers: ~640
  known_issues: []
  batch: 1
```

### Batch 2（6 个仓库）

```yaml
- source_id: awe_world_models
  url: https://github.com/knightnemo/Awesome-World-Models
  priority: P2
  est_papers: ~492
  batch: 2

- source_id: awe_rag
  url: https://github.com/jxzhangjhu/Awesome-LLM-RAG
  priority: P2
  est_papers: ~30
  batch: 2

- source_id: awe_3d_generation
  url: https://github.com/justimyhxu/awesome-3D-generation
  priority: P2
  est_papers: ~110
  batch: 2

- source_id: awe_controllable_video
  url: https://github.com/mayuelala/Awesome-Controllable-Video-Generation
  priority: P2
  est_papers: ~286
  batch: 2

- source_id: awe_speech_llm
  url: https://github.com/ga642381/speech-trident
  priority: P2
  est_papers: ~201
  batch: 2

- source_id: awe_multimodal_reasoning
  url: https://github.com/HITsz-TMG/Awesome-Large-Multimodal-Reasoning-Models
  priority: P2
  est_papers: 550+
  batch: 2
```

### Batch 3（4 个仓库）

```yaml
- source_id: awe_digital_human
  url: https://github.com/weihaox/awesome-digital-human
  priority: P3
  est_papers: ~348
  batch: 3

- source_id: awe_human_interaction
  url: https://github.com/soraproducer/awesome-human-interaction-motion-generation
  priority: P3
  est_papers: ~144
  batch: 3

- source_id: awe_text_to_motion
  url: https://github.com/Zilize/awesome-text-to-motion
  priority: P3
  est_papers: ~185
  batch: 3

- source_id: awe_3d4d_world_models
  url: https://github.com/worldbench/awesome-3d-4d-world-models
  priority: P3
  est_papers: ~213
  batch: 3
```

---

## CLI Agent 执行指令模板

新会话启动时，粘贴以下 prompt：

```
你正在执行 ResearchWiki 的批量构建任务。

工作目录：ResearchFlow/ResearchWiki/
任务 spec：_private/planning/rwiki/rwiki_batch_task_spec.md
架构参考：_private/rwiki_architecture.md

执行规则：
1. 读取目标 source 的 meta.yaml，确定当前进度
2. 从上次中断的 step 继续执行
3. 每完成一个 step 或处理 20 条记录，更新 meta.yaml
4. 如果上下文即将耗尽，立即保存所有进度到 meta.yaml 和 csv，输出当前状态摘要，然后停止
5. enrich 步骤中，对 missing_paper_link 的条目用论文标题搜索 arxiv/semantic scholar 补全
6. 网络请求失败的条目标记 failed 跳过，不阻塞
7. 不要等我确认，自动持续执行直到该 source 的当前 step 完成或上下文耗尽

当前任务：处理 source_id=<填入目标 source>，从 Step <填入步骤> 开始。
```

---

## 并行策略

- Pilot（awe_human_motion）先单独跑通，验证流程
- Batch 1 的 7 个仓库可以开 7 个并行会话，每个会话处理一个 source
- 每个会话独立读写自己的 `sources/<source_id>/` 目录，不冲突
- `_global/paper_registry.csv` 的写入需要在 enrich 完成后统一合并，避免并发写冲突

---

## 注意事项

1. 每个 awesome 仓库的 README 格式不同，parser 需要 agent 现场分析并编写
2. enrich 是最耗时的步骤，预计每个仓库需要多个会话
3. filter 步骤产出 review_queue.csv 后需要人工审阅一次，之后的 download + analyze 可以全自动
4. 跨仓库去重在各自 enrich 完成后统一执行，不在单个 source 内处理
