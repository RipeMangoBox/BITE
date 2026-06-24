---
title: "MoDebug 支撑路线：VLM 输出交叉检查"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-20T00:00:00+08:00
status: active
tags:
  - MoDebug
  - VLM
  - output_crosscheck
  - support_route
---

# MoDebug 支撑路线：VLM 输出交叉检查

## 角色

VLM / PoseFix / trajectory evidence 只服务 decoded motion 的交叉检查。它们回答：

```text
候选 motion window 中是否有足够可见证据支持某个 text unit 或属性 cue？
```

它们不承担最终评价器角色，也不负责生成 MoDebug 的主机制解释。

## 当前边界

已有 VLM pilot 的保守结论见 [[paperIDEAs/MoDebug/VLM/README|MoDebug VLM README]]：

1. 适合可见姿态变化、显著肢体动作、转身、带轨迹叠加的往返位移。
2. 不适合精确步数、前进/后退、左右侧、回到起点的最终判断。
3. `0.5s` slice 适合 human check；`0.2s` 只做边界细化。
4. PoseFix 只做静态几何 cross-check。

## 使用策略

1. 不让 VLM 自由 caption 全序列后直接判分。
2. 先给定 `text_unit`、candidate window 和 expected cue。
3. 要求 VLM 输出 `evidence / uncertainty / limitation`。
4. 最终 label 写成 `diagnostic` 或 `cross_check`，并记录 evaluator、protocol、artifact_path、n/evaluable 与 coverage。

## 何时比较 Qwen-VL

只有在下面条件成立时才值得比较 GPT-5.5 VLM 与 Qwen-VL：

1. 已有候选 window；
2. human check 觉得窗口边界或弱动作看不清；
3. 输出只用于 cross-check；
4. 能记录每个模型的失败类型，而不是只看一个总分。
