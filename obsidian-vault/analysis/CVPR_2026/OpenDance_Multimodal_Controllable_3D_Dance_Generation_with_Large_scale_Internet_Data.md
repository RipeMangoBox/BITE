---
title: "OpenDance: Multimodal Controllable 3D Dance Generation with Large-scale Internet Data"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OpenDance_Multimodal_Controllable_3D_Dance_Generation_with_Large_scale_Internet_Data.pdf
project_link: "https://open-dance.github.io"
code_link: null
aliases:
- OpenDance
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过构建大规模多模态数据集（OpenDanceSet）并在其上设计一个解耦条件与掩码联合预测的统一框架（OpenDanceNet），实现从“仅音乐”到“音乐+任意组合控制信号”的生成跨越。
primary_logic: 将风格信号（音乐、文本）与空间信号（2D关键点、轨迹）解耦编码，并通过多模态掩码联合预测范式强制模型学习精细的帧级约束，从而在一次生成中同时满足高保真、多样性与灵活控制。
claims:
- OpenDanceSet 提供100.26小时、14种流派、5种同步模态（3D运动、音乐、2D关键点、轨迹、文本）的丰富标注，解决了多模态舞蹈数据稀缺。
- Disentangled Dance Tokenizer (DDT) 避免早期跨模态融合，允许稀疏的帧级约束（如部分关键点或轨迹）直接填充并编码为独立令牌，实现精确的空间控制。
- Multimodal-Condition Transformer (MCT) 不仅生成运动令牌，还同时预测被掩码的轨迹和2D关键点令牌，使空间监督成为内在生成目标而非附加条件。
- AIST++ 上 FID_k ↓ = 24.82
---

# OpenDance: Multimodal Controllable 3D Dance Generation with Large-scale Internet Data

> [!tip] 核心洞察
> 将风格信号（音乐、文本）与空间信号（2D关键点、轨迹）解耦编码，并通过多模态掩码联合预测范式强制模型学习精细的帧级约束，从而在一次生成中同时满足高保真、多样性与灵活控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | OpenDance：基于大规模互联网数据的多模态可控3D舞蹈生成 |
| 英文题名 | OpenDance: Multimodal Controllable 3D Dance Generation with Large-scale Internet Data |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.07565) · [Project](https://open-dance.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | OpenDanceNet |
| Dataset | AIST++, OpenDanceSet |

> [!tip] 效果简介
> - AIST++ 上，FID_k ↓ 24.82 vs - (best among compared methods) (-)；BAS ↑ 0.2513 vs - (highest) (-)。
> - OpenDanceSet 上，FID_k ↓ 23.19 vs - (best) (-)；BAS ↑ 0.2472 vs - (highest) (-)。

## 概要

3D舞蹈生成长期受困于两个根本瓶颈：① 大规模、丰富标注的多模态舞蹈数据缺失，使灵活条件生成不可行；② 缺少能够处理任意组合多样性条件（音乐、文本、关键点、轨迹）的统一生成框架，导致可控性差。现有方法（如 **Bailando** (Siyao et al., CVPR 2022)、**EDGE** (Tseng et al., arXiv 2022)、**TM2D** (Gong et al., ICCV 2023)）大多仅支持音乐条件，无法在单一模型中同时响应多种空间与风格控制信号。

本文提出 **OpenDance**，核心贡献包括：
- **OpenDanceSet**：一个大规模多模态3D舞蹈数据集，包含100.26小时、14种流派、5种同步模态（3D运动、音乐、2D关键点、轨迹、文本），通过半自动标注流水线结合预训练估计器、LLM、人工标注员与专业艺术家构建。
- **OpenDanceNet**：一个统一的掩码建模框架，将风格信号（音乐、文本）与空间信号（2D关键点、轨迹）解耦编码，并通过多模态掩码联合预测范式强制模型学习精细的帧级约束，实现“Music+X”任意组合条件下的可控生成。

核心因果机制在于：**Disentangled Dance Tokenizer (DDT)** 避免早期跨模态融合，允许稀疏帧级约束直接编码为独立令牌；**Multimodal-Condition Transformer (MCT)** 不仅生成运动令牌，还同时预测被掩码的轨迹和关键点令牌，使空间监督成为内在生成目标。随机模态级掩码进一步防止模型过度依赖单一模态，强制学习细粒度空间约束。

实验表明，OpenDanceNet 在 AIST++ 和 OpenDanceSet 上均取得领先的生成质量与可控性。消融实验确认，联合预测机制、多条件训练以及各项辅助损失（$\mathcal{L}_{\mathrm{traj}}$、$\mathcal{L}_{\mathrm{kpts}}$、$\mathcal{L}_{\mathrm{fk}}$、$\mathcal{L}_{\mathrm{con}}$）对空间对齐和物理合理性都不可或缺。当前方法尚未包含手指与面部表情，文本描述也尚不支持细粒度视觉-语言编辑，这些构成了未来的改进方向。

3D 舞蹈生成旨在从音乐或其他控制信号中自动合成逼真、多样且与输入高度对齐的人体运动序列。这项任务在虚拟人动画、游戏、影视和社交媒体内容创作中具有广泛的应用前景。然而，现有方法长期受制于两个根本性瓶颈，使得灵活、高保真的可控舞蹈生成难以实现。

**瓶颈一：大规模、丰富标注的多模态舞蹈数据缺失。** 舞蹈生成的质量和可控性高度依赖训练数据的规模与标注丰富度。现有数据集普遍存在规模小、主体少、流派单一、标注模态有限等问题（见 Table 1）。例如，广泛使用的 **AIST++** 虽然提供了高质量的音乐-舞蹈对，但其时长和流派覆盖远不足以支撑对多样化控制信号（如文本描述、空间轨迹、2D 关键点）的联合建模。这直接导致现有方法大多只能以音乐作为单一条件输入，无法实现灵活的多模态控制。

**瓶颈二：缺少能够处理任意组合多样性条件的统一生成框架。** 即便获得了多模态数据，如何在一个框架内有效融合异质条件信号仍是一大挑战。现有方法可大致归为两类：一类以 **Bailando** (Siyao et al., CVPR 2022) 为代表，采用 VQ-VAE 加自回归 Transformer 的范式，但仅支持音乐条件；另一类如 **EDGE** (Tseng et al., arXiv 2022) 和 **MotionMix** (Hoang et al., 2024) 基于扩散模型，虽具备一定的可编辑性，但在处理稀疏帧级空间约束（如部分关键点或轨迹）时，往往因早期跨模态融合而导致精细控制信号被粗粒度的风格信号淹没。此外，**TM2D** (Gong et al., ICCV 2023) 虽尝试了音乐+文本的双模态生成，但其架构并非为音乐、文本、关键点、轨迹的任意组合而设计，扩展性有限。

上述瓶颈的本质在于：**风格信号（音乐、文本）与空间信号（2D 关键点、轨迹）在信息粒度、时间密度和语义层级上存在根本差异**，将它们不加区分地送入统一的编码器或条件机制，必然导致模型倾向于依赖易于学习的粗粒度风格信号，而忽略对精细空间约束的建模。这意味着，要真正实现“音乐 + 任意控制信号”的可控生成，必须在数据层面提供足够丰富、同步的多模态标注，并在模型层面设计能够解耦编码、强制对齐的生成范式。

本文正是在这一背景下提出 **OpenDance**，其核心动机可概括为两点：
1. **构建 OpenDanceSet**——一个包含 100.26 小时、14 种舞蹈流派、5 种同步模态（3D 运动、音乐、2D 关键点、轨迹、文本）的大规模多模态数据集，从根本上缓解数据稀缺问题。
2. **设计 OpenDanceNet**——一个基于掩码建模的统一框架，通过解耦舞蹈分词器（DDT）和多模态条件 Transformer（MCT）的联合预测机制，将空间信号从风格信号中解耦，并以掩码联合预测作为内在生成目标，从而在一次生成中同时满足高保真、多样性与灵活控制的需求。

## 核心方法与创新机理

OpenDance 的核心创新在于**从“仅音乐驱动”到“音乐+任意组合控制信号”的生成范式跨越**，其实现依赖两条相互咬合的技术路线：① 构建首个大规模、多模态标注的 3D 舞蹈数据集 OpenDanceSet，为灵活条件生成提供数据底座；② 设计解耦条件与掩码联合预测的统一框架 OpenDanceNet，使风格信号（音乐、文本）与空间信号（2D 关键点、轨迹）在同一生成过程中被精细地共同建模。

### 关键 changed slots 分析

相较于现有基线方法，OpenDanceNet 在四个核心维度上实现了系统性改变：

**1. 条件输入：从单一音乐到 Music+X 的任意组合**

现有舞蹈生成方法几乎全部围绕音乐条件展开：**Bailando**（Siyao et al., CVPR 2022）以 VQ-VAE + GPT 架构实现音乐到舞蹈的生成；**EDGE**（Tseng et al., arXiv 2022）引入扩散模型支持可编辑生成，但条件空间仍限于音乐；**TM2D**（Gong et al., ICCV 2023）虽扩展至音乐+文本双模态，却无法处理关键点或轨迹等精确空间约束。OpenDanceNet 首次将条件空间扩展至音乐、文本、2D 关键点、全局轨迹的任意组合，使“仅指定末帧关键点+轨迹”或“音乐+随机几何轨迹”等灵活控制成为可能（Figure 5）。这一改变的**因果机制**在于：数据层面，OpenDanceSet 提供了五种同步模态的丰富标注（100.26 小时，14 种流派，Table 1）；模型层面，解耦编码与联合预测的设计使不同模态的条件信号能够被独立处理并在生成中协同作用。

**2. 运动令牌化：从共享编码到解耦离散令牌**

传统方法如 **AI Choreographer**（Li et al., ICCV 2021）和 **MoMask**（Guo et al., CVPR 2024）采用单一编码器直接处理运动或条件信号，导致不同模态的特征在早期即发生纠缠。OpenDanceNet 的 **Disentangled Dance Tokenizer (DDT)** 将关节旋转、2D 关键点、全局轨迹分别送入独立编码器，并通过三个专属码本 $C_i = \{ c_n \}_{n=1}^{N}$ 量化为离散令牌，输出统一表示 $\hat{z} \in \mathbb{R}^{3 \times T' \times d}$。这一设计的**关键优势**在于：避免早期跨模态融合，使稀疏的帧级约束（如仅提供末帧关键点或部分轨迹）能够被直接填充并编码为独立令牌，而不受其他模态的干扰（Section 4.1）。这从根本上解决了“空间精细条件被粗粒度风格信号淹没”的问题。

**3. 训练目标：从仅预测运动到掩码联合预测**

现有掩码建模方法（如 **MMM**，Pinyoanuntapong et al., CVPR 2024）仅以运动令牌为预测目标，空间信号仅作为附加条件输入。OpenDanceNet 的 **Multimodal-Condition Transformer (MCT)** 则被训练为同时预测被掩码的运动令牌、2D 关键点令牌和轨迹令牌，使空间监督成为**内在生成目标**而非外部条件（Section 4.2）。训练时，对音乐/文本按概率 $p_{\text{mask}}$ 进行模态级掩码，对轨迹/关键点进行令牌级掩码，构造掩码输入序列 $Z_{\text{mask}}$，并在掩码位置集合 $\mathcal{M}$ 上计算所有模态的交叉熵损失 $\mathcal{L}_{\text{CE}}^{\text{mask}} = - \mathbb{E}_{Z} \sum_{i \in \mathcal{M}} \log p_{\theta}(z_i \mid Z_{\text{mask}})$。消融实验（Table 5）证实：联合预测运动+轨迹+2D 关键点相较于仅预测运动，FIDk 从更高水平降至 47.18，FIDg 降至 21.34，空间可控性显著提升。

**4. 多模态学习平衡：随机模态级掩码防止条件坍塌**

当所有条件被同等对待时，模型倾向于依赖易学习的粗粒度风格信号（音乐、文本），而忽略挑战性的帧级空间约束。OpenDanceNet 通过**随机模态级掩码**机制（训练时以概率 $p_{\text{mask}}$ 随机丢弃音乐或文本模态）强制模型学习所有条件信号。多条件训练（Music+Traj+Kpts+Text）对比单条件训练的实验（Table 6）表明，该策略产生了更丰富的多样性和更优的生成质量（FIDk 48.46, FIDg 21.79）。此外，四个辅助损失项——轨迹损失 $\mathcal{L}_{\text{traj}}$、关键点损失 $\mathcal{L}_{\text{kpts}}$、前向运动学损失 $\mathcal{L}_{\text{fk}}$ 和接触一致性损失 $\mathcal{L}_{\text{con}}$——共同作用使 FIDk 降至 46.92，FIDg 降至 20.38（Table 7），证明各损失项对对齐和物理合理性都不可或缺。

### 推理阶段的迭代精炼创新

除训练阶段的创新外，OpenDanceNet 在推理时引入 **Multi-Step Logit-Ranked Re-Masking (MS-LRM)** 与脚步优化机制：通过 $N$ 步迭代重掩码低置信度令牌，并基于足滑损失梯度更新运动嵌入 $\hat{\mathbf{e}}_{\text{motion}} = \mathbf{e}_{\text{motion}} - \alpha \nabla_{\mathbf{e}_{\text{motion}}} \mathcal{L}_{\text{fs}}$，有效抑制 foot-skating 伪影（Section 4.4）。这一推理策略与训练时的联合预测目标形成闭环，使生成结果在物理合理性上进一步逼近真实舞蹈。

### 创新边界与局限

需要指出，当前创新集中在躯干与下肢的舞蹈控制，**尚未纳入详细的手指关节和面部表情**，因此精细手势与表情控制仍是空白。此外，文本描述依赖 LLM 生成和人工标注，尚不支持具备编辑能力的细粒度视觉-语言结构，这限制了文本控制的精确度。

OpenDanceNet 是一个基于掩码建模的统一舞蹈生成框架，其核心设计理念是**先解耦、后统一**：将风格信号（音乐、文本）与空间信号（2D 关键点、全局轨迹）分离编码，再通过多模态掩码联合预测范式将它们整合为一致的生成目标。这一设计直接回应了现有方法的两个根本瓶颈——多模态数据的缺失和灵活可控性的不足。

### 框架总览

整个 pipeline 由四个关键模块串联而成，形成“数据准备 → 令牌化 → 联合预测 → 迭代精炼”的完整链路：

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **Data Collection & Annotation Pipeline** | 半自动流水线从互联网视频中提取并标注多模态舞蹈数据 | 600+ 小时 RGB 舞蹈视频 | OpenDanceSet（100.26 小时，14 种流派，5 种同步模态） |
| **Disentangled Dance Tokenizer (DDT)** | 将关节旋转、2D 关键点、全局轨迹分别量化为离散令牌 | 运动序列 $\{J, K, X\}$ | 三类独立离散令牌 $\hat{z} \in \mathbb{R}^{3 \times T' \times d}$ |
| **Multimodal-Condition Transformer (MCT)** | 接收音乐/文本令牌作为风格条件，轨迹/关键点令牌作为空间条件，联合预测所有被掩码的令牌 | 掩码后的多模态令牌序列 $Z_{\text{mask}}$ | 重建的运动、轨迹、关键点令牌 |
| **Multi-Step Logit-Ranked Re-Masking (MS-LRM) + Footstep Optimization** | 推理时迭代重掩码低置信度令牌，并基于足滑损失梯度优化运动嵌入 | MCT 初始生成结果 | 精炼后的高质量舞蹈序列 |

### 模块间的输入输出流

框架的数据流遵循严格的解耦-统一逻辑：

1. **数据准备阶段**：原始视频经过预训练 3D 姿态估计器（world-grounded motion estimator）提取 SMPL 参数，获得局部关节旋转序列 $\{\pmb{\theta}_t\}_{t=1}^{T}$、全局平移序列 $\{\phi_t\}_{t=1}^{T}$、3D 关节位置 $\mathbf{X} \in \mathbb{R}^{J \times 3}$ 和网格顶点 $\mathbf{V} \in \mathbb{R}^{6890 \times 3}$。同时，通过 LLM 和人工标注生成流派文本描述，通过投影和估计器获取 2D 关键点与全局轨迹。后处理阶段使用卡尔曼滤波和 PFC 分数优化足部接触，并过滤低质量样本。

2. **令牌化阶段**：DDT 接收三类空间信号——关节旋转 $J \in \mathbb{R}^{T \times D_j}$、2D 关键点 $K \in \mathbb{R}^{T \times D_k}$、全局轨迹 $X \in \mathbb{R}^{T \times D_x}$——分别通过独立编码器映射为潜在特征 $z_i \in \mathbb{R}^{T' \times d}$，再经各自专属码本 $C_i = \{c_n\}_{n=1}^{N}$ 量化为离散令牌。**关键设计**：DDT 避免早期跨模态融合，使得稀疏的帧级约束（如仅给定末帧关键点或部分轨迹）可直接填充并编码为令牌，这是实现精确空间控制的基础。

3. **联合预测阶段**：MCT 将所有模态令牌拼接为统一序列 $Z = [Z_{\text{music}}, Z_{\text{text}}, Z_{\text{traj}}, Z_{\text{kpts}}]$。训练时，对音乐/文本施加概率 $p_{\text{mask}}$ 的模态级掩码，对轨迹/关键点施加令牌级掩码，构造 $Z_{\text{mask}}$。MCT 不仅预测被掩码的运动令牌，还**同时预测被掩码的 2D 关键点和全局轨迹令牌**，使空间监督成为内在生成目标而非附加条件。这一“掩码联合预测”机制强制模型学习精细的帧级空间约束，防止风格信号淹没稀疏的空间条件。

4. **推理精炼阶段**：MS-LRM 在 $N$ 步迭代中，每步根据预测置信度重新掩码低置信度令牌并重新生成。最后一步引入足滑损失 $\mathcal{L}_{\text{fs}}$ 的梯度，对运动嵌入进行一步精细调整：$\hat{\mathbf{e}}_{\text{motion}} = \mathbf{e}_{\text{motion}} - \alpha \nabla_{\mathbf{e}_{\text{motion}}} \mathcal{L}_{\text{fs}}$，有效抑制 foot-skating 伪影。

### 与基线方法的架构差异

相较于现有方法，OpenDanceNet 在三个关键维度上做出了结构性改变：

- **条件输入**：从“仅音乐”（**Bailando** (Siyao et al., CVPR 2022)、**EDGE** (Tseng et al., arXiv 2022) 等）扩展为“音乐 + 文本、2D 关键点、轨迹的任意组合”，实现真正的多模态可控生成。

- **运动令牌化**：从单一共享编码器直接处理运动/条件，转变为 DDT 的三分支解耦量化，使每类空间信号拥有独立的离散表示空间。

- **训练目标**：从仅预测运动令牌（自回归或扩散），转变为掩码联合预测——同时预测运动、2D 关键点、轨迹令牌，并通过辅助损失（$\mathcal{L}_{\text{traj}}$、$\mathcal{L}_{\text{kpts}}$、$\mathcal{L}_{\text{fk}}$、$\mathcal{L}_{\text{con}}$）强制对齐。随机模态级掩码策略进一步防止模型过度依赖某一模态，确保所有条件信号都被有效利用。

![[assets/figures/papers/paper_list_l954_https_arxiv_org_abs_2506_07565/figures/005_Figure_4.jpg]]
*Figure 4: Overview of OpenDanceNet, a masked-modeling-based dance generation framework. (a) We first train a Disentangled Dance Tokenizer (DDT) to quantize spatial signals (joint rotations, global trajectories, and 2D keypoints) into discrete tokens. (b) Then the Multimodal-Condition Transformer (MCT) is trained by randomly sampling subsets of control modalities and applying token-level masks over trajectories, 2D keypoints, and motion tokens, enabling the model to handle diverse condition combinations while generating coherent dance motions. (c) At inference time, OpenDanceNet supports arbitrary configurations of input conditions for flexible multimodal control, while Multi-Step Logit-Ranked Re-Mask...*

OpenDanceNet 的核心架构由三个紧密协作的模块构成：**解耦舞蹈分词器（DDT）**、**多模态条件 Transformer（MCT）** 以及推理阶段的 **多步对数排序重掩码与脚步优化（MS-LRM + Footstep Optimization）**。其设计哲学是“先解耦，后统一预测”——先将风格信号（音乐、文本）与空间信号（2D关键点、轨迹）分别编码为独立令牌，再通过掩码联合预测范式强制模型学习帧级约束。

### 4.1 解耦舞蹈分词器（DDT）

DDT 的设计目标是避免早期跨模态融合，使稀疏的帧级约束（如仅提供某一帧的关键点或部分轨迹）能够直接填充并编码为独立令牌。输入的运动序列被分解为三个模态：

- **关节旋转**：$J \in \mathbb{R}^{T \times D_j}$，表示长度为 $T$ 的局部关节旋转参数序列。
- **2D 关键点**：$K \in \mathbb{R}^{T \times D_k}$，为投影后的 2D 身体关键点坐标。
- **全局轨迹**：$X \in \mathbb{R}^{T \times D_x}$，描述人物在世界坐标系中的根位移。

每个模态通过专属编码器映射为潜在特征 $z_i \in \mathbb{R}^{T' \times d}$，随后经由各自的可学习码本 $C_i = \{ c_n \}_{n=1}^{N}$ 量化为离散令牌。三个模态的离散令牌堆叠形成统一表示 $\hat{z} \in \mathbb{R}^{3 \times T' \times d}$。这种解耦设计的关键优势在于：当用户仅提供稀疏空间约束时，缺失帧可直接填充零值后送入对应分支，无需改变编码器结构。

### 4.2 多模态条件 Transformer（MCT）

MCT 的核心创新在于将空间信号的重构从“附加条件”提升为“内在生成目标”。其输入序列由四类令牌拼接而成：

$$Z = [ Z_{\mathrm{music}}, Z_{\mathrm{text}}, Z_{\mathrm{traj}}, Z_{\mathrm{kpts}} ]$$

训练时构造掩码输入序列：

$$Z_{\mathrm{mask}} = [ (Z_{\mathrm{music}})_{p_{\mathrm{mask}}}, (Z_{\mathrm{text}})_{p_{\mathrm{mask}}}, \mathrm{Mask}(Z_{\mathrm{traj}}), \mathrm{Mask}(Z_{\mathrm{kpts}}) ]$$

其中音乐和文本采用**随机模态级掩码**（以概率 $p_{\mathrm{mask}}$ 整条置零），而轨迹和关键点采用**令牌级掩码**。这种不对称掩码策略迫使模型无法过度依赖某一模态，必须学习从风格信号推断空间结构，或从稀疏空间约束补全运动。

掩码预测的交叉熵损失为：

$$\mathcal{L}_{\mathrm{CE}}^{\mathrm{mask}} = - \mathbb{E}_{Z} \sum_{i \in \mathcal{M}} \log p_{\theta}(z_i \mid Z_{\mathrm{mask}})$$

其中 $\mathcal{M}$ 为所有被掩码位置的集合。这意味着 MCT 同时预测运动令牌、轨迹令牌和关键点令牌，使空间监督成为训练目标的有机组成部分，而非外部附加项。

### 4.3 辅助空间损失

仅靠交叉熵损失不足以保证生成运动的空间精度和物理合理性，因此引入四项辅助 L1 损失：

- **轨迹损失**：$\mathcal{L}_{\mathrm{traj}} = \lambda_{g} \| X - X_{\mathrm{pred}} \|_1$，约束全局位移的准确性。
- **关键点损失**：$\mathcal{L}_{\mathrm{kpts}} = \lambda_{\mathrm{kpts}} \| K - K_{\mathrm{pred}} \|_1$，对齐 2D 投影位置。
- **前向运动学损失**：$\mathcal{L}_{\mathrm{fk}} = \lambda_{\mathrm{fk}} \| F(J, X) - F(J_{\mathrm{pred}}, X_{\mathrm{pred}}) \|_1$，通过 FK 函数 $F(\cdot)$ 计算 3D 关节位置误差，确保运动学一致性。
- **接触一致性损失**：$\mathcal{L}_{\mathrm{con}} = \frac{\lambda_{\mathrm{con}}}{N} \sum_{i=1}^{N} \big\| ( F(J, X) - F(J_{\mathrm{pred}}, X_{\mathrm{pred}}) ) \cdot b^{i} \big\|_1$，仅在足部接触帧（由二值标签 $b^i$ 标记）上施加 FK 损失，强化着地时的物理合理性。

此外，**足滑损失** $\mathcal{L}_{\mathrm{fs}} = \lambda_{\mathrm{fs}} \| K - K_{\mathrm{pred}} \|_1$ 作用于足部接触标签，直接抑制 foot-skating 伪影。消融实验（Table 7）表明，所有辅助损失共同作用使 FIDk 降至 46.92，FIDg 降至 20.38，各损失项对对齐和物理合理性均不可或缺。

### 4.4 推理迭代精炼（MS-LRM + Footstep Optimization）

推理时采用 $N$ 步迭代掩码预测：每步根据预测置信度（logits）重掩码低置信度令牌，逐步精炼生成质量。在此基础上引入基于足滑损失梯度的两步优化：

- **对数动量更新**：$\hat{\mathbf{e}}_{\mathrm{logits}} = \mathbf{e}_{\mathrm{logits}} - \alpha \nabla_{\mathbf{e}_{\mathrm{logits}}} \mathcal{L}_{\mathrm{fs}}$，利用足滑损失梯度对运动令牌 logits 进行一步更新。
- **运动嵌入精细调整**：$\hat{\mathbf{e}}_{\mathrm{motion}} = \mathbf{e}_{\mathrm{motion}} - \alpha \nabla_{\mathbf{e}_{\mathrm{motion}}} \mathcal{L}_{\mathrm{fs}}$，在最后一步基于足滑损失梯度直接调整运动嵌入，进一步抑制滑步伪影。

这一推理策略将迭代掩码预测的全局一致性优势与梯度优化的局部物理约束相结合，在不增加训练成本的前提下显著提升了生成运动的物理合理性。

## 实验与关键发现

### 主实验结果

我们在两个数据集上对 OpenDanceNet 进行了定量评估：广泛使用的 **AIST++** 和本文构建的大规模多模态数据集 **OpenDanceSet**。评估指标涵盖运动质量（FID_k）、音乐对齐度（BAS）、物理合理性（PFC）以及轨迹/关键点控制精度（FID_g、FID_k）。

**在 AIST++ 上**（Table 2），OpenDanceNet 取得了最低的 PFC（物理接触分数），表明其生成的舞蹈动作具有最优的足部物理合理性。在运动质量上，FID_k 达到 24.82，优于所有对比方法；FID_g 为 12.54，具备竞争力。音乐对齐度 BAS 达到 0.2513，在所有方法中最高。这些结果表明，即使在训练数据规模远小于 OpenDanceSet 的 AIST++ 上，OpenDanceNet 仍能生成高质量、高音乐对齐度的舞蹈序列。

**在 OpenDanceSet 上**（Table 3），OpenDanceNet 的优势更为显著。FID_k 达到 23.19，FID_m 在优化后达到 7.72，均为最优。BAS 达到 0.2472，同样最高。这验证了 OpenDanceNet 在大规模多模态数据上的有效性，以及多条件联合训练对生成质量的提升作用。

**对比基线方法**，OpenDanceNet 在可控性上具有根本性优势。**Bailando**（Siyao et al., CVPR 2022）仅支持音乐条件生成，**EDGE**（Tseng et al., arXiv 2022）虽具备一定可编辑性但缺乏多模态空间控制，**TM2D**（Gong et al., ICCV 2023）支持音乐+文本双模态但无法处理关键点/轨迹约束。OpenDanceNet 首次实现了音乐与文本、2D 关键点、轨迹的任意组合控制，并在所有指标上保持领先或持平。

### 消融实验

为验证各设计选择的贡献，我们进行了系统的消融实验。

**控制信号类型的影响**（Table 4）。在仅音乐条件（Music Only）基础上，逐步加入轨迹（+Traj）和 2D 关键点（+Kpts）控制。在 OpenDanceSet 上，加入轨迹和关键点后 PFC 降至 0.181，FID 降至 48.03，FID_g 降至 11.99。空间信号的引入显著提升了生成质量和物理合理性，证明轨迹和关键点约束能有效引导模型生成更合理、更可控的舞蹈动作。

**联合预测机制**（Table 5）。对比仅预测运动令牌（Motion Only）与联合预测运动+轨迹+2D 关键点令牌（Joint Prediction）。联合预测使 FID_k 降至 47.18，FID_g 降至 21.34，空间可控性大幅提升。这验证了将空间信号重构作为内在生成目标（而非仅作为附加条件）的关键作用——模型被迫学习帧级的精细空间约束，而非仅依赖风格信号进行模糊生成。

**多条件训练**（Table 6）。对比单条件训练（仅音乐）与多条件训练（Music+Traj+Kpts+Text）。多条件训练产生更丰富的运动多样性和更优的生成质量：FID_k 为 48.46，FID_g 为 21.79。随机模态级掩码机制防止模型过度依赖单一模态（如仅依赖音乐），强制其学习利用所有可用条件信号，从而提升了可控性和多样性。

**辅助损失函数**（Table 7）。逐项消融 $L_{con}$（接触一致性）、$L_{fk}$（前向运动学）、$L_{traj}$（轨迹重构）、$L_{kpts}$（关键点重构）四项辅助损失。所有损失项共同作用使 FID_k 降至 46.92，FID_g 降至 20.38。其中 $L_{con}$ 对物理合理性贡献显著，$L_{fk}$ 对运动学一致性不可或缺，$L_{traj}$ 和 $L_{kpts}$ 则直接强化了空间控制精度。缺少任一项均会导致对应维度的性能退化。

### 失败模式与局限性分析

尽管 OpenDanceNet 在多模态可控舞蹈生成上取得了显著进展，仍存在以下局限：

1. **精细手势与表情缺失**：当前方法未包含详细的手指关节和面部表情参数，无法生成具有丰富手势和面部表现力的舞蹈动作。这限制了其在需要精细肢体语言的应用场景（如手语舞蹈、情感表达）中的适用性。

2. **数据集应用范围有限**：OpenDanceSet 目前仅在 3D 舞蹈生成任务上进行了基准测试，尚未推广至视频生成等其他生成任务。其多模态标注的潜力有待进一步挖掘。

3. **文本描述的粒度不足**：文本标注依赖 LLM 生成和人工后处理，尚不支持具备编辑能力的细粒度视觉-语言结构。这限制了通过文本对舞蹈风格、动作细节进行精确编辑的可能性。

### 重要图表结论

- **Table 1**：OpenDanceSet 在规模（100.26 小时）、流派数（14 种）、标注模态数（5 种同步模态）上全面超越先前 3D 舞蹈数据集，为多模态可控生成提供了数据基础。
- **Figure 3**：经后处理与过滤后，OpenDanceSet 的数据分布更接近高质量数据集 AIST++，物理性能指标显著改善，验证了数据清洗流水线的有效性。
- **Table 2 & Table 3**：OpenDanceNet 在两个数据集上均取得最优 FID_k 和 BAS，证明其在运动质量和音乐对齐度上的双重优势。
- **Table 4–7**：系统消融验证了解耦令牌化、联合预测、多条件训练和辅助损失四项核心设计的必要性与互补性。

![[assets/figures/papers/paper_list_l954_https_arxiv_org_abs_2506_07565/figures/002_Table_1.jpg]]
*Table 1: Comparison of previous 3D dance datasets. Time/Genre is the mean time (hours) for each genre. Our OpenDanceSet has more detailed and comprehensive annotations, more dancers with diverse movements, and longer duration*

![[assets/figures/papers/paper_list_l954_https_arxiv_org_abs_2506_07565/figures/007_Table_2.jpg]]
*Table 2: Comparison on AIST++ dataset [22]*

![[assets/figures/papers/paper_list_l954_https_arxiv_org_abs_2506_07565/figures/009_Table_3.jpg]]
*Table 3: Comparison on our proposed OpenDanceSet Dataset*

![[assets/figures/papers/paper_list_l954_https_arxiv_org_abs_2506_07565/figures/008_Table_4.jpg]]
*Table 4: Effect of control signal types on AIST and OpenDance-Set. Ablation results are reported on a subset of OpenDanceSet*

![[assets/figures/papers/paper_list_l954_https_arxiv_org_abs_2506_07565/figures/004_Figure_3.jpg]]
*Figure 3: Comparison of processed OpenDanceSet, before filtered OpenDanceSet, and AIST++. After post-optimization and filtering, OpenDanceSet fits dance data distribution and achieves better physical performance*

## 定位与知识库关联

### 1. 方法谱系：从单模态到多模态可控生成的演进

OpenDanceNet 并非凭空出现，而是站在两条技术路线的交叉点上：**音乐驱动的舞蹈生成**与**掩码建模（masked modeling）范式**。理解其谱系位置，需要先厘清它所回应的核心瓶颈——现有方法要么受限于单一音乐条件，要么无法在统一框架内处理音乐、文本、2D 关键点、全局轨迹等异质控制信号的任意组合。

**音乐条件生成路线**的早期工作以 **Bailando**（Siyao et al., CVPR 2022）为代表，采用 VQ-VAE 将运动量化为离散码本，再以 GPT 类自回归模型在音乐特征条件下逐帧预测运动令牌。这一范式奠定了“量化-生成”的基本骨架，但其条件空间仅限于音乐，无法引入空间约束。**EDGE**（Tseng et al., arXiv 2022）将扩散模型引入舞蹈生成，通过编辑能力部分缓解了可控性问题，但本质上仍是音乐到运动的单模态映射。**AI Choreographer**（Li et al., ICCV 2021）使用全注意力跨模态 Transformer 进行音乐到舞蹈的生成，同样未涉及多模态空间控制。**TM2D**（Gong et al., ICCV 2023）首次将文本引入舞蹈生成，实现了音乐+文本的双模态条件，但其文本仅作为风格提示，而非帧级空间约束。**FineDance**（Li et al., 2023）和 **LODGE**（Li et al., CVPR 2024）分别在细粒度编舞数据集和长序列生成上做出贡献，但条件空间仍限于音乐或音乐+风格描述。

**掩码建模路线**在人体运动生成领域展现出强大的序列建模能力。**MoMask**（Guo et al., CVPR 2024）和 **MMM**（Pinyoanuntapong et al., CVPR 2024）分别将掩码预测范式应用于文本到运动和音乐到运动的生成，证明掩码建模在运动令牌上的有效性。**MotionMix**（Hoang et al., 2024）通过弱监督扩散实现可控运动生成，但未触及舞蹈场景下的多模态联合预测。

OpenDanceNet 的关键跨越在于**将上述两条路线融合并升维**：它继承了 Bailando 的量化-生成骨架，但用 Disentangled Dance Tokenizer（DDT）替换了单一共享编码器，将关节旋转、2D 关键点、全局轨迹分别编码为三类独立离散令牌；它借鉴了 MoMask 的掩码预测思想，但将其扩展为**多模态掩码联合预测**——MCT 不仅预测被掩码的运动令牌，还同时预测被掩码的轨迹和关键点令牌，使空间监督从“附加条件”升格为“内在生成目标”。这一设计从根本上解决了早期方法中“所有条件同等对待，导致精细空间信号被粗粒度风格信号淹没”的问题。

### 2. 知识库定位：适用边界与局限

**适用边界**。OpenDanceNet 的核心能力在于“Music+X”范式下的灵活可控生成，其中 X 可以是文本描述、2D 关键点、全局轨迹的任意组合。其适用场景包括：给定音乐和最终姿态关键点的编舞补全、给定音乐和全局位移轨迹的舞台走位生成、以及仅给定音乐和文本风格描述的自由舞蹈生成。DDT 的解耦设计使得稀疏帧级约束（如仅在最后一帧指定关键点位置）能够被直接填充并编码为令牌，无需密集标注即可实现精确空间控制。

**已知局限**。根据论文自身披露，当前方法存在三个明确的能力边界：

1. **手指与面部缺失**：当前 SMPL 参数化仅覆盖身体关节，未包含详细的手指关节点和面部表情参数。这意味着 OpenDanceNet 无法控制手势细节和面部表现，在需要精细手部交互或表情同步的场景（如手势舞、情绪表演）中存在能力缺口。

2. **文本粒度的上限**：文本描述依赖 LLM 生成和人工标注的流水线，尚不支持更细粒度的、具备编辑能力的视觉-语言结构。这意味着用户无法通过自然语言精确指定“第 3 秒到第 5 秒左手举过头顶”这类时序定位描述。

3. **跨任务泛化未验证**：OpenDanceSet 作为大规模多模态数据集，目前仅在 3D 舞蹈生成任务上进行了基准测试，尚未在视频生成等其他生成任务上验证其数据价值。

**证据强度评估**。上述局限均来自论文自身的明确声明，置信度较高。但需注意，OpenDanceNet 在 AIST++ 和 OpenDanceSet 上的实验仅覆盖了音乐条件、音乐+轨迹、音乐+关键点等有限组合的消融，对于“音乐+文本+轨迹+关键点”全组合的极端场景，论文未提供系统性的定量评估，该边界需要人工验证。

### 3. 开放问题

从当前工作出发，三个开放问题值得关注：

1. **细粒度肢体的可控生成**：如何将详细的手指关节和面部表情纳入 DDT 的解耦编码框架？这涉及 SMPL-X 等扩展参数化模型的集成，以及对应码本设计和联合预测损失的重构。

2. **OpenDanceSet 的跨任务基准**：OpenDanceSet 提供了 100.26 小时、14 种流派的 3D 运动、音乐、2D 关键点、轨迹和文本五模态对齐数据，理论上可作为视频生成模型的监督信号。如何在视频扩散模型中利用这些多模态标注设立基准，是数据集价值释放的关键。

3. **视觉-语言架构的令牌化升级**：当前文本令牌来自 LLM 生成的粗粒度描述，若能设计更好的视觉-语言令牌化器，使文本能够精确锚定到时间片段和空间区域，将解锁“时序编辑”能力——例如“将第 2-4 秒的动作替换为旋转跳跃”。这需要重新思考文本编码器与运动令牌之间的对齐机制。

## 原文 PDF

![[paperPDFs/CVPR_2026/OpenDance_Multimodal_Controllable_3D_Dance_Generation_with_Large_scale_Internet_Data.pdf]]
