---
title: "StoryMotion Cinematic Section Graph Plan"
created: 2026-06-04T16:40:00+08:00
updated: 2026-06-05T00:00:00+08:00
status: active
hypothesis: "CSG 的 novelty 不在首次联合生成人体与相机运动，而在已有 human-camera timeline asset 中，局部编辑后保护已批准 interiors、仅在必要 boundary buffers 内做 contact- and framing-consistent local repair，并通过 dirty propagation、cache、undo 和 review scope 支撑多轮制作迭代。"
source_notes:
  - "[[ideas/StoryMotion/archived/v3/2026-06-03_storymotion_canonical_plan|StoryMotion ASG Canonical Plan]]"
  - "[[ideas/camera/2026-06-05_camera-movement-generation-system-survey-llm-audit-merged|Camera Movement 系统调研]]"
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing-aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|TSA]]"
  - "[[analysis/ECCV_2024/E.T._the_Exceptional_Trajectories_Text-to-camera-trajectory_generation_with_character_awareness|E.T.]]"
  - "[[analysis/ICCV_2025/GenDoP_Auto-regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography|GenDoP]]"
  - "[[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes|AdaViewPlanner]]"
  - "[[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image-to-Video_Generation|MotionCanvas]]"
  - "[[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text-to-Video_Generation|CameraCtrl]]"
  - "[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In-betweening_with_Diffusion_Models_CondMDI|CondMDI]]"
  - "[[analysis/SIGGRAPH_Asia_2024/MotionFix_Text-Driven_3D_Human_Motion_Editing|MotionFix]]"
tags:
  - StoryMotion
  - human_camera_motion
  - cinematic_section_graph
  - motion_editing
  - camera_trajectory
---

# StoryMotion: 影视化段落图的局部人机编辑修复

> [!abstract] 定位
> 本文档是 StoryMotion CSG 主线方案。[[ideas/StoryMotion/archived/v3/2026-06-03_storymotion_canonical_plan|2026-06-03 ASG 方案]] 保留为 human-motion-only 地基。CSG **不碰手绘 storyboard、不做 script-to-animation generation**，研究的是：**已有的 human-camera timeline asset 在局部编辑后，如何量化失效范围、保护已批准内容、仅在必要边界缓冲区做 world-space contact 与 screen-space framing 的联合修复**。

> [!warning] 硬约束
> CSG 不能 claim "首次 human-camera joint generation"、"理解电影镜头语言"、"从故事自动生成完整动画"。[[analysis/ICLR_2026/Pulp_Motion_Framing-aware_multimodal_camera_and_human_motion_generation|Pulp]]、[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|TSA]]、[[analysis/ECCV_2024/E.T._the_Exceptional_Trajectories_Text-to-camera-trajectory_generation_with_character_awareness|ET]]、[[analysis/ICCV_2025/GenDoP_Auto-regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography|GenDoP]]、[[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes|AdaViewPlanner]] 已覆盖或强挤压上述空间。CSG 的可守位置是：**局部编辑后保护已批准内容，并同时修复 world-space contact 与 screen-space framing**。

## 与 CameraShotEdit 的定位差异

CSG 与 [[ideas/StoryMotion/2026-06-05_camera-shot-edit|CameraShotEdit]] 是同一问题域下的两个不同切入点，必须严格区分：

| 维度 | CSG（本文） | [[ideas/StoryMotion/2026-06-05_camera-shot-edit\|CameraShotEdit]] |
|---|---|---|
| **输入** | 已有 human-camera timeline asset（已生成或已制作的完整序列） | source 3D human motion（可无 camera track）+ edit instruction + shot instruction |
| **触发条件** | 导演/动画师对已完成序列的某一段提出局部修改 | 创作者给定一段 motion 和分镜意图，需要同时做 motion edit 和 camera planning |
| **核心操作** | 量化编辑的失效传播范围 → 保护已批准 interiors → 仅在 boundary buffers 内联合修复 | 联合决定"哪些变化由人体编辑完成，哪些视觉变化由 camera reframe 吸收" |
| **camera track** | 已有（输入的一部分），可能被编辑连带失效 | 不一定有；shot instruction 驱动 camera planning 从零生成 |
| **输出** | 最小修改的 repaired human-camera asset + dirty radius + review scope | edited human motion + shot boundary annotations + 每个 shot 的 6-DoF camera track |
| **核心 novelty** | dirty propagation + protected interiors + cross-modal boundary repair | motion edit 与 shot planning 的联合决策 |
| **求解方式** | 确定性优化（QP/spline），不训练模型 | edit-then-plan pipeline，可能含学习组件 |

**一句话区分：**

> CSG 修复已经批准的 human-camera timeline——给定完整序列和局部修改指令，输出最小范围的修复；CameraShotEdit 从 source motion 和分镜指令出发——生成一个经过 motion edit 后仍满足多镜头构图约束的 cinematographic motion asset。

**两者的关系：** CSG 可以接收 CameraShotEdit 的输出作为输入——CameraShotEdit 生成初始 human-camera asset 后，导演提出局部修改，CSG 负责最小化修复。两者是 **生成 → 迭代修改** 的上下游关系，不是竞争关系。

## 缩写表

| 缩写 | 全称 | 含义 |
|---|---|---|
| ASG | Animation Section Graph | human-motion-only 的旧版 section graph 地基 |
| CSG | Cinematic Section Graph | human-camera section graph（新版主线） |
| DCC | Digital Content Creation | Blender / Maya / Unreal Sequencer 等制作环境 |
| FOV | Field of View | 相机视场角 / 焦距 |
| SE(3) | Special Euclidean group in 3D | 3D 刚体位姿（translation + rotation） |
| QP | Quadratic Programming | boundary repair 的确定性优化形式 |
| SMPL | Skinned Multi-Person Linear Model | 人体参数化模型 |
| CLaTr | Contrastive Language-Trajectory | E.T. 提出的语言-轨迹对比嵌入评估 |
| ET | E.T. / DIRECTOR | text-to-camera-trajectory with character awareness |
| TSA | Towards Storytelling Animations | joint human-camera synthesis |
| AVP | AdaViewPlanner | human-motion-conditioned viewpoint planning |

## 1. 问题定义

StoryMotion-CSG 解决的是 **human-camera 联合动画时间线中的局部编辑失效传播问题**。给定一段 3D human motion 段落和 camera trajectory 段落组成的序列——无论是由现有联合模型（[[analysis/ICLR_2026/Pulp_Motion_Framing-aware_multimodal_camera_and_human_motion_generation|Pulp]]、[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|TSA]]）生成的、在 DCC 中手工制作的、还是动捕采集的——对某一局部段落做编辑后，编辑点附近的段落边界会失效。更关键的是，这种失效是**跨模态的**：

- 修改角色的 root trajectory → 原有的 camera track 无法继续保持主体在画面中
- 修改 camera 的 push-in / orbit / reframe → 人体的 root/heading 可能需要配合调整才能让构图成立
- 人体边界在 3D 空间连续，不代表投影到屏幕上也连续——可能出现 bbox center jump、scale pop、headroom 突变、主体出画

**现有方法的不足：**
- 全量重生成：丢弃所有已批准的内容（full regenerate）
- 独立插值/融合：对人机和相机分别做 spline/crossfade，忽略跨模态耦合
- human-only ASG：只修人体边界，把所有失配压到人体 solver 上，不处理 camera 和 screen framing

**CSG 的贡献** 不在于生成，而在于**编辑契约**：将 human-camera asset 的局部修订形式化为 (1) 一个 Cinematic Section Graph 表示——节点带 locked interiors 和 editable boundary buffers，(2) 一个 dirty propagation 编译器——由编辑点出发自动识别哪些边界失效，(3) 一个 repair solver——最小化 world-space 和 screen-space 的不连续性，仅作用于受影响的 buffers。

## 2. 相关工作挤压

### 2.1 任务边界

| 工作 | 核心任务 | 与 CSG 的交集 | CSG 独有的 gap |
|---|---|---|---|
| [[analysis/ICLR_2026/Pulp_Motion_Framing-aware_multimodal_camera_and_human_motion_generation\|Pulp]] | text-conditioned human + camera joint generation，on-screen framing 辅助模态 | 已做人-相机联合生成和构图一致性 | 不处理已批准 interiors 的局部编辑、dirty propagation、undo/cache |
| [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions\|TSA]] | 两角色 + 动态相机的联合扩散生成 | 角色和相机在同一生成空间 | full sequence generation，非 post-edit local repair |
| [[analysis/ECCV_2024/E.T._the_Exceptional_Trajectories_Text-to-camera-trajectory_generation_with_character_awareness\|ET]] | text + character trajectory → camera trajectory | character-aware camera generation | 不生成人体，不做人体编辑后的相机修复 |
| [[analysis/ICCV_2025/GenDoP_Auto-regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography\|GenDoP]] | text/RGBD → director-style free-moving camera | camera-only planner | 不处理 human motion editing 和局部修复 |
| [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes\|AdaViewPlanner]] | 4D human motion + text → viewpoint planning | human-motion-conditioned viewpoint | 两阶段规划，不处理 DCC timeline edit protocol |
| [[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image-to-Video_Generation\|MotionCanvas]] | 用户指定 camera/object control → video | 可作为 actuator | 不自动决定 dirty radius，不保护 human/camera interiors |
| [[analysis/SIGGRAPH_2024/Flexible_Motion_In-betweening_with_Diffusion_Models_CondMDI\|CondMDI]] | mask-conditioned motion in-betweening | human boundary repair baseline | 不管 camera section、framing continuity、cache/undo |
| [[analysis/SIGGRAPH_Asia_2024/MotionFix_Text-Driven_3D_Human_Motion_Editing\|MotionFix]] | text-driven 3D human motion editing | human edit baseline | 不管 camera section 与 screen-space continuity |

**核心区分：** 现有生成器擅长产生完整序列；CSG 研究的是已生成或已批准的 asset 在局部修改后的最小重算和可审计版本稳定性。

### 2.2 挤压最紧的三个工作

- **Pulp Motion** (ICLR 2026)：已做 human-camera joint generation with on-screen framing。CSG 不与之竞争生成质量，而是指出 Pulp 生成的 asset 在导演要求局部修改时没有局部修复机制——这正是 CSG 解决的问题。CSG 可以接收 Pulp 的输出作为输入。
- **TSA** (CVPR 2026)：two-character + dynamic camera joint diffusion。同 Pulp：生成完整序列，不提供 post-edit repair contract。
- **GenDoP** (ICCV 2025)：camera-only trajectory generation。可以生成 camera 候选，但无法回答"改了人体之后 camera 哪些部分需要修"。

## 3. 任务定义

### 3.1 影视化段落图 (Cinematic Section Graph)

CSG 是一个有向无环图 $G = (V, E)$，节点为段落，边为连续性约束。

**节点。** 每个节点 $s_i \in V$ 是 HumanSection $H_i$ 或 CameraSection $C_i$：

- $H_i = (F_i, \mathbf{P}_i, \mathbf{R}_i, \mathbf{\Gamma}_i, L_i^H, B_i^{H,\text{pre}}, B_i^{H,\text{post}})$
  - $F_i = [t_i^{\text{start}}, t_i^{\text{end}}]$：帧范围
  - $\mathbf{P}_i$：关节旋转 / SMPL 参数
  - $\mathbf{R}_i$：世界坐标系下的 root translation 和 heading
  - $\mathbf{\Gamma}_i$：足部接触状态（二值或连续置信度）
  - $L_i^H \subseteq F_i$：**锁定的内部帧**（不可修改）
  - $B_i^{H,\text{pre}}, B_i^{H,\text{post}} \subseteq F_i$：段落首尾的**可编辑边界缓冲区**

- $C_i = (F_i, \mathbf{E}_i, \mathbf{K}_i, \mathbf{T}_i, L_i^C, B_i^{C,\text{pre}}, B_i^{C,\text{post}})$
  - $\mathbf{E}_i = \{(\mathbf{R}_t, \mathbf{t}_t) \in SE(3)\}_{t \in F_i}$：相机外参
  - $\mathbf{K}_i = \{\text{fov}_t\}_{t \in F_i}$：内参 / FOV
  - $\mathbf{T}_i$：构图目标（需保持在画面中的主体关节或 bounding box）
  - $L_i^C, B_i^{C,\text{pre}}, B_i^{C,\text{post}}$：与 human section 相同语义

**边。** 相邻段落 $s_i, s_j$ 之间的边 $e_{ij} \in E$ 携带三类连续性约束：

- **世界空间连续性**（human-human 边）：
  $$\text{world\_loss}(e_{ij}) = \lambda_r \|\Delta \mathbf{r}\| + \lambda_h \|\Delta \mathbf{h}\| + \lambda_v \|\Delta \mathbf{v}\| + \lambda_c \|\Delta \mathbf{\gamma}\|$$
  $\Delta \mathbf{r}, \Delta \mathbf{h}, \Delta \mathbf{v}$ 分别度量边界处 root position、heading、velocity 的跳变，$\Delta \mathbf{\gamma}$ 度量接触状态的不匹配。

- **相机空间连续性**（camera-camera 边）：
  $$\text{cam\_loss}(e_{ij}) = \lambda_T \|\Delta \mathbf{t}\| + \lambda_R \|\Delta \mathbf{R}\| + \lambda_f \|\Delta \text{fov}\| + \lambda_\omega \|\Delta \omega\|$$
  $\omega$ 为角速度，$\Delta$ 项分别度量位移、旋转、FOV、角速度的跳变。

- **屏幕空间连续性**（相机 $C_k$ 拍摄人体 $H_i$ 的任意边）：
  $$\text{screen\_loss}(e_{ij}, C_k) = \lambda_b \|\Delta \mathbf{b}\| + \lambda_s \|\Delta s\| + \lambda_h \|\Delta h\| + \lambda_v (1 - \text{vis})$$
  $\mathbf{b}$ 为投影后的 bbox 中心，$s$ 为 bbox 缩放，$h$ 为 headroom，$\text{vis}$ 为可见关节比例。

**这些 loss 之间可能冲突。** 满足 world-space contact continuity 可能迫使 root 调整，从而破坏 screen framing。Solver 必须在无法同时满足时报出不可行性，而非静默降低某一约束。

### 3.2 编辑类型（v0 范围）

v0 只支持低层、可自动生成和可量化的编辑命令：

| 编辑类型 | 参数 | 示例 |
|---|---|---|
| 人体 root 编辑 | root offset $\delta\mathbf{r}$、end root、heading change $\delta\mathbf{h}$ | 角色在段落中心左移 0.5m |
| 人体 retiming | duration scale factor $\alpha$、play rate | 将 2s 段落拉伸至 3s |
| 人体脚步调整 | 目标接触位置 $\mathbf{c}_{\text{target}}$ | 步点偏移 0.2m |
| 相机 reframe | 主体中心 $\mathbf{b}_{\text{target}}$、scale $s_{\text{target}}$、headroom $h_{\text{target}}$ | 保持主体在画面左侧 1/3、中景 |
| 相机路径 | push-in/pull-out 距离、truck/pan/tilt 偏移、orbit 角度 | 段落内 push-in 1m |

**v0 不做：** 模糊的导演语义（"更有电影感"）、手绘 storyboard/sketch、道具/手部接触、多角色交互、script-to-shot 规划。

### 3.3 脏传播 (Dirty Propagation)

给定编辑作用于段落 $s_k$，dirty compiler 执行：

1. **直接失效检测：** 对所有与 $s_k$ 相邻的边 $e$，计算 world_loss 和 screen_loss。若任一超过阈值 $\tau$，标记该边为 dirty。
2. **缓冲区激活：** 对每条 dirty edge $e_{ij}$，激活 $s_i$ 的 post-buffer $B_i^{\text{post}}$ 和 $s_j$ 的 pre-buffer $B_j^{\text{pre}}$。buffer 宽度由 loss 幅度、编辑强度和 contact/framing 置信度共同决定，不设固定常数。
3. **传递传播：** 若 $s_j$ 的 pre-buffer 延伸进入其 locked interior $L_j$（即 buffer 与锁定区域有交集），系统面临选择：(a) 缩小 buffer 并报告可能无法完全修复，或 (b) 提示用户解锁 $L_j$ 中的帧。**不自动解锁已批准内容。**
4. **输出：** dirty section set、active buffers、每条 dirty edge 的 loss breakdown。

### 3.4 修复目标

v0 使用确定性优化（QP / spline-based solver），不训练学习模型。优化变量仅限于所有 dirty boundary buffers 的并集：

$$\min_{\delta\mathbf{H}, \delta\mathbf{C}} \quad \mathcal{L} = w_{\text{contact}} \mathcal{L}_{\text{contact}} + w_{\text{world}} \mathcal{L}_{\text{world}} + w_{\text{screen}} \mathcal{L}_{\text{screen}} + w_{\text{cam}} \mathcal{L}_{\text{cam}} + w_{\text{hum}} \mathcal{L}_{\text{hum}} + w_{\text{edit}} \mathcal{L}_{\text{edit}}$$

约束条件：
$$\delta\mathbf{H}_t = \mathbf{0} \quad \forall t \in \bigcup_i L_i^H \qquad \delta\mathbf{C}_t = \mathbf{0} \quad \forall t \in \bigcup_i L_i^C$$

其中：
- $\mathcal{L}_{\text{contact}}$：human-human 边界的足部接触一致性
- $\mathcal{L}_{\text{world}}$：human-human 边界的 root position、heading、velocity 连续性
- $\mathcal{L}_{\text{screen}}$：所有跨模态边界的投影 bbox center、scale、headroom、visibility
- $\mathcal{L}_{\text{cam}}$：相机 SE(3) velocity、acceleration、jerk 平滑性
- $\mathcal{L}_{\text{hum}}$：修复后 buffer 内人体 pose velocity 平滑性
- $\mathcal{L}_{\text{edit}}$：与用户编辑目标的距离

**约束冲突是预期行为。** Contact continuity、screen framing 和 user edit intent 可能联合不可行。Solver 必须输出 failure report，指明哪些约束无法同时满足，而非静默降低某一 loss。

## 4. 数据：CSG-Bench-v0

### 4.1 字段可得性

| 字段 | 来源 | v0 判定 | 风险 |
|---|---|---|---|
| 人体帧 / SMPL / joints | AMASS、HumanML3D、MotionFix | 可靠 | 需统一 skeleton、fps、坐标系 |
| 人体帧范围 | BABEL segments、HumanML3D clips、系统切段 | 可靠（需质控） | section boundary ≠ 电影 shot |
| 人体语义标签 | BABEL、HumanML3D、MotionFix edit text | 筛选用，非硬约束 | — |
| Root path / heading | 从 motion frames 推导 | 可靠 | 坐标规范必须固定 |
| 足部接触 | foot height + velocity heuristic，少量人工校正 | 半自动 | 不能当真值；需要 noise ablation |
| 相机轨迹 | ET、DataDoP、PulpMotion、TSA、AIST++、3DPW、BEDLAM、MOvI | 可作先验/sanity check | 数据表示和开放性不统一 |
| 相机段落边界 | 系统切段或 DCC export | protocol 字段 | 数据集通常不给 DCC-style section |
| 相机意图 | subject center、shot scale、visibility、look-at、safe margin | v0 可合成 | 不等于导演语义标签 |
| Locked interiors / dirty flags / cache / undo | 系统生成 | protocol 字段 | 不能伪装成数据集字段 |

### 4.2 CSG-Bench-v0 构造

**核心原则：这是一个受控代理 benchmark，不是"真实电影数据集"。**

**构造步骤：**

1. **人体源：** 从 AMASS / BABEL / HumanML3D / MotionFix 选取步行、跑动、转身、停步、坐下/站起等基础动作。
2. **相机源：** 合成 follow、static、push-in、pull-out、truck、pan、tilt、orbit camera track。用 ET / DataDoP / PulpMotion / TSA 的轨迹统计做 sanity check——验证合成轨迹的 velocity、acceleration、jerk 分布在真实数据合理范围内。
3. **编辑协议：** 脚本自动生成 human edit、camera edit、mixed edit。每个 edit 记录 command log、locked mask、boundary buffer、dirty edges。
4. **投影层：** 用相机内外参投影 joints，生成 screen-space bbox、headroom、visibility、projected velocity。
5. **人工成本：** 只允许少量 contact active correction 或小规模 review，报告帧比例、时间、成本。

**真实配对相机 sanity check（必须）：**
- 20–50 条 ET / PulpMotion / TSA / BEDLAM / AIST++ 可用样本。
- 不训练，只做外推验证：插入局部 edit 后，CSG solver 是否比 baseline 更稳。
- 若真实样本上表现失效，不能继续 claim production relevance。

## 5. V0 实验方案

### 5.1 目标

证明 **camera-aware coupled boundary repair** 在单人、无道具、简单静态场景中，显著优于 human-only repair + camera reframe、spline blend 和 DCC-style crossfade。

**成功标准（必须同时满足）：**
1. Protected human/camera interiors 近零漂移（locked frames 上 MPJPE < 1mm）
2. Contact continuity 和 screen framing continuity 同时改善（分别优于 spline/DCC baseline）
3. Dirty radius 和 review scope 显著小于 full regenerate（dirty frame ratio < 全序列的 30%）
4. 多步 edit 后 cache reuse 和 undo fidelity 可审计
5. 真实配对 camera sanity check 不出现系统性失败

### 5.2 数据规模

| 组件 | 最低 | 目标 |
|---|---|---|
| 人体运动样本 | 50 | 100 |
| 每样本时长 | 5–10s | — |
| 每样本相机变体 | 4 | 8 |
| 编辑用例（总计） | 400 | 600+ |
| — 人体编辑 | ~100 | — |
| — 相机编辑 | ~100 | — |
| — 混合编辑 | ~100 | — |
| — 无编辑 sanity | ~100 | — |
| 真实配对验证样本 | 20 | 50 |

### 5.3 Baselines

| Baseline | 描述 | 测试什么 |
|---|---|---|
| Direct cut | 不做修复，直接拼接 | 所有连续性指标的下界 |
| Linear / Hermite / spline blend | 人机和相机独立插值 | 简单时序平滑是否足够 |
| DCC-style crossfade | 模拟 NLA / Sequencer overlap blend | 现有 DCC 工具是否已解决 |
| Human-only ASG + camera reframe | ASG 人体修复后，独立调整 camera look-at | 解耦修复是否足够 |
| CondMDI / MotionFix boundary repair | 用学习模型修人体边界，相机独立平滑 | 学习式 in-betweening 在无相机感知时是否够用 |
| Camera-only replan (GenDoP 风格) | 固定人体，重生成或平滑相机 | 仅相机侧修复是否足够 |
| Full regenerate | 联合模型重生成整个序列 | 质量上界；测试 interior 保护是否必要 |
| CSG ablations | 移除 screen loss、contact loss、dirty propagation、固定 buffer 宽度 | 将增益归因到各 CSG 组件 |

### 5.4 Metrics

| 指标 | 度量内容 | 通过阈值（草案） |
|---|---|---|
| Edit target error | 人体/相机编辑是否达成 | 不显著劣于 baseline |
| Protected interior drift | locked frames 上的 MPJPE / rotation / camera pose | $\approx 0$，必须显著低于 full regenerate |
| Contact continuity | 边界处 foot height、velocity、接触点漂移 | Mean < 2cm，或报告失败率 |
| Camera smoothness | SE(3) velocity / acceleration / jerk、FOV jerk | 低于 spline / DCC blend |
| Screen continuity | 边界处 bbox center jump、scale jump、headroom jump | Mean < 5% viewport |
| Visibility | 可见关节比、bbox 在画面内比例 | 失败率 < 10% |
| Dirty radius | dirty sections / dirty frames | 显著小于 full regenerate |
| Cache reuse | 未受影响 section 的 cache hit ratio | 多步 edit 后优势持续 |
| Undo fidelity | undo 后 motion / camera / metadata 恢复误差 | $\approx 0$ |
| Review scope | 需重审的 section 数 / 时间长度 | 小于 full regenerate 和 camera-only replan |

### 5.5 必须实验

1. **字段可得性审计：** 50–100 样本，统计每个字段来自 data / projection / synthetic protocol / manual 的比例、失败率、成本
2. **人体编辑 → 相机修复：** root / heading / retiming edit 后，比较 no repair、spline、human-only ASG + reframe、CSG full objective
3. **相机编辑 → 人体保护：** push-in / orbit / reframe edit 后，证明 protected human interior 近零漂移且 screen continuity 改善
4. **Contact noise ablation：** no contact、heuristic contact、oracle contact，观察 solver 对错误 contact 的敏感性
5. **多步脏传播：** 10 步 edit sequence，测 dirty radius、cache reuse、review scope、undo fidelity
6. **真实配对相机 sanity check：** 20–50 条真实或半真实样本，不训练也要测外推

### 5.6 通过 / 停止标准

**通过标准：**
- CSG 在 contact continuity、screen continuity、protected drift、dirty radius 上同时优于主要基线
- 真实 paired camera sanity check 不出现系统性失败（定义为 >30% cases 中 CSG 劣于 DCC crossfade）
- 多步 edit 的 cache reuse 和 review scope 有显著优势
- 小规模 animator / reviewer 盲评（3–5 人）确认 boundary artifact 和意图保留不差于 DCC baseline

**停止或转向标准：**
- Spline / DCC crossfade 已经接近上限，CSG 优势不显著（primary metrics 上 effect size < 10%）
- Solver 在超过 30% cases 中不收敛或 failure report 过多
- Contact heuristic 错误导致修复质量不可控，人工校正成本不可接受
- Full regenerate 在用户研究中被偏好，且用户不在意 interior drift

## 6. 风险

| 风险 | 严重度 | 缓解 | 升级触发条件 |
|---|---|---|---|
| Novelty 被 joint generation 工作挤压 | 高 | 正面区分 CSG 是 local edit repair 而非 full generation | Reviewer 仍认为与 Pulp/TSA 重叠 |
| 合成相机 benchmark 被认为太 toy | 高 | 真实配对相机 sanity check + animator review | 真实样本 sanity check 失败 |
| Contact heuristic 不可靠 | 高 | Confidence weighting、noise ablation、报告人工校正成本 | >30% cases 需人工校正 contact |
| CSG solver 输给 spline / DCC blend | 高 | Strong baselines + 明确停止规则 | Primary metrics 上无显著优势 |
| Dirty propagation 被视为工程细节 | 中 | 多步 edit 实验证明 review scope / cache reuse 优势 | Reviewer 认为是实现细节 |
| 真实制作需求不明 | 中 | Animator review + 局部编辑案例研究 | Animator 反馈无痛点 |

## 7. 立即下一步

1. **写 CSG schema：** 将 HumanSection、CameraSection、FramingEdge、ProtocolMetadata 形式化为带验证的数据结构
2. **字段可得性审计：** 先统计字段可得性，不先写 solver
3. **生成 CSG-Bench-v0：** 50–100 人体样本，每样本 4–8 相机变体，400 编辑用例
4. **先实现 baselines：** direct cut、linear、spline、DCC crossfade、human-only ASG + reframe
5. **检查上界：** 如果 spline / DCC crossfade 已接近饱和，停止或改方向
6. **实现确定性 CSG solver：** QP / spline with projection loss
7. **真实配对相机 sanity check：** 20–50 真实样本，大规模投入前先评估
8. **设计 animator review：** 3–5 名 animator，只问局部编辑、重审范围、意图保留，不问抽象电影感

## Source Notes

- [[ideas/StoryMotion/archived/v3/2026-06-03_storymotion_canonical_plan|StoryMotion ASG Canonical Plan]]
- [[ideas/camera/2026-06-05_camera-movement-generation-system-survey-llm-audit-merged|Camera Movement 系统调研]]

## Source Papers

- [[analysis/ICLR_2026/Pulp_Motion_Framing-aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]
- [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]
- [[analysis/ECCV_2024/E.T._the_Exceptional_Trajectories_Text-to-camera-trajectory_generation_with_character_awareness|E.T. / DIRECTOR]]
- [[analysis/ICCV_2025/GenDoP_Auto-regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography|GenDoP / DataDoP]]
- [[analysis/ICLR_2026/AdaViewPlanner_Adapting_Video_Diffusion_Models_for_Viewpoint_Planning_in_4D_Scenes|AdaViewPlanner]]
- [[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image-to-Video_Generation|MotionCanvas]]
- [[analysis/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text-to-Video_Generation|CameraCtrl]]
- [[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]
- [[analysis/SIGGRAPH_2024/Flexible_Motion_In-betweening_with_Diffusion_Models_CondMDI|CondMDI]]
- [[analysis/SIGGRAPH_Asia_2024/MotionFix_Text-Driven_3D_Human_Motion_Editing|MotionFix]]
