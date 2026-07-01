---
title: "CameraShotEdit: camera-shot-aware 3D human motion editing"
created: 2026-06-05T00:26:11+08:00
updated: 2026-06-05T00:26:11+08:00
status: proposal
hypothesis: 现有 2024+ 工作已覆盖 human-camera joint generation、human-conditioned camera planning、camera-controlled video 和 human motion editing，但尚未覆盖 source 3D human motion + edit instruction + shot instruction 下的 edit-aware cinematography；可守切入点是联合决定人体编辑、镜头规划和构图修复，而不是首次生成人体-相机序列。
tags:
  - camera_movement_generation
  - human_motion_editing
  - cinematography
  - multi_shot_camera
  - research_idea
source_notes:
  - "[[ideas/poool/2026-06-03_camera-movement-generation-survey|Camera Movement Generation 系统调研]]"
  - "[[ideas/poool/2026-06-04_camera-movement-generation-llm-audit-merged|Camera Movement Generation LLM 审查与合并整理]]"
  - "[[2026-06-04_storymotion_cinematic_section_graph_plan|StoryMotion Cinematic Section Graph Plan]]"
source_papers:
  - "[[analysis/SIGGRAPH_Asia_2024/MotionFix_Text-Driven_3D_Human_Motion_Editing|MotionFix]]"
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing-aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]"
  - "[[analysis/ECCV_2024/E.T._the_Exceptional_Trajectories_Text-to-camera-trajectory_generation_with_character_awareness|E.T. / DIRECTOR]]"
  - "[[analysis/ICCV_2025/GenDoP_Auto-regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography|GenDoP / DataDoP]]"
  - "[[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes|AdaViewPlanner]]"
  - "[[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image-to-Video_Generation|MotionCanvas]]"
  - "[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]"
  - "[[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text-to-Video_Generation|CameraCtrl]]"
  - "[[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text-Driven_Multi-Shot_Video_Creation|ShotVerse]]"
---

# CameraShotEdit: camera-shot-aware 3D human motion editing

> [!abstract] 结论先行
> **严格意义上，已有工作还没有覆盖“source 3D human motion + motion edit instruction + camera shot / movement instruction -> edited human motion + multi-shot camera trajectory”的完整任务。** 2024 年以后最接近的是两条线：一条是 [[analysis/ICLR_2026/Pulp_Motion_Framing-aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]、[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]、Auteur、[[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes|AdaViewPlanner]] 的 human-camera generation / planning；另一条是 [[analysis/SIGGRAPH_Asia_2024/MotionFix_Text-Driven_3D_Human_Motion_Editing|MotionFix]] 等 motion edit。它们没有把 **source motion preservation、editing success、screen framing、multi-shot continuity** 放进同一个编辑闭环。

检索时点：2026-06-05 Asia/Shanghai。  
调研方式：本地 KB 覆盖检查 + 3 个阅读 agent 分别检索 human motion、video generation、camera/cinematography control + DeepSeek 审稿式讨论 + arXiv/CVF/OpenReview/项目页交叉核验。

---

## 0. 是否已有覆盖

### 0.1 简短判断

没有直接覆盖，但不是空白方向。

更准确的边界是：

- **已有覆盖 A：human-camera joint generation**。Pulp Motion 将任务定义为 text-conditioned human motion + camera trajectory joint generation，并用投影得到的 on-screen framing 辅助模态桥接两者；Towards Storytelling Animations 联合生成两个角色与相机运动；这类工作不是 source motion edit。
- **已有覆盖 B：human-motion-conditioned camera planning**。E.T. / DIRECTOR 给定文本和角色轨迹生成 camera trajectory；Auteur 用 language + coarse human motion 生成 human-centric camera DSL keyframes，再转为 6-DoF camera；AdaViewPlanner 用 4D human motion 和文本做 viewpoint planning；这些工作把 motion 当条件，不编辑 motion。
- **已有覆盖 C：camera-controlled video / re-camera**。MotionCtrl、CameraCtrl、MotionCanvas、TrajectoryCrafter、Latent-Reframe 等能控制或重定向视频相机，但不输出可编辑的 3D human motion，也不保证 motion edit 保真。
- **已有覆盖 D：3D human motion edit**。MotionFix 等处理 source motion + edit text，但不建模 camera track、shot boundary、framing、out-of-frame failure。

因此，**“带 camera 分镜/运动的 edit”如果指 3D motion asset 层面的 joint editing，目前还没有单篇工作完整覆盖。** 如果只指“先编辑 motion，再拿 edited motion 去生成 camera”，则 naive pipeline 已经可由 MotionFix + E.T./Auteur/AdaViewPlanner 近似实现；新方案必须证明 joint edit 的必要性。

### 0.2 最容易打掉 gap 的工作

- **Auteur**：外部新工作 [Auteur](https://arxiv.org/abs/2606.01900) 已经用 human-centric camera parameterization 和 DSL，把语言与 coarse human motion 映射到 6-DoF camera trajectory。它不编辑人体，但如果接一个 MotionFix，就会形成很强的两阶段 baseline。
- **Pulp Motion**：外部工作 [Pulp Motion](https://arxiv.org/abs/2510.05097) 已经明确做人-相机联合生成和 screen framing latent。它不是 edit，但其 auxiliary sampling 很容易被改造成 editing refiner。
- **StoryMotion-CSG**：本地已有 [[2026-06-04_storymotion_cinematic_section_graph_plan|StoryMotion-CSG]] 做 local human-camera timeline asset repair。CameraShotEdit 必须避免重复它的“保护已批准 interiors + boundary repair”主张。

### 0.3 与 StoryMotion-CSG 的关系

CameraShotEdit 不应定位成已有 human-camera asset 的局部修复；这是 StoryMotion-CSG 的空间。

CameraShotEdit 的边界应是：

- 输入可以只有 source / generated 3D human motion，不一定已有 camera track。>- 用户给的是 motion edit instruction 与 shot instruction，例如“把走路改成跑步；先远景跟拍，再切中景环绕，最后特写停步”。
- 输出是 edited human motion、shot boundary annotations、每个 shot 的 6-DoF camera / FOV track、screen-space framing targets。
- 重点是 **motion edit 与 shot planning 的联合决策**：哪些动作变化应由人体编辑完成，哪些视觉变化可由 camera reframe 吸收；哪些镜头保留，哪些重规划。

一句话区分：

> StoryMotion-CSG 修复已经批准的 human-camera timeline；CameraShotEdit 从 source motion 和分镜指令出发，生成一个经过 motion edit 后仍满足多镜头构图约束的 cinematographic motion asset。


>[!note]
想到有趣的做法，将human motion和camera motion的token拼接，文本作为condition，可以控制模型进行统一的human&camera的motion生成。例如
+ unified framework for human&camera motion generation&edit（先找到灵感来源的paper）
	+ generation
		+ \<text, human> + \<masked camera> -> camera
		+ \<text, camera> + \<masked human> -> human
		+ \<text> + \<masked camera, masked human> -> camera, human
	+ edit
		+ token level的edit
+ further
	+ 将text纳入unified framework，作 generation & understanding
		+ 问题：understanding要做什么
		+ 多数据集能力如何挖掘
		+ 能否类似于posefix、motionfix，让模型理解camera的edit（不知道现有工作是否cover）

>[!疑惑]
>1. 直接将camera motion按照human motion的范式处理是否可行？两者concate后一起生成是否可行？有研究这么做吗？
>2. human motion+camera motion后，camera渲染视图是否参与training时的network参数优化？使用的是监督学习吗，gt来自于数据集吗？是否有工作进行自监督弱监督无监督的探索？
>3. [[2026-06-04_storymotion_cinematic_section_graph_plan]]的方案设计太虚头巴脑，自说自话，缺乏学术严谨，本md的idea设计合理许多。先让agent大刀阔斧修缮[[2026-06-04_storymotion_cinematic_section_graph_plan]]，只保留核心、有依据、有价值的信息和idea，去掉无意义的过于乐观的规划。
>4. camera + StoryMotion两部分的md涉及的工作，给出一个核心推荐阅读顺序列表md

---

## 1. Idea decomposition and association

### 1.1 问题重述

给定一段 3D human motion $M_0$，可选已有 camera track $C_0$，自然语言动作编辑指令 $e_m$，以及 camera shot / movement 指令 $e_c$，系统输出：

```text
edited human motion M*
+ multi-shot camera trajectory C*
+ shot boundary / shot type annotations S*
+ screen-space framing constraints F*
+ optional rendered preview / video-control conditions
```

核心不是“让视频更电影感”，而是把 motion edit 的成功条件从 body-space 扩展到 screen-space：

- 人体动作确实按 $e_m$ 被编辑。
- 未编辑身体部分和未编辑时间段尽量保留 source motion。
- 主体在每个 shot 中满足 shot size、screen position、headroom、visibility、look-at 等构图约束。
- shot boundary 的 cut / transition / camera acceleration / FOV schedule 可控。
- 简单两阶段 pipeline 失败时，系统可联合调整 human root / timing / local pose 与 camera path。

### 1.2 子问题拆解

| 子问题                         | 输入                                   | 输出                                    | 关键难点                                              | 现有支撑                                                    |
| --------------------------- | ------------------------------------ | ------------------------------------- | ------------------------------------------------- | ------------------------------------------------------- |
| Motion edit                 | source motion + edit text            | edited motion                         | 编辑成功与 source preservation 的平衡                     | MotionFix                                               |
| Shot planning               | edited/source motion + shot text     | shot list + target framing            | 文本分镜到 shot size / angle / movement / boundary 的落地 | E.T., GenDoP, Auteur, ShotVerse                         |
| Camera trajectory synthesis | shot list + human trajectory         | 6-DoF camera + FOV                    | 保持主体构图，避免出框，平滑运镜                                  | Pulp Motion, TSA, AdaViewPlanner                        |
| Joint repair                | edited motion + camera + constraints | repaired motion/camera                | 决定改人还是改相机；约束冲突时报告失败                               | StoryMotion-CSG 思路，但任务边界不同                              |
| Preview / actuator          | motion + camera                      | video / render / controller condition | 视频一致性、遮挡补全、身份保持                                   | MotionCtrl, CameraCtrl, MotionCanvas, TrajectoryCrafter |

### 1.3 可守 novelty

不要 claim：

- 首次 joint human-camera generation。
- 首次 camera trajectory generation。
- 首次 cinematic video generation。
- 首次 local human-camera asset repair。

可以 claim：

- 首个明确以 **source 3D human motion editing + cinematography instruction** 为输入的任务定义和 benchmark。
- 首个同时评估 **edit success、source preservation、screen framing、shot continuity、out-of-frame rate** 的 motion edit setting。
- 一个 **Edit-then-Plan with Joint Repair** 框架，在 naive pipeline 失败的出框、构图跳变、shot transition 断裂、camera-only 过度补偿场景中联合优化 human 和 camera。

---

## 2. Real scenarios and pain points

### 2.1 典型场景

- 动画 / 游戏 previs：已有一段走路、打斗或舞蹈 motion，导演要把动作改成更强烈，同时自动生成分镜和运镜。
- 短视频 / 虚拟人内容制作：生成或 mocap 得到的人体动作质量可用，但缺 camera shot design；用户希望用文本快速指定“先远景、再推近、最后绕拍”。
- DCC / Unreal Sequencer 辅助：motion artist 修改动作后，希望 camera track 自动跟随重规划，而不是手工重新 keyframe。
- 视频生成后端控制：把 3D motion + camera track 转为 CameraCtrl / MotionCanvas / MotionCtrl 可执行条件，得到 preview video。

### 2.2 现有痛点

- Motion edit 方法只看 skeleton / body-space，编辑后可能在屏幕上出框或构图崩掉。
- Camera planning 方法默认 human trajectory 已定，不会反过来告诉 motion editor“这个 root shift 会导致原分镜无法成立”。
- Camera-controlled video 方法大多执行给定 camera path，不负责生成或修正 motion edit。
- 多镜头分镜里 cut / transition / shot scale 的评估不在 motion editing benchmark 中。
- naive pipeline 可用，但会把错误传递下去：先 edit 出一个 camera 不可拍的 motion，再强行规划 camera，可能导致运镜过急、FOV 抖动、主体出框或 shot boundary 断裂。

---

## 3. Related-work support and research opportunities

### 3.1 Related-work overview

Human motion / editing 侧：

- [[analysis/SIGGRAPH_Asia_2024/MotionFix_Text-Driven_3D_Human_Motion_Editing|MotionFix]]：用 source motion + edit text 的三元组训练 conditional diffusion，是最直接的 motion edit baseline；外部论文页也明确其目标是给定 3D human motion 和文本修改描述后生成 edited motion：[MotionFix](https://arxiv.org/abs/2408.00712)。
- InterEdit / MotionLab / SimMotionEdit 一类工作继续拓展 motion edit、多人体或交互一致性，但 camera / framing 不是变量。

Human-camera generation / camera planning 侧：

- [[analysis/ICLR_2026/Pulp_Motion_Framing-aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]：把 human motion 与 camera trajectory 放入 joint generation，并用 on-screen framing 作为辅助模态；是最重要的挤压项，但它不是 source edit。
- [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]：联合生成两个角色和 camera，用 Toric 表示建模构图；仍是 full sequence synthesis。
- [[analysis/ECCV_2024/E.T._the_Exceptional_Trajectories_Text-to-camera-trajectory_generation_with_character_awareness|E.T. / DIRECTOR]]：从 text + character trajectory 到 camera trajectory；强支撑“根据 human motion 规划 camera”的可行性。
- [[analysis/ICCV_2025/GenDoP_Auto-regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography|GenDoP / DataDoP]]：从文本 + RGBD 生成自由移动艺术相机轨迹；外部论文页显示 DataDoP 包含 29K real-world shots、depth maps 和 detailed captions：[GenDoP](https://arxiv.org/abs/2504.07083)。
- Auteur：语言 + coarse human motion 到 human-centric camera DSL keyframes，再转 6-DoF camera，是最强的新近 camera-framing baseline。
- [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes|AdaViewPlanner]]：利用视频扩散先验做 4D human scene viewpoint planning。
- [[analysis/arxiv_2026/ShotVerse_Advancing_Cinematic_Camera_Control_for_Text-Driven_Multi-Shot_Video_Creation|ShotVerse]]：Plan-then-Control 多镜头框架；外部论文页显示它用 VLM planner 生成 globally aligned camera trajectories，再由 controller 渲染多镜头视频：[ShotVerse](https://arxiv.org/abs/2603.11421)。

Video generation / actuator 侧：

- [[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]：独立控制 camera motion 与 object motion，适合作为 camera + human control 的视频生成后端；外部论文页也强调 camera pose / trajectory 是 appearance-free condition：[MotionCtrl](https://arxiv.org/abs/2312.03641)。
- [[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text-to-Video_Generation|CameraCtrl]]：Plucker camera embedding 注入视频扩散 temporal attention，可作为 camera trajectory actuator。
- [[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image-to-Video_Generation|MotionCanvas]]：用户驱动的 scene-space camera / object motion 设计转成 video diffusion conditioning；外部论文页明确它面向 I2V cinematic shot design：[MotionCanvas](https://arxiv.org/abs/2502.04299)。
- Latent-Reframe、TrajectoryCrafter、Vid-CamEdit、ReCamMaster：可做已有视频重运镜，但不编辑 3D human motion。

### 3.2 Support points

- Pulp Motion 证明 screen-space framing 是连接 human motion 和 camera trajectory 的自然桥梁。
- E.T. / GenDoP / Auteur 证明 human trajectory / RGBD / language 可以驱动 cinematographic camera planning。
- MotionFix 证明 source motion + edit text 的三元组数据和编辑评估是可做的。
- MotionCtrl / CameraCtrl / MotionCanvas 证明生成出的 camera path 可以进入视频扩散后端执行。

### 3.3 Research opportunities

1. **任务定义机会**：把 motion edit 从 body-space task 扩展为 body-space + screen-space task。
2. **评估机会**：建立 camera-aware motion edit benchmark，而不是只看 motion retrieval / FID。
3. **方法机会**：用 deterministic joint repair 打掉 naive pipeline 的 failure cases，避免一开始押注难以训练的 full joint diffusion edit model。
4. **交互机会**：让用户指定 shot pattern，同时保留 motion editor 对动作内容的控制。

---

## 4. Proposed method: Edit-then-Plan with Joint Repair

### 4.1 输入输出

输入：

```text
M0: source 3D human motion, joints / SMPL / root trajectory
C0: optional source camera track
em: motion edit instruction
ec: camera shot / movement instruction
L: optional locked mask / source preservation mask
```

输出：

```text
M*: edited 3D human motion
C*: multi-shot camera trajectory, SE(3) + intrinsics / FOV
S*: shot boundary, shot type, transition type
F*: target screen framing, bbox scale / center / headroom / visibility
R*: violation report and optional preview/video-control conditions
```

### 4.2 Pipeline

**Stage 1: Motion edit proposal**

- 用 MotionFix-like editor 生成 $M_e$。
- 保留 source preservation mask：未编辑关节、未编辑片段、root trajectory 是否允许改变。
- 输出 edit confidence：如果动作编辑必须大幅改变 root / timing，就把相关 shot 标记为高风险。

**Stage 2: Shot planner**

- 将 $e_c$ 解析为 shot list：shot type、duration、transition、subject target、movement primitive。
- 可用 rule + MLLM / DSL 做第一版，不训练大模型。
- 对每个 shot 生成目标 framing：screen center、bbox height ratio、headroom、view angle、look-at target、safe margin。

**Stage 3: Camera trajectory planner**

- 根据 $M_e$ 的 root / pelvis / torso / head trajectory 生成每个 shot 的 camera keyframes。
- 表示建议：
  - world-space camera: $T_t \in SE(3)$ + FOV。
  - human-centric parameters: distance、azimuth、elevation、screen offset、shot scale。
  - optional Toric / DSL representation for framing-friendly control。
- 先用 deterministic spline / constrained optimization 生成可解释 baseline，再考虑学习 refiner。

**Stage 4: Joint violation detector**

计算每帧和每个 shot boundary 的 violation：

```text
motion_loss      = edit_target_error + source_preservation_error
framing_loss     = bbox_center_error + bbox_scale_error + headroom_error
visibility_loss  = out_of_frame + occlusion_proxy
camera_loss      = velocity / acceleration / jerk / FOV jerk
boundary_loss    = shot_transition_error + projected_motion_jump
```

关键是判断 violation 应由谁吸收：

- 如果 motion edit 只造成 screen framing 问题，优先 camera reframe。
- 如果 camera reframe 需要极端 FOV / 急加速，释放局部 human root / timing。
- 如果两者冲突，输出 failure report，而不是强行平滑。

**Stage 5: Joint repair**

v0 使用 deterministic optimization：

```text
min_{delta_M, delta_C} 
  w_edit      * L_edit(M0, M*; em)
+ w_keep      * L_preserve(M0, M*, L)
+ w_frame     * L_framing(P(M*, C*), F*)
+ w_vis       * L_visibility(P(M*, C*))
+ w_cam       * L_camera_smooth(C*)
+ w_boundary  * L_shot_boundary(M*, C*, S*)
+ w_motion    * L_motion_smooth(M*)
```

约束：

- 只允许修改 editable joints / editable frames / editable camera segments。
- camera FOV 和 acceleration 有物理上限。
- human foot contact、root velocity、身体平衡有硬或软约束。
- locked region 近零漂移。

可选 learned refiner：

- 小 Transformer / diffusion refiner 只接收 violation window。
- 目标是自然度和减少 optimizer artifact，不承担主要 novelty。

### 4.3 为什么不直接做 joint diffusion edit model

DeepSeek 讨论给出的强结论：v0 不应押注 full joint diffusion edit。

原因：

- 缺少 source motion + edit text + source/target camera + shot instruction 的配对数据。
- human pose、camera SE(3)、FOV、shot boundary 是异构状态空间，统一扩散训练风险高。
- shot boundary 是离散结构，直接并入连续扩散会让数据和模型复杂度同时上升。
- deterministic planner + repair 更容易分解验证，也更容易证明 naive pipeline 的失败点。

因此 v0 推荐主线：

> **Edit-then-Plan with Joint Repair**：先生成 motion edit proposal 和 shot/camera proposal，再用 screen-space 与 body-space 约束做联合修复。

---

## 5. Benchmark: CameraShotEdit-Bench-v0

### 5.1 数据构造

目标不是伪装成真实电影数据集，而是构造可量化的 controlled proxy。

数据建议：

- Source motion：AMASS / HumanML3D / BABEL 中 200 条 4-8 秒动作，覆盖 walk、run、turn、jump、sit/stand、dance、gesture。
- Motion edit：从 MotionFix edit text 模板和手写规则生成 10-20 类编辑，例如 walk->run、add jump、turn around、raise arm、kick、crouch。
- Shot instruction：5 类模板：
  - single medium follow shot
  - wide-to-medium two-shot with cut
  - wide-medium-close three-shot sequence
  - orbit / truck / push-in moving shot
  - static-to-handheld style reframe
- Camera source：
  - 无 camera track：测试 from-motion shot generation。
  - 中性 camera track：测试 source camera adaptation。
  - 故意 corrupt camera track：测试 joint repair。
- 真实 sanity check：抽 20-50 条 E.T. / PulpMotion / TSA / AIST++ / BEDLAM 可用样本做外推验证，不用于主训练。

### 5.2 Baselines

| Baseline | 做法 | 预期失败点 |
|---|---|---|
| MotionFix only + static camera | 只编辑人体，camera 不动 | 出框、构图差 |
| MotionFix + E.T./Auteur-style camera planner | 先编辑 motion，再重新规划 camera | source camera 丢失、shot boundary 不稳、camera 过度补偿 |
| Camera-only reframe | 固定 edited motion，只优化 camera | 极端 FOV / jerk / out-of-frame 仍可能发生 |
| Human-only repair + camera smoothing | 只修 motion，再平滑 camera | screen-space discontinuity 未被显式优化 |
| Full regenerate | 直接 joint generate human-camera | source preservation 差 |
| StoryMotion-CSG-like local repair | 有完整 timeline 时做局部修复 | 不适合 from-motion shot planning，可作为资产编辑对照 |
| CameraShotEdit variants | 去 joint repair、去 framing loss、去 shot boundary loss、固定 buffer | 验证各模块必要性 |

### 5.3 Metrics

Motion / edit：

- Edit success：动作分类器 + text-motion evaluator + 10% 人工标注。
- Source preservation：未编辑关节 MPJPE、root drift、velocity drift、locked frame drift。
- Motion naturalness：foot contact error、acceleration、jerk、FID / diversity。

Camera / framing：

- Framing quality：bbox center error、bbox height ratio error、headroom error、look-at error。
- Out-of-frame rate：任一关键关节或 bbox 超出 viewport 的帧比例。
- Camera smoothness：translation / rotation velocity、acceleration、jerk、FOV jerk。
- Shot compliance：shot type classifier / heuristic 是否匹配 wide / medium / close / orbit / push-in。
- Shot continuity：transition boundary 的 projected subject jump、camera discontinuity、scale pop。

System / workflow：

- Violation repair success：修复前后 violation count。
- Tradeoff report quality：无法同时满足约束时是否正确指出冲突。
- Human study：编辑自然度、分镜合理性、是否比 naive pipeline 更可用。

### 5.4 最小成功标准

MVP 不需要漂亮视频，只需要证明：

- 在至少 200-400 个合成 edit cases 上，CameraShotEdit 比 naive pipeline 显著降低 out-of-frame rate 和 framing error。
- Source preservation 不显著差于 MotionFix-only baseline。
- Camera jerk / FOV jerk 不显著高于 camera-only planner。
- 在 20-50 个真实 paired sanity cases 上，failure mode 与合成 benchmark 一致。

---

## 6. Risk analysis

| 风险 | 严重程度 | 必须解决/可绕过 | 处理方案 | 对路线影响 |
|---|---|---|---|---|
| Naive pipeline 已经足够好 | 高 | 必须解决 | 专门构造出框、shot scale pop、FOV 过度补偿、boundary 断裂 cases，证明 joint repair 优势 | 决定 novelty 是否成立 |
| 数据太合成 | 高 | 必须缓解 | 主 benchmark 明确叫 controlled proxy；加入真实 paired sanity check | 影响可信度 |
| Shot instruction 太主观 | 中 | 可绕过 | v0 只做有限 shot templates 和可量化 framing targets | 降低范围但提高可验证性 |
| Joint optimizer 牺牲 motion edit | 高 | 必须解决 | 使用 preservation mask 和 edit loss，报告 tradeoff curve | 影响编辑任务本质 |
| Camera repair 产生不自然运镜 | 中 | 必须解决 | 限制 acceleration、jerk、FOV；引入 camera smoothness loss | 影响 demo |
| StoryMotion-CSG 重复 | 高 | 必须解决 | 明确本方案 from-motion + shot planning，不做已批准 asset 的 local dirty propagation | 影响内部选题定位 |
| 视频后端不稳定 | 低 | 可绕过 | v0 以 3D render / viewport projection 为主，video diffusion 只做 optional preview | 避免被 actuator 拖垮 |

---

## 7. Strong contribution statement

可防守的一句话：

> **CameraShotEdit is the first camera-shot-aware 3D human motion editing framework that takes source motion, a motion edit instruction, and a cinematography instruction as input, then jointly produces an edited human motion and multi-shot camera trajectory while preserving source motion fidelity and satisfying screen framing, shot type, and boundary continuity constraints.**

中文版本：

> **CameraShotEdit 首次把 3D human motion edit 明确定义为 body-space 与 screen-space 的联合编辑问题：在 source motion、动作编辑指令和分镜运镜指令下，同时输出 edited motion 与 multi-shot camera trajectory，并用 source 保真、构图、出框率和镜头连续性共同评价。**

更保守版本：

> **CameraShotEdit introduces a camera-aware benchmark and an Edit-then-Plan with Joint Repair baseline for 3D human motion editing under cinematography instructions.**

---

## 8. Near-term executable steps

1. **复现实验前的覆盖验证**：用 MotionFix 编辑 20 条 HumanML3D motion，再用 E.T./Auteur-style rule planner 生成 camera，统计出框率、bbox scale pop、camera jerk；若 naive pipeline 已足够好，收窄到 failure-aware joint repair。
2. **实现 projection evaluator**：给定 skeleton + SE(3) + FOV，输出 bbox center、height ratio、headroom、out-of-frame、projected velocity jump。
3. **构建 5 类 shot templates**：先不训练，手写从 shot type 到 framing target / camera spline 的规则。
4. **实现 joint repair v0**：只优化 camera pose + FOV；v1 再释放 human root / timing；v2 释放局部 pose。
5. **写 CameraShotEdit-Bench-v0**：保存 source motion、edit text、shot instruction、edited proposal、camera proposal、violation report、repair output。
6. **对比 StoryMotion-CSG**：把本方案的 from-motion planning cases 与 CSG 的 local timeline repair cases 分开，避免内部路线打架。

---

## 9. Evidence links

外部主证据：

- [MotionFix: Text-Driven 3D Human Motion Editing](https://arxiv.org/abs/2408.00712)
- [Pulp Motion: Framing-aware multimodal camera and human motion generation](https://arxiv.org/abs/2510.05097)
- [Auteur: Language-Driven Cinematographic Framing for Human-Centric Video Generation](https://arxiv.org/abs/2606.01900)
- [GenDoP: Auto-regressive Camera Trajectory Generation as a Director of Photography](https://arxiv.org/abs/2504.07083)
- [ShotVerse: Advancing Cinematic Camera Control for Text-Driven Multi-Shot Video Creation](https://arxiv.org/abs/2603.11421)
- [MotionCtrl: A Unified and Flexible Motion Controller for Video Generation](https://arxiv.org/abs/2312.03641)
- [MotionCanvas: Cinematic Shot Design with Controllable Image-to-Video Generation](https://arxiv.org/abs/2502.04299)

DeepSeek 讨论摘要：

- gap 成立但必须防 naive pipeline：MotionFix + E.T./Auteur/AdaViewPlanner 是强 baseline。
- 新方案必须强调 edit preservation 和 joint repair，而不是 camera generation。
- 推荐 planner + deterministic repair + optional learned refiner，不推荐 v0 直接做 full joint diffusion edit。
- benchmark 必须包含 pipeline failure cases，并用真实 paired samples 做 sanity check。
