---
created: 2026-04-29T20:35
updated: 2026-05-01T15:05:48+08:00
title: MoDebug Attention Filter Evaluator Pipeline Update
status: archived
tags:
  - MoDebug
  - evaluator
  - attention-filter
  - temporal-evaluator
  - pipeline-update
source_papers:
  - "[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Q_Zoom_Query_Aware_Adaptive_Perception_for_Efficient_Multimodal_Large_Language_Models|Q-Zoom]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Zooming_without_Zooming_Region_to_Image_Distillation_for_Fine_Grained_Multimodal_Perception|Zooming without Zooming]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_How_Do_Transformers_Learn_to_Associate_Tokens_Gradient_Leading_Terms_Bring_Mechanistic_Interpretability|How Do Transformers Learn to Associate Tokens]]"
related_notes:
  - "[[2026-04-29_modebug-roadmap]]"
  - "[[2026-04-29_modebug-exec-plan]]"
  - "[[2026-04-29_modebug-full-vs-event-level-alignment-analysis]]"
  - "[[2026-04-29_modebug-evaluator-status-summary]]"
  - "[[2026-04-29_modebug-attention-extraction-feasibility]]"
  - "[[paperIDEAs/MoDebug/2026-04-30_modebug-render-video-mllm-sidecar-feasibility]]"
---
# MoDebug Attention Filter Evaluator Pipeline Update

> [!warning] Archived
> This note is implementation support for the Temporal Evidence Filter. It is not an active evaluator entry. Current MoDebug entry, terms, and active file list are in [[ideas/MoDebug/README]].

> [!abstract] **TL;DR**
> - attention filtering 值得作为 MoDebug 的新支线尝试，但不应直接替换当前正式 evaluator 栈。
> - 正确切入点不是 raw attention judge，而是 **relative / counterfactual attention + corruption calibration**。
> - 近期建议新增 `Temporal Attention Filter`：先做 generation observation、evidence routing 和 event interval mining，再决定是否进入 guidance 或 learned evaluator。
> - Event-T2M 内部 G1/G2 attention extraction 已 opt-in 跑通并完成 `256` condition rows；raw cross-attention finite 但 diffuse，且现有 artifact 缺 per-head metric，当前不应进入 reward。
> - 后续如果 signal 成立，可发展成 `Interval-to-Full-Motion Distillation`，把 ZwZ 的 region-to-image 思路迁移到 temporal evaluator。

## 1. 固定假设

这份 note 的映射假设如下：

1. Q-Zoom 和 ZwZ 的原始对象是空间区域；MoDebug 需要把 `region` 映射成 `event temporal interval / latent denoising window`。
2. 当前正式 evaluator 仍保持 `Event-T2M self eval` + `TMR omission side signal` + `ChronAccRet ordering evidence / omission cross-check`，attention filter 暂时只作为新增诊断层。
3. attention 信号优先从 motion-native 链路提取；如果 Event-T2M 内部 attention 难以稳定取得，再走 render-to-video + MLLM attention sidecar。
4. attention filter 的第一目标是判断“看哪里”和“是否需要更贵 evaluator”，不是直接给最终 paper metric。

## 2. 三篇论文给 MoDebug 的直接启发

[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Q_Zoom_Query_Aware_Adaptive_Perception_for_Efficient_Multimodal_Large_Language_Models|Q-Zoom]] 的关键启发是：不要给所有 query 同样的感知预算。先用 query-aware gating 判断是否需要高分辨率，再用 self-distilled RPN 定位 RoI。迁移到 MoDebug，就是先判断某个样本是否需要 expensive temporal evaluator，再定位哪个 event interval 最可疑。

[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Zooming_without_Zooming_Region_to_Image_Distillation_for_Fine_Grained_Multimodal_Perception|Zooming without Zooming]] 的关键启发是：如果测试时 zoom 工具有效，可以把工具行为前移到训练期，生成干净局部监督，再蒸馏回全局输入。迁移到 MoDebug，就是先用 event segment / temporal crop / interval overlay 产生高置信监督，再训练模型在 full motion 上恢复 event-level temporal evidence。

[[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_How_Do_Transformers_Learn_to_Associate_Tokens_Gradient_Leading_Terms_Bring_Mechanistic_Interpretability|How Do Transformers Learn to Associate Tokens]] 的关键提醒是：attention 的底层来源更像语料统计诱导的 association，而不是天然的 error detector。它可以解释模型为什么看某些 token，但不能保证模型会对 drop / replace / shuffle 敏感。

因此，attention 本身不是 error detector 的担心仍然成立；变化在于，现在可以把 attention 放进一个可验证流程里，而不是把 raw attention 直接当 verdict。

## 3. 推荐新增模块：Temporal Attention Filter

建议在 generation observation 与正式 guidance 之间插入一层：

```text
HumanML3D-E ordered events
  -> Event-T2M generation / GT motion
  -> Temporal Attention Filter
  -> TMR / ChronAccRet / human review routing
  -> optional inference-time guidance
```

`Temporal Attention Filter` 的职责：

1. **event interval miner**：为每个 `event_k` 找一个候选时间峰值或区间。
2. **corruption-sensitive evidence logger**：比较 original / drop / replace / shuffle 下 attention 是否按预期变化。
3. **query-aware evaluator router**：把低置信、强冲突、疑似 omission/order violation 的样本送给更贵 evaluator 或人工复核。
4. **future lightweight evaluator seed**：如果 attention signal 稳定，再蒸馏成小模型或 reward feature。

它暂时不承担：

1. 不作为最终 ordering metric。
2. 不替换 ChronAccRet。
3. 不在 Gate 通过前进入 sampling guidance 主回路。

## 4. attention 不能 raw，用 relative / counterfactual

raw attention 的问题是它可能只反映常见语义关联、token 频率、全局 summary 或模型习惯，而不是当前 event 是否真的发生。

建议改成四类相对信号：

1. **query-relative attention**  
   `A(event_k query) - A(generic motion query)`，去掉通用视觉/动作 summary 成分。

2. **corruption-relative attention**  
   比较 `full original events` 与 `drop / replace / shuffle` 的 event attention。若 drop 后目标 event 的峰值和覆盖率不下降，说明 attention 对 omission 不敏感。

3. **order-relative attention**  
   记录每个 event 的 attention peak time，检查 `peak(event_i) < peak(event_j)` 是否与文本顺序一致。shuffle 后如果 peak order 不变，说明这条 attention 不足以做 ordering evidence。

4. **distractor margin**  
   用 hard negative event query 与真实 event query 比较 attention concentration 和 motion-text score。若 distractor 也能获得相似峰值，说明 attention 只是找到了常见动作区域。

最小日志字段建议追加到 manifest 或独立 jsonl：

```yaml
sample_id: "004965"
event_idx: 2
event_text: "a person picks something up."
condition: "full_original"
attn_peak_t: 0.42
attn_interval: [0.31, 0.52]
attn_mass_top_interval: 0.37
attn_entropy: 1.84
relative_gap_vs_generic: 0.12
relative_gap_vs_corrupted: 0.19
order_peak_rank: 2
flag:
  - candidate_middle_event
  - route_to_human_review
```

## 5. 对当前 pipeline 的具体更改

### 5.1 近期：作为 generation observation lane，不改主结论

当前 evaluator status 不需要重写。Temporal Attention Filter 应放在 [[2026-04-29_modebug-exec-plan|Exec Plan]] 的 generation observation lane 中，而不是作为新的正式 evaluator：

```text
G1: attention map observation
G2: denoising trajectory observation
G3: gradient sensitivity observation
G4: inference-time guidance MVP
```

该 lane 的输入是 `HumanML3D-E` ordered events、GT motion、Event-T2M on-policy samples，以及已有 corruption family：`drop / replace / shuffle`。

输出不是一个总分，而是三类 evidence：

1. `coverage evidence`：event query 是否集中到一个合理 interval。
2. `sensitivity evidence`：corruption 是否改变对应 attention。
3. `routing evidence`：attention filter 是否能提高 human-review / ChronAccRet / TMR 的有效命中率。

已同步的 implementation / observation 状态：

1. Event-T2M 的 `MiniConformer.cross_attn` 是关键 hook；已新增 opt-in instrumentation，默认采样行为不变。
2. G1/G2 logging 已打开 `need_weights=True`、`average_attn_weights=False`；但已落盘的 `observations.jsonl` 只保存 head-averaged summary，没有 `head` / `head_idx` / per-head metric。
3. G3 不能直接复用默认 sampling path，因为 `sample_motion()` 被 `@torch.no_grad()` 包住；只能在 frozen denoiser 的窄作用域 diagnostic forward 中局部启用 gradient。
4. `linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/g1g2_condition_probe_64samples_step10/observations.jsonl` 已完成 `256` condition rows、`10240` attention records、`0` finite failure。
5. `g1g2_observation_analysis_summary.json` 显示 full normalized entropy mean `0.9962925080675632`，condition-order peak match `0.05234375`；`head_filtering_analysis.json` 进一步给出 `blocked_no_per_head_artifact`。因此 raw attention 只能继续作为 observation / routing candidate，不是 reward feature。

### 5.2 中期：Q-Zoom 式 gating

把 Q-Zoom 的 `是否需要高分辨率` 改成 MoDebug 的 `是否需要 temporal evaluator escalation`：

```text
low uncertainty + no order violation
  -> bypass expensive evaluator, only log TMR / generation sanity

high entropy / low event coverage / peak-order violation / high distractor margin
  -> run ChronAccRet / TMR cross-check / human review / optional MLLM sidecar
```

这个 gating 可以先不训练，直接用阈值版；等样本积累后，再用 consistency labels 自监督训练：

```text
cheap attention/TMR decision agrees with expensive evaluator
  -> bypass label

cheap decision disagrees with ChronAccRet / human review / stronger MLLM sidecar
  -> escalation label
```

高风险路由不包含 `AToM`。它只保留为 MotionGPT native eval reproduction record，不能作为 current MoDebug evaluator、scorer 或 judge。

### 5.3 后期：Interval-to-Full-Motion Distillation

如果 G1-G3 证明 attention / gradient 确实能稳定定位事件区间，则可以迁移 ZwZ：

```text
event interval crop / temporal segment
  -> teacher verifies event presence/order on segment
  -> add interval overlay / timestamp hint during training
  -> distill back to full motion or rendered full video
  -> test-time remove interval hint
```

这相当于把 `Region-to-Image Distillation` 改成 `Interval-to-Full-Motion Distillation`。训练时 interval 是 privileged information；测试时模型必须在 full sequence 里自己找 evidence。

对应的 MoDebug 版 dual-view protocol：

```text
Regional / Segment View:
  给 teacher 或 evaluator 只看目标 event segment

Global / Full Motion View:
  给 evaluator 看完整 motion

Temporal Zooming Gap:
  segment-view 能判别，但 full-motion view 判别失败的比例
```

这个 gap 能把两种失败拆开：

1. 事件本身不可识别。
2. 事件可识别，但 evaluator 在完整序列里找不到它。

## 6. Go / No-Go Gates

### Gate A：localization sanity

在 GT motion 和少量人工可读样本上，event attention 的 peak / interval 必须大体落在符合事件描述的时间段。若没有人工标注 interval，可先用粗窗口、event count partition、人工 10-20 条复核作为弱验证。

最低通过标准不是追求高精度边界，而是证明它不是均匀分布或固定位置偏置。

当前状态：raw cross-attention 未通过 Gate A。`256` condition rows 中 attention finite，但 normalized entropy 均值接近 `1.0`，condition-order peak match 只有 `0.05234375`。后续 filtering 发现现有 artifact 缺 per-head metric，无法判断少数可用 head subset。

### Gate B：corruption sensitivity

在 `drop / replace / shuffle` 上必须有方向正确的变化：

1. `drop event_k` 后，`event_k` 的 relative attention mass 或 TMR score 应下降。
2. `shuffle events` 后，attention peak order 应更容易违反原始顺序。
3. `replace` 后，真实 event query 与 distractor query 应出现 margin。

如果 raw attention 在这些 corruption 下几乎不变，这条路线只能保留为 logging，不进入 evaluator。

当前状态：Gate B 为 mixed。full-vs-replace 的 target peak shift mean 为 `82.682421875` frames，full-vs-shuffle 为 `57.181640625` frames，说明 corruption 会扰动 peak；但方向语义尚未建立，不能直接升级为 reward。

### Gate C：routing gain

attention filter 必须提高后续 evaluator 的有效使用率。可验证方式：

1. attention 高风险样本中，人工或 ChronAccRet 确认的 ordering/omission 问题比例更高。
2. attention 低风险样本中，generation quality 和 temporal metrics 不出现系统性坏例。
3. routing 后总体计算量下降或人工复核命中率上升。

### Gate D：guidance safety

只有 Gate A-C 通过后，才允许把 attention-derived interval 送进 inference-time guidance。进入 guidance 前还要做 gradient health check：梯度不爆、不破坏 CFG 采样稳定性、不显著拉低 Event-T2M native generation metrics。

## 7. 近期最小实验

近期最小实验已完成，不直接上训练：

1. 样本：使用已固定 observation pool：`linkedCodebases/EventT2M-codes-main/logs/modebug_observation_pool/manifest.jsonl`，共 `64` 条 `HumanML3D-E test >=3 events`，含 4 条固定 seed 与 `28` 条 `5plus` 高风险样本。
2. 条件：每条保留 `full / drop / replace / shuffle`。
3. attention 源：优先探索 Event-T2M 内部 event-text 到 motion latent/timestep 的 attention；若不可取，按 [[paperIDEAs/MoDebug/2026-04-30_modebug-render-video-mllm-sidecar-feasibility|Render-to-Video + MLLM Sidecar Feasibility]] 做小样本 sidecar pilot。
4. 指标：记录 `attn_peak_t / interval mass / entropy / generic-relative gap / corruption-relative gap / event peak order`。
5. 判定：Gate A 未过，Gate B mixed，不把结果写成正式 evaluator。

日志字段以 `linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/schema.yaml` 为准；README 中的 Gate A-D 只定义 observation gate，不定义 final evaluator。

这个实验已回答最关键的问题：

> attention 对 MoDebug 的 ordering / omission 是有 counterfactual sensitivity，还是只是在看常见正确关联？

当前答案：raw attention 有工程可提取性，也会被 corruption 扰动，但过于 diffuse；现有 artifact 无法做真实 per-head filtering。下一步只能二选一：改 logging 保存 per-head metric 后小规模重跑，或转入 render-to-video + MLLM sidecar pilot；二者都不能直接进入 guidance。

## 8. 叙事收口

paper-safe 的说法应是：

> We introduce an attention-guided temporal evidence filter to route ambiguous samples and mine event intervals, while keeping formal temporal evaluation separate. Raw attention is not treated as a judge; it is calibrated by event corruptions and only promoted when it shows counterfactual sensitivity.

中文收口：

> attention 过滤不是新主 evaluator，而是 `temporal evidence filter / interval miner / evaluator router`。只有当它在 drop、replace、shuffle 上显示出稳定的反事实敏感性，才升级为 reward feature 或轻量 evaluator。
