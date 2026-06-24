---
created: 2026-04-17
updated: 2026-04-21
status: active
title: "TAMR Roadmap"
---

# TAMR Roadmap

> 指标释义与公式见 `METRICS.md`。

> 唯一活跃路线图。个人思路原稿见 `2026-04-19_ripemangobox_roadmap.md`。
> 旧版 roadmap 已归档至 `archived/roadmap_history/`。

## RULE

1. 不强求独立成文，做出效果为第一目标。
2. 复用 MotionPatches `14×5` patch grid，创新集中到 structured score。
3. 训练和推理保留 global retrieval 路径，structured path 必须参与最终排序。
4. 样本按 `single / ordered / parallel` 三类处理。

## 核心假设

**structured matching > global matching**：event-segment 有序匹配的 retrieval score 优于纯 global cosine。

## 竞争格局

```
                Spatial 粒度
                Global              Joint/Part-level
Temporal  Global │ TMR, MoCHA        │ PST, MaxSim         │
粒度              │                   │                     │
          ──────┼───────────────────┼──────────────────────┤
          Event/│ 旧 TAMR (S2E-v2)  │ ← 空白 ← 我们的位置  │
          Ordered│ (delta 太小)      │                      │
```

## 方法概要

- Text side：caption → event decomposition → event encoder → per-event embedding + body-group weight
- Motion side：MP `14×5` patch tokens → 沿时间维池化为 14 segment tokens（保留 5 body-group）
- Matching：event × segment 相似度 → ordered 样本用 monotonic DP；parallel 放宽顺序；single 走 global fallback
- Score：`λ_g · global_score + λ_s · structured_score`（v1 先做 rerank，不替换 global score）
- Loss：`L_global + L_order(shuffle vs correct) + L_struct(hard neg) + L_group(稀疏约束)`

## 执行顺序

### Phase 0：默认配置锁定 ✅ 已基本完成

轻量消融结论（⚠️ 非 MP 原生架构，基于 2 层 Transformer baseline）：

- `kimodo_like_261` 略优（14.16），`pos66` 仅差 0.11（14.05）
- text encoder 收益 schema-dependent：`kimodo + t5-base` 最优（+1.22），`pos66` 对 text encoder 不敏感
- `vanilla TMR + HumanML3D-E-MP` 的 6-way motion rep eval 已完成：
  - `kimodo261` 最强（`PrimaryScore=40.58`）
  - `pos66 / hml272 / hy201` 第二梯队（`37.35~37.46`）
  - `guo263` 只是内部 baseline，不再是最优
  - `smpl135` 基本 collapse，当前不再作为候选

**决策：MotionPatches 的 R1 仍用 `pos66 + DistilBERT`**（MP 原生表示，零额外变量）。
若继续扩 vanilla TMR 线，`kimodo_like_261` 是最强 motion rep 候选。完整消融推迟到 R1 通过后，在 MP 架构上做 2×2（`{pos66, kimodo_like_261} × {DistilBERT, t5-base}`）。

### Phase 1：R1 核心方法验证（当前最高优先级）

目标：验证核心假设 "structured matching > global matching"。

> ⚠️ Training-time event alignment 路线（D1/D2a/D2b/P2a）已基本证伪：evt_align loss 与 global retrieval loss 存在梯度冲突，所有变体均不如 vanilla TMR baseline。转向推理时 structured rerank。

策略：先在 TMR 上验证（代码和 checkpoint 都在），通过后再迁移到 MotionPatches。每一步是前一步的 gate。


| Step  | 验证目标                       | Gate 条件                            |
| ----- | -------------------------- | ---------------------------------- |
| R1-S0 | TMR temporal tokens 有时序区分度 | 余弦相似度随窗口偏移单调下降                     |
| R1-S1 | Event embeddings 有意义       | event-motion sim > random baseline |
| R1-S2 | Top-K ceiling 足够高          | ceiling@100 > 80%（K≥2 子集）          |
| R1-S3 | Reverse-order sanity       | 正序 > 反序比例 > 60%                    |
| R1-S4 | Structured rerank 端到端      | K≥2 子集 R@1 > +2pp                  |


详细实验设计见 `ROADMAP_naive_stage1.md`。

Smoke gate（全局）：

- K>=2 子集上 CAR/TAR 相对 plain00 > +3pp
- 或全局 PrimaryScore > 44.5（超过 S2E-v2 fair 的 44.45）

### Phase 2：消融 + 空间扩展（R1 通过后）

- MP 架构上 motion rep × text encoder 2×2 消融
- 用最优配置重跑 R1
- V2 Joint-Group Refinement：在 segment 内引入 body-group 打分，验证空间细粒度是否必要

### Phase 3：并行感知 + 收尾

- V3 Parallel-Aware Relaxation：仅在误差分析显示必要时启动
- 完整 ablation table + error analysis + 可视化

## Smoke Gate（全局）

- 新方法必须在 packaged-root fair eval 下超过 `S2E-v2 fair = 44.4487`
- `normal` 和 `nsim` 不能一升一降换分
- 单 seed `<= +0.5` 增益不继续扩线

## 已知风险

1. **Training-time event alignment 已证伪**：D1/D2a/D2b/P2a 路线在当前 loss 设计下均不如 vanilla TMR baseline。evt_align loss 与 global retrieval loss 存在梯度冲突。已转向推理时 rerank。
2. **K=1 占比 ~50.7%**：一半样本无法受益 → 全局指标涨幅可能仅 1~2pp → 缓解：分层报告 condition2/3/4
3. **14-bin 固定切分 vs 语义边界不对齐** → 缓解：先跑 fixed 14-bin，不够再上 soft position prior
4. **structured score 噪声拖累 global score** → 缓解：Phase 1 只做 rerank，风险隔离
5. **TMR temporal tokens 可能无时序区分度** → 缓解：R1-S0 gate 验证，不过则需换 backbone

## Motion 侧池化策略备忘（不影响 Phase 1 MVP）

Phase 1 用 14 segment tokens（沿 body-group 池化）验证有序匹配假设，以下三条为后续升级预留路径：

1. **segment encoder 保留未池化的 14×5 patch tokens 作为备选输出。** Phase 2 引入 joint-group 或 late interaction 时可直接使用，不需重训 motion encoder。实现：segment encoder 同时输出 `seg_tokens [B,14,D]` 和 `patch_tokens [B,14,5,D]`，Phase 1 只用前者。
2. **若 Phase 1 DP 路径质量分析显示 bin 边界不对齐是主要错误来源，Phase 2 优先考虑 late interaction（event token 直接与 70 patch tokens 做 MaxSim + 时序约束），而非增加 bin 数量。** 增加 bin 需改 MP patch grid，代价大；late interaction 只改 matching module，motion encoder 不动。
3. **不在 Phase 1 引入 learnable segmentation 或 cross-attention token selection。** 这些是 Phase 2+ 的可选升级，当且仅当 fixed 14-bin 被证明是性能瓶颈时才启动。

## 设计借鉴

- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]：event 作为最小语义单元
- [[paperAnalysis/Motion_Generation/ECCV_2024/2024_ChroAccRet_Chronologically_Accurate_Retrieval_for_Temporal_Grounding_of_Motion_Language_Models|ChroAccRet]]：chronology negatives
- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction|MaxSim]]：token-patch late interaction
- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval|PST]]：joint→segment→global 层级对齐
- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]：motion token 结构化分解

## Stop List

- 不再叠 auxiliary head / adapter / evidence head
- 不再把 REF00 当新方法线
- 不再扩写 phase / hybrid 叙事
- 不再把 motion representation 小改动当核心机制突破
- Phase 0.5（ClipModel 下完整消融）等 R1 有正信号后再做
