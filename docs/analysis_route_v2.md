# Analysis Route V2

## 1. 旧路线的问题

旧 V6 路线把语义理解拆成 `shallow_extractor`、`reference_role`、`deep_analyzer`、`graph_candidate`、`kb_profiler`、`paper_report` 等多个 semantic agent。这个切分便于工程追踪，但会损害高维理解：

- `shallow_extractor` 容易把摘要和引言压成 TL;DR，过早固化低维贡献叙事。
- `reference_role` 独立运行时缺少方法机制语境，容易把 comparison baseline、method source、same-task prior 混在一起。
- `deep_analyzer` 消费浅层 blackboard 后，容易补全前序叙事，而不是重新诊断真实瓶颈。
- `graph_candidate` / `kb_profiler` 在理解未稳定前生成节点和边，会把 method、task、mechanism 的层次混淆。
- `paper_report` 容易变成 blackboard 综合摘要器，而不是因果诊断后的 writer。

V2 已在主 ingest workflow 中收敛到一个强 `analysis_agent`、一个 `writer_agent`，其余 materialization 尽量 deterministic。

## 2. 新版目标结构

V2 分四层：

| Layer | 职责 | 不做什么 |
|-------|------|----------|
| Parse layer | PDF 事实抽取：markdown、reading order、tables、formulas、figure assets、caption、section text | 不做贡献判断 |
| Analysis truth layer | 一个强 analysis agent 回答 real bottleneck、causal knob、capability delta，并输出 method skeleton、decisive change、trade-off、evidence anchors | 不写长报告 |
| Writer layer | 只把 verified truth 写成可读报告，区分压缩层和展开层 | 不新增 unsupported claims |
| Deterministic materialization | 从 parse output 和 verified truth 生成 DeltaCard、EvidenceUnit、GraphAssertion、paper_report_sections、vault export | 不让 LLM 决定版本/去重/导出过滤 |

当前主链路已经完成 2-agent 重构：`AgentRunner.AGENT_PROMPTS` 和 `ContextPackBuilder.PACK_CONFIGS` 的 active keys 只有 `analysis_agent` / `writer_agent`。旧 `shallow_extract`、`reference_role_map`、`deep_analysis`、`graph_candidates`、`kb_profiles` 仍作为 blackboard item type 存在，但它们是 `analysis_agent` 输出的兼容投影，不再由独立 semantic agent 在主 ingest workflow 中生成。

## 3. MinerU 的位置

MinerU 是 parse layer 默认强解析器，不只是图表裁剪工具。

- Markdown text / reading order: L2 `evidence_spans.mineru_markdown` 进入 deep/report context，用于双栏阅读顺序和方法段落补足。
- Tables: MinerU HTML/CSV 与 table assets 进入 `extracted_tables` 和 `paper_figures`。
- Formulas: MinerU markdown block math / content list formulas 进入 `extracted_formulas`；arXiv TeX 可用时仍可作为零 OCR 来源，但本次最终回灌状态统一以离线 MinerU output 为准。
- Figure assets: MinerU image/chart/table assets 进入 L2 `extracted_figure_images` 与 `paper_figures`，exporter 用这些资产解析 `{{FIG:...}}` / `{{TBL:...}}`。

规则：任何已进入 score、downloaded、L1、L2、L3、L4、checked 阶段的论文，L2 parse 必须强制尝试 MinerU。失败可降级，但 `parse_metadata` 必须记录最终 parser 和 source。

## 4. 字段职责分工

`核心洞察`
: 导出页顶部方法一句话。必须写成 causal chain：what changed -> which bottleneck / constraint changed -> which capability changed。不能只是 TL;DR。

`核心创新`
: report section。只展开 decisive causal knob 和与 baseline 的差异，不列模块清单，不复述 abstract。

`整体框架`
: report section。只讲 system skeleton：input -> module A -> module B -> output，各模块输入、输出、职责。不解释为什么有效，避免和核心创新重复。

`核心直觉`
: 方法直觉层。解释具体模块为什么改变约束、分布或信息流，可比 `核心洞察` 更展开，但仍不能变成贡献点列表。

`core_operator` / `primary_logic` / `claims`
: 压缩检索层字段，服务检索和图谱，不是正文复读。后续应从 analysis truth layer deterministic compression 生成。

## 5. 这 5 篇重分析实际策略

执行环境：`conda run -n RF ...`，`PYTHONNOUSERSITE=1`，显式 DB URL `postgresql+asyncpg://rf:***@127.0.0.1:5432/researchflow`，`ALLOW_LLM_IMAGE_UPLOAD=false`。

| Paper | paper_id | 实际策略 |
|-------|----------|----------|
| AIREAI | `147942cd-6284-4aa7-bddf-a097b112e56f` | 重跑 L2；强制 MinerU fallback；桥接离线 MinerU；重跑 report；重刷 vault |
| 3DGEER | `08f8f231-d7ae-4127-a47d-a5ddb1fea800` | 同上 |
| ADEPT | `8582023f-c0db-48e3-8411-b2b4e1441acc` | 同上 |
| ACE | `a58dd10c-8e25-458e-b37c-1fb35a62eed3` | 同上 |
| AC-Sampler | `c28f1e8c-dcaf-437c-afb4-805e6f6d1803` | 同上 |

本轮还明确执行了 text-only policy：图片资产可以落库和导出，但不会上传给 DeepSeek/LLM writer，也不会放进 agent context 的 URL 字段。

## 6. 已落实到代码

- `backend/config.py`: 新增 `allow_llm_image_upload`，默认 `False`。
- `backend/services/parse_service.py`: score/L2+ 阶段强制尝试 MinerU；VLM figure/formula/table 路径受 `allow_llm_image_upload` 硬门控制；`parse_metadata` 记录 `llm_image_upload_enabled`。
- `backend/services/vlm_extraction_service.py`: 所有带 image payload 的 VLM 调用在默认配置下直接跳过。
- `backend/services/figure_extraction_service.py`: precise VLM figure extraction 默认禁用。
- `backend/services/formula_extraction_service.py`: VLM page/crop OCR 默认禁用，只保留 text/GROBID/MinerU 路径。
- `backend/services/context_pack_builder.py`: active context pack 收敛到 `analysis_agent` / `writer_agent`；writer context 只传 figure label、page、role、type、caption，不传 `public_url` 或 raw image。
- `backend/services/agent_runner.py`: active agent 收敛到 `analysis_agent` / `writer_agent`；writer prompt 要求 `> [!tip] 效果简介`，并保持 `核心创新` / `整体框架` / `module_formulas` 的职责分离。
- `backend/services/analysis_service.py`: L3 prompt 将 method summary 与 core intuition 分离。
- `backend/services/ingest_workflow.py`: 主链路只调用 `analysis_agent` / `writer_agent`；analysis truth 投影为兼容 blackboard item type 后再做确定性 materialization；新报告递增 `report_version`，旧 current report 标记为 `superseded`；批量重分析必须显式使用 `force_reanalyze=True` 才绕过已有 L4 的幂等保护。
- `backend/services/context_pack_builder.py`: writer 只读取每种 verified blackboard item 的最新版本，并加入确定性的 `lineage_positioning_context`，含已落库 paper relations、facets、method profile 摘要。
- `backend/services/vault_export_v6.py`: exporter 优先从 current `core_innovation` 生成顶部 `核心洞察`；current title 查询优先 current report；旧 `### 效果简介` 在导出时转换为 `> [!tip] 效果简介`；无 marker fallback 最多注入少量图表，避免末尾图表堆积。
- `backend/services/report_service.py`: briefing prompt 输入优先包含 current `core_innovation`。
- `scripts/bridge_mineru_local_outputs.py`: 将离线 MinerU markdown/tables/formulas/figure assets 回灌到 current L2、`paper_figures` 并重导出。
- `scripts/reanalyze_and_compare.py`: report snapshot 只统计 current report sections，并保留 total versions。
- `scripts/reparse_target_papers.py` / `scripts/verify_target_reanalysis.py`: 本次 5 篇重跑和核验脚本。
- `requirements.txt`: 增加 `socksio`，修复 SOCKS proxy 下 `httpx`/MinerU API 尝试报错。

## 7. 后续 TODO

- 将 MinerU figure asset upload 纳入通用 `parse_service.py` 主路径；本轮图表资产通过 bridge 脚本落库。
- 继续审计零散读取 `paper_report_sections` 的 ad hoc 查询，确保只读 current/latest。
- 将 `core_operator`、`primary_logic`、`claims` 从 writer prose 中解耦，改由 analysis truth layer 压缩生成。
