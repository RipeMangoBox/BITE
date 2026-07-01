---
title: StoryMotion Novelty and Value Positioning
created: 2026-06-02T21:30:04+08:00
updated: 2026-06-02T23:09:30+08:00
status: archived
hypothesis: StoryMotion 的可守 novelty 不在 storyboard-to-animation 或 generic keyframe control，而在 multi-shot motion asset 的 shot-local editing contract：锁定未编辑 shot 内部帧，只允许被编辑 shot 与邻接 boundary buffer 改变，从而优化 fidelity、continuity、editing efficiency 的 Pareto trade-off。
source_papers:
  - "[[STMC_Multi-Track_Timeline_Control_for_Text-Driven_3D_Human_Motion_Generation|STMC]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In-betweening_with_Diffusion_Models_CondMDI|CondMDI]]"
  - "[[analysis/ECCV_2024/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model|MotionLCM]]"
  - "[[analysis/SIGGRAPH_2025/Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation|Sketch2Anim]]"
  - "[[analysis/Whitepaper_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]]"
  - "[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per-Joint_Latent_Decomposition|PRISM]]"
  - "[[analysis/arxiv_2026/ActionPlan_Future-Aware_Streaming_Motion_Synthesis_via_Frame-Level_Action_Planning|ActionPlan]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion-Condition-Motion_Paradigm|MotionLab]]"
  - "[[analysis/arxiv_2026/Sketch2Colab_Sketch-Conditioned_Multi-Human_Animation_via_Controllable_Flow_Distillation|Sketch2Colab]]"
  - "[[analysis/arxiv_2025/STAGE_Storyboard-Anchored_Generation_for_Cinematic_Multi-shot_Narrative|STAGE]]"
  - "[[analysis/arxiv_2025/FairyGen_Storied_Cartoon_Video_from_a_Single_Child-Drawn_Character|FairyGen]]"
  - "[[analysis/arxiv_2026/AnyAct_Towards_Human_Reenactment_of_Character_Motion_From_Video|AnyAct]]"
  - "[[analysis/CVPR_2026/Unifying_Precise_Keyframes_and_Semantic_Control_via_Multi-level_Diffusion|Multi-level Diffusion]]"
  - "[[analysis/arxiv_2026/Learning_Context-Adaptive_Motion_Priors_for_Masked_Motion_Diffusion_Models_with_Efficient_Kinematic_Attention_Aggregation|MMDM+KAA]]"
tags:
  - StoryMotion
  - motion_generation
  - motion_editing
  - storyboard
  - research_positioning
---

# StoryMotion Novelty and Value Positioning

> [!note] 继承关系
> 这份笔记记录 2026-06-02 的 novelty/价值定位推理，核心结论先被 [[ideas/StoryMotion/archived/v3/2026-06-03_storymotion_canonical_plan|StoryMotion Canonical Plan]] 继承并进一步收缩，随后被当前 CSG 主线 [[2026-06-04_storymotion_cinematic_section_graph_plan|StoryMotion Cinematic Section Graph Plan]] 取代。

> [!abstract] 核心结论
> StoryMotion 现在最稳的定位不是“更好的文本到动作生成器”，也不是“第一个 storyboard 到 3D motion”。这些空间已经被 STMC、Sketch2Anim、Sketch2Colab、STAGE、FairyGen、CondMDI、Kimodo、MotionLab、PRISM 和 ActionPlan 大幅压缩。可守的定位应是：**面向生成后 multi-shot motion asset 的局部编辑协议与系统层**。它把 shot 变成可缓存、可锁定、可局部失效、可边界自适应的编辑单元；目标是在动画迭代中避免“改一个局部导致全片漂移”。

---

## 1. 一句话定位

**StoryMotion = ShotGraph-based local editing layer for generated or mocap motion assets.**

它不应该声称自己比 CondMDI 更会做 in-betweening，也不应该声称自己比 Sketch2Anim 更理解 storyboard。它应该声称：

- 输入是一段已经生成或已有的 multi-shot motion asset，以及结构化 ShotGraph。
- 用户编辑一个 shot 的 text、end pose、root waypoint、duration 或 object/scene anchor。
- 系统只重新生成或优化被编辑 shot 与邻接 boundary buffer。
- 未编辑 shot 的 interior frames 作为 locked asset，保持 near-identical 或 exact preserve。
- 评价目标不是单次生成质量最大化，而是 **edit success、interior drift、boundary continuity、invalidated radius、runtime** 的 Pareto 优势。

这是一种 **editing contract**，不是一个普通 generation claim。

## 2. 为什么原始宽 claim 不够 novel

### 2.1 “multi-track / timeline control” 已被 STMC 占据

[[STMC_Multi-Track_Timeline_Control_for_Text-Driven_3D_Human_Motion_Generation|STMC]] 已经把复杂文本运动形式化为 multi-track timeline control：每个时间区间绑定文本，在去噪过程中做身体部位拼接和时序缝合。它直接覆盖“复杂多段文本动作组合”的大部分叙事空间。

所以 StoryMotion 不能主打“我能按时间线生成多段动作”。要避开 STMC，必须强调 **生成后反复编辑、缓存、锁定、局部失效**，而不是一次性 timeline synthesis。

### 2.2 “keyframe / waypoint / in-betweening control” 已被 CondMDI、Kimodo、MotionLab 占据

[[analysis/SIGGRAPH_2024/Flexible_Motion_In-betweening_with_Diffusion_Models_CondMDI|CondMDI]] 已经把 motion in-betweening 统一成 mask-conditioned diffusion，支持灵活关键帧、部分关节、根轨迹和文本风格控制。

[[analysis/Whitepaper_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation|Kimodo]] 和 [[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion-Condition-Motion_Paradigm|MotionLab]] 进一步压缩了“keyframe + trajectory + text control”的空间。

所以 StoryMotion 不能说“我有 start/end pose 和 waypoint，因此 novel”。这些只是输入条件，不能构成主要创新。

### 2.3 “storyboard/sketch to animation” 已被 Sketch2Anim/Sketch2Colab 压缩

[[analysis/SIGGRAPH_2025/Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation|Sketch2Anim]] 已经明确处理 sketch storyboard 到 3D animation，并用 2D-3D embedding alignment 与轨迹/关键姿态控制解决跨域生成问题。[[analysis/arxiv_2026/Sketch2Colab_Sketch-Conditioned_Multi-Human_Animation_via_Controllable_Flow_Distillation|Sketch2Colab]] 进一步走向 storyboard-style sketches、object-aware、multi-human motion。视频域里，[[analysis/arxiv_2025/STAGE_Storyboard-Anchored_Generation_for_Cinematic_Multi-shot_Narrative|STAGE]] 和 [[analysis/arxiv_2025/FairyGen_Storied_Cartoon_Video_from_a_Single_Child-Drawn_Character|FairyGen]] 已经把 storyboard / shot-level narrative 作为视频生成结构使用，因此 StoryMotion 不能把“有分镜输入”本身作为主 novelty。

因此 StoryMotion 不能把 novelty 放在“storyboard 输入”。更稳的说法是：StoryMotion 可以接收 storyboard-derived motion asset，但它研究的是 **生成后 motion asset 的版本化局部编辑**。

### 2.4 “long-horizon streaming / narrative continuity” 已被 PRISM/ActionPlan 威胁

[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per-Joint_Latent_Decomposition|PRISM]] 和 [[analysis/arxiv_2026/ActionPlan_Future-Aware_Streaming_Motion_Synthesis_via_Frame-Level_Action_Planning|ActionPlan]] 已经覆盖 streaming、future-aware planning、叙事连续、离线/在线生成和部分编辑。

StoryMotion 不能和它们抢“长程理解”主战场。它的区别必须是：**有意限制变更半径**，把下游 drift 视为 bug，而不是上下文自适应的一部分。

## 3. 挤压赛道矩阵

> [!note] 读表方式
> “挤压”不是说这些工作已经完全做了 StoryMotion，而是说它们已经压住了某些宽泛 claim。StoryMotion 只有在避开这些被压住的 claim，并把剩余空间做实，才有价值。

| Work                                                                                                                             | 挤压维度                                                                                    | 已经压住的 StoryMotion 宽 claim                                | 没压住的剩余空间                                                                                 | 对 StoryMotion 的启发                                                 | 你需要判断                                                               |
| -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| [[STMC_Multi-Track_Timeline_Control_for_Text-Driven_3D_Human_Motion_Generation\|STMC]]                        | 多轨时间线、复杂动作组合、测试时拼接                                                                      | “我能把多段文本动作按 timeline 组合成一段 3D motion”                    | 生成后版本管理、shot 锁定、反复局部编辑、cache invalidation                                                | StoryMotion 不应主打 timeline generation，而应主打 generated asset editing | STMC 是否已经支持用户改第 2 段后保持第 1/3 段 interior 不漂移                          |
| [[analysis/SIGGRAPH_2024/Flexible_Motion_In-betweening_with_Diffusion_Models_CondMDI\|CondMDI]]                                  | 任意关键帧、部分关节、根轨迹、mask-conditioned in-betweening                                           | “我能用 start/end pose、关键帧、根轨迹生成或补间 B 段”                    | 多 shot 资产协议、locked interior、局部失效半径、可逆编辑日志                                                | CondMDI 应作为 generator/baseline，而不是 StoryMotion 要竞争的核心生成器          | full-sequence CondMDI hard-mask A/C 是否已经足够快且足够稳                     |
| [[analysis/ECCV_2024/MotionLCM_Real-time_Controllable_Motion_Generation_via_Latent_Consistency_Model\|MotionLCM]]                | 实时可控生成、latent consistency、ControlNet spatial control                                    | “我能快速按 trajectory / spatial control 生成 motion”           | 生成后的 shot graph、版本稳定性、undo、边界自适应策略                                                       | MotionLCM 可作为低延迟局部 generator                                      | 实时生成是否已经让局部缓存的 runtime 价值变小                                         |
| [[analysis/Whitepaper_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation\|Kimodo]]                                         | 高质量 text + keyframes + waypoints + dense paths 可控生成                                     | “我能同时控制文本、关键帧、waypoint、dense path”                       | 已批准片段的锁定、不重采样、不漂移、版本对比                                                                   | StoryMotion 要避免把 waypoint control 当 novelty                       | Kimodo 是否已有明确的 local edit radius 和 preserve contract                |
| [[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion-Condition-Motion_Paradigm\|MotionLab]] | 统一 generation/editing/in-betweening/style/trajectory 框架                                 | “我能统一多种 motion generation/editing task”                  | production-style asset versioning、locked shot interior、cache/undo/invalidation           | StoryMotion 不是统一模型，而是编辑系统协议                                       | MotionLab 的 source motion editing 是否已经能表达 shot-level locked regions |
| [[analysis/SIGGRAPH_2025/Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation\|Sketch2Anim]]                    | sketch/storyboard 到 3D animation、多条件草图控制                                                | “我是 storyboard-conditioned 3D animation/motion”          | 对已经生成的 multi-shot motion asset 做局部稳定修改                                                   | StoryMotion 应作为 Sketch2Anim 之后的 editing layer                     | Sketch2Anim 是否处理反复改某个 shot 并保持其他 shot interior                      |
| [[analysis/arxiv_2026/Sketch2Colab_Sketch-Conditioned_Multi-Human_Animation_via_Controllable_Flow_Distillation\|Sketch2Colab]]   | storyboard-style sketch、object-aware、多人体 3D motion                                      | “我能从 storyboard/sketch 理解多人/物体场景并生成 motion”              | 单人体/弱交互条件下的 post-generation local edit contract                                          | StoryMotion MVP 应避免抢 object-aware multi-human story understanding | 如果你想做多人/物体，Sketch2Colab 的挤压会非常强                                     |
| [[analysis/arxiv_2025/STAGE_Storyboard-Anchored_Generation_for_Cinematic_Multi-shot_Narrative\|STAGE]]                           | 视频域结构化 storyboard、start/end frame pairs、多镜头记忆、镜头间转换训练                                    | “我能用 storyboard 组织 multi-shot narrative”                    | 3D skeleton motion asset 的可锁定局部编辑、数值级 interior drift/continuity 评估                            | 视频域已经证明分镜结构有价值；StoryMotion 需要转到 3D motion 编辑 contract      | STAGE 的视频级 consistency 是否已经足以削弱 StoryMotion 的 storyboard 叙事       |
| [[analysis/arxiv_2025/FairyGen_Storied_Cartoon_Video_from_a_Single_Child-Drawn_Character\|FairyGen]]                             | MLLM 生成 structured storyboard、shot design、角色风格一致的故事视频                                      | “我能从一个故事/分镜生成角色动画视频”                                     | 3D skeletal motion 的可复用资产层、局部修改半径、跨 shot root/contact 状态记忆                              | StoryMotion 不应抢儿童画/视频故事生成，而应借鉴 shot planning 输入              | 如果 StoryMotion 只讲 story-driven animation，FairyGen 会造成强挤压             |
| [[analysis/arxiv_2026/AnyAct_Towards_Human_Reenactment_of_Character_Motion_From_Video\|AnyAct]]                                  | 视频到角色动作复演、character motion transfer、人类视频驱动角色动作                                        | “我能把视频里的角色动作迁移/复演到目标角色”                                  | 对已生成 3D motion asset 的局部版本稳定编辑                                                            | 可作为 video-to-motion / reenactment 侧参考，不应作为 StoryMotion MVP 主线       | 如果输入改成 video reference，AnyAct 类工作的挤压会明显增强                         |
| [[analysis/CVPR_2026/Unifying_Precise_Keyframes_and_Semantic_Control_via_Multi-level_Diffusion\|Multi-level Diffusion]]          | 文本条件 motion in-betweening、精确关键帧控制、语义控制与空间控制统一                                         | “我能同时满足文本语义与精确 keyframe 约束”                              | 多 shot asset locking、编辑日志、cache invalidation、跨 shot 局部失效策略                              | 关键帧控制不能作为 StoryMotion 主贡献，必须作为局部 generator/baseline          | full-sequence keyframe-constrained diffusion 是否支配 shot-local 方案        |
| [[analysis/arxiv_2026/Learning_Context-Adaptive_Motion_Priors_for_Masked_Motion_Diffusion_Models_with_Efficient_Kinematic_Attention_Aggregation\|MMDM+KAA]] | masked motion completion/refinement/in-betweening、KAA 时空聚合                                  | “我能用 masked diffusion 局部补全或重生成 motion”                    | shot 语义边界、locked interior contract、版本化资产操作                                                   | MMDM+KAA 可以作为局部重生成 baseline；不能让 StoryMotion 退化成普通 mask inpainting | mask-based 局部补全是否已足以覆盖 B 段重生成                                      |
| [[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per-Joint_Latent_Decomposition\|PRISM]]                       | streaming/narrative motion、per-joint latent decomposition                               | “我能长程连续生成，并处理叙事动作流”                                      | 有意限制下游 drift、锁定未编辑 shot、可审计局部变更                                                          | 可借鉴 per-joint latent 做 boundary adapter 或影响区域估计                   | PRISM 是否支持上游编辑后下游 interior exact/near preserve                      |
| [[analysis/arxiv_2026/ActionPlan_Future-Aware_Streaming_Motion_Synthesis_via_Frame-Level_Action_Planning\|ActionPlan]]           | future-aware streaming/offline synthesis、frame-level planning、zero-shot edit/in-between | “我能做长程 planning、未来感知、streaming/offline motion synthesis” | asset-level cache、局部编辑半径、导演式版本稳定                                                         | StoryMotion 不应讲 future-aware planning，要讲 edit stability           | ActionPlan 的 zero-shot editing 是否已经有 locked asset 保真指标              |
| Game animation trees / crossfade                                                                                                 | clip 替换、state machine、crossfade、工业片段拼接                                                  | “我能把片段局部替换并平滑过渡”                                         | generative B 段 + learned semantic/kinematic boundary adapter + motion-generation metrics | 必须打工业 crossfade/spline baseline，否则系统价值站不住                         | 传统 crossfade 在你的目标数据上是否已经足够好                                        |


### 3.1 挤压强度排序

| Claim                                                     | 挤压强度 | 主要挤压者                                                        | 判断                             |
| --------------------------------------------------------- | ---: | ------------------------------------------------------------ | ------------------------------ |
| storyboard/sketch to 3D animation                         |   很强 | Sketch2Anim, Sketch2Colab                                    | 不建议主打                          |
| video-domain storyboard / multi-shot narrative generation |   很强 | STAGE, FairyGen                                              | 只能作为跨域参考，不能当 3D motion novelty |
| keyframe/waypoint/trajectory control                      |   很强 | CondMDI, Kimodo, MotionLCM, MotionLab, Multi-level Diffusion | 只能作为条件接口                       |
| complex multi-action timeline generation                  |    强 | STMC, ActionPlan                                             | 不建议作为核心 novelty                |
| long-horizon narrative/streaming continuity               |    强 | PRISM, ActionPlan                                            | 不建议抢主战场                        |
| generic motion editing unified model                      |  中到强 | MotionLab, CondMDI, ActionPlan, MMDM+KAA                     | 需要收窄到 shot-local asset editing |
| shot-level locked interior preserve                       |    中 | CondMDI hard-mask 可模拟，但未必是系统目标                               | 可守，但必须实验证明 full inpainting 不支配 |
| cache invalidation / edit radius / reversible edit log    |    弱 | 相关工作少直接形式化                                                   | 剩余空间较清楚                        |
| learned boundary adapter under locked-interior contract   |    中 | blend/crossfade/in-betweening 会挤压                            | 可守，但必须赢 naive 和工业基线            |

### 3.2 剩余空间是否有价值的判定标准

| 剩余空间                         | 成立条件                                        | 不成立条件                         | 最小验证                                          |
| ---------------------------- | ------------------------------------------- | ----------------------------- | --------------------------------------------- |
| locked-interior shot editing | 动画迭代中确实需要已批准片段不漂移                           | 用户更偏好全局自适应，允许全片变化             | 用户任务或 case study：只改 B，A/C 不需重审                |
| dynamic boundary buffer      | 固定 2/4/8 帧 buffer 无法覆盖不同编辑幅度                | 固定宽度 + spline 已足够             | 编辑幅度 vs 最优 buffer width 曲线                    |
| learned boundary adapter     | 显著降低 jump/jerk/foot slip，且 interior drift 小 | linear/spline/crossfade 已接近上限 | direct cut、linear、spline、crossfade、adapter 对比 |
| cache invalidation           | 多轮编辑中 cache hit 高，重算区域小                     | 几次编辑后无效区域快速扩散成全局              | 10-step edit sequence 的 invalidated radius 曲线 |
| generator-agnostic protocol  | CondMDI/MotionLCM/MotionLab 都能接入            | 只对某个 generator 的文件格式有效        | 至少两个 generator 的相同 ShotGraph 接口               |
| reversible edit log          | undo/redo 能精确恢复旧版本                          | 保存完整副本才可恢复，空间爆炸               | 操作栈复杂度、恢复误差、存储开销                              |

## 4. 真正可守的 novelty 在哪里

### 4.1 从 generation problem 转成 asset editing problem

大多数 motion generation 论文的隐含目标是：给定条件，生成一段尽可能自然、语义正确的 motion。StoryMotion 的目标不同：

> 在已有 multi-shot asset 中，局部修改一个 shot，同时最大限度不破坏已经批准的其他片段。

这在动画制作、previs、game cinematic、AI-assisted mocap cleanup 中有实际价值。导演或动画师常常已经批准 A 和 C，只想改 B 的落点、节奏或 pose。如果系统每次都全段重采样，A/C 的细节会漂移，人工验收成本会爆炸。

### 4.2 Shot 不是时间切片，而是可编辑资产单元

StoryMotion 的 shot 应该包含：

- semantic text
- start/end pose
- root/heading/velocity state
- waypoints
- optional camera/object anchors
- interior latent/cache
- boundary buffer policy
- dependency edges to neighboring shots
- invalidation state

这比普通时间段更强。它是 **可版本化的 conditioning block**，可以被锁定、替换、撤销、重算和审计。

### 4.3 Novelty 是“变更半径可控”

普通 full-sequence generation 的问题是：输出是整体样本。编辑 B 之后，C 可能变得更自然，但也可能漂移。StoryMotion 把目标改成：

- B 要满足新编辑条件。
- A/C interior drift 要低。
- boundary jump、heading jump、jerk、foot slip 要低。
- invalidated radius 要小。
- runtime 要低。

这不是单指标最优，而是工具系统里的 Pareto 优势。

### 4.4 Boundary adapter 是关键技术，不是装饰

如果只有 linear blend，StoryMotion 没有论文价值。真正需要做的是：

- dynamic boundary width：根据 B 的编辑幅度决定需要释放多少邻接帧。
- learned boundary adapter：只改 boundary buffer，预测 root、heading、velocity、foot contact 的连续过渡。
- latent/interior cache：未编辑区域复用原 latent 或原 motion token，避免全局漂移。
- edit log / undo stack：保存操作历史与失效区域，让局部编辑可逆。

### 4.5 它不是替代 CondMDI，而是要求 CondMDI 接受编辑协议约束

CondMDI 可以作为 B 的局部 generator，也可以作为 full-sequence constrained inpainting baseline。StoryMotion 的问题是：

> 当 A/C 已被批准并锁定时，怎样用尽量小的 invalidated radius 完成 B 的编辑？

这个问题可以调用 CondMDI、MotionLCM、MotionLab 或 Kimodo 作为局部生成器，但贡献在 ShotGraph、cache、adapter 和 evaluation contract。

## 5. 多角度价值解释

### 5.1 研究价值

它把 motion generation 从“单次采样质量”推进到“可编辑生成资产”。这类似图像生成从 prompt-to-image 走向 layer、mask、ControlNet、inpainting、history-aware editing。motion 领域现在有强大的生成器，但缺少对 **版本稳定性** 和 **局部编辑半径** 的正式建模。

### 5.2 工程价值

动画迭代最怕不可控漂移。全段重生成看起来质量高，但每次都需要重新检查所有片段。StoryMotion 如果能保证“只影响 B 和 boundary buffer”，就能把 QA 范围从全片缩小到局部。

### 5.3 用户体验价值

对创作者来说，重要问题不是“能不能生成一个不错的动作”，而是：

- 我改一个落点，会不会把之前满意的走路细节改掉？
- 我能不能撤销这次修改？
- 我能不能只让前后 8 帧适配，而不动整段？
- 我能不能比较两个版本的变更区域？

StoryMotion 的价值就在这些生成模型论文常忽略的交互约束。

### 5.4 评价价值

现有指标常看 FID、R-precision、keyframe error、trajectory error。StoryMotion 需要引入编辑系统指标：

| Metric | Measures | Why it matters |
|---|---|---|
| edit success | B 是否满足新 text/pose/waypoint | 局部编辑是否有效 |
| interior drift | A/C 内部帧相对原 asset 的偏移 | 已批准片段是否被破坏 |
| boundary continuity | root jump、heading jump、jerk、foot slip | 局部替换是否自然衔接 |
| invalidation radius | 需要重算或改动的帧数 | 可控变更半径 |
| runtime | 局部重算 vs 全段重算时间 | 交互式编辑可用性 |
| reversibility | undo 后是否恢复原 asset | 版本管理可信度 |

### 5.5 负面价值判断也很重要

如果 StoryMotion 无法证明 learned boundary adapter 明显优于 linear blend、spline 和 game crossfade，它就只是后处理工具。如果 full-sequence CondMDI constrained inpainting 在 fidelity、continuity、runtime 上全面支配 StoryMotion，方向应停止或转向。

## 6. GPT vs DeepSeek 博弈记录

### Round 1：反方问题

**DS 问 1：与 CondMDI 的本质区别是什么？**

GPT 答：CondMDI 是生成器或补间器；StoryMotion 是编辑协议。CondMDI 可以作为 B 段 generator，也可以作为 full-sequence constrained inpainting baseline。区别不在“能不能约束关键帧”，而在是否提供 ShotGraph、locked interior、cache invalidation、boundary-width scheduling 和可审计编辑日志。必须通过实验比较 CondMDI full-sequence inpainting 与 shot-local editing 的 Pareto 曲线，否则该区别不成立。

**DS 问 2：near-identical 与 exact preserve 是否和 continuity 冲突？**

GPT 答：冲突存在，而且这是方向的核心。StoryMotion 不应再说 A/C 全部 bit-identical 且边界完美连续。正确 contract 是：A/C interior locked，邻接 boundary buffer 可释放。claim 应是 interior fidelity 与 boundary continuity 的可控 Pareto，而不是两者同时绝对最优。

**DS 问 3：boundary adapter 的创新性是什么？**

GPT 答：如果只是线性 blend，没有创新。必须是可学习 adapter，并且显式预测或约束 root、heading、velocity、foot contact，配合 dynamic boundary width。基线必须包括 direct cut、linear blend、spline、game crossfade、CondMDI full inpainting。

**DS 问 4：locked interior 是否不实用？**

GPT 答：它不适合所有情况。它适合“已批准片段不希望漂移”的 production/editing 场景。若用户希望全局风格重新协调，就应该切换到 global regenerate 模式。StoryMotion 的定位应是局部编辑模式，不是唯一编辑模式。

**DS 问 5：多人和物体交互怎么办？**

GPT 答：第一版应明确限制为 single-human、无强物理交互或弱 object anchor。多人交互会让 locked interior 更难，因为接触约束跨 shot 和跨角色传播。这个不应作为 MVP 主 claim。

**DS 问 6：为什么不做 PRISM 式 per-joint editing？**

GPT 答：per-joint 是可扩展方向，不是第一版核心。StoryMotion 的粒度是 production shot，而不是 joint latent。它可以吸收 PRISM 的 per-joint decomposition 作为 boundary adapter 或局部影响区域估计，但主贡献仍是 shot-level edit contract。

**DS 问 7：效率优势是否夸大？**

GPT 答：不能只说“局部生成更快”。必须测端到端，包括加载、cache、adapter、后处理。真正的效率应包括人工验收范围：全段重生成要检查全段，shot-local 只检查 B 和 boundary。

**DS 问 8：为什么叫 StoryMotion？story 信息在哪里？**

GPT 答：如果不处理 story understanding，就不要声称 storyboard semantics。更稳的名字可解释为 story-level multi-shot motion asset editing。它可以接收来自 storyboard/sketch 系统的结果，但不是 sketch understanding 模型。

### Round 2：反方升级后的结论

DeepSeek 第二轮把条件压得更清楚：

- 若只是 CondMDI output 裁剪、替换和 blend，价值低。
- 若实现完整 ShotGraph、cache、learned boundary adapter、dynamic width、undo/invalidation，并与 CondMDI full inpainting、game crossfade、linear/spline blend 严格比较，则从“低价值”上升为“有条件可投”。
- 更适合 SIGGRAPH/TOG production/system 或 animation-oriented venue；如果包装成 CV 主会的通用生成算法，风险仍高。

## 7. 必须做的实验

### 7.1 核心对比

| Baseline | Why needed |
|---|---|
| direct cut | 证明边界问题真实存在 |
| linear blend / spline | 证明不是简单平滑就够 |
| game-style crossfade | 对比工业常用片段替换方案 |
| CondMDI full-sequence constrained inpainting | 检验 StoryMotion 是否只是冗余协议 |
| local CondMDI for B + learned boundary adapter | StoryMotion 主方法 |
| MotionLCM/Kimodo/MotionLab local generator variant | 验证协议是否 generator-agnostic |

### 7.2 编辑类型

- B.end_pose edit：改变 B 末端 pose 或 root heading。
- B.root_waypoint edit：改变路径中点或终点。
- B.duration edit：改变节奏，测试时间拉伸与边界连续。
- B.text edit：从 walk 改为 turn、sit、jump 等。

### 7.3 指标

- B target error：编辑目标是否达成。
- A/C interior MPJPE or rotation error：未编辑区域漂移。
- boundary root/heading jump。
- transition jerk。
- foot slip ratio。
- invalidated radius。
- runtime and cache hit rate。
- user study：动画师或 motion researcher 评价局部可控性与视觉自然度。

### 7.4 最小可接受成功标准

StoryMotion 不需要在全局 motion naturalness 上赢 full regeneration。它需要证明：

- 在相近 B edit success 下，interior drift 明显低于 full-sequence inpainting。
- 在相近 interior drift 下，boundary continuity 明显优于 direct cut 和 naive blend。
- invalidated radius 和人工检查范围显著小于 full regeneration。
- learned boundary adapter 相比 linear/spline/crossfade 有统计显著优势。

## 8. 当前 MVP 的意义和局限

当前 4090 真实 MVP 只证明了 harness，不证明方法有效：

- 数据来自真实 CondMDI diffusion run，不是模拟。
- 72 frames 被切成 A `0:24`、B `24:48`、C `48:72`。
- 替换 B 后，A/C interior exact preserve。
- 但 boundary jump 明显变大：observed BC `0.003840`，shot-local BC `0.038063`。
- 简单 boundary blend 降到 `0.023085`，但仍不是 learned adapter。

这个结果的价值是把核心矛盾暴露出来：**局部保真很容易，边界连续很难**。下一步不是继续声称成功，而是把它转成 boundary adapter 的训练与评估问题。

## 9. 结论

StoryMotion 的 novelty 可以成立，但必须换一种说法：

> 不是“第一个 storyboard-conditioned 3D motion generator”，而是“第一个系统性形式化并优化 multi-shot motion asset 的局部编辑 contract：locked interior + adaptive boundary + cache invalidation + reversible edit log”。

价值也不是生成质量本身，而是 production/editing workflow 中的 **稳定性、可审计性、局部变更半径和迭代效率**。

最危险的失败模式是：做成一个简单的 B 段重生成加 blend。如果这样，它会被 CondMDI、STMC、MotionLab、游戏 crossfade 和普通 inpainting 同时打掉。

最有希望的路线是：

1. 接受 CondMDI/MotionLCM/MotionLab/Kimodo 作为 generator，而不是竞争 generator。
2. 把贡献集中到 ShotGraph、locked cache、dynamic boundary width、learned boundary adapter、undo/invalidation。
3. 用严格实验回答：为什么全段 constrained inpainting 不够，为什么 naive blend 不够，为什么工业 crossfade 不够。
4. 明确第一版边界：single-human、无强接触、多 shot post-generation editing。

只要这个定位守住，StoryMotion 是一个有价值的系统型研究问题；如果回到宽泛的 storyboard-to-motion 或 keyframe-control 叙事，则 novelty 很弱。
