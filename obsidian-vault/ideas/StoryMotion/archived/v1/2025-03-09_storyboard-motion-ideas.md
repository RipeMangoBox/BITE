---
created: 2026-03-08T14:35
updated: 2026-04-12T18:29
title: 2025-03-09 分镜 + 文本驱动的动作生成脑暴
source:
  - merged from the 2026-03-11 keyframe-text-rich-inbetweening draft
---
# 2025-03-09 分镜 + 文本驱动的动作生成脑暴

> 灵感来源：视频生成中「图像分镜（storyboard）+ 文本描述」联合控制的范式（如 STAGE、VAST、StoryDiffusion），希望在 3D 动作生成领域引入类似的「分镜 + text」接口与建模方式。

---
Drawing：[[Storyboard|Storyboard]]

## 一、想法拆解与联想

- **问题重述**  
  - 现有视频生成模型已经开始支持「图像分镜序列 + 文本描述」作为输入，用 storyboard 约束镜头结构与视觉布局，用文本补充细节与风格；  
  - 你希望在 **动作生成** 中也有类似的接口：用户给出若干关键「动作分镜」（可以是 2D/3D pose、低帧率草图动作、甚至简单 stick figure），再配合文本描述，让模型生成**时序连续、细节丰富且物理合理**的全身 3D 动作。

- **多维拆解**  
  - **输入形式**：  
    - 分镜 = 一系列关键时间点的姿态/短片段（keyframes / key-poses / skeleton thumbnails），可能是 2D 或 3D；  
    - 文本 = 整体语义描述（「角色愤怒地挥拳冲向镜头」）、风格描述（「夸张卡通」、「写实冷酷」）、物理 / 节奏约束（「停顿后突然加速」）。  
  - **输出目标**：  
    - 全时长 3D 动作序列，**严格通过这些分镜**，在分镜之间进行高质量「in-betweening」；  
    - 细节（力量感、身体协同、面部 / 手势）由模型自动补足，文本控制整体表现风格与情绪；  
    - 在需要时可以进一步接到数字人、视频渲染或游戏引擎。
  - **模型职责拆分**：  
    - 「规划层」：理解文本与分镜序列，决定各分段的运动类型、节奏与重要关键帧；  
    - 「生成层」：在给定关键 pose / 片段与高层语义条件下，做高保真动作 in-betweening 与 refinement；  
    - 「物理 / retargeting 层」：保证物理合理性与跨体型可用性。

- **与现有工作的联想连接**  
  - 视频侧：  
    - **STAGE**：用 storyboard 锚定多镜头叙事结构；  
    - **VAST**：用 pose、分割图、深度等中间表示作为 storyboard 控制视频生成；  
    - **StoryDiffusion**：通过一致 self-attention 保证长序列图像 / 视频的一致性。  
  - 动作侧：  
    - Keyframe / trajectory 控制的 motion diffusion（如 Guided Motion Diffusion, CondMDI, sMDM, IKMo, Move-in-2D 等），已经证明「稀疏 keyframes + 文本」在动作 in-betweening 中非常有效。  
  - 你的 idea 可以视为：**把 storyboard-style thinking 和 keyframe motion diffusion 做一次系统融合和接口提升**。

---
## 二、真实场景与需求痛点

- **典型场景 1：动画 / 游戏分镜到 3D 动作**  
  - 动画导演 / 游戏动作设计师通常已经有清晰的分镜草图（2D 略图）和文字说明；  
  - 目前 pipeline：分镜 → 动捕 / 手 K 动画 → 大量反复修改与润色。  
  - 痛点：  
    - 手工 K 动画或动捕清洗成本极高；  
    - 分镜与最终动作之间存在较大「语义落差」，分镜难以直接驱动生成。

- **典型场景 2：虚拟人 / 直播脚本到动作**  
  - 内容团队往往有台本（文本）和若干「关键姿态」或海报式图像，想让虚拟人按脚本演绎；  
  - 需要可控的分段动作设计，而不是连续黑盒生成。  
  - 痛点：  
    - 现有 text-to-motion 接口太粗糙，只能整体描述，难以对每一小段精确控制；  
    - 编辑难：如果只想改其中一小段的姿态或表演强度，经常需要重生成整段。

- **典型场景 3：原型设计与快速迭代**  
  - 导演 / 设计师希望快速用「几张草图 + 标签」搭出 rough blocking，看整体节奏是否合适，再决定是否精修；  
  - 需要的是**高可控 / 高交互**而非一键成片。  

- **总结痛点**  
  - 缺乏一个自然的「分镜 + 文本 → 动作」接口，使得动补 / K 动无法真正站在 storyboard 这一上游资产上；  
  - 现有 motion diffusion 虽支持 keyframe / 轨迹，但缺少故事层次的结构建模与统一接口。

---
## 三、相关工作支持与研究空间（分镜 + text → motion）

### 3.1 相关工作概览（视频 & 动作）
- **Storyboard / 结构化控制的视频生成**  
  - **STAGE: Storyboard-Anchored Generation for Cinematic Multi-shot Narrative**（2025，multi-shot narrative）  
    - 思路：用 storyboards（每个 shot 的起止帧）锚定整部影片，学习跨镜头记忆与过渡，实现长叙事视频生成。  
    - 启示：  
      - 将长序列拆为结构化 shots，并为每个 shot 设计中间表征，是处理长程叙事的一条路。  
  - **VAST: Video As Storyboard from Text**（2024）  
    - 思路：text → 中间表示（pose、segmentation、depth）→ diffusion 生成视频；  
    - 把这些中间表示视为「可编辑 storyboard」。  
  - [StoryDiffusion: Consistent Self-Attention for Long-Range Image and Video Generation](https://storydiffusion.github.io/) (NeurIPS 2024 Spotlight)
    - 思路：在 diffusion 中引入一致 self-attention 与 semantic motion predictor，使多图像 / 视频片段保持一致的角色与语义。

- **Keyframe / 轨迹条件的动作生成**  
  - **IKMo: Image-Keyframed Motion Generation with Trajectory-Pose Conditioned Motion Diffusion Model**  
    - 从用户图像和文本提取关键 pose + 轨迹，用 ControlNet 风格结构控制 motion diffusion；  
    - 证明了「图像 keyframe + 文本」组合在动作生成上的可行性。  
  - **CondMDI / GMD / sMDM 等 keyframe-based diffusion**  
    - 支持稀疏 keyframe、部分 body constraints 和文本联合控制 in-betweening；  
    - 强调「动画师风格的 keyframe-centric workflow」。  
  - **Move-in-2D**  
    - 用 2D scene image + text 作为条件，生成与背景对齐的 3D motion，说明 2D 条件完全可以驱动 3D 动作。

### 3.2 支持点

- 以上工作共同证明：  
  - **中间表征 + 文本** 是可扩展的控制接口（视频侧 = 分割 / pose / depth，动作侧 = keyframe / 轨迹 / skeleton）；  
  - 稀疏的 keyframe / storyboard，经过合适的 diffusion / Transformer in-betweening，可以恢复出高质量连续时序；  
  - 2D 线索（图像 / 视频 / pose）可以可靠地约束 3D 动作生成。
- **ResearchWY 当前收录下的直接证据链**
  - [[paperAnalysis/Motion_Generation/SIGGRAPH_2024/2024_CondMDI_Flexible_Motion_In_betweening_with_Diffusion_Models|CondMDI]] 是目前最直接支持“关键帧 + 可选文本 → 补间”的代表工作；
  - 但现有 keyframe / in-betweening 文献的主目标仍偏向**平滑过渡、约束满足、自然度**，而不是“在关键帧之间生成更丰富的中间语义动作”；
  - 因此这个方向真正值得保留的增量，不是重复证明 keyframe+text 可行，而是把 **storyboard 级结构控制、rich in-betweening、上游制作资产接入** 统一成一个更自然的生成接口。

### 3.3 研究空间

- **从「局部 keyframe」提升到「故事级分镜」**  
  - 现有 motion diffusion 多以局部 keyframe / 轨迹为单位，没有系统地建模整段故事结构（多镜头、多 shot、多情节避让）。  
  - 你的 idea 可以：  
    - 引入「shot / segment」概念，将长动作序列拆为若干分镜段落，每段有自己的 keyframes + 文本；  
    - 建立 cross-segment consistency（动作风格 / 角色设定 / 节奏）的统一建模。

- **统一分镜表示**
  - 动画 / 游戏制作中，分镜形式多样：草图、分镜表、pose 图、简笔二维图等；  
  - 研究空间在于设计一个**统一、可学习的 storyboard 表示**，既兼容 2D/3D pose，也能编码镜头信息（视角、距离）。  

- **与物理、retargeting 的结合**
  - 大多数 keyframe motion 工作关注「语义正确 + 视觉合理」，对物理和跨体型一致性关注有限；  
  - 你的方向可以把 storyboard-conditioned 生成与课题 A 中「高保真物理」和「高保真重定向」结合起来，构成完整 pipeline。

---
## 四、前沿交叉技术与验证思路

### 4.1 可借鉴的前沿技术

- **Storyboard / 中间表征驱动的视频扩散**  
  - STAGE / VAST / StoryDiffusion 的共同点：  
    - 用结构化 storyboard（pose、seg、depth、关键帧）作为 diffusion 的控制信号；  
    - 将长序列拆为 shots，并通过记忆或一致性模块保持整体风格与语义。  

- **Keyframe-based Motion Diffusion 与 ControlNet 思路**  
  - IKMo、CondMDI、GMD、sMDM 等证明：  
    - 稀疏 keyframe + 文本足够支撑高质量 motion in-betweening；  
    - 可以通过 ControlNet / dense guidance 把稀疏姿态信号变成对整个时序的软约束。

- **长序列与阶段化建模**  
  - 结合你在 `2025-03-08` 中总结的：Motion Mamba、TransPhase、TEDi 等长序列模型 + MoE / phase-based 建模；  
  - 可以将「分镜段落」作为 gating 或 expert 划分依据，建立「分段专家」结构。

### 4.2 可能的系统设计草图

- **接口设计**  
  - 输入：  
    - 分镜序列：\[(t\_i, pose\_i, optional image/sketch\_i)\]\_{i=1..K}；  
    - 文本：整体描述 + 段落描述（每个分镜附带一段文本说明）。  
  - 输出：  
    - 全序列 3D motion（可选：同时输出中间渲染或 2D 可视化）。

- **模型分层**  
  1. **Storyboard encoder**：  
     - 将一系列分镜（时间戳 + pose + optional image）编码为一组 tokens，包含时序与身体结构信息；  
     - 可以使用 Transformer / Mamba + GCN、part-based 表示。  
  2. **Text encoder**：  
     - 使用预训练 LLM / text encoder，将全局/局部文本编码为条件向量；  
     - 支持「整体风格」与「每段指令」。  
  3. **Motion diffusion / Transformer decoder**：  
     - 在 storyboard + text 条件下生成整段动作；  
     - 训练时 mask 非 keyframe 帧，学习 in-betweening；  
     - 使用 Consistency / LCM 风格蒸馏，提升推理速度。  
  4. **物理 / retargeting 后端**：  
     - 接入物理增强与跨体型重定向模块，对生成结果做后处理或联合训练。

- **验证思路（MVP 实验）**  
  - 数据层：  
    - 从现有 motion dataset 中自动抽 keyframes 作为 “分镜”，附上自动或人工文本描述；  
    - 或利用已有文本-caption 数据（HumanML3D）+ 关键姿态抽取构建伪分镜数据。  
  - 评估：  
    - 标准 motion generation 指标（R-precision, FID, diversity）；  
    - 分镜一致性：生成动作在 keyframe 处与输入差异；  
    - 人类偏好：对比「只用文本」 vs 「分镜+文本」在可控性与表达力上的提升。

---
## 五、总结与下一步

- **核心 idea 概括**  
  - 将视频生成中的「storyboard + text」控制范式迁移到 3D 动作生成：通过统一的分镜表示和文本条件，引导大模型在分镜之间生成高保真、物理合理且风格一致的动作。  
  - 相比现有 keyframe-based motion diffusion，你的方向更强调**故事结构（多段分镜）与上游制作资产（分镜稿）**的融合，而不仅是局部 in-betweening。

- **近期可执行步骤**  
  1. 在 ResearchWY 中基于 paper-knowledge-base 系统整理 storyboard-based video generation 与 keyframe-based motion diffusion 代表论文，做一页「相关工作 & 研究空间」表；  
  2. 选定一个简单场景（例如单人情绪化行走 / 打招呼序列），构造小规模「分镜 + 文本 + 动作」数据集，用现有 motion diffusion baseline 实验「keyframe + text」的性能上限；  
  3. 在此基础上逐步加入「分镜段落结构」（shot / segment），测试长序列下 storyboard 控制的效果；  
  4. 结合你在腾讯犀牛鸟课题脑暴中的方向，思考如何将该接口接入游戏 / 动画制作 pipeline，作为实际落地的 selling point。



## storyboard motion generation（Q&A）

**Q1：这个任务的定义是什么？**
- **A**：输入为「分镜约束（关键动作/草图/图片）+ 动作脚本（文本）+（可选）场景」，输出为一段**连续**的 3D 动作序列，满足脚本语义、满足分镜约束，并（可选）与场景交互合理。

**Q2：它和 motion-inbetweening / T2M 的关键区别是什么？**
- **A**：把“分镜”定义成 **multi-shot / camera-discontinuous constraints**：关键帧来自不同 shot（相机跨度大、观测不连续），但输出必须是一段**单一连续**的 3D motion。
  - 相比 **inbetweening**：不再假设关键帧都在同一坐标系/同一观测视角里“可直接插值”。
  - 相比 **T2M**：不是纯文本自由生成，而是要同时满足分镜硬约束（关键姿态/轨迹/片段）。
  - 对应参考：从 storyboard 的 2D 约束桥接到 3D 控制并生成连续片段：[[paperAnalysis/Motion_Generation/TOG_2025/2025_Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation|Sketch2Anim]]。

**Q3：输入/输出接口怎么拆最清晰（MVP 优先）？**
- **A（MVP, Minimum viable product，不引入场景）**：
  - **Input**
    - 分镜约束：\(\{(y_i,\tau_i,\pi_i)\}_{i=1..K}\)，每个 shot 给 2D keypose / stickman / 草图轨迹 \(y_i\)，其落点时间 \(\tau_i\)，以及相机投影（或弱透视参数）\(\pi_i\)；
    - 动作脚本：整体文本 +（可选）shot/段落级子指令（更像“动作剧本”而非一句 caption）。
  - **Output**
    - 连续 3D motion \(X_{1:T}\)，同时满足：投影一致性 \(\pi_i(X_{\tau_i})\approx y_i\)、长程平滑/连贯、脚本语义对齐。

**Q4：如果加 scene-aware，该怎么加而不让链路爆炸？**
- **A**：把“场景”当作一个可插拔条件分支或后处理目标，而不是从零做一个端到端的大系统：
  - **scene-aware inbetweening 模块**：给定（稀疏/噪声）关键帧 + 场景几何，补全中间并显著降低碰撞/足滑/抖动：[[paperAnalysis/Human_Interaction/ICCV_2025/2025_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions|SceneMI]]。
  - **两阶段（导航→交互）模块**：先生成走到目标物体附近的轨迹，再生成交互动作（坐下等）：[[paperAnalysis/Motion_Generation/ECCV_2024/2024_TesMo_Generating_Human_Interaction_Motions_in_Scenes_with_Text_Control|TeSMo]]。

**Q5：数据怎么拿？我缺“带相机的分镜-motion”怎么办？**
- **A**：不必强依赖真实“分镜+相机+3D motion”成对数据，优先用“可控伪分镜”构造训练对：
  - **路线 A（推荐，合成分镜）**：用任意 mocap/文本数据（HumanML3D/KIT/AMASS 等）抽 K 个关键时刻/短片段，然后**每个 shot 独立采样相机**渲染出 2D 约束（keypose / stickman / 轨迹草图），天然得到 camera-discontinuous storyboard。
    - 2D 约束 → 3D 控制的桥接思路可直接对齐：[[Sketch2Anim]]、[[paperAnalysis/Motion_Generation/CVPR_2025/2025_StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman|StickMotion]]。
  - **路线 B（带场景、多视角渲染）**：直接使用可渲染 multi-view 的 HSI 数据/基座：
    - MoCap 级、100 场景、15 小时，并提供 multi-view/ego-view 渲染：[[paperAnalysis/Human_Interaction/CVPR_2024/2024_TRUMANS_Scaling_Up_Dynamic_Human_Scene_Interaction_Modeling|TRUMANS]]。
    - SceneMI 也以 TRUMANS 为核心训练/评测基座：[[SceneMI]]。

**Q6：一条“最小可行链路（MVP）”长什么样？**
- **A**：
  - **分镜表示统一**：stickman / 2D keypose / 轨迹（可参考 StickMotion 的 stickman 约束形式）；
  - **生成器（先不加场景）**：用 keyframe/inpainting 风格的扩散作为骨架，先把“遵守稀疏约束补全整段”跑通；
  - **再叠加**：shot/段落脚本（多段文本）→ 长序列组合能力 → scene-aware 分支（可选）。

### knowledge base：推荐 backbone / 模块（paperAnalysis 本地连接）

- **Storyboard/草图 → 3D 生成（核心接口）**
  - [[paperAnalysis/Motion_Generation/TOG_2025/2025_Sketch2Anim_Towards_Transferring_Sketch_Storyboards_into_3D_Animation|Sketch2Anim]]：2D↔3D 约束对齐 + Trajectory-ControlNet + Keypose Adapter。
  - [[paperAnalysis/Motion_Generation/CVPR_2025/2025_StickMotion_Generating_3D_Human_Motions_by_Drawing_a_Stickman|StickMotion]]：stickman-as-condition，适合作为“分镜关键姿态/草图”的低门槛输入代理。

- **Keyframe / in-betweening backbone（MVP 生成器优先）**
  - [[paperAnalysis/Motion_Generation/SIGGRAPH_2024/2024_CondMDI_Flexible_Motion_In_betweening_with_Diffusion_Models|CondMDI]]：mask 条件扩散，支持任意稀疏/局部关键帧约束（很适合承载 storyboard 约束）。
  - [[paperAnalysis/Motion_Generation/ICCV_2025/2025_Less_Is_More_Improving_Motion_Diffusion_Models_with_Sparse_Keyframes|Less Is More (sMDM)]]：关键帧中心建模（高效且更像动画工作流）。

- **长序列/脚本驱动 backbone（把“分镜段落/shot”变成可执行长动作）**
  - [[paperAnalysis/Motion_Generation/CVPR_2024/2024_FlowMDM_Seamless_Human_Motion_Composition_with_Blended_Positional_Encodings|FlowMDM]]：多段文本 → 一次性长动作组合（对“分镜段落脚本”很友好）。
  - [[paperAnalysis/Motion_Generation/ECCV_2024/2024_Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation|Motion Mamba]]：长序列效率与质量兼顾（作为长时 backbone 候选）。
  - [[paperAnalysis/Motion_Generation/TPAMI_2023/2023_MotionDiffuse_Text_Driven_Human_Motion_Generation_with_Diffusion_Model|MotionDiffuse]]：time-varied prompts 的长动作控制思路（可迁移到“脚本分段条件”）。

- **Scene-aware / HSI 模块（可插拔增强）**
  - [[paperAnalysis/Human_Interaction/ICCV_2025/2025_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions|SceneMI]]：scene-aware inbetweening（关键帧 + 场景 → 中间补全，显著降碰撞/足滑/抖动）。
  - [[paperAnalysis/Motion_Generation/ECCV_2024/2024_TesMo_Generating_Human_Interaction_Motions_in_Scenes_with_Text_Control|TeSMo]]：导航→交互两阶段，适合作为“scene-aware 版本”的结构模板。
  - [[paperAnalysis/Human_Interaction/CVPR_2024/2024_TRUMANS_Scaling_Up_Dynamic_Human_Scene_Interaction_Modeling|TRUMANS]]：HSI 数据与 episode-wise 生成范式（也提供 multi-view/ego-view 渲染）。
  - [[paperAnalysis/Human_Interaction/ICCV_2025/2025_SIMS_Simulating_Human_Scene_Interactions_with_Real_World_Script_Planning|SIMS]]：RAG+LLM 把主题变脚本/关键帧，再由低层控制执行（适合你“动作脚本”输入形态）。

- **相机/镜头侧的可借鉴表示（如果未来把 camera 当显式条件）**
  - [[paperAnalysis/Image_Video_Generation/CVPR_2025/2025_TokenMotion_Decoupled_Motion_Control_via_Token_Disentanglement_for_Human_centric_Video_Generation|TokenMotion]]：把 camera trajectory 与 human motion 都 token 化，并做可学习融合（更偏 video，但对“相机条件怎么进模型”有启发）。
