---
title: "ResearchFlow x Zotero 接入调研与方案"
created: 2026-04-13T17:34:28
updated: 2026-04-13T17:40:00
scope: private
type: design-note
tags:
  - zotero
  - integration
  - researchflow
  - bibliography
---

# ResearchFlow x Zotero 接入调研与方案

> [!abstract] **TL;DR**
> - 推荐路线不是“让 ResearchFlow 变成另一个 Zotero”，而是让 Zotero 做书目/附件/阅读流入口，ResearchFlow 做结构化分析与 agent 检索层。
> - 一期建议采用“`pyzotero` + Zotero Web API / local API 为主，Better BibTeX 为可选增强，Obsidian 插件不作为硬依赖”的混合方案。
> - 现有 `analysis_log.csv` 只有 8 列，`paperAnalysis/` frontmatter 也缺少 `authors`、`doi`、`citekey`、`zotero_key` 等字段；这些是最明显的接入缺口。
> - 实现上应保持 `analysis_log.csv` 兼容，把 Zotero 富 metadata 放到 `paperAnalysis/processing/zotero/` 的独立 manifest 中，再把必要子集映射进现有 pipeline。

## 一、先下结论

1. ResearchFlow 的强项是“读完 PDF 后的结构化分析、比较、brainstorm、agent 检索”，不是书目采集和引文管理。
2. Zotero 的强项是“收藏入口、metadata 清洗、PDF/批注、引用样式和 group library”，不是下游研究知识层。
3. 因此最合理的边界是：
   - Zotero = bibliographic source of truth
   - ResearchFlow = analytical source of truth
4. 接入不应以 Obsidian 插件为中心，因为 ResearchFlow 的核心不是“把 Zotero note 渲染成 Markdown”，而是“把文献入口稳定地转成可分析、可增量维护的知识库对象”。

## 二、ResearchFlow 当前状态与接入缺口

### 2.1 当前仓库观察

截至 2026-04-13，本地仓库现状：

- `paperAnalysis/` 下已有 20 篇分析笔记。
- `paperPDFs/` 下已有 20 个 PDF。
- `paperCollection/` 下已有 26 个导航页。
- `paperAnalysis/analysis_log.csv` 当前只有 8 列：
  - `state`
  - `importance`
  - `paper_title`
  - `venue`
  - `project_link_or_github_link`
  - `paper_link`
  - `sort`
  - `pdf_path`

`paperAnalysis/*.md` 的 frontmatter 当前主要包含：

- `title`
- `venue`
- `year`
- `tags`
- `core_operator`
- `primary_logic`
- `claims`
- `pdf_ref`
- `category`

### 2.2 ResearchFlow 已有优势

- 本地优先：Markdown + CSV + PDF，没有数据库和后端依赖。
- agent 友好：核心信息以 frontmatter 和固定模板沉淀，不依赖单次对话上下文。
- 结构化深度高：`core_operator`、`primary_logic`、`claims` 这类字段，明显强于一般的引用/批注工具。
- 下游能力完整：collect、download、analyze、index、query、compare、idea、review 形成闭环。
- 与 Obsidian 兼容，但又不被 Obsidian 绑定。

### 2.3 现阶段缺口

- 没有 Zotero item identity：
  - 缺少 `zotero_key`
  - 缺少 `zotero_library_id` / `zotero_library_type`
  - 缺少 item 级 provenance
- 缺少书目字段：
  - `authors`
  - `doi`
  - `url`
  - `abstract`
  - `citekey`
- 缺少 Zotero collection/tag 到 RF 分类体系的映射。
- 缺少 Zotero note / annotation 的导入落点。
- 缺少增量同步机制；目前 intake 更偏网页/GitHub/PDF 驱动。
- 现有 `analysis_log.csv` 很轻，直接塞入过多 Zotero 字段容易破坏已有脚本兼容性。

## 三、GitHub 相关开源方案调研

### 3.1 相关项目对比

| 项目 | 角色 | 维护信号（截至 2026-04-13） | 核心优势 | 主要要求 | 对 ResearchFlow 的价值 | 局限/判断 |
| --- | --- | --- | --- | --- | --- | --- |
| ResearchFlow | 本地研究知识库与 agent workflow | 当前本地仓库；20 篇 analysis；20 个 PDF | 结构化分析、对比、检索、idea 生成、Obsidian 兼容 | Python 3.10+；本地文件系统；可选 Obsidian | 提供 Zotero 下游分析层 | 不是书目管理器；缺少 bibliographic sync |
| [zotero/zotero](https://github.com/zotero/zotero) | Zotero 官方桌面端 | 13.9k stars；2026-04-10 推送 | 收藏、组织、批注、引用、附件与 group library 能力完整 | Zotero 桌面端；其自身数据目录与同步体系 | 是 RF 最自然的上游 source of truth | 不提供 RF 这种结构化分析知识层 |
| [retorquere/zotero-better-bibtex](https://github.com/retorquere/zotero-better-bibtex) | 引文键与导出增强 | 6.5k stars；2026-04-13 推送 | 稳定 citekey、自定义导出、auto export、pull export | Zotero 插件；Zotero 8+ 更合适 | 适合作为 citekey 与导出增强层 | 不负责 RF 的知识建模；Zotero 8 已有原生 citation key，BBT 不应成为唯一前提 |
| [obsidian-community/obsidian-zotero-integration](https://github.com/obsidian-community/obsidian-zotero-integration) | Obsidian 导入插件 | 1.6k stars；2026-03-06 推送 | 把 citation、bibliography、notes、PDF annotations 导入 Obsidian；模板灵活 | Obsidian；Better BibTeX；模板配置；注释抽取依赖外部工具 | 适合作为“annotation/notes 到 Markdown”的参考实现 | 更像个人笔记导入器，不是批量知识库同步器 |
| [windingwind/zotero-better-notes](https://github.com/windingwind/zotero-better-notes) | Zotero 端笔记工作流增强 | 7.6k stars；2026-04-11 推送 | note template、Markdown 双向同步、导出、多种 API、自动化工作流 | Zotero 8/9；插件生态 | 若未来做 Zotero 端插件/自动回写，这是最值得参考的能力面 | 能力强但偏“Zotero 内部 note OS”，不宜作为 RF 的硬依赖 |
| [urschrei/pyzotero](https://github.com/urschrei/pyzotero) | Python API client | 1.3k stars；2026-04-08 推送 | 最贴合 RF 现有 Python 脚本体系；支持 Web API、本地读取模式、CLI、MCP | Web API 需 API key + library ID；本地模式需允许 local API | 最适合做 RF 的主同步桥 | 需要自己设计 manifest、映射规则、增量状态 |
| [kujenga/zotero-mcp](https://github.com/kujenga/zotero-mcp) | AI/agent live query bridge | 142 stars；2025-05-10 推送 | 直接把 Zotero 暴露给 MCP client；支持 metadata / fulltext tools | MCP client；local API 或 Web API；部分 fulltext 依赖 Beta | 适合未来让 agent 直接查 live library | 适合交互式检索，不适合作为稳定批量 ingestion 主链路 |
| [argenos/zotero-mdnotes](https://github.com/argenos/zotero-mdnotes) | 旧式 Markdown 导出插件 | 1.4k stars；已 archived；2024-10-18 最后推送 | 把 item metadata 和 notes 导出为 Markdown；批量导出思路清晰 | 老版 Zotero；常配合 Zotfile 与 Better BibTeX | 可参考其“导出到 Markdown”的设计 | 仓库已归档，且 README 明确不兼容 Zotero 7，不应采用 |
| [MunGell/ZotServer](https://github.com/MunGell/ZotServer) | 本地 HTTP bridge | 112 stars；2022-07-11 最后推送 | 提供 local-only HTTP API，说明“桌面应用桥接 Zotero”这条路线可行 | Zotero 插件 | 可作为“本地桥”架构参考 | 更新停滞，适合作为参考而非依赖 |

### 3.2 功能能力矩阵

| 能力 | ResearchFlow | Zotero 官方/BBT | Obsidian Zotero Integration | Better Notes | Pyzotero |
| --- | --- | --- | --- | --- | --- |
| 书目信息管理 | 弱 | 强 | 中 | 中 | 中 |
| PDF/附件管理 | 中 | 强 | 中 | 中 | 中 |
| 引文键 / BibTeX | 弱 | 强 | 依赖 Zotero/BBT | 中 | 弱 |
| 高亮/批注抽取 | 弱 | 中 | 强 | 强 | 中 |
| Markdown/Obsidian 输出 | 强 | 弱 | 强 | 强 | 弱 |
| 结构化深度分析 | 强 | 弱 | 弱 | 弱 | 弱 |
| 批量脚本化同步 | 中 | 中 | 弱 | 中 | 强 |
| agent 直接检索 | 强 | 弱 | 弱 | 弱 | 中 |
| 双向同步潜力 | 中 | 中 | 弱 | 强 | 中 |

### 3.3 对这些方案的判断

- 最适合做 ResearchFlow 主桥的是 `pyzotero`。
  - 原因：ResearchFlow 现有自动化以 Python 脚本为主，最容易接入现有 `scripts/` 体系。
- 最适合做 citekey/导出增强的是 `Better BibTeX`，但它不应是强制依赖。
  - 原因：Zotero 8 已有 native citation key 字段，BBT 的核心增益更多在 auto export 和高级导出。
- 最适合参考 annotation/Markdown 模板链路的是 `Obsidian Zotero Integration`。
- 如果未来要做 Zotero 端插件或回写工作流，`Better Notes` 是最值得研究的对象。
- `MCP` 方案适合“让 agent 直接查活库”，不适合替代 deterministic batch sync。
- `mdnotes` 和 `ZotServer` 更适合当历史参考，不适合当主依赖。

### 3.4 补充判断

- [jbaiter/zotero-cli](https://github.com/jbaiter/zotero-cli) 提供了一个有价值的 CLI 交互模型：
  - 搜索 item
  - 编辑 notes
  - 启动 attachment 阅读
  - 但其更新明显慢于 `pyzotero`，更适合作为 UX 参考，而不是 RF 的主桥。

## 四、ResearchFlow 接入 Zotero 的需求拆解

### 4.1 P0：必须先满足的需求

- 从 Zotero library / collection / tag 增量导入候选论文到 ResearchFlow。
- 自动解析并映射以下字段：
  - 标题
  - 作者
  - venue / publicationTitle
  - year
  - DOI / URL
  - tags
  - collections
  - attachment path
- 能把 PDF 落到 `paperPDFs/`，或至少把已有本地附件路径映射成 `pdf_path`。
- 保留可追踪 identity：
  - `zotero_key`
  - `zotero_library_id`
  - `zotero_library_type`
  - `dateModified` / `version`
- 支持增量同步，避免每次全量重扫。
- 不破坏现有 `analysis_log.csv` 与 `papers-analyze-pdf` 流程。

### 4.2 P1：高价值但可第二阶段做的需求

- 导入 child notes、PDF annotations、highlight comments。
- 支持把 Zotero tag / collection 自动映射到 RF `sort` 与 frontmatter tags。
- 支持 group library。
- 支持基于 `since` / version 的真正增量同步。
- 在 `paperAnalysis/*.md` 中保留回链字段，如 `citekey`、`doi`、`zotero_key`。

### 4.3 P2：可选增强

- 把 ResearchFlow 的分析摘要或状态写回 Zotero note/tag。
- 给 agent 提供 live Zotero query 能力（MCP）。
- 做 Zotero 插件，在 item add/modify/delete 时触发同步。
- 把 Zotero 阅读阶段和 ResearchFlow 分析阶段形成完整状态机。

## 五、推荐的架构边界

### 5.1 Source of truth 分工

- Zotero 负责：
  - bibliographic metadata
  - creators
  - DOI / URL / citation key
  - collections / tags
  - PDF attachments
  - highlights / notes
  - reading workflow
- ResearchFlow 负责：
  - `analysis_log.csv`
  - `paperPDFs/` 的归一化落盘
  - `paperAnalysis/` 结构化分析
  - `paperCollection/` 导航层
  - 下游 compare / idea / review / code-context 工作流

### 5.2 不建议做的事情

- 不建议把 Zotero SQLite 当主接口。
  - 官方文档明确建议优先使用 Web API 或 JavaScript API；SQLite 只应只读访问，且 schema 可能随版本变化。
- 不建议把 Obsidian 插件当作 RF 的主同步链路。
  - 它们更适合个人阅读笔记导入，不适合作为批量、可复现的知识库 intake 协议。
- 不建议一开始就做重型双向同步。
  - 双向改写最容易造成 source-of-truth 混乱。

## 六、推荐方案：Hybrid，但以 Python/API 为主

### 6.1 方案对比

| 方案 | 描述 | 优点 | 问题 | 结论 |
| --- | --- | --- | --- | --- |
| A. Obsidian 插件优先 | 让 Zotero -> Obsidian 插件输出 Markdown，再被 RF 吸收 | 对单人笔记友好；模板现成 | 依赖 Obsidian；难保证批量、一致、可增量 | 不推荐作为主链路 |
| B. BBT 导出优先 | 用 Better BibTeX auto export / pull export 产出文件，再由 RF ingest | 简单；citekey 稳定；本地友好 | 对 notes/annotations 支持弱；对复杂 mapping 不够直接 | 可作为增强层 |
| C. API 优先 | 用 `pyzotero` 读 Web API / local API，RF 自己生成 manifest 和映射 | 最贴合现有脚本体系；可做增量；控制力最强 | 需要自己实现字段映射与状态管理 | 推荐主链路 |
| D. Zotero 插件优先 | 直接写 Zotero 插件，用 JS API / notification 做实时同步 | 实时性最好；能监听 add/modify/delete | 实现与维护成本高；会把 RF 深度绑到 Zotero | 适合后续高级版，不适合一期 |

### 6.2 最推荐的落地形式

一期推荐：

1. 主桥：`pyzotero`
2. 数据源：
   - 本地桌面场景：优先 local API
   - 远程 / 群组 / CI 场景：退回 Zotero Web API
3. 可选增强：
   - `Better BibTeX` 负责 citation key 和 auto export
4. 不作为硬依赖：
   - Obsidian Zotero Integration
   - Better Notes
   - MCP

### 6.3 为什么是这个组合

- `pyzotero` 最符合 ResearchFlow 现有 `scripts/` 结构。
- Web API 支持 `since` 增量同步思路以及 `bibtex`、`biblatex`、`csljson`、`csv` 等导出格式，适合 manifest + 增量缓存。
- local API 适合本地优先、无额外 API key 的工作流。
- BBT 可以把 citekey 和导出做强，但不会把 RF 锁死在某个 Zotero 插件上。
- JavaScript API 的 notification system 说明“未来做 Zotero 插件实时同步”是可行的，但没必要在一期就承担这部分复杂度。
- 这套组合不会让 ResearchFlow 偏离“文件驱动、agent 可复用、Obsidian 可选”的原始定位。

## 七、具体的数据流建议

### 7.1 建议的数据流

```text
Zotero Library
  -> scripts/zotero/sync_library.py
  -> paperAnalysis/processing/zotero/<sync_stamp>/
     - library_manifest.jsonl
     - attachments.csv
     - notes_annotations.jsonl
     - sync_report.md
  -> 映射出新增/更新项
  -> append / update paperAnalysis/analysis_log.csv
  -> 复制或链接 PDF 到 paperPDFs/
  -> 继续走 papers-analyze-pdf
  -> 在 paperAnalysis/*.md 中写入 Zotero provenance 字段
```

### 7.2 为什么要单独建 manifest，而不是直接扩充 `analysis_log.csv`

因为 `analysis_log.csv` 现在本质是轻量 triage 表，不是 rich metadata database。

如果直接把 Zotero 所有字段塞进 `analysis_log.csv`，会带来三个问题：

- 现有脚本与 skill 对列数和列名的隐式假设可能被打破。
- CSV 会迅速变成“半结构化数据库”，难维护。
- Zotero 的 notes / annotations / collection path 本来就不适合压平到一张短表。

因此更稳妥的做法是：

- `analysis_log.csv` 继续只保存下游 pipeline 需要的最小字段。
- Zotero 的富 metadata 进入 `paperAnalysis/processing/zotero/` 的 `jsonl/csv` manifest。
- 分析完成后，只把少量稳定字段写入 `paperAnalysis/*.md` frontmatter。

### 7.3 字段映射建议

| Zotero 字段 | 建议落点 | 说明 |
| --- | --- | --- |
| `key` | `zotero_key` | item identity，必须保留 |
| `library.id` / `library.type` | `zotero_library_id` / `zotero_library_type` | 兼容 personal / group library |
| `version` / `dateModified` | manifest 增量状态 | 用于增量同步 |
| `title` | `paper_title` / `title` | 直接映射 |
| `creators` | `authors` | 新增到 frontmatter，建议字符串列表 |
| `publicationTitle` / `conferenceName` / `proceedingsTitle` | `venue` | 需要一层正规化 |
| `date` | `year` | 正规化成整数年份 |
| `DOI` | `doi` | 新增 frontmatter 字段 |
| `url` | `paper_link` 或 `project_link_or_github_link` | 需要区分 paper URL 与 project URL |
| `collections` | `sort` + `zotero_collections` | `sort` 用规则映射；原 collection path 原样保留 |
| `tags` | `tags` + `zotero_tags` | RF tags 与 Zotero tags 分层保存 |
| PDF attachment path | `pdf_path` / `pdf_ref` | 归一化到 `paperPDFs/` |
| child notes | `notes_annotations.jsonl` 或单独 markdown | 先做 staging，不必一开始写进分析正文 |
| annotations | `notes_annotations.jsonl` 或 `annotations.md` | 后续再决定是否模板化注入分析笔记 |
| citation key | `citekey` | 若存在 BBT 或 Zotero 8 native citekey，则保存 |

### 7.4 建议新增的 frontmatter 字段

以下字段建议新增为“可选字段”，不破坏现有 schema：

```yaml
authors:
  - "First Last"
doi: "10.xxxx/xxxx"
url: "https://..."
citekey: "author2025paper"
zotero_key: "ABCD1234"
zotero_library_id: "1234567"
zotero_library_type: "user"
zotero_collections:
  - "Inbox/Motion"
  - "ToRead/Scaling"
zotero_tags:
  - "to-read"
  - "important"
```

这些字段的价值是：

- 让 `paperAnalysis/` 里的笔记可以回溯到 Zotero 原始对象。
- 方便以后做导出、分享、引用、回写。
- 不影响现有按 `core_operator` / `primary_logic` / `tags` 的检索逻辑。

## 八、建议的一期实现顺序

### Phase 1：最小可用同步

目标：让 Zotero collection 可以一键变成 ResearchFlow 的候选列表。

- 新增 `scripts/zotero/sync_library.py`
- 支持：
  - 读取 user / group library
  - 按 collection / tag 过滤
  - 输出 `library_manifest.jsonl`
  - 生成 `sync_report.md`
  - 把必要字段映射到 `analysis_log.csv`
- PDF 先做“复制或软链接到 `paperPDFs/`”二选一
- 不做 write-back
- 不做复杂 annotation 模板

### Phase 2：附件与批注增强

目标：让阅读痕迹进入 ResearchFlow，但不污染主分析文本。

- 导入 child notes 与 PDF annotations 到 `paperAnalysis/processing/zotero/`
- 为每个 item 生成一个 staging note：
  - `paperAnalysis/processing/zotero/items/<zotero_key>.md`
- 后续 `papers-analyze-pdf` 或新 skill 可以选择性读取这些 staging notes 作为辅助证据

### Phase 3：live agent access 与回写

目标：让 agent 可以一边查 live library，一边更新 RF。

- 引入 `zotero-mcp` 作为可选 live query bridge
- 评估是否需要 Zotero 插件：
  - 监听 add/modify/delete
  - 自动打 tag
  - 可选写回 summary / analysis status

## 九、对 skill / repo 结构的建议

### 9.1 建议新增脚本目录

```text
scripts/zotero/
  sync_library.py
  normalize_items.py
  import_annotations.py
  write_manifest.py
```

### 9.2 建议新增处理目录

```text
paperAnalysis/processing/zotero/
  <sync_stamp>/
```

理由：

- 已经存在 `paperAnalysis/processing/github_awesome/` 的先例。
- Zotero 同步本质上也是 intake processing，而不是最终 evidence note。
- 把原始同步产物和最终 `paperAnalysis/*.md` 分层，便于审计与重放。

### 9.3 建议新增 skill

后续可以考虑新增：

- `papers-sync-from-zotero`
  - 负责：从 Zotero ingest 到 `analysis_log.csv` + `paperPDFs/`
- `papers-import-zotero-annotations`
  - 负责：把 child notes / highlights 导入 processing 层

这样比把 Zotero 逻辑塞进现有 `papers-download-from-list` 或 `papers-analyze-pdf` 更干净。

## 十、风险与开放问题

- collection 到 `sort/category` 的映射是手工配置，还是自动推断？
- PDF 是复制、硬链接还是软链接？
  - 复制最稳，但占空间。
  - 链接更省空间，但跨平台与移动性要考虑。
- Zotero tag 是否直接映射到 RF `tags`？
  - 不建议全量直通，容易污染现有 tag 体系。
- 是否把 annotations 直接写入分析笔记正文？
  - 一期不建议。更稳的做法是先做 staging，再由分析流程选择性吸收。
- 是否强依赖 Better BibTeX？
  - 不建议。应把它作为增强项，而非进入门槛。
- 是否做双向同步？
  - 二期之前不建议。

## 十一、最终建议

ResearchFlow 接入 Zotero 的正确方向不是“再做一个 Obsidian 笔记插件”，也不是“把 Zotero 元数据整表塞进现有 CSV”。

更稳、更符合 ResearchFlow 定位的做法是：

1. 把 Zotero 视为上游 bibliographic / reading system。
2. 用 `pyzotero` + Web API / local API 建立稳定的、可增量的 intake bridge。
3. 保持 `analysis_log.csv` 轻量，把 rich metadata 放进 `paperAnalysis/processing/zotero/`。
4. 只把少量稳定 provenance 字段写回 `paperAnalysis/*.md`。
5. 把 BBT、Better Notes、MCP 都当成可选增强，而不是基础依赖。

如果只做一期，我会建议把目标收敛成一句话：

> 让 Zotero collection 中“值得分析”的论文，能够零手工地进入 ResearchFlow 的 `analysis_log.csv`、`paperPDFs/` 和后续分析流程。

## 十二、参考链接

### ResearchFlow 仓库内参考

- `README_CN.md`
- `AGENTS.md`
- `paperAnalysis/analysis_log.csv`
- `paperAnalysis/processing/github_awesome/`

### 外部 GitHub / 官方文档

- [Zotero 官方仓库](https://github.com/zotero/zotero)
- [Better BibTeX for Zotero](https://github.com/retorquere/zotero-better-bibtex)
- [Obsidian Zotero Integration](https://github.com/obsidian-community/obsidian-zotero-integration)
- [Better Notes for Zotero](https://github.com/windingwind/zotero-better-notes)
- [Pyzotero](https://github.com/urschrei/pyzotero)
- [zotero-cli](https://github.com/jbaiter/zotero-cli)
- [zotero-mcp](https://github.com/kujenga/zotero-mcp)
- [zotero-mdnotes](https://github.com/argenos/zotero-mdnotes)
- [ZotServer](https://github.com/MunGell/ZotServer)
- [Zotero Web API v3](https://www.zotero.org/support/dev/web_api/v3/start)
- [Zotero Web API Basics](https://www.zotero.org/support/dev/web_api/v3/basics)
- [Zotero JavaScript API](https://www.zotero.org/support/dev/client_coding/javascript_api)
- [Direct Access to the Zotero SQLite Database](https://www.zotero.org/support/dev/client_coding/direct_sqlite_database_access)
