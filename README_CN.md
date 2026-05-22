<p align="center">
  <img src="./assets/LOGO.png" alt="ResearchFlow logo" width="280"/>
</p>

<h1 align="center">ResearchFlow</h1>

<p align="center"><strong>面向研究 Agent 的结构化论文分析与 Research Memory</strong></p>

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

> 🔥 **ResearchFlow 社区交流** | **[💬 微信交流 / ResearchFlow微信交流群](./WECHAT_CN.md)**

---

> 🧠 **先构建知识，再让 Agent 行动。** 大多数 AI 科研工具关注“帮你跑实验、写论文”。ResearchFlow 更关注上游问题：**你的 agent 在做决策时，手里有没有足够的、结构化的、可检索的论文证据？**
>
> 🧩 **把结构化论文分析沉淀为可复用的 research memory。** ResearchFlow 会把论文 PDF 和论文列表整理成本地知识库：结构化分析笔记、轻量索引、Obsidian 友好的导航页面，以及后续 idea 或 review notes。
>
> 🪶 **本地优先，低锁定。** 当前默认 workflow 是 **local files only**：PDF、Markdown 笔记、JSONL 索引和 idea notes 都放在 `obsidian-vault/` 下。正常使用不需要 API server、数据库或服务部署。

💡 _ResearchFlow 是一种方法论和本地知识工作流，不是封闭平台。真正有价值的是你持续积累的 research memory。_

## 🔭 当前目标

- [X] 发布更强的论文分析模板，让论文理解更结构化、可比较、可复用。
- [ ] 提升从候选论文到维护索引的自动化程度。
- [ ] 发布高质量论文分析知识库，支持 human-in-the-loop 研究。
- [ ] 改进结构化 metadata，支持检索、过滤和跨论文对比。

## 🎯 不只是 prompt，而是完整的知识管线

给 ResearchFlow 一个研究方向，它可以帮你把知识库逐步建起来：

```text
collect candidate papers / import local PDFs
  -> download when needed
  -> MinerU PDF parse
  -> structured paper analysis
  -> index
  -> query / ideate / review / export
```

### 正式分析链

- MinerU 对每篇 PDF 解析一次；已有解析结果会优先复用。
- 解析出的 Markdown 会被切分成 chunks，再做 chunk-level anchor extraction，
  收集有出处的证据，而不是直接做整篇摘要。
- 主分析阶段合并 anchors、紧凑论文上下文和图表信息，生成 verified JSON。
- Section writers 基于 verified evidence 生成七个报告章节。
- Vault 导出、图片放置、索引刷新和 audit 在适用时作为确定性的本地检查执行。

每个阶段的细节、reasoning 设置、validation 规则和实测成本/耗时见
[正式本地分析链详情](docs/formal-analysis-chain.md)。

你可以用四种常见模式使用它：

| 模式     | 用途                                                    | 常用入口                                                                        |
| -------- | ------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Build    | 收集候选论文、下载 PDF、分析论文并刷新索引              | `research-workflow`                                                           |
| Query    | 按主题、任务、方法、venue、年份、标题或技术标签检索论文 | `papers-query-knowledge-base`                                                 |
| Decision | 在选择 baseline、修改方案或写 related work 前对比方法   | `papers-query-knowledge-base`                                                 |
| Idea     | 基于本地知识库生成、收敛并压力测试研究方向              | `research-brainstorm-from-kb`, `idea-focus-coach`, `reviewer-stress-test` |

适合以下场景：

- 从网页、GitHub 论文列表或本地 PDF 文件夹构建特定方向的论文知识库。
- 将 PDF 转换为结构化分析笔记，保留可比较字段、证据 anchor、公式、表格、
  figure/table metadata 和 reading-order context。
- 在选择 baseline、写 related work 或调整研究方案前，对比不同方法。
- 基于已有论文生成研究想法，收敛为可执行计划，并用 reviewer 视角做压力测试。
- 导出可分享 Markdown，或在 Obsidian 中浏览知识库。

## 🏗️ 三层架构

```text
┌─────────────────────────────────────────────────────────┐
│  输出层              obsidian-vault/ideas/              │
│                      ideas, plans, review notes          │
├─────────────────────────────────────────────────────────┤
│  索引层              obsidian-vault/index/              │
│                      JSONL index + Obsidian pages        │
├─────────────────────────────────────────────────────────┤
│  证据层              obsidian-vault/analysis/           │
│                      structured notes + logs             │
│                      obsidian-vault/paperPDFs/           │
│                      source PDFs                         │
└─────────────────────────────────────────────────────────┘
```

- `obsidian-vault/paperPDFs/` 存放原始 PDF。
- `obsidian-vault/analysis/` 存放每篇论文的结构化分析笔记和日志。这是 Agent
  最应该读取的证据层。
- `obsidian-vault/index/` 存放生成的检索索引和导航页面。规模较大时，
  Agent 应先读 `index.jsonl` 过滤候选，再读取对应 analysis notes。
- `obsidian-vault/ideas/` 存放后续研究输出，例如 brainstorm notes、聚焦计划、
  reviewer critiques 和 daily logs。
- Obsidian 是可选的，只是浏览和 backlink 层；仓库作为普通本地文件夹也能工作。

## 🤖 Agent 兼容

ResearchFlow 有意保持朴素：文件夹、Markdown、JSONL、CSV 和 `SKILL.md`。因此同一
份 research memory 可以被多个 Agent 共享：

- Claude Code / Cursor 可以直接读取 `.claude/skills`。
- Codex CLI 可以用 `scripts/setup_shared_skills.py` 生成本地 alias。
- 其他能读取文件的 Agent 可以直接读取 `obsidian-vault/index/index.jsonl`
  和 `obsidian-vault/analysis/`，无需特殊集成。

## 🚀 快速开始

ResearchFlow 的用户可能在 macOS、Windows 或 Linux 上工作。默认分析 workflow
不强依赖 `jq`、`curl`、`make` 这类系统命令。PDF 相关的 Poppler、Ghostscript
已经写在 Conda 环境中，不需要在 README 里按某个系统单独安装。

### 1. 创建 conda 环境

```bash
git clone https://github.com/<your-username>/ResearchFlow.git
cd ResearchFlow

conda env create -f environment/environment.yml
conda activate researchflow
```

### 2. 配置模型和解析工具

大多数本地操作不需要提交配置文件。需要设置模型密钥、模型名或 parser override
时，在仓库根目录创建自己的 `.env`，并参考
[environment/.env.example](environment/.env.example)。不要把密钥写进
`.env.example`。

常见 OpenAI-compatible 变量：

```dotenv
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
```

### 3. 安装或配置 MinerU

正式论文分析推荐使用 MinerU。请让 Agent 根据你的机器安装、配置并验证 MinerU，
不要在 README 中按长篇手工步骤操作。

最小验证方式：`mineru --help` 能运行，或在 `.env` 中设置 `MINERU_CLI_PATH`
指向 MinerU 可执行文件。

### 4. 准备 Agent Skills

Claude Code 和 Cursor 可以直接读取 `.claude/skills`。如果需要 Codex 兼容路径，
运行：

```bash
python3 scripts/setup_shared_skills.py
```

然后从统一 workflow skill 开始：

```text
/research-workflow
我想从 PDF 构建 controllable motion generation 的论文知识库。
请告诉我下一步应该做什么，以及会生成哪些结果。
```

默认 workflow 不需要启动任何服务。使用 `obsidian-vault/` 下的本地文件夹作为工作
状态即可。

## 📖 使用示例

从零构建一个主题知识库：

```text
/research-workflow
我想构建 text-driven reactive motion generation 的论文知识库。
请从候选论文收集开始，告诉我每个阶段应该使用哪个 skill。
```

从 GitHub 论文列表收集候选论文：

```text
/papers-collect-from-github-repo
从这个 GitHub repository 收集 controllable human motion generation 相关论文：<URL>
只保留 diffusion、controllability、real-time generation 或 long-form motion 相关条目。
输出适合后续下载 workflow 使用的候选列表。
```

从本地 PDF 文件夹导入 PDF：

```text
/research-workflow
我已经有一批 PDF 放在 /path/to/pdf-folder。
请按 category Motion_Generation、venue CVPR、year 2026
注册到 obsidian-vault/paperPDFs/，然后告诉我应该先分析哪篇。
```

根据候选列表下载 PDF：

```text
/papers-download-from-list
下载当前候选列表中仍标记为 Wait 的论文。
报告成功下载、失败和跳过的数量。
```

为准备好的 PDF 生成深度报告：

```text
/paper-report
为 obsidian-vault/paperPDFs/<Category>/<Venue_Year>/<Paper>.pdf 生成 deep report。
将报告保存在 obsidian-vault/analysis/ 下，并保留 source anchors。
```

需要真实流水线产物和带图表导出的 vault 笔记时，直接运行正式本地分析链：

```bash
python3 scripts/run_local_paper_analysis.py \
  --pdf "obsidian-vault/paperPDFs/<Category>/<Venue_Year>/<Paper>.pdf" \
  --conf-year "<Venue_Year>" \
  --export-vault
```

如果 MinerU 输出已经存在，复用它而不是重新解析：

```bash
python3 scripts/run_local_paper_analysis.py \
  --mineru-output "<mineru_output_dir>" \
  --paper-pdf "obsidian-vault/paperPDFs/<Category>/<Venue_Year>/<Paper>.pdf" \
  --conf-year "<Venue_Year>" \
  --export-vault
```

如果有规范化的 MinerU 缓存，可以让 runner 按 PDF stem 自动发现单篇解析目录：

```bash
python3 scripts/run_local_paper_analysis.py \
  --pdf "obsidian-vault/paperPDFs/<Category>/<Venue_Year>/<Paper>.pdf" \
  --conf-year "<Venue_Year>" \
  --mineru-output-root "<mineru_output_root>" \
  --require-existing-mineru-output \
  --export-vault
```

做受控实验时，保留真实 venue/year 元数据，只用 `--vault-note-dir`
重定向 Markdown 输出目录。

正式本地 runner 是生成流水线产物的默认分析路线。

从论文列表批量分析：

```bash
python3 scripts/run_paper_list_analysis.py \
  --source obsidian-vault/paper_list.csv \
  --state Downloaded \
  --limit 25 \
  --mineru-output-root "<mineru_output_root>" \
  --require-existing-mineru-output
```

更大规模运行时，用 `papers-batch-analyze` 切分列表，并行启动最多 4 个 worker agent。

必要时也可以手动刷新索引：

```bash
python3 .claude/skills/papers-build-index/scripts/build_paper_index.py
```

生成的索引首页是 `obsidian-vault/index/_Index.md`。被 Git 跟踪的
`obsidian-vault/index/README.md` 只作为公开占位说明，builder 不会覆盖它。

如果想在不使用私人论文数据的情况下验证 index/workflow 链路：

```bash
python3 scripts/smoke_index_workflow.py
```

询问文献问题：

```text
/papers-query-knowledge-base
对比 DART、OmniControl 和 MoMask 在 long-horizon controllable generation 上的设计。
重点看表示方式、控制接口和实验证据。
```

基于本地知识库生成想法：

```text
/research-brainstorm-from-kb
我想研究 text-driven reactive motion generation。
请基于已经分析的论文提出 3 个方向。
```

把宽泛想法收敛成可执行计划：

```text
/idea-focus-coach
我的想法是用 diffusion model 做 reactive motion generation，
但我不确定范围应该多大，也不确定第一个实验应该是什么。
请把它收敛成一个可执行 MVP。
```

像 reviewer 一样压力测试想法：

```text
/reviewer-stress-test
请从 ICLR reviewer 的角度 review 我的想法：
[粘贴 idea 描述，或指向 obsidian-vault/ideas/ 下的文件]
重点关注 novelty、实验设计和与 SOTA 的差异。
```

## ✨ 核心能力

维护中的 skill 库位于 `.claude/skills`。

| 需求                       | Skill                                         |
| -------------------------- | --------------------------------------------- |
| 判断下一步 pipeline        | `research-workflow`                         |
| 从本地文件夹导入 PDF       | 把 PDF 文件夹路径提供给 `research-workflow` |
| 从网页收集候选论文         | `papers-collect-from-web`                   |
| 从 GitHub 论文列表收集候选 | `papers-collect-from-github-repo`           |
| 根据 triage list 下载 PDF  | `papers-download-from-list`                 |
| 生成单篇深度报告           | `paper-report`                              |
| 重建本地索引               | `papers-build-index`                        |
| 基于本地笔记查询/对比论文  | `papers-query-knowledge-base`               |
| 基于知识库生成研究想法     | `research-brainstorm-from-kb`               |
| 把想法收敛为可执行计划     | `idea-focus-coach`                          |
| 做 reviewer 风格压力测试   | `reviewer-stress-test`                      |
| 导出可分享 Markdown        | `notes-export-share-version`                |

完整 skill 地图见 [.claude/skills/README.md](.claude/skills/README.md)。

## 仓库结构

```text
ResearchFlow/
├── .claude/skills/                 维护中的 Agent skill library
├── assets/                         公开 logo 和 README 素材
├── environment/                    conda、dotenv 和本地环境文件
├── linkedCodebases/                可选：链接相关本地代码仓库
├── obsidian-vault/
│   ├── paperPDFs/                  本地 PDF
│   ├── analysis/                   每篇论文的结构化分析笔记
│   ├── index/                      生成的 JSONL 索引和导航页面
│   └── ideas/                      ideas、plans、reviews 和 logs
├── scripts/                        设置、维护和审计工具
├── AGENTS.md                       面向 Agent 的本地 workflow 规则
├── README.md                       英文入口
└── README_CN.md                    中文入口
```

生成语料、私人笔记、本地凭据、缓存和大型研究产物不应进入 Git。

## 补充配置

`<a id="codex-cli-compat"></a>`

<details>
<summary>Codex CLI compatibility</summary>

Claude Code / Cursor 不需要这一步；Codex CLI 需要。

仓库不跟踪 `.codex/`。clone 后，在本机生成 `.codex/skills` 和
`.codex/skills-config.json`：

```bash
python3 scripts/setup_shared_skills.py
```

只检查 alias 是否存在、不改动文件：

```bash
python3 scripts/setup_shared_skills.py --check
```

</details>

`<a id="obsidian-config"></a>`

<details>
<summary>Obsidian setup</summary>

- Obsidian 是可选的可视化层，但推荐配置。
- 如果需要 graph view、backlinks 和人工浏览，可以把 `obsidian-vault/` 作为
  Obsidian vault 打开。
- 不要把 Obsidian 页面当作独立 source of truth；它们只是 workflow 生成或维护的
  本地文件。

</details>

ResearchFlow 当前只支持通过 conda 环境和本地命令运行本地文件工作流。

## 数据卫生

- `.env` 只保留在本地，只提交 `environment/.env.example`。
- PDF、生成的分析笔记、生成索引、vault 页面、缓存、模型输出和私有实验不应进入
  源码历史，除非你有意发布经过整理的示例。
- 保持标准 `obsidian-vault/` 布局，这样 Agent 和脚本才能找到预期输入输出。
- 不要把无关论文组混在同一个 category，除非你希望它们在检索时一起出现。
- 发布 fork 或 release 前，建议做一次敏感信息扫描。

## Citation

如果 ResearchFlow 对你的研究有帮助，请直接引用本仓库：

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
