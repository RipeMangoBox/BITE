---
title: "StoryMotion Current: v11 C0 Co-mainline"
status: v11_c0_lat_geo_co_mainline
hypothesis: |
  v11 C0-LAT and C0-GEO are co-equal system mainlines: they share one audited
  v9 Stage1/Human owner and differ only in the Camera objective. Keeping both
  preserves the observed semantic/geometry Pareto instead of selecting on
  statistically unresolved Camera geometry differences.
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
  - "[[2026-07-29_storymotion-v11-v9-owner-stage2-three-mode-rescue-contract]]"
created: 2026-07-12T14:30:00+08:00
updated: 2026-07-31T23:30:00+08:00
---

# StoryMotion Current: v11 C0 Co-mainline

> [!important] 当前裁决
> 自 2026-07-31 起，v11 C0-LAT 与 C0-GEO 的 EMA Camera `105K` endpoint
> 共同成为 StoryMotion mainline。两者同享 exact v9 Pulp-only Stage1、owning
> decoder/cache/train-only statistics 与冻结 Human `105K` teacher，只在 Camera
> objective 上分叉。C0-GEO 相对 C0-LAT 的 Direct-C 与 sequential 六项 Camera
> geometry 95% CI 全部跨零，语义、覆盖与构图字段又形成混合 Pareto，因此不把
> 任一臂降为 subordinate alternate。C3-25 转为 former-mainline system baseline。

本页只拥有当前选择、允许的 claim、活跃 blocker 与 evidence link。正式数字与哈希
只见 [[StoryMotion-valid-metric-ledger]]；版本事件只见 [[version_family]]；论文中稿
差距与实验优先级只见 [[StoryMotion-iclr-reliability]]。

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

StoryMotion 的目标是中稿 ICLR 2027。当前最可信的中心主张不是“全面 SOTA”，而是：

> 以 non-causal asymmetric Human-first factorization，将 Human generation、
> observed-Human Camera completion 与 sequential joint generation统一到一个可审计
> 系统中；保护 Human owner，并用 LAT/GEO 双 endpoint 显式保留 Camera
> semantic／geometry Pareto。

这一定义下，C0-LAT 与 C0-GEO 是同一方法的两个报告 endpoint，不是两个互相竞争
的论文方法。数值比较、视觉对比和局限必须同时呈现两者。

## 4. 活跃 blocker

1. **Stage1 设计依据。** v9 Stage1 的 Human anchor、interaction residual 与三阶段
   schedule 偏复杂。需要把每个部件绑定到明确 failure mode，并用最小 matched
   ablation 证明必要性；不能只以“v10 更简单但退化”代替，因为 v10 同时改变了
   owner、Camera factorization、loss 与下游训练，尚不是干净反证。
2. **统计与感知证据。** 当前主线选择主要来自 seed17。论文还需要独立重复、盲评／
   人体偏好与失败分层，避免只凭 development pure4,053 和均值指标定论。
3. **Editing scope。** 现有系统尚无 formal edit task、mask protocol 或对应训练阶段。
   若把 editing 写入主贡献，必须补任务定义与验证；若不补，则从标题、摘要和主
   contribution 中删除，只保留 future work。
4. **可复现性。** 需要冻结论文代码、配置、三模式 evaluator、checkpoint/decoder
   身份、训练成本和最小复现实验包。详细优先级与停止条件见
   [[StoryMotion-iclr-reliability]]。

## 5. 当前行动边界

- 冻结 C0-LAT 与 C0-GEO 两个 mainline endpoint，不因单个 raw mean 继续选臂。
- C1、v10 Camera Stage2、swapped-host replay 和新 Stage1 全量训练均不是默认下一步；
  只有它们直接关闭论文 hard gap 时才重新授权。
- 优先完成论文 claim、Stage1 因果依据、multi-seed／盲评和可复现实验矩阵。
- Editing 先做 paper-scope 决策，再决定是否设计训练阶段；不以“架构可能支持”写成
  已验证能力。

## 6. Canonical owners

- 当前选择、blocker 与行动边界：本页。
- 正式数值、公平对比与 artifact hashes：[[StoryMotion-valid-metric-ledger]]。
- 其余 run identity 与 visual index：[[Storymotion-exp-sha]]。
- evaluator／decoder／指标语义：[[StoryMotion-metric-computation-io]]。
- 版本完成事件与 invalidation：[[version_family]]。
- ICLR claim-evidence gap 与实验优先级：[[StoryMotion-iclr-reliability]]。
- v11 原始四臂合同与停止规则：
  [[2026-07-29_storymotion-v11-v9-owner-stage2-three-mode-rescue-contract]]。
