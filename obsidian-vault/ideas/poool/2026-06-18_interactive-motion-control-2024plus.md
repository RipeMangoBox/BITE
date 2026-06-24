---
title: "2024+ 交互式 Motion Control：从输入模态扩展到控制仲裁"
status: draft
created: 2026-06-18T17:01:33+08:00
updated: 2026-06-18T17:36:00+08:00
hypothesis: 交互式 motion control 的下一步不应继续堆输入模态，而应把已有的特定模态控制推进到通用冲突仲裁、闭环局部修复和可验证交互指标。
tags:
  - paper-idea
  - Motion_Generation
  - interactive_control
  - multimodal_control
  - character_animation
source_papers:
  - "[[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM (SIGGRAPH_2025)]]"
  - "[[analysis/SIGGRAPH_2025/Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation.md|Sketch2Anim (SIGGRAPH_2025)]]"
  - "[[analysis/CVPR_2026/Sketch2Colab.md|Sketch2Colab (CVPR_2026)]]"
  - "[[analysis/ICCV_2025/PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learning.md|PRIMAL (ICCV_2025)]]"
  - "[[analysis/arxiv_2026/AnyAct_Towards_Human_Reenactment_of_Character_Motion_From_Video.md|AnyAct (arxiv_2026)]]"
  - "[[analysis/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.md|PoseAnything (CVPR_2026)]]"
  - "[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl (SIGGRAPH_2024)]]"
  - "[[analysis/CVPR_2025/Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories.md|Motion Prompting (CVPR_2025)]]"
  - "[[analysis/ICLR_2024/OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation.md|OmniControl (ICLR_2024)]]"
  - "[[analysis/ECCV_2024/TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis.md|TLControl (ECCV_2024)]]"
  - "[[analysis/ICCV_2025/MaskControl_Spatio_Temporal_Control_for_Masked_Motion_Synthesis.md|MaskControl (ICCV_2025)]]"
  - "[[analysis/ICLR_2025/DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control.md|DART (ICLR_2025)]]"
  - "[[analysis/ICCV_2025/MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space.md|MotionStreamer (ICCV_2025)]]"
  - "[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.md|PRISM (arxiv_2026)]]"
  - "[[analysis/WHITEPAPER_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation.md|Kimodo (WHITEPAPER_2026)]]"
  - "[[analysis/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives.md|MotionBricks (SIGGRAPH_2026)]]"
  - "[[analysis/AAAI_2025/MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Controls.md|MotionCraft (AAAI_2025)]]"
  - "[[analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling.md|AnyMo (arxiv_2026)]]"
  - "[[analysis/arxiv_2025/DualFlow_Unified_Multi_Modal_Interactive_Reactive_3D_Motion_Generation_via_Rectified_Flow.md|DualFlow (arxiv_2025)]]"
  - "[[analysis/arxiv_2024/It_Takes_Two_Real_time_Co_Speech_Two_persons_Interaction_Generation_via_Reactive_Auto_regressive_Diffusion_Model.md|It Takes Two (arxiv_2024)]]"
  - "[[analysis/arxiv_2026/TextOp_Real_time_Interactive_Text_Driven_Humanoid_Robot_Motion_Generation_and_Control.md|TextOp (arxiv_2026)]]"
  - "[[analysis/arxiv_2026/KV-Control_Parameter-Efficient_KV_Injection_for_Trajectory-Controlled_Text-to-Motion.md|KV-Control (arxiv_2026)]]"
  - "[[analysis/arxiv_2026/DrawMotion_Generating_3D_Human_Motions_by_Freehand_Drawing.md|DrawMotion (arxiv_2026)]]"
  - "[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]]"
  - "[[analysis/arxiv_2025/FlexMotion_Lightweight_Physics-Aware_and_Controllable_Human_Motion_Generation.md|FlexMotion (arxiv_2025)]]"
  - "[[analysis/arxiv_2025/CoMPAS3D_A_Dataset_and_Benchmark_for_Interactive_Motion.md|CoMPAS3D (arxiv_2025)]]"
  - "[[analysis/arxiv_2025/MEgoHand_Multimodal_Egocentric_Hand-Object_Interaction_Motion_Generation.md|MEgoHand (arxiv_2025)]]"
  - "[[analysis/arxiv_2025/Cross-Modal_Instructions_for_Robot_Motion_Generation.md|CrossInstruct (arxiv_2025)]]"
  - "[[analysis/arxiv_2025/MotionDuet_Dual-Conditioned_3D_Human_Motion_Generation_with_Video-Regularized_Text_Learning.md|MotionDuet (arxiv_2025)]]"
---

# 2024+ 交互式 Motion Control：从输入模态扩展到控制仲裁

## 结论先行

这批工作表面上都在说“control”，但它们解决的不是同一个问题。真正的分界不在输入是 sketch、视频、轨迹、文本还是力，而在四件事：

1. 控制信号在语义上处于哪一层：任意时序信号、轨迹、关节、部位、跨对象动作、多人关系、物理冲量。
2. 控制如何执行：检索匹配、冻结生成器外挂 adapter、扩散/流模型条件注入、短窗口自回归、测试时优化、物理反应器。
3. 是否真的闭环：多数论文的 interactive 只是“推理快”，不是用户持续输入后系统持续响应、修正、仲裁。
4. 用户工作流价值：动画师要的是低成本表达意图、快速迭代和局部可修；机器人/游戏要的是低延迟、稳定性和物理可执行。

所以我对这个方向的判断是：**2024-2026 已经把“可以接收哪些输入模态”卷得很满，前沿正在从输入扩展转向条件整合、冲突仲裁与闭环可验证**。这不是说冲突仲裁完全没人做：[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]] 已经正面处理 text + trajectory 的条件冲突，[[analysis/arxiv_2026/KV-Control_Parameter-Efficient_KV_Injection_for_Trajectory-Controlled_Text-to-Motion.md|KV-Control (arxiv_2026)]] 也把几何约束做成 attention-side 的可寻址控制记忆。但这些还主要局限在特定模态对和特定骨干上，离“任意异质控制信号进入同一个闭环系统后能被解释、让步、局部修复”还有距离。[[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM (SIGGRAPH_2025)]] 的意义也在这里：它不是生成质量 SOTA，而是把“任意时序信号能否成为 motion control interface”这个问题从成对监督里解放出来。

## [[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM (SIGGRAPH_2025)]] 为什么可能值得 SIGGRAPH

用户没 get 到 [[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM (SIGGRAPH_2025)]] 的价值是合理的，因为如果按 text-to-motion 或 diffusion generation 的标准看，它没有创造新动作、没有复杂语义理解，也不是画质/动作质量榜单冠军。但 SIGGRAPH 看重的不总是“模型更大”，还看重动画管线里是否出现了新的可用控制接口。

[[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM (SIGGRAPH_2025)]] 的核心是 metric-aligning motion matching：给定一段任意时序控制序列和一个 motion 数据库，它不学习控制信号到动作的显式映射，而是用 fused semi-unbalanced Gromov-Wasserstein 一类最优传输目标，让两个序列各自内部的距离结构对齐。换句话说，它不问“这个波峰语义上是不是跳跃”，而问“这段控制信号内部的相似/变化结构，能否和 motion 库中某段动作的相似/变化结构对应起来”。这让手绘曲线、合成波形、音频包络、已有 motion、甚至非标准输入都可以变成 motion matching 的控制条件。

实际价值主要有三点：

- **零训练的跨域控制接口**：换一种控制信号，不需要重新标注成对数据，也不需要重新训练 adapter。
- **DCC/动画管线友好**：输出仍是 motion matching 式 clip 选择、拼接和 blending，天然接近动画师已有工作流。
- **低数据场景可用**：对中小项目或角色定制场景，几分钟/几十分钟 motion 库比大规模 paired dataset 更现实。

这也是它能进 SIGGRAPH 的理由：它把“任意时序 sequence 控制 motion sequence”变成了一个可运行的统一接口，而不是再为每个控制模态写一套规则或训练一套模型。

硬伤也很清楚：

- **动作上限被数据库锁死**：[[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM (SIGGRAPH_2025)]] 本质是 retrieval + matching + blending，不会创造库外动作。
- **度量设计决定成败**：如果控制信号的内部距离结构和 motion 语义不一致，优化目标会给出数学上合理但动画上荒谬的对应。
- **高层语义弱**：它不理解“先走三步再跳起”，除非这种结构已经以可度量的形态出现在控制信号和 motion 库里。
- **长序列与实时性压力大**：最优传输对齐在长时序上不是天然低延迟机制，更像离线/准离线创作工具。
- **物理约束外置**：motion matching 结果仍需 IK、foot locking、碰撞处理等后处理，否则会滑步或穿模。

所以 [[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM (SIGGRAPH_2025)]] 的准确定位不是“万能 motion generator”，而是**动画创作里的 universal temporal control adapter**。它值得关注的不是最终动作是否比 [[analysis/WHITEPAPER_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation.md|Kimodo (WHITEPAPER_2026)]]、[[analysis/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives.md|MotionBricks (SIGGRAPH_2026)]] 更强，而是它把控制接口从“语义标注/配对训练”推进到“结构对齐/无监督匹配”。


>[!思考1]
>目标：任意拓扑的motion retarget.
>输入：video / 3d skeleton motion.
>输出：video & 3d skeleton motion.
>参考：
>1. retarget若干工作（人到动物、动物到人、人到人、motion to motion）；
>2. 动作映射：[[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM (SIGGRAPH_2025)]]、[[analysis/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.md|PoseAnything (CVPR_2026)]]（任意对象的视频动作生成）；
>3. 动作retarget rep：[[analysis/SIGGRAPH_2024/WalkTheDog_Cross_Morphology_Motion_Alignment_via_Phase_Manifolds.md|WalkTheDog (SIGGRAPH_2024)]]（多对象共享motion phase/manifold）、[[analysis/CVPR_2024/Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches.md|MotionPatches (CVPR_2024)]]（动作）；
>核心思想：既然[[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM (SIGGRAPH_2025)]]能够无监督学习动作的matching，[[analysis/SIGGRAPH_2024/WalkTheDog_Cross_Morphology_Motion_Alignment_via_Phase_Manifolds.md|WalkTheDog (SIGGRAPH_2024)]]能够多对象share motion phase，[[analysis/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.md|PoseAnything (CVPR_2026)]]有望在video层面进行任意对象的动作控制，有机会设计一种shared表征，用于任意拓扑的动作retarget。同时，思考如何利用视频和3d两种数据类型。大概率没有mapping，尝试自己构建mapping，或者如何无监督。
>任务：基于本md的相关工作，与ds max严肃讨论，生成obsidian-vault/ideas/poool新md。



## 2024+ 工作谱系

### 1. 显式几何控制：关节、轨迹、关键帧

这条线解决“我想让身体某部分准确经过这里”。代表包括 [[analysis/ICLR_2024/OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation.md|OmniControl (ICLR_2024)]]、[[analysis/ECCV_2024/TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis.md|TLControl (ECCV_2024)]]、[[analysis/ICCV_2025/MaskControl_Spatio_Temporal_Control_for_Masked_Motion_Synthesis.md|MaskControl (ICCV_2025)]]、[[analysis/arxiv_2026/KV-Control_Parameter-Efficient_KV_Injection_for_Trajectory-Controlled_Text-to-Motion.md|KV-Control (arxiv_2026)]]、[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]]、[[analysis/ICCV_2023/Guided_Motion_Diffusion_for_Controllable_Human_Motion_Synthesis.md|GMD (ICCV_2023)]]、[[analysis/ECCV_2024/MotionLCM_Real_time_Controllable_Motion_Generation_via_Latent_Consistency_Model.md|MotionLCM (ECCV_2024)]]、[[analysis/WHITEPAPER_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation.md|Kimodo (WHITEPAPER_2026)]]、[[analysis/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives.md|MotionBricks (SIGGRAPH_2026)]]、[[analysis/CVPR_2024/DNO_Optimizing_Diffusion_Noise_Can_Serve_As_Universal_Motion_Priors.md|DNO (CVPR_2024)]]/[[analysis/CVPR_2026/Towards_Highly_Constrained_Human_Motion_Generation_with_Retrieval_Guided_Diffusion_Noise_Optimization.md|RG-DNO (CVPR_2026)]]。

本地 KB 中，[[analysis/ICLR_2024/OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation.md|OmniControl (ICLR_2024)]] 通过全局坐标空间引导和 realism guidance 平衡控制精度与自然度；[[analysis/ECCV_2024/TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis.md|TLControl (ECCV_2024)]] 在 part-structured latent 里做测试时优化；[[analysis/ICCV_2025/MaskControl_Spatio_Temporal_Control_for_Masked_Motion_Synthesis.md|MaskControl (ICCV_2025)]] 直接优化 masked motion model 的 logits；[[analysis/arxiv_2026/KV-Control_Parameter-Efficient_KV_Injection_for_Trajectory-Controlled_Text-to-Motion.md|KV-Control (arxiv_2026)]] 把连续几何约束编码成部位-时间可寻址的 K/V 记忆，在冻结骨干自注意力中低参数注入轨迹控制；[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]] 则把 text + trajectory 分成“轨迹控制简化表示”和“文本条件全身修复”两个阶段，以 decoupling 避免两类条件直接互相拉扯；[[analysis/WHITEPAPER_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation.md|Kimodo (WHITEPAPER_2026)]] 和 [[analysis/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives.md|MotionBricks (SIGGRAPH_2026)]] 展示了大规模/实时控制系统如何把 root、pose、keyframe、end-effector 和 2D path 统一起来。

这条线最拥挤，也最容易做成伪增量：再加一种轨迹条件、再换一个 adapter、再多一个控制指标，通常不够。真正难点是当文本、轨迹、关键帧和身体部位约束互相冲突时，系统如何局部仲裁，而不是默认强控覆盖语义。[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]] 已经给了一个 text + trajectory 的早期答案，但它更像固定二阶段策略，不是通用 conflict arbiter。

### 2. Sketch / drawing / storyboard 控制

这条线解决“用户不会写精确轨迹，但能画出运动意图”。[[analysis/SIGGRAPH_2025/Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation.md|Sketch2Anim (SIGGRAPH_2025)]] 用 3D keypose/trajectory 条件训练 motion generator，再把 2D sketch encoder 映射到同一 embedding；[[analysis/CVPR_2026/Sketch2Colab.md|Sketch2Colab (CVPR_2026)]] 用 rectified flow student、能量引导和 CTMC 接触调度处理双人协作；[[analysis/arxiv_2026/DrawMotion_Generating_3D_Human_Motions_by_Freehand_Drawing.md|DrawMotion (arxiv_2026)]]、[[analysis/CVPR_2025/StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman.md|StickMotion (CVPR_2025)]] 则把 freehand drawing / stickman 作为用户友好的空间条件。

价值不是“sketch 比 text 高级”，而是 sketch 降低了表达细粒度空间关系的成本。[[analysis/arxiv_2026/DrawMotion_Generating_3D_Human_Motions_by_Freehand_Drawing.md|DrawMotion (arxiv_2026)]] 的用户实验很能说明这点：自由手绘比纯文本减少约 46.7% 操作时间，说明 sketch 是工作流价值，而不只是新模态。硬伤是配对数据和 synthetic drawing bias：模型很可能学会了某种规范化草图，而不是自然用户草图。后续如果只做“新的 sketch encoder”，容易被认为是输入换皮；更重要的是 sketch 与文本、接触、轨迹发生冲突时如何解释和修正。

### 3. 视频/任意对象到 motion 的跨模态桥接

[[analysis/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.md|PoseAnything (CVPR_2026)]]、[[analysis/arxiv_2026/AnyAct_Towards_Human_Reenactment_of_Character_Motion_From_Video.md|AnyAct (arxiv_2026)]]、[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl (SIGGRAPH_2024)]]、[[analysis/CVPR_2025/Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories.md|Motion Prompting (CVPR_2025)]]、[[analysis/SIGGRAPH_2025/Reenact_Anything_Semantic_Video_Motion_Transfer_Using_Motion_Textual_Inversion.md|Reenact Anything (SIGGRAPH_2025)]]、[[analysis/SIGGRAPH_2025/AnyTop_Character_Animation_Diffusion_with_Any_Topology.md|AnyTop (SIGGRAPH_2025)]]、[[analysis/arxiv_2025/MEgoHand_Multimodal_Egocentric_Hand-Object_Interaction_Motion_Generation.md|MEgoHand (arxiv_2025)]]、[[analysis/arxiv_2025/MotionDuet_Dual-Conditioned_3D_Human_Motion_Generation_with_Video-Regularized_Text_Learning.md|MotionDuet (arxiv_2025)]] 属于这一侧。它们不是单纯控制人体 skeleton，而是从视频、任意对象、相机轨迹、局部 2D 轨迹或跨拓扑角色中抽取可迁移的 motion intent。

[[analysis/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.md|PoseAnything (CVPR_2026)]] 用 part-aware temporal coherence 处理任意对象 pose-guided video；[[analysis/arxiv_2026/AnyAct_Towards_Human_Reenactment_of_Character_Motion_From_Video.md|AnyAct (arxiv_2026)]] 用局部稀疏 2D 关节轨迹作为跨结构桥，把 character video 的动作映射到 human motion；[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl (SIGGRAPH_2024)]] 和 [[analysis/CVPR_2025/Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories.md|Motion Prompting (CVPR_2025)]] 则说明视频生成里相机、对象轨迹和点轨迹已经变成通用 motion prompt。[[analysis/arxiv_2025/MEgoHand_Multimodal_Egocentric_Hand-Object_Interaction_Motion_Generation.md|MEgoHand (arxiv_2025)]] 把 egocentric RGB、文本、初始手姿态、VLM 推理和深度空间线索接到 hand-object motion generation；[[analysis/arxiv_2025/MotionDuet_Dual-Conditioned_3D_Human_Motion_Generation_with_Video-Regularized_Text_Learning.md|MotionDuet (arxiv_2025)]] 则把视频作为训练时分布先验，用 DASH/DUET 让 text-only 推理继承视频时空先验。

这里的真问题是“什么是可迁移 motion intent”。如果对象没有稳定关节拓扑，[[analysis/arxiv_2026/AnyAct_Towards_Human_Reenactment_of_Character_Motion_From_Video.md|AnyAct (arxiv_2026)]] 这类稀疏局部轨迹会退化成光流/点跟踪；如果视频里动作和外观/相机强耦合，[[analysis/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.md|PoseAnything (CVPR_2026)]] 式 part coherence 也可能只是在视频域保外观，而不是得到了可复用的 3D motion control representation。

>[!思考2]
>疑惑：motion领域是否有inversion相关工作？他们的目标是什么？为什么使用inversion（冻结权重，优化token/latent）而不是微调模型？
>任务：基于本md的相关工作， $papers-query-knowledge-base以及web增强检索，核心工作（高相关度、高可信度、高质量、24年及以后顶会）分析入库，不要任何参考论文都入库，与ds max严肃讨论，生成obsidian-vault/ideas/poool新md。

>[!思考3，for StoryMotion]
>关于：StoryMotion如何解耦human和camera双分支，防止互相损害生成，以及实现解耦控制；
>参考：MotionPrompting等支持画面、对象、轨迹、相机可控生成的video工作
>任务：参考本md涉及的video工作，与ds max严肃讨论，设计human-camera双分支解耦生成与控制的机制，更新obsidian-vault/ideas/StoryMotion/2026-06-18_storymotion-v4-iclr-reliability-completion.md。

### 4. 多人协作与反应式 motion

[[analysis/NEURIPS_2024/InterControl_Zero_shot_Human_Interaction_Generation_by_Controlling_Every_Joint.md|InterControl (NEURIPS_2024)]]、[[analysis/ICLR_2025/InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Modelling.md|InterMask (ICLR_2025)]]、[[analysis/arxiv_2026/HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Motion_Generation.md|HINT (arxiv_2026)]]、[[analysis/arxiv_2025/Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Constraints.md|Leader-Follower (arxiv_2025)]]、[[analysis/arxiv_2025/DualFlow_Unified_Multi_Modal_Interactive_Reactive_3D_Motion_Generation_via_Rectified_Flow.md|DualFlow (arxiv_2025)]]、[[analysis/arxiv_2024/COLLAGE_Collaborative_Human_Agent_Interaction_Generation_using_Hierarchical_Latent_Diffusion_and_Language_Models.md|COLLAGE (arxiv_2024)]]、[[analysis/arxiv_2024/It_Takes_Two_Real_time_Co_Speech_Two_persons_Interaction_Generation_via_Reactive_Auto_regressive_Diffusion_Model.md|It Takes Two (arxiv_2024)]]、[[analysis/CVPR_2026/Sketch2Colab.md|Sketch2Colab (CVPR_2026)]] 构成这条线。它们关心的不是单人动作是否符合文本，而是多人之间的接触、同步、领随、语音反应、协作任务。

本地 KB 里 [[analysis/NEURIPS_2024/InterControl_Zero_shot_Human_Interaction_Generation_by_Controlling_Every_Joint.md|InterControl (NEURIPS_2024)]] 把多人交互简化为关节接触对；[[analysis/ICLR_2025/InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Modelling.md|InterMask (ICLR_2025)]] 把两人互动建成协同 masked token 预测；[[analysis/arxiv_2026/HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Motion_Generation.md|HINT (arxiv_2026)]] 做 autoregressive multi-human；[[analysis/arxiv_2025/DualFlow_Unified_Multi_Modal_Interactive_Reactive_3D_Motion_Generation_via_Rectified_Flow.md|DualFlow (arxiv_2025)]] 用 rectified flow 统一交互与反应；[[analysis/arxiv_2024/It_Takes_Two_Real_time_Co_Speech_Two_persons_Interaction_Generation_via_Reactive_Auto_regressive_Diffusion_Model.md|It Takes Two (arxiv_2024)]] 是语音驱动双人实时互动。

这条线最容易被误解成“把两个单人模型拼起来”。真正 gap 在于**人在回路的协同**：当人类实时控制 A，B 是否能理解 A 的变化并保持互动语义，而不是离线生成一段双人动作。[[analysis/CVPR_2026/Sketch2Colab.md|Sketch2Colab (CVPR_2026)]] 已经把 sketch 多约束推到双人协作，但还不是实时 co-adaptation。

### 5. 实时/流式角色控制

[[analysis/ICLR_2025/DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control.md|DART (ICLR_2025)]]、[[analysis/ICCV_2025/MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space.md|MotionStreamer (ICCV_2025)]]、[[analysis/ICCVW_2025/Causal_Motion_Tokenizer_for_Streaming_Motion_Generation.md|Causal Motion Tokenizer (ICCVW_2025)]]、[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.md|PRISM (arxiv_2026)]]、[[analysis/arxiv_2026/TextOp_Real_time_Interactive_Text_Driven_Humanoid_Robot_Motion_Generation_and_Control.md|TextOp (arxiv_2026)]]、[[analysis/ICCV_2025/PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learning.md|PRIMAL (ICCV_2025)]]、[[analysis/SIGGRAPH_2024/CAMDM_Taming_Diffusion_Probabilistic_Models_for_Character_Control.md|CAMDM (SIGGRAPH_2024)]]、[[analysis/ECCV_2024/MotionLCM_Real_time_Controllable_Motion_Generation_via_Latent_Consistency_Model.md|MotionLCM (ECCV_2024)]]、[[analysis/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives.md|MotionBricks (SIGGRAPH_2026)]] 属于这条线。它们的关键不只是采样更快，而是能否在用户持续输入时低延迟响应。

[[analysis/ICCV_2025/PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learning.md|PRIMAL (ICCV_2025)]] 的判断很重要：短时间尺度约 0.5 秒内，人体运动主要由物理和局部状态主导，因此可用单帧状态条件的短窗口自回归 diffusion 学到冲量反应。[[analysis/ICLR_2025/DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control.md|DART (ICLR_2025)]] 用 motion primitive latent diffusion 支持实时 text-driven control；[[analysis/ICCV_2025/MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space.md|MotionStreamer (ICCV_2025)]] 和 [[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.md|PRISM (arxiv_2026)]] 强调 causal latent / per-joint latent，减少长时 drift；[[analysis/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives.md|MotionBricks (SIGGRAPH_2026)]] 则给出接近工业实时的模块化 latent 生成。

但大多数所谓 streaming 仍没有做到真正 closed loop。用户打断、环境突变、多人协作、物理扰动同时发生时，系统需要重新规划、局部修复和冲突仲裁。只把 diffusion 蒸馏到 1-4 步，并不自动等于交互系统。[[analysis/arxiv_2025/FlexMotion_Lightweight_Physics-Aware_and_Controllable_Human_Motion_Generation.md|FlexMotion (arxiv_2025)]] 值得放进这条线的边界参考：它把肌肉激活、关节驱动力矩、接触力等物理参数变成可控潜变量，但它仍偏生成/控制模型，不是用户持续介入后的闭环 repair system。

### 6. 多模态统一与对话式控制

[[analysis/AAAI_2025/MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Controls.md|MotionCraft (AAAI_2025)]]、[[analysis/ECCV_2024/MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts.md|MotionChain (ECCV_2024)]]、[[analysis/ICLR_2025/Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with_LLMs.md|Motion Agent (ICLR_2025)]]、[[analysis/arxiv_2025/OmniMotion-X_Versatile_Multimodal_Whole-Body_Motion_Generation.md|OmniMotion-X (arxiv_2025)]]、[[analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling.md|AnyMo (arxiv_2026)]] 把文本、语音、音乐、轨迹、参考 motion、对话等条件统一进一个模型或统一 token/latent 空间。它们的价值是工程整合和任务覆盖，尤其 [[analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling.md|AnyMo (arxiv_2026)]]/[[analysis/arxiv_2025/OmniMotion-X_Versatile_Multimodal_Whole-Body_Motion_Generation.md|OmniMotion-X (arxiv_2025)]] 这种大规模多模态数据路线说明“任意模态条件 motion generation”正在成为基础设施。[[analysis/arxiv_2025/Cross-Modal_Instructions_for_Robot_Motion_Generation.md|CrossInstruct (arxiv_2025)]] 虽然是机器人而非人体动画，也应作为旁证：它把 sketch/text 跨模态指令转成 3D robot trajectory，说明“用户用低成本跨模态符号表达运动意图”正在从 character animation 扩展到 embodied control。

但这里也有最大伪 gap：把多种条件拼到一个 transformer 不等于解决多模态控制。真正问题是不同条件冲突时谁优先、如何局部降权、如何把错误归因到某个模态或某个时间段。当前统一模型多数只证明“可以接很多输入”，没证明“会处理输入之间的矛盾”。

## 控制输入不是核心，控制仲裁才是核心

把这些工作放在一起，可以看到一个明确趋势：输入模态的扩展已经很快从 novelty 变成 commodity。

- text + trajectory 已有 [[analysis/ICLR_2024/OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation.md|OmniControl (ICLR_2024)]]、[[analysis/ECCV_2024/TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis.md|TLControl (ECCV_2024)]]、[[analysis/ICLR_2025/DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control.md|DART (ICLR_2025)]]、[[analysis/arxiv_2026/KV-Control_Parameter-Efficient_KV_Injection_for_Trajectory-Controlled_Text-to-Motion.md|KV-Control (arxiv_2026)]]、[[analysis/WHITEPAPER_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation.md|Kimodo (WHITEPAPER_2026)]]。
- sketch + trajectory 已有 [[analysis/SIGGRAPH_2025/Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation.md|Sketch2Anim (SIGGRAPH_2025)]]、[[analysis/CVPR_2026/Sketch2Colab.md|Sketch2Colab (CVPR_2026)]]、[[analysis/arxiv_2026/DrawMotion_Generating_3D_Human_Motions_by_Freehand_Drawing.md|DrawMotion (arxiv_2026)]]、[[analysis/CVPR_2025/StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman.md|StickMotion (CVPR_2025)]]。
- video / pose / arbitrary object 已有 [[analysis/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.md|PoseAnything (CVPR_2026)]]、[[analysis/arxiv_2026/AnyAct_Towards_Human_Reenactment_of_Character_Motion_From_Video.md|AnyAct (arxiv_2026)]]、[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl (SIGGRAPH_2024)]]、[[analysis/CVPR_2025/Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories.md|Motion Prompting (CVPR_2025)]]。
- multi-person 已有 [[analysis/NEURIPS_2024/InterControl_Zero_shot_Human_Interaction_Generation_by_Controlling_Every_Joint.md|InterControl (NEURIPS_2024)]]、[[analysis/ICLR_2025/InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Modelling.md|InterMask (ICLR_2025)]]、[[analysis/arxiv_2026/HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Motion_Generation.md|HINT (arxiv_2026)]]、[[analysis/arxiv_2025/DualFlow_Unified_Multi_Modal_Interactive_Reactive_3D_Motion_Generation_via_Rectified_Flow.md|DualFlow (arxiv_2025)]]、[[analysis/CVPR_2026/Sketch2Colab.md|Sketch2Colab (CVPR_2026)]]。
- real-time / streaming 已有 [[analysis/ICCV_2025/PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learning.md|PRIMAL (ICCV_2025)]]、[[analysis/ICLR_2025/DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control.md|DART (ICLR_2025)]]、[[analysis/ICCV_2025/MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space.md|MotionStreamer (ICCV_2025)]]、[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.md|PRISM (arxiv_2026)]]、[[analysis/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives.md|MotionBricks (SIGGRAPH_2026)]]、[[analysis/arxiv_2026/TextOp_Real_time_Interactive_Text_Driven_Humanoid_Robot_Motion_Generation_and_Control.md|TextOp (arxiv_2026)]]。
- any-modality / unified control 已有 [[analysis/AAAI_2025/MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Controls.md|MotionCraft (AAAI_2025)]]、[[analysis/ECCV_2024/MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts.md|MotionChain (ECCV_2024)]]、[[analysis/arxiv_2025/OmniMotion-X_Versatile_Multimodal_Whole-Body_Motion_Generation.md|OmniMotion-X (arxiv_2025)]]、[[analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling.md|AnyMo (arxiv_2026)]]。
- physics / embodied control 已有 [[analysis/arxiv_2025/FlexMotion_Lightweight_Physics-Aware_and_Controllable_Human_Motion_Generation.md|FlexMotion (arxiv_2025)]]、[[analysis/ICCV_2025/PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learning.md|PRIMAL (ICCV_2025)]]、[[analysis/arxiv_2025/Cross-Modal_Instructions_for_Robot_Motion_Generation.md|CrossInstruct (arxiv_2025)]]。

如果继续做“我也支持一种新条件”，风险很高。新增入库的 [[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]] 和 [[analysis/arxiv_2025/CoMPAS3D_A_Dataset_and_Benchmark_for_Interactive_Motion.md|CoMPAS3D (arxiv_2025)]] 也提示了一个修正：冲突仲裁和交互评价已经开始出现，不应再写成空白领域；更准确的 gap 是“已有 early solution，但还窄、还离线、还没有通用闭环”。更有价值的问题是：

1. **冲突检测**：系统能否知道文本说“慢走”但轨迹要求快速转向，或 sketch 要求接触但物理会穿模？
2. **局部仲裁**：[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]] 可以用二阶段 decoupling 处理 text + trajectory，但 sketch/video/physics/contact/person-pair 同时出现时，是改根轨迹、改手部姿态、改 timing，还是降低某个条件权重？
3. **闭环重规划**：用户中途修改输入后，系统是否能保留过去动作、修复未来片段，而不是整段重生成？
4. **交互评估**：FID/R-Precision 不够，必须测 latency、controllability、legibility、proficiency appropriateness、long-horizon drift。

[[analysis/arxiv_2025/CoMPAS3D_A_Dataset_and_Benchmark_for_Interactive_Motion.md|CoMPAS3D (arxiv_2025)]] 已经入库，价值在于把 interactive motion 的评价从传统 kinematic metrics 推到 move legibility 和 proficiency appropriateness；[[analysis/arxiv_2026/DrawMotion_Generating_3D_Human_Motions_by_Freehand_Drawing.md|DrawMotion (arxiv_2026)]] 的用户研究则补了“用户完成同一控制目标需要多少操作时间”的工作流指标。这个方向如果没有评价升级，很容易变成 demo paper。

## 真 gap 与伪 gap

### 伪 gap

**再加一个控制模态。**  
除非新模态能改变工作流，否则只是 adapter 论文。Draw/sketch/video/trajectory/audio/reference motion 都已经有人做，单纯“支持 X 输入”不够。

**多模态统一。**  
[[analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling.md|AnyMo (arxiv_2026)]]、[[analysis/arxiv_2025/OmniMotion-X_Versatile_Multimodal_Whole-Body_Motion_Generation.md|OmniMotion-X (arxiv_2025)]]、[[analysis/AAAI_2025/MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Controls.md|MotionCraft (AAAI_2025)]] 已经说明统一输入空间可行。[[analysis/arxiv_2025/MotionDuet_Dual-Conditioned_3D_Human_Motion_Generation_with_Video-Regularized_Text_Learning.md|MotionDuet (arxiv_2025)]] 也说明视频可以作为训练时分布先验来改善 text-only motion。没有冲突仲裁、局部诊断或 closed-loop user study 的统一模型，很难构成强贡献。

**实时推理加速。**  
[[analysis/ECCV_2024/MotionLCM_Real_time_Controllable_Motion_Generation_via_Latent_Consistency_Model.md|MotionLCM (ECCV_2024)]]、[[analysis/ICLR_2025/DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control.md|DART (ICLR_2025)]]、[[analysis/ICCV_2025/MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space.md|MotionStreamer (ICCV_2025)]]、[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.md|PRISM (arxiv_2026)]]、[[analysis/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives.md|MotionBricks (SIGGRAPH_2026)]] 都在做低延迟。只说“采样更快”不是交互；必须证明用户打断和环境变化下仍稳定。

**零样本跨角色/跨对象。**  
[[analysis/arxiv_2026/AnyAct_Towards_Human_Reenactment_of_Character_Motion_From_Video.md|AnyAct (arxiv_2026)]]、[[analysis/CVPR_2026/PoseAnything_General_Pose_guided_Video_Generation_with_Part_aware_Temporal_Coherence.md|PoseAnything (CVPR_2026)]]、[[analysis/SIGGRAPH_2025/AnyTop_Character_Animation_Diffusion_with_Any_Topology.md|AnyTop (SIGGRAPH_2025)]]、[[analysis/arxiv_2025/MoCapAnything_Unified_3D_Motion_Capture_for_Arbitrary_Skeletons_from_Monocular_Videos.md|MoCapAnything (arxiv_2025)]] 系列已经覆盖很多跨拓扑叙事。真正难的是没有稳定骨架/关键点时的 motion intent 抽取，而不是再做一次 retargeting。

### 真 gap

**异质控制信号冲突仲裁。**  
文本、轨迹、sketch、pose、接触、物理、多人关系会互相矛盾。[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]] 已经把 text + trajectory 冲突作为核心问题处理，这是一个重要修正：冲突仲裁不是空白，而是 emerging topic。剩余 gap 是通用性和闭环性：现有方案多是固定模态对、固定二阶段策略，缺少能在 body-part × time-window 上解释多源冲突、动态让步并触发局部修复的 arbiter。

**闭环交互而非快速离线生成。**  
用户持续输入、途中修改、环境扰动、多角色响应，是交互式 motion control 的本体。当前很多 interactive 仍是 prompt-to-sequence。

**长时稳定性与局部修复。**  
自回归/流式模型容易 drift；离线扩散模型重生成成本高。缺少“保留已执行历史 + 局部重规划未来”的通用机制。

**交互评价体系。**  
需要从 kinematic realism 转向 controllability、legibility、response latency、repair cost、user workload、proficiency appropriateness。[[analysis/arxiv_2025/CoMPAS3D_A_Dataset_and_Benchmark_for_Interactive_Motion.md|CoMPAS3D (arxiv_2025)]] 开了一个很好的头，但目前还偏 salsa/dance domain；[[analysis/arxiv_2026/DrawMotion_Generating_3D_Human_Motions_by_Freehand_Drawing.md|DrawMotion (arxiv_2026)]] 的操作时间指标更接近创作工具 UX，但还不是通用交互质量标准。

**跨域控制的 few-shot personalization。**  
[[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM (SIGGRAPH_2025)]] 零训练但不创造；生成模型能创造但需要配对数据。中间路线是：用户给几个自定义控制信号样例，系统学会该用户/项目的控制语义，并仍保持 motion prior。

## 一个可写成研究方向的聚焦

我建议把 idea 聚焦为：

**Closed-loop controllable motion generation with conflict-aware arbitration**

中文表述可以是：**面向交互式动作生成的控制冲突仲裁与闭环局部修复**。

### 核心假设

交互式 motion control 的主要失败，不是模型不会接收控制信号，而是多个控制信号在时间、身体部位和物理约束上发生冲突时，模型缺少通用机制判断“谁应该让步”。[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]] 证明了 text + trajectory 冲突可以通过解耦和修复缓解；[[analysis/arxiv_2026/KV-Control_Parameter-Efficient_KV_Injection_for_Trajectory-Controlled_Text-to-Motion.md|KV-Control (arxiv_2026)]] 证明了几何约束可以作为低参数 attention memory 精准注入；[[analysis/arxiv_2026/DrawMotion_Generating_3D_Human_Motions_by_Freehand_Drawing.md|DrawMotion (arxiv_2026)]] 证明了手绘控制确实降低用户表达成本。但这些仍没有合成一个通用闭环系统。如果把控制信号统一表示成可定位的约束单元，并用一个 arbiter 在 body part / joint / time window 上动态分配权重，再配合局部重采样或短窗口反应器，就能比直接拼接多模态条件更稳定、更可解释。

### 为什么不是伪 gap

已有工作分别解决了输入扩展、快速推理、轨迹跟随和多模态融合，[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]] 也已经把冲突本身作为 text + trajectory 的一等对象建模。因此新的切口不能只声称“我处理冲突”，而必须处理**跨模态、跨部位、跨时间窗口的可解释仲裁与闭环局部修复**。[[analysis/SIGGRAPH_2025/MAMM_Motion_Control_via_Metric_Aligning_Motion_Matching.md|MAMM (SIGGRAPH_2025)]] 绕过配对训练但不能创造；[[analysis/WHITEPAPER_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation.md|Kimodo (WHITEPAPER_2026)]]/[[analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling.md|AnyMo (arxiv_2026)]] 支持多条件但冲突解释弱；[[analysis/ICCV_2025/PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learning.md|PRIMAL (ICCV_2025)]] 实时反应但长期语义弱；[[analysis/CVPR_2026/Sketch2Colab.md|Sketch2Colab (CVPR_2026)]] 能量约束强但主要是离线协作生成；[[analysis/arxiv_2025/CoMPAS3D_A_Dataset_and_Benchmark_for_Interactive_Motion.md|CoMPAS3D (arxiv_2025)]] 提供交互评价启发但还不覆盖通用创作/游戏/机器人场景。冲突仲裁和闭环修复恰好在这些路线之间。

### 技术模块

**1. Constraint Unit Parser**  
把文本、sketch、轨迹、pose/video reference、接触/物理信号转成统一约束单元：

- 时间范围：start/end 或 sliding window。
- 身体范围：root、left hand、right hand、foot、whole body、person-pair。
- 约束类型：semantic、trajectory、keypose、contact、style、physics。
- 强度与可放松性：hard / soft / preference。

**2. Conflict Detector**  
在生成前和生成中检测冲突：

- 文本速度/方向与轨迹曲率冲突。
- sketch 接触点与双人骨架可达性冲突。
- pose/video reference 与人体拓扑或关节限制冲突。
- 物理接触与视觉/语义目标冲突。

最小实现可以不追求完美语义解析，而是用可微 surrogate：trajectory error、contact distance、joint limit violation、foot sliding、text-motion similarity delta。

**3. Arbitration Policy**  
输出 body-part × time-window 的控制权重，而不是一个全局 CFG scale：

- 哪些约束保留硬控。
- 哪些约束改成 soft guidance。
- 哪些部位用 motion prior 补全。
- 哪些窗口触发局部重采样。

实现上可以先从规则 + learned gate 做起，后续再接 RL/preference。

**4. Local Repair Sampler**  
不整段重生成，只修未来窗口或冲突窗口：

- 对已执行/已确认帧加 lock mask。
- 对冲突窗口做 masked diffusion / masked flow / token logits optimization。
- 对边界帧加 continuity loss，防止接缝断裂。

这个模块可以基于 [[analysis/ICCV_2025/MaskControl_Spatio_Temporal_Control_for_Masked_Motion_Synthesis.md|MaskControl (ICCV_2025)]]、[[analysis/ICLR_2025/DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control.md|DART (ICLR_2025)]]、[[analysis/ICCV_2025/MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space.md|MotionStreamer (ICCV_2025)]]、[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.md|PRISM (arxiv_2026)]] 或 [[analysis/WHITEPAPER_2026/Kimodo_Scaling_Controllable_Human_Motion_Generation.md|Kimodo (WHITEPAPER_2026)]] 的 latent/token 表示，不必从零训练大模型。

**5. Interaction Evaluation Suite**  
除了 FID/R-Precision，必须有：

- 控制成功率：轨迹/接触/keypose 满足率。
- 冲突恢复率：加入矛盾条件后能否局部让步并保持可用。
- 响应延迟：用户修改到可见修复的时间。
- 长时 drift：30-60 秒持续交互后的滑步、jerk、root drift。
- 可读性：第三方能否看出意图，类似 [[analysis/arxiv_2025/CoMPAS3D_A_Dataset_and_Benchmark_for_Interactive_Motion.md|CoMPAS3D (arxiv_2025)]] 的 legibility。
- 用户负担：达到目标需要几次修改/几笔 sketch/多少秒。

### 最小实验

不要一上来做全模态大一统。最小可行版本选两类最有代表性的冲突：

1. **Text + trajectory 冲突**：文本给风格/速度/动作类型，轨迹给根路径或手部路径。对比 [[analysis/ICLR_2024/OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation.md|OmniControl (ICLR_2024)]]、[[analysis/ECCV_2024/TLcontrol_Trajectory_and_Language_Control_for_Human_Motion_Synthesis.md|TLControl (ECCV_2024)]]、[[analysis/arxiv_2026/KV-Control_Parameter-Efficient_KV_Injection_for_Trajectory-Controlled_Text-to-Motion.md|KV-Control (arxiv_2026)]]、[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]]；核心不是赢正常样本，而是在 deliberately conflicting prompts 下同时降低轨迹误差、语义崩坏和 motion artifact。
2. **Sketch/contact + two-person 冲突**：用户画接触/交接草图，但轨迹或骨架可达性不完全一致。对比 [[analysis/CVPR_2026/Sketch2Colab.md|Sketch2Colab (CVPR_2026)]]、[[analysis/arxiv_2026/DrawMotion_Generating_3D_Human_Motions_by_Freehand_Drawing.md|DrawMotion (arxiv_2026)]]、[[analysis/NEURIPS_2024/InterControl_Zero_shot_Human_Interaction_Generation_by_Controlling_Every_Joint.md|InterControl (NEURIPS_2024)]]、[[analysis/ICLR_2025/InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Modelling.md|InterMask (ICLR_2025)]]；核心是把 sketch 噪声、接触不可达和两人动作错位转成可检测冲突，而不是整段重生成。
3. **物理/视频参考冲突作为延伸**：用 [[analysis/arxiv_2025/FlexMotion_Lightweight_Physics-Aware_and_Controllable_Human_Motion_Generation.md|FlexMotion (arxiv_2025)]]、[[analysis/ICCV_2025/PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learning.md|PRIMAL (ICCV_2025)]]、[[analysis/arxiv_2025/MEgoHand_Multimodal_Egocentric_Hand-Object_Interaction_Motion_Generation.md|MEgoHand (arxiv_2025)]]/[[analysis/arxiv_2026/AnyAct_Towards_Human_Reenactment_of_Character_Motion_From_Video.md|AnyAct (arxiv_2026)]] 风格输入构造“视觉参考看似合理但物理不可达”的案例，先作为分析集，不急着成为第一版主实验。

只要能证明仲裁器在冲突场景下显著降低“轨迹满足但动作僵硬”或“动作自然但控制失败”的 tradeoff，就有贡献。

### Reviewer 会攻击什么

- **“[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]] 已经做了冲突协调”**：必须承认 [[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]] 是强 baseline，并证明你的贡献不是 text + trajectory 的又一个二阶段方案，而是能扩展到 sketch/contact/video/physics 的通用局部仲裁。
- **“这只是多条件 weighting”**：必须证明权重是 body-part × time-window 局部、可解释、能响应冲突，而不是调几个 CFG scale。
- **“冲突场景是你人工构造的”**：需要从用户草图错误、轨迹噪声、视频 reference 不可达等真实交互噪声中构建 benchmark。
- **“没有新模型，只是系统拼装”**：SIGGRAPH/CHI/UIST 可以接受系统，但 CVPR/ICLR 需要更强的模型或学习机制。要把 arbitration policy 和 local repair sampler 做成核心算法，而不只是 pipeline。
- **“评估主观”**：主观 user study 必须配合自动指标，尤其 response latency、repair cost、constraint satisfaction。
- **“实时性不够”**：如果 local repair 超过几百毫秒，就不能叫 closed-loop，只能叫 iterative editing。

### 更激进的高上限分支

DeepSeek 讨论中提出的更高风险路线是：**物理、数据和人类三者在实时运动交互中的仲裁机制**。也就是用长期 diffusion planner、短窗口 physics-aware reactor 和 joint-level gating 做真实时交互角色控制。这个方向更接近 [[analysis/ICCV_2025/PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learning.md|PRIMAL (ICCV_2025)]] 的后续，但工程风险很高：要同时满足实时响应、物理稳定和运动表现力。它适合 SIGGRAPH/UIST 系统论文，不适合短期做成稳妥的 CVPR-style 增量。

我会把它作为上限方向，而不是当前最小切口。当前更稳的切口是：**先在可控生成模型里做 conflict-aware arbitration + local repair，再逐步引入物理 reactor**。

## 新候选入库状态

基于 web/arXiv 增强检索发现的 8 篇新候选已完成入库。BITE 分析链按 `job=4` 并行运行，结果目录为 `obsidian-vault/batches/motion_interactive_control_web_20260618/analysis/`，`summary.json` 记录 `done=8`、`failed=0`、`skipped=0`。对应 `paper_list.csv` 行已从 `Downloaded` 合并为 `checked`，本 note 的 `source_papers` 已补入全部 8 篇本地 analysis note。

本次新增外部入口：

- [KV-Control: Parameter-Efficient K/V Injection for Trajectory-Controlled Text-to-Motion](https://arxiv.org/abs/2606.05624)
- [DrawMotion: Generating 3D Human Motions by Freehand Drawing](https://arxiv.org/abs/2605.20955)
- [Coordinating Multiple Conditions for Trajectory-Controlled Human Motion Generation](https://arxiv.org/abs/2605.13729)
- [FlexMotion: Lightweight, Physics-Aware, and Controllable Human Motion Generation](https://arxiv.org/abs/2501.16778)
- [Salsa as a Nonverbal Embodied Language -- The CoMPAS3D Dataset and Benchmarks](https://arxiv.org/abs/2507.19684)
- [MEgoHand: Multimodal Egocentric Hand-Object Interaction Motion Generation](https://arxiv.org/abs/2505.16602)
- [Cross-Modal Instructions for Robot Motion Generation](https://arxiv.org/abs/2509.21107)
- [MotionDuet: Dual-Conditioned 3D Human Motion Generation with Video-Regularized Text Learning](https://arxiv.org/abs/2511.18209)

去重结论保持不变：[[analysis/arxiv_2026/TextOp_Real_time_Interactive_Text_Driven_Humanoid_Robot_Motion_Generation_and_Control.md|TextOp (arxiv_2026)]]、[[analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling.md|AnyMo (arxiv_2026)]]、[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.md|PRISM (arxiv_2026)]]、[[analysis/arxiv_2026/HINT_Hierarchical_Interaction_Modeling_for_Autoregressive_Multi_Human_Motion_Generation.md|HINT (arxiv_2026)]]、[[analysis/arxiv_2024/It_Takes_Two_Real_time_Co_Speech_Two_persons_Interaction_Generation_via_Reactive_Auto_regressive_Diffusion_Model.md|It Takes Two (arxiv_2024)]]、[[analysis/CVPR_2025/StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman.md|StickMotion (CVPR_2025)]]、[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md|Pulp Motion (arxiv_2025)]]、[[analysis/arxiv_2025/OmniMotion-X_Versatile_Multimodal_Whole-Body_Motion_Generation.md|OmniMotion-X (arxiv_2025)]] 等已经在本地库中有 analysis note 或 checked 记录，不应重复入库。

## 下一步

后续如果要推进成正式课题，优先把“最小实验”细化成可执行 benchmark：两类主冲突、[[analysis/arxiv_2026/Coordinating_Multiple_Conditions_for_Trajectory-Controlled_Human_Motion_Generation.md|CMC (arxiv_2026)]]/[[analysis/arxiv_2026/KV-Control_Parameter-Efficient_KV_Injection_for_Trajectory-Controlled_Text-to-Motion.md|KV-Control (arxiv_2026)]]/[[analysis/arxiv_2026/DrawMotion_Generating_3D_Human_Motions_by_Freehand_Drawing.md|DrawMotion (arxiv_2026)]]/[[analysis/CVPR_2026/Sketch2Colab.md|Sketch2Colab (CVPR_2026)]] 等强 baseline、自动指标和一个小规模用户 study protocol。
