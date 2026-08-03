---
title: "StoryMotion v11 Actor–Director Counterfactual Control"
hypothesis: |
  StoryMotion的可用性主张应从模糊的三模式统一，收缩为Actor–Director不对称因子化：
  Actor文本生成Human，Director文本在读取final Human后生成human-centric Camera；
  在共享噪声的单轴反事实下，输出应跟随被替换的文本，同时守住未替换轴的合同。
status: closed_screen_failed
tags:
  - StoryMotion
  - DIRECT
  - paper/B
  - control
  - counterfactual
  - ICLR
  - ICLR/2027
  - status/closed
source_notes:
  - "[[DIRECT/current]]"
  - "[[StoryMotion-iclr-reliability]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[2026-07-29_storymotion-v11-v9-owner-stage2-three-mode-rescue-contract]]"
source_papers:
  - "[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation]]"
  - "[[analysis/SIGGRAPH_ASIA_2025/Uni3C_Unifying_Precisely_3D-Enhanced_Camera_and_Human_Motion_Controls_for_Video_Generation]]"
created: 2026-07-31T18:59:00+08:00
updated: 2026-08-03T14:30:39+08:00
---

# StoryMotion v11 Actor–Director Counterfactual Control

> [!important] 因果问题
> 当前证据证明了Direct-H、Direct-C与sequential Human→Camera能运行，但没有证明
> 两条语言轴在同一系统内可独立操纵。本文只回答：在共享采样噪声时，替换Actor或
> Director指令是否引发方向正确的语义响应，并满足不应改变的合同。

正式主线数字与artifact hashes仍只归属
[[StoryMotion-valid-metric-ledger]]。本页拥有反事实控制轴的预声明、screen gate与
screen决策；screen通过后才允许预注册pure4,053 formal评估。

## 1. 任务语义

- **Actor generation**：Human文本 → Human motion。
- **Director planning**：final／observed Human与Camera文本 → human-centric Camera
  trajectory。
- **Joint generation**：先执行Actor，再执行Director；不是第三个对称生成器，也不
  重新引入evolving-H joint parallel。

该表述把系统定位为可复用的3D previsualization／control-plan generator。Uni3C与
ActCam的强项是把已给定的Human／Camera控制送入Video Generation；Auteur已覆盖
语言驱动的人体相对Camera planning。因此StoryMotion不能声称ViGen没有Human–Camera
控制，只能检验更窄的差异：独立双文本、连续dense 3D plan、Camera对final Human的
反应，以及可复用／可编辑的显式轨迹。

## 2. 预声明设计

共同边界：v11 C0-LAT与C0-GEO `105K` co-mainline、exact v9 Pulp-only non-causal
Stage1 owner、frozen v9 Human `105K` teacher、Euler-50、CFG=1、seed17。所有
constructor、checkpoint、cache与decoder继续 fail closed 于 `is_causal == false`。

### 2.1 Director edit

对每个target选择一个**真实帧长完全相同**、Human文本与Camera文本均不同的donor：

1. 固定target的cached teacher-final Human；
2. 固定同一个Camera初始噪声；
3. 只把Camera文本从target替换为donor；
4. 比较原输出对target／donor文本的CLaTr相似度，以及编辑输出对donor／target文本的
   CLaTr相似度；
5. 验证decoded Human199与Human joints逐位不变，并测Camera center／rotation响应。

### 2.2 Actor edit

1. 固定同一个Human初始噪声；
2. 只把Human文本从target替换为同长度donor；
3. 两条Human结果分别进入Camera planner；Camera文本与Camera初始噪声保持相同；
4. 用TMR双向对比检验Human是否跟随被替换的Actor文本；
5. 用CLaTr与projected-Human outscreen检验同一Director文本是否保持，同时允许Camera
   trajectory因Human变化而自适应。

两条轴都报告逐sample分数与target-level bootstrap。主要语义量为：

`0.5 × [(original, own) - (original, donor) + (edited, donor) - (edited, original)]`

这个双向contrast排除了“两个文本本来就一难一易”对单向差值的混淆。

## 3. N128 screen gate

screen是诊断，不是formal evidence。C0-LAT与C0-GEO使用同一ordered target／donor
pair、同一噪声公式和同一evaluator。

| gate | 预声明条件 |
| --- | --- |
| Director未编辑轴 | decoded Human199与Human joints `max_abs == 0` |
| Director输出响应 | Camera center或rotation平均变化大于`1e-6` |
| Director语义响应 | factorial CLaTr contrast的bootstrap 95%下界大于`0` |
| Actor输出响应 | decoded Human joint平均变化大于`1e-6` |
| Actor语义响应 | factorial TMR contrast的bootstrap 95%下界大于`0` |
| Camera自适应 | Actor edit后Camera center或rotation平均变化大于`1e-6` |
| Director指令保持 | Actor edit前后固定Camera文本CLaTr差的95%下界大于`-5`分 |
| 可见性保持 | Actor edit前后outscreen差的95%上界小于`+0.10` |

只有两臂均关闭语义与合同gate，才进入pure4,053 formal与paper-facing fixed-8 Demo。
单臂通过只能说明该endpoint具备screen-level control，不得改写co-mainline身份。
若两臂失败，不通过提高MAE预算补救；失败定位到Stage2文本依赖、Pulp caption信号
或Camera planner。失败后允许固定样本的diagnostic viewer检查尾部，但不得包装成
能力Demo。

## 4. 决策记录

| version / run | boundary | status | decision |
| --- | --- | --- | --- |
| v11 C0-LAT / `v11_c0_lat_actor_director_control_n128_seed17_5090g2_r2_20260731` | exact-length paired N128 | screen failed one gate | retain diagnostic；do not escalate to formal |
| v11 C0-GEO / `v11_c0_geo_actor_director_control_n128_seed17_5090g3_r2_20260731` | exact-length paired N128 | screen failed one gate | retain diagnostic；do not escalate to formal |

> [!failure] Screen裁决：控制响应成立，级联鲁棒性未闭合
> 两臂均通过Director／Actor semantic response、Director edit下Human逐位精确、Camera
> response／adaptation与visibility gate；两臂均只失败Actor edit后的固定Camera文本
> 非劣gate。因此不运行pure4,053、不把完整独立双文本控制写入paper claim，也不以
> 扩样本或放宽margin事后救gate。

关键screen结果如下；数值是target-level `N=128` bootstrap 95%区间：

- C0-LAT：Director factorial CLaTr `37.103 [32.334, 41.789]`；Actor factorial TMR
  `16.578 [14.084, 19.130]`；固定Camera文本CLaTr差
  `-3.804 [-8.417, 0.925]`；outscreen差`0.009 [-0.031, 0.049]`。
- C0-GEO：Director factorial CLaTr `37.510 [32.640, 42.570]`；Actor factorial TMR
  `16.578 [14.084, 19.130]`；固定Camera文本CLaTr差
  `-3.285 [-7.638, 0.979]`；outscreen差`0.021 [-0.015, 0.058]`。
- 两臂Director edit的decoded Human199／joints `max_abs=0.0`。Actor edit使Human
  joints平均变化`0.594 m`；Camera center／rotation平均响应分别为LAT
  `2.100 m / 57.085°`、GEO `2.034 m / 54.303°`。

平均值掩盖了明显尾部。post-hoc failure taxonomy显示，固定Camera文本CLaTr下降超过
`5`分的样本占LAT `39.84%`、GEO `39.06%`；下降超过`20`分的样本占LAT
`24.22%`、GEO `18.75%`。该下降与Human joint变化量、Camera center变化量或rotation
变化量的线性相关均很弱；当前证据更符合**unseen counterfactual Human context下的
Camera instruction robustness不足**，而不是简单的编辑幅度阈值。

可审计源保留在两条远端run的`control_contract.json`、`screen_n128/results.json`与
`records.jsonl`。LAT／GEO `results.json` SHA-256分别为
`11976d37b3157811cdf949d595ef978d55c2454648fdfde06f786585b9708072`与
`11e46f80b6420f5890b0f31617b0737d3a13b469d8a22e9edf74554718ae4fa7`。

canonical layout位于`runs/train|eval|vis/stage2/<same-run-id>`。train root的
`experiment_contract.json`与原screen control contract逐字节相同；LAT／GEO合同
SHA-256分别为
`306fad1becd59bb15960d6a83119674d4e3edf8302fb74bf6a3150a8817c18d8`与
`914fe9794d0265e0df8bc91ef105e1b7ec070ccec24ab0aba8c1a5355a8ea374`，train
manifest均冻结为`screen_failed`。

为避免均值隐藏失败尾部，另以ordered first-8而非best-8生成四栏diagnostic viewer：
Director原／编辑与Actor原／编辑并排，LAT／GEO使用相同sample IDs。视觉manifest
分别位于对应`runs/vis/stage2/<run>/fixed8_r2/visual_manifest.json`；viewer只承担
screen解释，不改变失败裁决。LAT／GEO visual manifest SHA-256分别为
`11538b72f4b4fdc912cc6edca74f405ceaea9ea22f032c1975ac65f7e42edb62`与
`e327963de5d1694b0704d82e0ce72a8f2a96f4c952701f320b1fe6b6bf7055ec`。

## 5. 后续边界

- screen通过：冻结evaluator与pair rule，另建pure4,053 contract；随后才制作
  paper-facing Actor／Director control Demo。
- 本次screen失败：不把“独立双文本控制”写入论文主claim；先检查caption可辨识度与
  conditioner依赖，再决定补数据／先验或重做dense human-relative Camera planner。
- 本轴不训练MAE，不声称提高C0生成上限，也不承担Stage1简化结论。
