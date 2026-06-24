---
title: "VLM切片标注试验：HumanML3D-E Q_009402"
created: 2026-05-13T23:55:00+08:00
updated: 2026-05-16T17:37:56+08:00
status: pilot
tags:
  - MoDebug
  - HumanML3D_E
  - VLM_caption
  - event_timestamping
hypothesis: |
  包含转身和回到起点的短 locomotion 样本，可以测试全局轨迹 overlay 是否能补强 VLM 对 motion-side event 边界的判断。
source_papers:
  - "[[paperIDEAs/2026-05-12_fine-grained-text-motion-alignment-design|CPGA 时间戳设计]]"
---

# VLM切片标注试验：Q_009402

## 一句话结论

`Q_009402` 是轨迹/转身合理性检查样本：转身最可靠，前走和继续走是中等证据，`stops where he started` 必须依赖 MP4/root trace，不能只看 root 居中的静态 sheet。`0.5s` 最适合人工检查完整事件链，`0.2s` 只用于定位转身窗口。

## 实验设置

- 样本：HumanML3D-E-MP 测试样本 `Q_009402`
- GT caption：`the rig walks forward then turns around and continues walking before stopping where he started`
- 文本侧 event：
  1. 向前走：`The rig walks forward.`
  2. 转身：`The rig turns around.`
  3. 继续走：`The rig continues walking.`
  4. 在起点附近停下：`The rig stops where he started.`
- motion 长度：`60` frames，按 `20 FPS` 约 `3.0s`
- 输入形式：22-joint skeleton contact sheets + GT MP4/root trace
- root 轨迹复核：end-start x/z 为 `[0.0202, -0.0161]`，range x/z 为 `[0.1264, 1.1585]`
- 证据角色：`cross_check`

> [!warning] 证据边界
> 这个样本能支持“转身 + 回到起点”的可观察性，但不能把静态图单独写成回到起点 evaluator。回到起点是轨迹 claim，必须保留 root trace/MP4 证据。

## 人工检查入口

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/Q_009402/gt_motion.mp4]]

- Manifest：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/Q_009402/manifest.json]]
- Caption JSON：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/Q_009402/vlm_caption_results.json]]
- 渲染脚本：[[scripts/modebug_vlm_slice_caption_pilot.py]]

全序列：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/Q_009402/full_sequence_progression.png]]

全局轨迹版：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/Q_009402/full_sequence_progression_global_trajectory.png]]

`1.0s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/Q_009402/slice_1p0s_triplets.png]]

`0.5s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/Q_009402/slice_0p5s_triplets.png]]

`0.2s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/Q_009402/slice_0p2s_triplets.png]]

## 子实验结论

| 子实验 | 结论 | 人工检查重点 |
|---|---|---|
| 全序列图 | 能看出走路、转身、最后站住的大体顺序。 | 不要只凭静态姿态判断“回到起点”。 |
| 全局轨迹图 | 对 `stops where he started` 是必要证据；root 大幅 excursion 后终点接近起点。 | 检查路径是否先离开再返回。 |
| `1.0s` 切片 | 粗粒度可读：`0.0s-1.0s` 走，`1.0s-2.0s` 转身并继续走，`2.0s-3.0s` 停。 | 事件压缩严重，不适合精细边界。 |
| `0.5s` 切片 | 最适合完整链检查：`0.0s-1.0s` 前走，`1.0s-1.5s` 转身，`1.5s-2.2s` 继续走，`2.2s-3.0s` 停。 | 重点确认 turn 是否在 `1.0s-1.5s`。 |
| `0.2s` 切片 | 转身局部化最好，主转身约 `1.0s-1.4s`。 | 只用于 turn onset/completion，不单独做走路 caption。 |

## GT 对齐判断

| GT event | 支持强度 | 结论 |
|---|---|---|
| walks forward | 中 | 早期腿部交替和姿态支持 walking，但绝对 forward 方向依赖 MP4/root trace。 |
| turns around | 强 | 转身是最可靠事件，`1.0s-1.5s` 最清楚。 |
| continues walking | 中 | 转身后仍有 stepping，但很快混入停止阶段。 |
| stops where he started | 中 | 停止可见，回到起点由 root trace 支持，不由 static sheet 单独支持。 |

## 人工复核清单

- [ ] 在 GT MP4 中确认 root 是否先远离再回到起点附近。
- [ ] 检查 `0.5s` 切片的 `1.0s-1.5s` 是否为 turn around。
- [ ] 检查转身后是否仍有至少一段 continuation walking。
- [ ] 把 `stops` 和 `where he started` 分开标注：前者是姿态/速度，后者是轨迹。

## 可用结论

1. 这是 trajectory-aware slice prompt 的 sanity 样本。
2. 对转身，静态切片已经有强证据。
3. 对回到起点，必须把 root trace 和 MP4 作为证据来源。
4. 下一步 prompt 应分开问 `turn onset`、`turn completion`、`stop`、`endpoint close to start`。

## 证据记录

- date: `2026-05-14`
- artifact_path: `artifacts/modebug_vlm_slice_caption_pilot_20260513/Q_009402/`
- evaluator: `Codex GPT-5 visual inspection via image view`
- protocol: `全序列 progression + 0.2s / 0.5s / 1.0s start/mid/end contact sheets + GT MP4/root trace 交叉检查`
- motion_source: `HumanML3D-E-MP 测试样本 Q_009402`
- condition_pair: `GT event decomposition vs VLM captions from rendered motion slices`
- n/evaluable: `1/1 sample; 4/4 text events`
- coverage: `single pilot sample`
- role: `cross_check`
- used_for: `observation`
- limitations: `静态 contact sheet, sheet 中 root 居中, 仅渲染骨架, 未做人工裁决, 未做 held-out 验证`
