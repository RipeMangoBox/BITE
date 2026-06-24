---
title: "VLM切片标注试验：HumanML3D-E 011798 轨迹 sanity"
created: 2026-05-14T15:32:00+08:00
updated: 2026-05-16T17:37:56+08:00
status: pilot
tags:
  - MoDebug
  - HumanML3D_E
  - VLM_caption
  - trajectory_rendering
hypothesis: |
  长程往返 locomotion 样本可以测试全局 root trajectory overlay 和 PoseFix 几何侧证据是否能共同提高 motion-side event 边界可读性。
source_papers:
  - "[[paperIDEAs/2026-05-12_fine-grained-text-motion-alignment-design|CPGA 时间戳设计]]"
---

# VLM切片标注试验：011798 轨迹 sanity

## 一句话结论

`011798` 是当前最强的轨迹感知合理性检查样本。全局 root path 明确显示远离、折返、接近起点；`0.5s` 切片能给出可检查的出发、外行、转向、返回、停止窗口；PoseFix 对身体转向和局部几何有帮助，但不能判断精确步数、jog 速度意图或相对身体朝向的前进/后退。结论只能作为 `cross_check / diagnostic`。

## 实验设置

- 样本：HumanML3D-E-MP 测试样本 `011798`
- MoDebug battery 别名：`m0gt_long_horizon_001`
- GT caption：`a person who is standing with his hands by his sides, turns and steps backwards, jogs forward six steps, turns 180 degrees and jogs four steps, then stops and resumes his original position.`
- 文本侧 event：
  1. 转身并后退：`a person who is standing with his hands by his sides, turns and steps backwards.`
  2. 向前 jog 六步：`a person who is standing with his hands by his sides, jogs forward six steps.`
  3. 转身 180 度并 jog 四步：`a person who is standing with his hands by his sides, turns 180 degrees and jogs four steps.`
  4. 停下并回到原始位置：`a person who is standing with his hands by his sides, stops and resumes his original position.`
- motion 长度：`151` frames，按 `20 FPS` 约 `7.55s`
- root trajectory：`span_x=2.843`，`span_z=0.471`，`path=6.127`，`net=0.131`
- 输入形式：VLM 静态切片 + root trajectory overlay + PoseFix static pose-pair snippet adapter
- 证据角色：`cross_check`

> [!warning] 证据边界
> 轨迹图能支持“远离和返回”；PoseFix 能支持“身体转向和局部姿态变化”；二者都不能单独证明 `six steps`、`four steps`、`jog` 或相对身体朝向的 `forward/backward`。

## 人工检查入口

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/011798/gt_motion.mp4]]

- Manifest：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/011798/manifest.json]]
- Caption JSON：[[artifacts/modebug_vlm_slice_caption_pilot_20260513/011798/vlm_caption_results.json]]
- 渲染脚本：[[scripts/modebug_vlm_slice_caption_pilot.py]]
- PoseFix snippet JSON：[[artifacts/modebug_posefix_snippet_caption_20260514/011798/posefix_snippet_results.json]]
- PoseFix integrated snippet JSON：[[artifacts/modebug_posefix_snippet_caption_20260514/011798/gpt_integrated_snippet_caption.json]]
- PoseFix adapter 脚本：[[scripts/modebug_posefix_snippet_caption.py]]
- PoseFix integration 脚本：[[scripts/modebug_integrate_posefix_snippet_caption.py]]

全序列：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/011798/full_sequence_progression.png]]

全局轨迹版：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/011798/full_sequence_progression_global_trajectory.png]]

`1.0s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/011798/slice_1p0s_triplets.png]]

`0.5s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/011798/slice_0p5s_triplets.png]]

`0.2s` 切片：

![[artifacts/modebug_vlm_slice_caption_pilot_20260513/011798/slice_0p2s_triplets.png]]

## 子实验结论

| 子实验 | 结论 | 人工检查重点 |
|---|---|---|
| 全序列图 | 能看出长程往返结构，但没有轨迹时方向和回到起点不够直观。 | 先看整体 pose progression，再看轨迹版确认路径。 |
| 全局轨迹图 | 这是本样本最关键证据：root path 长、net displacement 小，支持回到起点。 | 检查是否有远离、折返、返回近起点三段。 |
| `1.0s` 切片 | 能给出粗窗口：出发、外行、转向、返回、停止，但边界偏粗。 | 适合快速 human sanity check。 |
| `0.5s` 切片 | 最适合人工边界检查：`0.0s-1.0s` start/prep，`1.0s-2.0s` departure，`2.0s-4.0s` outbound，`4.0s-5.0s` reversal，`5.0s-7.0s` return，`7.0s-7.55s` stop。 | 重点检查 `4.0s-5.0s` 是否为折返窗口。 |
| `0.2s` 切片 | 能细化窗口，但不适合自由 caption。 | 只用于 refine 出发、折返、停止边界。 |
| PoseFix `1.0s` | 支持身体转向、膝/脚/手肘变化，与轨迹粗窗口一致。 | 不要用 PoseFix 判断 step count 或 jog。 |
| PoseFix `0.5s` | 强化边界：出发、外行、折返、返回、停止都能用 root delta + yaw 复核。 | 看 yaw 和 root delta 是否支持折返。 |

## PoseFix 几何侧补充

PoseFix pass 用静态 pose-pair 比较替代自由 VLM snippet caption，并结合 root trajectory。它的作用是几何侧交叉检查，不是动态 motion caption。

- 代码：[[linkedCodebases/posescript-posefix]]，本地路径 `/data/Life Me/Coding/Github/Motion/posescript-posefix`，branch `posefix`，commit `f5282b1`
- 环境：local `motionfix` conda env，额外加入 `tabulate` 和 `nltk`
- adapter：每个 snippet 取首帧/尾帧 22-joint pose，root-centered 后送入 PoseFix；root translation 和 torso-lateral yaw 另外记录
- 范围：只做 `1.0s` 和 `0.5s`；`0.2s` 太碎，不作为主 PoseFix caption 粒度

| PoseFix 粒度 | 可用结论 | 不可用结论 |
|---|---|---|
| `1.0s` | 支持初始转身、外行、折返、返回、最终放慢。 | 不能判断六步、四步、jog 速度意图。 |
| `0.5s` | 支持更清楚的 boundary：出发 `1.0s-2.0s`，外行 `2.0s-4.0s`，折返 `4.0s-5.0s`，返回 `5.0s-7.0s`，停止 `7.0s-7.55s`。 | 不能替代视频或 foot contact 计步。 |

## GT 对齐判断

| GT event | 支持强度 | 结论 |
|---|---|---|
| turns and steps backwards | 中 | 起始转向和离开起点可见；backwards 依赖身体朝向，当前证据不足以单独确认。 |
| jogs forward six steps | locomotion 强，count 中/弱 | 外行 locomotion 很清楚，但 `six steps` 不能由当前静态图稳定计数。 |
| turns 180 degrees and jogs four steps | 中到强 | 折返和返回 phase 清楚；`180 degrees` 和 `four steps` 需要视频、facing indicator 或 foot contact。 |
| stops and resumes original position | 强 | root trajectory 支持终点接近起点，最后站立/停止也可见。 |

## 与其他样本的定位

| 样本 | 主要价值 | 限制 |
|---|---|---|
| `V_004012` | 原地单腿动作正例 | 几乎不测轨迹 |
| `T_004973` | 姿态型下蹲/站起正例 | 不测大位移 |
| `008354` | 轻踢 + 小幅前后移动 | 轨迹和左右脚中等 |
| `009041` | 投掷强，弱 locomotion/后踢失败样本 | 不适合证明完整 timestamp |
| `Q_009402` | 短转身 + 回起点 sanity | 轨迹短，事件压缩 |
| `011798` | 长程往返轨迹最强 sanity | step count 和 forward/backward 仍不稳 |

## 人工复核清单

- [ ] 先看 GT MP4，确认外行和返回是否真实存在。
- [ ] 在全局轨迹图中确认 `path` 长且 `net` 小，支持 回到起点。
- [ ] 在 `0.5s` 切片中确认 `4.0s-5.0s` 是否为折返。
- [ ] 检查 `7.0s-7.55s` 是否已经停止且接近起点。
- [ ] 不要把 `six steps`、`four steps` 写成已验证，除非另有 foot contact 或人工计步记录。
- [ ] 检查 forward/backward 是否有 body-facing cue；如果没有，标为 ambiguous。

## 可用结论

1. `011798` 应作为下一轮 VLM/PoseFix trajectory-aware prompt 的主样本。
2. 全局轨迹 overlay 明显提高 回到起点 和 outbound/return phase 的可读性。
3. PoseFix 可以替代一部分局部几何 caption，但必须和 trajectory 或 video 结合使用。
4. 这个样本仍不能支持精确 step count evaluator，也不能单独解决 facing-relative forward/backward。

## 证据记录

- date: `2026-05-14`
- artifact_path: `artifacts/modebug_vlm_slice_caption_pilot_20260513/011798/`
- evaluator: `GPT-5.5 visual inspection via Codex image view`
- protocol: `render same pilot sheets plus global root trajectory overlay; caption from static visual evidence; PoseFix paircode snippets added as geometry 交叉检查`
- motion_source: `HumanML3D-E-MP 测试样本 011798`
- condition_pair: `original overlay vs global-trajectory overlay vs PoseFix static pose-pair snippet adapter`
- n/evaluable: `1/1`
- coverage: `one long-horizon locomotion sample`
- role: `cross_check`
- used_for: `observation`
- limitations: `仅静态 sheet 与 PoseFix 静态 pose-pair caption; 精确 step count 和相对身体朝向的 forward/backward 语义仍需要视频或显式朝向标注确认`
