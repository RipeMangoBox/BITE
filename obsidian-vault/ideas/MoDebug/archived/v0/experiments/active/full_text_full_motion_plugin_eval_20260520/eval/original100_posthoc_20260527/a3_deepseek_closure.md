---
title: "a3 DeepSeek 闭环摘要"
created: 2026-05-27T00:00:00+08:00
updated: 2026-05-27T00:00:00+08:00
type: consultation_log
tags:
  - MoDebug
  - DeepSeek
  - Original100
---

## 轮次 1

- 我给 DeepSeek 的输入：总体统计、bucket 分布、典型 partial/all-fail 样本、初始假设 A-D。
- DeepSeek 的主要挑刺：
  - 不能把“短文本/低复杂度”直接等同于“容易”，需要交叉看 `left/right x sequential x long_text`。
  - 要把 sample 侧难度和 model/path 侧缺陷拆开。
  - “MotionGPT 轨迹更强”“MoLingo 上肢更强”都还缺专门子集统计。
  - `GT 6/100` 噪声应单列，不要混进模型责任。
- 因此我补做了交互统计和歧义样本剔除检验。

## 轮次 2

- 我补充了交互项：
  - `left/right` 平均失败数 `1.204`；剔除 GT 歧义后仍是 `1.227`。
  - `left/right + sequential` 为 `1.636`；`+ long_text` 为 `1.737`；`+ hold/stop` 为 `1.727`。
  - `left/right + object` 只有 `0.842`，提示“侧别词”不是在任意上下文都同样困难。
- DeepSeek 收敛出的判断：
  - 可以稳写“侧别 grounding 是本诊断集里最突出的难点之一，并与多阶段/长文本有强交互”。
  - 模型个性应优先写“错误集中在哪”，不要过度升级成全局能力结论。
  - 指标应先保留最能区分模型、且短期可标注的量：LRGA 与阶段覆盖。

## 轮次 3

- 我继续补三类证据：
  - `left/right + upper_body`：MoLingo `7/37` 错，MotionGPT `9/37`，MoMask `13/37`，MoGenTS `14/37`；去掉 sequential 后 MoLingo `2/20` 错最低。
  - trajectory 关键词子集：MotionGPT `3/19`，MoLingo `4/19`，MoMask `6/19`，MoGenTS `7/19`；去掉 spin-only 后分别为 `2/16, 3/16, 4/16, 6/16`。
  - partial pattern 最大簇是 `1100`（MotionGPT+MoLingo 对，后两者错），共 `7` 个。
- DeepSeek 最终收敛结果：
  - 主指标最小集：`LRGA` + `SCS`。
  - 轨迹形状更适合做根轨迹叠加图，不宜直接升级成主指标。
  - 报告措辞要显式加上“在 Original100 诊断集中观察到”，避免把这里当 final evaluator。

## 最终采纳

- 采纳：
  - 用交互统计把“侧别 + 多阶段 + 长文本”写成 hardest corner，而不是泛泛说“复杂文本难”。
  - 用 `left/right + upper_body` 子集支持 MoLingo 的非对称上肢侧别相对稳定。
  - 用 trajectory 关键词子集支持“MotionGPT/MoLingo 在该子集相对稳于后两者”，但不升级成全局强结论。
  - 指标只保留 `LRGA` 与 `SCS` 为 P0，其他主要做可视化。
- 未采纳：
  - 不把“轨迹形状 fidelity”升级成第三个主指标。
  - 不把“物理失真”当主结论或主指标。
