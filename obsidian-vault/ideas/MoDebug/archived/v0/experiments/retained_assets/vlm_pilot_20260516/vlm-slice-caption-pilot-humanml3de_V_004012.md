---
title: "VLM切片标注试验：HumanML3D-E V_004012"
created: 2026-05-14T14:29:44+08:00
updated: 2026-05-16T17:37:56+08:00
status: pilot
tags:
  - MoDebug
  - HumanML3D_E
  - VLM_caption
  - event_timestamping
hypothesis: |
  对渲染后的 HumanML3D-E motion 做细粒度 VLM 切片标注，可以作为 motion-side event 边界的交叉检查；但结论强度取决于动作是否在静态骨架视图中可观察。
source_papers:
  - "[[paperIDEAs/2026-05-12_fine-grained-text-motion-alignment-design|CPGA 时间戳设计]]"
---

# VLM切片标注试验：V_004012

## 一句话结论

`V_004012` 是一个适合 VLM 切片标注的正例：单腿上抬、向外踢、收回这三段在静态骨架图中都可见。最可靠粒度是 `0.5s`；`0.2s` 适合细化边界但不适合单独生成语义 caption。结论只能作为 `cross_check`，不能作为正式 evaluator。

## 实验设置

- 样本：HumanML3D-E-MP 测试样本 `V_004012`
- GT caption：`the person raises their left foot up to their kinee and then kicks their foot out, then returns their foot to their knee`
- 文本侧 event：
  1. 抬起左脚到膝盖附近：`the person raises their left foot up to their knee.`
  2. 把脚向外踢出：`the person kicks their foot out.`
  3. 把脚收回到膝盖附近：`the person returns their foot to their knee.`
- motion 长度：`80` frames，按 `20 FPS` 约 `4.0s`
- 输入形式：22-joint skeleton 静态 contact sheet，不是原生 RGB video
- 证据角色：`cross_check`

> [!warning] 证据边界
> 这个试验只说明渲染图中能否看出动作片段，不证明 VLM 可以成为最终时间戳 evaluator。左脚/右脚和“回到膝盖”这种精细关系仍需要人工或更明确的视角校验。

## 人工检查入口

先看 GT MP4，再看全序列和 `0.5s` 切片；`0.2s` 只用于边界复核。

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/V_004012/gt_motion.mp4]]

- Manifest：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/V_004012/manifest.json]]
- Caption JSON：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/V_004012/vlm_caption_results.json]]
- 渲染脚本：[[scripts/modebug_vlm_slice_caption_pilot.py]]

全序列：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/V_004012/full_sequence_progression.png]]

全局轨迹版：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/V_004012/full_sequence_progression_global_trajectory.png]]

`1.0s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/V_004012/slice_1p0s_triplets.png]]

`0.5s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/V_004012/slice_0p5s_triplets.png]]

`0.2s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/V_004012/slice_0p2s_triplets.png]]

## 子实验结论

| 子实验 | 结论 | 人工检查重点 |
|---|---|---|
| 全序列图 | 能看出一条清晰的单腿轨迹：抬腿、伸出、收回。 | 检查是否真是同一条腿完成连续动作。 |
| 全局轨迹图 | 对这个样本帮助有限，因为主要动作是原地单腿动作，不是大位移 locomotion。 | 不要把轨迹弱当成动作弱。 |
| `1.0s` 切片 | 能恢复粗顺序，但边界太粗：第 2 秒附近抬腿，第 3 秒附近踢出，第 4 秒收回。 | 适合快速确认三段结构，不适合精确 onset。 |
| `0.5s` 切片 | 最适合人工检查：`1.0s-2.0s` 抬腿，`2.5s-3.5s` 踢出，`3.5s-4.0s` 收回。 | 重点看 `2.5s-3.5s` 的外踢是否足够清楚。 |
| `0.2s` 切片 | 能细化腿部轨迹，但单帧语义太碎。 | 只用于确认抬腿和踢出的大致边界，不单独当 caption 证据。 |

## GT 对齐判断

| GT event | 支持强度 | 结论 |
|---|---|---|
| raises left foot up to their knee | 强 | `1.0s-2.0s` 附近的屈膝抬腿很清楚。左脚身份仍依赖渲染视角。 |
| kicks foot out | 强 | `2.5s-3.5s` 看到抬起的脚向外伸出，是本样本最稳的事件。 |
| returns foot to their knee | 中 | 最后阶段能看到腿收回，但“回到膝盖”这个精细关系不如“收回到身体附近”稳定。 |

## 人工复核清单

- [ ] 先看 GT MP4，确认动作不是渲染图造成的错觉。
- [ ] 在 `0.5s` 切片里确认 `1.0s-2.0s` 是否为抬腿。
- [ ] 在 `0.5s` 切片里确认 `2.5s-3.5s` 是否为向外踢。
- [ ] 检查最后 `3.5s-4.0s` 是否是“回到膝盖”还是仅仅“收回腿”。
- [ ] 标注左/右脚是否能从当前视角可靠判断。

## 可用结论

1. 这个样本可以作为 VLM slice-caption 路线的 lower-body 正例。
2. `0.5s` 是最适合人工检查和 VLM prompt 的默认粒度。
3. `0.2s` 只作为 边界细化，不作为独立 event caption。
4. 下一步如果要做 event-level boundary，需要把已知 event 逐个问 VLM，而不是让 VLM 自由描述全序列。

## 证据记录

- date: `2026-05-14`
- artifact_path: `artifacts/modebug_vlm_slice_caption_pilot_20260513/V_004012/`
- evaluator: `GPT-5 visual inspection via Codex image view`
- protocol: `全序列 progression + 0.2s / 0.5s / 1.0s start/mid/end contact sheets`
- motion_source: `HumanML3D-E-MP 测试样本 V_004012`
- condition_pair: `GT event decomposition vs VLM captions from rendered motion slices`
- n/evaluable: `1/1 sample; 3/3 text events`
- coverage: `single pilot sample`
- role: `cross_check`
- used_for: `observation`
- limitations: `静态 contact sheet, root 居中, 左右侧依赖渲染视角, 未使用原生视频输入, 未做人工裁决, 未做 held-out 验证`
