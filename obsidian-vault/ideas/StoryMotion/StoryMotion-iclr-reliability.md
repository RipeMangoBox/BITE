---
title: "StoryMotion Paper A ICLR Reliability and Closure Contract"
status: in_progress
hypothesis: |
  Paper A检验在冻结Human prior及其输出路径时，非对称Human–Camera扩展能否支持
  Direct-H、Direct-C与sequential composition。当前剩余两项核心科学任务是修正并审计
  Pulp Camera text，以及完成独立Human／Camera specialist cascade系统对照。
tags:
  - StoryMotion
  - paper/A
  - reliability
  - submission-closure
  - status/active
aliases:
  - StoryMotion-ICLR-Reliability
source_notes:
  - "[[StoryMotion/current]]"
  - "[[StoryMotion/version_family]]"
  - "[[StoryMotion/StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion/StoryMotion-metric-computation-io]]"
  - "[[StoryMotion/paper-boundary]]"
created: 2026-06-18T00:00:00+08:00
updated: 2026-08-03T17:20:00+08:00
---

# StoryMotion Paper A ICLR Reliability and Closure Contract

> [!important] 唯一live范围
> 本页只拥有Paper A的claim–evidence gap、投稿实验优先级、停止条件和降级措辞。
> 正式数字与hash只见[[StoryMotion/StoryMotion-valid-metric-ledger]]；DIRECT状态只见
> [[DIRECT/current]]。拆分前完整方案已归档，不再授权Rect、HumanML3D跨配对、program
> solver、Actor–Director数据、ViGen utility、editing或joint-parallel训练。

## 1. 已冻结的方法与已有证据

$$
p(H,C\mid T_H,T_C)=p_H(H\mid T_H)p_C(C\mid H,T_C).
$$

Paper A只报告：

1. Direct-H：$T_H\rightarrow H$；
2. Direct-C：observed $H+T_C\rightarrow C$；
3. sequential composition：先生成并固定$H$，再由同一个Camera branch生成$C$。

当前训练主线已经闭合。v11 C0-LAT与C0-GEO共享exact v9 Pulp-only non-causal Stage1、
owning decoder／cache／train-only stats及冻结v9 Human `105K` teacher，仅Camera objective不同。
seed17与seed23四个Camera endpoint均完成`105K`、Pulp pure4,053三接口、official metrics、
decoded geometry／physical diagnostics和10,000次paired bootstrap。24个Camera geometry差异的
95% CI全部跨零，因此只能写“没有稳健单一objective胜者”；不能写LAT／GEO等价，也不能选择GEO。

## 2. 独立specialist cascade系统对照

> [!important] 2026-08-03 Stage1复用裁决
> 4090上的v7.33 Camera14 separate AE已完成可复用边界：`162,760`个ordered Pulp train
> IDs、`4,053`个ordered pure-test IDs、seed17、batch128、`636,000` updates、non-causal、
> Human199＋Camera14、H128＋C64，以及owning checkpoint／decoder和official pure4,053
> reconstruction eval。逐项审计确认其train／test IDs及顺序与v9 mainline相同。因此按预声明
> “存在则只重训Stage2，否则Stage1＋Stage2均重训”，本对照**不重训Stage1**。

该对照不是H199 round-trip测试。它比较完整系统的共享／关系型Stage1与H／C-separate Stage1，
并为Human与Camera分别训练Stage2权重、优化器和checkpoint。由于Stage1 architecture本身改变，
它是full-stack specialist system comparison，不是只隔离Stage2 sharing的matched ablation。

| arm | Stage1所有权 | Stage2所有权 | Human接口 | Camera训练positive | 允许回答的问题 |
| --- | --- | --- | --- | --- | --- |
| A · StoryMotion C0-LAT | exact v9 H-anchor Pulp-only；H128＋I16＋C48 | protected Human teacher＋Camera endpoint | H128 latent直连 | paired GT-H latent＋原Camera | current reference |
| B · Specialist-Native-LAT | v7.33 separate AE；独立$E_H/D_H$与$E_C/D_C$；H128＋C64 | fresh Human specialist＋fresh Camera specialist；独立optimizer／checkpoint | observed或先生成并固定的H128 | paired GT-H latent＋原Camera；不构造generated-H＋原Camera positive | 完整独立specialist cascade在同数据、同Stage2预算下是否优于StoryMotion |

### 2.1 冻结身份与预算

- Stage1 parent：`v7_33_separate_official14_ae_500ep_seed17_4090_20260713`；last checkpoint
  SHA-256为`b8f8ca74748650481cd0901a1476b1580636aaf5fdcd7d4629b223655811aeb4`。
- Stage1 contract：`is_causal=false`，Human199＋Camera14，H128＋C64，hidden256，downsample4；
  Human encoder／decoder与Camera encoder／decoder无共享参数。总参数`957,333`；四个模块依次为
  `251,520 / 379,335 / 60,224 / 266,254`。
- Stage1 exposure：seed17、batch128、`636,000` optimizer steps；train／test IDs分别为
  `162,760 / 4,053`，与v9 mainline逐项同序。历史pure4,053 artifact SHA-256为
  `ca31514032105a84497083983f8d4fc175526cb0900aeea0d4e503a83d9c018d`。
- Stage2 Human：与C0 Human模块相同的ViMoGen LightFlow，`71,870,080`参数，fresh seed17，
  Human-text-only，batch128，`105K` optimizer steps，LAT flow，EMA `0.9999`。
- Stage2 Camera：与C0-LAT Camera模块相同的CameraConditionedFlow，`84,492,096`参数，fresh
  seed17，GT-H-only，batch128，`105K` optimizer steps，LAT flow，EMA `0.9999`。
- 总Stage2 exposure与C0 matched：Human `105K×128`＋Camera `105K×128`；不追加GEO臂，避免把
  specialist轴与Camera objective轴相乘。正式比较只对C0-LAT，不据此评价C0-GEO。
- checkpoint数按逻辑owner计为两个Stage2 endpoint：Human teacher与Camera specialist；Stage1
  owning checkpoint单独报告。GPU小时、峰值显存及Direct-H／Direct-C／sequential p50／p95
  latency按实际测量报告，不用空闲GPU时间替代计算成本。

### 2.2 训练与评测gate

1. 先以owning v7.33 AE按exact valid length重建train／pure-test cache；禁止让non-causal encoder
   读取future padding。cache必须记录checkpoint、manifest、ordered IDs、latent order和train-only
   normalization hashes。
2. optimizer前必须通过：Stage1 strict load、H／C branch无共享参数、cache train/test identity、
   H128＋C64 shape、`is_causal=false`、decoder round trip、8-sample finite bridge和初始参数hash。
3. Camera只在真实Pulp pair上训练$p_C(C\mid H,T_C)$；Human condition来自同pair的GT Human经
   v7.33 $E_H$编码。generated-H route没有合法re-execution target，只做sequential推理测试。
4. first-512只作screen，不提前选checkpoint；正式endpoint固定EMA `105K`，在同一pure4,053上
   报Direct-H、Direct-C、sequential、official metrics、decoded geometry／physical、10,000次
   paired bootstrap和盲样本。
5. 若B优于A，只能支持“完整specialist system是强对照”，不能否定能力保持式非对称分解；若B
   不优于A，只能写“在该预声明数据／预算下没有胜过StoryMotion”，不能把差异单独归因为Stage2
   sharing。任何参数或速度优势必须用完整系统参数、GPU小时和推理测量支持。

### 2.3 可选H199接口消融

`H128 → D_H → H199 → E_H → H128`仍只检验显式Human API round-trip；它不属于本次
Specialist-Native训练，也不阻塞Paper A。正文不声称latent接口优越时不执行。

## 3. 投稿闭环矩阵

| 优先级 | 闭环单元 | 当前artifact事实 | 最小剩余动作 | 是否训练 | 关闭后的claim |
| --- | --- | --- | --- | --- | --- |
| P0 scientific core | Pulp Camera文本 | 已定位坐标选择会翻转方位；新caption尚未形成正式版本 | 冻结extrinsic convention、生成`T_C^geo`、保留raw provenance、自动一致性检查、分层人工抽检与directional subset审计 | 否，先审计 | 通过后写版本化factual caption修正 |
| P0 system control | Independent specialists | v7.33 separate AE的162,760／4,053、non-causal、H199＋C14 parent及hash已闭合；尚无当前ViMoGen specialist Stage2 | exact-length cache后fresh训练Human／Camera各105K；单一LAT objective；三接口pure4,053 formal | 是，仅Stage2 | 完整specialist cascade system comparison；不作Stage2单变量归因 |
| P1 submission | Human保持 | seed17／23 Direct-H共享冻结owner；seed23 replay已过 | 把checkpoint／输出逐元素保持检查固化为公开测试 | 否 | Camera扩展不改变Human owner及输出路径 |
| P1 submission | relation-interface机制 | 结构合同存在；活动ledger没有正式zero／shuffle／route机制表 | 仅在正文需要机制归因时做冻结checkpoint敏感性检查 | 否 | 最多支持接口被使用，不宣称每个Stage1部件必要 |
| P1 submission | 同协议主表 | C0、C3与PulpMotion pure4,053已有正式行；v9仅first-512；TSA／Auteur无活动formal row | 冻结baseline eligibility、split、N、decoder和指标；补可执行且任务匹配的缺行，不可比字段留空 | 原则上评测；未定义实现不长训 | 只作同协议或显式system-boundary比较 |
| P1 submission | Sealed final audit | pure4,053已多次用于开发；seed23复现已闭合 | 冻结方法／指标／prompt taxonomy后，以新sampling seed一次性跑三接口及预注册表 | 否 | 降低selection leakage；不再据sealed结果改模型 |
| P1 submission | 感知与失败披露 | fixed样例存在；随机／最好／最差分层和盲评未闭合 | 冻结cohort与排序规则，完成基础盲评、failure taxonomy、random／best／worst补充材料 | 否 | 视觉可信度与局限；不承担production claim |
| P1 submission | 复现与成本 | contracts、hash和正式artifact齐，但论文包未冻结 | clean revision、环境、命令、三接口evaluator、参数量、GPU小时、p50／p95延迟、显存、table generator和最小demo | 否 | 可复现性与计算成本 |
| P2 optional | H199 interface | C0已是Stage2 specialist decomposition；没有H199 round-trip正式结果 | 只有选择latent-interface优势claim时才做identity guard、pure4,053与paired bootstrap | 否 | 只决定可选接口优势，不决定Paper A主张 |

### 3.1 Caption训练的条件边界

Camera文本修正通过数据审计后，默认只构成数据质量贡献，不自动授权Camera `105K`重训。
只有正文准备主张“geometry-derived caption改善生成”，才需要另冻raw-text／geo-text matched
训练合同、单一objective、预算和决策阈值；没有这项训练时，正文不得写生成增益。

### 3.2 Baseline边界

- C3-25与PulpMotion native的Pulp pure4,053行已经存在，不应重复训练。
- v9只有first-512，不能伪装成pure4,053 matched row。
- TSA／Auteur只有在输入、输出、数据和指标能对齐且存在可执行artifact时才进入formal表；
  否则只进入related-work任务边界，不为凑表启动未定义长训。
- Uni3C、ActCam与ViGen utility不属于Paper A实验门槛。

## 4. Claim冻结表

### 4.1 初稿现在可以写死

- 方法是能力保持式非对称扩展，不是对称joint generator。
- Direct-H复用冻结Human prior；Direct-C与sequential复用同一Camera branch。
- Composition是两个条件分布的顺序组合，`joint_parallel=false`。
- seed17／23不支持稳健的单一LAT／GEO胜者；两者作为共同mainline报告。
- Paper A只使用Pulp factual Human–Camera pairs；不构造generated-H与原GT Camera positive。

### 4.2 必须等实验再决定

- Pulp Camera caption修正能否列为数据贡献；由一致性审计和人工抽检决定。
- 完整independent specialist cascade是否形成质量、参数或推理成本优势；由预声明LAT单臂决定。
- 是否优于公开baseline、是否有主观优势；由同协议主表、sealed audit与盲评决定。

### 4.3 可选、不阻塞主张

- 若正文不声称latent接口优于显式Human API，则无需运行H199 cascade。
- 若正文需要relation／interaction机制归因，再补zero／shuffle／route检查；否则只把Stage1写成
  冻结representation owner，不写component necessity。

### 4.4 当前禁止写入摘要或contribution

- “latent直连优于普通cascade”——除非未来选择并完成H199接口消融。
- “共享／关系型Stage1优于完整独立specialist stack”——等待Specialist-Native-LAT正式结果。
- “LAT与GEO等价”或“GEO优于LAT”。
- “Stage1每个部件都必要”、全面SOTA、calibrated physical validity或production-ready。
- 同步joint generation、独立双文本控制、editing、Rect、program transfer或ViGen utility。

## 5. 本周初稿与实验冻结顺序

初稿可以立即开始。方法、问题定义、数据边界、现有seed17／23结果和限制可直接成文；数据贡献
和baseline superiority暂留占位符。当前顺序是：

1. 完成Camera convention与caption数据审计；
2. 复用已审计v7.33 separate AE，完成Specialist-Native-LAT的两套Stage2 `105K`与formal audit；
3. 冻结同协议baseline表，并按正文实际claim决定是否补最小机制检查；
4. 冻结所有选择后做sealed audit、盲评与失败分层；
5. 最后一次性冻结复现包、参数／GPU小时／推理成本和论文表格；
6. H199 evaluator-only审计仅在选择latent-interface优势claim时执行。

当前不进入critical path：H199 round-trip、caption重训、v10、C1、editing、
Camera MAE、Human locality short screen、joint-parallel和DIRECT实验。

## 6. 历史材料

重构前的完整reliability页与拆分前Actor–Director附录保留在
[[StoryMotion/archived/paper-scope/2026-08-03_storymotion-iclr-reliability-pre-closure-refactor]]。
它只作provenance，不是当前Paper A训练授权。
