---
title: "Research Transition Tracks: 从 Motion 到 Human-Camera-Video 与 3D 生成"
status: strategy/converged
created: 2026-07-08T21:20:00+0800
updated: 2026-07-08T21:20:00+0800
tags:
  - research_strategy
  - motion_generation
  - human_camera_video
  - character_animation
  - 3d_generation
  - siggraph
  - industrial_research
  - graduation_plan
aliases:
  - motion-to-3d-video-transition
hypothesis: |
  未来两年最稳的路线不是彻底丢掉 motion，也不是继续卷 text-to-motion，而是把已有 ReactDance、StoryMotion、人-相机建模经验迁移到更真实的工业控制问题：human-camera-video controllable generation、production character-camera authoring，以及 3D 生成数据质量/修复。主线应优先押注 StoryMotion 延伸的人-相机-视频控制；角色动画/RL 可作为控制接口和物理一致性模块，不宜单独作为毕业主赛道；混元 3D 实习应转化为 3D/video 数据、评估、修复和动态资产经验，而不应依赖团队 technical report 作为个人论文产出。
source_papers:
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]"
  - "[[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation|MotionCanvas]]"
  - "[[analysis/SIGGRAPH_2024/MotionCtrl_A_Unified_and_Flexible_Motion_Controller_for_Video_Generation|MotionCtrl]]"
  - "[[analysis/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion|Direct-a-Video]]"
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]"
  - "[[analysis/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives|MotionBricks]]"
  - "[[analysis/TOG_2025/Control_Operators_for_Interactive_Character_Animation|Control Operators]]"
  - "[[analysis/SIGGRAPH_ASIA_2024/MaskedMimic_Unified_Physics_Based_Character_Control_Through_Masked_Motion_Inpainting|MaskedMimic]]"
  - "[[analysis/SIGGRAPH_2025/PARC_Physics_based_Augmentation_with_Reinforcement_Learning_for_Character_Controllers|PARC]]"
  - "[[analysis/SIGGRAPH_2025/Diffuse-CLoC_Guided_Diffusion_for_Physics-based_Character_Look-ahead_Control|Diffuse-CLoC]]"
  - "[[analysis/SIGGRAPH_ASIA_2022/PADL_Language_Directed_Physics_Based_Character_Control|PADL]]"
  - "[[analysis/SIGGRAPH_2026/ArtiFixer_Enhancing_and_Extending_3D_Reconstruction_with_Auto_Regressive_Diffusion_Models|ArtiFixer]]"
  - "[[analysis/SIGGRAPH_2026/Prox_E_Fine_Grained_3D_Shape_Editing_via_Primitive_Based_Abstractions|Prox-E]]"
  - "[[analysis/ICLR_2026/ShapeGen4D_Towards_High_Quality_4D_Shape_Generation_from_Videos|ShapeGen4D]]"
  - "[[analysis/ICLR_2026/Text_to_3D_by_Stitching_a_Multi_view_Reconstruction_Network_to_a_Video_Generator|VIST3A]]"
related_notes:
  - "[[ideas/StoryMotion]]"
  - "[[ideas/poool/2026-06-30_human-camera-video_work_taxonomy|human-camera-video taxonomy]]"
  - "[[ideas/poool/2026-06-20_body-locked-camera-grammar|body-locked camera grammar]]"
  - "[[ideas/poool/2026-06-22_storyboard-key-shot-camera-data-gap|storyboard key-shot camera data gap]]"
---

# Research Transition Tracks: 从 Motion 到 Human-Camera-Video 与 3D 生成

> [!summary] 当前判断
> 你不应该把 motion 完全丢掉，也不应该继续押注泛化的 text-to-motion。更合理的路径是把 motion 变成 **3D/video 生成里的结构化控制变量**：人怎么动、相机怎么看、屏幕里如何构图、生成结果如何可编辑和可修复。这样既保留 ReactDance 和 StoryMotion 的论文连续性，又能借混元 3D 实习切到 3D/video 工业问题。

## 1. Idea decomposition and association

### 1.1 约束与目标

当前约束不是“哪个方向理论上最前沿”，而是四个条件同时成立：

- **毕业约束**：两年内还需要至少一篇 CCF A 级别主论文，以及两篇在投论文储备。已经有 ReactDance，但如果完全丢掉 motion，相当于主动放弃一条已验证的论文资产。
- **资源约束**：混元 3D 实习能给到 3D 生成、数据处理、工程 pipeline 和工业评估视角，但团队产出主要是 technical report，不能默认转化为个人一作论文。
- **已有进度**：StoryMotion 是当前最快能推进的工作，问题已经自然落在 human-camera joint modeling。
- **赛道约束**：text-to-motion 太窄且越来越卷；通用 video generation 和 text-to-3D 又过度依赖大模型资源，不适合作为两年毕业主赌注。

因此，推荐的方向不是三选一，而是一个主线加两个受控支线：

| 优先级 | 路线 | 论文定位 | 工业相关性 | 竞争强度 | 与个人资产匹配 |
|---|---|---|---|---|---|
| P0 | Source-reliable human-camera-video control | StoryMotion 后续主线 | 高 | 中 | 极高 |
| P1 | Production character-camera authoring | 第二篇或并行投稿 | 高 | 中 | 高 |
| P2 | Animation-ready 3D asset repair / dynamic asset data | 实习转向与长期职业线 | 极高 | 中高 | 中高 |
| 不建议主线 | Pure RL / physics-based character control | 高风险独立赛道 | 中高 | 高 | 中 |

### 1.2 最终建议

**主线：继续 StoryMotion，但把论文叙事从 motion generation 改成 human-camera-video control 的前置基础。**

StoryMotion 不要写成“又一个 human-camera joint diffusion”。它更应该变成后续路线的基座：

- **从动作生成转向视频控制**：human motion 和 camera trajectory 是 video generation 的结构化控制信号。
- **从离线生成转向生产控制**：用户最终关心的是屏幕构图、镜头语义、人物是否在框、动作是否可读。
- **从单一数据域转向 source reliability**：真实 mocap、视频估计 motion、生成 motion、重建 3D 资产的噪声结构不同，模型应显式处理来源可靠性。

这条主线的下一步论文可以暂定为：

> **Source-Reliable Human-Camera Control for Character-Centric Video Generation**

核心不是做一个更大的模型，而是证明：当 human motion 来源不可靠、camera 约束稀疏或需要编辑时，一个人-相机统一控制层能比通用 video camera control 更稳定地保持人物构图、动作可读性和镜头意图。

## 2. Real scenarios and pain points

### 2.1 真实场景一：角色中心视频生成与镜头控制

SIGGRAPH/CVPR/ICLR 的趋势已经很明确：video generation 正在从文本提示转向结构化控制。问题是，通用 camera control 只解决“相机怎么动”，不一定解决“人怎么被拍”。

相关证据：

- [[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]
  - `core_operator`：构造 camera-aligned depth 和 pose 条件，并用两阶段 denoising schedule；早期 depth+pose 锁定全局结构，后期 pose-only 保留细节。
  - `primary_logic`：从参考图中移除静态 actor，将 actor depth 对齐到 scene，在冻结视频模型上实现 zero-shot camera 与 3D motion 联合控制。
  - 启示：视频模型真正需要的是 **camera + human 3D motion 的联合控制**，不是单独的 camera trajectory。
- [[analysis/SIGGRAPH_2025/MotionCanvas_Cinematic_Shot_Design_with_Controllable_Image_to_Video_Generation|MotionCanvas]]
  - `core_operator`：Motion Signal Translation 把用户的 3D scene-space 意图转成 2D screen-space 条件信号。
  - `primary_logic`：训练只依赖自动抽取的 2D track/bbox 信号，推理时用深度和针孔相机模型桥接 3D intention 与 2D condition。
  - 启示：工业用户想在 3D/scene space 表达意图，但模型更容易消费 screen-space 控制。StoryMotion 可以把 human-camera latent 映射到 screen-space framing/editing。
- [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]
  - `core_operator`：用 screen-framing guidance 权重进行辅助采样，将 human+camera latent 映射到 framing latent。
  - `primary_logic`：human-camera consistency 可以被建模为 screen-space framing consistency。
  - 启示：StoryMotion 的差异点不应只是 joint generation，而应是 **framing-aware control under unreliable sources**。

真实痛点：

- 视频生成用户很难只靠文本稳定表达 “低角度跟拍奔跑人物，人物始终保持三分线偏左，动作在转身时可读”。
- 通用 camera control 常把相机当全局运动，不保证人物在框、动作可读或镜头语义一致。
- 生成/估计得到的人体 motion 有噪声，直接作为视频条件会导致人物漂移、深度错位或画面重构不稳定。

### 2.2 真实场景二：动画/游戏/短剧生产里的角色-相机 authoring

纯 text-to-motion 的用户价值有限，因为生产中真正需要的是可控、可编辑、可迭代的动作与镜头。

相关证据：

- [[analysis/SIGGRAPH_2026/MotionBricks_Scalable_Real_Time_Motions_with_Modular_Latent_Generative_Model_and_Smart_Primitives|MotionBricks]]
  - `core_operator`：结构化多头 latent tokenizer、root-pose 解耦、多 codebook 量化。
  - `primary_logic`：把动作拆成 root trajectory 和 pose latent generation，用模块化 coarse-to-fine flow 实现实时生成。
  - 启示：SIGGRAPH-style animation 价值不在“文本生成一段动作”，而在 **实时、模块化、可编辑、可嵌入 production**。
- [[analysis/TOG_2025/Control_Operators_for_Interactive_Character_Animation|Control Operators]]
  - `core_operator`：把用户控制拆成 Null/Bool/Encode/And/Or/Set/Array 等语义 operator，并自动映射到可训练模块。
  - `primary_logic`：用户定义控制 schema，系统生成对应网络结构，降低非技术用户 authoring 门槛。
  - 启示：你可以把 human-camera 控制做成 authoring interface，而不是只做 benchmark 上的生成模型。

真实痛点：

- 动作、相机、构图通常分属不同工具链；AI 生成结果难以进入可编辑流程。
- 动画师更需要 “锁定人物朝向、保持镜头语法、局部重写动作” 这类控制，而不是一次性完整生成。
- 游戏/短剧/AI 漫剧等场景需要轻量、可交互、能快速预览的角色-相机控制，不一定需要最大模型。

### 2.3 真实场景三：3D 生成中的数据质量、修复与 animation-ready asset

混元 3D 实习的最大价值不一定是直接发 text-to-3D 论文，而是让你接触工业 3D 生成 pipeline 中的真实问题：数据清洗、重建缺陷、资产修复、动态一致性、评估指标。

相关证据：

- [[analysis/SIGGRAPH_2026/ArtiFixer_Enhancing_and_Extending_3D_Reconstruction_with_Auto_Regressive_Diffusion_Models|ArtiFixer]]
  - `core_operator`：opacity-aware noise mixing；高 opacity 区域使用 degraded render 作为 denoise source，低 opacity 区域注入 Gaussian noise，并做 bidirectional-to-causal autoregressive distillation。
  - `primary_logic`：把 degraded 3D reconstruction 当作 source distribution，约束生成、避免 mode collapse，同时修复 artifact 和补全缺失内容。
  - 启示：3D 生成的真实问题常常不是“从零生成”，而是 **对已有重建/生成结果做可信修复和扩展**。
- [[analysis/SIGGRAPH_2026/Prox_E_Fine_Grained_3D_Shape_Editing_via_Primitive_Based_Abstractions|Prox-E]]
  - `core_operator`：用 superquadric primitive abstraction 生成 VLM 可编辑 JSON，再通过 proxy-induced denoising 控制 3D diffusion。
  - `primary_logic`：显式、可解释的 primitive representation 桥接 VLM 与 3D generator。
  - 启示：工业 3D 编辑需要中间表示，不只是端到端生成。
- [[analysis/ICLR_2026/ShapeGen4D_Towards_High_Quality_4D_Shape_Generation_from_Videos|ShapeGen4D]]
  - `core_operator`：在 pretrained 3D model 中插入 spatiotemporal attention、time-aligned latent queries 和 shared noise，把 3D prior 扩展为 4D shape generation。
  - `primary_logic`：动态 mesh sequence 可以被看作 frame-dependent 3D generation，并继承 Hunyuan3D/Step1X 这类 3D prior。
  - 启示：3D 与 video 的交界正在变成真实赛道，但重模型训练门槛高。

真实痛点：

- 工业 3D 生成会遇到大量 dirty data：重建缺口、漂浮部件、纹理/几何不一致、生成资产不可 rig、不可动画化。
- 通用 text-to-3D 太卷，且基础模型资源高度集中；更适合切入的是评估、数据质量、修复、动态/角色资产约束。
- 如果能把 3D asset 与角色动画连接起来，例如 animation-ready character asset repair，就能同时利用 motion 背景和实习资源。

## 3. Related-work support and research opportunities

### 3.1 P0 主线：Source-Reliable Human-Camera-Video Control

**一句话定位**：把 StoryMotion 扩展为面向视频生成的 human-camera control layer，重点解决不同 motion source 可靠性、screen-space framing、camera/edit condition 的一致性。

为什么赛道真实：

- ActCam 证明 frozen video model 可以通过 depth/pose 条件做 camera + 3D motion 联合控制。
- MotionCanvas 证明 3D scene-space intention 到 2D screen-space signal 的转换是可发表、可落地的问题。
- Pulp Motion 和 Towards Storytelling Animations 证明 human-camera joint modeling 本身已经是明确研究方向。

为什么不过度卷：

- 不直接和 Sora/Runway/Pika/大厂通用 T2V 比生成质量。
- 不做泛化 camera trajectory control，而做 **character-centric framing and motion readability**。
- 不做单纯 joint diffusion，而做 **source-aware, reliability-aware, edit-aware** 的控制层。

与个人经历和资源的关系：

- ReactDance 提供多人动作、节奏、互动经验。
- StoryMotion 已经有人-相机统一建模进度，是最短路径。
- 混元 3D 实习能补充 3D/video 数据处理、渲染、重建、评估经验。
- 该方向可在公开数据和开源视频模型上做 proxy，不完全依赖内部模型。

可写的研究问题：

1. **Source reliability modeling**：motion 来源可能是真实 mocap、视频估计、生成 motion、3D reconstruction tracking；不同来源的噪声结构应影响 camera 生成和 screen-space control。
2. **Framing-aware correction**：给定初始 human motion 和粗 camera path，模型自动修正 camera，使人物在框、动作关键部位可读、shot scale 稳定。
3. **Video-condition bridge**：把 human-camera trajectory 转成 depth、pose、bbox、track、mask 等视频模型可消费条件，并比较不同 condition 的稳定性。
4. **Editability**：支持局部重写镜头，如 keep action fixed but change shot scale / angle / tracking style。

最小可发表版本：

- 输入：human motion 或 noisy/generated human motion，加上稀疏 camera/text/framing intent。
- 输出：camera trajectory 或 video-control condition。
- 评估：screen-space in-frame ratio、bbox scale stability、joint visibility、action readability、人评镜头语义一致性、视频生成后控制保持度。
- Baseline：Pulp Motion 风格 joint generation、MotionCanvas 风格 signal translation、简单 camera heuristic、已有 StoryMotion variant。

止损标准：

- 如果 StoryMotion 对 camera/framing 的优势无法在 screen-space 指标上稳定复现，则不扩展到视频。
- 如果 video generation 质量完全掩盖 control 差异，则先退回 skeleton/mannequin/rendered character 控制，不急着做最终视频。
- 如果公开模型无法稳定接受 condition，则论文主体保持在 human-camera control，视频只作为 demo 和下游验证。

### 3.2 P1 支线：Production Character-Camera Authoring

**一句话定位**：把动作和镜头从“生成结果”变成“可编辑控制对象”，做面向动画/游戏/短剧生产的 authoring interface。

为什么赛道真实：

- MotionBricks 的实时模块化生成说明 production animation 关心 latency、局部控制、组合能力。
- Control Operators 说明 SIGGRAPH/TOG 接受“控制接口 + 可训练模块”的问题设定。
- MotionCanvas 说明 cinematic shot design 已经从模型条件控制走向用户意图表达。

为什么不过度卷：

- 避免和大规模 text-to-motion benchmark 竞争。
- 避免和纯游戏 animation controller 老牌系统正面硬拼。
- 选择“character motion + camera + screen composition”的交叉点，竞争者少于单独角色动画或单独 camera control。

适合你的版本：

- 做一个 **Shot grammar / operator-driven character-camera authoring** 系统。
- 输入不是自然语言生成全部内容，而是结构化 intent：shot scale、angle、tracking style、character facing、root path、key pose、keep-in-frame constraint。
- 输出是可编辑的 motion/camera pair，而不是一次性视频。

可能的论文贡献：

1. 一个统一控制 schema：把 character root、pose、camera、screen framing 拆成 operator。
2. 一个训练或优化框架：将 operator 转成 latent constraints 或 sampling guidance。
3. 一个 authoring benchmark：测试局部编辑、组合泛化、实时预览、人评可用性。

风险：

- Demo 和系统完整度要求高。
- 如果只做 UI，没有清晰模型贡献，会被认为是工程系统。
- 如果评价只靠人评，论文风险较高；必须有稳定的可量化 control metrics。

适合作为：

- StoryMotion 后的第二篇；
- SIGGRAPH Asia / TOG / CVPR 的 production-oriented 投稿；
- 找工作展示：比纯 benchmark paper 更能体现工业实用性。

### 3.3 P2 支线：Animation-Ready 3D Asset Repair / Dynamic Asset Data

**一句话定位**：从混元 3D 数据处理经验切入 3D 生成，不做通用 text-to-3D，而做“可动画化/可视频化的 3D 资产质量控制、修复与评估”。

为什么赛道真实：

- ArtiFixer 说明 reconstruction repair 和 artifact removal 是 SIGGRAPH 级问题。
- Prox-E 说明显式中间表示对 3D editing 有价值。
- ShapeGen4D 和 VIST3A 说明 3D prior 正在向 video/4D 扩展。

为什么不宜直接当毕业主线：

- 大模型、内部数据和算力依赖更强。
- 如果论文必须脱离内部资源复现，选题需要重新设计 public proxy。
- 通用 3D editing / 3D generation 已经很卷，必须绑定角色、动态、动画可用性，才能和你的 motion 背景形成差异。

较好的切入方式：

1. **3D asset quality scoring for animation readiness**：评价生成角色资产是否能 rig、是否几何连通、关节区域是否可变形、纹理是否随动作稳定。
2. **Repair for riggable / dynamic characters**：面向角色动画的局部几何修复、缺失部位补全、拓扑或 proxy 一致性。
3. **Video-to-4D / generated-asset temporal consistency audit**：借鉴 ShapeGen4D，但先从评估和数据修复切入，不直接训练 foundation model。

实习策略：

- 在混元内部优先争取参与 **数据质量、自动评估、资产修复、video-to-3D/4D、动态资产** 相关任务。
- 如果只能做不可公开的数据清洗或团队 report，仍然把它当作经验积累，但不要把毕业希望押在内部论文。
- 同步构建一个 public proxy：用公开重建/生成资产做小规模 benchmark，确保外部可投稿。

### 3.4 不建议作为主线：Pure RL / Physics-Based Character Control

RL/physics-based character control 是真赛道，但不适合你现在把它作为两年毕业主线。

相关证据：

- [[analysis/SIGGRAPH_ASIA_2024/MaskedMimic_Unified_Physics_Based_Character_Control_Through_Masked_Motion_Inpainting|MaskedMimic]]
  - `core_operator`：把随机 masked motion sequence 训练成 partial-constraint controller。
  - `primary_logic`：将 physics-based control 重定义为 motion inpainting，用一个模型支持多种约束。
- [[analysis/SIGGRAPH_2025/PARC_Physics_based_Augmentation_with_Reinforcement_Learning_for_Character_Controllers|PARC]]
  - `core_operator`：RL tracker 模仿生成 motion，并把物理可行的修正 motion 回填数据集。
  - `primary_logic`：generator 和 tracker 共演化，让 physics simulation 成为数据质量过滤器。
- [[analysis/SIGGRAPH_2025/Diffuse-CLoC_Guided_Diffusion_for_Physics-based_Character_Look-ahead_Control|Diffuse-CLoC]]
  - `core_operator`：联合扩散 state-action distribution，使 predicted states 条件化 action generation。
  - `primary_logic`：把 kinematic guidance 迁移到 physics-based control。

为什么不建议主线：

- 社区壁垒高：仿真、reward、policy training、数据集、实时控制都要补。
- 与 StoryMotion 目前进度距离较远，短期内不能直接转化为毕业论文。
- 如果只做 camera + RL，会很容易变成系统工程，论文问题不够清楚。

推荐用法：

- 把 physics/RL 当成 **后处理和验证模块**，例如用物理控制器过滤不合理 motion，或者作为 generated motion reliability 的一类 source。
- 把 MaskedMimic/PARC 的思想迁移到 P0/P1：用 partial constraint / inpainting / simulation feedback 提升 motion-camera control 的可信度。
- 只在 P0/P1 已经稳定后，再考虑 “character-camera controller with physical feasibility”。

## 4. Frontier cross-domain techniques and validation ideas

### 4.1 核心技术组合

推荐组合不是“再训练一个大模型”，而是四层结构：

1. **Source layer**：真实 mocap、视频估计、生成 motion、重建 3D tracking、用户编辑轨迹。
2. **Reliability layer**：估计每个 source 的噪声、不确定性、缺失部位、时间稳定性。
3. **Human-camera control layer**：生成或修正 camera trajectory，同时保持人物构图、动作可读性、shot grammar。
4. **Video/3D condition layer**：转成 pose/depth/bbox/track/mask/primitive proxy 等下游模型可用条件。

这套结构能自然连接三类工作：

- StoryMotion：提供 human-camera joint modeling。
- MotionCanvas/ActCam：提供 video model condition bridge。
- ArtiFixer/Prox-E/ShapeGen4D：提供 3D source repair 和 dynamic asset extension 的启发。

### 4.2 三个候选题目

| 候选题 | 最小贡献 | 目标会议 | 需要资源 | 风险 |
|---|---|---|---|---|
| Source-Reliable Human-Camera Control | source-aware human-camera generation/correction + framing metrics | ICLR/CVPR | 中 | 需要明确优于 StoryMotion 的新问题 |
| Operator-Driven Character-Camera Authoring | 可组合 control operators + 局部编辑 benchmark | SIGGRAPH Asia/CVPR | 中高 | demo 和 user study 压力 |
| Animation-Ready 3D Asset Repair | 面向动态角色的 3D asset 质量评估/修复 | SIGGRAPH/CVPR | 高 | 依赖数据与内部资源 |

### 4.3 建议实验路线

**阶段 A：0-4 周，锁定 StoryMotion 的毕业价值**

- 明确 StoryMotion 的论文 claim：不是一般 motion generation，而是 human-camera joint modeling and framing-aware control。
- 把已有结果整理成三个层级：motion/camera 数值指标、screen-space framing 指标、可视化 case。
- 建立 source reliability 小实验：真实 motion、生成 motion、扰动 motion 分别作为输入时，camera/framing 是否退化。

**阶段 B：4-8 周，验证 P0 是否能成为下一篇**

- 做一个 zero/low-training bridge：把 StoryMotion 输出转成视频模型条件，例如 pose、depth、bbox、track。
- 比较三类控制：camera-only、human-only、human-camera。
- 若视频模型不稳定，退回 rendered character 或 mannequin scene，仍然评价 framing and readability。

**阶段 C：8-12 周，决定实习资源转化方式**

- 在混元内部争取任务迁移到 video-to-3D/4D、3D asset repair、自动评估、dynamic asset data。
- 询问是否存在可公开数据、可公开 benchmark、可个人一作投稿的子问题。
- 如果内部只能参与 technical report，则保留实习经验，但论文路线回到 P0/P1 的公开 proxy。

### 4.4 内部活水 vs 外部实习

优先级建议：

1. **先内部活水，不立刻跳**：你已经在混元体系内，先用 1-2 个月争取从数据处理靠近 3D/video 生成、评估、修复、动态资产任务。
2. **判断是否能个人论文化**：核心问题不是团队强不强，而是你是否能拿到明确 ownership、可公开实验、可复现 benchmark。
3. **若不能论文化，再跳外部**：如果内部长期只能做不可公开 pipeline 或团队 report，则应寻找更适合个人一作的学术工业实习，目标是 video/3D generation + controllability/evaluation，而不是单纯大模型训练。

判断标准：

- 能否定义一个你主导的问题，而不是只接流水线任务。
- 能否把内部经验复刻成公开 proxy。
- 能否在 3-4 个月内产出一套可投稿图表和 ablation。
- 是否与你的 P0/P1 形成叙事连续性。

## 5. Summary and next steps

### 5.1 方向排序

**第一选择：StoryMotion -> Source-Reliable Human-Camera-Video Control**

这是毕业和转向最统一的方案。它保留 motion 资产，但研究对象升级为 video/3D generation 的可控接口。它不需要你直接和通用 T2V 或 text-to-3D foundation model 硬拼，也能把混元 3D 实习经验吸收进数据、condition、evaluation、repair。

**第二选择：Production Character-Camera Authoring**

这是更 SIGGRAPH/工业化的路线，适合作为第二篇或后续工作。它能服务找工作，但要注意 demo、用户流程和可量化评估，否则容易像系统展示。

**第三选择：Animation-Ready 3D Asset Repair**

这是职业长期价值很高的路线，但短期毕业风险更高。只有当混元内部能给到可公开数据/任务/ownership 时，才应升级为主线；否则先作为实习方向和中长期储备。

**不建议：纯 text-to-motion 或纯 RL character control**

text-to-motion 太窄且已不符合你的转向目标。纯 RL/physics control 虽然真实，但迁移成本和社区壁垒过高，应作为物理可行性、数据过滤、局部控制模块，而不是毕业主赌注。

### 5.2 接下来三件事

1. **给 StoryMotion 重写定位**：从“human-camera 统一建模”改成“character-centric video/animation control 的 foundation layer”，补 screen-space framing、source reliability、editability 三类实验。
2. **在混元内部主动靠近 3D/video 数据问题**：优先找 asset repair、dynamic/4D、video-to-3D、automatic evaluation，而不是只做无论文 ownership 的数据处理。
3. **启动 P0 的最小验证**：用公开视频模型或 rendered proxy 验证 human-camera condition 是否比 camera-only / human-only 更稳定地保持人物构图和动作可读性。

> [!note] 关键原则
> 未来两年不要问“我还做不做 motion”，而要问：**motion 如何成为 3D/video 生成里最有价值、最难被通用大模型自动学会的控制接口？** 这个问题能把 ReactDance、StoryMotion、混元 3D 实习和后续找工作连接起来。
