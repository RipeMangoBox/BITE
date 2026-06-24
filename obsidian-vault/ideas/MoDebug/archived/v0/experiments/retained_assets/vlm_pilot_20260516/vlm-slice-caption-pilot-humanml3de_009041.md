---
title: "VLM切片标注试验：HumanML3D-E 009041"
created: 2026-05-13T23:55:00+08:00
updated: 2026-05-16T17:37:56+08:00
status: pilot
tags:
  - MoDebug
  - HumanML3D_E
  - VLM_caption
  - event_timestamping
hypothesis: |
  VLM 切片标注能否同时处理 locomotion、上肢动作和下肢回踢，需要区分“动作确实不可见”和“渲染格式削弱了证据”。
source_papers:
  - "[[paperIDEAs/2026-05-12_fine-grained-text-motion-alignment-design|CPGA 时间戳设计]]"
---

# VLM切片标注试验：009041

## 一句话结论

`009041` 是一个失败边界样本：右手投掷动作很清楚，但前走和右腿后踢都弱。这个样本说明当前静态 centered skeleton 更擅长显著上肢动作，不擅长弱 locomotion 和小幅后踢。它应该作为 renderer/prompt 风险样本，而不是 VLM 路线的正例。

## 实验设置

- 样本：HumanML3D-E-MP 测试样本 `009041`
- GT caption：`a person walks forward from a neutral position and throws an object with right hand and right leg kicks back`
- 文本侧 event：
  1. 从中立姿态向前走：`a person walks forward from a neutral position.`
  2. 用右手投掷物体：`a person throws an object with right hand.`
  3. 右腿向后踢：`a person kicks back with right leg.`
- motion 长度：`108` frames，按 `20 FPS` 约 `5.4s`
- 输入形式：22-joint skeleton contact sheets，不是原生 RGB video
- 证据角色：`cross_check`

> [!warning] 证据边界
> 本样本不能证明 VLM timestamping 失败；它更直接暴露的是当前视觉输入格式不足。投掷可见，前走和后踢证据弱。

## 人工检查入口

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/009041/gt_motion.mp4]]

- Manifest：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/009041/manifest.json]]
- Caption JSON：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/009041/vlm_caption_results.json]]
- 渲染脚本：[[scripts/modebug_vlm_slice_caption_pilot.py]]

全序列：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/009041/full_sequence_progression.png]]

全局轨迹版：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/009041/full_sequence_progression_global_trajectory.png]]

`1.0s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/009041/slice_1p0s_triplets.png]]

`0.5s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/009041/slice_0p5s_triplets.png]]

`0.2s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/009041/slice_0p2s_triplets.png]]

## 子实验结论

| 子实验 | 结论 | 人工检查重点 |
|---|---|---|
| 全序列图 | 右手投掷动作可见；前走和右腿后踢不稳。 | 不要把“看到手臂投掷”误扩展成三个 event 都可见。 |
| 全局轨迹图 | 对前走有一定帮助，但位移证据仍不强。 | 检查是否有明确 root forward movement。 |
| `1.0s` 切片 | `1.0s-2.0s` 投掷最明显；其余阶段多为恢复和轻微腿部变化。 | 只能给投掷粗边界。 |
| `0.5s` 切片 | 能把投掷准备和投掷峰值分开，但仍不能稳定确认后踢。 | 看 `0.5s-2.0s` 的手臂轨迹；谨慎处理腿部 event。 |
| `0.2s` 切片 | 能细看手臂动作和恢复，但语义过碎。 | 用于确认投掷窗口，不用于判断右腿后踢。 |

## GT 对齐判断

| GT event | 支持强度 | 结论 |
|---|---|---|
| walks forward from a neutral position | 弱 | 有轻微位移和重心变化，但 centered static view 难以证明 forward walking。 |
| throws an object with right hand | 强 | `0.8s-2.0s` 右臂抬起、摆动、释放式轨迹清楚。 |
| kicks back with right leg | 弱 | 腿部变化存在，但不足以和普通恢复或重心转移区分。 |

## 人工复核清单

- [ ] 在 GT MP4 中确认是否真的存在明显前走。
- [ ] 在 `0.5s` 切片中确认投掷窗口是否为 `0.5s-2.0s`。
- [ ] 单独检查右腿后踢是否可见；如果不确定，应标为 ambiguous。
- [ ] 记录当前渲染图是否遮蔽了前后方向和腿部后踢。

## 可用结论

1. 这个样本是 VLM slice-caption 的负面/风险样本。
2. 上肢大幅动作可以被当前切片捕捉，弱 locomotion 和腿部后踢不稳定。
3. 下一轮 renderer 必须加入 root trajectory、body-facing cue 和短 MP4 event window。
4. 不能把这个样本用于支持“VLM 能完整 timestamp 三个 event”的结论。

## 证据记录

- date: `2026-05-13`
- artifact_path: `artifacts/modebug_vlm_slice_caption_pilot_20260513/009041/`
- evaluator: `GPT-5.5 visual inspection via Codex image view`
- protocol: `全序列 progression + 0.2s / 0.5s / 1.0s start/mid/end contact sheets`
- motion_source: `HumanML3D-E-MP 测试样本 009041`
- condition_pair: `GT event decomposition vs VLM captions from rendered motion slices`
- n/evaluable: `1/1 sample; 3/3 text events`
- coverage: `single pilot sample`
- role: `cross_check`
- used_for: `observation`
- limitations: `静态 contact sheet, root 居中, 未使用原生视频输入, 未做人工裁决, 未做 held-out 验证`
