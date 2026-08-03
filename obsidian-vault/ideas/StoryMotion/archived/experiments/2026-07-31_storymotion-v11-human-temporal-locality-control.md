---
title: "StoryMotion v11 Human Temporal Locality Control"
hypothesis: |
  在Human128内部连续区间变化、mask外latent逐元素固定时，exact non-causal
  owning decoder应把Human199变化限制在有限guard band内；若world Human仍在
  远端漂移，则Human editing必须显式约束root translation与heading endpoint，
  不能仅靠latent clamp。
status: endpoint_oracle_pass_short_screen_authorized
archived: 2026-08-03
tags:
  - StoryMotion
  - version/v11
  - control/human_inpainting
  - status/active
source_notes:
  - "[[current]]"
  - "[[StoryMotion-iclr-reliability]]"
  - "[[DIRECT/2026-08-01_storymotion-multipair-data-training-plan]]"
  - "[[2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]"
created: 2026-07-31T20:10:00+08:00
updated: 2026-08-03T14:30:39+08:00
---

# StoryMotion v11 Human Temporal Locality Control

> [!important] Causal question
> 只改变Human128的中心连续区间、保持mask外Human128与全部Camera64逐元素不变时，
> exact v9 non-causal owning decoder会不会改变远端Human199或world Human？该问题只
> 审计representation／decoder适配性，不证明语义编辑或生成质量。

本页拥有Human temporal locality这一独立轴的合同、screen数字与停止裁决。Camera
locality只见[[2026-07-31_storymotion-v11-camera-temporal-inpainting-control]]；正式
生成数字仍只进入[[StoryMotion-valid-metric-ledger]]。

## 1. 预声明边界

- 唯一owner是v11 C0-LAT／C0-GEO共享的exact v9 Pulp-only non-causal Stage1：
  `human128+interaction16+camera48`；本screen不比较LAT与GEO Camera objective。
- ordered cohort是eval顺序中首64个至少有10个有效latent token的样本，保证中心
  `25%`／`50%` gap加两侧2-token guard band后仍有far context；不是按结果筛选。
- 两个确定性operator是Human128线性补间与区间反转。它们只用于产生可测扰动，不
  冒充semantic edit；Camera64、stats、sample identity与owning decoder全部固定。
- 无optimizer、无Stage2 sampling、无joint parallel。所有constructor／checkpoint／
  decoder继续要求`is_causal=false`。
- `root_translation_aligned_joint_mpjpe_m`只逐帧去除root translation，**没有对齐
  heading**；不得称为local-pose error。

预声明authorization要求每个operator／gap同时满足：mask外Human128 max-abs为`0.0`；
far Human199、root-translation-aligned joints、world root与global joints相对mask内
变化的比值均不超过`0.10`。

## 2. N64 screen结果

> [!warning] 裁决：naive latent clamp失败；endpoint-aware短screen获授权
> 共`64 × 2 gaps × 2 operators = 256`条condition records。所有mask外Human128
> `max_abs=0.0`，且两token guard band之外的Human199 RMSE在256条记录中逐条为
> `0.0`。这说明non-causal owning decoder的**feature-space远端泄漏没有发生**。
> 但world root／global joints均未通过`0.10` endpoint gate，因此当前Human128不
> 适合只靠latent clamp做world-space-preserving edit。随后N8 endpoint oracle四格全过，
> 只证明存在可优化headroom，授权一个带endpoint loss的amortized短screen；仍不授权
> MAE长训或paper editing claim。

| version / run | operator / gap | far／masked Human199 | far／masked root-translation-aligned joints | far／masked root | far／masked global joints | decision |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| v11 shared Stage1 / `v11_shared_human128_locality_n64_seed17_5090g3_20260731` | linear / `25%` | `0.0000` | `0.4476` | `1.2719` | `1.1123` | fail |
| v11 shared Stage1 / `v11_shared_human128_locality_n64_seed17_5090g3_20260731` | reverse / `25%` | `0.0000` | `0.0094` | `0.5587` | `0.4778` | fail |
| v11 shared Stage1 / `v11_shared_human128_locality_n64_seed17_5090g3_20260731` | linear / `50%` | `0.0000` | `0.6574` | `1.1638` | `1.1147` | fail |
| v11 shared Stage1 / `v11_shared_human128_locality_n64_seed17_5090g3_20260731` | reverse / `50%` | `0.0000` | `0.0183` | `0.4398` | `0.3907` | fail |

绝对量级同样不能忽略：linear `25%／50%`的far root ADE分别为
`0.2786 m／0.4930 m`，far global MPJPE为`0.2936 m／0.5092 m`；reverse对应far
root ADE为`0.1123 m／0.1309 m`。linear operator在guard band外仍有
`0.0427 m／0.0683 m`的root-translation-aligned误差，说明除了translation累积，
heading也发生了远端改变；reverse的该误差仅`0.0008 m／0.0018 m`，但root
translation endpoint仍明显漂移。

`results.json`中的`decoder_feature_locality_pass=false`是预声明的**组合gate**，同时
包含Human199与未对齐heading的root-translation-aligned geometry；它不表示
Human199发生了far-context泄漏。逐record Human199 far error与known-latent error都
是exact zero。

## 3. 机制解释与架构要求

non-causal decoder只在edit边界附近改变Human199；真正的远端world drift来自
Human199 root translation／yaw增量的时序积分。mask外feature即使不变，编辑区改变的
累计root state仍会成为所有后续frame的初始条件。区间反转大体保留heading终点，因此
translation-aligned远端误差很小，但3D root displacement的积分次序仍改变，world
endpoint没有恢复。

因此，Human editing若重开，representation必须至少满足一个方案：

1. 把body／root trajectory拆开，body edit不默认改root；
2. 用absolute root position与heading，或segment anchor + local residual，替代只靠
   velocity／yaw increment累积；
3. 在edit interval两端显式约束root position、heading与必要的velocity连续性，并先做
   latent endpoint-closure oracle；
4. Human edit完成后把**最终Human**交给Director重新规划Camera，不要求旧Camera轨迹
   对新Human逐位不变。

### 3.1 预声明endpoint-closure oracle

在决定必须更换representation前，允许一次ordered first-8 latent optimizer oracle：

- 复用相同eligible cohort的前8个样本、`25%／50%` gap与linear／reverse proposal；
- 模型参数、Stage1、Camera64、mask外Human128全部冻结，只优化mask内delta；
- Adam `200`步、learning rate `0.05`、gradient norm clip `10`；loss只读取guard band
  之外的world root MSE与root-translation-aligned joint MSE，权重分别为`10／5`，另用
  `0.01` proposal-anchor防止退回原始latent；不读取mask内GT reconstruction；
- 每个operator／gap都必须保持mask外Human128 exact，far Human199、root、global joints
  与root-translation-aligned joints的far／masked比值均不超过`0.10`；同时优化后
  mask内latent edit幅度必须保留proposal的`[0.5, 1.5]`，排除直接复制原序列；
- 四个cell全过才说明当前Human128存在可amortize的endpoint headroom；它仍不直接授权
  MAE长训，只允许设计带root／heading endpoint loss的短screen。任一cell失败则维持
  `stopped_world_endpoint_gate`。

### 3.2 Endpoint oracle结果

> [!success] 四格通过existence gate
> mask-local delta在不读取mask内GT reconstruction的前提下，把四格far world error均
> 压到预声明`0.10`以下；mask外Human128继续exact，mask内latent edit幅度保留
> `1.02–1.12×`，排除了直接复制原latent。该结果只回答“当前Human128是否存在
> endpoint-closure解”，不回答这个解是否自然、语义正确或能被网络摊销学习。

| version / run | operator / gap | far／masked root | far／masked global joints | far／masked root-translation-aligned joints | latent edit retention | decision |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| v11 shared Stage1 / `v11_shared_human128_endpoint_oracle_n8_seed17_5090g3_20260731` | linear / `25%` | `0.0402` | `0.0349` | `0.0284` | `1.0253×` | pass |
| v11 shared Stage1 / `v11_shared_human128_endpoint_oracle_n8_seed17_5090g3_20260731` | reverse / `25%` | `0.0064` | `0.0057` | `0.0068` | `1.0202×` | pass |
| v11 shared Stage1 / `v11_shared_human128_endpoint_oracle_n8_seed17_5090g3_20260731` | linear / `50%` | `0.0025` | `0.0029` | `0.0028` | `1.1212×` | pass |
| v11 shared Stage1 / `v11_shared_human128_endpoint_oracle_n8_seed17_5090g3_20260731` | reverse / `50%` | `0.0045` | `0.0042` | `0.0035` | `1.0165×` | pass |

far root ADE的代表性变化为：linear `25%`从`0.2517 m`降到`0.0050 m`，linear
`50%`从`0.7642 m`降到`0.0009 m`；far global MPJPE分别从`0.2619 m／0.8100 m`
降到`0.0076 m／0.0013 m`。但reverse proposal的masked global MPJPE在`25%／50%`
从`0.1803 m／0.3765 m`变为`0.2627 m／0.4852 m`。预声明gate只要求保留latent edit
幅度，没有把deterministic proposal当作mask内GT；因此这不是gate violation，却明确
说明oracle不能被包装为可用编辑质量。

本结果授权的唯一下一步是：冻结generation endpoint，以同样的root／heading far
endpoint loss训练一个短程mask-aware Human head，并同时gate semantic edit、boundary
continuity、masked motion quality与generation replay。该短screen通过前，Human MAE
长训与论文editing claim仍不授权；本oracle也不能抬高C0 generation ceiling。

## 4. Artifact identity

- contract SHA-256：
  `89f3810983dfec084825aa82e9ff5c7e10d2da53c22d8dd3a5e70a9ab952381f`
- results SHA-256：
  `61533b369a8336cff2fde407d5aa502a9f08922f95d6d9c7c4e67997ee13d798`
- records SHA-256：
  `2fcfc3ad54b36a82f655c0dbb5b015fa7d739ff12c532a0d280843579d048254`
- fixed samples SHA-256：
  `444a8477e5a7f9bbdf5b07f932c72239c12e3236b6ebf8f4a31c8b36de287590`
- canonical run status：`screen_failed_world_endpoint_locality`；train／eval／vis共用
  同一run id，train root manifest持有上述artifact引用。

Endpoint oracle另由同一functional layout保留：

- contract SHA-256：
  `b515894c71aa1e1af93822e29a1ac189c9d17ca621db577ca38589783231de16`
- results SHA-256：
  `975a5541e86aef747aa656ace4c7cee4ef5d59eddc29950ae9ab407910d01851`
- records／optimizer trace／fixed samples SHA-256：
  `28f12625d5bfa1099cc83fafbeee84911bc6c8f9c1b5062c916e403c3c5faf57`／
  `258458cff0a2fae23907983e354c6126854d1b3d1176c243e883b5ce68334a32`／
  `e878a74d9179d56e777e53f39bc4fd8937f4f31e3d9347f55fabe8082de9f99a`
- canonical run status：`oracle_pass_short_screen_authorized`。
