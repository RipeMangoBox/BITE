---
created: 2026-04-11T16:00
updated: 2026-04-11T18:30
scope: private
---

# ResearchFlow 推进路线图（私有）

> 本文件不进入开源仓库（已加入 `.gitignore`），仅用于个人推进规划。

## 阅读顺序建议

- 先看「一、定位优势」和「二、架构演进计划」，统一产品判断。
- 再看「三、分析模板演进」和「四、Skill 体系」，明确具体落地改动。
- 最后看「五、ARIS 适配协议」「六、ResearchWiki 产物计划」「七、论文准备路线」和「八、近期 TODO」，对齐外部对接与执行顺序。

---

## 一、定位优势：ResearchFlow vs ARIS Research Wiki

### 1.1 本质差异

| 维度 | ARIS Research Wiki | ResearchFlow |
| --- | --- | --- |
| 定位 | Session-level memory（边做边记） | Pre-built evidence layer（先建好再接入） |
| 论文来源 | LLM 搜 arXiv 后临时生成摘要 | 读完整 PDF 后结构化深度分析 |
| 分析深度 | thesis + method + limitations（几句话） | Three Questions + Aha! Moment + core_operator + primary_logic |
| 结构化程度 | 自由格式 Markdown | 严格 YAML frontmatter + 固定模板，字段级可检索 |
| 质量保障 | 无（取决于当次 LLM 表现） | 模板约束 + 结构检查 + metadata 审计 skill |
| 知识规模 | 单项目积累，通常几十篇 | 可预建数百篇，跨项目复用 |
| 跨工具共享 | ARIS 内部状态，不可外部访问 | Platform-agnostic，Claude Code / Codex CLI / Cursor / 任意 agent 可读 |
| 领域覆盖 | Per-project，换方向从零开始 | ResearchWiki 提供 domain-level 预建知识库 |
| 论文间关系 | typed edges（extends/contradicts），但基于 LLM 临时判断 | 从完整 PDF 的 Related Work 提取 + Obsidian 双链可视化 |

### 1.2 核心叙事

ARIS Research Wiki 解决的是“别重复犯错”（anti-repetition memory）。
ResearchFlow 解决的是“做决策时手里有没有足够的结构化证据”（evidence-grounded decision）。
两者互补，不矛盾。最强组合是：

- ResearchFlow 提供 pre-built 的深度证据层。
- ARIS Wiki 在此基础上做 session-level 的 idea / experiment / claim 积累。
- 自动化工具的 idea 生成、review、rebuttal 都站在 ResearchFlow 的证据之上。

### 1.3 护城河

1. **数据壁垒**：数百篇论文的深度结构化分析（ResearchWiki），工作量本身是护城河。
2. **质量壁垒**：严格模板 + 审计机制，不是 LLM 随机生成能替代的。
3. **生态壁垒**：如果成为 ARIS 等工具的“官方证据层”，绑定关系不可复制。
4. **先发壁垒**：arXiv preprint + GitHub commit history 占 priority。
5. **Obsidian 生态壁垒**：双链关系图 = 本地化 Connected Papers，RF + Obsidian 的组合体验不可替代。

---

## 二、架构演进计划

### 2.1 当前架构（v1）

```text
paperPDFs/         ← 原始 PDF
paperAnalysis/     ← 结构化分析笔记（核心证据层）
paperCollection/   ← 可选统计 / 导航层
paperIDEAs/        ← 下游产出
```

### 2.2 目标架构（v2：四实体 + 关系图 + 渐进披露 + Obsidian 双链）

```text
ResearchFlow/
├── paperPDFs/                    ← Raw Sources（不可变）
├── paperAnalysis/                ← Paper 实体（深度分析，核心证据层）
│   ├── <Category>/<Venue_Year>/  ← 按领域/会议组织
│   └── analysis_log.csv          ← 论文状态追踪
├── paperIDEAs/                   ← Idea 实体（brainstorm 产出 + 外部工具回写）
├── paperExperiments/             ← [新增] Experiment 实体（实验记录回写）
├── paperClaims/                  ← [新增] Claim 实体（可验证声明 + 证据状态）
├── graph/                        ← [新增] 关系图
│   └── edges.jsonl               ← typed edges
├── wiki/                         ← [新增] 渐进披露入口（agent 专用）
│   ├── index.md                  ← 内容目录（agent 首先读这个）
│   ├── log.md                    ← 时序操作日志（append-only）
│   ├── query_pack.md             ← 查询结果持久化
│   ├── SCHEMA.md                 ← Wiki 协议 + Obsidian Markdown 约定
│   └── adapters/                 ← 外部工具适配协议
│       └── aris.md               ← ARIS 对接协议文档
├── paperCollection/              ← Obsidian 人类导航层（保留）
├── .claude/skills/               ← Skill 定义
└── AGENTS.md                     ← Schema 层
```

### 2.3 四实体模型

| 实体 | 目录 | 来源 | 核心字段 |
| --- | --- | --- | --- |
| Paper | `paperAnalysis/` | `papers-analyze-pdf` 生成 | `title`, `venue`, `year`, `core_operator`, `primary_logic`, `tags`, `pdf_ref`, `claims` (list), `related_papers` (list) |
| Idea | `paperIDEAs/` | brainstorm 生成或外部工具回写 | `hypothesis`, `status` (`proposed/testing/failed/succeeded`), `failure_notes`, `source_papers` |
| Experiment | `paperExperiments/` | 外部工具回写（ARIS 等） | `metrics`, `verdict`, `hardware`, `duration`, `linked_idea`, `linked_claims` |
| Claim | `paperClaims/` | 从 Paper 分析中提取或外部工具回写 | `statement`, `evidence_status` (`reported/supported/invalidated`), `source_paper`, `source_experiment` |

### 2.4 关系图（`graph/edges.jsonl`）

每行一条 typed edge：

```json
{"from": "paper:2026_Motion_R1", "to": "paper:2025_MotionGPT", "rel": "extends", "note": "CoT + RL binding 扩展了 LLM-motion 范式"}
{"from": "idea:001", "to": "paper:2026_Motion_R1", "rel": "inspired_by"}
{"from": "experiment:exp_001", "to": "claim:C1", "rel": "supports"}
{"from": "paper:2026_A", "to": "paper:2025_B", "rel": "contradicts", "note": "A 的消融否定了 B 的核心假设"}
```

关系类型枚举：`extends`、`contradicts`、`supersedes`、`inspired_by`、`concurrent`、`supports`、`invalidates`、`tested_by`。

数据来源：

- Paper 间关系：`papers-analyze-pdf` 从 Related Work / Method 部分提取，写入 frontmatter 的 `related_papers` 字段，同时写入 `graph/edges.jsonl`。
- Idea → Paper：`research-brainstorm-from-kb` 生成时写入。
- Experiment → Claim：`external-writeback` 接收外部工具回写时写入。

### 2.5 渐进披露机制

设计原则：脏标记 + 批量刷新，避免逐篇更新的 token 浪费。
RF 是 pre-built 的离线知识库，不是实时 session 工具。渐进披露层的更新策略如下：

| 文件 | 更新时机 | 更新方式 |
| --- | --- | --- |
| `wiki/log.md` | 每次 analyze 批次完成后 | append 一条记录（极低开销） |
| `wiki/index.md` | `papers-build-collection-index` 执行时 | 批量重建（和 `paperCollection` 同步刷新） |
| `wiki/query_pack.md` | `papers-query-knowledge-base` 执行后（可选） | 覆盖写入最近查询结果 |

脏标记机制：

- `wiki/index.md` frontmatter 含 `stale: true/false`。
- `papers-analyze-pdf` 批次完成后设 `stale: true`。
- `papers-build-collection-index` 完成后设 `stale: false`。
- agent 读到 `stale: true` 即知 index 可能不完整，可决定是否先触发 build。

### 2.6 `paperCollection` 定位（保留）

明确定位为“Obsidian 人类导航层”，不再让 agent 依赖它。

- 对人类：`by_task` / `by_technique` / `by_venue` 页面在 Obsidian 里提供 graph view、backlink、快速跳转。
- 对 agent：`wiki/index.md` 取代 `paperCollection` 成为入口。
- `papers-build-collection-index` 同时生成 `paperCollection/`（给人类）和 `wiki/index.md`（给 agent）。
- RF + Obsidian 的组合体验是核心卖点之一，`paperCollection` 是这个体验的关键组件。

### 2.7 论文间关系链（本地化 Connected Papers）

这是高价值差异化方向。Connected Papers 收费且不可本地化，RF 填补这个空缺。

实现方案：

- 数据来源：`papers-analyze-pdf` 分析时从 Related Work / Method 提取关系，写入 frontmatter 的 `related_papers` 字段。
- 存储：`graph/edges.jsonl`。
- Obsidian 联动：`paperAnalysis` 笔记中用 `[[ ]]` wiki link 链接相关论文，Obsidian graph view 自动生成关系网络。
- agent 联动：agent 读 `graph/edges.jsonl` 做关系查询，例如“找所有 extend 了 MotionGPT 的论文”。

### 2.8 Obsidian Markdown 约定

在 `wiki/SCHEMA.md` 中定义，所有 skill 生成的 Markdown 必须遵循：

- 内部链接用 `[[ ]]` wiki link，不用 `[]()` Markdown link。
- 引用块用 `> [!abstract]` / `> [!note]` callout 语法。
- frontmatter 必须是合法 YAML。
- 不使用 HTML 标签。
- 图片引用用 `![[path]]` 格式。
- 参考 `kepano/obsidian-skills` 的 obsidian-markdown 规范。

---

## 三、分析模板演进

### 3.1 保留不动的（高价值）

- YAML frontmatter（`core_operator`, `primary_logic`, `tags`, `venue`, `year`, `pdf_ref`）是机器检索命脉。
- Quick Links & TL;DR 用于 agent 快速定位 + 人类快速浏览。
- Part II 的 Aha! Moment 是 RF 分析质量的核心差异化。

### 3.2 调整项

| 板块 | 现状 | 调整 |
| --- | --- | --- |
| Part I「能力签名」 | 偏 API 文档风格（输入/输出/中间态表格），对 agent 检索价值低 | 精简为“问题定义 + 核心能力 + 边界条件”三段，砍掉 API 接口表格 |
| Part III「Technical Deep Dive」 | 和 Part II 有重叠，经常变成 Part II 的细化版 | 重命名为「Evidence & Limits」，聚焦：关键实验信号 + 局限性 + 可复用组件，明确和 Part II 的边界 |
| frontmatter | 缺少 `claims` 字段 | 新增 `claims`（list）：2-3 条可验证声明，为 Claim 实体提供数据源 |
| frontmatter | 缺少关系字段 | 新增 `related_papers`（list）：该论文明确 extends/contradicts 的论文，为 graph 提供种子数据 |
| 笔记底部 | 只有 PDF embed | 新增 `[[ ]]` wiki link 区域，链接 `related_papers` 中的论文，驱动 Obsidian graph view |

### 3.3 不新增的

- 不加「Reproducibility Checklist」: reviewer 的事，不是证据层的事。
- 不加「Code Snippets」: 代码联动由 `code-context-paper-retrieval` 负责。

### 3.4 更新后的模板结构

```markdown
---
title: "..."
venue: CVPR
year: 2025
tags: [...]
core_operator: ...
primary_logic: |
  ...
pdf_ref: paperPDFs/...
category: ...
claims:                          # [新增]
  - "Claim 1: ..."
  - "Claim 2: ..."
related_papers:                  # [新增]
  - {title: "PaperX", rel: "extends", note: "..."}
  - {title: "PaperY", rel: "contradicts", note: "..."}
---

# Paper Title

> [!abstract] **Quick Links & TL;DR**

## Part I：问题与挑战
- 问题定义（1-2 段）
- 核心能力（该方法能/不能做什么）
- 边界条件（在哪些条件下有效/失效）

## Part II：方法与洞察
- 设计哲学
- **The "Aha!" Moment**（必须保留）
- 战略权衡

## Part III：证据与局限
- 关键实验信号（信号类型 + 结论，不堆数字）
- 局限性与失败模式
- 可复用组件（哪些 operator/设计可迁移）

## Related Papers
- [[paperAnalysis/.../PaperX.md|PaperX]] — extends: ...
- [[paperAnalysis/.../PaperY.md|PaperY]] — contradicts: ...

## Local Reading
![[paperPDFs/...]]
```

---

## 四、Skill 体系（精简后）

### 4.1 Skill 审计结论

ARIS 的 `/research-wiki` 用 1 个 skill + 子命令覆盖所有功能，因为它的 wiki 功能浅。RF 的 skill 多是因为功能深度大，但需要消除冗余。

原则：不为 wiki 层单独建 skill，而是让现有 skill 在执行时顺带维护 wiki 层。

### 4.2 合并

- `papers-collect-from-web` + `papers-collect-from-github-awesome` → `papers-collect`
- 通过参数区分来源类型（`web` / `github-awesome`）
- 减少用户选择负担

### 4.3 现有 skill 扩展

| Skill | 扩展内容 |
| --- | --- |
| `papers-analyze-pdf` | frontmatter 新增 `claims` + `related_papers`；批次完成后 append `wiki/log.md` + 设 `wiki/index.md stale:true`；笔记底部新增 `[[ ]]` 双链区域 |
| `papers-build-collection-index` | 同时生成 `paperCollection/`（人类）和 `wiki/index.md`（agent）；完成后设 `stale:false` |
| `papers-query-knowledge-base` | 先读 `wiki/index.md` 做渐进披露；查询结果可选回写 `wiki/query_pack.md` |
| `research-brainstorm-from-kb` | 生成 idea 时写入 `graph/edges.jsonl`（`inspired_by` 关系） |
| `reviewer-stress-test` | review 结果可关联到 Claim 实体，标记被质疑的 claim |
| `papers-audit-metadata-consistency` | 扩展检查范围到 graph 孤立节点、矛盾 claim、过时关系、Obsidian 双链断裂 |
| `research-workflow` | 新增 experiment / claim 阶段路由 |

### 4.4 新增 skill（仅 1 个）

| Skill | 功能 | 优先级 |
| --- | --- | --- |
| `external-writeback` | 统一接收外部工具（ARIS 等）的回写：experiment 结果 → `paperExperiments/`，claim 状态更新 → `paperClaims/`，idea 状态更新 → `paperIDEAs/`，同时更新 `graph/edges.jsonl` + `wiki/log.md`。这是 RF 作为共享证据层的关键接口。 | P0 |

### 4.5 取消的 roadmap 新增 skill

| 原计划 Skill | 取消原因 |
| --- | --- |
| `wiki-ingest` | ingest 动作已由 `papers-analyze-pdf`（paper）和 `research-brainstorm-from-kb`（idea）覆盖，不需要独立入口 |
| `wiki-lint` | 合并到 `papers-audit-metadata-consistency` 的扩展范围 |
| `wiki-query` | `papers-query-knowledge-base` 加渐进披露即可，不需要新 skill |
| `claim-tracker` | claim 生命周期分散在 analyze（提取）、`external-writeback`（更新）、audit（检查）中 |
| `adapter-aris` | 不是 skill，而是协议文档，放在 `wiki/adapters/aris.md` |

### 4.6 最终 skill 清单（15 个）

#### 路由层

- `research-workflow`：统一入口

#### 构建链

- `papers-collect`：从 `web` / `github-awesome` 收集
- `papers-download-from-list`：下载 PDF
- `papers-analyze-pdf`：结构化分析 + `claims` + `related_papers` + `log`
- `papers-build-collection-index`：生成 `paperCollection` + `wiki/index.md`

#### 使用链

- `papers-query-knowledge-base`：渐进披露 + `query_pack` 回写
- `papers-compare-table`：结构化对比表
- `research-brainstorm-from-kb`：idea 生成 + graph 写入
- `idea-focus-coach`：方案收敛
- `reviewer-stress-test`：审稿压测 + claim 关联
- `code-context-paper-retrieval`：代码联动检索

#### 支撑链

- `papers-audit-metadata-consistency`：元数据 + graph + claim 健康检查
- `notes-export-share-version`：笔记导出
- `external-writeback`：外部工具回写接口

#### 元技能

- `domain-fork`：领域迁移
- `skill-fit-guard`：skill 匹配检测

---

## 五、ARIS 适配协议（`wiki/adapters/aris.md`）

不是 skill，而是一份协议文档 + 示例配置。

### 5.1 对接映射

#### `ARIS /research-lit`

- 优先读 `paperAnalysis/`（pre-built 证据）。
- 如果 `paperAnalysis` 中没有，再 fallback 到 arXiv 搜索。
- 新发现的论文可通过 `external-writeback` 回写。

#### `ARIS /idea-creator`

- 读 `paperAnalysis/` + `paperIDEAs/`（含失败记录）。
- 生成的 idea 通过 `external-writeback` 回写到 `paperIDEAs/` + graph。
- 失败 idea 的 `failure_notes` 作为 anti-repetition 输入。

#### `ARIS /result-to-claim`

- 实验结果通过 `external-writeback` 写入 `paperExperiments/`。
- claim 状态更新写入 `paperClaims/`。
- graph 新增 `supports` / `invalidates` edges。

### 5.2 关键原则

- RF 定义数据格式和写入协议，不依赖 ARIS 内部实现。
- 任何自动化工具只要遵循 `external-writeback` 的输入格式就能接入。
- RF 的 pre-built 证据 + ARIS 的 session memory 共存，不互相替代。

---

## 六、ResearchWiki 产物计划

### 6.1 定义

ResearchWiki = ResearchFlow 方法论在特定研究方向上的预建知识库产物。

每个 ResearchWiki 是一个独立的 ResearchFlow 实例，包含该方向的：

- 数百篇论文的深度结构化分析（`paperAnalysis/`）
- 预建的 `wiki/index.md` / `graph/edges.jsonl` / claim 网络
- Obsidian 双链关系图（本地化 Connected Papers）
- 可直接被 ARIS 等工具接入使用

### 6.2 首批方向

| 方向 | 预估论文数 | 主要来源 | 优先级 |
| --- | --- | --- | --- |
| Human Motion Generation | 200+ | 现有 KB + `awesome-human-motion` | P0（已有基础） |
| Diffusion Models (core) | 150+ | `awesome-diffusion-models` | P1 |
| LLM Agents | 150+ | `awesome-llm-agents` | P1 |
| Video Generation | 100+ | `awesome-video-generation` | P2 |
| Multimodal LLM | 100+ | `awesome-mllm` | P2 |

### 6.3 交付标准

- [ ] `paperAnalysis/` 覆盖该方向 top venue 近 2 年核心论文
- [ ] 每篇分析通过结构检查（Three Questions + Aha! Moment 完整）
- [ ] `wiki/index.md` 完整，可被 agent 直接使用
- [ ] `graph/edges.jsonl` 包含 `extends` / `contradicts` 关系
- [ ] `paperClaims/` 提取了核心论文的可验证声明
- [ ] Obsidian graph view 可正常展示论文关系网络
- [ ] metadata 审计通过

---

## 七、论文准备路线

### 7.1 核心叙事

> 自动化科研工具缺乏结构化证据层，导致 idea 空泛、实验缺乏依据、rebuttal 无法有力回应。ResearchFlow 提供 pre-built、structured、platform-agnostic 的 evidence layer，ResearchWiki 提供 domain-specific 的预建知识库。实验证明接入后显著提升自动化科研的产出质量。

### 7.2 实验设计（核心 ablation）

| 配置 | 描述 |
| --- | --- |
| Baseline | ARIS 原生（无 ResearchFlow） |
| +RF | ARIS + ResearchFlow evidence layer（无预建知识库） |
| +RF+RW | ARIS + ResearchFlow + ResearchWiki（预建 domain KB） |
| +ARIS-Wiki | ARIS + 自带 Research Wiki（对照组） |

评测维度：

- Idea quality：`novelty score`、与已有工作重叠率、`feasibility`
- Citation accuracy：引用真实性、相关性
- Experiment design：实验方案合理性、baseline 选择质量
- Review response：reviewer concern 回应的证据充分性
- 端到端：最终论文的 auto-review score

### 7.3 多平台验证

至少在 2 个自动化工具上验证（证明 platform-agnostic）：

- ARIS（首选，6.1k star，社区活跃）
- AI Scientist 或 MLR-Copilot（如果可获取）

### 7.4 时间线

#### Phase 1（现在 → 4 周）

- 分析模板 v2（`claims` + `related_papers` + Part I/III 调整）
- `papers-collect` 合并
- `graph/edges.jsonl` 格式规范
- `wiki/` 渐进披露层实现（`index.md` + `log.md` + `SCHEMA.md`）
- `external-writeback` skill 开发
- Human Motion Generation ResearchWiki 完善

#### Phase 2（4 → 8 周）

- ARIS 适配协议文档 + 联调
- `papers-build-collection-index` 扩展（同时生成 `wiki/index.md`）
- `papers-audit` 扩展（graph + claim 健康检查）
- 第二个 ResearchWiki 方向启动
- 实验设计细化 + 评测指标确定

#### Phase 3（8 → 12 周）

- 跑完整 ablation 实验
- 多平台验证（如果可行）
- arXiv technical report 占坑

#### Phase 4（12 → 16 周）

- 正式论文撰写
- 目标：ICLR 2027 或 NeurIPS 2026（取决于 deadline）

---

## 八、近期 TODO（本周）

- [x] 确认 `_private/` 已被 `.gitignore` 排除
- [ ] 更新 `papers-analyze-pdf` `SKILL.md`：frontmatter 新增 `claims` + `related_papers`
- [ ] 更新 `papers-analyze-pdf` `SKILL.md`：Part I 精简 + Part III 重命名
- [ ] 设计 `graph/edges.jsonl` 格式规范文档
- [ ] 设计 `wiki/SCHEMA.md`（Obsidian Markdown 约定 + Wiki 协议）
- [ ] 合并 `papers-collect-from-web` + `papers-collect-from-github-awesome` → `papers-collect`
- [ ] 草拟 `external-writeback` skill 的输入格式
- [ ] 草拟 `wiki/adapters/aris.md` 适配协议
- [ ] 开始写 arXiv technical report outline

---

## 附：本版更新点

1. 渐进披露改为脏标记 + 批量刷新策略，取消逐篇更新。
2. 新增第三节「分析模板演进」，Part I 精简、Part III 重新定位、frontmatter 扩展。
3. `paperCollection` 明确保留为 Obsidian 人类导航层。
4. 新增论文间关系链设计（本地化 Connected Papers + Obsidian 双链）。
5. 新增 Obsidian Markdown 约定（参考 `kepano/obsidian-skills`）。
6. Skill 体系大幅精简：合并 1 个、取消 4 个 roadmap 新增、只新增 1 个 `external-writeback`，最终 15 个。
7. ARIS 适配从 skill 改为协议文档。
8. TODO 更新为具体可执行项。


## 后期可借鉴DeepWiki的优化点
1. MCP 接口思路：DeepWiki 通过 MCP server 让外部 agent 查询知识库。ResearchWiki 目前靠 agent 直接读文件系统，这在本地场景够用，但如果未来要支持远程 agent 或多人协作，MCP 是一个值得考虑的接口层。不过这是后期优化，不是现在的优先级。
2. 自动架构图生成：DeepWiki 自动生成 Mermaid 架构图。ResearchWiki 可以借鉴这个思路——在 wiki/index.md 或 paperCollection/ 中自动生成研究方向的方法演进图（比如 motion generation 领域的方法谱系图），用 Mermaid 渲染。这对 Obsidian 用户体验是一个加分项。