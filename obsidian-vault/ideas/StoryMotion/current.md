---
title: "StoryMotion: Preserving Human Motion Priors in Asymmetric Human–Camera Generation"
status: v11_c0_lat_geo_co_mainline
hypothesis: |
  Paper A StoryMotion owns the v11 C0-LAT/C0-GEO co-mainline and tests a
  capability-preserving asymmetric Human–Camera extension. The remaining core
  scientific tasks are the versioned correction and audit of Pulp Camera text,
  plus an Independent Conditional Cascade and a secondary fully-separate system comparison.
tags:
  - StoryMotion
  - version/v11
  - stage1
  - stage2
  - protected-human
  - status/active
aliases:
  - StoryMotion-Current
source_notes:
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[Storymotion-exp-sha]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[StoryMotion-iclr-reliability]]"
  - "[[paper-boundary]]"
created: 2026-07-12T14:30:00+08:00
updated: 2026-08-03T18:05:00+08:00
---

# StoryMotion: Preserving Human Motion Priors in Asymmetric Human–Camera Generation

> [!important] 当前裁决
> 自 2026-07-31 起，v11 C0-LAT 与 C0-GEO 的 EMA Camera `105K` endpoint
> 共同成为 StoryMotion mainline。两者同享 exact v9 Pulp-only Stage1、owning
> decoder/cache/train-only statistics 与冻结 Human `105K` teacher，只在 Camera
> objective 上分叉。C0-GEO 相对 C0-LAT 的 Direct-C 与 sequential 六项 Camera
> geometry 95% CI 全部跨零，语义、覆盖与构图字段又形成混合 Pareto，因此不把
> 任一臂降为 subordinate alternate。C3-25 转为 former-mainline system baseline。

> [!important] seed23 matched repeat已闭合
> 两条C0 objective均以训练seed23从零启动并完成Camera `105K`、pure4,053三模式、
> decoded geometry／physical与10,000次paired bootstrap。Direct-H frozen-owner replay
> 通过；两个seed内的GEO−LAT及两个objective的seed23−seed17共24项Camera geometry
> 95% CI全部跨零。独立训练seed缺口已经关闭，但sealed audit与视觉失败分层仍未完成；
> C0-LAT／C0-GEO共同mainline不变。正式证据见
> [[StoryMotion-valid-metric-ledger#3.14 v11 C0 seed23 105K pure4,053 matched repeat]]。

> [!important] Paper A scope
> 本页只服务 **StoryMotion: Preserving Human Motion Priors in Asymmetric Human–Camera
> Generation**。DIRECT文档已迁移到`obsidian-vault/ideas/DIRECT/`，其状态只见
> [[DIRECT/current|DIRECT current]]。两篇论文仍共享StoryMotion代码仓库；当前不创建
> DIRECT代码仓库。完整贡献边界见[[paper-boundary]]。

> [!failure] Explicit framing `30K` 不进入 mainline
> 冻结 C0-GEO 上的 CF-4 framing adapter 虽在 N64／pure4,053 都形成可测 control
> adherence，absent-control 路径也保持 exact，但 matched pure4,053 Direct-C 与
> sequential 在 semantic、coverage、caption 与 projective framing 多字段回退。
> 因而该轴以 diagnostic-only 关闭；C0-LAT／C0-GEO co-mainline 不变。裁决见
> [[archived/experiments/2026-07-31_storymotion-v11-explicit-framing-control]]，正式数值见
> [[StoryMotion-valid-metric-ledger#3.12 v11 explicit framing-control 30K pure4,053 formal]]。

> [!warning] Camera触发hard stop；Human只有endpoint headroom，editing退出投稿queue
> Camera64在mask外exact时仍造成far world Camera-center漂移，endpoint oracle也失败，
> 因而当前Camera representation停止。Human128的naive clamp同样产生root／global-joint
> 漂移，但N8 mask-local endpoint oracle四格全过，证明当前Human128存在端点闭合headroom。
> 这只保留为endpoint-existence evidence；为收缩投稿scope，不再安排Human短screen，两轴
> 均不启动MAE长训，也不形成paper editing claim。分别见
> [[archived/experiments/2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]与
> [[archived/experiments/2026-07-31_storymotion-v11-human-temporal-locality-control]]。

> [!important] v10关闭；Raw-H只作为v9 sibling control
> 不再补v10 corrected endpoint、176D cache或Stage2。Stage1 observation现为低优先级，
> 只允许在保留exact v9 Human owner、Camera64 layout与non-causal边界下另建sibling；当前
> Paper A不启动Raw-H Stage1长训，也不借该历史轴改变matched specialist合同。

## 0. Paper A路由

- 当前论文：StoryMotion Paper A。
- 当前方法owner：v11 C0-LAT／C0-GEO共同mainline。
- 当前实验owner：[[StoryMotion-iclr-reliability]]。
- 正式数字owner：[[StoryMotion-valid-metric-ledger]]。
- DIRECT状态与队列：[[DIRECT/current|DIRECT current]]；不在本页复述。
- 代码仍只有`linkedCodebases/StoryMotion/`；文档按Paper A／DIRECT分目录。

本页只拥有当前选择、允许的 claim、活跃 blocker 与 evidence link。正式数字与哈希
只见 [[StoryMotion-valid-metric-ledger]]；版本事件只见 [[version_family]]；Paper A中稿
差距与优先级只见[[StoryMotion-iclr-reliability]]。

## 1. 共同 mainline 合同

| component / run | fixed boundary | current role |
| --- | --- | --- |
| shared Stage1 / `stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726` | non-causal；Human199 + Camera14；`human128+interaction16+camera48`；owning `D_h/D_c/D_f` | C0 两臂唯一合法 representation owner |
| shared Human / `v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727` | Human text → Human128；EMA `105K`；Camera 训练全程冻结 | Direct-H owner；sequential 的第一阶段 |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | GT-H Camera training；latent flow；Camera EMA `105K` | co-mainline |
| v11 C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 同 C0-LAT，另加 calibrated Stage1-style decoded Camera auxiliary | co-mainline |
| v8.1C C3-25 / canonical `105K` | former joint-AE + Unified-3；formal joint parallel | primary former-mainline baseline |

两个 v11 endpoint 都必须报告三种模式：

1. Direct-H：Human text → Human；
2. Direct-C：GT／observed Human + Camera text → Camera；
3. formal sequential：先 Human text → Human，再以最终 Human + Camera text → Camera。

`joint_parallel=false` 是 v11 固定边界。未经单独授权，不补训、不评估，也不以
joint parallel gate v11。历史合同中的 `diagnostic_only=true` 与
`promotion_eligible=false` 保留为当时执行授权的 provenance；本次 selection event
不回写 immutable artifacts。

## 2. 选择依据与结论边界

- 四臂均已闭合 Camera optimizer `105K`、pure4,053 三模式 formal audit、decoded
  geometry、no-reference physical diagnostics、10,000 次 matched bootstrap 和
  fixed-8 visual。C1 两臂不进入 mainline。
- C0-LAT 与 C0-GEO 的 Human 输出逐字段相同；Camera objective 差异没有形成稳健
  geometry 胜者，且 semantic／coverage／framing 各有取舍。共同 mainline 是对现有
  证据的直接表达，不是回避选择。
- 对 C3-25 的比较是 system replacement boundary：Stage1、decoder、sampler 和
  formal joint solver 都不同。可以报告三模式系统级 Pareto，不写成单变量支配。
- v9 final 只有 first-512 的 Direct-H／Direct-C／joint-parallel；PulpMotion 是 native
  joint baseline。sample count、条件合同与 decoder 不同的字段必须显式留空或限制结论。
- v11 自由 Human 的语义／构图改善与偏低 dynamics 幅度并存。contact／skate 仍是
  heuristic，不能写成 calibrated physical validity。

## 3. 当前论文主张

StoryMotion 的目标是中稿 ICLR 2027。当前中心主张收口为：

> 以non-causal asymmetric unified framework支持Human generation、observed-Human
> Camera generation与sequential Human-then-Camera generation；在Camera扩展中保持
> Human owner及其输出路径不变，并由同一Camera模型执行observed-H与generated-H。

Sequential是factorized joint distribution的两个推理pass，不声称同步或双向joint
denoising。Direct-H是被保留的基础能力，不写成Camera扩展带来的新提升。C0-LAT与
C0-GEO是同一方法的两个报告endpoint，数值、视觉与局限必须同时呈现，不跨endpoint
摘取单列最优。DIRECT的可迁移摄影program属于第二篇，不再覆盖本主张。

Paper A另纳入一项次要数据贡献：固定Pulp Camera convention，根据实际Camera参数变化
新增无歧义caption，同时保留原caption、来源与修订版本。该修正尚未完成，不得提前写成
已发布数据集或已证实增益；它只修复factual监督，不产生Rect或跨Human positive。首个
`N=512`、seed17、无LLM的TriMotion-compatible geometry screen已经完成自动检查，但其阈值与
raw conflict都仍是screen级结果，不能据此启动全量语言化或宣称缺陷比例。

## 4. 活跃 blocker

1. **Camera文本有效性。** `paperA_pulp_trimotion_geometry_screen_n512_seed17_20260803`
   已在不调用LLM的前提下完成首帧相对RDF轨迹、symbolic phases、Pulp临时阈值、全局刚体
   gauge与时间反转检查。下一步先人工复核随机／高风险子集并校正阈值与raw-text parser，之后
   才能冻结全量规则、生成short／long文本并做matched Stage2数据消融。约16万样本不能依赖
   逐条人工修订。
2. **独立specialist cascade。** `0803-1647`要求的主对照必须有独立且Human-conditioned的
   Camera Stage1，即$E_C(H,C)$与$D_C(H,z_C)$。v7.33只有$E_C(C)$／$D_C(z_C)$，且旧任务
   fresh重训Human Stage2，因此不是该主对照。旧任务已按合同不匹配停止并保留；当前GPU1
   运行Independent Conditional Camera64 Stage1，固定exact v9 Human owner，之后只训练
   Camera Stage2；该Stage2还必须等待Camera caption选择冻结。GPU0并行运行用户另行确认必要的
   v7.33 fully-separate native variant；它
   复用已审计Stage1并fresh训练Human／Camera两个Stage2。两者都只用factual GT-H／GT-C
   positive。当前fully-separate训练使用raw Camera text，是`T_0`系统对照；如果最终caption
   选择不是raw，仍需matched重训，不能把当前checkpoint当作canonical-text结果。正式解释严格分开。完整预声明见
   [[StoryMotion-iclr-reliability#2. 独立specialist cascade系统对照]]。
3. **投稿证据闭环。** 冻结PulpMotion同split、同sample count、同指标的主表；Pulp Motion
   与TSA是结构化motion主baseline，Auteur、Uni3C与ActCam按不同任务层级比较。
   seed23独立长训与matched repeat audit已闭合，两个seed都不支持单一
   Camera objective胜出；仍需sealed audit、随机／最好／最差可视化和failure taxonomy。
   基础盲评只用于可信度。最终还需冻结论文代码、配置、三接口evaluator、checkpoint／decoder身份、
   参数量、GPU小时、推理成本与最小复现实验包。
4. **可选接口消融，不阻塞主张。** current sequential直接把Human generator的H128交给
   Camera。H199 cascade只是在两者之间插入`D_H`与`E_H`，检验显式Human API的round-trip
   误差；它不改变Human owner、Camera branch或概率分解。只有正文准备声称“latent直连优于
   普通串行接口”时才做该evaluator-only对照，不重训Stage1／Stage2。
5. **措辞边界。** sequential不写成同步joint；显式3D motion generation不写成ViGen
   controllability；生产可用性、Rect与program transfer全部留给DIRECT。

RV、Rect、HumanML3D、Director ownership与ViGen utility均由
[[DIRECT/current|DIRECT current]]路由，不再阻塞Paper A收口。

## 5. 当前行动边界

- 冻结 C0-LAT 与 C0-GEO 两个 mainline endpoint，不因单个 raw mean 继续选臂。
- Paper A后续specialist实验若没有另行说明，默认seed17；run ID与contract仍必须显式记录
  `seed17`。改变seed必须预先写明理由，历史seed23 provenance不改名。
- Paper A当前并行关闭两个核心工作包：Pulp Camera坐标／文本修正，以及Independent
  Conditional Cascade主对照；fully-separate native variant作为第二系统边界，不替代主对照。
- Camera text在`N=512` geometry screen之后仍保持“无LLM、未授权全量”；先复核临时阈值、
  原文冲突判定与高风险样本，再决定全量处理合同。
- H199 decode→re-encode只保留为可选接口消融，不在当前critical path；不为它启动任何训练。
- multi-seed matched repeat已经闭合，不再等待Rect或ViGen utility。
- v10 Camera Stage2、C1、swapped-host replay和当前Camera64 MAE长训均保持关闭。
- Formal editing与learned bounded staging留作投稿后future work，不进入当前queue。

## 6. Canonical owners

- 当前选择、blocker 与行动边界：本页。
- 正式数值、公平对比与 artifact hashes：[[StoryMotion-valid-metric-ledger]]。
- 其余 run identity 与 visual index：[[Storymotion-exp-sha]]。
- evaluator／decoder／指标语义：[[StoryMotion-metric-computation-io]]。
- 版本完成事件与 invalidation：[[version_family]]。
- 两篇论文正式题名、单仓库规则、scope与venue边界：
  [[paper-boundary]]。
- Paper A的claim–evidence gap、降级条件与reliability计划：
  [[StoryMotion-iclr-reliability]]；其中拆分前内容不是当前实验授权。
- DIRECT当前状态与全部Paper B owner：[[DIRECT/current|DIRECT current]]。
- Camera temporal editing representation stop：
  [[archived/experiments/2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]。
- Human temporal locality与endpoint headroom：
  [[archived/experiments/2026-07-31_storymotion-v11-human-temporal-locality-control]]。
- v11 原始四臂合同与停止规则：
  [[archived/versions/v11/2026-07-29_storymotion-v11-v9-owner-stage2-three-mode-rescue-contract]]。
