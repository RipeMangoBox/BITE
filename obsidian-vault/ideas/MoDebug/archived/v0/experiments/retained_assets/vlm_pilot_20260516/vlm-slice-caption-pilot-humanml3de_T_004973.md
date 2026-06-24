---
title: "VLM切片标注试验：HumanML3D-E T_004973"
created: 2026-05-14T14:24:21+08:00
updated: 2026-05-16T17:37:56+08:00
status: pilot
tags:
  - MoDebug
  - HumanML3D_E
  - VLM_caption
  - event_timestamping
hypothesis: |
  对以姿态变化为主的 motion，静态 skeleton 切片可能足以给出 motion-side event 边界交叉检查；但身体朝向和前后方向语义仍可能不可靠。
source_papers:
  - "[[paperIDEAs/2026-05-12_fine-grained-text-motion-alignment-design|CPGA 时间戳设计]]"
---

# VLM切片标注试验：T_004973

## 一句话结论

`T_004973` 是姿态定义动作的正例：下蹲、双臂伸出、回到站立都能在静态骨架切片里看到。`0.5s` 粒度最适合人工检查；主要不确定性是“双臂向前伸”在当前视角下容易被看成“向外伸”。

## 实验设置

- 样本：HumanML3D-E-MP 测试样本 `T_004973`
- GT caption：`a person bends down at knees and brings both arms out extended in front of him and returns to standing position`
- 文本侧 event：
  1. 屈膝下蹲：`a person bends down at knees.`
  2. 双臂向前伸出：`a person brings both arms out extended in front of him.`
  3. 回到站立姿态：`a person returns to standing position.`
- motion 长度：`100` frames，按 `20 FPS` 约 `5.0s`
- 输入形式：22-joint skeleton contact sheets，不是原生 RGB video
- 证据角色：`cross_check`

> [!warning] 证据边界
> 下蹲和站起是强证据；“in front of him” 是视角语义，当前单视角静态图不能完全证明。

## 人工检查入口

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/T_004973/gt_motion.mp4]]

- Manifest：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/T_004973/manifest.json]]
- Caption JSON：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/T_004973/vlm_caption_results.json]]
- 渲染脚本：[[scripts/modebug_vlm_slice_caption_pilot.py]]

全序列：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/T_004973/full_sequence_progression.png]]

全局轨迹版：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/T_004973/full_sequence_progression_global_trajectory.png]]

`1.0s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/T_004973/slice_1p0s_triplets.png]]

`0.5s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/T_004973/slice_0p5s_triplets.png]]

`0.2s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/T_004973/slice_0p2s_triplets.png]]

## 子实验结论

| 子实验 | 结论 | 人工检查重点 |
|---|---|---|
| 全序列图 | 能看到从站立到下蹲再回到站立的完整变化。 | 确认动作不是单纯手臂变化，而是膝盖和身体高度一起变化。 |
| 全局轨迹图 | 位移很小，对这个样本不是关键证据。 | 不需要用轨迹判断 event，主要看姿态。 |
| `1.0s` 切片 | 能确认粗顺序，但把下蹲和双臂伸出合并在同一阶段。 | 适合确认大体结构，不适合拆分手臂和膝盖 onset。 |
| `0.5s` 切片 | 最清楚：`1.5s-2.0s` 开始下蹲，`2.0s-2.5s` 最深下蹲且双臂伸出，`2.5s-3.5s` 回站。 | 重点看 `2.0s-2.5s` 是否同时满足膝盖下蹲和双臂伸出。 |
| `0.2s` 切片 | 能细化 onset/offset，但语义过碎。 | 用来确认 `1.4s-2.0s` 下蹲开始和 `2.8s-3.6s` 站起结束。 |

## GT 对齐判断

| GT event | 支持强度 | 结论 |
|---|---|---|
| bends down at knees | 强 | 骨架高度和膝盖弯曲在 `1.5s-2.8s` 明显可见。 |
| brings both arms out extended in front of him | 中 | 双臂伸出可见，但“向前”与“向外”在当前视角下不完全可分。 |
| returns to standing position | 强 | `2.8s-3.6s` 身体回到站立，后半段保持稳定站姿。 |

## 人工复核清单

- [ ] 在 GT MP4 中确认 `2.0s-2.5s` 是否为最深下蹲。
- [ ] 检查双臂是否确实向身体前方伸出，而不是侧向展开。
- [ ] 检查下蹲和双臂伸出是否同步发生，还是存在明显先后。
- [ ] 检查 `3.0s-3.5s` 是否已经回到站立。

## 可用结论

1. 这个样本适合测试姿态型 event boundary。
2. 对下蹲和回站，VLM 静态切片有较强可观察性。
3. 对前后方向语义，需要侧视角、斜视角或 body-facing indicator。
4. 后续 prompt 应把“膝盖弯曲”和“双臂伸出方向”拆开问，避免一个 caption 混合两个证据角色。

## 证据记录

- date: `2026-05-14`
- artifact_path: `artifacts/modebug_vlm_slice_caption_pilot_20260513/T_004973/`
- evaluator: `GPT-5.5 visual inspection via Codex image view`
- protocol: `全序列 progression + 0.2s / 0.5s / 1.0s start/mid/end contact sheets`
- motion_source: `HumanML3D-E-MP 测试样本 T_004973`
- condition_pair: `GT event decomposition vs VLM captions from rendered motion slices`
- n/evaluable: `1/1 sample; 3/3 text events`
- coverage: `single pilot sample`
- role: `cross_check`
- used_for: `observation`
- limitations: `静态 contact sheet, 手臂前向/侧向存在视角歧义, 未使用原生视频输入, 未做人工裁决, 未做 held-out 验证`
