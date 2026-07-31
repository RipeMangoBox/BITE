---
title: "Human-Camera-Video 现有工作分类归纳：从预训练泛化能力到真实工业痛点"
status: draft
created: 2026-06-30T20:26:48+0800
updated: 2026-07-01T14:49:01+0800
tags:
  - StoryMotion_Background
  - Human_Camera_Video
  - Motion_Generation
  - Camera_Control
  - Skeleton_Reconstruction
  - Motion_Understanding
  - next-work-ideation
  - target/ICLR
  - target/CVPR
  - target/SIGGRAPH
  - industrial-research
  - status/draft
aliases:
  - Human-Camera-Video taxonomy
hypothesis: |
  StoryMotion 的框架、任务设置和指标结果已经足以支撑 ICLR 投稿的基础，剩余工作主要是研究问题凝练、方法抽象和论文表述。本笔记不再为 StoryMotion 补工业包装，而是把 StoryMotion 视为前序基础，面向下一篇 human-camera-video 新工作做 bottom-up 分类归纳。新工作的关键问题是：如何把 generative、human motion、skeleton、retarget、video、multimodal、RL、agentic、physics、camera 等主流方向中的预训练泛化能力，迁移到更实用的结构化 human-camera-video 控制、理解、修复和评估任务中。
source_papers:
  - "[[analysis/SIGGRAPH_ASIA_2025/AnimaX_Animating_the_Inanimate_in_3D_with_Joint_Video_Pose_Diffusion_Models|AnimaX]]"
  - "[[analysis/SIGGRAPH_ASIA_2025/CamCloneMaster_Enabling_Reference_based_Camera_Control_for_Video_Generation|CamCloneMaster]]"
  - "[[analysis/arxiv_2026/CoMoVi_Co_Generation_of_3D_Human_Motions_and_Realistic_Videos|CoMoVi]]"
  - "[[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation|CameraCtrl]]"
  - "[[analysis/ICLR_2025/MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generation|MotionClone]]"
  - "[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]"
  - "[[analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion|Direct-a-Video]]"
  - "[[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation|MotionCanvas]]"
  - "[[analysis/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength|I2VControl-Camera]]"
  - "[[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation|ShotVerse]]"
  - "[[analysis/arxiv_2026/CT_1_Camera_Trajectory_Generation_for_Camera_Controlled_Video_Generation|CT-1]]"
  - "[[analysis/arxiv_2026/CamDirector_Camera_Trajectory_Control_for_Long_term_Video_Generation|CamDirector]]"
  - "[[analysis/CVPR_2026/BulletTime_Decoupled_Control_of_Time_and_Camera_Pose_for_Video_Generation|BulletTime]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]"
  - "[[analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling|AnyMo]]"
  - "[[analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]]"
  - "[[analysis/arxiv_2026/MoCapAnything_V2_End_to_End_Motion_Capture_for_Arbitrary_Skeletons|MoCapAnything V2]]"
  - "[[analysis/arxiv_2026/PALUM_Part_based_Attention_Learning_for_Unified_Motion_Retargeting|PALUM]]"
  - "[[analysis/TOG_2024/SKEL_Betweener_a_Neural_Motion_Rig_for_Interactive_Motion_Authoring|SKEL-Betweener]]"
  - "[[analysis/arxiv_2026/Reconstruction-Anchored_Diffusion_Model_for_Text-to-Motion_Generation|RAM]]"
  - "[[analysis/arxiv_2026/UniMo_Unified_Motion_Generation_and_Understanding_with_Chain_of_Thought|UniMo]]"
  - "[[analysis/CVPR_2026/LLaMo_Scaling_Pretrained_Language_Models_for_Unified_Motion_Understanding_and_Generation_with_Continuous_Autoregressive_Tokens|LLaMo]]"
  - "[[analysis/arxiv_2026/SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Rendering_and_MLLMs|SkeletonLLM]]"
  - "[[analysis/ICLR_2025/Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with_LLMs|Motion-Agent]]"
  - "[[analysis/arxiv_2026/MotionRFT_Unified_Reinforcement_Fine-Tuning_for_Text-to-Motion_Generation|MotionRFT]]"
  - "[[analysis/NEURIPS_2025/SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization|SoPo]]"
  - "[[analysis/arxiv_2026/PhysMoDPO_Physically-Plausible_Humanoid_Motion_with_Preference_Optimization|PhysMoDPO]]"
  - "[[analysis/ICLR_2025/MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions|MotionCritic]]"
  - "[[analysis/TOG_2024/MoConVQ_Unified_Physics_Based_Motion_Control_via_Scalable_Discrete_Representations|MoConVQ]]"
  - "[[analysis/SIGGRAPH_2024/SuperPADL_Scaling_Language_Directed_Physics_Based_Control_with_Progressive_Supervised_Distillation|SuperPADL]]"
  - "[[analysis/arxiv_2026/PhyGile_Physics_Prefix_Guided_Motion_Generation_for_Agile_General_Humanoid_Motion_Tracking|PhyGile]]"
  - "[[analysis/arxiv_2026/HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_Human_Videos|HumanX]]"
  - "[[analysis/arxiv_2026/HumanScore_Benchmarking_Human_Motions_in_Generated_Videos|HumanScore]]"
  - "[[analysis/CVPR_2026/What_Are_You_Doing_A_Closer_Look_at_Controllable_Human_Video_Generation|WYD]]"
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]"
  - "[[analysis/ICCV_2025/A_Unified_Model_for_Egocentric_Motion_Reconstruction_Forecasting_and_Generation|UniEgoMotion]]"
  - "[[analysis/CVPR_2026/EgoPoseFormer_v2_Accurate_Egocentric_Human_Motion_Estimation_for_ARVR|EgoPoseFormer v2]]"
  - "[[analysis/CVPR_2026/EgoControl_Controllable_Egocentric_Video_Generation_via_3D_Full_Body_Poses|EgoControl]]"
  - "[[analysis/CVPR_2026/EgoX_Egocentric_Video_Generation_from_a_Single_Exocentric_Video|EgoX]]"
  - "[[analysis/arxiv_2025/MEgoHand_Multimodal_Egocentric_Hand-Object_Interaction_Motion_Generation|MEgoHand]]"
related_notes:
  - "[[ideas/StoryMotion/2026-06-30_storymotion-industrial-qa-route|StoryMotion industrial brainstorm]]"
  - "[[ideas/StoryMotion/2026-06-29_storymotion-v6.2|StoryMotion v6.2]]"
---

## 与 StoryMotion 的关系

StoryMotion 当前更适合作为 ICLR 论文基础：它的问题设置、统一框架、joint 指标优势和 camera/human completion 诊断可以支撑一篇学术论文。后续对 StoryMotion 的重点应是收敛研究问题、抽象方法贡献、明确指标边界和修正文稿表述。

这份笔记讨论的是 **下一篇新工作**。它可以继承 StoryMotion 的 human-camera joint modeling 经验，也可以复用 StoryMotion 的数据、生成结果、metric 和 failure diagnosis，但目标不必服务于 StoryMotion 本身。更准确的定位是：从 StoryMotion 往外跨到 **human-camera-video**，提高实用性，并与预训练视频模型、MLLM、motion understanding、camera control、skeleton/retarget、physics/reward 等主流方向接轨。

## 潜在投稿目标

下一篇工作可以同时瞄准 ICLR、CVPR、SIGGRAPH/SIGGRAPH Asia，但三类 venue 对“好问题”的偏好不同，因此 idea 不能只按一个会议口味收敛。

| 目标 venue | 更看重的问题形态 | 方法贡献需要长什么样 | 风险 |
| --- | --- | --- | --- |
| ICLR | 表示学习、后训练、统一建模、泛化机制 | 清晰抽象的能力迁移机制，例如 video prior 到 structured motion/camera 的接口，或 reward/post-training 统一框架 | 若工业任务太具体，可能被认为只是应用系统 |
| CVPR | 视觉生成、视频理解、human video、可控生成、benchmark | 可见的视觉结果、强 baseline、可复现评测，最好连接 video diffusion 或 MLLM | 若只停留在 3D motion 指标，可能不够视觉主流 |
| SIGGRAPH / SIGGRAPH Asia | 动画、相机、角色控制、authoring、生产可用性 | 真实创作痛点、可编辑接口、资产可用、camera/human coordination、用户或工作流价值 | 若只有指标提升、没有可用性叙事，会显得不够图形学 |

因此新 idea 的最低要求是：既要有 ICLR 式可抽象机制，又要有 CVPR 式 human-video/video-prior 连接，还要保留 SIG 式可控、可编辑、可导出的生产价值。StoryMotion 可以提供起点，但不能成为边界。

更具体地说，下一篇工作不应先问“投哪个会”，而应先检查它是否满足对应 venue 的最低证据门槛：

| 目标 venue | 最小可接受证据 | 更适合的方向形态 | 不适合的方向形态 |
| --- | --- | --- | --- |
| ICLR | 形式化问题定义、可复用的能力迁移机制、清楚的 ablation 和失败分析 | compositional conditioning、post-training、video prior 到 structured motion/camera 的接口抽象 | 只展示工具效果，缺少机制解释 |
| CVPR | 明确任务定义、公开数据或可复现实验、强 baseline、可见的视频/重建结果 | human-camera-video control、monocular human-camera reconstruction、human video 结构化诊断 | 只在 3D motion 指标上小幅提升，缺少视觉侧连接 |
| SIGGRAPH / SIGGRAPH Asia | 高质量 demo、可编辑接口、可导出资产、创作流程价值 | camera-aware animation authoring、reference-based camera/motion control、retarget/export/repair 工具链 | 只有自动指标，没有 artist/user workflow 叙事 |

在 4 卡 5090、无需大规模数据构建的限制下，优先级最高的不是“训练更大的模型”，而是下面三类可验证问题：

1. **解耦式 human-camera 条件接口**：用现有 motion/camera 数据和预训练视频模型，研究 skeleton、camera trajectory、screen-space trajectory、motion strength 等条件如何组合、冲突和解耦。ICLR 价值在接口和组合泛化机制，CVPR 价值在可控视频/重建结果，SIG 价值在可编辑镜头工具。
2. **video prior 作为 human-camera 逆问题约束**：把预训练视频模型、MLLM 或 learned critic 作为测试时优化/后训练信号，服务 monocular reconstruction、camera completion、motion repair、badcase ranking。CVPR 更自然，ICLR 需要把它抽象成 inverse problem 或 preference extraction。
3. **结构化诊断和修复闭环**：从生成视频中恢复 skeleton/motion/camera，诊断 biomechanics、framing、occlusion、shot continuity，再用轻量 refiner 或 DPO/RFT 修复。它不一定最炫，但很贴近工业可用：能评估、能定位、能修复。

应明确暂时丢弃的方向：

- 大规模 human-camera-video 数据集构建或端到端视频模型重训练。
- 纯 prompt engineering 的 zero-shot demo。
- 全栈物理仿真 + RL + 视频生成闭环。
- 只做单目 3D 重建、且不接入 video prior / camera control / motion repair 的路线。
- 只追求 StoryMotion 指标续涨，而没有新任务接口或新能力定义的路线。

这份笔记不按关键词机械分类。`generative`、`human`、`motion`、`skeleton`、`retarget`、`video`、`multimodal`、`RL`、`agentic`、`physics`、`camera` 都是检索入口，但真正有用的分类轴是：

- **能力从哪里来**：自有 motion 数据、预训练视频模型、LLM/MLLM、物理控制器、reward/critic、几何重建模块。
- **能力要解决什么**：通用泛化、精确控制、资产可用、物理可执行、语义理解、多镜头叙事、生成结果修复。
- **能力如何被注入**：adapter/LoRA、attention injection、joint diffusion、reference conditioning、reward fine-tuning、post-training、planner-controller decomposition。
- **工业痛点在哪里**：用户不会手写轨迹，生成结果不可控，不可导出，不可修，不可评估，不能跨骨骼/跨视频/跨镜头稳定复用。

因此下面的分类是“能力获取范式”，不是关键词分类。

## 总览分类

| 能力范式                      | 代表工作                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 研究动机                        | 目标能力                                                           | 对下一篇工作的启发                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------- |
| 预训练视频模型迁移                 | [AnimaX(SIGGRAPH_ASIA_2025)](analysis/SIGGRAPH_ASIA_2025/AnimaX_Animating_the_Inanimate_in_3D_with_Joint_Video_Pose_Diffusion_Models.md), [CoMoVi(arxiv_2026)](analysis/arxiv_2026/CoMoVi_Co_Generation_of_3D_Human_Motions_and_Realistic_Videos.md), [CamCloneMaster(SIGGRAPH_ASIA_2025)](analysis/SIGGRAPH_ASIA_2025/CamCloneMaster_Enabling_Reference_based_Camera_Control_for_Video_Generation.md), [MotionClone(ICLR_2025)](analysis/ICLR_2025/MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generation.md)                                                                                                                                                         | 专用 motion 数据不足，视频模型已有丰富时空先验 | 类别泛化、参考运动克隆、视频和3D运动协同                                          | 不要只做小型 motion 模型，可把视频先验作为 human-camera-video 的泛化来源          |
| 显式相机与运动解耦                 | [MotionCtrl(SIGGRAPH_2024)](analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md), [Direct-a-Video(SIGGRAPH_2024)](analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion.md), [CameraCtrl(ICLR_2025)](analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md), [I2VControl-Camera(ICLR_2025)](analysis/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength.md), [MotionCanvas(SIGGRAPH_2025)](analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.md) | 文本无法精确表达相机和主体运动             | 相机、主体、屏幕轨迹、运动强度独立控制                                            | camera-human coupling 应成为可控对象，而非隐式副产品                       |
| 电影级多镜头规划                  | [ShotVerse(arxiv_2026)](analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation.md), [CT-1(arxiv_2026)](analysis/arxiv_2026/CT_1_Camera_Trajectory_Generation_for_Camera_Controlled_Video_Generation.md), [CamDirector(arxiv_2026)](analysis/arxiv_2026/CamDirector_Camera_Trajectory_Control_for_Long_term_Video_Generation.md), [BulletTime(CVPR_2026)](analysis/CVPR_2026/BulletTime_Decoupled_Control_of_Time_and_Camera_Pose_for_Video_Generation.md)                                                                                                                                                                              | 用户不会手写复杂镜头轨迹，长视频和多镜头缺一致性    | 自动轨迹规划、长程相机控制、世界时间与相机解耦                                        | human-camera 不只是单段补全，还应考虑 shot-level 规划和连续性                 |
| 骨骼和资产可用表示                 | [PRISM(arxiv_2026)](analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.md), [MoCapAnything V2(arxiv_2026)](analysis/arxiv_2026/MoCapAnything_V2_End_to_End_Motion_Capture_for_Arbitrary_Skeletons.md), [PALUM(arxiv_2026)](analysis/arxiv_2026/PALUM_Part_based_Attention_Learning_for_Unified_Motion_Retargeting.md), [SKEL-Betweener(TOG_2024)](analysis/TOG_2024/SKEL_Betweener_a_Neural_Motion_Rig_for_Interactive_Motion_Authoring.md)                                                                                                                                                                                                   | joint 坐标好看不等于动画资产可用         | 任意骨骼、重定向、旋转恢复、稀疏关键帧补间                                          | 新工作若不能稳定转 skeleton/rotation/retarget，工业价值有限                 |
| 运动理解和多模态推理                | [UniMo(arxiv_2026)](analysis/arxiv_2026/UniMo_Unified_Motion_Generation_and_Understanding_with_Chain_of_Thought.md), [LLaMo(CVPR_2026)](analysis/CVPR_2026/LLaMo_Scaling_Pretrained_Language_Models_for_Unified_Motion_Understanding_and_Generation_with_Continuous_Autoregressive_Tokens.md), [SkeletonLLM(arxiv_2026)](analysis/arxiv_2026/SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Rendering_and_MLLMs.md), [Motion-Agent(ICLR_2025)](analysis/ICLR_2025/Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with_LLMs.md)                                                                                                                       | 文本和运动粒度不匹配，模型缺动作阶段理解        | 生成和理解统一、CoT、对话式编辑、跨格式 skeleton understanding                   | understanding 应服务 control、repair、attribution，而不是单独做 caption |
| RL和偏好后训练                  | [MotionRFT(arxiv_2026)](analysis/arxiv_2026/MotionRFT_Unified_Reinforcement_Fine-Tuning_for_Text-to-Motion_Generation.md), [SoPo(NEURIPS_2025)](analysis/NEURIPS_2025/SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization.md), [MotionCritic(ICLR_2025)](analysis/ICLR_2025/MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions.md), [PhysMoDPO(arxiv_2026)](analysis/arxiv_2026/PhysMoDPO_Physically-Plausible_Humanoid_Motion_with_Preference_Optimization.md)                                                                                                                                                                                     | 监督损失和自动指标不等于人类偏好或物理可行       | reward tuning、preference optimization、critic-guided generation | 4卡资源下更适合做 post-training，而不是大规模重训                            |
| 物理执行闭环                    | [MoConVQ(TOG_2024)](analysis/TOG_2024/MoConVQ_Unified_Physics_Based_Motion_Control_via_Scalable_Discrete_Representations.md), [SuperPADL(SIGGRAPH_2024)](analysis/SIGGRAPH_2024/SuperPADL_Scaling_Language_Directed_Physics_Based_Control_with_Progressive_Supervised_Distillation.md), [PhyGile(arxiv_2026)](analysis/arxiv_2026/PhyGile_Physics_Prefix_Guided_Motion_Generation_for_Agile_General_Humanoid_Motion_Tracking.md), [HumanX(arxiv_2026)](analysis/arxiv_2026/HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_Human_Videos.md)                                                                                                                         | 运动学生成在仿真或机器人上不可执行           | 物理可行、可跟踪、可交互、从视频到技能                                            | 不必把 physics 做成主任务，但应把物理/接触作为高价值约束和评价                        |
| Human video 诊断和 benchmark | [HumanScore(arxiv_2026)](analysis/arxiv_2026/HumanScore_Benchmarking_Human_Motions_in_Generated_Videos.md), [WYD(CVPR_2026)](analysis/CVPR_2026/What_Are_You_Doing_A_Closer_Look_at_Controllable_Human_Video_Generation.md), [CoMoVi(arxiv_2026)](analysis/arxiv_2026/CoMoVi_Co_Generation_of_3D_Human_Motions_and_Realistic_Videos.md)                                                                                                                                                                                                                                                                                                                                                    | 视频视觉质量提升后，人体运动错误更隐蔽         | 生物力学评分、人类视频细粒度失败诊断                                             | human-camera-video 需要检测 motion 是否真实，而不是只看视频观感               |

## 0.1 Camera movement understanding & generation 是否已被覆盖

结论：**camera generation/control 已经很密，camera movement understanding 正在快速变热，但 Motion-Agent 式的“camera movement understanding + generation + editing”统一框架仍没有被完全覆盖；human-camera unified generation & understanding 仍有空位，但不能写成“首个 camera unified model”。**

现有覆盖大致分成三组。

第一组是 **camera control / generation**。这条线已经非常拥挤：[CameraCtrl(ICLR_2025)](analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md) 用 Plücker embedding 做相机条件注入，[I2VControl-Camera(ICLR_2025)](analysis/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength.md) 把相机刚性运动和主体动态强度拆开，[CamCloneMaster(SIGGRAPH_ASIA_2025)](analysis/SIGGRAPH_ASIA_2025/CamCloneMaster_Enabling_Reference_based_Camera_Control_for_Video_Generation.md) 把相机控制接口变成 reference video，[MotionCanvas(SIGGRAPH_2025)](analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.md) 把 3D 创作意图转成 2D 控制信号，[GEN3C(CVPR_2025)](analysis/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.md) 用显式 3D cache 保证相机控制与世界一致性，[OmniCam(arxiv_2025)](analysis/arxiv_2025/OmniCam_Unified_Multimodal_Camera_Control_for_Video_Generation.md) 进一步统一多种 camera control 输入，[ActCam(SIGGRAPH_2026)](analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation.md) 则在冻结视频模型上做零样本 joint camera + 3D motion control。这说明“再做一个 camera-conditioned video generation”很难形成新论文主线。

第二组是 **camera movement understanding / benchmark**。Web 补强显示，[CameraBench(NeurIPS_2025)](https://arxiv.org/abs/2504.15376) 已经把 camera motion understanding 定义为一个专家标注 benchmark，区分几何 primitive 和语义 primitive；[CineTechBench(arxiv_2025)](https://arxiv.org/abs/2505.15145) 同时评估 cinematographic technique understanding 和 generation，覆盖 shot scale、shot angle、composition、camera movement、lighting、color、focal length；[Geometry-Guided Camera Motion Understanding in VideoLLMs(CVPRW_2026)](https://openaccess.thecvf.com/content/CVPR2026W/PVUW/html/Feng_Geometry-Guided_Camera_Motion_Understanding_in_VideoLLMs_CVPRW_2026_paper.html) 明确指出 VideoLLM 缺少 camera motion 显式表示；[CamReasoner(arxiv_2026)](https://arxiv.org/abs/2602.00181) 用 Observation-Thinking-Answer 和 RL 训练 camera movement spatial reasoning。这些工作说明“理解相机运动”已是明确赛道，不是空白。

第三组是 **camera-centric unified multimodal model**。最接近的是 [Thinking with Camera(ICLR_2026)](https://arxiv.org/abs/2510.08673)：它把 camera 当作 language，统一 camera-centric understanding 和 generation，并用大规模 vision-language-camera triplets 训练 Puffin。这已经覆盖了“camera understanding + generation 统一”的宏观 claim。因此下一篇不能声称“首次统一 camera understanding and generation”。

更合理的空位是：**把 camera movement 从纯视觉/摄影术对象，推进到 human motion 绑定的结构化 token：同时支持 camera captioning / camera QA / camera generation / human-aware camera editing / failure diagnosis。** 这更像 [Motion-Agent(ICLR_2025)](analysis/ICLR_2025/Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with_LLMs.md) 和 [LLaMo(CVPR_2026)](analysis/CVPR_2026/LLaMo_Scaling_Pretrained_Language_Models_for_Unified_Motion_Understanding_and_Generation_with_Continuous_Autoregressive_Tokens.md) 在 human motion 上做的事情，但对象从 `motion token` 扩展为 `human token + camera token + shot token`。

可写成下一篇候选问题：

```text
Can a lightweight motion-aware language/agent framework unify
human motion understanding, camera movement understanding,
human-camera generation, and camera-aware refinement
without large-scale retraining?
```

这个方向的边界也要清楚：

- 不做通用 camera-centric MLLM，因为 [Thinking with Camera(arxiv_2025)](https://arxiv.org/abs/2510.08673) 已经走大模型和大数据路线。
- 不做单纯 camera control，因为 [CameraCtrl(ICLR_2025)](analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md)、[GEN3C(CVPR_2025)](analysis/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.md)、[ActCam(SIGGRAPH_2026)](analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation.md) 已经把 control 精度推得很远。
- 不做大规模 camera annotation；更可行的是利用 Pulp/StoryMotion 结构化数据、CameraBench/CineTechBench 的 taxonomy、公开视频模型输出和已有 metrics 构造小规模 instruction / preference / diagnosis 数据。
- 核心贡献应是 **human-camera token/interface + interleaved understand-generate-refine loop**，而不是“相机轨迹生成器指标更高”。

## 0.2 Ego-view motion reconstruction & generation 是否值得切入

结论：**ego 视角 motion recon/generation 是真实需求且是热门方向，但已经有明显赛道宽度和强工作；不建议作为下一篇主线，除非切入口收窄到 human-camera coupling 的特殊问题。**

它的真实需求很明确：AR/VR、智能眼镜、第一人称交互、远程临场、运动指导、机器人从人类第一人称示范中学习，都需要从头戴相机和稀疏传感器恢复或生成全身运动。本地 KB 和 web 都显示 2025 之后这条线增长很快。

[Ego4o(CVPR_2025)](https://arxiv.org/abs/2504.08449) 做 multi-modal egocentric motion capture and understanding，把 ego image、1-3 个 IMU、motion description 编到 motion VQ-VAE latent，支持部分输入并可生成 motion descriptions。[UniEgoMotion(ICCV_2025)](analysis/ICCV_2025/A_Unified_Model_for_Egocentric_Motion_Reconstruction_Forecasting_and_Generation.md) 更直接：一个统一 conditional diffusion model 同时做 egocentric reconstruction、forecasting、generation，并提出 head-centric representation 与 EE4D-Motion。[EgoPriMo(arxiv_2026)](https://arxiv.org/abs/2606.08495) 进一步把 ego observation + text prompt 转成 SMPL full-body motion prior，用于 humanoid control。[EgoPoseFormer v2(CVPR_2026)](analysis/CVPR_2026/EgoPoseFormer_v2_Accurate_Egocentric_Human_Motion_Estimation_for_ARVR.md) 在 AR/VR egocentric motion estimation 上强调实时、半监督和高精度。[EgoControl(CVPR_2026)](analysis/CVPR_2026/EgoControl_Controllable_Egocentric_Video_Generation_via_3D_Full_Body_Poses.md)、[EgoX(CVPR_2026)](analysis/CVPR_2026/EgoX_Egocentric_Video_Generation_from_a_Single_Exocentric_Video.md)、[MEgoHand(arxiv_2025)](analysis/arxiv_2025/MEgoHand_Multimodal_Egocentric_Hand-Object_Interaction_Motion_Generation.md) 则说明 ego video generation、exo-to-ego、hand-object motion generation 都在快速扩展。

因此，ego 方向不是“不真实”，而是**过于真实以至于竞争很强**。如果直接做 “egocentric motion reconstruction/generation”，会遇到三个问题：

- 数据依赖强：EgoExo4D、Nymeria、EgoBody3M、HOI 数据和设备设置差异很大，独立 4 卡难以系统追赶。
- baseline 强：UniEgoMotion 已经统一 reconstruction / forecasting / generation，Ego4o 已经统一 capture / understanding，EgoPriMo 又把 humanoid control 接上。
- 和 StoryMotion 的差异不自然：ego camera 是佩戴者头部相机，StoryMotion/cinematic camera 是外部叙事镜头；二者都包含 camera + motion，但相机语义不同。

可保留的窄切口：

1. **ego 作为 human-camera coupling 的极端测试集**：把 head-mounted camera 看成最强耦合相机，研究相机噪声、头部运动和全身 motion reconstruction/generation 的可靠性边界。
2. **ego-to-cinematic retarget**：从 first-person demonstration 恢复 human motion，再生成 third-person cinematic camera；这比直接做 ego reconstruction 更贴近 StoryMotion/human-camera-video。
3. **camera source-aware motion representation**：统一 external cinematic camera、head-mounted ego camera、generated camera 三类 source，研究同一 human motion 在不同 camera source 下的表示和可靠性。
4. **ego badcase evaluator**：利用 ego 方向的 head-centric representation 和 scene contact 约束，为 human-camera-video 生成结果提供物理/可见性诊断。

优先级判断：**ego 不应作为下一篇主线；可以作为 stress test、应用章节或一个 future direction。** 若要主攻 ego，必须找到比 UniEgoMotion/Ego4o/EgoPriMo 更窄且更锋利的 claim，例如“从 ego demonstration 到 cinematic human-camera authoring”，而不是“统一 ego motion recon/gen”。

## 1. 预训练视频模型迁移：从专用 motion 数据到泛化时空先验

这是一条非常重要的主线。它的共同判断是：专用 3D motion 数据、camera 数据、skeleton 数据都太窄，而大规模视频模型已经学到了丰富的时空动态、物体运动、相机运动和视觉语义。研究的关键不再是从零训练一个更大的 motion model，而是设计一个能把视频先验“接入”结构化 motion/camera 表示的接口。

[AnimaX(SIGGRAPH_ASIA_2025)](analysis/SIGGRAPH_ASIA_2025/AnimaX_Animating_the_Inanimate_in_3D_with_Joint_Video_Pose_Diffusion_Models.md) 的做法很典型：它不直接在稀疏姿态图上训练一个孤立姿态扩散模型，而是把 3D 动画问题转成多视图视频和姿态的联合扩散，用共享位置编码把视频模型中的运动先验迁移到低自由度骨架动画。它的目标能力是类别无关 3D 动画生成，而不是人类专用动作生成。局限也很清楚：固定相机、短视频、训练集仍偏人形。

[CoMoVi(arxiv_2026)](analysis/arxiv_2026/CoMoVi_Co_Generation_of_3D_Human_Motions_and_Realistic_Videos.md) 更直接地说明 human motion 和 video 不是两条独立链路。它把 3D 人体运动编码成 2D motion representation，并在预训练视频扩散模型上做双分支协同生成。这里的目标不是“生成视频后再估 motion”或“生成 motion 后再驱动视频”，而是在同一去噪循环内让运动提供结构先验、视频模型提供泛化先验。

[CamCloneMaster(SIGGRAPH_ASIA_2025)](analysis/SIGGRAPH_ASIA_2025/CamCloneMaster_Enabling_Reference_based_Camera_Control_for_Video_Generation.md) 把相机控制从显式参数转为参考视频 latent：用户不需要相机参数，模型直接从参考视频中克隆相机运动。它的关键不是 camera parameter 更准，而是用户接口从“写轨迹”变成“给参考”。这对工业很重要，因为真实创作者更容易找参考镜头，而不是手写 SE(3) 序列。

[MotionClone(ICLR_2025)](analysis/ICLR_2025/MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generation.md) 则是免训练方向：从预训练视频模型的时序注意力中抽取主导运动成分，用稀疏注意力对齐实现 motion cloning。它说明预训练模型内部已有可用的运动表征，只是需要从噪声注意力中分离出来。

对下一篇工作的启发：如果只在现有 human-camera 数据上训练一个小模型，泛化上限很可能受数据限制。更有潜力的问题是：**能否把预训练视频模型的运动/相机/视觉泛化能力，迁移到结构化 human-camera motion 表示上，同时保留 skeleton 和 camera 的可控性**。

## 2. 显式相机与运动解耦：从“视频动了”到“哪个实体以什么方式动”

这一类工作都在反对一个隐式假设：视频中的 motion 可以用一个统一的运动条件表达。实际不是这样。相机运动是全局视角变化，主体运动是局部动态，human root 是角色位移，skeleton 是关节结构，screen trajectory 是画面空间控制，camera trajectory 是三维观察者运动。

[MotionCtrl(SIGGRAPH_2024)](analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md) 把相机姿态序列注入时序 Transformer，把物体轨迹特征注入空间卷积层。它的动机是相机运动和物体运动的物理属性不同，因此控制信号应进入不同模型部位。

[Direct-a-Video(SIGGRAPH_2024)](analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion.md) 进一步把相机控制和物体控制拆成训练阶段和推理阶段两个模块：相机通过自监督裁剪/缩放增强学习，物体通过空间交叉注意力调制控制。它的工业意义是少依赖昂贵标注。

[CameraCtrl(ICLR_2025)](analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md) 说明相机表示本身很关键。原始外参矩阵太抽象，Plücker 嵌入提供逐像素几何解释，且相机条件更适合注入时间注意力。

[I2VControl-Camera(ICLR_2025)](analysis/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength.md) 提供了更值得下一篇工作吸收的思想：把相机刚性运动和主体动态分解，分别用稠密点轨迹和 motion strength 控制。这意味着 camera control 不应只输出一条轨迹，还应允许用户调节主体运动强度、跟随强度和镜头强度。

[MotionCanvas(SIGGRAPH_2025)](analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.md) 则解决用户意图和模型条件之间的空间鸿沟：用户在 3D 场景空间中思考，视频模型在 2D 屏幕空间中训练。它用 Motion Signal Translation 把 3D 意图转成 2D 控制信号，规避 3D 标注依赖。

对下一篇工作的启发：human-camera coupling 不能只作为 unified framework 的优势来讲。更真实的问题是：**哪些运动应该耦合，哪些必须解耦；何时 camera 应跟随 human，何时 camera 应忽略 noisy/generated human；如何给用户可调的 follow/framing/motion strength**。

## 3. 电影级多镜头规划：从单段相机补全到 shot-level control

这类工作把相机控制从“逐帧轨迹生成”推到“镜头语言和多镜头结构”。工业视频创作中，用户不只是要一条相机轨迹，而是要 shot type、运动节奏、主体强调、镜头切换和长程一致性。

[ShotVerse(arxiv_2026)](analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation.md) 的核心是 plan-then-control。它把任务拆成 `P(Trajectory | Caption)` 和 `P(Video | Caption, Trajectory)`，先从文本规划电影级轨迹，再让视频生成器执行轨迹。它说明“相机控制”本身也可分为 planner 和 controller 两层。

[CT-1(arxiv_2026)](analysis/arxiv_2026/CT_1_Camera_Trajectory_Generation_for_Camera_Controlled_Video_Generation.md) 把相机轨迹生成独立出来，作为视觉-语言-相机条件分布建模任务。它的目标不是直接生成视频，而是从图像和文本意图推理平滑、场景感知的相机轨迹。

[CamDirector(arxiv_2026)](analysis/arxiv_2026/CamDirector_Camera_Trajectory_Control_for_Long_term_Video_Generation.md) 关注长视频 trajectory editing。它说明长程相机控制需要世界缓存、历史引导和自回归一致性，而不是短片段独立生成。

[BulletTime(CVPR_2026)](analysis/CVPR_2026/BulletTime_Decoupled_Control_of_Time_and_Camera_Pose_for_Video_Generation.md) 把世界时间和相机姿态解耦。这个问题对下一篇 human-camera-video 工作很关键：human motion 的时间进度、camera 的时间采样、镜头运动速度不是同一件事。当前很多 human-camera 任务默认单一时间轴，会限制子弹时间、慢动作、freeze-frame、环绕拍摄等能力。

[Towards Storytelling Animations(CVPR_2026)](analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md) 直接把角色和相机作为多实体联合生成对象，动机是分离生成角色和相机会导致构图失衡、主体脱框和叙事不连贯。它说明 human-camera 联合建模的问题定义是成立的，但也暴露出下一步必须处理 shot-level 结构和控制接口。

对下一篇工作的启发：camera completion 只是最低层任务。更贴近工业的问题是：**给定故事/动作阶段/参考镜头，自动规划并执行 human-aware camera shot sequence，而不是只补全一段 camera trajectory**。

## 4. 骨骼、重建和重定向：从 benchmark joint 到 animation-ready motion

这类工作提醒一个容易被忽略的工业事实：joint coordinate 指标好，不等于可用于动画资产。真实生产要处理 rotation、骨长、局部坐标轴、不同 skeleton 拓扑、IK、retarget、streaming 和 sparse keyframe editing。

[PRISM(arxiv_2026)](analysis/arxiv_2026/PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition.md) 的关键是 per-joint latent decomposition。它认为每帧单向量 latent 会把 root、trajectory、joint rotation 缠在一起，浪费模型容量。它的目标是流式生成、姿态条件生成和文本到动作统一，靠的是时间乘关节的结构化 latent grid。

[MoCapAnything V2(arxiv_2026)](analysis/arxiv_2026/MoCapAnything_V2_End_to_End_Motion_Capture_for_Arbitrary_Skeletons.md) 的核心问题是 pose-to-rotation 的病态性。相同 3D joint position 在不同 rest pose 和局部坐标轴下可以对应不同 rotation。它用 reference pose-rotation pair 锚定局部坐标系，使任意骨骼动捕变成可学习端到端任务。这对下一篇工作很关键：如果输出只在 joint position 空间可用，后续导出到资产骨骼会遇到旋转恢复和坐标系问题。

[PALUM(arxiv_2026)](analysis/arxiv_2026/PALUM_Part_based_Attention_Learning_for_Unified_Motion_Retargeting.md) 把 retarget 的关键放在 part-based attention 和共享连接关节上，目标是跨拓扑骨骼重定向，不靠手工关节对应。它的动机来自工业角色骨骼的多样性。

[SKEL-Betweener(TOG_2024)](analysis/TOG_2024/SKEL_Betweener_a_Neural_Motion_Rig_for_Interactive_Motion_Authoring.md) 代表可编辑 authoring 需求：动画师给少量关键帧或关节约束，模型需要补全中间运动。它不是泛化生成，而是把神经模型接到 Maya/Blender 式工作流。

[RAM(arxiv_2026)](analysis/arxiv_2026/Reconstruction-Anchored_Diffusion_Model_for_Text-to-Motion_Generation.md) 则说明 reconstruction branch 可以成为 motion latent manifold 的锚点，不只是预训练 autoencoder。它启发下一篇工作用 reconstruction consistency 限制生成偏离 skeleton/camera/video manifold。

对下一篇工作的启发：**如果只报告 joint/camera 指标，不解决 skeleton representation、rotation recovery、retarget 和 sparse editing，新工作很难成为工业可用 motion 系统**。

## 5. Motion understanding 和多模态推理：从 caption 到可操作语义

这一类工作不是简单做 motion captioning，而是在尝试把 motion 变成能被 LLM/MLLM 理解、规划、编辑和评价的对象。

[UniMo(arxiv_2026)](analysis/arxiv_2026/UniMo_Unified_Motion_Generation_and_Understanding_with_Chain_of_Thought.md) 把运动渲染成视频，用 VLM 生成 motion-consistent CoT，再用 GRPO 做组级优化。它的目标是把 T2M 和 M2T 统一，并缓解文本-运动语义鸿沟。需要注意的是，它在 FID 上并非绝对强项，说明 understanding 和低层运动保真仍有张力。

[LLaMo(CVPR_2026)](analysis/CVPR_2026/LLaMo_Scaling_Pretrained_Language_Models_for_Unified_Motion_Understanding_and_Generation_with_Continuous_Autoregressive_Tokens.md) 关注两个瓶颈：离散量化带来的运动抖动，以及直接微调 LLM 导致语言能力遗忘。它用连续因果 VAE 和 MoT 分离语言/运动参数，目标是统一理解和生成，同时保留 LLM 泛化能力。

[SkeletonLLM(arxiv_2026)](analysis/arxiv_2026/SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Rendering_and_MLLMs.md) 的启发是：不要强迫 MLLM 直接吃 skeleton 坐标，而是把骨架序列可微渲染成 MLLM 原生视觉模态，解决跨 skeleton 格式和语义鸿沟。它说明 skeleton understanding 可以通过“翻译成预训练模型母语”实现。

[Motion-Agent(ICLR_2025)](analysis/ICLR_2025/Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with_LLMs.md) 展示了 agentic 编排：GPT-4 做高层计划，MotionLLM 做 motion translation，多轮生成/编辑不需要额外对话数据。它的启发是 agentic 不应代替 motion 模型，而应作为 planner/coordinator 调用可验证的低层 motion tools。

对下一篇工作的启发：motion understanding 最有价值的入口不是“给生成结果写 caption”，而是：

- 识别动作阶段，指导 camera 何时推近、跟随、停顿。
- 解释 badcase 是 semantic mismatch、root jump、camera drift、framing failure 还是 skeleton invalid。
- 把用户编辑指令转成 sparse motion/camera constraints。
- 作为 reward 或 ranking 信号进行后训练。

## 6. RL、偏好和后训练：从监督拟合到目标能力对齐

这一类工作与 4 卡 5090 的资源约束高度相关。它们共同说明：如果已有预训练生成模型或 checkpoint，不一定要构建大数据或重训全模型，可以通过 reward、preference、critic、DPO/RFT 或 small LoRA 后训练改变模型偏好。

[MotionRFT(arxiv_2026)](analysis/arxiv_2026/MotionRFT_Unified_Reinforcement_Fine-Tuning_for_Text-to-Motion_Generation.md) 把异构运动表示映射到共享语义空间，训练统一 reward，并用 EasyTune 解耦去噪链梯度，降低内存。它说明 motion diffusion 的强化微调可以做得更省显存。

[SoPo(NEURIPS_2025)](analysis/NEURIPS_2025/SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization.md) 关注偏好数据构造：离线优质样本提供稳定偏好方向，在线生成负样本提供多样性。它的启发是下一篇工作可以用已有 GT/高质量样本作为 preferred，用当前模型或公开视频模型生成 badcase 作为 non-preferred，不必先做人类大规模偏好数据。

[MotionCritic(ICLR_2025)](analysis/ICLR_2025/MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions.md) 证明学习型评价器比传统启发式指标更接近人类偏好，并可作为微调信号。当前不适合复刻它的大规模人工偏好数据，但可以把它的思想缩小为 proxy critic、small preference calibration 或 badcase ranker。

[PhysMoDPO(arxiv_2026)](analysis/arxiv_2026/PhysMoDPO_Physically-Plausible_Humanoid_Motion_with_Preference_Optimization.md) 把 WBC 当黑盒物理验证器，使用物理跟踪后的奖励构造偏好数据。对应到 human-camera-video，新工作不应只在原始 motion/camera 空间评价，而要在“经过渲染/重建/retarget/相机投影后”的下游空间评价。

对下一篇工作的启发：后训练最现实的工业入口是 **generated output replay + proxy reward/preference + LoRA/adapter**。这比重新构建大数据集更符合独立实验资源。

## 7. 物理执行闭环：从 kinematic plausibility 到 executable motion

这类工作不一定直接成为下一篇工作的主线，但它定义了“motion 工业可用”的更高标准：运动不只是看起来像，还要能被物理角色或机器人跟踪、执行、交互。

[MoConVQ(TOG_2024)](analysis/TOG_2024/MoConVQ_Unified_Physics_Based_Motion_Control_via_Scalable_Discrete_Representations.md) 用离散 VQ 表示统一物理运动控制，并强调离散表示对噪声鲁棒。它说明 motion representation 的鲁棒性会影响后续物理控制和大规模技能组合。

[SuperPADL(SIGGRAPH_2024)](analysis/SIGGRAPH_2024/SuperPADL_Scaling_Language_Directed_Physics_Based_Control_with_Progressive_Supervised_Distillation.md) 的关键不是“RL 更强”，而是发现直接在大规模数据上用 RL 会失效，因此把 RL 限制在小专家，再用监督蒸馏扩展到大控制器。这是一种资源和目标解耦的训练范式。

[PhyGile(arxiv_2026)](analysis/arxiv_2026/PhyGile_Physics_Prefix_Guided_Motion_Generation_for_Agile_General_Humanoid_Motion_Tracking.md) 用物理前缀作为生成和执行共享接口，把生成锚定在机器人可执行动态流形上。

[HumanX(arxiv_2026)](analysis/arxiv_2026/HumanX_Toward_Agile_and_Generalizable_Humanoid_Interaction_Skills_from_Human_Videos.md) 的洞察是：对机器人技能而言，物理合理的交互比光度精确重建更重要。这个优先级转换很适合提醒下一篇工作：如果目标是工业可用，指标不应只围绕重建误差，而应围绕下游可用性。

对下一篇工作的启发：不必马上做机器人，但可以借鉴“物理验证器/下游验证器”的思想。比如 human-camera motion 是否可渲染、可 retarget、可被 camera 投影稳定跟踪、可保持 foot contact 和骨长一致。

## 8. Human video 诊断：视觉质量提升后，人体运动错误更隐蔽

[HumanScore(arxiv_2026)](analysis/arxiv_2026/HumanScore_Benchmarking_Human_Motions_in_Generated_Videos.md) 和 [WYD(CVPR_2026)](analysis/CVPR_2026/What_Are_You_Doing_A_Closer_Look_at_Controllable_Human_Video_Generation.md) 共同说明一个趋势：视频模型视觉质量越来越强，传统视觉指标不再足以判断 human video 是否可用。真实问题转向人体结构、生物力学、动作保真、多演员、遮挡、交互和非典型动作。

HumanScore 把评估维度切到解剖、运动学和动力学正确性，例如骨长稳定、关节活动范围、自碰撞、运动极值和平滑度。WYD 则通过细粒度人类视频类别和人类对齐指标，暴露可控 human video 在多演员、遮挡、物体消失、身份崩溃、非典型动作等场景的失败。

对下一篇工作的启发：如果 human-camera-video 要连接 video，它不能只输出 motion，也不能只看 video aesthetics。真实痛点是 **human video 看起来真实但 motion/skeleton/camera 不可信**。这正好连接 skeleton reconstruction、motion understanding、camera framing 和 generated video evaluation。

## 归纳出的真实需求痛点

### 痛点 1：专用 motion 数据不足，如何借用预训练视频模型的泛化能力

现有工作已给出清晰趋势：AnimaX、CoMoVi、CamCloneMaster 都不是从零学习全部能力，而是把预训练视频模型的时空先验转成 pose、motion 或 camera control 能力。下一篇工作的机会不是重训一个更大的 motion model，而是研究 **video prior 到 structured human-camera motion 的迁移接口**。

可能问题形态：

- 视频模型内部的时序注意力是否能作为 human/camera motion prior。
- 参考视频能否作为 camera/human motion style control，而不是显式轨迹输入。
- 2D pose/video branch 能否辅助 3D human-camera motion 生成，提高泛化和语义丰富度。

### 痛点 2：相机控制不是轨迹拟合，而是用户可用的镜头接口

CameraCtrl、CamCloneMaster、CT-1、ShotVerse 共同说明，用户不想手写相机外参。真实接口可能是参考视频、文本意图、shot type、camera strength、follow strength 或自动 planner。

可能问题形态：

- 给定 human motion 和参考镜头，克隆 camera style 到新 motion。
- 给定文本动作阶段，自动规划 camera trajectory，再由结构化 human-camera 模块执行。
- 给定同一 human motion，输出不同 camera strength 的可控镜头版本。

### 痛点 3：human-camera coupling 的可靠性缺口

Towards Storytelling Animations 和 StoryMotion 都在强调角色和相机联合生成。但 MotionCtrl/I2VControl/BulletTime 又说明，耦合必须是可解释、可拆分、可调节的。StoryMotion 暴露出的 Pulp relative camera latent 依赖 human/root，可以作为下一篇工作的诊断起点：一旦 human 是 generated/noisy，camera 就可能失稳。

可能问题形态：

- generated-human-aware camera control。
- reliability-aware camera conditioning。
- noisy skeleton 下 camera 退化斜率评估。
- camera 是否应跟随 root、关节中心、动作语义焦点或 screen-space subject。

### 痛点 4：benchmark joint motion 不是 animation-ready skeleton motion

MoCapAnything V2、PALUM、PRISM、SKEL-Betweener 都说明 skeleton 表示是核心工业问题。下一篇工作若只输出 joint coordinate，后续 animation asset 使用仍要面对 rotation recovery、retarget、IK、骨长稳定和可编辑约束。

可能问题形态：

- human-camera motion 输出到 SMPL/rotation/target skeleton 的 representation adapter。
- 参考姿态-旋转对作为 skeleton export 的坐标轴锚点。
- 任意 sparse joint/camera keyframe inbetweening。
- motion reconstruction branch 作为 skeleton manifold anchor。

### 痛点 5：motion understanding 应进入控制和修复闭环

UniMo、LLaMo、SkeletonLLM、Motion-Agent 的共同价值不是“会说 motion caption”，而是把 motion 转成可推理对象。下一篇工作需要的是动作阶段、身体部位、语义焦点和 badcase 归因。

可能问题形态：

- 把 motion understanding score 用作 camera planner 的条件。
- 识别动作阶段，让 camera 在关键动作处推近或保持主体。
- 用 understanding module 给 cleanup/refiner 提供 edit instruction。
- 对 generated human-camera-video 输出 failure tags。

### 痛点 6：后训练比大数据更适合当前资源

MotionRFT、SoPo、MotionCritic、PhysMoDPO 说明模型能力可以通过后训练和偏好优化改变。对于 4 卡 5090，更现实的是 LoRA/adapter + generated output replay + proxy reward，而不是构建大数据。

可能问题形态：

- 用前序 StoryMotion 或公开视频模型生成结果构造 preferred/non-preferred 对。
- 用 camera framing、motion smoothness、bone consistency、semantic alignment 做 proxy reward。
- 对 camera branch 或 refiner 做小规模 RFT/DPO。
- 不追求通用 reward model，只做 human-camera-video-specific badcase ranker。

### 痛点 7：video 生成的人体动作需要结构化诊断

HumanScore 和 WYD 指出，人眼和传统视频指标会漏掉人体运动异常。human-camera-video 如果要工业可用，需要把 video 输出还原到 skeleton/motion 层做诊断。

可能问题形态：

- 从生成视频估计 skeleton，评估骨长、关节范围、自碰撞、运动平滑。
- 把 camera framing 和 human biomechanics 联合评分。
- 发现 video 看似逼真但 3D motion 不可信的样本，作为后训练负样本。

### 痛点 8：长视频和多镜头需要世界记忆，而不是片段拼接

CamDirector、ShotVerse、BulletTime 都在处理长程一致性、多镜头结构和世界时间/相机解耦。下一篇工作如果扩展到 story 级别，不能只把短片段拼起来。

可能问题形态：

- human-camera motion 的 shot-level memory。
- 跨片段 camera continuity 和 subject continuity。
- 世界时间、动作阶段、camera pose 三者解耦。
- 多镜头生成中保持角色身份、空间方向和动作节奏。

### 痛点 9：物理和接触不是必须主线，但可以是高价值验证器

MoConVQ、SuperPADL、PhyGile、HumanX 的共同教训是：可执行性来自下游验证闭环。下一篇工作未必要做 humanoid control，但可以把物理/接触作为验证器或 reward。

可能问题形态：

- foot contact、ground penetration、root acceleration 作为 motion reward。
- human-object/human-scene contact 作为 camera emphasis 的条件。
- 通过 retarget 或 simple physics check 过滤不可用 motion。

### 痛点 10：下一篇工作需要从能力统一变成接口统一

现有工作越来越少把贡献写成“我统一了任务”，而是写成“我统一了接口”：参考视频接口、skeleton 接口、trajectory 接口、motion-language 接口、physics prefix 接口、planner-controller 接口。

下一篇工作更需要回答：

- 用户输入是什么：caption、reference video、sparse keyframe、camera style、shot plan、motion edit instruction。
- 模型输出能给谁用：动画资产、视频模型、camera planner、motion refiner、human video evaluator。
- 失败能否被定位：human semantic、skeleton validity、camera framing、motion-camera coupling、video rendering。

## 对下一篇工作的引导性结论

当前最值得保留的主线思路是 **pretrained generative prior for structured human-camera-video control**。

这不是继续包装 StoryMotion，也不是让新工作直接变成视频生成模型，而是把下一篇工作定位为结构化中间层：

```text
pretrained video / MLLM / reward / physics priors
  -> structured human skeleton + camera trajectory + shot semantics
  -> controllable generation / repair / retarget / video grounding
```

这个定位比单纯“unified human-camera generation”更接近真实需求，因为它承认：

- 泛化能力主要来自预训练大模型和公开视频先验。
- 工业可用性来自结构化接口、可控性、可导出、可修复、可评估。
- 4 卡 5090 条件下，最现实的技术杠杆是 adapter、post-training、reference conditioning、generated-output replay 和 proxy reward。

后续 brainstorm 应围绕这些痛点继续展开，而不是过早收敛到单一执行方案。
