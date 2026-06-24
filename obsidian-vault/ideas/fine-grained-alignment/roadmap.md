---
title: "MLPA 当前路线图"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-26T22:44:25+08:00
status: active
hypothesis: "MLPA 的投稿切口是跨领域机制启发的 event-time-body correspondence layer，而不是 motion related work 防撞综述或 MoDebug 的 text embedding 支线。"
tags:
  - MLPA
  - roadmap
  - mechanism_transfer
  - event_time_body_correspondence
source_papers:
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning|ActionPlan]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval|PST]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_MaxSim_Fine_Grained_Motion_Retrieval_Joint_Angle_Late_Interaction|MaxSim]]"
---

# MLPA 当前路线图

> [!abstract] 当前判断
> MLPA 可以和 MoDebug 独立成文，但贡献必须落到 **event-time-body correspondence layer**：用跨领域机制构造可审计的局部 text-motion 对应对象，再证明它能改善 timestamping、retrieval、rerank 或 verifier。pivot-first generation 是后置扩展，只有 correspondence layer 在定位和选择候选上成立后才进入。

> [!note] 2026-05-26 数据路线更新
> 主数据证据切到 Kimodo / BONES-SEED / SEED-Timeline。HumanML3D/HumanML3D-E 继续保留为 baseline-rich 的快速诊断和 VLM pseudo-label 工作台，但 Qwen3-VL-Plus 输出不得作为 event boundary ground truth 或 final evaluator。详见 [[2026-05-26_kimodo-seed-humanml3d-data-route|Kimodo/SEED 与 HumanML3D 双轨数据路线]]。

> [!note] 2026-05-26 MoLingo / PoseFix 分支更新
> MoLingo SAE retraining 暂定为 generator-backbone side branch：统一称 **TPA-SAE**，先在 SAE 上验证原始 semantic loss + Temporal-Phrase Alignment，而不是直接重训完整 generator。HumanML3D 的细粒度数据构造优先仿照 FineMotion 使用 PoseFix 片段几何描述，角色限定为 weak sidecar / diagnostic。详见 [[2026-05-26_molingo-sae-and-posefix-sidecar-route|MoLingo TPA-SAE and PoseFix Sidecar Route]]。

> [!note] 2026-05-26 4090 TPA-SAE 实验状态
> 远端 MoLingo 已切到 `TPA` 分支，当前有效 head 为 `45a3f2f`。已完成 `wm / tpa_abspos / token_sentence` 的代码实现、DS Max 检查、semantic loss 聚合修复、tensor smoke、fixed 真实 debug batch smoke 和 DeepSeek blocking-bug 复核；`45a3f2f` 前两个 short diagnostic 因 raw semantic loss 误入 total loss 作废。`tpa_abspos` 与 `token_sentence(sentence_ratio=0.5)` 两个 fixed short diagnostic 已完成并生成 `checkpoint-last.ckpt`，初始 `MPJPE=145.5051`、`FID=683.7445`，观测训练显存约 `2.3GB/GPU`，日志未检出 fatal error。本次角色仅为 `diagnostic`；由于没有 final eval 或中途 eval 曲线，下一步先补 `WM` 对照与 `batch_size=32` memory probe，再决定是否进入 `SL / WM / MWM / TPA-select` clean proof。

## 一句话主张

MLPA 构造一个模型无关的局部对应层，把 text events、body-part phrases 和 temporal attributes 对齐到 motion chunks、body-part tokens 与 root-contact cues，从而支持 motion timestamping、candidate rerank 和 verifier / guidance。

## 问题重构

当前 text-motion alignment 的瓶颈不是简单的 text encoder 不够强，而是三种压缩同时发生：

1. `text compression`：多事件、顺序、频率、部位信息被压入全局文本表征。
2. `motion compression`：长 motion 被压成 sequence latent 或 code tokens，局部时间和身体结构不一定可检索。
3. `correspondence compression`：即使全局 text-motion 匹配高，也不知道哪个 text span 对应哪个 motion segment。

因此 MLPA 的目标是：

```text
global text-motion matching
-> event / phrase / attribute to time / body / cue correspondence
```

## 跨领域机制迁移

| 来源领域 | 可迁移机制 | Motion-specific translation | 不可照搬 |
| --- | --- | --- | --- |
| 3DGS | explicit sparse anchors、local residuals、visibility / coverage、densification | event / body / contact pivots；低置信区域局部补采样或细化 | photometric / projection geometry 等价 |
| Triplane | factorized low-dimensional interaction planes | `time × body-part`、`time × semantic-unit`、`body-part × attribute/contact` planes | radiance-field generator |
| MLLM / A.I.R. | query-aware evidence acquisition | text-unit conditioned boundary search；粗候选、局部验证、DP / OT 聚合 | 全视频自由 caption 总分 |
| Bottleneck / ACCORD / A2D | global condition bottleneck、dependence probe、span-level target | drop / replace / shuffle / mask-part counterfactual locality；wrong unit-wrong chunk dependence bias | 外领域公式直接搬运 |

详见 [[ideas/fine-grained-alignment/mechanism_transfer/README|跨领域机制迁移笔记]]。

## 对应对象

MLPA 输出不是一个总分，而是一组局部对应：

```text
T_events = {event_k}
T_phrases = {body_phrase_j, attribute_j}
M_chunks = {time_window_n}
M_parts = {body_part_b}
M_cues = {root/contact/velocity/pose cue}

A_event_time[k, n]
A_phrase_part_time[j, b, n]
null_mass[k]
monotonic_path
confidence / uncertainty
```

每个高分对应都应该能回到 text unit、motion window、body part 和 evidence cue。

## 最小可行序列

### MVP-0：Data Contract / Dataset Gate

目标：先确认 event text、motion path、timestamp、split 和 evaluator 角色，避免把自建伪标签或非官方 split 写成官方监督。

当前数据角色：

1. Kimodo / SEED-Timeline：主线 event-time supervision。
2. Kimodo official train split cache：只允许作为 disposable engineering cache，不参与 final evaluation。
3. HumanML3D/HumanML3D-E：baseline、failure bank、窗口级 Qwen diagnostic 和 small-scale ablation。

通过条件：

1. Kimodo/SEED event fields 能映射到 motion path 与 frame window；
2. official split、disposable cache 和 diagnostic data 的角色分开记录；
3. Qwen/VLM 输出只记录为 pseudo-label 或 diagnostic；
4. 每条 metric 保留 `role`、`used_for` 和 `limitations`。

### MVP-A：Event-Guided Motion Timestamping

输入：ordered text units + original full motion。

输出：每个 text unit 的 verification scaffold，包括 candidate window、confidence、null / ambiguous label、body-part group、root / contact / velocity cue 和 evidence trace。

通过条件：

1. text-unit-to-chunk retrieval 优于 full-prompt global matching；
2. timestamping 优于 equal-duration split；
3. 对 late unit / order / count 的失败能产生更高 uncertainty 或 null mass；
4. human cross-check 支持主要 window。

### MVP-B：Frozen MLPA Rerank【删去】

输入：同一 prompt 的多候选 generated motions。

输出：基于 local correspondence 的 rerank score。

通过条件：

1. human / held-out instruction satisfaction 优于 global scorer rerank；
2. drop / replace / shuffle counterfactual locality 有效；
3. 分数提升不能只来自 prompt expansion 或 LLM planning baseline。

### MVP-C：Verifier / Guidance Readiness

目标：把 verification scaffold 用于局部判断和轻量推理时控制，同时继续隔离 correspondence 能力与 generator 训练能力。

允许的形态：

1. local verifier；
2. candidate rerank；
3. low-confidence chunk resampling；
4. small adapter；
5. masked cross-attention gating。
6. MoLingo TPA-SAE short-run ablation，但只能作为 generator-backbone side branch。

禁止的形态：

1. 从零训练新 generator；
2. 把 MLPA verifier 写成 final evaluator；
3. 在没有 timestamping 或 rerank 正信号时加入 alignment loss；
4. 把 LLM prompt expansion 当作 scaffold 贡献。
5. 把 MoLingo TPA-SAE 内部 side signal 当作 MLPA 主表 evaluator。

通过条件：

1. verifier / guidance 不只提升 MLPA 自身分数，也提升 human / independent instruction satisfaction；
2. naturalness、diversity、contact realism 不显著退化；
3. low-confidence / null 记录能解释失败样例，而不是强行打高分。

### MVP-D：Pivot-First Generation Extension

生成阶段的新明确点是：MLPA 的 pivot 不只用于 representation-side semantic alignment，也可以作为 generation-side scaffold。但它必须是后置阶段，只有 timestamping / rerank / verifier 已经证明 correspondence 有用后才进入。

候选形态：

```text
text events / body phrases / temporal attributes
-> generation scaffold
-> fine-grained event / body-part motion refinement
-> MLPA verifier / rerank / local resampling
```

这条路线借鉴 MoMask 的基础层 token + residual refinement 和 ActionPlan 的先 plan 后 motion，但 MLPA 的差异在于：coarse level 不是纯 motion quantization 或 frame action label，而是可审计的 event-time-body semantic pivot。

generation scaffold 的当前定义：

```text
event windows
body-part activity map
root / contact cue map
duration and order constraints
null / low-confidence regions
optional transition slots
```

进入条件：

1. MVP-A 或 timestamping gate 证明 event unit 能稳定定位 motion chunks；
2. MVP-B 或 frozen rerank 证明 local correspondence score 能改善候选选择；
3. MVP-C 证明 verifier / guidance 对 human 或 independent evaluator 有正信号；
4. body-part / contact cue 至少有一个局部 probe 通过；
5. 生成改进不能只来自 LLM prompt expansion。

## 可以写的贡献

1. model-agnostic event-time-body correspondence layer；
2. ordered text units 的 motion-side timestamping protocol；
3. generation-oriented local verifier / reranker；
4. 3DGS / triplane / MLLM 机制的 motion-specific translation；
5. counterfactual locality / null-mass / monotonic correspondence diagnostics；
6. 后置的 pivot-first generation scaffold，如果先通过 timestamping / rerank / verifier 关口。

## 不能写的贡献

1. 首次 semantic motion latent；
2. 首次 event-level conditioning；
3. 首次 body-part control；
4. 首次 symbolic planner；
5. DP / OT / MaxSim 算子原创；
6. VLM 是最终 evaluator；
7. 解决全部 text-motion alignment。
8. BABEL 提供完整 event-time-body ground truth。
9. pivot-first generation 是第一阶段主 claim。

## 与 MoDebug 的关系

MoDebug 可以提供 stress cases 和扰动规范，但 MLPA 的主实验必须证明 correspondence layer 本身有用。

允许共享：

1. hard multi-event prompts；
2. `drop / replace / shuffle` counterfactual probe；
3. human / VLM cross-check 的证据规范。

不能共享为主 claim：

1. generator-internal trace diagnosis；
2. propagation signature；
3. signature-targeted guidance。

## 下一步三关

1. 关口 0：直接使用 Kimodo/SEED 官方 timeline 与官方 split 打通 event text、frame window、motion feature 和 correspondence record。
2. 关口 1：用 existing motion + ordered text units 做 unit-to-chunk retrieval，比较 global full prompt baseline。
3. 关口 2：加入 body-part phrase / contact-root cue，验证 part localization 优于 wrong body group。
4. 关口 3：把 correspondence score 用于 frozen rerank，比较 global scorer 与 LLM-plan baseline。
5. 若前 3 关通过，再试 generation scaffold -> event-detail refinement 的轻量 generator coupling。
6. 并行做 MoLingo TPA-SAE memory probe：用户指定的 `tpa_abspos` 与 `token_sentence` fixed short diagnostic 已完成并保存 checkpoint；下一步补 `WM` 对照与 `batch_size=32` memory probe，再进入 `SL / WM / MWM / TPA-select` clean proof。该分支只用于判断是否值得后续 generator coupling。

详细表见 [[gates|实验关口]]。

补充判断见 [[2026-05-24_pivot-first-generation-route|Pivot-First Generation Route for MLPA]]。

数据路线补充见 [[2026-05-26_kimodo-seed-humanml3d-data-route|Kimodo/SEED 与 HumanML3D 双轨数据路线]]。

MoLingo TPA-SAE 与 PoseFix sidecar 补充见 [[2026-05-26_molingo-sae-and-posefix-sidecar-route|MoLingo TPA-SAE and PoseFix Sidecar Route]]。
