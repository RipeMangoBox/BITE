# BITE v0.4 微信群更新草稿

面向：ResearchFlow v0.1.1 时期进群的早期微信群用户。

目的：说明 ResearchFlow 到 BITE v0.4 的主要变化，降低老用户迁移认知成本，邀请大家试用和反馈。

语气：真诚、克制、偏开发者更新，不做强营销。

## 可补充的核心迭代点

你原来总结的 4 点已经覆盖了主线。建议再补 4 个“对用户有感”的变化：


| 维度         | v0.1.1 时期                                                              | v0.4 可以强调的变化                                                                                  |
| ---------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 资产体系       | 以 `paperAnalysis/`, `paperPDFs/`, `paperCollection/`, `paperIDEAs/` 为主 | 升级为 `L0-L5` 资产层级：PDF、单篇分析、领域 vault、跨领域 vault、idea vault、experiment vault                      |
| 分析链可验证性    | 已有本地 Markdown/CSV 和 skills，但分析链还偏早期                                    | 形成 formal local analysis chain：解析复用、chunk anchor、主分析 JSON、分 section 写作、图表放置、vault export、结构校验 |
| 批量与索引能力    | 示例知识库为主，规模较小                                                           | 支持 `paper_list.csv` 批量队列、`obsidian-vault/index/index.jsonl` 检索索引和导航页，适合更大规模资产                 |
| 公开资产同步     | 主要靠本地样例和个人构建                                                           | PaperBite-Assets 发布到 HuggingFace，可按 `text/assets/all` 增量同步公开 evidence layer                   |
| 多 Agent 共享 | Claude/Codex 兼容已经出现                                                    | 进一步明确为本地优先 research memory：Markdown、JSONL、CSV、SKILL.md，供 Claude Code、Codex CLI、Cursor 等读取     |
| 研究闭环       | collect/download/analyze/query/idea 初步串联                               | 明确为 build -> query/decision -> idea/focus/review/export，更像一个从证据到 idea 的研究工作流                  |


不建议在群公告里重点讲的内容：

- 具体 reasoning 参数、cache profile、section worker 等实现细节。
- 私有批处理目录、内部评估成本、单次 A/B 细节。
- “v0.4 已经完全稳定”这类过满表述。更稳妥的说法是“核心链路已经重构完成，还在继续打磨”。

## 推荐群公告

各位 ResearchFlow 早期朋友，跟大家同步一个比较大的更新：

当时大家进群时，GitHub 开源版本还是 `ResearchFlow v0.1.1`。这段时间项目做了一轮比较彻底的重构，现在推进到了 `v0.4`，并正式更名为 **BITE**：**Bibliographic Intelligence for Thought Emergence**。

改名不是为了换包装，而是因为项目重心变得更清楚了：它不只是“管理文献流程”，而是希望把论文分析沉淀成可复用的 evidence vault，让后续的查询、对比、idea 生成和 reviewer 视角检查都有证据锚点。

这次从 v0.1.1 到 v0.4，主要变化有几类：

1. **分析链重构**
  现在的分析链更强调分层和可验证：从 PDF 解析复用、chunk 级 evidence anchor，到主分析 JSON、分 section 报告、核心图表/公式/实验证据抽取，再到 Obsidian vault 导出和结构校验。
   简单说，以前更像“把论文分析成笔记”，现在更像“把论文拆成可追溯、可复用、可被 agent 检索的证据资产”。
2. **分析资产体系升级**
  现在引入了 `L0-L5` 的资产层级：从原始 PDF、单篇论文分析、领域 vault、跨领域 vault，到 idea vault 和 experiment vault。
   这个变化的目标是让 idea 不是凭空生成，而是从已有 evidence 中逐步涌现；同时通过方法局限、增量视角和实验证据，帮助大家更快判断一个方向值不值得继续推进。
3. **文件布局重构**
  项目现在把分析工具链和分析资产隔离开：工具、skills、linkedCodebase 仍在项目中维护；真正给 Obsidian 打开的内容集中在 `obsidian-vault/`。
   这样可以避免 linkedCodebase 或大规模工程文件拖慢 Obsidian，也更适合把 vault 当作长期 research memory 来维护。
4. **公开第一批大规模分析资产**
  这次公开了 ICLR 2026 热门方向近 1k 篇论文的结构化分析资产，目前本地统计约 974 篇 ICLR 2026 分析笔记。后续会继续开放更大体量的分析资产。
   这部分更适合做跨方向检索和启发，比如从 agent、MLLM、RL、video、generative model、safety 等方向之间找交叉点。
5. **索引、批量和同步能力增强**
  v0.4 不只是多了一批笔记，也补上了更完整的批量分析、索引构建和同步能力。现在可以通过 `paper_list.csv` 管理论文队列，通过 `index.jsonl` 做快速检索，也可以从 HuggingFace 的 PaperBite-Assets 增量同步公开 evidence layer。
6. **从 ResearchFlow 到 BITE**
  BITE 的全称是 **Bibliographic Intelligence for Thought Emergence**。我理解它更准确地描述了这个项目现在想做的事：先把文献证据结构化，再让 research idea 在证据之间自然浮现，并保留每一步判断的出处。

这些改动还在继续打磨中，尤其是大规模资产、分析质量和跨方向检索体验，还有很多可以改进的地方。欢迎大家试用、吐槽、提 issue，也欢迎直接在群里说哪里不好用。

感谢大家从 ResearchFlow 早期一路关注到现在。

## 更短版本

各位 ResearchFlow 早期朋友，同步一个大更新：项目已经从 `ResearchFlow v0.1.1` 推进到 `v0.4`，并正式更名为 **BITE**：**Bibliographic Intelligence for Thought Emergence**。

这次变化不只是改名，主要是把项目从“本地论文知识库”推进到“可复用的 evidence vault + idea 涌现工作流”：

- 分析链重构：更规范的分层分析，更细的核心图文、公式、实验 evidence，更强调可追溯和可验证。
- 资产体系升级：引入 `L0-L5` 层级，从 PDF、单篇分析、领域/跨领域 vault，到 idea vault 和 experiment vault。
- 文件布局重构：分析工具链和 `obsidian-vault/` 分离，Obsidian 只聚焦研究资产，减少大 linkedCodebase 带来的卡顿。
- 公开资产：已开放 ICLR 2026 热门方向近 1k 篇结构化分析资产，后续会继续扩大。
- 批量/索引/同步增强：支持 `paper_list.csv` 队列、`index.jsonl` 检索索引和 HuggingFace PaperBite-Assets 增量同步。

欢迎大家试用 v0.4，也欢迎直接提意见。感谢大家从 ResearchFlow 早期一路关注到现在。

## 一页图文案

标题：ResearchFlow v0.1.1 -> BITE v0.4

副标题：从本地论文知识库，到 evidence-driven research memory

左侧：v0.1.1

- `paperAnalysis/`
- `paperPDFs/`
- `paperCollection/`
- `paperIDEAs/`
- 本地 Markdown/CSV
- 小规模示例知识库
- 查询、对比、idea 初步串联

右侧：v0.4

- `obsidian-vault/analysis/`
- `obsidian-vault/index/`
- `obsidian-vault/paperPDFs/`
- `obsidian-vault/ideas/`
- formal analysis chain
- `L0-L5` 资产层级
- ICLR26 近 1k 篇公开资产
- HuggingFace 增量同步
- 多 Agent 共享 research memory

底部一句话：

先沉淀结构化证据，再让 idea 从 evidence 中涌现。

## 依据

- GitHub release `V0.1.1`：2026-04-11 发布，说明其为 ResearchFlow 第一个 archived open-source release，包含 `paperAnalysis/`, `paperPDFs/`, `paperCollection/`, `paperIDEAs/`、共享 skills、双语文档和示例知识库。
- 当前 README：项目已更名为 BITE，并说明 PaperBite-Assets 已发布到 HuggingFace，覆盖 `L0-L3` 结构化论文资产。
- 当前 `docs/formal-analysis-chain.md`：记录 v0.4 的 formal local analysis chain。
- 当前 `docs/asset-architecture.md`：记录 `L0-L5` 资产层级。
- 当前本地统计：`obsidian-vault/analysis/` 约 1268 篇分析笔记，其中 `ICLR_2026` 约 974 篇。
- DeepSeek 外部视角建议：公告应聚焦资产层级、证据链、公开资产同步和多 Agent research memory，避免堆实现参数。

