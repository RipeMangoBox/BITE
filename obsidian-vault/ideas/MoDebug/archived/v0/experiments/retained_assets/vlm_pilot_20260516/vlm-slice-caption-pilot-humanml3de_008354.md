---
title: "VLM切片标注试验：HumanML3D-E 008354"
created: 2026-05-14T14:35:00+08:00
updated: 2026-05-16T17:37:56+08:00
status: pilot
tags:
  - MoDebug
  - HumanML3D_E
  - VLM_caption
  - event_timestamping
hypothesis: |
  短事件链中如果包含清晰的局部肢体动作，VLM 切片标注可以提供可读的 event 顺序证据；但轻微 locomotion 和左右脚身份仍依赖渲染视角。
source_papers:
  - "[[paperIDEAs/2026-05-12_fine-grained-text-motion-alignment-design|CPGA 时间戳设计]]"
---

# VLM切片标注试验：008354

## 一句话结论

`008354` 是一个中等偏正的样本：前进、轻踢、后退回起点三段顺序可以看出，最强证据是 `1.0s-1.5s` 左右的轻踢；前进和回起点是中等证据，因为 centered skeleton 会削弱全局位移。

## 实验设置

- 样本：HumanML3D-E-MP 测试样本 `008354`
- GT caption：`a figure walks forward and gives a sligh kick with thr left foot before stepping backward to the starting position`
- 文本侧 event：
  1. 向前走：`a figure walks forward.`
  2. 用左脚轻踢：`a figure gives a slight kick with thr left foot.`
  3. 后退回起始位置：`a figure steps backward to the starting position.`
- motion 长度：`83` frames，按 `20 FPS` 约 `4.15s`
- 输入形式：22-joint skeleton contact sheets，不是原生 RGB video
- 证据角色：`cross_check`

> [!warning] 证据边界
> 轻踢动作可见，但 `left foot` 与全局前进/后退方向不能只靠静态 centered sheet 下最终结论。

## 人工检查入口

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/008354/gt_motion.mp4]]

- Manifest：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/008354/manifest.json]]
- Caption JSON：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/008354/vlm_caption_results.json]]
- 渲染脚本：[[scripts/modebug_vlm_slice_caption_pilot.py]]

全序列：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/008354/full_sequence_progression.png]]

全局轨迹版：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/008354/full_sequence_progression_global_trajectory.png]]

`1.0s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/008354/slice_1p0s_triplets.png]]

`0.5s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/008354/slice_0p5s_triplets.png]]

`0.2s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/008354/slice_0p2s_triplets.png]]

## 子实验结论

| 子实验 | 结论 | 人工检查重点 |
|---|---|---|
| 全序列图 | 可以看出小幅前进、下肢轻踢、回到近似起点的三段顺序。 | 确认轻踢不是普通步态摆腿。 |
| 全局轨迹图 | 对前进和后退回位有帮助，但轨迹幅度不大。 | 检查起点和终点是否足够接近。 |
| `1.0s` 切片 | 粗略可读：`1.0s-2.0s` 是主踢腿窗口，`2.0s-3.0s` 是回退。 | 边界不细，适合做快速 sanity check。 |
| `0.5s` 切片 | 最清楚：`0.5s-1.0s` 前进准备，`1.0s-1.5s` 轻踢最明显，`1.5s-3.0s` 回退。 | 重点看 `1.0s-1.5s` 的脚是否有独立踢出。 |
| `0.2s` 切片 | 可细化轻踢窗口，但语义碎片化。 | 用于确认 `1.0s-1.6s` 的脚部 swing，而不是单独 caption。 |

## GT 对齐判断

| GT event | 支持强度 | 结论 |
|---|---|---|
| walks forward | 中 | 能看到小幅前进，但 centered sheet 会压低 locomotion 可见性。 |
| gives a slight kick with thr left foot | 中 | 下肢 swing 在 `1.0s-1.5s` 清楚，但左/右脚身份不够稳。 |
| steps backward to the starting position | 中 | 轨迹和最终姿态支持回到近似起点，但动作幅度较小。 |

## 人工复核清单

- [ ] 先在 GT MP4 中确认轻踢是否真实存在。
- [ ] 检查 `0.5s` 切片中 `1.0s-1.5s` 是否为轻踢而非正常迈步。
- [ ] 检查全局轨迹图是否显示先前进再回退。
- [ ] 标注左脚身份是否能可靠判断。

## 可用结论

1. 这个样本支持“短事件链 + 局部下肢动作”可以用 VLM 切片做交叉检查。
2. `0.5s` 粒度最适合人工检查轻踢和回退阶段。
3. 左右脚和小幅 locomotion 不能只依赖当前静态图，需要视频或更强的侧向/轨迹 cue。

## 证据记录

- date: `2026-05-14`
- artifact_path: `artifacts/modebug_vlm_slice_caption_pilot_20260513/008354/`
- evaluator: `GPT-5 visual inspection via Codex image view`
- protocol: `全序列 progression + 0.2s / 0.5s / 1.0s start/mid/end contact sheets, with light root/foot coordinate sanity check`
- motion_source: `HumanML3D-E-MP 测试样本 008354`
- condition_pair: `GT event decomposition vs VLM captions from rendered motion slices`
- n/evaluable: `1/1 sample; 3/3 text events`
- coverage: `single pilot sample`
- role: `cross_check`
- used_for: `observation`
- limitations: `静态 contact sheet, root 居中, 左右侧存在歧义, 未使用原生视频输入, 未做人工裁决, 未做 held-out 验证`
