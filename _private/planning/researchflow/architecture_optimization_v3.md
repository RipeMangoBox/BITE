---
created: 2026-04-16T15:00
updated: 2026-04-16T17:00
scope: private
---

# RF 架构优化路线 v3

> 承接 `roadmap.md` v2 架构，聚焦三个核心问题的诊断与解决方案。
> v3.1 更新：补充 ARIS 工具边界原则、index.jsonl 检索层设计、paperCollection 保留策略。
> v3.2 更新：旧 wiki 层合并入 paperCollection/（index.jsonl 移至 paperCollection/index.jsonl）；删除 papers-compare-table（功能由 papers-query-knowledge-base 覆盖）。

## 问题诊断

### 问题 1：Navigation Layer 没有实际作用

**现状**：`paperCollection/` 定位为 Obsidian 人类导航层，但实际上：

- agent 不依赖它（所有 skill 从 `paperAnalysis/` 出发）
- 人类用户在 Obsidian 中主要靠 graph view + backlink，不需要手工维护的 `by_task/by_technique/by_venue` 页面
- `papers-build-collection-index` 是唯一写入 `paperCollection/` 的 skill，但它的触发频率低，产出价值不明确
- roadmap v2 已经规划了 `paperCollection/index.jsonl` 作为 agent 入口，进一步要求 `paperCollection/` 从纯导航层升级为索引层

**结论**：`paperCollection/` 在当前架构中是一个"看起来有用但没人真正依赖"的层。

### 问题 2：Skill 体系面向人 vs 面向 agent 的兼容性

**现状**：

- 20 个 skill，按功能已经分类（构建链 / 使用链 / 支撑链 / 元技能）
- 但存在冗余：
  - `papers-analyze-pdf` vs `paperbite-analysis`：前者是完整 pipeline skill（路径解析 + 批量 + log 更新），后者是内部分析质量合约。两者的分析模板定义有重叠。
  - `papers-query-knowledge-base` vs `code-context-paper-retrieval`：后者本质是前者 + 代码环境检测，可以作为前者的 mode 而非独立 skill
  - `research-workflow` 作为路由层，和 `User_README_CN.md` 的路由表功能重叠
- 面向人的 skill 设计（交互式、建议式触发）和面向 agent 的需求（确定性输入输出、可编排）之间存在张力
- 当前 skill 的输入输出合约不够严格，agent 难以自动编排

### 问题 3：分析笔记格式不够 agent-friendly

**现状**：

- `paperbite-analysis` 定义的分析模板面向人类阅读优化（叙事性强、直觉优先）
- agent 需要的是：结构化字段可直接提取、关系可遍历、claim 可追踪
- frontmatter 已经有 `core_operator`/`primary_logic`/`claims`，但 body 部分是自由文本，agent 提取成本高
- 缺少 agent 专用的摘要层（类似 TL;DR 但更结构化）

---

## 优化路线

### Phase 0：立即可执行（本周）

#### 0.1 Navigation Layer → Index Layer（架构描述更新）

- [x] README.md / README_CN.md 架构图：三层改为 Output + Index + Retrieval，`paperCollection/` 统一为索引与导航层（含 `index.jsonl` + Obsidian 页面）
- [x] AGENTS.md：index layer 描述替代 navigation layer，`paperCollection/` 统一服务 agent 和 Obsidian
- [x] `papers-build-collection-index` 保留，描述更新为同时生成 `paperCollection/index.jsonl`（agent）和 Obsidian 导航页
- 旧 wiki 层已合并入 `paperCollection/`，不再作为独立顶层目录

#### 0.2 Skill 合并第一轮（消除明确冗余）

- [x] `paperbite-analysis` 合并进 `papers-analyze-pdf`（确认完全覆盖后删除）
- [x] `papers-compare-table` 删除（功能由 `papers-query-knowledge-base` 覆盖；分析笔记缺乏完整指标表，强行结构化对比会产生误导）
- [ ] `papers-collect-from-web` + `papers-collect-from-github-awesome` → `papers-collect`（改动较大，单独 session 执行）

#### 0.3 ARIS 工具边界原则

RF 是 pre-built evidence layer（数据层），不是 execution engine。工具边界：

| 放在 RF | 放在 ARIS 侧 |
| --- | --- |
| `external-writeback`（写入协议） | 读取 `paperAnalysis/` 的 adapter |
| `paperCollection/adapters/aris.md`（协议文档，planned） | idea/experiment/claim 的 CRUD 逻辑 |
| 数据格式 schema（`paperCollection/SCHEMA.md`，planned） | session memory 与 RF 证据的融合策略 |

原则：RF 定义数据格式和写入协议，ARIS 侧实现调用逻辑。任何自动化工具只要遵循 `external-writeback` 的输入格式就能接入。

### Phase 1：Dual-Interface Skill 设计（1-2 周）

核心思路：每个 skill 同时支持人类交互模式和 agent 编排模式，而不是为两类用户分别建 skill。

#### 1.1 Skill 接口标准化

每个 SKILL.md 新增 `## Agent Interface` 节：

```yaml
agent_interface:
  input:
    required: [pdf_path]
    optional: [category, venue, year, language]
  output:
    files: [paperAnalysis/<Category>/<Venue_Year>/<Year>_<Title>.md]
    status: checked | analysis_mismatch
    structured_return:
      - field: md_path
        type: string
      - field: claims
        type: list[string]
  deterministic: true  # agent 可以不经交互直接调用
```

- 人类模式：保持现有交互式体验（建议、确认、解释）
- Agent 模式：跳过交互，严格按 input → output 合约执行
- 通过 `mode: human | agent` 参数切换（默认 human）

#### 1.2 Skill 精简（合并 query 系列）

- `code-context-paper-retrieval` 合并为 `papers-query-knowledge-base` 的 `mode: code-context`
- 保留独立 skill 入口作为 alias（向后兼容），但实际执行逻辑统一

#### 1.3 research-workflow 重定位

- 从"人类路由助手"转变为"pipeline orchestrator"
- 人类模式：保持现有交互式路由
- Agent 模式：接受 pipeline spec（如 `stages: [collect, download, analyze]`），自动编排执行

### Phase 2：Agent-Friendly 分析格式（2-4 周）

#### 2.1 分析笔记新增 Agent Summary Block

在现有 `> [!abstract] Quick Links & TL;DR` 之后，新增：

```markdown
> [!info] **Agent Summary**
> - **task_path**: text → motion sequence
> - **bottleneck**: compound instruction decomposition
> - **mechanism_delta**: CoT decomposition + RL binding → reduced semantic drift
> - **evidence_signal**: FID↓12%, R-Precision↑8% on HumanML3D
> - **reusable_ops**: [CoT-decomposition, RL-binding-reward]
> - **failure_modes**: [long-sequence > 10s, rare-action-vocabulary]
```

设计原则：
- 每个字段都是 key-value，agent 可直接 parse
- 与 frontmatter 互补：frontmatter 是检索维度，Agent Summary 是理解维度
- 人类阅读时折叠或跳过，不影响阅读体验

#### 2.2 Frontmatter 扩展（承接 roadmap v2）

- `related_work_position` 已有，保持
- `claims` 已有，保持
- 新增 `agent_digest`（可选）：一行结构化摘要，格式 `bottleneck → mechanism → capability_delta`

#### 2.3 paperbite-analysis 模板更新

更新合并后的 `papers-analyze-pdf` 模板，在分析质量合约中加入 Agent Summary Block 的生成规则。

### Phase 3：Agent Pipeline 基础设施（4-8 周）

#### 3.1 paperCollection/ 统一索引层 + index.jsonl 检索层

`paperCollection/index.jsonl` 作为 agent 的主检索入口（旧 wiki 层已并入 paperCollection/）：

```jsonl
{"path":"paperAnalysis/MLLM/CVPR_2026/2026_XXX.md","title":"...","category":"Multimodal_LLM","venue":"CVPR","year":2026,"tags":["task/vqa","moe"],"core_operator":"...","claims_count":3}
```

- 每行一篇论文，只含检索维度字段（不含 body）
- 5000 篇约 2-3 MB，agent 可一次性读入做 filter（5000 → 20-50 篇候选）
- `papers-analyze-pdf` 不直接改动 index
- `papers-build-collection-index` 执行时全量重建 `index.jsonl` 与 Obsidian 导航页（保证一致性）

`paperCollection/` 统一服务两个消费者：

| | Obsidian 导航页 | index.jsonl |
| --- | --- | --- |
| 格式 | Markdown 导航页 | JSONL 结构化数据 |
| 消费者 | 人类（Obsidian） | agent |
| 更新方式 | 全量重建 | 全量重建 |

#### 3.2 graph/edges.jsonl（承接 roadmap v2）

- `papers-analyze-pdf` 分析时提取 `related_work_position` → 写入 edges
- `research-brainstorm-from-kb` 生成 idea 时写入 `inspired_by` edges

#### 3.3 external-writeback skill（承接 roadmap v2）

- 统一外部工具回写接口
- 支持 experiment / claim / idea 状态更新

---

## Skill 体系最终目标（Phase 1-2 完成后）

### 功能类划分

#### 🔧 构建链（Build）
- `papers-collect`（合并后）
- `papers-download-from-list`
- `papers-analyze-pdf`（含 paperbite 质量合约）
- `papers-build-collection-index`（生成 agent index + Obsidian 导航页）

#### 🔍 使用链（Use）
- `papers-query-knowledge-base`（含 code-context mode，也处理 comparison requests）
- `research-brainstorm-from-kb`
- `idea-focus-coach`
- `reviewer-stress-test`

#### 🛠 支撑链（Support）
- `papers-audit-metadata-consistency`
- `notes-export-share-version`
- `papers-sync-from-zotero`
- `external-writeback`（新增）

#### 🧭 编排层（Orchestration）
- `research-workflow`（dual-mode: human router + agent orchestrator）

#### ⚙️ 元技能（Meta）
- `domain-fork`
- `skill-fit-guard`
- `write-daily-log`
- `rf-obsidian-markdown`（约定，非执行 skill）

总计：17 个（从 20 个精简到 17 个，合并 3 个冗余）

### 每个 skill 的 dual-interface 保证

| 模式 | 触发 | 交互 | 输出 |
| --- | --- | --- | --- |
| human | 自然语言 / slash 命令 | 建议式、可确认 | 解释性文本 + 文件 |
| agent | 结构化参数 | 无交互 | 结构化 return + 文件 |

---

## 与 roadmap v2 的关系

| roadmap v2 规划 | 本文档处理 |
| --- | --- |
| 四实体模型 | 保持，Phase 3 执行 |
| paperCollection/ 内渐进披露 | 保持，Phase 3 执行，在统一索引层内承载导航与后续协议文档 |
| graph/edges.jsonl | 保持，Phase 3 执行 |
| papers-collect 合并 | 提前到 Phase 0 执行 |
| external-writeback | 保持，Phase 3 执行 |
| ARIS 适配 | 保持，依赖 Phase 3 基础设施 |
| 分析模板演进 | 扩展：新增 Agent Summary Block（Phase 2） |
| paperCollection 保留 | 修正：物理保留，统一为 Index Layer（含 index.jsonl + Obsidian 导航页），旧 wiki 层已合并入此目录 |

---

## 立即可执行的步骤清单

以下步骤已在 Phase 0 中执行：

1. ✅ `paperbite-analysis` 删除（所有规则已被 `papers-analyze-pdf` 覆盖）
2. ✅ `papers-compare-table` 删除（功能由 `papers-query-knowledge-base` 覆盖）
3. ✅ 旧 wiki 层合并入 `paperCollection/`（`index.jsonl` 移至 `paperCollection/index.jsonl`）
4. ✅ README.md / README_CN.md 架构图更新为统一 Index Layer
5. ✅ AGENTS.md 更新 index layer 描述
6. ✅ User_README.md / User_README_CN.md 反映 skill 精简
7. ✅ research-workflow / papers-build-collection-index / papers-query-knowledge-base SKILL.md 更新
8. ✅ skills-config.json 移除 paperbite-analysis 和 papers-compare-table

待后续 session 执行：

9. [ ] 合并 `papers-collect-from-web` + `papers-collect-from-github-awesome` → `papers-collect`
10. ✅ 实现 `paperCollection/index.jsonl` 生成逻辑（在 build script 中，由 build 全量重建）
11. [ ] Agent Summary Block 模板设计与 `papers-analyze-pdf` 更新
