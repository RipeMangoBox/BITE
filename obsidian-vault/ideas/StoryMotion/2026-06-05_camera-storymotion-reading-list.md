---
title: "Camera + StoryMotion 核心推荐阅读顺序"
created: 2026-06-05T00:00:00+08:00
updated: 2026-06-05T00:00:00+08:00
status: reference
tags:
  - reading_list
  - camera_movement
  - storymotion
  - human_camera_motion
---

# Camera + StoryMotion 核心推荐阅读顺序

> 按理解依赖排序，从领域全景到具体提案。每层标注必读/选读。

---

## Layer 1: 领域全景（必读，2 篇）

| # | 文档 | 为什么读 | 预计时间 |
|---|---|---|---|
| 1 | [[ideas/camera/2026-06-05_camera-movement-generation-system-survey-llm-audit-merged\|Camera Movement 系统调研]] | 了解 camera movement generation 的全景：任务分类（A/B/C/D/E）、关键论文、发展脉络、gap。这是所有后续阅读的背景地图。 | 30min |
| 2 | [[ideas/StoryMotion/2026-06-05_camera-shot-edit\|CameraShotEdit]] | 理解 "human motion edit + camera shot planning" 这个交叉问题的边界，以及已有覆盖的完整分析（§0 是精华）。 | 20min |

---

## Layer 2: 主线论文（必读，5 篇）

> 按时间线和逻辑依赖排列。

| #   | 论文                                                                                                                                      | 核心贡献                                                                                               | 阅读重点                                                        |
| --- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| 3   | [[analysis/ECCV_2024/E.T._the_Exceptional_Trajectories_Text-to-camera-trajectory_generation_with_character_awareness\|E.T. / DIRECTOR]] | text-to-camera trajectory with character awareness。第一个把角色轨迹和相机轨迹对齐的工作，定义了 CLaTr 评估指标。              | 数据集构造、CLaTr embedding、为什么 character-aware 是关键               |
| 4   | [[analysis/ICCV_2025/GenDoP_Auto-regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography\|GenDoP / DataDoP]]               | director-style camera trajectory generation。自回归 token 生成 camera trajectory，DataDoP 数据集（29K shots）。 | camera tokenization、DataDoP 的 labeling 质量、自回归 vs 扩散的选择      |
| 5   | [[analysis/ICLR_2026/Pulp_Motion_Framing-aware_multimodal_camera_and_human_motion_generation\|Pulp Motion]]                             | **最关键**。text-conditioned joint human-camera generation，screen-space framing as auxiliary modality。 | screen framing latent 的对齐机制、auxiliary sampling 可否转为 editing |
| 6   | [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions\|Towards Storytelling Animations]]     | 三实体（两角色+相机）联合生成。CVPR 2026，代表 joint generation 的 SOTA。                                              | 与 Pulp Motion 的差异、multi-character 如何处理                      |
| 7   | [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes\|AdaViewPlanner]]               | 4D human motion → viewpoint planning。利用预训练 T2V 的摄影先验。                                              | 如何从 T2V 中提取 camera prior、两阶段规划的设计                           |

---

## Layer 3: 执行器与控制器（选读，4 篇）

> 如果你关心"camera trajectory 如何变成视频"，读这些。

| # | 论文 | 核心贡献 |
|---|---|---|
| 8 | [[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation\|MotionCtrl]] | camera/object motion 解耦控制的基线 |
| 9 | [[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text-to-Video_Generation\|CameraCtrl]] | Plücker embedding + plug-and-play camera module |
| 10 | [[analysis/CVPR_2025/GEN3C_3D-Informed_World-Consistent_Video_Generation_with_Precise_Camera_Control\|GEN3C]] | 3D-consistent camera-controlled video |
| 11 | [[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image-to-Video_Generation\|MotionCanvas]] | scene-space interactive shot design |

---

## Layer 4: StoryMotion 提案（必读，2 篇）

| # | 文档 | 核心问题 | 预计时间 |
|---|---|---|---|
| 12 | [[ideas/StoryMotion/2026-06-04_storymotion_cinematic_section_graph_plan\|StoryMotion CSG Plan]] | 已有 human-camera timeline 局部编辑后，如何量化失效范围、保护已批准内容、仅修复 boundary？ | 25min |
| 13 | [[ideas/StoryMotion/2026-06-05_unified-human-camera-motion-token-framework\|Unified Token Framework]] | 能否用 unified mask-then-predict 范式统一 human-camera 的生成和编辑？（Q&A 格式） | 20min |

---

## Layer 5: 编辑相关（选读，2 篇）

> 如果聚焦 edit 方向。

| # | 论文 | 核心贡献 |
|---|---|---|
| 14 | [[analysis/SIGGRAPH_Asia_2024/MotionFix_Text-Driven_3D_Human_Motion_Editing\|MotionFix]] | text-driven 3D human motion editing |
| 15 | [[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text-Driven_Multi-Shot_Video_Creation\|ShotVerse]] | multi-shot camera planning，planner/controller 分层 |

---

## 推荐阅读路径

**如果你关注 human-camera joint generation：**
```
1 → 5 → 6 → 7 → 12 → 13
```

**如果你关注 motion editing + camera planning：**
```
1 → 2 → 12 → 13 → 14
```

**如果你想快速了解领域 gap：**
```
1 → 2 → 5 → 13
```
