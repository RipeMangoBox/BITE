# ResearchFlow 网页端与全球化产品策略备忘录

日期：2026-05-25

目标：思考 ResearchFlow 从本地论文证据工作流升级为服务器部署/网页端产品后，如何覆盖并最终超过 Ponder 的优势维度；同时评估“全球可访问网页”相对“仅国内访问”对产品制作、部署、宣传流程的影响。

方法：基于既有 RF/Ponder 对比、本地架构与部署草案、权威外部资料，并与 DeepSeek `deepseek-reasoner` 进行了 3 轮 max reasoning 讨论。本文采用 research-thinking 的“上限思维、竞品聚焦、逆推思维、跳坑思维”整理。

说明：本文的法律与合规部分用于产品规划和风险识别，不构成法律意见；正式上线前仍应由目标市场的专业律师审阅。

## 0. 先给结论

ResearchFlow 的真实优势不应该表述为“我也有画布、也有上传、也有 Agent”，而应表述为：

> RF 是面向严肃研究的 structured evidence engine。Ponder 强在思考空间和交互，RF 要在交互上追平，但护城河必须仍然是可审计、可复现、可批量扩展的论文证据体系。

如果要公开说“RF 的知识体量和分析深度远超 Ponder”，必须先做实测和可复现 benchmark。否则它只是口号，在全球市场还会带来广告合规风险。更稳的市场表述是：

> ResearchFlow is built for evidence-grounded research memory: every claim traces back to structured paper evidence.

建议路线不是一开始全量追赶 Ponder，而是分阶段：

1. 先上线 PDF 深度分析 SaaS，验证核心价值和付费意愿。
2. 再产品化自然语言检索、引用管理、导出、轻协作。
3. 最后扩展画布、多模态、团队 workspace，形成完整研究工作台。

## 1. 当前基础与机会

### 1.1 RF 已有的强基础


| 能力           | 当前依据                                                                          | 战略价值                                |
| ------------ | ----------------------------------------------------------------------------- | ----------------------------------- |
| 本地证据工作流      | README 强调 structured, searchable paper evidence、local-first、plain files。      | 可以转化为 SaaS 的“可验证证据层”，区别于普通 AI 摘要工具。 |
| 可审计 pipeline | MinerU parse、chunk anchors、verified JSON、deterministic checks、七段报告。           | 支撑“分析深度”和“可信度”主张。                   |
| 多 agent 可读写  | Markdown、JSONL、CSV、SKILL.md、`index.jsonl` 和 `analysis/`。                      | 适合 API-first、MCP、agent ecosystem。   |
| 服务化草案        | PostgreSQL 作为唯一真相源，DeltaCard 不可变中间真相层，UI/导出/Agent 是投影。                        | 已具备从本地文件流迁移到 Web 产品的数据抽象。           |
| 知识图谱设计       | Taxonomy DAG、Method Evolution DAG、Paper Layer、Cross-paper Abstraction；约 40 表。 | Ponder 公开资料未展示同等深度的论文方法演化与证据图谱。     |
| 后端部署草案       | FastAPI、Next.js、PostgreSQL pgvector、Redis、worker、MCP、Caddy、对象存储。              | 技术上具备单主机产品雏形。                       |


### 1.2 Ponder 需要被 cover 的优势


| Ponder 优势              | RF 要 cover 的产品化要求                                           | 风险                                   |
| ---------------------- | ----------------------------------------------------------- | ------------------------------------ |
| 低门槛 Web 产品             | 注册、上传、解析进度、报告查看、自然语言查询要形成完整闭环。                              | 只把 pipeline 放到网页上不等于产品。              |
| 多格式输入                  | PDF 之外支持 Word、图片 OCR、音频/视频转写，至少要有路线。                        | 多模态会稀释论文证据核心，需分阶段做。                  |
| 无限画布/思考空间              | 图谱画布、节点拖拽、证据卡片、人工笔记、分组和连线。                                  | 不要一开始做通用白板，否则与 Ponder/Heptabase 同质化。 |
| Ponder Agent           | RF 需要一个统一 Agent 入口，能提问、比较、整理、导出，并始终显示证据来源。                  | Agent 权限、安全和幻觉控制必须严肃设计。              |
| 团队 workspace           | organization、project、library、成员权限、共享报告、注释。                  | 多租户隔离和权限系统是 P0 架构问题。                 |
| 自然语言问整个收藏              | NLQ 到结构化检索、向量检索、全文检索、多文档对比。                                 | 需要让结果可验证，而不是只给 chat answer。          |
| 引用和参考文献管理              | BibTeX/RIS/CSL 导出，DOI/arXiv/S2/OpenAlex 匹配，引用上下文。           | 外部 API ToS、缓存和署名要核查。                 |
| 导出报告/导图/Markdown/文档/演示 | Markdown、DOCX、PDF、PPTX、mindmap/markmap。                     | 导出质量会影响付费转化，不能只是原始文本下载。              |
| 订阅/积分/高级模型/高峰优先        | usage meter、plans、subscriptions、job priority、model routing。 | 商业化、滥用防护、账单支持会显著增加复杂度。               |


## 2. “超过 Ponder”必须证据化

### 2.1 不要直接上口号

以下说法在公开页面上都需要证据：


| 说法                       | 为什么危险                                             | 替代表述                                                                   |
| ------------------------ | ------------------------------------------------- | ---------------------------------------------------------------------- |
| RF 知识体量远超 Ponder         | 没有实测规模、索引量、更新频率、覆盖范围就不可验证。                        | Built for scalable paper evidence bases.                               |
| RF 分析深度远超 Ponder         | 必须同输入对比，否则是主观判断。                                  | Evidence-grounded structured analysis with traceable anchors.          |
| 完全 cover Ponder          | 现阶段多模态、协作、画布、计费都还未产品化。                            | Covers the evidence layer that generic research workspaces often miss. |
| 最强 AI research workspace | 全球广告语风险高，FTC 要求广告 claims 真实、不误导并有 substantiation。 | A structured evidence workspace for serious research.                  |


### 2.2 建议建立公开 benchmark


| Benchmark | 方法                                                        | 指标                                                                |
| --------- | --------------------------------------------------------- | ----------------------------------------------------------------- |
| 单篇深度分析对比  | 选 5 篇公开论文，同一 PDF 输入 RF 与 Ponder，人工盲审输出。                   | 证据锚点数、结构字段完整率、方法/实验/局限覆盖率、事实错误率、可追溯性。                             |
| 批量体量测试    | 处理 1k、5k、10k 篇论文，记录耗时、失败率、成本、索引查询延迟。                      | throughput、cost per paper、parse failure rate、query latency。       |
| 引用与元数据准确率 | 用 DOI/arXiv/S2/OpenAlex/Crossref 多源验证。                    | title match accuracy、venue/year accuracy、citation match accuracy。 |
| 用户任务测试    | 让研究生完成 related work、baseline comparison、idea stress test。 | 完成时间、可用证据数、主观满意度、二次修正次数。                                          |


## 3. 产品侧注意点

### 3.1 逆推：要真正 cover Ponder，需要哪些模块


| 模块              | MVP 要求                                         | 后续增强                                            | 是否必须首发   |
| --------------- | ---------------------------------------------- | ----------------------------------------------- | -------- |
| 上传与解析           | PDF 上传、队列进度、失败重试、报告生成。                         | Word、图片 OCR、音视频转写。                              | 是        |
| 结构化报告           | 七段报告、证据锚点、PDF 原文跳转、图表/公式面板。                    | 报告版本、人工修订、差异对比。                                 | 是        |
| Evidence Search | 按 paper/method/task/dataset/venue 搜索；NLQ 入口。   | 多文档 compare、claim map、contradiction map。        | 是        |
| Agent           | 问答、总结、比较、导出，必须显示来源。                            | 可执行 research workflow、自动补论文、自动做 literature map。 | 是，但权限要克制 |
| 引用管理            | BibTeX/RIS 导出、reference panel、DOI/arXiv/S2 链接。 | Zotero/Mendeley/EndNote integration。            | 是        |
| 团队协作            | 共享 library、项目成员、评论。                            | 实时协作、活动 feed、权限审计。                              | Beta 后   |
| 画布              | 不做通用画布，先做 graph viewer。                        | 可编辑 canvas、节点笔记、分组、mindmap 导出。                  | Beta 后   |
| 多模态             | 暂不首发，保留接口。                                     | 音视频转写、图片 OCR、截图公式识别。                            | 否        |
| 计费              | Alpha 可邀请制；Beta 接 Stripe。                      | 积分、套餐、发票、团队 seats、高峰优先。                         | Beta 必须  |
| 安全合规            | 删除/导出数据、隐私政策、AI 生成标注、审计日志。                     | 数据区域、企业 DPA、SOC2 准备。                            | 是        |


### 3.2 关键 UX 原则


| 设计点           | 说明                                                                    |
| ------------- | --------------------------------------------------------------------- |
| 上传后立即有反馈      | 解析 PDF 可能慢。必须显示 pipeline 进度：上传、元数据、正文解析、证据抽取、报告生成、索引完成。               |
| 先显示可用中间结果     | 不要等全链路结束才出页面；先显示 metadata、abstract、目录，再逐步填充证据和报告。                     |
| 结构化视图优先       | 默认显示论文报告、证据列表、引用、图表公式。画布不是首屏核心。                                       |
| 每个 AI 结论都可回溯  | 页面上要有 source anchor、PDF 跳转、confidence、模型版本。                           |
| Query 结果不是纯聊天 | 结果应包含 answer、supporting evidence、conflicting evidence、related papers。 |
| 透明展示成本和等待     | 免费用户剩余次数、排队位置、预计完成时间要清晰。                                              |
| 低门槛但不牺牲严肃性    | 首屏不是营销 hero，而是可用的 research workspace。                                 |


### 3.3 架构与数据注意点


| 问题               | 注意点                                                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| 多租户隔离            | 现有 PostgreSQL truth source 要增加 users、organizations、projects、memberships、roles；每条 paper/report/evidence 都要绑定 tenant。 |
| DeltaCard 与删除权   | 不可变快照和 GDPR 删除权冲突。需要软删除、匿名化，或 per-user encryption key，删除密钥即不可恢复。                                                    |
| MCP 暴露面          | MCP SSE 工具必须加 OAuth/API key、scope、rate limit。读写权限分离，高风险写操作需要审计。                                                     |
| Prompt injection | 用户上传论文可能包含恶意指令。LLM 上下文必须隔离，工具调用白名单，输出要做 source-grounding 检查。                                                        |
| 外部 API ToS       | S2、OpenAlex、Crossref、OpenReview、GitHub 等商业使用、缓存和署名规则要逐一核查。                                                          |
| 区域部署             | 全球版至少预留 US/EU 区域。EU 用户数据尽量存 EU，减少 GDPR Article 44 跨境传输复杂度。                                                          |
| 对象存储             | PDF/图片/导出物要有 tenant isolation、signed URL、生命周期清理、virus scan。                                                         |
| 审计日志             | 记录用户操作、模型调用、输入输出摘要、版本、来源，支持合规和用户纠错。                                                                                 |


## 4. 全球可访问 vs 国内优先的影响

### 4.1 核心差异表


| 维度   | 国内优先                           | 全球可访问                                                                     | 影响                                  |
| ---- | ------------------------------ | ------------------------------------------------------------------------- | ----------------------------------- |
| 域名   | `.cn` 或国内备案域名，中文为主。            | 建议主域名 `.com`，英文默认，中文 `/zh` 或子域。                                           | 影响 SEO、品牌认知、备案策略。                   |
| 备案   | 中国大陆服务器通常需要 ICP 备案；经营性服务还涉及许可。 | 海外部署不需要 ICP 才能服务国际用户，但中国大陆访问性能和合规另算。                                      | 如果想同时服务中国大陆和全球，可能需要双部署/双域名。         |
| CDN  | 阿里云/腾讯云国内 CDN。                 | Cloudflare/CloudFront/Fastly 等全球 CDN，必要时双 CDN 智能 DNS。                     | 影响全球延迟、DDoS、防火墙环境、证书和缓存。            |
| 区域部署 | 单区域中国大陆或香港。                    | US/EU 至少预留；企业版可能需要数据区域选择。                                                 | 数据库、对象存储、任务队列都要有 region 概念。         |
| 支付   | 微信、支付宝、CNY、国内发票。               | Stripe/Adyen、信用卡、Apple Pay/Google Pay、VAT/GST、退款。                         | 账单、税务、失败支付、风控和客服复杂度大幅上升。            |
| 合规   | PIPL、数据安全法、网络安全法、ICP、等保视业务而定。  | GDPR、UK GDPR、CCPA/CPRA、EU AI Act、Cookie consent、WCAG、FTC 广告规则。            | 法律文本和产品功能必须同步设计。                    |
| SEO  | 百度、知乎、小红书、中文关键词。               | Google/Bing、英文内容、hreflang、sitemap、structured data、Core Web Vitals。        | 不能后期再补 i18n，否则 URL 和 canonical 会返工。 |
| i18n | 简体中文即可。                        | 英文默认，中文、繁体、日/韩/德/法按市场扩展；法律文本也要多语言。                                        | 前端从第一天就要抽离文案。                       |
| 社媒社区 | 微信群、公众号、知乎、B站、小红书。             | X/Twitter、LinkedIn、Reddit、Hacker News、Discord、YouTube、GitHub Discussions。 | 内容调性从“教程引流”转为“技术信任和社区对话”。           |
| 内容营销 | 中文案例、效率工具、科研方法论。               | 英文技术博客、benchmark、公开对比、开放数据案例、学术 KOL。                                      | 需要可引用证据，不宜夸大竞品对比。                   |
| 用户支持 | 中文群和国内工作时间。                    | 英文 help center、工单、Discord、24h 首次响应 SLA。                                   | 时区与法律/账单问题会变成运营负担。                  |
| 发布节奏 | 可按国内节假日和备案进度安排。                | 需要避开 US/EU 假期，考虑全球发布窗口和搜索引擎收录周期。                                          | 发布前内容和社区预热更重要。                      |


### 4.2 全球优先的 P0 清单


| 优先级 | 动作                                           | 原因                                                                        |
| --- | -------------------------------------------- | ------------------------------------------------------------------------- |
| P0  | 注册并使用 `.com` 主域，设计 `/en`、`/zh` 或英文根路径加中文子路径。 | Google Search Central 建议多语言页面使用不同 URL，并用 hreflang/canonical/sitemap 说明关系。 |
| P0  | 前端从第一天接入 i18n。                               | 后期把硬编码中文改成多语言成本很高。                                                        |
| P0  | 全球 CDN 与 HTTPS。                              | 全球访问速度、TLS、DDoS 防护、缓存策略都依赖它。                                              |
| P0  | 最小合规包。                                       | 隐私政策、Cookie banner、数据删除/导出、AI 生成标注、DPA 模板。                                |
| P0  | 数据区域字段。                                      | 即使第一版只有一个区域，也要在 schema 中预留 region，否则后续迁移痛苦。                               |
| P0  | 英文 landing page 与 benchmark 页面。              | 全球获客首先靠可信英文内容，而不是中文转译。                                                    |
| P0  | 竞品对比审查。                                      | “超过 Ponder”必须有公开方法和数据，避免 FTC/广告风险。                                        |


### 4.3 国内优先会不同的地方


| 决策   | 国内优先可能做法     | 全球优先建议                                   |
| ---- | ------------ | ---------------------------------------- |
| 注册方式 | 手机号短信优先。     | 邮箱 + Google/GitHub OAuth 优先，手机号可选。       |
| 支付   | 微信/支付宝先行。    | Stripe 先行，微信/支付宝作为中国补充。                  |
| 内容   | 中文教程和社群裂变。   | 英文 benchmark、技术博客、open dataset demo。     |
| 合规   | 备案和 PIPL 优先。 | GDPR/AI Act/CCPA/WCAG/FTC 与 PIPL 并行。     |
| 基础设施 | 阿里云上海/腾讯云广州。 | US/EU 区域优先，国内可通过独立中国部署补充。                |
| 社区   | 微信群为主。       | Discord/GitHub Discussions 为主，微信群作为中文社区。 |
| SEO  | 百度收录、中文关键词。  | Google Search Console、英文关键词、hreflang。    |


## 5. 营销侧注意点

### 5.1 定位语建议


| 场景        | 建议表述                                                                                                             | 避免表述                                 |
| --------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| 首页主张      | Evidence-grounded research memory for papers, methods, and ideas.                                                | The best AI research workspace.      |
| 对比 Ponder | Ponder is great for interactive thinking; RF focuses on auditable paper evidence and structured research memory. | RF completely beats Ponder.          |
| 深度分析      | Seven-section structured reports with traceable evidence anchors.                                                | Deepest paper analysis in the world. |
| 知识体量      | Built to scale from one paper to thousands with indexed evidence.                                                | The largest research knowledge base. |
| AI 信任     | Every answer cites source evidence and shows uncertainty.                                                        | Hallucination-free AI.               |


### 5.2 内容营销路线


| 阶段       | 内容                                                                                                          | 目的         |
| -------- | ----------------------------------------------------------------------------------------------------------- | ---------- |
| Alpha 前  | 3 篇英文技术博客：structured paper analysis、evidence anchors、method evolution graph。                                | 建立技术可信度。   |
| Alpha 首发 | 5 篇公开论文 demo，展示 RF 报告、证据锚点、Ponder/Elicit/Scite 类工具对比方法。                                                     | 证据化“深度”优势。 |
| Beta     | Use-case landing pages：literature review、baseline comparison、PhD reading workflow、AI research agent memory。 | SEO 获客。    |
| 付费后      | 用户案例、实验室工作流、API/MCP 集成教程。                                                                                   | 提升转化和留存。   |


### 5.3 社区与渠道


| 渠道                         | 做法                                                          |
| -------------------------- | ----------------------------------------------------------- |
| GitHub                     | 保持开源本地版，README 清晰说明本地版与 SaaS 的关系。                           |
| X/Twitter                  | 发布技术 thread、benchmark、论文分析案例。                               |
| LinkedIn                   | 面向科研团队、R&D、AI for Science、企业研究部门。                           |
| Reddit                     | 谨慎进入 r/MachineLearning、r/PhD、r/AskAcademia，只发真实 demo，避免广告腔。 |
| Hacker News                | 适合 Show HN，但必须有在线 demo 和技术透明度。                              |
| Discord/GitHub Discussions | 做英文社区入口，微信群作为中文补充。                                          |
| YouTube                    | 做 3 分钟 demo：上传 PDF、生成证据报告、问收藏、导出。                           |


## 6. 法务与合规风险


| 风险                        | 依据/说明                                                                                     | 产品动作                                                           |
| ------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| GDPR 域外适用                 | GDPR Article 3 覆盖向 EU 数据主体提供 goods/services 或监测行为。                                        | EU 用户隐私权利、删除/导出、DPA、数据区域、SCC。                                  |
| Data protection by design | GDPR Article 25 要求设计和默认保护。                                                                | 最小化收集、默认私有、权限隔离、加密、短期日志。                                       |
| Processor 与第三方模型          | GDPR Article 28 涉及 processor 合同，Article 44 涉及国际传输。                                        | 与 LLM/API vendors 签 DPA，说明 subprocessors，EU 数据尽量走 EU/US 合规供应商。 |
| AI Act 透明度                | EU AI Act 2024-08-01 生效，多数规则 2026-08-02 适用，GPAI obligations 2025-08-02 生效。                | 标注 AI 生成、记录模型版本、用户反馈和纠错机制。                                     |
| CCPA/CPRA                 | 加州用户有知情、删除、选择退出出售/共享等权利。                                                                  | 隐私入口、Do Not Sell/Share 判断、数据请求流程。                              |
| WCAG 2.2                  | W3C WCAG 2.2 是当前 Web 可访问性标准之一。                                                            | 键盘可操作、对比度、语义标签、屏幕阅读器、错误提示。                                     |
| LLM 安全                    | OWASP LLM Top 10 包括 prompt injection、sensitive information disclosure、excessive agency 等。 | 工具权限、上下文隔离、输出检查、tenant boundary。                               |
| 广告宣称                      | FTC 要求广告真实、不误导，AI claims 需要 substantiation；背书需披露 material connection。                     | 所有竞品对比加方法和数据；KOL/用户推荐披露利益关系。                                   |
| ICP                       | 中国大陆经营/非经营互联网信息服务涉及许可或备案要求。                                                               | 国内服务器和中国大陆域名路线需先备案/许可；海外国际版可独立推进。                              |


## 7. 最危险的 10 个盲点


| 盲点              | 危害                            | 修正                                                   |
| --------------- | ----------------------------- | ---------------------------------------------------- |
| 未实测就宣称远超 Ponder | 广告风险、投资人不信、用户反感。              | 先 benchmark，再营销。                                     |
| 全球合规滞后          | GDPR/AI Act/CCPA/ICP 风险，后期返工。 | 合规与架构并行，最小合规包 P0。                                    |
| 多模态/画布/协作稀释核心   | 团队过载，产品同质化。                   | MVP 专注 PDF 深度证据引擎。                                   |
| 开源版与 SaaS 关系不清  | 社区反噬或商业化受限。                   | 明确 license、功能边界、迁移路径。                                |
| 路线图过重           | 交付延期，错过窗口。                    | 分阶段验证 PMF。                                           |
| 外部 API 依赖脆弱     | API ToS、限速、成本和可用性风险。          | 缓存、fallback、vendor review。                           |
| 单位经济不清          | 学生预算低，低频使用难订阅。                | 免费额度 + 用量计费 + 团队 seats。                              |
| 多租户与 LLM 注入安全不足 | 数据泄露、工具滥用、合规事故。               | tenant isolation、RLS、tool scope、prompt injection 防御。 |
| SEO 从中文开始       | 英文域权重积累慢，URL 返工。              | `.com` 英文优先，中文子路径。                                   |
| 全球支持缺位          | 留存差、退款多、社区差评。                 | Help center、工单、Discord、24h 首次响应。                     |


## 8. 更保守但可执行的阶段化方案

### Phase 1：Evidence Engine Alpha，0-3 个月

目标：不要全面追 Ponder，先上线全球可访问的 PDF 深度分析 SaaS，验证 RF 核心优势。

必须做：

- PDF 上传、解析队列、七段结构化报告、证据锚点、PDF 跳转。
- Email + Google/GitHub OAuth。
- 个人 library 和项目页。
- BibTeX/RIS/Markdown 导出。
- 英文 landing page、3 篇技术博客、5 篇 demo paper benchmark。
- 最小合规包：隐私政策、Cookie banner、数据删除/导出、AI 生成标注、审计日志。
- `.com` 主域、i18n 基础、hreflang/sitemap 基础。

明确不做：

- 音视频/图片/Word 多模态。
- 无限画布。
- 实时团队协作。
- 复杂计费。
- 多区域数据库。

成功标准：

- 50 个真实研究用户试用。
- 至少 10 个用户愿意为更多额度付费。
- 5 篇公开 benchmark 能支撑“RF 更 evidence-grounded”的表述。

### Phase 2：Paid Beta，4-6 个月

目标：验证付费和留存。

新增：

- Stripe 订阅或用量计费。
- NLQ 查询整个个人 library。
- Word/DOCX 报告导出。
- Help center、Discord/GitHub Discussions。
- 基础团队共享：只做共享 library 和评论，不做实时协作。
- WCAG 2.2 AA 基础审计。
- 每周 1 篇英文 SEO 内容。

成功标准：

- 50 个付费用户或等价团队付费。
- 月流失率低于 8%。
- NLQ 使用率超过 30%。
- 单篇分析成本和毛利可解释。

### Phase 3：Research Workspace，7-12 个月

目标：在验证核心 PMF 后，再覆盖 Ponder 的体验优势。

新增：

- Graph viewer / lightweight canvas：先展示 RF 知识图谱，不做自由白板。
- 多格式输入：Word、图片 OCR、音频/视频转写按需求排序。
- 团队 workspace：RBAC、活动日志、共享注释。
- PPTX、mindmap、PDF 高质量导出。
- 高峰优先队列、模型分级、usage credits。
- 评估 US/EU 区域部署。

此阶段才适合更强对比话术：

> RF combines interactive research workspace features with deeper, traceable paper evidence analysis.

## 9. 最终建议

1. 不要把第一版目标定成“Ponder 全覆盖”。第一版目标应是“Ponder 做不到的 evidence-grounded paper analysis，我做到极致”。
2. “知识体量和深度远超”必须转化成指标：论文数量、锚点密度、字段完整率、错误率、查询延迟、成本。
3. 全球化要从第一天设计，不要先做国内中文版再翻译。域名、i18n、SEO、支付、合规、支持系统都会返工。
4. 开源本地版与商业 SaaS 的关系要提前说清楚：本地版保留研究工作流，SaaS 提供云端存储、协作、模型、导出、团队管理和全球可访问性。
5. 产品差异化不要丢：Ponder 是思考空间，ResearchFlow 应该成为有思考空间体验的证据引擎，而不是有证据功能的白板。

## 10. DeepSeek 讨论摘要


| 轮次    | 主题       | 关键反馈                                              | 本文采纳                              |
| ----- | -------- | ------------------------------------------------- | --------------------------------- |
| 第 1 轮 | 产品战略     | RF 深度分析强，但多模态、协作、画布、计费、合规是明显缺口。                   | 形成 cover Ponder 模块表和 P0/P1/P2 分层。 |
| 第 2 轮 | 全球化营销与部署 | 全球可访问不是国内版加翻译，而是域名/CDN/区域/支付/合规/SEO/i18n/支持全链路重构。 | 形成国内优先 vs 全球优先对照表。                |
| 第 3 轮 | 反方审查     | “超过 Ponder”需实测；路线图过重；多模态和协作可能稀释核心；开源/SaaS 关系必须定义。 | 采用更保守的三阶段方案。                      |


## 11. 证据索引

### 本地 ResearchFlow 证据

- `README.md:29-45`：ResearchFlow 聚焦 structured, searchable paper evidence；local-first；不是 closed platform，而是 methodology/local knowledge workflow。
- `README.md:67-85`：pipeline、MinerU parse、structured analysis、chunk anchors、verified JSON、deterministic checks。
- `README.md:125-149`：三层 vault 架构、plain files、多 agent 可读。
- `_private/researchflow-backend-docs/ARCHITECTURE.md:5-20`：PostgreSQL truth source、DeltaCard、UI/Agent 投影、PostgreSQL/pgvector/Redis/object storage。
- `_private/researchflow-backend-docs/ARCHITECTURE.md:25-60`：四层知识图谱与约 40 表支撑层。
- `_private/researchflow-backend-docs/ARCHITECTURE.md:114-153`：2-Agent pipeline、analysis_agent、deterministic scoring、writer_agent。
- `_private/researchflow-backend-docs/ARCHITECTURE.md:170-175`：三道防线。
- `_private/researchflow-backend-docs/DEPLOY.md:7-15`：单主机部署配置。
- `_private/researchflow-backend-docs/DEPLOY.md:50-60`：7 容器架构，包含 frontend、api、worker、mcp、caddy。
- `_private/researchflow-backend-docs/DEPLOY.md:230-247`：外部 API 清单。
- `_private/researchflow-backend-docs/METADATA_ACQUISITION.md:9-17`：fallback、二次审核、观测记账、限速、标题匹配门控。

### 外部可靠依据

- GDPR：Article 3 域外适用；Article 25 data protection by design/default；Article 28 processor；Article 44 国际传输。
- EU AI Act：2024-08-01 生效，大部分规则 2026-08-02 适用，GPAI obligations 2025-08-02 起适用。
- Google Search Central：多语言/多区域站点应使用不同 URL、hreflang、sitemap/canonical，不应只依赖 IP 自动重定向。
- W3C WCAG 2.2：Web 内容可访问性标准，覆盖 perceivable、operable、understandable、robust。
- OWASP Web Top 10 与 OWASP LLM Top 10：Web 和 LLM 应用的常见安全风险，包括 prompt injection、sensitive information disclosure、excessive agency 等。
- Stripe：支持多货币和多支付方式，但具体可用性受账户国家、客户国家、支付方式和币种影响。
- FTC：广告主张应真实、不误导并有 substantiation；背书/推荐中的 material connection 需要披露。
- 中国 ICP：经营性互联网信息服务需许可，非经营性互联网信息服务需备案；未取得许可或未履行备案不得提供相应服务。

