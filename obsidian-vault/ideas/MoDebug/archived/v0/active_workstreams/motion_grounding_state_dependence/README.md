---
title: "MoDebug 并行路线：Motion-Side Grounding 的可靠性与状态依赖风险"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-20T00:00:00+08:00
status: active
hypothesis: "motion-side event grounding 当前是并行资产路线；可靠性通过前不作为 MoDebug 主线前置条件，进入训练后必须处理 prefix-state shortcut 与 transition leakage。"
tags:
  - MoDebug
  - motion_grounding
  - state_dependence
  - data_augmentation
  - transition_modeling
---

# MoDebug 并行路线：Motion-Side Grounding 的可靠性与状态依赖风险

## 当前角色

motion-side event grounding 当前不是 MoDebug 插件评估的前置条件。MoDebug 主线可以只使用：

```text
full text -> baseline full motion
full text -> baseline+MoDebug full motion
```

本文件只管理并行 grounding 资产路线：先验证标注可靠性，再决定它是否进入更细粒度诊断、训练或论文附录。

## 可靠性关口

在进入任何 grounding-based training 前，先完成可靠性审计：

1. coverage：有多少 full motion 可以得到 candidate grounded units；
2. evaluator agreement：VLM、PoseFix、geometry、human check 的一致性；
3. uncertainty：每个 grounded unit 是否记录 uncertainty 与 limitation；
4. boundary ambiguity：是否区分 core evidence 与 transition 区域；
5. failure taxonomy：看不清、弱动作、左右混淆、步数不准、轨迹不准等失败类型是否单独记录。

通过条件：grounding 资产能稳定产出 `core window + uncertainty + limitation`，且不会把低置信边界伪装成干净监督。

## 问题定义

如果为 motion 侧添加 event grounding，训练样本往往会被写成：

```text
text_unit_k -> motion_segment_k
```

但真实生成过程更接近：

```text
start_state_k + text_unit_k + transition_context_k -> motion_segment_k -> end_state_k
```

其中 `start_state_k` 来自前一个事件结束时的姿态、朝向、root 速度、接触状态和动作相位。后续事件不是从静止标准姿态开始，而是从前缀 motion 的结束状态开始。因此，即使 VLM + PoseFix 能把 motion-side grounding 标注做得更干净，训练时仍然会遇到状态依赖问题。

## 是否会导致过拟合

会有明显风险，但它不是普通数据量不足导致的过拟合，而是 **条件状态混淆**：

1. `prefix-state shortcut`：模型学到“某类前序结束姿态后通常接某个动作”，而不是学到 text unit 的语义。
2. `transition leakage`：边界附近的过渡帧被归到前一事件或后一事件，模型把 transition cue 当成 event cue。
3. `position-order bias`：后续事件经常出现在固定时间位置，模型利用顺序或剩余时长 shortcut。
4. `state-event entanglement`：同一个动作事件在不同起始姿态、朝向、速度下应有不同实现，若训练只见过窄状态分布，会在新组合上失效。
5. `composition overfit`：模型能复现训练 clip 内的连续片段，但不能把同一 text unit 接到新的前序状态后。

所以，VLM + PoseFix 解决的是“能否标出可见证据”的问题，不解决“事件语义与前序状态是否可分”的问题。

## 数据增广能否解决

数据增广可以缓解，但不能单独解决。有效前提是训练目标要从独立片段改成状态条件化片段：

```text
p(motion_segment_k | text_unit_k)
```

应改为：

```text
p(motion_segment_k | text_unit_k, start_state_k, transition_context_k)
```

同时评估必须包含未见过的 `text_unit × start_state` 组合。如果只做普通随机增广，模型仍可能记住前缀状态分布。

## 推荐增广

### 1. 起始状态增广

目标：让同一个 text unit 见到更多起始状态。

可操作方式：

1. 按 root 朝向、root 速度、身体姿态、foot contact、motion phase 对 `start_state` 分桶。
2. 同一 text unit 采样不同 start-state bucket。
3. 对同一事件构造不同 pre-roll 长度，例如保留前 0、0.25、0.5、1.0 秒作为状态上下文。
4. 训练时显式输入 `start_state_summary`，避免模型把状态当隐变量记忆。

### 2. 边界扰动与 transition 软标签

目标：避免把边界标注误差变成强监督。

可操作方式：

1. 对 event boundary 做小幅 jitter，训练模型对边界附近不确定性鲁棒。
2. 把边界区域写成 `transition_or_uncertain`，不强行归入核心事件。
3. 对 loss 加 temporal soft mask：核心事件高权重，transition 低权重。
4. VLM / PoseFix 只为核心可见 cue 提供 cross-check，不裁决 transition 的精确归属。

### 3. 前缀交换与受控拼接

目标：检验同一 text unit 能否接到不同前序状态后仍保持语义。

可操作方式：

1. 在同一动作类别或相近 `start_state` bucket 内交换前缀。
2. 使用短 transition blender、IK 或 root trajectory smoothing 连接前缀与事件核心。
3. 用 PoseFix / geometry filter 去掉骨架畸形、脚滑严重或速度突变样本。
4. 拼接样本只作为 augmentation 或 stress test，不能直接当干净 ground truth。

### 4. 几何与时序不变性增广

目标：减少模型利用绝对坐标、朝向、速度模板的 shortcut。

可操作方式：

1. 全局平移和 yaw rotation。
2. 左右镜像，并同步替换 left / right 文本。
3. 合理范围内的 time warp，保留接触和相位一致性。
4. root trajectory 平滑扰动，检查 direction / path cue 是否仍可识别。

### 5. 反事实文本与状态配对

目标：迫使模型区分 text unit 与 start state。

可操作方式：

1. same start state + different text unit，作为 negative pair。
2. same text unit + different start state，作为 positive semantic pair。
3. drop / replace / shuffle 文本单元，检查 local score 是否只对目标单元变化。
4. 对比学习应拉近同一 text unit 在不同 state 下的语义证据，而不是只拉近整段 motion。

### 6. 历史上下文 dropout

目标：避免模型过度依赖前一个事件文本或完整前缀帧。

可操作方式：

1. 有时输入完整前缀状态。
2. 有时只输入 `start_state_summary`。
3. 有时 drop previous text unit。
4. 有时只保留核心 text unit。

如果性能只在完整前缀输入时高，说明模型可能依赖 prefix shortcut。

## 训练约束

训练目标应显式保留 grounded event 的状态条件，而不是把它当成独立动作片段。推荐记录：

```text
sample_id
text_unit_id
text_unit
segment_start
segment_end
core_start
core_end
transition_before
transition_after
start_state_summary
end_state_summary
prefix_context_path
grounding_evaluator
grounding_confidence
role
limitations
```

其中 `segment_*` 可以覆盖 transition，`core_*` 只覆盖高置信事件证据。训练 loss 应区分核心事件、transition 和不确定区域。

## 评估拆分

随机 split 不足以验证该问题。需要额外 held-out：

1. `heldout_start_state`：训练见过 text unit，但没见过该 start-state bucket。
2. `heldout_prefix_event`：训练见过当前 text unit，但没见过某类前序事件组合。
3. `heldout_transition_length`：训练没见过某个 transition duration bucket。
4. `heldout_composition`：训练见过单个事件，但没见过该事件序列组合。

只有这些 split 上仍然有效，才能说明 grounding 训练没有只记住前缀状态。

## 对 MoDebug 的结论

motion-side grounding 可以作为 MoDebug 的输出交叉检查和后续训练支撑，但当前主线先使用 full-text / full-motion 插件评估。

当前最稳妥的使用方式：

1. 主线先做 `baseline` vs `baseline+MoDebug` 的 full-motion paired evaluation。
2. grounding 并行做可靠性审计，只作为 `parallel_asset`。
3. 若进入训练，必须把 `start_state`、`transition` 和 `core event` 分开记录。
4. 数据增广优先服务状态解耦和 transition 鲁棒性，而不是盲目扩大样本量。
5. 论文中只在 held-out state / composition 评估通过后，才写 grounding-based training 带来泛化改善。
