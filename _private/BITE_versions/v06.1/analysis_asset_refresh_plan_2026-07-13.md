# BITE v06.1 分析资产全量复查计划

- created: 2026-07-13
- status: executed-with-documented-exceptions
- baseline: `_private/BITE_versions/v06/latest_analysis_chain_2026-07-03.md`
- target: `obsidian-vault/analysis/*/*.md`
- source policy: 不读取原 PDF，仅使用 v06 分析链、优秀范例和现有分析笔记

## 目标与验收边界

本轮目标是把旧版本分析资产统一到 v06 的可读性与可检索性标准，重点处理 2026-06-26 前创建或仍保留旧链结构的 paper notes。执行阶段只改分析 Markdown；不重新解析 PDF，不补写缺乏现有笔记证据的论文事实，也不顺带重建索引。

验收条件：

1. 笔记结构、frontmatter 和内部 embed 符合 v06 约定。
2. 外部 paper/project/code 链接语法有效且无明显重复；本地 PDF、图片 embed 均能解析到现有文件。
3. 核心方法图、主结果、关键消融和代表性定性图被保留；冗余补充图表被删除。
4. 删除图片后同步删除孤立 caption 和重复解释，不改变论文结论与数值。
5. 每篇修改均能通过 deterministic 检查，并留下逐篇变更原因与批次汇总。

## 当前资产盘点

扫描口径为 `obsidian-vault/analysis/*/*.md`，排除 `analysis/README.md`、MinerU 中间目录和报告文件。

| 项目 | 数量 | 说明 |
|------|-----:|------|
| 顶层 paper notes 总量 | 5,345 | 本轮总扫描集合 |
| v06 canonical 五章节结构 | 1,997 | 仅做保守校验，默认不改写 |
| 旧或非 canonical 结构 | 3,348 | 主要刷库候选 |
| Git 可证实在 06-26 前创建 | 3,455 | 均首次出现在 06-24 导入提交 |
| Git 可证实在 06-26 后创建 | 100 | 默认保护 |
| 无可靠 Git 创建记录 | 1,790 | 不能用日期单独判定 |
| 含“补充图/补充图表”标题 | 2,835 | 图片语义复查候选 |
| 恰有 12 张图片 | 1,509 | 旧模板批量堆图的强信号 |
| 当前无效图片 embed | 66 | 硬错误，涉及路径或缺失资产 |
| 当前无效 PDF embed | 13 | 硬错误 |
| 缺 `project_link` | 1,841 | 旧 frontmatter 差异 |
| 缺 `code_link` | 1,981 | 旧 frontmatter 差异 |

日期统计存在边界限制：v06 已移除 `created` 字段，文件 mtime 又曾被批量刷新；因此不能把 mtime 当创建时间。执行集合应由“可证实创建日期”和“结构版本”联合决定。

## 建议的参与集合

采用三层集合，避免误刷已升级资产：

1. **主集合**：3,348 篇旧或非 canonical 结构笔记。
2. **补充集合**：结构已 canonical，但 Git 可证实在 06-26 前创建，且存在硬错误、补充图堆叠或旧链接残留的笔记。
3. **保护集合**：06-26 后创建且已 canonical 的笔记；只修断链、无效 embed 等硬错误，不做正文重写。

最终参与数量需在 dry-run 清单生成后锁定。预计语义刷新的上限为 3,348 篇，硬错误保守修复可能额外覆盖少量 canonical 笔记；不能直接把 3,455 当作最终数量。

## 逐篇刷新规则

### A. 结构与 frontmatter

- 统一为 YAML frontmatter、H1、核心洞察 callout、元数据表、效果简介以及五个 canonical 主章节。
- canonical 主章节为：`概要`、`核心方法与创新机理`、`实验与关键发现`、`定位与知识库关联`、`原文 PDF`。
- frontmatter 必备键按 v06 基线检查；缺失的 `project_link` / `code_link` 写 `null`，不从猜测补 URL。
- `pdf_ref` 与 PDF embed 使用 vault 相对路径 `paperPDFs/...`；图片使用 `assets/figures/papers/...`，禁止 `obsidian-vault/`、绝对路径和 `../` 前缀。
- 保留现有 source anchors、公式、指标和论文内编号；结构迁移不得造成证据锚点丢失。

### B. Links 有效性

- 检查 Markdown 语法、URL scheme、重复链接和显示标签；统一论文入口显示为 `paper`。
- paper URL 优先采用现有 `paper_list.csv` 的对应记录；无法匹配时保留原 URL 并标记复核，不联网猜测替换。
- `project_link` / `code_link` 与元数据表保持一致；同 URL 不重复展示。
- 本地 wikilink/embed 必须实际存在。断开的图片 embed 删除或改到能够唯一确认的现有资产；断开的 PDF embed 只在能由 `pdf_ref` 或文件名唯一解析时修复，否则进入异常清单。

### C. 图片保留与删除

不使用“超过 6 张即机械截断”。按信息角色排序：

1. 必留：总体方法/系统管线图。
2. 优先保留：主结果表、关键消融、能解释核心机制的图、代表性定性对比。
3. 通常删除：补充数据集结果、更多可视化样例、重复尺度/视角、训练细节截图、与正文结论重复的多张表。
4. 若论文核心贡献本身依赖多个阶段或多类定性证据，可超过 6 张，但必须在变更日志中说明。
5. 默认目标为 3–6 张；零图笔记不为凑数而添加图片。
6. 删除 embed 时一并删除其 caption；长英文 caption 压缩为中文信息标签，保留 Figure/Table 编号与关键结论。

### D. 内容去冗余

- 把旧七段式内容映射到 v06 四个分析章节，合并重复的“概述/背景/核心创新/整体框架”叙述。
- 同一指标不在概要、效果简介和实验章节反复展开；效果简介保留结论，实验章节保留证据与解释。
- 不删除公式推导中的必要定义，不自行修正看似可疑但无法由现有笔记确认的数值。
- 对证据不足、链接无法唯一修复、图片角色不明确的项目标记 `manual_review`，不静默猜测。

## 执行分级与批次

### 运行声明（2026-07-13）

- goal: 将目标分析笔记迁移到 v06.1 结构，修复链接/embed，并按语义角色清理冗余图片。
- source: v06 分析链、两篇 canonical 范例、现有 analysis note；禁止读取原 PDF。
- selection rule: 非 canonical 主集合；canonical 笔记仅在存在 P0/P1 检测项时参与。
- budget: 校准批次 20 篇；通过后每批 50 篇，最多 3 个互斥 batch 并行。
- output target: `obsidian-vault/analysis/*/*.md`；manifest 与批次报告写入 `_private/BITE_versions/v06.1/runs/2026-07-13/`。
- state rule: 单篇 deterministic validation 与批次复查均通过后，才允许 `analysised → checked`。

每篇先分类，再修改：

- P0：断 PDF/图片 embed、frontmatter 无法解析、缺 PDF 章节。
- P1：旧结构迁移、链接冲突、12 图模板堆叠、明显重复章节。
- P2：caption 过长、轻微格式不一致、非关键冗余。
- Skip：已 canonical 且无检测问题。

建议每批 50 篇，先做一个 20 篇校准批次，其中包含旧结构、12 图、断链和 canonical 保护样本。校准批次经人工确认后再锁定 prompt、规则与批量预算。

每批输出：输入清单、修改清单、跳过清单、异常清单、修改前后图片数、链接修复数、结构迁移数和验证结果。批次失败不得影响已完成批次。

## Dry-run 与最终验证

执行前先生成不写库的 manifest，至少包含：

- note path、集合来源、结构版本、图片数、补充图片标题、断链数、缺失字段、建议优先级；
- 预计参与总数以及按 venue/year 的分布；
- 20 篇校准样本名单。

写库后执行：

1. YAML 和必备字段校验。
2. canonical 章节及 PDF embed 校验。
3. 全部本地 embed 解析校验。
4. Markdown 表格中未转义 wikilink alias 分隔符检查。
5. 图片 caption 孤儿、重复 Links、旧 `[arXiv]` 标签和绝对路径检查。
6. 修改 diff 审计：只允许目标分析笔记与批次报告变化。

## 状态迁移

当前状态语义调整为：

```text
Wait → Downloaded → analysised → checked
```

`analysised` 表示分析笔记已生成并通过 deterministic export validation，但尚未完成本轮内容质量复查。校准和全量复查通过后，才将对应行从 `analysised` 提升为 `checked`。

## 待敲定事项

1. 是否接受“结构版本 + 可证实创建日期”的联合选择器，而不是仅依赖不可靠的文件日期。
2. 是否接受默认 3–6 张、允许有理由超过 6 张的图片规则。
3. 校准批次确认后，是全量自动推进，还是每个 50 篇批次抽查后继续。

## 执行结果（2026-07-13）

- 全库扫描：5,345 篇顶层 paper notes。
- 校准：20 篇，拆为 7/6/7 三个并行批次并逐篇验证。
- 确定性全量 pass：3,466 篇候选，拆为 1,131/1,147/1,188 三个 shard。
- 结构结果：5,341 篇满足严格 v06 canonical；剩余 4 篇均为运行启动前已有用户修改，未覆盖。
- 图片语义复查：2,906 篇，59 个 50 篇以内批次，多 agent 轮转完成。
- 最终图片数：41,414；仅删除高置信冗余图及配套 caption，超过 6 张但承担独立证据角色的图片予以保留。
- 本地 embed：剩余 1 个缺失 PDF，且无唯一候选，保守保留为 blocker。
- 状态：4,232 条 `analysised` 提升为 `checked`；82 条因无唯一映射、冲突映射或启动前 dirty 保持 `analysised`。
- 未读取原 PDF；未覆盖 5 篇启动前 dirty analysis notes。

详细 manifest、批次报告、备份和状态映射位于 `_private/BITE_versions/v06.1/runs/2026-07-13/`。
