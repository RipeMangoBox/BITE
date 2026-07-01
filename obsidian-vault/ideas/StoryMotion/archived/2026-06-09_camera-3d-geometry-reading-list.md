---
title: "StoryMotion 补缺阅读：Camera Geometry + Camera Trajectory Editing"
created: 2026-06-09T17:00:00+08:00
updated: 2026-06-13T15:05:16+08:00
status: reference
tags:
  - reading_list
  - camera_3d_geometry
  - camera_editing
  - storymotion
hypothesis: "StoryMotion camera 主线需要六类知识层：(1) subject-relative framing 的几何形式化；(2) camera / depth / point map 的统一 3D 几何编码；(3) text / content / 4D scene 到 camera trajectory 的 planner 与 camera editing baseline；(4) human-camera / object-camera joint control 竞品；(5) branch-mask / control-inpainting / observed-entity consistency 机制；(6) multi-entity role hierarchy 与 story-time / camera-time 解耦。MoDebug CFG guidance 机制阅读已迁移到 MoDebug training-dynamics reading list。"
---

# StoryMotion 补缺阅读：Camera Geometry + Camera Trajectory Editing

> [!abstract] 当前定位
> 这份 list 只服务 StoryMotion camera / geometry / camera-editing / human-camera joint control 主线。MoDebug 的 CFG residual、guidance、attention perturbation 机制阅读已迁移到 [[ideas/MoDebug/2026-06-09_training-dynamics-reading-list|MoDebug training dynamics reading list]]。

---

## S-Tier（必读）

| # | 论文 | 为什么现在必须读 | 核心方法 |
|---:|---|---|---|
| 1 | VGGT (CVPR 2025) | StoryMotion camera token 的 3D backbone。它给出 camera pose、depth、point map / point cloud 的统一 feed-forward 几何接口，是 camera-token 表征设计的优先参考。完整链接见：[[analysis/CVPR_2025/VGGT_Visual_Geometry_Grounded_Transformer]] | 前馈多视图几何估计，一次输出 camera pose、depth、point map / point cloud |
| 2 | Vid-CamEdit (AAAI 2026) | camera trajectory editing 的 pixel-level baseline。StoryMotion token edit 必须回答为什么 token-level camera/motion edit 优于这类生成式渲染编辑。完整链接见：[[analysis/AAAI_2026/Vid-CamEdit_Video_Camera_Trajectory_Editing_with_Generative_Rendering_from_Estimated_Geometry]] | 时序一致几何估计 → 2D flow → 条件视频扩散；分解式微调用多视图和视频数据替代 4D 数据 |
| 3 | D4RT (CVPR 2026) | StoryMotion camera-aware dynamic scene representation 的关键支线。它把 query point、target timestamp 和 camera frame 统一成动态重建接口，有助于思考 camera token 如何携带时空信息。完整链接见：[[analysis/CVPR_2026/Efficiently_Reconstructing_Dynamic_Scenes_One_D4RT_at_a_Time]] | query point + target timestamp + camera frame 的统一动态重建接口 |
| 4 | PAGE-4D (ICLR 2026) | 动态场景里分离 camera pose 与 moving object，对 StoryMotion 的 human-motion / camera-motion 解耦很关键。完整链接见：[[analysis/ICLR_2026/PAGE-4D_Disentangled_Pose_and_Geometry_Estimation_for_VGGT-4D_Perception]] | Dynamics-Aware Aggregator 用动态 mask 区分 pose / geometry 对动态内容的依赖 |
| 5 | Pulp Motion (ICLR 2026) | 最直接竞品：已经覆盖 framing-aware multimodal camera + human motion generation。StoryMotion 必须把差异落到三模式 branch-mask 条件补全和叙事条件，而不是泛泛 joint generation。完整链接见：[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]] | continuous human/camera latent + projection/framing guidance |
| 6 | ActCam (SIGGRAPH 2026) | 已覆盖 zero-shot joint camera + 3D human motion control。StoryMotion 需要说明 subject-relative framing、叙事阶段条件和 generated geometry 评估上的差异。完整链接见：[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation]] | camera-aligned depth/pose condition + two-stage denoising schedule |
| 7 | COIN (ECCV 2024) | branch-mask / control-inpainting 机制必读。它的 control-inpainting、软修复、多步 DDIM 和人-场景深度关系约束直接对应 StoryMotion 的 sampler 与 Mode B 风险。完整链接见：[[analysis/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation]] | control-inpainting diffusion prior + dynamic control + soft repair |
| 8 | AdaViewPlanner (ICLR 2026) | 直接覆盖给定 4D 人体内容与文本指令的 viewpoint planning，是 human→camera / narrative camera planner 的强竞品。完整链接见：[[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes]] | 利用 T2V 摄影先验，两阶段从人体运动生成相机轨迹 |
| 9 | CT-1 (arXiv 2026) | 直接覆盖 image/text-to-camera trajectory generation。StoryMotion 必须强调 observed branch 与 subject-relative constraints，而不是泛化为 camera transformer。完整链接见：[[analysis/arxiv_2026/CT_1_Camera_Trajectory_Generation_for_Camera_Controlled_Video_Generation]] | VLC model + diffusion Transformer + wavelet trajectory regularization |
| 10 | BulletTime (CVPR 2026) | 明确解耦 world time 与 camera pose，对 StoryMotion 的 story-time / camera-time / subject-motion 分解很关键。完整链接见：[[analysis/CVPR_2026/BulletTime_Decoupled_Control_of_Time_and_Camera_Pose_for_Video_Generation]] | Time/4D-RoPE + Time/Camera-AdaLN 解耦时间与相机 |
| 11 | Toric Space (TOG 2015) | subject-relative framing 的经典几何锚点；不是生成竞品，但应支撑 Mode A/B 的 framing gate。完整链接见：[[analysis/TOG_2015/Intuitive_and_Efficient_Camera_Control_with_the_Toric_Space]] | 两目标构图的角度三元组参数化与屏幕空间约束 |

---

## A-Tier（强烈推荐）

| # | 论文 | 为什么推荐 | 核心方法 |
|---:|---|---|---|
| 12 | E.T. / Director (ECCV 2024) | character-aware camera trajectory 直接前作，支撑 human→camera 模式必须看到角色轨迹。完整链接见：[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness]] | character trajectory conditioned camera diffusion + CLaTr evaluation |
| 13 | GenDoP (ICCV 2025) | director-of-photography camera token 路线，作为 text/content→camera planner baseline。完整链接见：[[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography]] | auto-regressive discrete camera trajectory generation |
| 14 | ShotVerse (arXiv 2026) | text-driven multi-shot camera planner / controller 竞品。StoryMotion 若讲 narrative/storyboard，必须说明角色、branch-mask 与人相机条件补全上的差异。完整链接见：[[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text_Driven_Multi_Shot_Video_Creation]] | plan-then-control: caption→trajectory, caption+trajectory→video |
| 15 | CamDirector (arXiv 2026) | 长视频 camera trajectory control 与 source consistency 强竞品，对 observed branch continuation 很关键。完整链接见：[[analysis/arxiv_2026/CamDirector_Camera_Trajectory_Control_for_Long_term_Video_Generation]] | world cache + hybrid warping + history-guided autoregressive diffusion |
| 16 | 3D Scene Prompting (ICLR 2026) | scene-consistent camera control 强竞品，支撑 StoryMotion 的 observed-scene / branch memory 评估。完整链接见：[[analysis/ICLR_2026/3D_Scene_Prompting_for_Scene_Consistent_Camera_Controllable_Video_Generation]] | 3D scene memory + dual spatio-temporal sliding window |
| 17 | Taming Video Models (CVPR 2026) | 零样本 camera control 强竞品，挑战训练式 camera controller 的必要性。完整链接见：[[analysis/CVPR_2026/Taming_Video_Models_for_3D_and_4D_Generation_via_Zero_Shot_Camera_Control]] | trajectory guidance + motion-channel filtering + self-correction |
| 18 | 3DTrajMaster (ICLR 2025) | 多实体 3D trajectory binding 强 baseline。StoryMotion 的主次关系与 subject-relative framing 需要和这种 6DoF 多实体控制区分。完整链接见：[[analysis/ICLR_2025/3DTrajMaster_Mastering_3D_Trajectory_for_Multi_Entity_Motion_in_Video_Generation]] | 6DoF entity pose sequence + gated self-attention object injector |
| 19 | Direct-a-Video (SIGGRAPH 2024) | camera movement + object motion 解耦控制基础竞品。完整链接见：[[analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion]] | trainable camera module + cross-attention object trajectory modulation |
| 20 | MotionCtrl (SIGGRAPH 2024) | 全局相机 / 局部物体分层控制 baseline。完整链接见：[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation]] | camera RT 注入 temporal Transformer，object trajectory 注入 convolution |
| 21 | SynCamMaster (ICLR 2025) | 多相机同步生成支线，StoryMotion 需要 multi-camera 或多视角一致性时再读。完整链接见：[[analysis/ICLR_2025/SynCamMaster_Synchronizing_Multi-Camera_Video_Generation_from_Diverse_Viewpoints]] | DiT 中插入跨视图自注意力，相机外参嵌入驱动多视角同步 |
| 22 | Director3D (NeurIPS 2024) | Text → camera trajectory + 3D scene 的完整生成管线，适合 StoryMotion 扩到 scene generation 时读。完整链接见：[[analysis/NEURIPS_2024/Director3D_Real-world_Camera_Trajectory_and_3D_Scene_Generation_from_Text]] | 轨迹扩散 Transformer → 高斯多视角扩散 → SDS++ refine |
| 23 | Beyond Static Scenes (arXiv 2025) | camera-controllable background + human foreground 合成启发，适合后续从 latent motion 扩到 video/background。完整链接见：[[analysis/arxiv_2025/Beyond_Static_Scenes_Camera_controllable_Background_Generation_for_Human_Motion]] | camera pose Plucker control + background generation / consistency multitask |
| 24 | Free-Form Motion Control (arXiv 2025) | 合成数据与 6D camera/object 控制对照，适合设计数据和对比实验。完整链接见：[[analysis/arxiv_2025/Free_Form_Motion_Control_A_Synthetic_Video_Generation_Dataset_with_Controllable_Camera_and_Object_Motions]] | synthetic dataset + disentangled camera/object motion controllers |

---

## B-Tier（选读）

| # | 论文 | 选读理由 | 核心方法 |
|---:|---|---|---|
| 25 | Generative Camera Dolly (ECCV 2024) | 极端 camera movement 下的新视角合成参考，可用于评估 camera edit 的边界。完整链接见：[[analysis/ECCV_2024/Generative_Camera_Dolly_Extreme_Monocular_Dynamic_Novel_View_Synthesis]] | 极端单目动态 novel view synthesis |
| 26 | AsymLoc (CVPR 2026) | 高效视觉定位支线，用于移动端 / 实时 camera localization。完整链接见：[[analysis/CVPR_2026/AsymLoc_Towards_Asymmetric_Feature_Matching_for_Efficient_Visual_Localization]] | 非对称特征匹配实现高效视觉定位 |
| 27 | Grounded Latents (CVPR 2026) | entity-centric 4D latent 启发，适合 StoryMotion 扩到 multi-entity role hierarchy。完整链接见：[[analysis/CVPR_2026/Grounded_Latents_for_Entity_Centric_4D_Scene_Generation]] | 每个前景 actor 一个 grounded latent，分阶段布局/特征/运动扩散 |
| 28 | ConsisDrive (ICLR 2026) | 实例 mask / identity consistency 机制启发；不是 human-camera 直接竞品。完整链接见：[[analysis/ICLR_2026/ConsisDrive_Identity_Preserving_Driving_World_Models_for_Video_Generation_by_Instance_Mask]] | 3D box projection instance mask 控制注意力与损失 |
| 29 | AnchorCrafter (TVCG 2026) | HOI 视频生成与物体外观保持启发；不是直接 camera-framing 竞品。完整链接见：[[analysis/IEEE_TRANSACTIONS_ON_VISUALIZATION_AND_COMPUTER_GRAPHICS_2026/AnchorCrafter_Animate_CyberAnchors_Saling_Your_Products_via_Human_Object_Interacting_Video_Generation]] | object appearance aware HOI generation + disentangled cross-attention |
| 30 | CoMoVi (arXiv 2026) | 3D motion 与 realistic video co-generation 启发；适合后续从 motion latent 扩展到 video。完整链接见：[[analysis/arxiv_2026/CoMoVi_Co_Generation_of_3D_Human_Motions_and_Realistic_Videos]] | dual-branch diffusion for 3D motion and video co-generation |
| 31 | MoMask (CVPR 2024) | 仅作为 motion token 背景保留，不作为 camera geometry 核心阅读。完整链接见：[[analysis/CVPR_2024/MoMask_Generative_Masked_Modeling_of_3D_Human_Motions]] | RVQ 多层离散运动 token，M-Transformer 并行基座预测，R-Transformer 逐层精细化 |
| 32 | HumanTOMATO (ICML 2024) | 仅用于理解 whole-body motion token 与 TMR alignment；核心机制阅读留在 MoDebug list。完整链接见：[[analysis/ICML_2024/HumanTOMATO_Text-Aligned_Whole-Body_Motion_Generation]] | H2VQ 分层离散编码身体 / 手 / 脸，TMR 提供运动感知语言先验与序列级对齐 |

---

## 与 StoryMotion 当前路线的对应关系

| StoryMotion 问题 | 必读参考 | 作用 |
|---|---|---|
| camera token 应编码什么 | VGGT / D4RT | camera pose、depth、point map、timestamp-aware dynamic geometry |
| token-level camera edit 如何对比 pixel-level edit | Vid-CamEdit / Generative Camera Dolly | 提供 pixel-level camera trajectory editing baseline 和极端运动边界 |
| subject-relative framing 如何形式化 | Toric Space / Pulp Motion | 把 framing 写成主体相对屏幕空间约束，而不是泛化 camera pose regression |
| human-camera joint control 竞品 | Pulp Motion / ActCam / AdaViewPlanner / E.T. / GenDoP / ShotVerse / CT-1 | 约束 StoryMotion 新颖性：不能只声称 joint camera-human，而要证明三模式条件补全与叙事/主次关系条件 |
| branch-mask inpainting 机制 | COIN / CondMDI / MotionFix / ConsisDrive | 为 Mode A/B/C 的 observed branch 保持、soft repair、sampler 和 identity mask 设计提供机制参考 |
| 多实体主次关系控制 | 3DTrajMaster / Direct-a-Video / MotionCtrl / Grounded Latents | 提供 object/entity trajectory baseline，StoryMotion 应强调 subject-relative framing 与 narrative role hierarchy |
| human motion 与 camera motion 如何解耦 | PAGE-4D / D4RT | 用 dynamic mask、camera frame、time query 区分相机运动和主体运动 |
| story-time / camera-time 如何解耦 | BulletTime / CamDirector / 3D Scene Prompting / Taming Video Models | 世界时间、相机观察、场景记忆和零样本 camera control 的强竞品与评估约束 |
| 几何 backbone 如何鲁棒迁移 | Emergent Outlier View Rejection / VGGT-Segmentor / LILA | noisy view 过滤、cross-view segmentation、动态 3D feature 监督 |

---

## 推荐阅读路径

**若服务 StoryMotion camera token MVP：**

```text
VGGT → Vid-CamEdit → D4RT → PAGE-4D
```

**若服务当前 continuous stage2 / official bridge：**

```text
Pulp Motion → COIN → ActCam → AdaViewPlanner → CT-1 → BulletTime
```

**若服务多实体 / 主次关系扩展：**

```text
Toric Space → 3DTrajMaster → Direct-a-Video → MotionCtrl → Grounded Latents → ConsisDrive
```

**若服务 StoryMotion camera-editing 对比实验：**

```text
Vid-CamEdit → Generative Camera Dolly → Director3D → CamDirector
```

**若服务动态 3D / 多视角扩展：**

```text
VGGT → D4RT → PAGE-4D → 3D Scene Prompting → Taming Video Models → CamDirector
```
