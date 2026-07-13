---
title: "Gloria: Consistent Character Video Generation via Content Anchors"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Gloria_Consistent_Character_Video_Generation_via_Content_Anchors.pdf
project_link: "https://yyvhang.github.io/Gloria_Page/"
code_link: null
aliases:
- Gloria
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 通过内容锚点（全局、视角、表情）提供稳定参考，配合‘超集内容锚定’避免复制粘贴、‘RoPE弱条件’解决多锚点冲突，从而控制生成一致性。
primary_logic: 将角色视频生成视为‘从外向内看’场景，利用一组锚点帧紧凑地表征角色的多视角外观和表情，并作为全局参考引导长序列生成。
claims:
- 在长时一致性上，Gloria在Sub.、Back.、Arcface等指标上显著优于现有方法
- 在多视角外观和表情身份一致性上，Gloria的DINO-I、CLIP-I、Exp.等指标大幅领先
- 消融实验表明，超集内容锚定和RoPE弱条件分别消除了复制粘贴模式并解决了多锚点冲突，显著提升一致性
- 注意力可视化证明模型在角色转身时高度关注视角锚点，验证了锚点的有效利用
---

# Gloria: Consistent Character Video Generation via Content Anchors

> [!tip] 核心洞察
> 将角色视频生成视为‘从外向内看’场景，利用一组锚点帧紧凑地表征角色的多视角外观和表情，并作为全局参考引导长序列生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | Gloria：基于内容锚点的角色一致性视频生成 |
| 英文题名 | Gloria: Consistent Character Video Generation via Content Anchors |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.29931) · [Project](https://yyvhang.github.io/Gloria_Page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Gloria |
| Dataset | Long-term Consistency Testset, Multi-View Appearance & Expressive ID Testset, Fundamental Capability Testset, CelebV-HQ |

> [!tip] 效果简介
> - Long-term Consistency Testset (20 clips, 5-10 min) 上，Subject Consistency, Background Consistency, Arcface 0.960, 0.951, 0.787 (显著优于所有对比方法)。
> - Multi-View Appearance & Expressive ID Testset (50 characters, 40 sets) 上，DINO-I, CLIP-I, Exp. 0.821, 0.858, 0.717 (显著优于多参考方法)。
> - Fundamental Capability Testset (95 cases) 上，IQA, AES, Sync-C, Sync-D 4.65, 3.63, 5.12, 8.83 (全面领先)。

## 概要

### 问题与瓶颈
在长序列、多视角和复杂表情变化下保持角色外观与身份的一致性，是当前角色视频生成的核心挑战。现有方法通常缺乏紧凑且结构化的持久视觉参考，导致生成结果在长时间跨度内出现身份漂移、背景退化或视角错乱。Gloria 将这一问题重新定义为“从外向内看”的场景：通过一组精心构建的**内容锚点（Content Anchors）**，为模型提供稳定、可区分的全局外观、多视角和表情参考。

### 核心方法定位
Gloria 的核心创新在于**内容锚点框架**，包含三个关键设计：

1. **三类结构化锚点**：全局锚点（$C_g$）提供场景与外观的整体参照，视角锚点（$C_v$）编码多角度外观，表情锚点（$C_e$）捕捉面部表情身份。三者共同构成角色的紧凑视觉表征。
2. **超集内容锚定（Superset Content Anchoring）**：将锚点采样范围从训练片段内扩展到全源视频，迫使模型学习跨片段的关联而非简单的复制粘贴，从根本上消除了“copy-paste”模式。
3. **RoPE弱条件（RoPE as Weak Condition）**：为不同类型的锚点及其子类别分配独立的时间偏移量（见公式 $\text{RoPE}_i = \text{RoPE}(t + o_i + so_j, h_i, w_i)$），使模型在自注意力中隐式区分多锚点身份，解决了多锚点同时注入时的注意力冲突问题。

在方法谱系上，Gloria 以 **Wan-I2V** 为骨干架构，通过全注意力机制将锚点潜在表示与视频序列拼接注入，同时支持文本、图像和音频等多模态条件。与仅使用单一参考图像或文本的方法（如 **InfiniteTalk**、**HunyuanAvatar**、**Phantom** 等）相比，Gloria 首次在统一框架内实现了长时、多视角外观和表情身份的三维一致性控制。

### 主要结果概要
在长时一致性测试集上，Gloria 的 Subject Consistency 达 **0.960**、Background Consistency 达 **0.951**、Arcface 达 **0.787**，显著优于所有对比方法（Table 1）。在多视角外观与表情身份一致性测试中，DINO-I 达 **0.821**、CLIP-I 达 **0.858**、Exp. 达 **0.717**，大幅领先多参考方法（Table 2）。消融实验（Table 4、Figure 7、Figure 8）证实：超集内容锚定消除了复制粘贴模式，RoPE弱条件有效解决了多锚点冲突，注意力可视化（Figure 10）进一步验证了模型在角色转身时对视角锚点的高度关注。此外，Gloria 支持生成超过 10 分钟的连续角色视频，并在基础能力测试（Table 3）和 CelebV-HQ 基准（Table 7）上全面领先。



角色视频生成是当前视觉内容创作的核心需求之一，其目标是在保持角色外观一致性的前提下，生成长时间、多视角、表情丰富的动态视频。近年来，扩散模型（diffusion models）的快速发展显著提升了视频生成的视觉质量与运动自然度，但在**角色身份一致性**这一关键维度上仍存在明显瓶颈。

现有方法通常依赖单一参考图像或文本描述来约束角色外观。这类方案在短视频片段中尚可维持基本一致性，但面对**长序列生成**时，参考信息逐渐稀释，导致角色外观漂移、背景退化，甚至出现“复制粘贴”式的伪影（copy-paste pattern）。部分工作尝试引入多参考帧来增强约束，但由于缺乏对参考帧类型的结构化区分，不同锚点之间容易产生注意力冲突，反而引发生成混乱。此外，现有方法在同时处理**多视角外观保持**与**表情身份一致性**两个子问题时，往往顾此失彼——要么视角切换时角色特征丢失，要么表情变化时身份信息被覆盖。

Gloria 的动机正是源于这一观察：**角色视频生成本质上是一个“从外向内看”的场景**，即用户需要从不同角度观察同一角色在不同表情下的动态表现。因此，一个紧凑而结构化的参考表征——而非零散的多帧输入——才是解决一致性问题的关键。基于此，Gloria 提出**内容锚点（Content Anchors）**框架，将角色视觉属性编码为一组精心构造的锚点帧（全局锚点、视角锚点、表情锚点），并设计配套的注入与消歧机制，使得模型能够稳定地参考这些锚点生成长达 10 分钟以上的一致角色视频。



## 核心方法与创新机理

Gloria的核心创新在于将角色视频生成重新定义为“从外向内看”的场景，并引入**内容锚点（Content Anchors）**作为紧凑、结构化的持久视觉参考。与现有方法仅依赖单一参考图像或文本提示不同，Gloria通过一组精心设计的锚点帧（全局锚点、视角锚点、表情锚点）来表征角色的多视角外观和表情身份，从而在长序列生成中维持一致的角色身份。

### 关键机制：从瓶颈到因果调控

现有角色视频生成方法面临的核心瓶颈是：缺乏紧凑的结构化参考帧来提供持久的外观和身份信息，导致长序列、多视角和表情变化下的一致性崩溃。Gloria通过以下三个因果调控旋钮解决了这一问题：

**1. 内容锚点注入（Anchor Injection）**
Gloria通过全注意力机制将内容锚点注入视频扩散模型的潜在空间。具体而言，锚点帧经3D VAE编码并补丁化后，直接与视频潜在表示拼接，使模型在去噪过程中持续访问全局外观（全局锚点）、多视角特征（视角锚点）和表情身份（表情锚点）。这一设计将角色一致性从隐式记忆转化为显式条件，显著降低了长序列生成中的身份漂移。

**2. 超集内容锚定（Superset Content Anchoring, SCA）**
传统方法在训练时仅从当前片段内采样参考帧，容易诱导模型学习“复制粘贴”模式——直接复制参考帧内容而非建立语义对应。Gloria的SCA策略将锚点选择范围扩展到全源视频，引入与当前片段外观、视角或表情不同但属于同一角色的“超集”锚点。这迫使模型学习跨帧的鲁棒对应关系，而非简单的帧复制。消融实验（Table 4）表明，SCA策略在长时一致性指标（Sub.、Back.）上带来显著增益，且定性结果（Figure 7）显示移除SCA后模型出现明显的复制粘贴伪影。

**3. RoPE弱条件（RoPE as Weak Condition, RWC）**
多锚点共存时，模型难以区分不同锚点的功能角色，导致注意力冲突和生成混乱。Gloria提出RWC策略：在3D RoPE的时间维度上，为每种锚点类型（全局、视角、表情）及其子类别分配不同的时间偏移量 $o_i$ 和 $so_j$，即：
$$RoPE_i = RoPE(t + o_i + so_j, h_i, w_i)$$
这一设计以弱条件形式隐式编码锚点身份，使模型在自注意力计算中能够区分不同锚点的来源和用途，从而精准提取对应内容。消融实验（Figure 8）直接验证了RWC的关键作用：移除RWC后，多锚点冲突导致生成结果混乱；加入RWC后，模型能正确选择与文本提示匹配的锚点内容。

### 方法谱系与知识库定位

Gloria基于**Wan-I2V**架构构建，属于视频扩散模型（Video Diffusion Model）的范畴，采用流匹配（Flow Matching）作为训练目标。在技术路线上，Gloria与以下方法形成对比：

- **多参考方法**（如**Phantom**、**Humo**）：这些方法也使用多张参考图像，但缺乏结构化的锚点类型区分和冲突解决机制，在多视角和表情一致性上弱于Gloria（Table 2）。
- **长时一致性方法**（如**InfiniteTalk** (Shaoshu Yang et al., 2025)）：这些方法关注时序平滑性，但未显式建模角色外观的持久参考，在长序列中易发生身份退化。
- **商业模型**（如**Kling**、**Vidu-Q2**）：这些模型在基础生成能力上表现强劲，但在角色身份一致性方面缺乏专门的锚定机制。

Gloria的独特贡献在于将“内容锚点”系统化为一套完整的框架，包含锚点类型设计、采样策略（SCA）和冲突消解机制（RWC），为角色一致性视频生成提供了可扩展的技术方案。



Gloria 的整体流水线围绕“内容锚点”（Content Anchors）这一核心概念构建，将角色视频生成重新定义为“从外向内看”的场景：通过一组紧凑、结构化的锚点帧，持久地为生成过程提供外观与身份参考。流水线主要由数据构建、锚点编码与注入、多模态条件融合以及分块自回归推理四个环节构成，其整体结构如图 3 所示。

### 数据流水线与锚点构建

在训练数据准备阶段（图 2），系统首先对原始视频进行清洗与人体检测，随后从完整的源视频中提取三类内容锚点：
- **全局锚点（Global Anchor, C_g）**：选取角色正面、中性表情的清晰帧，捕获整体场景与身份信息。
- **视角锚点（Viewpoint Anchor, C_v）**：按角色朝向（相对于相机）分类，提供多视角外观参考。数据流水线在自建测试集上达到 98% 的视角锚点提取准确率。
- **表情锚点（Expression Anchor, E_e）**：按面部表情类别（如高兴、悲伤、惊讶等）分类，提供表情身份参考。仅使用 EmotiEffLib 时提取准确率为 66%，引入 Gemini 评判后提升至 82%。

三类锚点的设计分别对应长时一致性、多视角外观一致性和表情身份一致性这三个生成目标，构成后续所有模块的输入基础。

### 锚点编码与注入

锚点帧通过 3D VAE 编码为潜在表示，经补丁化（patchify）后与目标视频的噪声潜在表示在序列维度上拼接，送入 DiT 骨干网络进行全注意力计算。这一注入方式使得锚点信息能够直接参与自注意力交互，而非仅作为外部条件。

为消除训练中出现的“复制-粘贴”模式，Gloria 提出了**超集内容锚定（Superset Content Anchoring, SCA）**策略：锚点的选择范围从当前训练片段扩展至整个源视频，使锚点可能包含与当前片段不同的视角、表情或姿态。这迫使模型学习跨帧的对应关系，而非简单复制锚点内容。

为解决多锚点同时注入时的注意力冲突问题，Gloria 引入**RoPE 弱条件（RoPE as Weak Condition, RWC）**机制。在 3D RoPE 的位置编码中，为不同类型的锚点及其子类别分配不同的时间偏移量：

$$RoPE_i = RoPE(t + o_i + so_j, h_i, w_i)$$

其中 $o_i$ 为锚点类型（全局、视角、表情）的基础偏移，$so_j$ 为子类别（如视角类型、表情类别）的附加偏移。这种隐式的身份编码使模型在自注意力计算中能够区分不同锚点的来源与角色，从而按需提取对应信息。

### 多模态条件融合

除内容锚点外，Gloria 支持文本、图像和音频作为额外条件输入。文本和图像条件通过交叉注意力层注入 DiT 骨干；音频条件则采用局部窗口注意力机制，在时序维度上对齐唇动与语音，确保口型同步。

### 分块自回归推理

对于长视频生成，Gloria 采用分块自回归（Chunk-wise Autoregressive）推理策略。视频被划分为有重叠的片段，每个新片段的去噪过程以前一片段的最后 4 帧潜在表示作为前缀 token 进行初始化。相邻片段之间通过线性混合权重 $w = [1, 0.67, 0.33, 0]$ 进行过渡融合，公式为 $w \cdot x_1 + (1-w) \cdot x_2$，从而保证片段边界的平滑衔接。该策略使 Gloria 能够生成超过 10 分钟的角色视频。

### 训练策略

模型训练分为三个阶段递进进行：首先注入音频分支，确保基础的口型同步能力；随后引入全局锚点，建立长时一致性；最后加入视角和表情锚点，实现多视角外观与表情身份的一致性控制。这种渐进式训练策略有助于各模块的稳定收敛。

### 补充图表

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/003_Figure_3.jpg]]
*Figure 3: Overall of the Gloria pipeline, which includes the source of content anchors (Superset Anchors), the manner to inject these anchors (RoPE as Weak Condition), and the overall framework with multi-modal conditions e.g., text and audio*



### 3.1 内容锚点编码与注入

Gloria 的核心机制是将角色视频生成建模为“从外向内看”的场景，通过一组紧凑的结构化锚点帧（content anchors）提供持久的视觉参考。锚点帧分为三类：

- **全局锚点 $C_g$**：从源视频中选取一帧，捕获角色的整体场景、外观和背景信息，提供长时一致性基础。
- **视角锚点 $C_v$**：从全源视频中采样不同朝向的帧（如正面、侧面、背面），表征角色的多视角外观。
- **表情锚点 $C_e$**：选取不同表情的帧（如中性、微笑、惊讶），提供表情身份参考。

锚点帧经 3D VAE 编码后，补丁化（patchify）并与目标视频的噪声潜在表示在序列维度拼接，统一送入 DiT 骨干网络进行全注意力计算。这一设计使锚点信息直接参与自注意力，而非通过额外的交叉注意力分支注入，从而在生成全程提供稳定的全局参考。

### 3.2 超集内容锚定（Superset Content Anchoring）

传统方法在训练时仅从当前训练片段内采样锚点，导致模型学会“复制粘贴”锚点内容，而非建立语义对应。Gloria 提出超集内容锚定策略：将锚点选择范围扩展至全源视频，允许采样片段外（extra-clip）的锚点帧。这些片段外锚点具有不同的视角、表情或姿态，迫使模型学习从锚点中提取相关外观信息并与当前片段建立对应关系，而非简单复制。消融实验（Table 4）表明，该策略是消除复制粘贴模式、提升长时一致性的关键。

### 3.3 RoPE 弱条件：多锚点消歧

当同时注入全局、视角和表情三类锚点时，模型需区分不同锚点的角色。Gloria 提出“RoPE 弱条件”（RoPE as Weak Condition），在 3D RoPE 位置编码中为不同锚点类型和子类别分配不同的时间偏移量：

$$ \text{RoPE}_i = \text{RoPE}(t + o_i + s_{o_j}, h_i, w_i) $$

其中 $t$ 为当前帧的时间索引，$o_i$ 为锚点类型偏移（全局、视角、表情各取不同值），$s_{o_j}$ 为子类别偏移（如视角锚点中的正面、侧面、背面）。这种隐式编码方式使模型在自注意力计算中能区分不同锚点的身份，避免多锚点间的注意力冲突。图 8 的消融显示，移除 RoPE 弱条件后多锚点冲突导致生成混乱，加入后模型能正确选择对应锚点内容。

### 3.4 流匹配训练目标

视频生成过程采用流匹配（flow matching）框架，训练目标为：

$$ \mathcal{L} = \mathbb{E}_{x_0, x_1, c, t} \left\| u(x_t, c, t; \theta) - v_t \right\|^2 $$

其中 $x_0$ 为噪声，$x_1$ 为目标视频帧，$v_t = x_1 - x_0$ 为真实速度场，$c$ 为条件信息（文本、图像、音频及内容锚点），$u(\cdot; \theta)$ 为模型预测的速度场。

### 3.5 分块自回归推理

长视频生成采用分块自回归策略：视频被划分为重叠的块（chunk），每块生成时以前一块最后 4 帧作为前缀 token 初始化去噪过程。相邻块之间通过线性混合权重进行过渡，权重为 $w = [1, 0.67, 0.33, 0]$，对前一块最后 $n$ 帧与后一块前 $n$ 帧执行 $w \cdot x_1 + (1-w) \cdot x_2$ 的加权融合。该机制保证块间过渡平滑，支持超过 10 分钟的连续视频生成。

### 补充图表

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline to construct training clips and charactercentric anchor frames, e.g., global, viewpoint, and expression. The blue arrow marks the subject’s forward orientation, whereas the green arrow marks the camera-facing direction*

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/012_Figure_8.jpg]]
*Figure 8: The left includes the first frame, viewpoint anchor frames and the text prompt. The right side shows generated videos, the bottom row indicates using “RoPE as Weak Condition” (RWC) while the top row dose not employ it*

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/009_Figure_7.jpg]]
*Figure 7: (a) Ablation of the global anchor*



## 实验与关键发现

### 评估体系与基准构建

Gloria 围绕角色视频生成的三个核心维度——长时一致性、多视角外观一致性与表情身份一致性——构建了多层次的评估体系。论文自建了三个专用测试集：（1）长时一致性测试集，包含 20 个 5–10 分钟的片段；（2）多视角外观与表情身份测试集，覆盖 50 个角色、40 组设定；（3）基础能力测试集，包含 95 个案例。此外，还在公开数据集 CelebV-HQ（100 个案例）上与以人物为中心的方法进行了对比。

### 长时一致性：锚点驱动的持久化参考

长时一致性是视频生成的核心瓶颈之一。随着生成时长增加，传统方法容易发生外观漂移和背景退化。Gloria 通过全局锚点 $C_g$ 提供贯穿全序列的稳定视觉参考，有效抑制了这一问题。

**定量结果（Table 1）**：在长时一致性测试集上，Gloria 取得了 Subject Consistency 0.960、Background Consistency 0.951、Arcface 0.787 的成绩，显著优于所有对比方法。表 1 的具体对比数值需查阅原文，但 verified analysis 确认 Gloria 在所有三项指标上均达到最优。

**关键机制**：注意力可视化分析（Figure 9）揭示了锚点的工作方式——模型在生成的不同分块（每个 5 秒）中持续关注全局锚点帧，注意力分数在长序列中保持稳定，这解释了为何背景和主体身份不会随时间退化。消融实验（Figure 7a）提供了反向证据：移除全局锚点后，背景在生成过程中迅速劣化。

### 多视角外观与表情身份一致性

多视角外观一致性和表情身份一致性是角色视频生成中更具挑战性的维度——模型不仅需要记住角色长相，还需在不同视角和表情下保持身份不变。

**定量结果（Table 2）**：Gloria 在 DINO-I 上达到 0.821，CLIP-I 达到 0.858，Exp. 达到 0.717，大幅领先多参考方法（如 Humo、Phantom 等）。这表明内容锚点比简单的多参考图像注入更能保持身份一致性。

**用户调研验证（Figure 4）**：在表情身份一致性和多视角外观的主观评估中，Gloria 同样获得最高偏好率。Figure 12 提供了更细粒度的主题评估分解。

**注意力机制的证据（Figure 10）**：当文本提示要求角色转身时，模型对后视角锚点的注意力分数显著上升；而当文本未指示旋转时，注意力分数保持平稳低位。这直接验证了视角锚点 $C_v$ 被模型有效利用，而非被忽略或产生冲突。

### 基础能力评估

除一致性指标外，Gloria 在基础生成质量上也表现全面。在基础能力测试集上（Table 3），Gloria 取得 IQA 4.65、AES 3.63、Sync-C 5.12、Sync-D 8.83 的成绩，全面领先对比方法。用户调研（Figure 6）进一步确认了主观偏好的一致性。

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/008_Table_3.jpg]]
*Table 3: Quantitative comparison of fundamental capability*

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/007_Figure_6.jpg]]
*Figure 6: The user study results of fundamental capability*

在 CelebV-HQ 数据集上（Table 7），Gloria 的 FID 为 25.50、FVD 为 90.86，优于 **FantasyTalking**、**HunyuanAvatar** 和 **InfiniteTalk**（Yang et al., 2025）等以人物为中心的方法，证明了内容锚点框架在通用人物视频生成任务上的竞争力。

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/019_Table_7.jpg]]
*Table 7: Quantitative comparison results on CelebV-HQ with the human-centric methods. Fantasy. denotes FantasyTalking, Huny.A. is HunyuanAvatar and Infinite. indicates InfiniteTalk*

### 消融实验：锚点类型与训练策略的因果分析

消融实验（Table 4）系统拆解了各组件的作用：

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/010_Table_4.jpg]]
*Table 4: Quantitative ablation results of content anchors*

- **仅使用全局锚点 + 超集内容锚定（w/ $C_g$, SCA）**：在长时一致性指标上表现最佳，说明全局锚点是持久化外观的核心。
- **加入视角锚点 $C_v$ 和表情锚点 $C_e$**：多视角外观一致性（DINO-I、CLIP-I）和表情一致性（Exp.）显著提升，验证了这两类锚点的独立贡献。
- **移除超集内容锚定（SCA）**：模型出现复制粘贴模式（copy-paste pattern），即直接复制锚点帧内容而非建立语义对应关系。SCA 通过从全源视频采样片段外锚点，迫使模型学习关联而非复制。
- **移除 RoPE 弱条件（RWC）**：多锚点之间产生冲突，生成结果混乱（Figure 8）。RWC 为每种锚点类型和子类别分配不同的时间偏移 $o_i + so_j$（见公式 $RoPE_i = RoPE(t + o_i + so_j, h_i, w_i)$），隐式编码锚点身份，使模型能够区分并正确选择对应锚点的内容。

### 数据分布与公平性

Table 5 和 Table 6 分别展示了视角锚点和表情锚点的类别分布。数据分布存在不均衡（如某些视角类别样本较少），模型在少数类别上的表现可能欠佳。表情锚点提取的准确率为 82%（使用 EmotiEffLib + Gemini judge 精炼），意味着约 18% 的训练数据可能包含噪声标签，这是潜在的性能瓶颈。论文未进行专项的公平性评估，少数群体和极端视角下的表现需要进一步验证。

### 失败模式与局限性

1. **多角色场景不支持**：内容锚点框架当前仅适用于单角色场景，无法处理角色间交互。
2. **表情锚点噪声**：82% 的提取准确率意味着训练信号存在噪声，在非典型表情上可能导致身份漂移。
3. **极端视角退化**：受限于训练数据分布，在极端或罕见视角下生成质量可能下降。
4. **推理成本**：分块自回归推理虽支持长视频生成，但计算和时间成本较高。模型训练需 512 块 A800 GPU，复现门槛高。
5. **领域泛化未验证**：在非人类角色（卡通形象、动物等）上的表现尚未探索。

### 补充图表

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison of ap*

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/013_Figure_10.jpg]]
*Figure 10: Left: the first frame and a back-view anchor frame. Right: the generated results and the corresponding attention score curve of the generated sequence toward the back-view anchor. The upper and lower rows show results generated under different texts*

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/011_Figure_9.jpg]]
*Figure 9: Self-attention maps of the generated sequence and its attention toward the global anchor across different chunks (each lasting 5s). The rightmost dashed column indicates the attention score from the generated sequence to the global anchor frame*

![[assets/figures/papers/paper_list_l990_https_arxiv_org_abs_2603_29931/figures/004_Figure_4.jpg]]
*Figure 4: The user study results of expressive ID and multi-view appearance consistency*



## 定位与知识库关联

### 1. 从“单帧参考”到“结构化锚点”：角色一致性生成的范式迁移

Gloria 的核心贡献在于将角色视频生成的一致性控制，从依赖单一参考图像或文本提示的隐式约束，升级为基于一组结构化“内容锚点”的显式、持久化参考框架。这一转变解决了此前方法的根本瓶颈：缺乏紧凑的、覆盖多视角与多表情的持久外观和身份参考，导致长序列生成中角色外观漂移、视角变化时身份丢失。

与现有主流方法相比，Gloria 的差异化定位清晰：
- **相对于单参考方法**（如 **Wan-I2V**、**Kling**、**Vidu-Q2** 等商业模型及 **FantasyTalking**、**Omnihuman1.5** 等学术模型）：这些方法通常仅接受单张图像或文本作为外观条件，在生成长视频时缺乏对角色背面、侧脸等未见视角的显式引导，导致一致性随时间衰减。Gloria 通过全局锚点、视角锚点和表情锚点三类帧，为模型提供了“从外向内看”的完整外观参照系。
- **相对于多参考方法**（如 **Humo**、**Phantom**、**HunyuanCustom**）：这些方法虽然支持多张参考图像，但未对不同参考帧的角色（全局身份、特定视角、特定表情）进行结构化区分，导致多锚点信息在注意力机制中产生冲突。Gloria 通过“RoPE 弱条件”机制，为每类锚点及其子类别分配不同的时间偏移，隐式编码锚点身份，使模型能够根据生成需求选择性关注对应锚点。
- **相对于长时一致性方法**（如 **InfiniteTalk** (Yang et al., 2025)、**HunyuanAvatar**、**WanS2V**）：这些方法或依赖时序自回归扩展，或采用隐式身份嵌入，但缺乏显式的全局场景参考，导致背景和角色外观在长序列中逐渐退化。Gloria 的全局锚点提供了跨越所有生成分块（chunk）的稳定场景级参考，实验表明移除全局锚点会导致背景快速退化（Figure 7a）。

### 2. 关键技术机制的知识贡献

Gloria 提出的两项核心机制——**超集内容锚定** 和 **RoPE 弱条件**——分别解决了内容锚点框架中的两个关键挑战，其设计思路对后续研究具有启发性：

**超集内容锚定** 解决了“复制粘贴”模式问题。当模型仅从训练片段内采样锚点时，倾向于直接复制锚点帧内容而非学习外观关联。通过将锚点选择范围扩展到全源视频，引入片段外锚点（具有不同视角、表情或姿态），强制模型学习跨帧的外观对应关系而非简单复制。这一策略的消融实验（Table 4）证实：仅使用全局锚点配合超集内容锚定，即可在长时一致性指标上达到最优；加入视角和表情锚点后，多视角外观和表情一致性进一步提升。

**RoPE 弱条件** 解决了多锚点冲突问题。当同时注入全局、视角、表情三类锚点时，模型的自注意力机制难以区分各锚点的不同用途。Gloria 在 3D RoPE 的时间维度上为不同类型锚点分配不同的固定偏移量 $o_i$，并为同类锚点内的不同子类别（如正面、背面、左侧面等视角）分配子偏移量 $so_j$：

$$\text{RoPE}_i = \text{RoPE}(t + o_i + so_j, h_i, w_i)$$

这一设计的精妙之处在于：它不强制模型必须使用某个锚点（弱条件），而是通过位置编码的差异让模型“感知”到不同锚点的身份差异，从而在生成过程中自主选择关注正确的锚点。消融实验（Figure 8）直观展示了这一机制的效果：无 RoPE 弱条件时，多锚点冲突导致生成混乱；加入后，模型能正确选择对应锚点的内容。

### 3. 适用边界与局限

Gloria 的设计假设和实验设置定义了其当前适用边界，这些边界同时指向了方法的局限和未来改进方向：

**角色范围限制**：方法明确限定于单角色场景，不支持多角色交互。内容锚点的构建流程（人体检测、视角估计、表情识别）均针对人类角色设计，其在非人类角色（卡通形象、动物、虚构生物）上的泛化性尚未验证。

**数据流水线依赖**：内容锚点的质量高度依赖前端数据流水线的精度。视角锚点提取准确率为 98%，但表情锚点提取准确率仅为 82%（EmotiEffLib 单独使用时仅 66%，结合 Gemini judge 后提升至 82%）。这意味着约 18% 的表情锚点可能包含噪声标签，在极端表情或非典型面部特征上可能进一步退化。

**计算与推理成本**：推理采用分块自回归方式，长视频生成的计算和时间成本较高。训练需要大规模 GPU 资源（512 A800），限制了方法的可复现性和社区推广。模型规模与数据规模的 scaling 实验（Table 8）显示性能随资源增加而提升，但未给出效率优化的具体方案。

**分布偏差**：训练数据中视角和表情类别的分布不均衡（Table 5、6），模型在少数类别（如极端俯仰角、罕见表情）上的表现可能欠佳。这一公平性问题未在论文中进行专项评估。

### 4. 开放问题与后续方向

基于 Gloria 的当前设计，以下开放问题值得后续研究关注：

1. **多角色扩展**：如何将内容锚点框架扩展到多角色场景？可能的思路包括为每个角色维护独立的锚点集，但需要解决角色间遮挡、交互时的锚点冲突和注意力分配问题。

2. **跨域泛化**：内容锚点框架能否泛化到非人类角色？这需要重新设计锚点提取流水线（如动物姿态估计、卡通角色关键点检测），并验证超集内容锚定和 RoPE 弱条件在不同视觉域的有效性。

3. **自适应锚点选择**：当前锚点依赖人工指定或固定规则选择。能否通过自适应机制（如基于文本提示的锚点检索、在线锚点优化）减少人工输入，提升方法的自动化程度？

4. **效率优化**：如何通过模型蒸馏、锚点压缩、推理调度优化等手段降低模型规模和推理延迟，使方法适用于实时或近实时应用场景？

5. **表情锚点精度提升**：82% 的表情锚点提取准确率仍有提升空间。更强的多模态大模型（MLLM）精炼策略，或端到端学习锚点选择，可能是改进方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Gloria_Consistent_Character_Video_Generation_via_Content_Anchors.pdf]]
