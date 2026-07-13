---
title: Hoi3DGen Generating High Quality Human Object Interactions in 3D
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Hoi3DGen_Generating_High_Quality_Human_Object_Interactions_in_3D.pdf
project_link: null
code_link: https://github.com/
aliases:
- HGHQHOI3
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用多模态大语言模型分解复杂交互描述为外观、动作和接触子任务，实现自动化的高质量文本标注，并基于筛选出的少量多样化样本微调视图条件的文本到图像模型，从而大幅提升交互生成的文本一致性和接触准确性。
primary_logic: 通过分解标注任务并利用开源 MLLM 生成详细交互描述，可以用少量高质量数据微调现有生成模型，激活其隐式的人物交互能力，同时保持多样性和泛化性，再结合多视图条件和 3D 提升管道实现精确的语义接触控制。
claims:
- Hoi3DGen 在文本一致性 GPT 评分上达到 0.81，远超 TRELLIS 的 0.04 和 InterFusion 的 0.15，接触准确率高达 90%。
- 2D 生成模型微调后接触准确率从基线的 45.76% 提升至 90%，GPT 评分从 0.31 提升至 0.69。
- 数据过滤使接触准确率从 0.80 提升至 0.90，重新纹理化使 GPT 评分从 0.05 提升至 0.75。
- 多视图条件采样将 3D 提升后的接触准确率从单视图的 78.3% 提升至三视图的 90.0%。
---

# Hoi3DGen Generating High Quality Human Object Interactions in 3D

> [!tip] 核心洞察
> 通过分解标注任务并利用开源 MLLM 生成详细交互描述，可以用少量高质量数据微调现有生成模型，激活其隐式的人物交互能力，同时保持多样性和泛化性，再结合多视图条件和 3D 提升管道实现精确的语义接触控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | Hoi3DGen：生成高质量的三维人物交互 |
| 英文题名 | Hoi3DGen Generating High Quality Human Object Interactions in 3D |
| 会议/期刊 | arXiv 2026 |
| Links | [Code](https://github.com/) · [paper](https://arxiv.org/abs/2603.12126) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Hoi3DGen |
| Dataset | 文本一致性和3D质量（GPT评分）, 接触准确率（3D交互）, 2D生成文本一致性与接触准确率 |

> [!tip] 效果简介
> - 文本一致性和3D质量（GPT评分） 上，GPT选择的偏好比率 0.81 (Text Consistency) / 0.79 (3D Quality) vs TRELLIS 0.04/0.21, InterFusion 0.15/0.00 (4–15× improvement over baselines)。
> - 接触准确率（3D交互） 上，接触部位与文本提示的一致性百分比 90% vs TRELLIS N/A, InterFusion N/A (N/A)。
> - 用户研究偏好 上，参与者选择的比例 91.09% (文本一致性) / 85.56% (3D质量) vs TRELLIS 3.44%/10.16%, InterFusion 5.47%/3.28% (显著优于其他方法)。

## 概要

**问题瓶颈**：从文本描述生成高质量、接触语义精确的三维人物交互（HOI）面临双重挑战——一方面缺乏大规模、细粒度且配对准确的文本-3D交互数据，另一方面现有基于分数蒸馏采样（SDS）的方法难以在保持3D模型质量的同时精确控制接触语义。

**核心思路**：Hoi3DGen 提出了一套从数据到生成的完整解决方案。首先，通过将复杂的交互描述任务分解为外观标注、交互标注和描述生成三个子任务，利用开源多模态大语言模型（MLLM）实现自动化的高质量文本标注；然后，仅需从标注数据中筛选出 400 个高质量样本（8 种接触配置各 50 个），即可微调视图条件的文本到图像模型，激活其隐式的人物交互生成能力，同时保持多样性和泛化性；最后，通过多视图条件采样和 3D 提升管道实现精确的语义接触控制。

**方法定位**：Hoi3DGen 区别于通用的文本到3D对象生成模型（如 **TRELLIS**）和基于 SDS 的交互生成模型（如 **InterFusion**），其关键创新在于“分解标注-筛选微调-视图控制-3D提升”的级联范式，而非直接训练一个端到端的文本到3D交互模型。

**主要结果**：在文本一致性 GPT 评分上，Hoi3DGen 达到 0.81，远超 TRELLIS 的 0.04 和 InterFusion 的 0.15（4–15× 提升）；接触准确率高达 90%，而基线方法基本无法处理接触语义。用户研究中，91% 的参与者在文本一致性上偏好 Hoi3DGen，86% 在 3D 质量上偏好 Hoi3DGen。消融实验证实，数据过滤、重新纹理化和多视图采样各自对接触准确率和文本一致性有显著贡献。

### 3D人物交互生成的任务困境

生成高质量的三维人物交互（Human-Object Interaction, HOI）是计算机视觉与图形学中的核心挑战，其目标是根据文本描述生成包含精确接触语义的、纹理化的人体与物体三维网格。该任务在具身智能、虚拟现实和内容创作等领域具有广泛应用前景，但当前技术路线面临根本性瓶颈：**缺乏大规模、细粒度且配对准确的文本-3D人物交互数据**，导致现有方法难以精确控制接触语义并保持三维模型质量。

### 现有方法的根本局限

当前文本到3D交互生成主要存在两条技术路线，但均存在显著缺陷：

**通用文本到3D对象生成模型**（如TRELLIS）能够直接生成完整网格，但其设计目标为独立对象，完全不具备交互语义理解能力。当输入包含复杂交互描述的文本时，这类模型无法生成人体与物体之间的接触关系，导致输出与文本严重不一致。实验表明，TRELLIS在文本一致性GPT评分上仅获得0.04，远低于Hoi3DGen的0.81（Table 1）。

**基于分数蒸馏采样（Score Distillation Sampling, SDS）的交互生成模型**（如InterFusion）虽然专门针对交互场景设计，但SDS方法本身存在Janus问题（多面体效应）和生成质量低下的固有限制。InterFusion在文本一致性评分上仅达到0.15，3D质量评分为0.00，表明其无法同时满足语义准确性和视觉质量的要求（Table 1）。

### 核心瓶颈的因果分解

上述方法失败的根本原因可归结为三个相互关联的瓶颈：

1. **数据瓶颈**：现有3D HOI数据集（如ProciGen，约75万样本）虽然规模可观，但缺乏细粒度的自然语言描述，尤其是关于接触部位、动作类型和物体属性的详细标注。手动标注此类数据成本极高且难以规模化。

2. **语义控制瓶颈**：文本到3D的映射高度复杂，涉及外观理解、姿态推理和接触语义三个层面。直接将复杂交互描述映射到三维空间而不进行任务分解，导致生成模型难以学习精确的语义对应关系。

3. **视图一致性与遮挡瓶颈**：单视图生成无法处理遮挡区域的接触关系，导致三维重建后接触部位丢失或错误。需要多视图条件采样来克服这一限制。

### Hoi3DGen的动机与核心洞察

针对上述瓶颈，Hoi3DGen提出了一种全新的解决思路：**通过分解标注任务并利用开源多模态大语言模型（MLLM）生成详细交互描述，可以用少量高质量数据微调现有生成模型，激活其隐式的人物交互能力，同时保持多样性和泛化性**。

核心洞察在于：现有的文本到图像扩散模型（如SANA）虽然未专门针对交互场景训练，但其在大规模图文数据上预训练获得的视觉先验中已经隐式包含人物交互的知识。通过精心设计的自动标注管道生成高质量配对数据，并对模型进行轻量级微调，即可激活这些隐式能力，使其能够精确遵循接触语义生成交互图像。再结合多视图条件采样和三维提升管道，即可实现从文本到高质量三维交互网格的端到端生成。

这一思路的关键优势在于：无需从头训练三维生成模型，而是充分利用二维基础模型的强大生成能力，通过数据质量提升和视图条件控制来实现三维交互的精确生成，从而在保持生成多样性的同时大幅提升接触准确率。

## 核心方法与创新机理

Hoi3DGen 的核心创新在于绕开了“大规模配对文本-3D交互数据”这一根本瓶颈，转而通过**分解式自动标注 + 小样本视图条件微调**，激活现有生成模型的隐式交互能力。其技术路线可概括为三个相互耦合的关键机制。

### 1. 分解式 MLLM 自动标注：从粗粒度网格到细粒度文本

现有 3D 人物交互（HOI）数据集缺乏细粒度的自然语言描述，手动标注成本极高。Hoi3DGen 提出将复杂的交互描述任务**分解为三个子任务**，分别由开源多模态大语言模型（MLLM）完成（Sec 3.1）：

- **外观标注**：利用 InternVL 描述人体与物体的视觉属性。
- **交互标注**：识别动作类型及接触的身体部位。
- **融合生成**：将上述子任务结果输入 LLaMA，整合为包含外观、动作和接触语义的完整自然语言描述。

这一策略将原本 MLLM 难以直接解决的复杂任务，转化为多个可独立完成的简单子问题，从而实现了大规模、高质量文本标注的自动化。

### 2. 小样本高质量数据筛选与视图条件微调

直接使用全量 ProciGen 数据集（约 75 万样本）进行训练，反而会因数据噪声降低模型性能。Hoi3DGen 的关键操作是**极端的数据筛选**：从 8 种接触配置中各选取 50 个高质量样本，仅用 400 个筛选后的 3D HOI 实例进行微调（Sec 3.1 Filtering）。

在此基础上，Hoi3DGen 引入**视图条件控制**：在文本提示中附加视图描述（front、left diagonal、right diagonal），使微调后的 SANA 扩散模型能够生成指定视角的交互图像。这一设计直接服务于后续的多视图 3D 提升，有效克服了单视图重建中的遮挡问题。

### 3. 重新纹理化：解耦接触语义与纹理质量

Hoi3DGen 在 3D 重建后引入一个独立的**重新纹理化步骤**，使用 Flux 模型对生成网格进行纹理增强（Sec 3.2）。消融实验（Table 3）表明，该步骤对接触准确率影响极小（0.90 → 0.85），但 GPT 评分从 0.05 跃升至 0.75，证明其作用在于提升视觉质量，而非接触语义——实现了两者的有效解耦。

### 与 Baseline 的本质差异

| 维度 | 基线方法 | Hoi3DGen |
|------|---------|----------|
| 数据策略 | 有限手动标注或无详细接触描述 | 分解式 MLLM 自动标注，生成细粒度文本 |
| 训练规模 | 全量 ProciGen（~75 万） | 精选 400 高质量样本 |
| 视角控制 | 无视图条件，随机生成 | 文本附加视图描述，可控多视角采样 |
| 纹理处理 | 扩散模型直接输出 | 独立 Flux 重新纹理化 |

与 **TRELLIS**（通用文本到 3D，无交互语义）和 **InterFusion**（基于 SDS，存在 Janus 问题且生成质量低）相比，Hoi3DGen 的核心优势在于：用极少量高质量数据微调现有模型，激活其隐式的交互理解能力，同时保持多样性和泛化性，再通过多视图条件与 3D 提升管道实现精确的语义接触控制。

Hoi3DGen 提出了一条从文本描述到高质量三维人物交互（HOI）生成的完整流水线。该框架的核心洞察在于：通过将复杂的交互描述任务分解为外观、动作和接触等子任务，利用开源多模态大语言模型（MLLM）自动生成高质量标注，从而用少量筛选数据微调现有生成模型，激活其隐式的人物交互能力。

流水线由三个核心阶段串联构成：

1. **自动数据标注管道**：给定一个三维人物交互网格，首先利用 **InternVL** 分别进行外观标注（描述人物与物体的视觉特征）和交互标注（描述动作及接触的身体部位），随后由 **LLaMA** 整合这些子任务结果，生成最终的详细自然语言描述。这一分解式标注策略解决了大规模、细粒度配对文本-3D交互数据匮乏的瓶颈。

2. **视图条件二维图像生成器**：基于 **SANA** 扩散模型进行微调。输入不仅包含交互文本提示 $t$，还附加视图描述 $t_v$（如 front、left diagonal、right diagonal），使模型能够生成指定视角下的交互图像。微调采用标准的 EDM 风格扩散损失函数：
   $$\mathcal{L} = \mathbb{E}_{x_0, \epsilon, \sigma} \left[ \left\| \epsilon - \epsilon_\theta (z_t, \sigma, \mathrm{cond}) \right\|_2^2 \right]$$
   其中条件 $\mathrm{cond}$ 包含文本提示和视图描述。训练数据经过严格筛选：从 ProciGen 数据集的 8 种接触配置中各选取 50 个高质量样本，共 400 个实例用于微调，而非使用全部约 75 万样本。

3. **三维交互重建与语义分割**：将多视图生成的二维图像通过 **Hunyuan3D** 提升为带纹理的三维网格。随后利用 **GSAM2** 进行视频分割，并通过多视图顶点可见性检查和多数投票机制为网格顶点分配语义标签，实现人体与物体的分离。分割后的人体网格通过 **CameraHMR** 和 Chamfer 优化与 SMPL 模型配准，最终输出可动画的 SMPL 模型及精确的接触语义。

整个框架的输出包括：分割后的人体网格、物体网格，以及与之对齐的可动画 SMPL 模型，三者共同构成符合精确接触语义的高质量三维交互场景。

![[assets/figures/papers/paper_list_l21_Hoi3DGen_Generating_High_Quality_Human_Object_Interactions_in_3D/figures/001_Figure_1.jpg]]
*Figure 1: Given detailed text descriptions of human, object and their interactions, Hoi3DGen generates high quality textured human and object meshes that follow precisely the contact semantics, together with an aligned animatable SMPL model*

![[assets/figures/papers/paper_list_l21_Hoi3DGen_Generating_High_Quality_Human_Object_Interactions_in_3D/figures/002_Figure_2.jpg]]
*Figure 2: HOI3D framework overview. Top: We first leverage the existing multimodal foundation model InternVL [9] to perform decomposed annotation of human, object, and human-object-interaction of samples from the ProciGen [59] dataset. We then use LLaMa [17] to create a final detailed caption for the sample. Bottom: We leverage our data consisting of high-quality and diverse human-objectinteractions to fine-tune an existing text-to-image model. Subsequently, we establish a pipeline to reconstruct high-fidelity textured 3D meshes. The output of our final text-to-3D inference pipeline consists of segmented meshes for the human and object, as well as an animatable SMPL model*

Hoi3DGen 的核心架构由四个紧密协作的模块构成，分别解决数据标注、2D 交互生成、3D 重建与语义分割、以及可动画化人体配准问题。以下逐一阐述各模块的设计动机与关键公式。

### 自动数据标注管道

该模块旨在解决大规模、细粒度文本-3D 交互配对数据匮乏的瓶颈。其核心创新在于将复杂的交互描述任务**分解**为多模态大语言模型（MLLM）可独立解决的子任务，而非直接生成完整描述。

具体流程为：首先利用 **InternVL** 对 3D 交互样本分别进行外观标注（描述人物与物体的颜色、纹理、形状等）和交互标注（描述动作类型及接触的身体部位）；随后，由 **LLaMA** 整合这些结构化标注，生成自然语言形式的最终描述。这种分解策略绕过了现有 MLLM 在一步式生成复杂交互描述时常见的遗漏和幻觉问题，确保了标注的完整性与准确性。

### 视图条件 2D 图像生成器

该模块负责从文本描述和指定的相机视角生成高保真交互图像。其基础是一个预训练的文本到图像扩散模型（SANA），通过微调激活其隐式的人物交互能力。

**条件机制**：不同于传统无条件生成，该模块在文本提示 $t$ 后附加视图描述 $t_v$（如 "front view"、"left diagonal view"、"right diagonal view"），形成联合条件 $\mathrm{cond} = (t, t_v)$，从而精确控制生成图像的视角。这一设计是后续多视图 3D 提升的基础。

**训练目标**：微调采用标准的 EDM 风格扩散损失函数，最小化预测噪声与真实噪声之间的均方误差：

$$
\mathcal{L} = \mathbb{E}_{x_0, \epsilon, \sigma} \left[ \left\| \epsilon - \epsilon_\theta (z_t, \sigma, \mathrm{cond}) \right\|_2^2 \right]
$$

其中，$x_0$ 为原始图像，$\epsilon$ 为添加的高斯噪声，$\sigma$ 为噪声强度，$z_t$ 为加噪后的潜在表示，$\epsilon_\theta$ 为以条件 $\mathrm{cond}$ 为输入的噪声预测网络。通过在此损失下训练，模型学会在给定文本和视图条件下生成语义一致、视角可控的交互图像。

### 3D 交互重建与语义分割

该模块将 2D 生成结果提升为带纹理的 3D 网格，并实现人体与物体的精确分离。

**3D 重建**：对视图条件生成器输出的三张不同视角图像，直接应用 **Hunyuan3D** 进行 3D 重建，获得三个独立的带纹理交互网格。

**交互分割**：为分离人体与物体，采用基于多视图掩码投票的策略。首先利用 **GSAM2** 视频分割模型在各视图中提取对象掩码 $\mathbf{M}_i^o$。对于网格上的每个顶点 $\mathbf{v}$，通过深度一致性检查判断其在视图 $i$ 中的可见性：

$$
\mathrm{vis}_i(\mathbf{v}) = \mathbf{1}[ -\delta \leq z_i(\mathbf{v}) - \mathbf{D}_i(\pi_i(\mathbf{v})) \leq \delta ]
$$

其中，$z_i(\mathbf{v})$ 为顶点在视图 $i$ 相机坐标系下的深度，$\mathbf{D}_i(\pi_i(\mathbf{v}))$ 为投影点 $\pi_i(\mathbf{v})$ 处的渲染深度，$\delta$ 为深度容差。该公式确保仅当顶点位于网格表面且未被遮挡时，才被视为可见。

随后，对可见顶点进行多数投票，为每个顶点赋予对象标签 $l(\mathbf{v})$：

$$
l(\mathbf{v}) = \begin{cases} 1, & \text{if } \frac{1}{|\mathcal{V}(\mathbf{v})|} \sum_i \mathbf{M}_i^o[\pi_i(\mathbf{v})] > \tau \\ 0, & \text{otherwise} \end{cases}
$$

其中，$\mathcal{V}(\mathbf{v})$ 为顶点 $\mathbf{v}$ 可见的视图集合，$\tau$ 为投票阈值。该机制有效融合多视图信息，克服了单视图分割中因遮挡和视角歧义导致的边界模糊问题。

### SMPL 配准与语义接触计算

该模块将可动画化的 SMPL 人体模型对齐到分割后的人体网格上，从而获取关节语义并精确定位接触点。

**初始配准**：首先使用 **CameraHMR** 从各视图图像中估计 SMPL 参数，作为初始姿态。

**优化对齐**：为提升配准精度，选取投影到人体掩码内的顶点子集进行 Chamfer 距离优化：

$$
\mathcal{V}' = \{ \mathbf{v} \in \mathcal{V} \mid \mathbf{M}_{\mathrm{front}}^h[ \pi_{\mathrm{front}}(\mathbf{v}) ] = 1 \}
$$

其中，$\mathbf{M}_{\mathrm{front}}^h$ 为前视图的人体掩码。仅在此可靠子集上优化 SMPL 参数，避免了因分割误差导致的错误对齐。配准完成后，可直接根据 SMPL 的关节拓扑确定各身体部位的语义标签，并计算与物体网格的接触点。

### 重新纹理化

作为后处理步骤，使用 **Flux** 模型对生成的 3D 网格进行重新纹理化。消融实验表明，该步骤对接触准确率影响较小（0.90 → 0.85），但能显著提升 GPT 评分（0.05 → 0.75），证明其主要贡献在于增强纹理质量和视觉保真度，而非交互语义。

## 实验与关键发现

### 主要结果：文本一致性、3D质量与接触准确率

Hoi3DGen 在三个核心维度上均显著超越现有方法。表1汇总了与通用文本到3D模型 TRELLIS 和交互专用模型 InterFusion 的定量对比。在文本一致性 GPT 评分上，Hoi3DGen 达到 0.81，而 TRELLIS 仅为 0.04，InterFusion 为 0.15，提升幅度达 4–15 倍。在 3D 质量 GPT 评分上，Hoi3DGen 获得 0.79，TRELLIS 为 0.21，InterFusion 为 0.00，提升幅度达 3–7 倍。更重要的是，Hoi3DGen 实现了 90% 的接触准确率——即生成的人体-物体接触部位与文本描述的一致性比例，而两个基线方法均无法输出可评估的交互接触。

用户研究进一步验证了上述自动指标：在文本一致性上，91.09% 的参与者偏好 Hoi3DGen 的结果；在 3D 质量上，85.56% 的参与者做出相同选择。这些结果确认了 Hoi3DGen 在语义对齐和几何保真度上的双重优势。

InterFusion 基于分数蒸馏采样（SDS），生成速度慢且受 Janus 问题困扰，输出质量低（见图4定性对比）。TRELLIS 作为通用对象生成模型，虽然能产生完整网格，但完全缺乏交互语义，无法生成人体与物体的接触关系。

### 2D 生成阶段的独立评估

为隔离 2D 生成模块的贡献，表2将微调后的视图条件扩散模型与预训练的 SANA 基线进行对比。微调后，GPT 评分从 0.31 提升至 0.69，接触准确率从 45.76% 跃升至 90%。这表明，即使仅在 400 个高质量样本上微调，模型也能获得精确的接触语义理解能力。

值得注意的是，CLIP 评分在本任务中表现出不可靠性。如图3所示，尽管 Hoi3DGen 生成的图像明显更符合交互描述，CLIP 评分却呈现相反趋势。原因在于 CLIP 对细粒度交互语义（如具体接触部位）的敏感度不足，因此本研究主要依赖 GPT 评分和接触准确率作为文本一致性的评估指标。

### 消融实验

表3报告了关键设计选择的消融结果。

**数据过滤的影响**：移除数据过滤步骤（即使用全部约 75 万 ProciGen 样本训练），接触准确率从 0.90 降至 0.80，GPT 评分从 0.75 骤降至 0.20。这证明仅用少量高质量样本微调远优于使用全量噪声数据。高质量标注和筛选是激活模型隐式交互能力的关键。

**重新纹理化的影响**：移除 Flux 重新纹理化步骤后，GPT 评分从 0.75 暴跌至 0.05，而接触准确率仅从 0.90 小幅降至 0.85。这表明重新纹理化主要贡献于视觉质量和文本一致性感知，对接触几何的影响相对有限。两项设计结合达到最优效果。

### 多视图条件采样的有效性

表4展示了不同视角数量对 3D 提升后接触准确率的影响。使用单视图生成图像进行 3D 重建时，接触准确率为 78.3%；增加至双视图提升至 86.7%；三视图达到 90.0%。从单视图到三视图，绝对提升达 11.7 个百分点。视图条件采样使模型能够从互补角度生成交互图像，有效克服遮挡问题，为后续的 3D 提升提供更稳定的多视图输入。

### 分部位接触准确率分析

表5按身体部位细分接触准确率。Hoi3DGen 在右手、左手、右脚、左脚、双腿等各类接触场景中均保持高准确率。相比之下，SANA 基线仅能较好地跟随“右手”和“双腿”接触，在其他部位（尤其是单脚接触）上表现不佳。这进一步证实微调使模型获得了细粒度的部位级接触理解能力，而非简单的整体姿态匹配。

### 失败模式与局限性

尽管整体性能优异，Hoi3DGen 在以下场景中仍存在不足：

1. **复杂姿态描述的跟随困难**：当文本描述包含非常细微或复杂的人体姿态差异时，模型可能无法精确复现。这一方面源于文本描述姿态本身具有模糊性，另一方面训练数据中缺乏足够多样的独特姿态示例来覆盖所有特征姿态。
2. **开放问题**：论文提出了若干未来方向，包括引入专用的文本到人体姿态生成模块以提升姿态跟随能力、扩展至更广泛的对象类别和未见过的交互组合、以及将方法从静态 3D 姿态扩展至动态交互序列生成。

![[assets/figures/papers/paper_list_l21_Hoi3DGen_Generating_High_Quality_Human_Object_Interactions_in_3D/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with text-to-3D models. We compare our method against TRELLIS [55], a general text-to-3D object generation model, and InterFusion [10], a text-to-3D interaction model. Our method outperforms all prior arts in both consistency to input text and quality of the generated 3D interactions by a very large margin*

![[assets/figures/papers/paper_list_l21_Hoi3DGen_Generating_High_Quality_Human_Object_Interactions_in_3D/figures/013_Table_2.jpg]]
*Table 2: Quantitative comparison with 2D baselines. We compare our method against pretrained text-to-2D generation SANA [56] model. Our method achieves higher text consistency and 3D interaction quality. The CLIP score is however not very informative due to its limited sensitivity to fine-grained text [23, 73] as we also show in Fig. 3*

![[assets/figures/papers/paper_list_l21_Hoi3DGen_Generating_High_Quality_Human_Object_Interactions_in_3D/figures/014_Table_3.jpg]]
*Table 3: Ablation studies. Our proposed data filtering improves contact accuracy and retexturing improves consistency to text input (GPT score). Combining both achieves the best result*

![[assets/figures/papers/paper_list_l21_Hoi3DGen_Generating_High_Quality_Human_Object_Interactions_in_3D/figures/036_Figure_11.jpg]]
*Figure 11: More qualitative comparison. Our method consistently produces high quality results with correct contact and details*

## 定位与知识库关联

### 任务定位与核心瓶颈

Hoi3DGen 瞄准的是**文本到三维人物-物体交互（Text-to-3D HOI）生成**这一新兴任务。该任务要求从自然语言描述中生成具有精确接触语义的、可分割的人体和物体三维网格，并附带可驱动的 SMPL 模型。其核心瓶颈在于：**缺乏大规模、细粒度且配对准确的文本-3D交互数据**，而现有基于分数蒸馏采样（SDS）的方法难以精确控制接触语义并保持三维模型质量。

### 与现有方法的谱系关系

#### 文本到3D通用生成模型：TRELLIS

**TRELLIS** 是通用文本到3D对象生成模型，可直接从文本生成完整的三维网格。然而，TRELLIS 的设计目标不包含人物交互语义——它生成的是单一对象而非交互场景，无法理解“人手持物”“人坐在椅子上”等接触关系。在 Hoi3DGen 的评测中，TRELLIS 的文本一致性 GPT 评分仅为 0.04，且接触准确率无法评估（N/A），这从反面证明了通用生成模型在交互场景下的根本性不足。

#### 基于SDS的交互生成模型：InterFusion

**InterFusion** 是基于分数蒸馏采样的文本到3D交互生成模型，是 Hoi3DGen 最直接的同任务基线。SDS 方法通过预训练扩散模型引导三维表示优化，但存在众所周知的 **Janus 问题**（多面不一致）和生成质量低的问题。InterFusion 的 GPT 文本一致性评分仅为 0.15，3D 质量评分为 0.00，且同样无法评估接触准确率。Hoi3DGen 在方法论上彻底绕开了 SDS 范式，转而采用“微调2D生成器 + 3D提升”的路线，从根本上规避了 Janus 问题。

#### 预训练文本到图像模型：SANA

**SANA** 是预训练的文本到图像扩散模型，作为 Hoi3DGen 微调的基座模型。未经微调的 SANA 在交互生成上表现有限：接触准确率仅 45.76%，GPT 评分为 0.31。Hoi3DGen 通过自动标注的高质量交互数据对 SANA 进行微调，将接触准确率提升至 90%，GPT 评分提升至 0.69，证明了**针对性数据微调可以激活预训练模型中隐式的交互生成能力**。

### 方法谱系中的关键创新定位

Hoi3DGen 的方法论创新可以沿三个维度定位：

1. **数据维度**：不同于依赖有限人工标注或弱监督的现有方法，Hoi3DGen 提出了**分解式多模态大语言模型自动标注管道**。它将复杂的交互描述分解为外观标注、交互标注和描述生成三个子任务，分别由 InternVL 和 LLaMA 完成。这一策略使得从 ProciGen 数据集中自动生成高质量文本配对成为可能。

2. **生成范式维度**：Hoi3DGen 采用**“微调2D扩散模型 + 多视图3D提升”**的范式，区别于 SDS 优化范式。具体而言，它在 SANA 扩散模型上引入视图条件（front / left diagonal / right diagonal），通过标准扩散损失进行微调：
   $$\mathcal{L} = \mathbb{E}_{x_0, \epsilon, \sigma} \left[ \left\| \epsilon - \epsilon_\theta (z_t, \sigma, \mathrm{cond}) \right\|_2^2 \right]$$
   其中条件 $\mathrm{cond}$ 包含交互文本提示和视图描述。随后使用 Hunyuan3D 将多视图图像提升为三维网格。

3. **后处理维度**：Hoi3DGen 引入了**重新纹理化**（使用 Flux 模型提升纹理质量）和**训练无关的 SMPL 配准管道**（基于 CameraHMR 和 Chamfer 优化），这些组件显著提升了输出质量，但对接触语义本身的影响有限（消融实验显示重新纹理化对接触准确率影响为 0.90→0.85）。

### 适用边界与局限

Hoi3DGen 的适用边界受以下因素制约：

- **姿态描述复杂性**：模型难以遵循非常复杂的人体姿态描述（如细微的动作差异）。这一局限部分源于文本描述姿态本身具有模糊性，部分源于训练数据中缺乏足够多样的独特姿态示例。
- **数据依赖**：方法依赖 ProciGen 数据集中的 3D HOI 样本进行标注和微调。尽管仅使用 400 个筛选后的高质量样本（8 种接触配置各 50 个），但其泛化性受限于该数据集的覆盖范围。
- **静态交互**：当前方法仅生成静态的三维交互姿态，不支持动态交互序列生成。

### 开放问题

1. **姿态生成模块化**：能否引入专用的文本到人体姿态生成模块，将复杂姿态描述显式转换为姿态参数（如 SMPL 参数），以突破姿态跟随瓶颈？
2. **跨类别泛化**：在更广泛的对象类别和未见过的人体-物体交互组合上，当前方法的泛化性如何？是否可以通过扩大训练数据的类别覆盖范围来进一步提升？
3. **动态交互扩展**：能否将该方法扩展至动态交互序列——即从文本生成连续的人体-物体交互动画，而非仅静态三维姿态？这需要解决时序一致性和物理合理性等新挑战。

## 原文 PDF

![[paperPDFs/arxiv_2026/Hoi3DGen_Generating_High_Quality_Human_Object_Interactions_in_3D.pdf]]
