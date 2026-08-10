---
title: "Motion Storyboard Previsualization Ideas"
created: 2026-06-01T14:05:11+08:00
updated: 2026-06-01T14:05:11+08:00
status: "brainstorm/ds-max-polished"
hypothesis: "把分镜、blocking pose、空间锚点和长程状态记忆变成 3D motion 的可编辑中间层，比直接迁移视频相机控制更贴近标准 3D 动作生成的真实缺口。"
tags:
  - Motion_Generation
  - research_idea
  - storyboard
  - previsualization
  - motion_inbetweening
  - scene_aware_motion
source_papers:
  - "[[StoryMotionnalysis/Image_Video_Generation/arXiv_2026/2026_STAGE_Storyboard_Anchored_Generation_for_Cinematic_Multi_shot_Narrative]]"
  - "[[StoryMotionnalysis/Motion_Generation/TOG_2025/2025_Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation]]"
  - "[[StoryMotionnalysis/Human_Interaction/ICLR_2025/2025_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes]]"
  - "[[StoryMotionnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning]]"
  - "[[StoryMotionnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition]]"
  - "[[StoryMotionnalysis/Human_Interaction/arXiv_2025/2025_UniHM_Universal_Human_Motion_Generation_with_Object_Interactions_in_Indoor_Scenes]]"
  - "[[StoryMotionnalysis/Motion_Generation/ICCV_2025/2025_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annotation_for_Fine_grained_Motion_Generation_and_Editing]]"
  - "[[StoryMotionnalysis/Motion_Generation/ICLR_2026/2026_ViMoGen_The_Quest_for_Generalizable_Motion_Generation_Data_Model_and_Evaluation]]"
---
# 2026-06-01 Motion Storyboard Previsualization Ideas

> [!abstract] TL;DR
> 本轮不继续 MoDebug / MoProbe，不做舞蹈，也不把视频生成里的相机控制直接搬到 canonical 3D motion。保留三条经过 ds max 打磨的方向：`MSP-2.0` 作为主线，`SOAMPrevis` 作为场景物体交互分支，`LMC-Memory` 作为长程连续性模块。`Blocking-pose-to-motion` 不单独成线，作为 MSP-2.0 的最小实验切片。

## 0. Boundary Conditions

- **非目标 1：视频相机控制直接迁移**  
  标准 text-to-motion 输出通常是 canonical / standard space 的 3D 动作序列，与相机视角没有天然绑定。Jianhong Bai 一类视频生成相机控制范式只有在目标变成“动作序列的相机控制 / 分镜生成 / previs 输出”时才相关。
- **非目标 2：舞蹈生成**  
  PAE+VQ 舞蹈重建结果只作为实操经验，不继续工作，不把舞蹈作为主任务或核心 benchmark。
- **非目标 3：MoDebug / MoProbe 延续**  
  近期没有稳定数据趋势支撑继续围绕诊断/探针路线加实验。本轮只抽取“结构化接口、可编辑中间层、长程连续性”的经验，不把 MoDebug/MoProbe 作为 idea 主体。
- **历史参考**  
  旧的分镜构思文件目前在 `obsidian-vault/.trash/2025-03-09_motion-llm-ideas.md`。它可作为思路背景，但本轮不恢复、不追加、不当作活动 source of truth。

## 1. Idea Decomposition and Association

### 1.1 Core Problem

当前 motion generation 的主流接口仍是“一句文本 -> 一段短动作”。但动画、游戏、影视 previs 需要的是：

- 用户能给出 story / shot list / blocking pose / root waypoint / object anchor；
- 系统输出可编辑的 3D motion，而不是最终视频；
- 多段之间 root trajectory、姿态、接触状态连续；
- 修改某个 shot 或物体位置时，可以局部重生成，而不是整段重来。

因此，本轮更合适的问题不是“把相机控制迁移到 motion”，而是：

> 如何把分镜级创作意图编译成 canonical 3D motion 的可编辑中间层，并在长序列 / 场景交互 / 局部修改中保持空间和状态连续？

### 1.2 Related Work Anchors

- [[StoryMotionnalysis/Image_Video_Generation/arXiv_2026/2026_STAGE_Storyboard_Anchored_Generation_for_Cinematic_Multi_shot_Narrative|STAGE]]：证明 storyboard / shot-level start-end anchors / memory pack 对多镜头叙事有效，但输出是视频，不是标准 3D motion。
- [[StoryMotionnalysis/Motion_Generation/TOG_2025/2025_Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation|Sketch2Anim]]：提供 sketch keypose + trajectory -> 3D animation 的直接参考，但更像单人动作草图串联，不是完整空间分镜预演。
- [[StoryMotionnalysis/Human_Interaction/ICLR_2025/2025_Sitcom_Crafter_A_Plot_Driven_Human_Motion_Generation_System_in_3D_Scenes|Sitcom-Crafter]]：能做 plot-driven stage-wise scene motion，但依赖 LLM 自由分解，缺少可编辑 storyboard / blocking pose 接口。
- [[StoryMotionnalysis/Human_Interaction/arXiv_2025/2025_UniHM_Universal_Human_Motion_Generation_with_Object_Interactions_in_Indoor_Scenes|UniHM]]：`continuous 6DoF waypoint + discrete local token` 是强支撑，说明全局空间摆放不应强行离散化，局部身体动作可以 token 化。
- [[StoryMotionnalysis/Motion_Generation/arXiv_2026/2026_PRISM_Streaming_Human_Motion_Generation_with_Per_Joint_Latent_Decomposition|PRISM]] 和 [[StoryMotionnalysis/Motion_Generation/CVPR_2026/2026_ActionPlan_Future_Aware_Streaming_Motion_Synthesis_via_Frame_Level_Action_Planning|ActionPlan]]：证明 long / streaming / editing 正在变成 motion 主战场，但它们没有显式处理 storyboard、scene object anchor 和跨 shot 状态记忆。

## 2. Real Scenarios and Pain Points

### 2.1 Animation / Game Previsualization

创作者不是只想要“walk then wave”这种单句动作，而是想快速搭 blocking：

- 第一个 shot：角色从门口走到桌边；
- 第二个 shot：转身拿起杯子；
- 第三个 shot：看向另一角色并后退；
- 修改需求：杯子位置移动、第二个 shot 的结束姿态改变、第三段不要重新生成前两段。

痛点是现有 T2M 很难同时满足空间锚点、跨段连续和局部编辑。

### 2.2 Scene-Aware Character Motion

场景物体改变后，motion 需要跟着改变，而不是只把 root 平移过去：

- 椅子移动后，坐下动作的 root、膝盖、骨盆和接触关系都需要调整；
- 桌面高度改变后，手臂、躯干前倾和脚步位置都需要局部适配；
- 这种变化应该由 affordance anchor 驱动，而不是纯文本重采样。

### 2.3 Long-Form Motion Composition

长动作常见失败不是单帧质量，而是段落边界：

- root position / heading 突变；
- 脚接触状态不连续导致滑步；
- 手持物状态在下一段消失；
- 上一段的身体状态没有进入下一段生成条件。

PRISM / ActionPlan 已经把“能生成长序列”推到前面，但还没有把“哪些状态必须被显式记住”做成可解释接口。

## 3. Related-Work Support and Research Opportunities

### 3.1 Support Points

- STAGE 的 start-end pair 与 memory pack 适合迁移成 motion 的 start-end pose / state memory，但需要去掉像素和相机假设。
- Sketch2Anim 证明草图式 keypose / trajectory 能作为创作接口，但更强的 3D spatial blocking 能减少 2D-to-3D ambiguity。
- UniHM 的混合表示说明：全局 6DoF 路径应保持连续，局部 pose / joint motion 可以走 token 或 latent。
- PRISM 的 per-joint latent decomposition 支持局部重生成和受影响关节编辑，是 scene-object editing 的自然底座。
- FineMotion 说明可自动构造细粒度 body-part / temporal 文本信号，可为 storyboard script compiler 或局部约束标签提供弱监督。

### 3.2 Opportunity Summary

这三个保留 idea 的关系是：

- `MSP-2.0`：主问题，定义 storyboard / blocking / waypoint -> 3D motion previs。
- `SOAMPrevis`：空间交互分支，解决物体 affordance anchor 和场景编辑。
- `LMC-Memory`：时间连续分支，解决多段生成和跨 shot 状态记忆。

三者可以组合成一条完整路线，也可以按实验风险拆开推进。最小可行优先级是：先做 `MSP-2.0` 的 blocking-pose / waypoint inbetweening 切片，再加 `LMC-Memory`，最后再上 `SOAMPrevis`。

## 4. Ds Max Polished Ideas

### 4.1 Idea A: MSP — Motion Storyboard Previsualization

**一句话定义**：输入结构化 story / shot list / blocking pose / root waypoint / optional object anchor，输出 canonical 3D motion 和可选 shot metadata，目标是成为动画/游戏 previs 的可编辑中间层。

#### Problem Definition

输入不是单句文本，而是 shot-level 结构：

- 每个 shot 的动作文本；
- start/end body pose 或 sparse blocking pose；
- root waypoint / 6DoF spatial anchor；
- 角色、物体、场景区域标签；
- 可选 shot metadata：景别、虚拟相机、剪辑关系。

输出是标准 3D motion 序列。相机/shot metadata 是服务 previs 的副产品，不作为 canonical motion 的必要条件。

#### Difference from Competitors

- 相对 STAGE：从视频首尾帧对转向 3D start-end pose / root waypoint，输出 3D motion，不输出最终 video。
- 相对 Sketch2Anim：从 2D sketch 控制升级为 3D blocking / spatial anchor，减少单视角 ambiguity，并强调多 shot continuity。
- 相对 Sitcom-Crafter：从 LLM 自由拆剧情转向用户可编辑的结构化 storyboard。
- 相对 UniHM：保留 continuous 6DoF waypoint 思想，但任务从 scene-aware T2M 扩展为 storyboard previs。
- 相对 ActionPlan：不是只做 frame-level action plan，而是引入创作管线中的 shot / blocking / waypoint 结构。

#### Method Core

- **Storyboard Encoder**：将 shot text、start-end pose、root waypoint、object anchor 编码成 `space-time anchor set`。
- **Hybrid Motion Representation**：global path 用 continuous 6DoF waypoint，local body motion 用 per-joint latent 或 local token。
- **Boundary-Conditioned Generator**：在扩散 / flow / masked model 中注入 start-end pose embedding，生成中间 motion。
- **Local Regeneration Interface**：修改某个 shot 的 anchor 后，只重生成对应段落，并通过状态锚点与前后段衔接。

#### Minimum Experiment

最小切片不要一开始做完整 storyboard，先做 **single-character two-shot blocking inbetweening**：

- 数据：从 HumanML3D / BABEL / AMASS 中自动抽取 2-4 秒片段，取 start/end pose + root path 作为 pseudo storyboard。
- 任务：给定 start pose、end pose、root waypoint、文本，生成中间 motion。
- Baseline：纯 text-to-motion；只给 start/end pose 的 inbetweening；只给 root path 的 trajectory control。
- 指标：MPJPE、root trajectory RMSE、start/end pose error、foot skating ratio、编辑后前段保持率。
- 成功标准：比纯文本和单一控制信号明显降低 root / boundary error，同时 motion quality 不崩。

#### Biggest Risk and Scope Cut

- 风险：完整 storyboard 标准化太重。  
  砍法：先只做 start/end pose + root waypoint，不做多角色、不做相机、不做物体。
- 风险：和传统 motion inbetweening 重叠。  
  砍法：把创新点压在“storyboard / blocking 作为创作接口 + continuous global path + local latent”的组合，而不是泛泛补间。
- 风险：多 shot memory 一开始难做。  
  砍法：第一版只做两个 shot，跨段连接用最后 K 帧状态锚点。

**保留判断**：强烈保留。它最贴合用户已有分镜想法，也最能绕开“视频相机控制不能直接迁移”的问题。

### 4.2 Idea B: SOAMPrevis — Scene-Object Affordance Motion Previs

**一句话定义**：把 storyboard 中的物体交互转成 affordance anchors，生成可编辑的 scene-object-aware 3D motion previs。

#### Problem Definition

输入：

- 单个 shot 的动作文本；
- 3D object anchor：物体位置、朝向、可交互部位、功能类型；
- 可选 root waypoint 和 start pose。

输出：

- 角色 motion；
- 接触时刻和接触部位；
- 当物体移动时，局部调整 motion。

这不是完整 HOI 终局生成，而是 previs 阶段的可编辑 motion blocking。

#### Difference from Competitors

- 相对 UniHM：从“文本 + 场景点云”转向“storyboard + object affordance anchor”，强调创作者可编辑。
- 相对 Sitcom-Crafter：物体关系由用户/分镜显式指定，不交给 LLM 自由决定。
- 相对 GRAB / BEHAVE 类 HOI：不只复现单物体交互，而是把交互 anchor 接到 storyboard previs 接口。
- 相对 Sketch2Anim：从 sketch pose/trajectory 扩展到可移动物体 anchor。

#### Method Core

- **Affordance Anchor Embedding**：把物体交互点表示为连续 6DoF anchor，加功能类型，如 `sit`、`grasp`、`place`、`lean`。
- **Contact-Aware Generator**：生成时显式约束手/脚/骨盆与 anchor 的距离和时序接触状态。
- **Per-Joint Local Editing**：借鉴 PRISM 的关节分解思想，物体移动时优先重生成 root、spine、arm 等受影响 token，而不是整段重采样。

#### Minimum Experiment

先不做完整室内场景，只做 **single-object single-shot affordance control**：

- 数据：GRAB / BEHAVE / HIMO / CHAIRS 中 pick、place、sit、touch 等简单交互。
- 任务：给定 object anchor 和文本，生成接触合理的短 motion。
- Baseline：只给文本；给文本 + root target；UniHM-style waypoint without contact anchor。
- 指标：contact distance、penetration / collision proxy、root-target error、MPJPE、物体移动后的局部编辑成功率。
- 成功标准：物体位置变化后，接触误差明显低于纯文本和 root-only baseline，且不需要整段重采样才能适配。

#### Biggest Risk and Scope Cut

- 风险：真实物体交互太难，接触/穿模指标容易不稳定。  
  砍法：第一版只做单手触碰或拿取，不做坐下、双手、复杂操作。
- 风险：scene mesh / object annotation 成本高。  
  砍法：只用 object anchor，不用完整 mesh；物体几何先简化为 bbox / contact point。
- 风险：与 UniHM 重叠。  
  砍法：强调 `editable affordance anchor for previs`，而不是通用 scene-aware T2M。

**保留判断**：作为 MSP-2.0 的场景交互扩展保留。单独成主线风险较高，但能显著提高 idea 的工业 previs 价值。

### 4.3 Idea C: LMC-Memory — Long-form Motion Continuity via Memory Anchors

**一句话定义**：为多段 motion generation 显式维护最小必要状态记忆，让下一段生成继承上一段的 root、heading、foot contact 和可选 hand-object state。

#### Problem Definition

长动作或多 shot 生成中的核心失败不是“不能继续生成”，而是段落边界状态断裂：

- root 位置/朝向突然跳；
- 脚触地状态不连续，引起滑步；
- 手持物或接触对象状态丢失；
- 上一段末尾姿态没有以可控方式进入下一段。

目标是在不引入视频或相机的前提下，定义 motion 专用的 memory anchor，作为下一段生成条件。

#### Difference from Competitors

- 相对 STAGE：借鉴 memory pack 思想，但 memory 内容从像素实体一致性改为 3D motion state consistency。
- 相对 PRISM：PRISM 用 causal VAE 和 self-forcing 抑制长序列漂移，但关键状态主要隐式存在 latent 中；这里显式定义 root/contact/object memory。
- 相对 ActionPlan：ActionPlan 有逐帧语义 plan 和 latent-specific timestep，但没有专门建模段间物理状态。
- 相对 FlowMDM / PriorMDM：它们更像片段 composition / blending，这里强调“最小必要状态”作为可解释条件。
- 相对 UniHM：waypoint 可指定空间目标，但不等于跨段状态记忆，尤其不处理接触状态。

#### Method Core

- **Memory Anchor Encoder**：从上一段末尾 K 帧提取 root position、root velocity、heading、foot contact、可选 hand-object state，编码为固定维度 anchor。
- **Anchor-Conditioned Generation**：下一段生成时将 anchor 作为 cross-attention / FiLM 条件注入扩散或 flow 模型。
- **Boundary Loss**：只在下一段前若干帧施加 root continuity、heading continuity、foot contact consistency，避免整个片段被锚点过度束缚。
- **Optional Memory Bank**：多 shot 时保存最近几个 anchor；第一版只用 last anchor。

#### Minimum Experiment

做 **two-segment continuation**，不直接挑战无限长：

- 数据：HumanML3D / BABEL 中切分长 motion，前段 A 给真实 motion，后段 B 给文本或动作标签。
- Baseline：纯文本生成后 root 对齐；简单插值/平滑；ActionPlan / PRISM 风格 continuation；FlowMDM/PriorMDM composition。
- Ours：root + heading anchor，增强版加 foot contact anchor。
- 指标：boundary root error、heading error、first-second foot slip ratio、transition jerk、用户偏好。
- 成功标准：root 对齐 baseline 不能解决 foot slip / jerk，而 anchor 模型能显著降低边界 artifact。

#### Biggest Risk and Scope Cut

- 风险：简单 root 对齐 + 平滑就能解决大部分问题，导致方法显得过度设计。  
  砍法：必须把 foot contact / heading / transition jerk 作为核心指标，证明不是只对齐位置。
- 风险：contact 标签噪声高。  
  砍法：第一版只用 root + heading anchor；若差异不够，再加入自动 foot contact。
- 风险：多段误差累积。  
  砍法：限制为两段或三段 continuation，先证明 memory anchor 的局部价值。

**保留判断**：保留，但更适合作为 MSP-2.0 的关键模块，而不是独立主线。若实验证明它比 root 对齐 + smoothing 强，再独立扩展。

## 5. Rejected or Down-ranked Ideas

- **Blocking-Pose-to-Motion / Spatial Keyframe Inbetweening**  
  不单独保留。它是 MSP-2.0 的最小实验切片；单独作为 idea 容易落入传统 motion inbetweening。
- **Motion Latent Interface for Downstream Video/Avatar Rendering**  
  暂时砍掉。`renderability-aware` 评测定义不清，容易转向视频/渲染系统，偏离当前想要的 motion idea 构建。
- **Fine-grained Motion Script Compiler**  
  降级为工具层。它适合给 MSP-2.0 提供结构化输入格式，但如果单独成论文，容易变成 workflow / DSL，而不是 motion generation 的核心方法。
- **继续 MoDebug / MoProbe**  
  本轮不保留。除非后续出现稳定数据趋势，否则不应继续把诊断/探针路线作为主 idea。

## 6. Summary and Next Steps

### 6.1 Recommended Research Position

最推荐的组合是：

> `MSP-2.0 = storyboard / blocking / waypoint -> 3D motion previs`  
> `LMC-Memory = cross-shot continuity module`  
> `SOAMPrevis = object affordance extension`

核心叙事是：视频生成的 storyboard 范式不能直接变成 motion 相机控制，但可以转译为 **3D motion previs 的可编辑结构化接口**。这个接口不追求最终像素质量，而是服务动画、游戏、虚拟人制作中的 blocking、inbetweening、局部重生成和场景交互预演。

### 6.2 Immediate To-do

1. **先做 MSP-2.0 最小切片**  
   从 HumanML3D/BABEL 自动构造 start/end pose + root waypoint pseudo-storyboard，验证 boundary + waypoint control 是否有效。
2. **并行做 LMC-Memory 小实验**  
   对两段 motion continuation 比较 `root smoothing`、`root+heading anchor`、`root+heading+foot contact anchor`。
3. **暂缓 SOAMPrevis**  
   等 MSP-2.0 的接口稳定后，再接入 object anchor；否则会同时面对 HOI 和 storyboard 两个难题。
4. **不要急着做相机输出**  
   相机/shot metadata 只作为 previs 的 optional annotation，不进入第一阶段训练和指标。

### 6.3 Venue Positioning

- SIGGRAPH / SIGGRAPH Asia：如果强调 animation previs、blocking pose、editable workflow。
- CVPR / ICCV / ECCV：如果强调 structured conditioning、scene/object affordance、benchmark。
- ICLR / NeurIPS：如果强调 representation、memory anchor、long-form generative modeling。
