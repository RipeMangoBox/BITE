---
title: Camera Movement Generation 系统调研与 LLM 审查合并版
created: 2026-06-05T00:00:00+08:00
updated: 2026-06-05T00:00:00+08:00
status: merged_survey
tags:
  - camera_movement_generation
  - camera_trajectory_generation
  - camera_controlled_video
  - text_to_camera
  - sketch_to_camera
  - llm_audit
source_notes:
  - "[[ideas/camera/2026-06-03_camera-movement-generation-survey.md|2026-06-03 survey]]"
  - "[[ideas/camera/2026-06-04_camera-movement-generation-llm-audit-merged.md|2026-06-04 LLM audit]]"
hypothesis: Camera movement generation 正在从显式轨迹控制走向文本、场景、角色、草图和导演意图驱动的自动运镜规划；但必须区分轨迹生成、给定轨迹执行、交互式路径指定、数据/评测工具。
---

# Camera Movement Generation 系统调研与 LLM 审查合并版

> [!abstract] 结论先行
> Camera movement generation 不是空白方向，但不能把所有 camera control / video motion control 都算作"自动生成运镜"。严格口径下，主线是从文本、角色轨迹、场景语义、音乐/动作或导演意图生成 camera pose / trajectory；下游 camera-controlled video、NVS、re-camera、pose dataset 和 motion brush 都只是辅助层。2024 年以后主线已经由 [[analysis/CGF_2024/Cinematographic_Camera_Diffusion_Model.md|Cinematographic Camera Diffusion]]、[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md|E.T. / DIRECTOR]]、[[analysis/NEURIPS_2024/Director3D_Real_world_Camera_Trajectory_and_3D_Scene_Generation_from_Text.md|Director3D]]、[[analysis/arxiv_2024/ChatCam_Empowering_Camera_Control_through_Conversational_AI.md|ChatCam]]、[[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md|GenDoP / DataDoP]] 推起来；2025-2026 年进一步扩展到 [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md|Pulp Motion]]、[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md|Towards Storytelling Animations]]、[[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.md|AdaViewPlanner]]、[[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation.md|ShotVerse]] 等 human-camera / multi-shot 场景。

检索与整理时点：2026-06-05 Asia/Shanghai。  
本 note 合并 [[ideas/camera/2026-06-03_camera-movement-generation-survey.md|系统调研]] 与 [[ideas/camera/2026-06-04_camera-movement-generation-llm-audit-merged.md|LLM 审查]]。

---

## 1. 任务边界与判定口径

核心判定问题只有一个：**系统是否生成或规划 camera pose / trajectory 本身。**

| 层级                                | 定义                                                |     是否主线 | 代表                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| --------------------------------- | ------------------------------------------------- | -------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A. Camera movement generation     | 从文本、角色、动作、音乐、场景语义或导演意图生成 camera pose / trajectory |        是 | [[analysis/CGF_2024/Cinematographic_Camera_Diffusion_Model.md\|CCD]], [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md\|E.T.]], [[analysis/NEURIPS_2024/Director3D_Real_world_Camera_Trajectory_and_3D_Scene_Generation_from_Text.md\|Director3D]], [[analysis/arxiv_2024/ChatCam_Empowering_Camera_Control_through_Conversational_AI.md\|ChatCam]], [[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md\|GenDoP]], [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md\|Pulp Motion]], [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.md\|AdaViewPlanner]] |
| B. Camera-controlled video / NVS  | 已给定 camera trajectory，模型负责生成或重渲染视频                |     辅助主线 | [[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md\|MotionCtrl]], [[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md\|CameraCtrl]], [[analysis/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength.md\|I2VControl-Camera]], [[analysis/CVPR_2025/AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transformers.md\|AC3D]], [[analysis/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.md\|GEN3C]]                                                                                                                                                                                                    |
| C. Sketch / interactive-to-camera | 用户画路径、拖拽相机、在 3D scene-space 指定 camera path        |      半主线 | [[analysis/arxiv_2025/RealCam_I2V_Real_World_Image_to_Video_Generation_with_Interactive_Complex_Camera_Control.md\|RealCam-I2V]], [[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.md\|MotionCanvas]], [[analysis/arxiv_2025/Free_Form_Motion_Control_A_Synthetic_Video_Generation_Dataset_with_Controllable_Camera_and_Object_Motions.md\|FMC / SynFMC]]                                                                                                                                                                                                                                                                                                                                                                            |
| D. Re-camera / trajectory editing | 源视频 + target camera trajectory，输出重运镜视频            | actuator | [[analysis/arxiv_2025/TrajectoryCrafter_Redirecting_Camera_Trajectory_for_Monocular_Videos_via_Diffusion_Models.md\|TrajectoryCrafter]], [[analysis/ICCV_2025/ReCamMaster_Camera_Controlled_Generative_Rendering_from_A_Single_Video.md\|ReCamMaster]], [[analysis/AAAI_2026/Vid_CamEdit_Video_Camera_Trajectory_Editing_with_Generative_Rendering_from_Estimated_Geometry.md\|Vid-CamEdit]]                                                                                                                                                                                                                                                                                                                                                                                                |
| E. 数据 / 评测 / 工具                   | 有 pose、label、SfM/SLAM 或 eval，但不生成运镜               |      非主线 | RealEstate10K, DL3DV, MVImgNet, CameraBench, DynPose-100K                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

完整本地链接示例：[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md|E.T.]]、[[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md|GenDoP]]、[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl]]、[[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md|CameraCtrl]]。

必须保留的边界：

- `camera movement generation` 要求模型生成或规划 camera pose / trajectory。
- `camera-controlled video` 通常是已给定轨迹后执行生成。
- `2D trajectory -> video motion` 不等于 `2D sketch -> 6-DoF camera trajectory`。
- `camera pose dataset` 不等于 `camera movement generation dataset`。
- `object/global motion control` 不能直接等同为 camera extrinsics generation。

---

## 2. 发展谱系

### 2.1 经典自动摄影与 HCI

早期路线使用规则、约束和 HCI 映射来生成或控制 camera path，例如 declarative camera control、procedural camera movements、path drawing for 3D walkthrough、sketch-based navigation、camera-on-rails、CineMPC 等。这条线的优势是可解释、可控、可执行；缺点是开放域语义、真实视频生成和多模态理解能力弱。

### 2.2 2023-2024：从视频运动控制中分离 camera motion

2023 年前后，视频生成中的 motion control 常把 camera motion、object motion、optical flow、2D point tracks 混成统一运动信号。2024 年以后，[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl]]、[[analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion.md|Direct-a-Video]]、[[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md|CameraCtrl]]、[[analysis/arxiv_2024/Latent_Reframe_Enabling_Camera_Control_for_Video_Diffusion_Model_without_Training.md|Latent-Reframe]] 等工作开始把 camera pose / trajectory 作为独立控制变量，camera control 从泛化 motion control 中分离出来。

关键转变：

- camera pose 由粗糙 pan / tilt / zoom 走向 6-DoF pose、Plucker embedding、dense point trajectory 或 scene-space path。
- camera/object motion 解耦成为视频控制系统的重要设计点。
- 但这条线多数仍是 **给定 camera path 后执行**，不是从导演意图自动生成 camera movement。

### 2.3 2024-2026：text / character / director style camera trajectory generation 成形

主线工作包括：

- [[analysis/CGF_2024/Cinematographic_Camera_Diffusion_Model.md|Cinematographic Camera Diffusion]]：文本与 keyframe 条件下生成电影相机轨迹。
- [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md|E.T. / DIRECTOR]]：从真实影视片段抽取 camera-character trajectory，做 text-to-camera trajectory with character awareness。
- [[analysis/NEURIPS_2024/Director3D_Real_world_Camera_Trajectory_and_3D_Scene_Generation_from_Text.md|Director3D]]：在 text-to-3D / 3D scene generation 中生成真实世界 camera trajectory。
- [[analysis/arxiv_2024/ChatCam_Empowering_Camera_Control_through_Conversational_AI.md|ChatCam]]：用对话式语言接口控制 camera trajectory。
- [[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md|GenDoP / DataDoP]]：用 director-of-photography 数据和自回归 token 轨迹生成更自由的艺术相机路径。
- [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md|Pulp Motion]] / [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md|Towards Storytelling Animations]] / [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.md|AdaViewPlanner]]：把 human motion、character interaction 与 viewpoint / camera trajectory 放进同一问题域。
- [[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation.md|ShotVerse]]：把 multi-shot camera planning 与 camera-controlled video controller 分成 planner / controller 两层。

---

## 3. 主线：生成 Camera Trajectory 本身

| 工作                                                                                                                                         |   年份 | 输入                                  | 输出                                  | 主线价值                                        | 注意事项                    |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ---: | ----------------------------------- | ----------------------------------- | ------------------------------------------- | ----------------------- |
| [[analysis/CGF_2024/Cinematographic_Camera_Diffusion_Model.md\|Cinematographic Camera Diffusion]]                                          | 2024 | 文本 + 可选 keyframes                   | camera trajectory                   | 将电影相机轨迹扩散生成任务化                              | 不处理人体 motion edit       |
| [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md\|E.T. / DIRECTOR]] | 2024 | 文本 + character trajectory           | camera trajectory                   | character-aware text-to-camera 数据与模型        | 角色是条件，不编辑角色动作           |
| [[analysis/NEURIPS_2024/Director3D_Real_world_Camera_Trajectory_and_3D_Scene_Generation_from_Text.md\|Director3D]]                         | 2024 | 文本                                  | camera trajectory + 3D scene        | 把 camera trajectory 纳入 text-to-3D           | 不等于 human-centric edit  |
| [[analysis/arxiv_2024/ChatCam_Empowering_Camera_Control_through_Conversational_AI.md\|ChatCam]]                                            | 2024 | 对话 / 文本指令                           | camera trajectory                   | 自然语言交互式 camera control                      | 细节需按原论文源核验              |
| [[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md\|GenDoP / DataDoP]]               | 2025 | 文本 + RGBD                           | camera trajectory tokens            | director-style free-moving camera           | DataDoP 数字需谨慎           |
| [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md\|Pulp Motion]]                             | 2026 | 文本                                  | human motion + camera trajectory    | framing-aware human-camera joint generation | ICLR 2026               |
| [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md\|Towards Storytelling Animations]]     | 2026 | character / story animation setting | character + camera motions          | 三实体 human-camera joint synthesis            | full generation，不是 edit |
| [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.md\|AdaViewPlanner]]               | 2026 | 4D scene / human motion + text      | viewpoint / camera trajectory       | 从 human motion 到 viewpoint planning         | 两阶段规划，不是 DCC edit       |
| [[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation.md\|ShotVerse]]               | 2026 | text-driven multi-shot instruction  | aligned camera trajectories + video | multi-shot planner / controller             | 新预印本，状态需持续核             |

相关本地笔记：[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md|Pulp Motion]]、[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md|Towards Storytelling Animations]]、[[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.md|AdaViewPlanner]]、[[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation.md|ShotVerse]]。

---

## 4. 下游执行器：Camera-Controlled Video / NVS / Re-camera

这条线对 camera movement generation 很重要，但通常不是"生成运镜本身"。它解决的是：给定 camera path 后如何让视频或新视角严格执行。

| 子方向                                | 输入                                      | 输出                      | 代表                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | 在系统中的角色          |
| ---------------------------------- | --------------------------------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| Text/image + camera pose control   | text/image + camera trajectory          | camera-controlled video | [[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md\|MotionCtrl]], [[analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion.md\|Direct-a-Video]], [[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md\|CameraCtrl]], [[analysis/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength.md\|I2VControl-Camera]], [[analysis/CVPR_2025/AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transformers.md\|AC3D]] | 执行 planner 给出的轨迹 |
| 3D/world-consistent camera control | seed views / scene memory + camera path | 一致的新视角视频                | [[analysis/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.md\|GEN3C]], [[analysis/ICLR_2026/3D_Scene_Prompting_for_Scene_Consistent_Camera_Controllable_Video_Generation.md\|3D Scene Prompting]], [[analysis/ICCV_2025/Stable_Virtual_Camera_Generative_View_Synthesis_with_Diffusion_Models.md\|Stable Virtual Camera]]                                                                                                                                                                                                                                                  | 降低长轨迹漂移          |
| Re-camera / trajectory editing     | source video + target camera trajectory | 重运镜视频                   | [[analysis/arxiv_2024/Latent_Reframe_Enabling_Camera_Control_for_Video_Diffusion_Model_without_Training.md\|Latent-Reframe]], [[analysis/arxiv_2025/TrajectoryCrafter_Redirecting_Camera_Trajectory_for_Monocular_Videos_via_Diffusion_Models.md\|TrajectoryCrafter]], [[analysis/ICCV_2025/ReCamMaster_Camera_Controlled_Generative_Rendering_from_A_Single_Video.md\|ReCamMaster]], [[analysis/AAAI_2026/Vid_CamEdit_Video_Camera_Trajectory_Editing_with_Generative_Rendering_from_Estimated_Geometry.md\|Vid-CamEdit]]                                                                                            | 将轨迹应用到已有视频       |
| Joint camera-object control        | camera path + object 6D / motion        | 联合控制视频                  | [[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md\|MotionCtrl]], [[analysis/arxiv_2025/Free_Form_Motion_Control_A_Synthetic_Video_Generation_Dataset_with_Controllable_Camera_and_Object_Motions.md\|FMC / SynFMC]], [[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.md\|MotionCanvas]]                                                                                                                                                                                                                    | 解耦 camera 和动态对象  |

关键判断：

- [[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl]]、[[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md|CameraCtrl]]、[[analysis/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.md|GEN3C]]、[[analysis/ICCV_2025/ReCamMaster_Camera_Controlled_Generative_Rendering_from_A_Single_Video.md|ReCamMaster]] 等是强 actuator / controller。
- 它们可作为 text-to-camera 或 human-to-camera planner 的后端。
- 但除非方法自己预测 camera pose / trajectory，否则不应归为 camera movement generation 主线。

---

## 5. Sketch / Interactive-to-Camera 专项边界

严格定义：

```text
2D / 3D stroke, storyboard cue, drag path, first frame / scene
-> 6-DoF camera trajectory / camera path
```

当前结论：

- 严格 `freehand 2D sketch -> 6-DoF camera movement` 现代生成论文很少。
- 更常见的是用户已经给 3D scene-space path，或在重建场景里拖拽 camera / object。
- [[analysis/arxiv_2025/RealCam_I2V_Real_World_Image_to_Video_Generation_with_Interactive_Complex_Camera_Control.md|RealCam-I2V]]、[[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.md|MotionCanvas]]、[[analysis/arxiv_2025/Free_Form_Motion_Control_A_Synthetic_Video_Generation_Dataset_with_Controllable_Camera_and_Object_Motions.md|FMC / SynFMC]] 更接近交互式 camera / object control，不等于纯 2D sketch 自动生成 camera extrinsics。
- Tora、DragNUWA、DragAnything、[[analysis/CVPR_2025/MotionPro_A_Precise_Motion_Controller_for_Image_to_Video_Generation.md|MotionPro]]、[[analysis/arxiv_2023/AnimateAnything_Fine_Grained_Open_Domain_Image_Animation_with_Motion_Guidance.md|AnimateAnything]] 等更偏 object / global video motion control，不能直接作为 sketch-to-camera 主线证据。

可形成的 gap：

> 用户在屏幕上画 2D 箭头、曲线或构图草图，系统自动消歧为带 depth、look-at、speed profile、focal schedule、collision / framing constraints 的 6-DoF camera trajectory。

---

## 6. 数据集与评测资源

### 6.1 数据集总览

| 数据 / 资源                                                                                                                                                   | 规模                               | 含 human                          | 含 camera             | 含 text                                     | 含 framing            | 评分         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | -------------------------------- | -------------------- | ------------------------------------------ | -------------------- | ---------- |
| [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md\|PulpMotion]]                                             | **193K samples / 314h**          | Y（完整 SMPL）                       | Y（6-DoF）             | Y（VLM 生成，同时描述 human+camera）                | Y（正交投影 screen-space） | ★★★        |
| [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md\|TSA / Storytelling Animations]]                      | 未公开总数（电影片段 + Cine Tracer 合成）     | Y（双角色 SMPL）                      | Y（Toric space）       | **N（无条件生成）**                               | 间接（Toric 参数隐含构图）     | ★★★        |
| [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md\|E.T. / Exceptional Trajectories]] | 115K samples / 11M frames / 120h | **部分**（简化 root+heading，非完整 SMPL） | Y（6-DoF）             | Y（双文本：camera motion + camera-character 关系） | N                    | ★★         |
| [[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md\|DataDoP]]                                       | 29K shots / ~11M frames          | **N**                            | Y（free-moving 6-DoF） | Y（motion + directorial 双字幕）                | N（有 depth，非 framing） | ★★         |
| DynPose-100K                                                                                                                                              | 100K                             | N                                | Y                    | N                                          | N                    | ★          |
| [[analysis/arxiv_2025/Free_Form_Motion_Control_A_Synthetic_Video_Generation_Dataset_with_Controllable_Camera_and_Object_Motions.md\|SynFMC]]              | 62K videos                       | N                                | Y（6D pose）           | N                                          | N                    | controller |
| RealCam-Vid / related I2V                                                                                                                                 | 100K+                            | N                                | Y（metric-scale）      | Y                                          | N                    | controller |
| CameraBench                                                                                                                                               | 3K videos                        | N                                | N（仅 label）           | Y（motion primitive labels）                 | N                    | 评测         |
| RealEstate10K                                                                                                                                             | 10K clips                        | N                                | Y（SLAM/BA）           | N                                          | N                    | 辅助         |
| DL3DV / MVImgNet                                                                                                                                          | 10K+                             | N                                | Y（multiview）         | N                                          | N                    | 辅助         |

数据分析，camera分支究竟是否需要human smpl motion的约束：
1. [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md|PulpMotion]]需要，因为将human motion和camera trajectory的token映射为中间变量z，把hm和ct的text condition混合为对z的处理。
	1. 好处：复用T2M框架
	2. 坏处：条件混合，指令不清晰，结果不咋地
2. [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md|TSA / Storytelling Animations]] 需要，因为无条件生成，所以利用 \<character A, camera>, \<character B, camera>, \<character A, character B>三元组来增加约束（对camera生效的实际是前两个约束）
3. [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md|E.T. / Exceptional Trajectories]] 不需要，因为仅通过 \<camera text, tracking point>来控制相机的运动，不关注人物具体运动（甚至可以把人物换成别的东西），因此 E.T. 的数据集对 camera有更好的control效果，可以作为能力来源补强。

### 6.2 前四名数据集详细差异

**PulpMotion → ★★★ 的理由（vs E.T. ★★）：**

| 维度         | PulpMotion (★★★)                                  | E.T. (★★)                                          | 差异解读                                                                                   |
| ---------- | ------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Human 表示   | **完整 SMPL 人体参数**（关节旋转 + root + 接触状态）              | 简化 root trajectory + heading（不是 SMPL，无关节级信息）       | PulpMotion 可直接用于 human motion editing；E.T. 的角色轨迹只能做 camera planning 的条件输入              |
| 模态配对       | **human + camera + text 三者配对**                    | camera + 简化角色轨迹 + text（human 是条件不是输出）              | PulpMotion 支持双向生成（human→camera 和 camera→human）；E.T. 仅支持 camera-from-character          |
| Framing 信号 | **有**（正交投影 screen-space bbox、headroom、visibility） | 无                                                  | PulpMotion 的 framing signal 是 human-camera 耦合的关键桥梁，可直接用于 screen-space continuity 训练和评估 |
| Text 质量    | VLM 生成（从 RGB frames 提取，描述 human+camera 联合语义）      | 双文本（camera motion 描述 + camera-character 关系描述，分开标注） | PulpMotion 的联合描述更接近真实导演语言；E.T. 的描述是分开的，缺少 human-camera 交互语义                            |
| 数据来源       | CondensedMovies → SLAHMR 提取 → generative prior 修复 | Condensed Movies Dataset → SfM/SLAM 提取             | 同源（CMD），但 PulpMotion 多了一步 generative refinement（修复 out-of-screen body parts）           |
| 规模         | **193K samples, 314h**                            | 115K samples, 11M frames, 120h                     | PulpMotion 大 68%                                                                       |

**TSA / Storytelling Animations → ★★★ 的理由（vs E.T. ★★）：**

| 维度 | TSA (★★★) | E.T. (★★) | 差异解读 |
|---|---|---|---|
| 角色数量 | **双角色**（two-character interaction） | 单角色 | TSA 支持角色间交互，更接近真实影视场景 |
| 生成范式 | **联合生成**（同时输出 character + camera motions） | 单向（character → camera only） | TSA 的双向交互模块可以同时优化角色和相机；E.T. 只能以角色为条件生成相机 |
| 相机表示 | **Toric space**（球面坐标系，天然适配环绕拍摄） | 6-DoF SE(3) | Toric space 对 cinematic camera（orbit、tracking）更自然；SE(3) 更通用但不够专业化 |
| 数据来源 | 电影片段 + **Cine Tracer 虚拟引擎合成** | CMD 电影片段 | TSA 的合成数据补充了真实电影中稀缺的极端视角和复杂调度 |
| Text 条件 | **无（无条件生成）** | 有（双文本描述） | **这是 TSA 的短板**——无条件生成限制了可控性，难以直接用于导演意图驱动 |

### 6.3 PulpMotion vs TSA 头部对决

**两个 ★★★ 数据集的核心差异：**

| 维度         | PulpMotion                               | TSA                      | 谁赢         | 为什么                                                                           |
| ---------- | ---------------------------------------- | ------------------------ | ---------- | ----------------------------------------------------------------------------- |
| Text 条件    | **有**（VLM 生成联合描述）                        | 无                        | PulpMotion | 文本条件是实现 "text→human+camera" 的必要前提；TSA 的无条件生成需要额外训练 text conditioning          |
| Framing 信号 | **显式**（正交投影，可训练可评估）                      | 隐式（Toric 参数间接约束构图）       | PulpMotion | 显式 framing 可以直接作为 loss 和 metric；TSA 的隐式约束难以量化和诊断                              |
| 角色数量       | 单人                                       | **双人**                   | TSA        | 双角色支持 interaction modeling（打斗、对话、追逐）——影视制作的核心需求                               |
| 数据规模       | **193K, 314h**                           | 未公开（估计 <50K）             | PulpMotion | 规模优势直接影响生成多样性和泛化                                                              |
| 相机表示       | SE(3)                                    | **Toric space**          | TSA        | Toric 对 cinematic camera 更友好：轨道拍摄 = 球面上的弧线，dolly zoom = 径向移动                  |
| 数据质量       | CMD + SLAHMR + **generative refinement** | CMD + **Cine Tracer 合成** | 各有优势       | PulpMotion 的 refinement 修复了 SLAHMR 的 out-of-screen 错误；TSA 的合成数据补充了真实数据缺失的极端场景 |
| Editing 支持 | 间接（auxiliary sampling 可改造为 editing）      | 无                        | PulpMotion | auxiliary sampling 提供了不重新训练即可干预生成的能力                                          |

**选型建议：**
- 做 **text-conditioned human-camera joint generation / editing** → PulpMotion（唯一同时有 text + framing + paired data 的选择）
- 做 **multi-character cinematic scene generation** → TSA（唯一支持双角色的数据集，但需补 text conditioning）
- 做 **camera-from-human planning** → E.T. + DataDoP 也可以（规模大、标注好），但不如 PulpMotion 的 framing 信号有价值

### 6.4 数据 gap

- RealEstate10K 偏静态室内 / 房产镜头，不足以训练动态人物运镜。
- [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md|E.T.]] 强 human/character-aware，但角色轨迹是简化 root+heading，非完整 SMPL，无法直接支持 human motion editing。
- [[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md|DataDoP]] 强 director-style free-moving camera，但完全没有 human motion，无法训练 human-camera 耦合。
- **TSA 缺 text condition**——双角色+相机的联合生成目前是无条件的，需要额外标注或架构改造才能支持文本驱动。
- sketch / freehand-to-camera 缺少 HumanML3D 级别的公开标准数据。
- 多镜头 camera planning 的公开 benchmark 仍很新，生态未稳定。

---

## 7. 前后向 Citation / Reference 谱系

共同上游：

- [[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl]] 线：AnimateDiff、VideoComposer、DragNUWA、RealEstate10K 等，把通用视频 motion control 分解成 camera / object controls。
- [[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md|CameraCtrl]] 线：[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl]]、[[analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion.md|Direct-a-Video]]、RealEstate10K、ACID、MVImgNet，把 camera pose 表示提升为 Plucker / dense geometry condition。
- [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md|E.T.]] 线：movie/CMD 数据、SLAHMR、[[analysis/CGF_2024/Cinematographic_Camera_Diffusion_Model.md|Cinematographic Camera Diffusion]]、camera-language trajectory embedding。
- [[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md|GenDoP]] 线：[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md|E.T.]]、[[analysis/NEURIPS_2024/Director3D_Real_world_Camera_Trajectory_and_3D_Scene_Generation_from_Text.md|Director3D]]、MovieShots、RealEstate10K、[[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md|CameraCtrl]]、[[analysis/arxiv_2025/TrajectoryCrafter_Redirecting_Camera_Trajectory_for_Monocular_Videos_via_Diffusion_Models.md|TrajectoryCrafter]]，从 character-centric 扩到 director-style free-moving camera。
- [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md|Pulp Motion]] / [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md|TSA]] / [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.md|AdaViewPlanner]] 线：human motion generation、framing constraints、character-camera interaction、4D scene viewpoint planning。

后继扩展：

- [[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl]] -> [[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md|CameraCtrl]] / [[analysis/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength.md|I2VControl-Camera]] / [[analysis/CVPR_2025/AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transformers.md|AC3D]] / [[analysis/ICLR_2026/3D_Scene_Prompting_for_Scene_Consistent_Camera_Controllable_Video_Generation.md|3D Scene Prompting]]：camera condition 更几何化、更稳定。
- [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md|E.T.]] -> [[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md|GenDoP]] / [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md|Pulp Motion]] / [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.md|AdaViewPlanner]]：从 text-to-camera 扩到 human-camera joint planning。
- [[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md|CameraCtrl]] -> [[analysis/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.md|GEN3C]] / [[analysis/ICCV_2025/ReCamMaster_Camera_Controlled_Generative_Rendering_from_A_Single_Video.md|ReCamMaster]] / [[analysis/arxiv_2025/TrajectoryCrafter_Redirecting_Camera_Trajectory_for_Monocular_Videos_via_Diffusion_Models.md|TrajectoryCrafter]]：从单段 camera control 扩到世界一致性和重运镜。
- [[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.md|MotionCanvas]] / [[analysis/arxiv_2025/Free_Form_Motion_Control_A_Synthetic_Video_Generation_Dataset_with_Controllable_Camera_and_Object_Motions.md|FMC]] / [[analysis/arxiv_2025/RealCam_I2V_Real_World_Image_to_Video_Generation_with_Interactive_Complex_Camera_Control.md|RealCam-I2V]]：把交互式 path control 引入创作接口，但不必然自动生成 camera movement。

---

## 8. 2025/2026 重点跟踪清单

|   年份 | 工作                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 为什么继续跟                                                          |
| ---: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 2025 | [[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md\|GenDoP / DataDoP]]                                                                                                                                                                                                                                                                                                                                                    | director-style camera trajectory generation 的核心数据与模型            |
| 2025 | [[analysis/arxiv_2025/Free_Form_Motion_Control_A_Synthetic_Video_Generation_Dataset_with_Controllable_Camera_and_Object_Motions.md\|FMC / SynFMC]]                                                                                                                                                                                                                                                                                                                              | camera/object 6D pose control 数据，适合 controller 和交互接口            |
| 2025 | [[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.md\|MotionCanvas]]                                                                                                                                                                                                                                                                                                                                                      | scene-aware cinematic shot design with I2V control              |
| 2025 | [[analysis/CVPR_2025/AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transformers.md\|AC3D]] / [[analysis/ICLR_2025/I2VControl_Camera_Precise_Video_Camera_Control_with_Adjustable_Motion_Strength.md\|I2VControl-Camera]] / [[analysis/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.md\|GEN3C]] / [[analysis/ICCV_2025/ReCamMaster_Camera_Controlled_Generative_Rendering_from_A_Single_Video.md\|ReCamMaster]] | camera-control actuator 与 3D 一致性基础                              |
| 2026 | [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md\|Pulp Motion]]                                                                                                                                                                                                                                                                                                                                                                  | text-conditioned human-camera joint generation 与 framing latent |
| 2026 | [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md\|Towards Storytelling Animations]]                                                                                                                                                                                                                                                                                                                                          | character-camera joint synthesis                                |
| 2026 | [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.md\|AdaViewPlanner]]                                                                                                                                                                                                                                                                                                                                                    | 4D human motion + text 的 viewpoint planning                     |
| 2026 | [[analysis/ICLR_2026/3D_Scene_Prompting_for_Scene_Consistent_Camera_Controllable_Video_Generation.md\|3D Scene Prompting]]                                                                                                                                                                                                                                                                                                                                                      | scene-consistent camera-controllable video                      |
| 2026 | [[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation.md\|ShotVerse]]                                                                                                                                                                                                                                                                                                                                                    | multi-shot camera planning / controller                         |

不建议作为 camera movement generation 核心主线：

- SketchVideo：除非明确输出 camera pose / trajectory，否则证据不足。
- [[analysis/CVPR_2025/MotionPro_A_Precise_Motion_Controller_for_Image_to_Video_Generation.md|MotionPro]]：精确 I2V motion controller，不是 camera trajectory generator。
- [[analysis/arxiv_2023/AnimateAnything_Fine_Grained_Open_Domain_Image_Animation_with_Motion_Guidance.md|AnimateAnything]]：image animation / motion guidance。
- AKiRa：camera ray / lens model augmentation。
- MVImgNet、DL3DV、RealEstate10K：pose / multiview data，不是 text/sketch-to-camera task。

---

## 9. 挑战、Gap 与 Future Directions

### 9.1 主要挑战

- **数据缺口**：真实动态场景的 camera trajectory + actor / object motion + directorial intent 标注仍少。
- **评价缺口**：缺少统一 camera trajectory quality、framing、shot continuity、semantic alignment 评测。
- **多模态对齐**：高层导演语言到 6-DoF pose / FOV / speed profile 的映射难。
- **几何与语义冲突**：好看的 shot 可能不满足物理可行性，几何平滑也不代表 cinematic。
- **交互控制**：文本、草图、关键帧、拖拽、shot list 如何统一为可执行 camera plan。
- **动态主体**：human / object motion 会显著干扰 camera pose estimation、NVS 和 re-camera。

### 9.2 值得推进的方向

- **text / shot list -> 6-DoF camera plan**：把影视镜头语言落到可评估轨迹。
- **human motion -> camera trajectory**：针对 3D human motion / SMPL / skeleton 的 human-centric camera planner。
- **sketch-to-camera**：从 2D stroke / storyboard arrow 自动消歧成 3D camera path。
- **camera-aware motion editing**：motion edit 后同步评估和修复 framing / out-of-frame / shot continuity。
- **planner + actuator 分层系统**：planner 生成 camera path，[[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md|CameraCtrl]] / [[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.md|MotionCanvas]] / [[analysis/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.md|GEN3C]] / [[analysis/ICCV_2025/ReCamMaster_Camera_Controlled_Generative_Rendering_from_A_Single_Video.md|ReCamMaster]] 执行。
- **benchmark 标准化**：统一 prompt、trajectory format、framing metric、user study protocol。

---

## 10. 最小可执行调研路线

1. 以 [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md|E.T.]]、[[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md|GenDoP]]、[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md|Pulp Motion]]、[[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.md|AdaViewPlanner]]、[[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation.md|ShotVerse]] 作为 camera movement generation 主读线。
2. 以 [[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl]]、[[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md|CameraCtrl]]、[[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.md|MotionCanvas]]、[[analysis/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.md|GEN3C]]、[[analysis/ICCV_2025/ReCamMaster_Camera_Controlled_Generative_Rendering_from_A_Single_Video.md|ReCamMaster]] 作为 actuator / controller 主读线。
3. 单独建立 sketch-to-camera 表，不混入 object motion brush。
4. 对每个条目记录四个字段：是否输出 camera pose、是否自动生成轨迹、是否处理动态主体、是否支持 multi-shot。
5. 新方案或论文写作时，先声明 taxonomy，再引用相关工作；否则容易被 reviewer 认为把不同任务混在一起。

---

## 11. Source Links

本地来源：

- [[ideas/camera/2026-06-03_camera-movement-generation-survey.md|Camera Movement Generation 系统调研]]
- [[ideas/camera/2026-06-04_camera-movement-generation-llm-audit-merged.md|Camera Movement Generation LLM 审查与合并整理]]

关键 analysis notes：

- [[analysis/CGF_2024/Cinematographic_Camera_Diffusion_Model.md|Cinematographic Camera Diffusion]]
- [[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness.md|E.T.]]
- [[analysis/NEURIPS_2024/Director3D_Real_world_Camera_Trajectory_and_3D_Scene_Generation_from_Text.md|Director3D]]
- [[analysis/arxiv_2024/ChatCam_Empowering_Camera_Control_through_Conversational_AI.md|ChatCam]]
- [[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography.md|GenDoP]]
- [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md|Pulp Motion]]
- [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md|Towards Storytelling Animations]]
- [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes.md|AdaViewPlanner]]
- [[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation.md|MotionCtrl]]
- [[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.md|CameraCtrl]]
- [[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation.md|MotionCanvas]]
- [[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation.md|ShotVerse]]
- [[analysis/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.md|GEN3C]]
- [[analysis/ICCV_2025/ReCamMaster_Camera_Controlled_Generative_Rendering_from_A_Single_Video.md|ReCamMaster]]
- [[analysis/arxiv_2025/TrajectoryCrafter_Redirecting_Camera_Trajectory_for_Monocular_Videos_via_Diffusion_Models.md|TrajectoryCrafter]]
- [[analysis/arxiv_2024/Latent_Reframe_Enabling_Camera_Control_for_Video_Diffusion_Model_without_Training.md|Latent-Reframe]]
- [[analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion.md|Direct-a-Video]]
