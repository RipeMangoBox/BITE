---
title: "MoDebug MoLingo Evidence and Mechanism Adaptation Plan"
created: 2026-06-13T14:48:00+08:00
updated: 2026-06-13T16:11:58+08:00
status: active_plan
hypothesis: "MoDebug 不能停留在 MoLingo 单点诊断，也不能 overclaim 成通用 CFG 修复；当前应以 MoLingo 为显微镜，系统发现 motion generator 在 layer、diffusion step、token、body part 上的引导分工，再将跨域 CFG、flow、attention、part guidance 机制适配为可迁移的 motion guidance 方法。"
tags:
  - MoDebug
  - MoLingo
  - cfg_guidance
  - related_work
  - negative_result
  - mechanism_adaptation
  - controllable_generation
  - multi_baseline_plan
source_papers:
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation]]"
  - "[[analysis/ICLR_2025/CFG_Manifold_constrained_Classifier_Free_Guidance_for_Diffusion_Models]]"
  - "[[analysis/ICLR_2025/Eliminating_Oversaturation_and_Artifacts_of_High_Guidance_Scales_in_Diffusion_Models]]"
  - "[[analysis/CVPR_2025/TCFG_Tangential_Damping_Classifier_free_Guidance]]"
  - "[[analysis/CVPR_2026/C2FG_Control_Classifier_Free_Guidance_via_Score_Discrepancy_Analysis]]"
  - "[[analysis/CVPR_2026/CFG_Ctrl_Control_Based_Classifier_Free_Diffusion_Guidance]]"
  - "[[analysis/arxiv_2025/CFG_Zero_Improved_Classifier_Free_Guidance_for_Flow_Matching_Models]]"
  - "[[analysis/CVPR_2026/FlowMotion_Training_Free_Flow_Guidance_for_Video_Motion_Transfer]]"
  - "[[analysis/CVPR_2024/Rethinking_the_Spatial_Inconsistency_in_Classifier_Free_Diffusion_Guidance]]"
  - "[[analysis/arxiv_2024/Pay_Attention_and_Move_Better_Harnessing_Attention_for_Interactive_Motion_Generation_and_Training_free_Editing]]"
  - "[[analysis/CVPR_2026/TempoControl_Temporal_Attention_Guidance_for_Text_to_Video_Models]]"
  - "[[analysis/CVPR_2026/ParTY_Part_Guidance_for_Expressive_Text_to_Motion_Synthesis]]"
ds_sessions:
  - f755c0261a58
  - eda6a8a54cf6
---

# 2026-06-13 MoDebug MoLingo 证据与机制适配计划

> [!abstract] 当前结论
> 旧版 MoDebug 的动态 gate、旧 APG hook、norm clamp 等正机制路线仍然没有得到“机制明确且结果强力”的支撑，这一点不变。但相关工作的定位需要修正：跨域 CFG / flow / attention / part guidance 工作不应被简单写成 novelty 压缩源，而应被当作可迁移的机制库。MoDebug 的下一步不是补旧实验漏洞，而是以 MoLingo 为第一个显微镜，系统发现 generator 不同 layer、diffusion step、text token、body part 的关注点和分工，再把这些机制适配为 motion-specific controllable guidance。

---

## 1. 旧实验的最终价值

本节基于 [[2026-06-11_modebug-cfg-mechanism]]、4090 official evaluator 结果，以及 DS 严肃复核。实验产物主要来自：

```text
/data/Life Me/ResearchWY Vault/artifacts/remote4090_motion/modebug_4090_20260612_results_l15_pareto/queue_summary.jsonl
/data/Life Me/ResearchWY Vault/artifacts/remote4090_motion/modebug_4090_20260612_results_layer_sanity/queue_summary.jsonl
/data/Life Me/ResearchWY Vault/artifacts/remote4090_motion/modebug_4090_20260612_results_l13_continuity/queue_summary.jsonl
/data/Life Me/ResearchWY Vault/artifacts/remote4090_motion/modebug_4090_20260612_results_l11_l10_continuity/queue_summary.jsonl
/data/Life Me/ResearchWY Vault/artifacts/remote4090_motion/modebug_4090_20260613_gate_negative_replace_gpu0/queue_summary.jsonl
/data/Life Me/ResearchWY Vault/artifacts/remote4090_motion/modebug_4090_20260613_gate_negative_replace_gpu1/queue_summary.jsonl
```

### 1.1 可以保留的观察

| 观察                              |                                                                                数据锚点 | 当前解释边界                                               |
| ------------------------------- | ----------------------------------------------------------------------------------: | ---------------------------------------------------- |
| baseline constant               |                                       `FID 3.5944 / Top1 0.7755 / Matching 14.7401` | 原始 MoLingo official evaluator 对照。                    |
| L15 replace current 崩坏          |                                       `FID 7.7003 / Top1 0.7240 / Matching 15.7381` | 这是最清晰 target，但只能说明该 intervention harmful。            |
| L10 replace current 接近 baseline |                                       `FID 3.6466 / Top1 0.7676 / Matching 14.7573` | 支持 late-layer sensitivity，不支持所有层通用。                  |
| L11-L14 replace continuity      | L11 `3.6253/14.8100`，L12 `3.6739/14.8572`，L13 `3.7322/14.9009`，L14 `3.9497/15.1405` | L11-L13 mild degradation，L14 pre-collapse，L15 cliff。 |
| fixed-scale substitution a0.9   |                           3-seed mean `FID 3.3841 / Top1 0.7683 / Matching 14.8116` | 可写为 fixed-scale substitution 指标改善；不要写成已证明 repair。    |

DS 要求把 “fixed residual recovery” 改成更中性的 **fixed-scale substitution** 或 **fixed-scale intervention**。原因是 baseline 本身已经强，`FID 3.3841` 优于 `3.5944` 不等于证明模型有机制缺陷被修复；它只是说明一个固定缩放 intervention 在该 evaluator 上给出更好的指标点。

### 1.2 被负结果降级的路线

| 路线                               |                                                                                     数据锚点 | 结论                           |
| -------------------------------- | ---------------------------------------------------------------------------------------: | ---------------------------- |
| `discrepancy_gate` adaptive gate | 4-seed mean `FID 3.4661±0.0806 / Matching 14.7515±0.0161`；same-alpha a0.7/a0.9 均弱于 fixed | 可作为诊断器或历史候选，不能作为主机制。         |
| gate trace                       |                                        L15 gate mean `0.903-0.905`；L11-L14 `0.955-0.969` | 接近常数缩放，不支持强动态筛选。             |
| APG `o0.25/p1.0`                 |                                              3-seed mean `FID 4.8224 / Matching 15.3383` | 负控失败，不能包装为 projection 成功。    |
| norm clamp `r0.5`                |                                              3-seed mean `FID 5.1222 / Matching 15.4098` | 负控失败，说明简单压小 residual 不是充分机制。 |
| 继续 tau/slope 网格                  |                                                               gate trace 已接近 fixed alpha | 低优先级；继续调参只是在找另一个线性系数。        |

新增 10 个 2026-06-13 run 全部 `failures=[]` 且 `mixer_applied=6850`，因此负结论不是 hook 未生效导致。

### 1.3 这些实验的核心价值

这些实验不是没有价值。它们的价值在于收缩问题空间：

1. 找到了 MoLingo 上一个清楚的 harmful intervention target：L15 `CFG_CA` replacement。
2. 证明 L15 不是完全孤立异常层，而是 late-layer replacement sensitivity 的 endpoint：L14 pre-collapse，L15 cliff。
3. 反证了旧版复杂路线：cosine gate、APG、norm clamp 没有超过 fixed-scale substitution。
4. 给下一步机制探针提供了最小 target/control：baseline、L10 replace、L14 replace、L15 replace、L15 fixed-scale substitution。

当前不能把这些结果写成“MoDebug 方法有效”。更准确的写法是：

```text
MoDebug used MoLingo as the first microscope to expose a concrete failure observation:
L15 CFG_CA replacement is sharply harmful, while a fixed-scale substitution gives better official-evaluator metrics than both baseline and the tested adaptive interventions.
The causal mechanism remains unproven.
```

---

## 2. 相关工作：从“压力源”改为“机制库”

本次本地 KB 检索覆盖 `obsidian-vault/index/index.jsonl` 3268 条索引、`obsidian-vault/analysis/` 3305 篇 note。修正后的判断是：

1. 没有工作直接 cover “MoLingo L15 `CFG_CA` replacement cliff + fixed-scale substitution improvement” 这个完整现象。
2. CFG / flow / attention / part guidance 工作会约束 MoDebug 的 overclaim，但它们首先是机制启发源，不是简单的 novelty killer。
3. 把这些机制适配到 motion generator 的 layer、step、token、part 分工上，本身可以构成创新；关键是要证明这种适配不是 MoLingo 单点调参。

相关链接：[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation|MoLingo]]、[[analysis/ICLR_2025/CFG_Manifold_constrained_Classifier_Free_Guidance_for_Diffusion_Models|CFG++]]、[[analysis/ICLR_2025/Eliminating_Oversaturation_and_Artifacts_of_High_Guidance_Scales_in_Diffusion_Models|APG]]、[[analysis/CVPR_2025/TCFG_Tangential_Damping_Classifier_free_Guidance|TCFG]]、[[analysis/CVPR_2026/C2FG_Control_Classifier_Free_Guidance_via_Score_Discrepancy_Analysis|C2FG]]、[[analysis/CVPR_2026/CFG_Ctrl_Control_Based_Classifier_Free_Diffusion_Guidance|CFG-Ctrl]]、[[analysis/arxiv_2025/CFG_Zero_Improved_Classifier_Free_Guidance_for_Flow_Matching_Models|CFG-Zero*]]、[[analysis/CVPR_2026/FlowMotion_Training_Free_Flow_Guidance_for_Video_Motion_Transfer|FlowMotion]]。

| 机制来源       | 核心问题                                   | 与 MoDebug 的同构关系                                                  | 适配方向                                                                      |
| ---------- | -------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------- |
| CFG++      | CFG 外推导致 off-manifold，重噪声步骤累积偏移        | fixed-scale substitution 已经暗示 MoLingo 中存在“不过度外推”的更好点             | 在 motion latent 或 velocity prediction 空间做插值/锚定，而不是只在 hidden residual 上缩放。 |
| APG        | CFG 更新方向中 parallel 和 orthogonal 分量作用不同 | 旧 APG 失败不等于方向分解无效，可能是分解空间错了                                      | 在 velocity、denoised latent、layer residual 三个空间比较方向分量，而不是只复用旧 hidden hook。 |
| TCFG       | cond/uncond 法向分量对齐，切向分量不对齐             | L14/L15 cliff 可能来自 late layer 中无条件/条件方向的切向漂移                     | 用 layer-step SVD 或低秩谱分析定位不对齐方向，再做阻尼。                                      |
| C2FG       | score discrepancy 随 diffusion time 变化  | MoDebug 需要从“某层有问题”升级为“某层在某些 step 有问题”                            | 设计 layer-specific 和 step-specific guidance schedule。                      |
| CFG-Ctrl   | 高增益线性引导会振荡或发散                          | L15 replacement cliff 可以被看作语义误差信号失稳                              | 记录 `e(t)=cond-uncond` 与 `e_dot(t)`，只在出现振荡证据时上控制律。                         |
| CFG-Zero*  | Flow Matching 初始速度估计可能不可靠              | MoLingo 是 rectified flow，early step 或特定 layer 可能需要 zero/scale 校正 | 用优化无条件速度尺度和 early-step suppression 做轻量 flow-specific test。                |
| FlowMotion | 输出端 latent prediction 已编码粗到细 motion    | MoDebug 不能只盯内部 hook，需比较 output-side motion representation        | 用 `z0_hat` / predicted motion latent 做 probe 和正则，验证内部层发现是否反映到运动空间。        |

### 2.1 Motion-specific 机制接口

相关链接：[[analysis/CVPR_2024/Rethinking_the_Spatial_Inconsistency_in_Classifier_Free_Diffusion_Guidance|S-CFG]]、[[analysis/arxiv_2024/Pay_Attention_and_Move_Better_Harnessing_Attention_for_Interactive_Motion_Generation_and_Training_free_Editing|MotionCLR]]、[[analysis/CVPR_2026/TempoControl_Temporal_Attention_Guidance_for_Text_to_Video_Models|TempoControl]]、[[analysis/CVPR_2026/ParTY_Part_Guidance_for_Expressive_Text_to_Motion_Synthesis|ParTY]]、[[analysis/arxiv_2026/MaxSim_Fine_grained_Motion_Retrieval_via_Joint_Angle_Motion_Images_and_Token_Patch_Late_Interaction|MaxSim]]、[[analysis/arxiv_2026/Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval_via_Pyramidal_Shapley_Taylor_Learning|PST]]、[[analysis/arxiv_2026/MoCHA_Denoising_Caption_Supervision_for_Motion_Text_Retrieval|MoCHA]]。

| 机制来源                 | 核心思想                                           | MoDebug 适配问题                                                  |
| -------------------- | ---------------------------------------------- | ------------------------------------------------------------- |
| S-CFG                | 不同语义区域需要不同 guidance scale                      | motion 中对应 body part / time span / token phrase，不应全局统一 alpha。 |
| MotionCLR            | cross-attention 决定词级动作执行时间，自注意力捕捉帧间相似          | MoLingo 的 multi-token cross-attention 可作为 token-time 控制接口。    |
| TempoControl         | 通过注意力时间曲线控制概念出现时序                              | MoDebug 可从“改 FID”扩展到“提前/推迟/增强特定动作”的可控生成。                      |
| ParTY                | 部件语义对齐与全身连贯性需要两阶段或融合机制                         | MoDebug 的 part-level guidance 不能只提升局部，还必须保持 root/torso 连贯。    |
| MaxSim / PST / MoCHA | 细粒度 text-motion retrieval 与 token-part-time 对齐 | 全局 FID/Matching 不够，需要 token、joint、segment、time slice 指标。      |

---

## 3. 新方案定位

### 3.1 推荐定位

不要把 MoDebug 写成“已经解决 motion diffusion CFG 问题”的通用方法，也不要降成“只描述 MoLingo 的诊断笔记”。推荐定位是：

```text
Layer-, Step-, Token-, and Part-aware Guidance Modulation for Text-to-Motion Flow Models.
```

中文表述：

```text
MoDebug 以 MoLingo 为首个显微镜，系统刻画 text-to-motion generator 在不同层、不同扩散步、不同文本词元和不同身体部件上的条件引导分工，并把跨域 CFG / flow / attention / part guidance 机制适配为 motion-specific controllable guidance。
```

MoLingo 当前实验的角色是 **mechanism discovery baseline**：它提供 L14 pre-collapse、L15 cliff、fixed-scale substitution improvement 这些可靠入口，但最终贡献必须走向多 baseline 迁移和更细粒度可控生成。

更重要的是，图谱不是独立目标。MoDebug 后续应先定义要展示的控制能力，再收集为该能力服务的最小图谱。否则 layer-step-token-part atlas 很容易变成大而无用的可视化。

### 3.2 可以写

- 旧版 adaptive gate、旧 APG hook、norm clamp 没有形成强结果，后续不应继续围绕这些旧路线调参。
- MoLingo 上已有稳定 target：L11-L15 replacement continuity、L14 pre-collapse、L15 cliff、fixed-scale substitution 指标改善。
- 跨域 CFG / flow / attention / part guidance 工作提供机制模板；motion 适配创新点在 layer/step/token/part 的结合与验证。
- 当前第一阶段目标是围绕 T1 时间区间控制和 T2 身体部件控制构建最小必要图谱，并产出可量化 demo，而不是先做全量 atlas。
- MoLingo 之后必须迁移到至少一个不同 text-to-motion backbone，证明发现不是单模型特例。

### 3.3 不能写

- 不能写“fixed-scale substitution repair 了 MoLingo”。
- 不能写“旧 gate 证明 adaptive guidance 有效”。
- 不能把 APG/norm clamp 失败写成 APG、TCFG、CFG++ 这类通用方法无效。
- 不能只用全局 FID/Matching 支撑机制发现。
- 不能在没有第二个 baseline 前声称通用 motion guidance principle。

---

## 4. 目标驱动机制适配

### 4.1 先定义能力，再做图谱

当前最危险的规划错误是“先做全量 atlas，再想怎么用”。修订后的原则是：每个图谱都必须回答一个明确能力目标，否则不做。

| 能力目标      | 最小 demo 定义                                                          | 需要的图谱                                                              | 图谱如何转成干预                                                                      | 两周优先级 |
| --------- | ------------------------------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------- | ----- |
| T1 时间区间控制 | 给定 `walk`/`run` 或 `jump`/`squat`，指定前后半段动作切换，生成 motion 应在目标帧区间执行对应动作 | layer-step 到 frame-level semantic logit 的影响张量；重点看哪些层/步能选择性影响前半或后半  | 对高选择性的 layer-step 接口做 frame mask guidance：前半段用动作 A guidance，后半段用动作 B guidance | P0    |
| T2 身体部件控制 | 给定 `right hand waving`，右手明显执行 waving，非目标关节变化受控                      | layer-step 到 joint/part displacement 的影响张量；root/torso/arms/legs 分组 | 对目标 part 高敏感、非目标 part 低敏感的接口做 part-specific scaling 或 mask                    | P0    |
| T3 词汇级强调  | `run fast` 相比普通 `run` 提高速度或步频，主体动作不变                                | token-layer-step 对速度、幅度、高度等属性的敏感性图谱                                | 只在目标词和目标属性敏感接口上提高 token guidance                                              | P1    |
| T4 多条件组合  | text A 和 text B 在不同时间/部件上组合，而不是互相覆盖                                 | 两个 guidance 方向在 layer-step 上的夹角、norm ratio、冲突区间                    | 低冲突接口线性混合，高冲突接口分时或分部件调度                                                       | P1    |

两周内优先做 T1 和 T2。T3/T4 是自然扩展，不进入当前 P0。这样 atlas 的范围被目标约束：T1 只收集 frame-level 影响，T2 只收集 part/joint 影响，不做无目的的全量图谱。

### 4.2 继承式路线表

这张表替代“从零开始的方案池”。旧实验不能丢；它们是约束、负结果或强基线。

| 机制 / 实验 | 状态 | 可继承结果 | 下一步 |
|---|---|---|---|
| Baseline constant | Done | `FID 3.5944 / Top1 0.7755 / Matching 14.7401`，所有实验的绝对对照 | 保留；不再重复，除非最终补多 seed 统计。 |
| L15 direct replacement | Evaluated: 高风险接口 | `FID 7.7003 / Matching 15.7381`，说明 L15 直接替换是 harmful target；不是“L15 必须剔除” | 作为约束边界：后续不能直接 replace L15；若动 L15，必须间接、阻尼或有动态证据。 |
| L10 direct replacement | Partial control | `FID 3.6466 / Matching 14.7573`，L10 接近 baseline，提供 safe-layer control | 用作 lower-risk interface 对照，但不是主提升方案。 |
| L11-L14 replace continuity | Done | L11-L13 mild degradation，L14 pre-collapse，L15 cliff | 继承为 layer safety boundary；T1/T2 的 layer 选择优先避开 L15 direct replacement，并关注 L12-L14 过渡。 |
| L15 discrepancy gate 4 seeds | Partial: 历史弱正 | `FID 3.4661±0.0806 / Matching 14.7515`，说明 non-uniform gate 有恢复能力 | 不丢弃，但旧 cosine gate 不能作为主机制；若重启 gate，必须服务 T1/T2 的 frame/part 目标。 |
| fixed residual scaling | Done: 当前最强简单修复 | a0.9 3-seed mean `FID 3.3841 / Matching 14.8116` | 所有新方法必须和它比；它是 strong baseline，不是最终能力展示。 |
| same-alpha gated vs fixed | Done | discrepancy a0.7/a0.9 被 fixed 支配或接近支配 | 作为“旧 cosine gate 独立价值不足”的证据，停止 tau/slope 网格。 |
| gate trace | Done | L15 mean `0.903-0.905`，L11-L14 `0.955-0.969`，旧 gate 近似常数缩放 | 新 gate 必须报告实际动态范围和 frame/part 选择性。 |
| APG hidden hook | Deprecated in current space | 3-seed `FID 4.8224 / Matching 15.3383` | 不继续旧 hidden APG；若借 APG，只能在 velocity / denoised latent / control-target 空间重做。 |
| norm clamp | Deprecated | 3-seed `FID 5.1222 / Matching 15.4098` | 不继续范数压小路线。 |
| Layer-step schedule | Not Started | 旧 CFG scalar schedule / C2FG-like sweep 没有直接服务 L15 branch 或能力 demo | 只有当 T1/T2 atlas 显示某些 layer-step 可控时才启动。 |
| Token-time attention guidance | Not Started | MotionCLR / TempoControl 是机制来源，尚未接入 MoLingo | 作为 T1 的主要 demo 路线。 |
| Part-aware guidance | Not Started | ParTY / S-CFG 是机制来源，尚未接入 MoLingo | 作为 T2 的主要 demo 路线。 |
| Flow `z0_hat` probe / regularization | Not Started | FlowMotion 是机制来源，当前无 MoLingo 输出端 probe | P1：用于解释 T1/T2 干预是否反映到 motion latent。 |
| Feedback damping | Not Started / Conditional | CFG-Ctrl 是机制来源，但当前没有 `e_dot` 振荡证据 | 只有 atlas 证明 L15 或 late layer 出现振荡时才做。 |
| Multi-baseline transfer | Not Started | 当前所有强证据都在 MoLingo | T1/T2 demo 成立后，迁移最小 wrapper 到第二 baseline。 |

### 4.3 显式能力 demo

| Demo | 可执行定义 | 最小指标 | 通过条件 |
|---|---|---|---|
| D1 时间区间控制 | 选择 `walk -> run`、`jump -> squat` 等动作对，指定前半/后半帧区间；用 frame-level action classifier 或 retrieval proxy 评估每帧动作 | 错位帧比例、动作切换边界误差、FID/Matching | 错位帧比例明显低于 text-only / fixed residual；FID 不明显差于 fixed residual。 |
| D2 身体部件控制 | `right hand waving`、`left leg kick` 等 prompt；目标 part 应响应，非目标 part 尽量不被拖动 | target part score、non-target joint drift、root drift、global FID | 目标 part score 上升，非目标 drift 低于全局 guidance，对全身连贯无明显破坏。 |
| D3 词汇级强调 | `run fast` vs `run` / `walk slowly`，只改变属性词强度 | velocity、step frequency、motion amplitude、动作类别保持率 | 属性变化单调且主体动作类别不变。 |
| D4 layer/step slider | 录制 layer/step guidance slider 对同一 prompt 的连续变化 | 定性 + 单调性统计 | 变化连续可预测，不是随机突变。 |

两周内强制 D1 和 D2。D3 可作为 P1，D4 可作为内部调试和展示工具。

### 4.4 方案使用规则

1. 不以“优化 FID”作为唯一目标；每个方案必须绑定 D1-D4 中至少一个能力 demo。
2. 不做无目标图谱；T1 做 frame-level 影响图谱，T2 做 part-level 影响图谱。
3. 不丢旧结果；所有 Done/Partial/Deprecated 都要作为强基线、约束或负结果进入最终叙事。
4. 不继续旧 gate 网格；如果有新 gate，必须证明它的动态范围和 frame/part 选择性。
5. 不直接动 L15 replace；L15 是高风险接口，只允许在有明确 damping / indirect control 证据时介入。

---

## 5. 两周目标驱动路线

| 阶段 | 时间 | 实验 | 目标 |
|---|---|---|---|
| Phase 1 | Day 1 | 选择 T1 demo prompt：`walk->run`、`jump->squat`；确认 text-only / fixed residual 能生成基本可识别动作 | 确认 demo 不被数据或 evaluator 卡死。 |
| Phase 2 | Day 2-3 | T1 图谱：对候选 layer-step 做小扰动，记录 frame-level action/retrieval logit 变化 | 找到对前半/后半帧选择性最高的接口。 |
| Phase 3 | Day 4-5 | T1 干预：frame mask guidance / token-time attention guidance；对比 text-only、baseline、fixed residual | 形成第一个显式时间区间控制 demo。 |
| Phase 4 | Day 6-7 | T1 鲁棒性：多 seed、换动作对、软 mask 边界 | 判断时间控制是否稳定，不稳定则停在 T1 修机制。 |
| Phase 5 | Day 8-9 | T2 图谱：右手/左腿/root/torso 的 part-level sensitivity | 找到目标 part 高敏感、非目标 part 低敏感的 layer-step。 |
| Phase 6 | Day 10-11 | T2 干预：part-specific scaling / mask；对比全局 guidance 和 fixed residual | 形成身体部件选择性控制 demo。 |
| Phase 7 | Day 12 | MoLingo 最佳 demo 补 3 seeds + global evaluator + fine-grained slices | 确认 demo 不是单 seed 偶然。 |
| Phase 8 | Day 13-14 | 把 D1 或 D2 的最小 wrapper 迁移到一个非 MoLingo baseline | 判断是否能进入多 baseline 路线。 |

暂缓项：

1. 不补 tau/slope gate 网格。
2. 不继续 norm clamp 或旧 hidden APG。
3. 不先跑全量 layer-step-token-part atlas。
4. 不把 fixed alpha 继续刷成主线。
5. 不先做 feedback damping，除非 T1/T2 图谱显示明确振荡或 late-layer instability。

---

## 6. ICLR 路线门槛

从 ICLR reviewer 角度，MoDebug 至少需要以下结果组合，才有机会从 MoLingo 单 baseline 走向可投路线：

1. **目标驱动图谱**：T1 的 frame-level 影响图谱能指导时间区间控制，T2 的 part-level 影响图谱能指导身体部件控制；图谱不能只是解释性可视化。
2. **显式可控性**：至少展示一个时间区间控制任务和一个身体部件控制任务，例如前半段 walk 后半段 run，或 right hand waving 且非目标关节 drift 受控。
3. **显著效果**：MoLingo official evaluator 上相对 baseline 或 fixed residual strong baseline 不出现明显质量 tradeoff；若 claim quality improvement，则 FID 至少有 8-10% 相对改善且 3 seeds 稳定。
4. **组件消融**：schedule、方向分解、token-time 或 part 组件各自移除会回退，不是单一 alpha 调参。
5. **跨模型迁移**：至少一个非 MoLingo text-to-motion backbone 同向提升；如果不能提升，也要解释清楚 MoLingo 特有条件并降级为 case study。
6. **鲁棒子集**：短 prompt、长 prompt、多动作 prompt、部件冲突 prompt 分开报告，不能只在挑选 subset 上有效。

如果最后只有 MoLingo 单模型、全局 FID 小幅提升、无机制图谱、无可控性，路线仍然达不到 ICLR 标准。

---

## 7. 推荐阅读更新

推荐阅读文件已更新到 [[2026-06-13_training-dynamics-reading-list]]。新的优先级不再按“谁压缩 novelty”排序，而是按机制适配排序：

1. S0：MoLingo 本体，作为首个显微镜必须精读。
2. S1：CFG++、APG、TCFG、C2FG、CFG-Ctrl、CFG-Zero*、FlowMotion，作为 guidance / flow 机制库。
3. S2：S-CFG、MotionCLR、TempoControl、ParTY，作为 token-time-part controllable motion 机制库。
4. S3：MaxSim、PST、MoCHA、Motion Attribution、ALG，用作细粒度评估和归因启发。

---

## 8. 一句话版本

MoDebug 当前不能靠旧 gate、APG hook、norm clamp 达到 ICLR；下一步应把 MoLingo 当作显微镜，先发现 layer、diffusion step、text token、body part 的引导分工，再把 CFG++、APG/TCFG、C2FG/CFG-Ctrl、FlowMotion、MotionCLR/TempoControl、ParTY 等机制适配成 motion-specific guidance，并用细粒度可控性和多 baseline 迁移证明它不是 MoLingo 单点调参。
