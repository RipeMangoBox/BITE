---
title: "Stroke3D: Lifting 2D strokes into rigged 3D model via latent diffusion models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Stroke3D_Lifting_2D_strokes_into_rigged_3D_model_via_latent_diffusion_models.pdf
project_link: https://whalesong-zrs.github.io/Stroke3D_project_page/
code_link: null
openreview_forum_id: VgOWxor3LV
aliases:
- Stroke3D
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入用户绘制的2D笔画作为结构条件（Jxy），约束骨架生成过程，从而消除文本到骨架的结构模糊性。"
primary_logic: "先由2D笔画和文本引导生成拓扑明确的可控3D骨架，再利用增强的骨骼-网格数据集和基于对齐分数的偏好优化，生成高质量的可绑定、可动画的网格，实现了端到端的易用3D资产生成。"
claims:
- "在骨架生成的Chamfer Distance所有指标上，Stroke3D均取得了最低的误差，优于RigNet、SKDream、MagicArticulate和UniRig。"
- "在网格生成的SKA评分中，结合TextuRig和SKA-DPO后，Mean Inst SKA分数高达87.83，比SKDream基线提高了约7.4分。"
- "引入结构条件（Jxy）后，模型收敛速度显著加快，验证了2D笔画结构指导的有效性。"
- "模型对输入噪声具有鲁棒性，能处理任意视角，并成功泛化到训练中未见的罕见概念如“Samurai”和“Turtle”。"
---

# Stroke3D: Lifting 2D strokes into rigged 3D model via latent diffusion models

> [!tip] 核心洞察
> 先由2D笔画和文本引导生成拓扑明确的可控3D骨架，再利用增强的骨骼-网格数据集和基于对齐分数的偏好优化，生成高质量的可绑定、可动画的网格，实现了端到端的易用3D资产生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Stroke3D：通过潜在扩散模型将2D笔画提升为绑定骨骼的3D模型 |
| 英文题名 | Stroke3D: Lifting 2D strokes into rigged 3D model via latent diffusion models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=VgOWxor3LV) · [Project](https://whalesong-zrs.github.io/Stroke3D_project_page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Stroke3D |
| Dataset | MagicArticulate test set, SKDream evaluation set |

> [!tip] 效果简介
> - MagicArticulate test set 上，CD-J2J (All) ↓ 为 0.048，对比 0.111 (SKDream)，变化 -0.063。
> - SKDream evaluation set 上，Mean Inst SKA Score ↑ 为 87.83，对比 80.43 (SKDream)，变化 +7.4。
> - SKDream evaluation set 上，Mean Class SKA Score ↑ 为 84.36，对比 74.38 (SKDream)，变化 +9.98。

## 概要

### 问题与瓶颈

从文本描述直接生成可绑定骨骼（rigging）并可动画的3D网格，面临两大核心困难。其一，文本到骨架存在严重的结构模糊性——同一段文字可以对应多种拓扑与姿态不同的骨架，导致模型难以稳定收敛。其二，训练数据的规模和覆盖范围有限，现有数据集在纹理质量、骨骼标注完整性以及姿态多样性上均存在明显短板，使得模型对罕见概念（如武士、乌龟）的生成不稳定，且姿态变化不够丰富。

### 核心思路

Stroke3D 将上述问题拆解为两个可控阶段，并以**用户绘制的2D笔画作为结构条件**来消除骨架生成的模糊性。在第一阶段，用户提供2D拓扑图（关节位置与连接边）和文本提示；模型通过**图变分自编码器（Sk-VAE）**将3D骨架图编码到连续隐空间，再由**图扩散变压器（Sk-DiT）**在该隐空间内以2D笔画和文本为条件进行去噪生成，从而获得拓扑明确、姿态可控的3D骨架。在第二阶段，引入**TextuRig数据集**（经纹理筛选和视觉语言模型重述的高质量骨骼-网格配对数据）增强训练，并采用**基于骨架-网格对齐分数的偏好优化（SKA-DPO）**对基础骨架-网格生成模型进行微调，最终产出几何保真度高、可直接绑定动画的3D网格。

### 方法定位

Stroke3D 在方法谱系中处于“条件生成+偏好优化”的交叉点。相较于依赖物理模拟或自回归生成的骨架方法（如 **RigNet** Xu et al., SIGGRAPH 2020、**MagicArticulate** Song et al., CVPR 2025、**UniRig** Zhang et al., SIGGRAPH 2025），Stroke3D 首次将用户手绘2D拓扑图作为显式条件引入扩散生成过程，实现了从“文本模糊控制”到“笔画结构控制”的转变。在网格生成侧，相较于仅使用监督微调的 **SKDream**（Xu et al., CVPR 2025 Highlight），Stroke3D 通过 TextuRig 数据增强和 SKA-DPO 偏好优化，直接以骨架-网格对齐程度作为优化信号，显著提升了生成质量。

### 主要结果

在骨架生成任务上，Stroke3D 在所有 Chamfer Distance 指标上均取得最低误差（Table 1），其中 CD-J2J (All) 降至 0.048，较 SKDream 的 0.111 降低约 57%。在网格生成任务上，结合 TextuRig 和 SKA-DPO 后，Mean Inst SKA 分数达到 87.83，比 SKDream 基线提高约 7.4 分；Mean Class SKA 分数达到 84.36，提升约 10 分（Table 2）。消融实验证实，引入结构条件（Jxy）后模型收敛速度显著加快（Figure 7），而 SKA-DPO 的偏好分数边际设为 0.1 时在实例级和类别级评分上取得最佳权衡（Table 3）。定性评估表明，模型对输入噪声具有鲁棒性，能处理任意视角，并成功泛化到训练中未见的罕见概念（Figure 11）。

### 局限与开放问题

当前方法仍受限于训练数据的姿态多样性不足，罕见类别生成不稳定；当2D笔画存在视角模糊（如侧视图关节重叠）时，生成质量会下降。此外，两阶段框架尚未实现端到端的文本到绑定网格生成。开放问题包括：如何利用更大规模的 Articulation-XL 等数据集扩展姿态覆盖；能否开发端到端网络直接从文本生成可绑定网格；以及如何系统性地处理笔画的视角模糊性。

三维资产的骨骼绑定是计算机图形学与动画制作中的核心环节，它为静态网格赋予可驱动的运动结构。然而，传统绑定流程高度依赖专业美术人员的手工操作——从拓扑分析、关节放置到蒙皮权重绘制，每一步都需要大量时间与领域经验。这一现状构成了三维内容规模化生产的显著瓶颈。

近年来，学术界开始探索自动化绑定方法。早期工作如 **RigNet**（Xu et al., SIGGRAPH 2020）尝试从输入网格直接预测骨骼结构，但其依赖于完整的三维几何信息作为输入，无法从更轻量的用户意图表达出发。随后出现的 **SKDream**（Xu et al., CVPR 2025 Highlight）将平均曲率流骨架提取与扩散模型相结合，实现了从文本到骨架再到网格的生成管线，但其文本条件存在固有的结构模糊性——同一句描述可以对应多种合理的骨骼拓扑，导致生成结果的不确定性。**MagicArticulate**（Song et al., CVPR 2025）与 **UniRig**（Zhang et al., SIGGRAPH 2025）则采用自回归生成范式，虽在特定指标上有所改进，但同样缺乏对骨骼拓扑的显式可控性。

上述方法的共同缺口在于：**用户无法以直观、低成本的方式精确指定期望的骨骼结构**。文本提示天然具有歧义，而完整三维网格的获取门槛又过高。这导致生成结果与用户意图之间存在难以弥合的“结构鸿沟”。

本文的核心动机正是弥合这一鸿沟。我们观察到，二维笔画是一种极为自然且高效的结构表达方式——用户仅需几笔勾勒即可传达物体的拓扑连接与大致姿态。**Stroke3D** 的核心洞察在于：将用户绘制的二维笔画作为结构条件（记作 $\mathbf{J}_{xy}$），与文本提示共同约束骨骼生成过程，从而消除文本到骨架的结构模糊性。这一设计使得用户能够以“所见即所得”的方式控制生成骨架的关节布局与拓扑连接，同时保留文本对语义类别和风格的高层引导。

在网格生成阶段，现有方法还面临训练数据质量不足的问题。SKDream 所使用的数据集中部分样本缺乏纹理信息，甚至存在骨骼标注不完整的情况（如鸟类骨架缺失关节），直接限制了生成网格的几何保真度与可动画性。为此，本文进一步构建了增强数据集 **TextuRig**，通过纹理筛选与视觉语言模型重述提升数据质量，并引入基于骨架-网格对齐分数的偏好优化策略 **SKA-DPO**，以提升生成网格与输入骨骼的结构一致性。

综上，Stroke3D 的动机可归结为三点：（1）提供一种直观的二维笔画交互方式，实现对三维骨骼结构的显式可控生成；（2）通过增强数据集与偏好优化，提升骨骼到网格生成的质量与对齐精度；（3）构建一个端到端易用的管线，使非专业用户也能快速产出可绑定、可动画的三维资产。

## 核心方法与创新机理

Stroke3D 的核心创新在于将用户绘制的 2D 笔画作为显式结构条件引入 3D 资产生成流程，从而解决了文本到骨架生成中的结构模糊性问题。与现有方法相比，该工作在三方面实现了关键突破：

**1. 2D 笔画驱动的可控骨架生成**

现有方法（如 **SKDream** (Xu et al., CVPR 2025)、**MagicArticulate** (Song et al., CVPR 2025)、**UniRig** (Zhang et al., SIGGRAPH 2025)）或依赖纯文本条件，或从 3D 网格出发生成骨架，缺乏对骨架拓扑和姿态的精细控制。Stroke3D 将用户直接绘制的 2D 拓扑图作为结构条件 $\mathbf{J}_{xy}$，注入到图潜在扩散模型 Sk-DiT 的去噪过程中。这一设计使模型能够从 2D 笔画中推断 3D 骨架的拓扑连接 $\mathbf{E}$ 和空间姿态，为生成过程提供了明确的几何约束。消融实验（Figure 7）验证了引入 $\mathbf{J}_{xy}$ 条件后模型收敛速度显著加快，训练损失下降更迅速。

**2. 数据增强与偏好优化的协同提升**

在网格生成阶段，基线方法 **SKDream** 使用的训练数据存在纹理缺失和骨骼标注不完整等问题（Figure 6a）。Stroke3D 通过两个协同策略实现提升：
- **TextuRig 数据集**：经过纹理筛选和 VLM 重述的高质量骨骼-网格数据集，扩充了训练数据的规模和多样性（Figure 6b）。
- **SKA-DPO 偏好优化**：基于骨架-网格对齐分数（SKA Score）构建偏好对，利用扩散 DPO 目标（Equation 2）对网格生成模型进行偏好微调，鼓励模型在几何保真度上向高质量样本对齐。

Table 2 显示，在 SKDream 基础上依次加入 TextuRig 和 SKA-DPO 后，Mean Inst SKA 分数从 80.43 提升至 87.83（+7.4），Mean Class SKA 分数从 74.38 提升至 84.36（+9.98），验证了数据与算法协同优化的有效性。

**3. 端到端的易用 3D 资产生成范式**

不同于传统方法需要专业建模技能，Stroke3D 构建了从用户笔画到可绑定、可动画 3D 网格的完整两阶段流程：先由 Sk-VAE 与 Sk-DiT 从 2D 笔画和文本生成拓扑明确的 3D 骨架，再由增强的网格生成模型输出高质量网格。Figure 11 的定性评估表明，该流程对输入噪声具有鲁棒性，能处理任意视角，并成功泛化到训练中未见的罕见概念（如“Samurai”、“Turtle”），体现了从 2D 到 3D 的实用化生成能力。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_VgOWxor3LV/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Stroke3D (§Section 3). During the training phase, Sk-VAE encodes a skeleton graph into a latent space. Subsequently, Sk-DiT is trained to generate these latent embeddings, conditioned on the corresponding 2D strokes and text prompt. After training with TextuRig, we leverage SKA-DPO to further refine SKDream with a skeleton-mesh alignment reward signal. The right side illustrates the implementation details of our models*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_VgOWxor3LV/figures/001_Figure_1.jpg]]
*Figure 1: We present Stroke3D (§Section 3), a novel framework that generates rigged 3D meshes from user-drawn strokes and language instructions. We show versatile downstream applications, including generation from different viewpoints, structural editing by adding strokes or modifying joint positions, and final animation. Skeleton color represents the depth in 3D space*

Stroke3D 采用**两阶段级联架构**，将用户输入的 2D 笔画和文本提示转化为可绑定、可动画的 3D 网格。其核心设计思想是将生成过程解耦为**可控骨架生成**与**增强网格合成**两个阶段，从而消除文本到骨架的结构模糊性，并在网格阶段注入更强的几何约束。

### 输入与输出

- **输入**：用户绘制的 2D 骨架拓扑图 $\mathcal{G}_{\mathbf{2D}} = (\mathbf{J}_{\mathbf{xy}}, \mathbf{E})$（由关节 2D 坐标和边连接关系构成）以及描述目标类别的文本提示。
- **输出**：带有完整骨骼绑定信息的 3D 网格，可直接用于动画驱动。

### 阶段一：可控骨架生成

该阶段的目标是从 2D 笔画和文本中生成拓扑明确、姿态可控的 3D 骨架。其核心模块为：

1. **Sk-VAE（Skeletal Graph Variational Autoencoder）**：将 3D 骨架图 $\mathcal{G} = (\mathbf{X}, \mathbf{E})$ 编码为连续隐空间表示。编码器采用 GCN 与 Transformer-Conv 的组合架构，解码器则从隐变量重建完整的 3D 关节坐标。训练目标为重建损失 $\mathcal{L}_{\mathrm{recon}} = \| \mathbf{X} - \mathbf{X}' \|_2^2$ 与 KL 散度 $\mathcal{L}_{KL}$ 的加权和。

2. **Sk-DiT（Skeletal Graph Diffusion Transformer）**：在 Sk-VAE 的隐空间内执行潜在扩散生成。该模块基于 DiT 架构，将标准自注意力层替换为 Transformer-Conv 以适配图结构数据。其训练目标为：
   $$\mathcal{L}_{\mathrm{Sk-DiT}} = \mathbb{E}_{\mathbf{z}_0, t, \epsilon, \mathbf{J}_{xy}, \mathbf{E}, \mathbf{c}_{\mathrm{text}}}\big[ \| \epsilon_\phi(\mathbf{z}_t, t, \mathbf{J}_{xy}, \mathbf{E}, \mathbf{c}_{\mathrm{text}}) - \epsilon \|_2^2 \big]$$
   其中 $\mathbf{J}_{xy}$ 作为**结构条件**直接注入去噪过程，约束生成骨架与用户笔画的拓扑一致性；$\mathbf{c}_{\mathrm{text}}$ 提供语义引导。

**关键机制**：2D 笔画条件 $\mathbf{J}_{xy}$ 是 Stroke3D 区别于纯文本驱动方法的核心因果旋钮。消融实验（Figure 7）表明，引入该条件后模型收敛速度显著加快，验证了显式拓扑指导对消除结构模糊性的有效性。

### 阶段二：增强网格合成

在获得 3D 骨架后，第二阶段将其转化为高质量的可绑定网格。Stroke3D 在现有骨架-网格生成模型 SKDream 的基础上进行了两项关键增强：

1. **TextuRig 数据集**：针对 SKDream 原始数据中部分样本缺乏纹理、骨骼标注不完整的问题，作者构建了经过纹理筛选和 VLM 重述的增强数据集。该数据集通过渲染骨架-网格的正交投影并利用 VLM 生成详细描述（Figure 2），提升了训练数据的质量和语义丰富度。

2. **SKA-DPO 偏好优化**：引入基于骨架-网格对齐分数（SKA Score）的偏好优化策略。具体而言，以 SKA 分数作为奖励信号构建胜出/败出样本对，使用扩散 DPO 目标进行微调：
   $$\mathcal{L}_{\mathrm{SKA-DPO}} = -\mathbb{E}_{(x^{win},x^{lose})\sim\mathcal{D}} \log\sigma\big( -\beta\big( \| \epsilon^{win} - \epsilon_\theta(x_t^{win}, t) \|_2^2 - \| \epsilon^{win} - \epsilon_{\mathrm{ref}}(x_t^{win}, t) \|_2^2 \big) - \big( \| \epsilon^{lose} - \epsilon_\theta(x_t^{lose}, t) \|_2^2 - \| \epsilon^{lose} - \epsilon_{\mathrm{ref}}(x_t^{lose}, t) \|_2^2 \big) \big)$$
   该目标鼓励模型相对于参考模型更准确地预测胜出样本的噪声，从而提升网格与骨架的几何一致性。

### 数据流与模块关系

整体数据流如 Figure 3 所示：训练阶段，Sk-VAE 先将骨架图编码至隐空间，Sk-DiT 在 2D 笔画和文本条件下学习生成隐嵌入；随后，SKDream 以生成的骨架为条件合成网格，并通过 TextuRig 数据增强和 SKA-DPO 偏好优化进行微调。推理阶段，用户提供笔画和文本后，Sk-DiT 采样隐变量并经 Sk-VAE 解码器还原为 3D 骨架，最终由增强后的 SKDream 生成可绑定网格。

### 方法定位

与现有方法相比，Stroke3D 的关键差异在于：骨架生成层面，用**潜在扩散模型 + 2D 笔画条件**替代了 RigNet（Xu et al., SIGGRAPH 2020）的网格到骨架学习、MagicArticulate（Song et al., CVPR 2025）和 UniRig（Zhang et al., SIGGRAPH 2025）的自回归生成范式；网格生成层面，在 SKDream（Xu et al., CVPR 2025 Highlight）基础上通过**数据增强 + 偏好优化**实现了显著提升，而非仅依赖 SDEdit（Meng et al., ICLR 2022）式的扩散编辑。

Stroke3D 采用两阶段流水线：**可控骨架生成**和**增强网格合成**。骨架生成阶段的核心模块是图变分自编码器（Sk-VAE）与图扩散变压器（Sk-DiT），网格合成阶段则基于 SKDream 模型进行数据增强与偏好优化。

### Sk-VAE

Sk-VAE 将三维骨架图 $\mathcal{G} = (\mathbf{X}, \mathbf{E})$ 编码到连续隐空间，其中 $\mathbf{X} \in \mathbb{R}^{N \times 3}$ 表示 $N$ 个关节点的三维坐标，$\mathbf{E}$ 为边拓扑。其编码器采用 GCN 与 Transformer-Conv 架构处理图结构数据。

训练目标由重建损失与 KL 散度加权组成：

$$\mathcal{L}_{\mathrm{G-VAE}} = \mathcal{L}_{\mathrm{recon}} + \beta \cdot \mathcal{L}_{KL}$$

其中重建损失为原始关节点坐标与解码器重建坐标之间的平方 $L_2$ 距离：

$$\mathcal{L}_{\mathrm{recon}} = \| \mathbf{X} - \mathbf{X}' \|_2^2$$

KL 散度约束隐空间分布逼近标准正态分布：

$$\mathcal{L}_{KL} = \frac{1}{2} \sum_{i=1}^{D} (\mu_i^2 + \sigma_i^2 - \ln(\sigma_i^2) - 1)$$

### Sk-DiT

Sk-DiT 在 Sk-VAE 的隐空间内执行潜在扩散生成，其架构基于 DiT 设计，并将标准自注意力层替换为 Transformer-Conv。用户绘制的二维笔画被形式化为二维骨架图 $\mathcal{G}_{\mathbf{2D}} = (\mathbf{J}_{\mathbf{xy}}, \mathbf{E})$，其中 $\mathbf{J}_{\mathbf{xy}}$ 为关节点的二维坐标，作为结构条件注入生成过程。

Sk-DiT 的训练目标为：

$$\mathcal{L}_{\mathrm{Sk-DiT}} = \mathbb{E}_{\mathbf{z}_0, t, \epsilon, \mathbf{J}_{xy}, \mathbf{E}, \mathbf{c}_{\mathrm{text}}}\big[ \| \epsilon_\phi(\mathbf{z}_t, t, \mathbf{J}_{xy}, \mathbf{E}, \mathbf{c}_{\mathrm{text}}) - \epsilon \|_2^2 \big]$$

其中 $\mathbf{z}_t$ 为时刻 $t$ 的噪声隐变量，$\epsilon_\phi$ 为去噪网络，$\mathbf{J}_{xy}$ 为二维关节坐标条件，$\mathbf{E}$ 为边拓扑条件，$\mathbf{c}_{\mathrm{text}}$ 为文本嵌入。模型学习在给定结构条件和语义条件下对隐变量进行去噪。

### SKA-DPO

在网格合成阶段，Stroke3D 在 SKDream 基础上引入基于骨架-网格对齐分数的偏好优化。偏好优化目标为：

$$\mathcal{L}(\theta) = - \mathbb{E}_{(x^{win},x^{lose})\sim\mathcal{D}} \log\sigma\big( -\beta\big( \| \epsilon^{win} - \epsilon_\theta(x_t^{win}, t) \|_2^2 - \| \epsilon^{win} - \epsilon_{\mathrm{ref}}(x_t^{win}, t) \|_2^2 \big) - \big( \| \epsilon^{lose} - \epsilon_\theta(x_t^{lose}, t) \|_2^2 - \| \epsilon^{lose} - \epsilon_{\mathrm{ref}}(x_t^{lose}, t) \|_2^2 \big) \big)$$

该损失鼓励模型 $\epsilon_\theta$ 相对于参考模型 $\epsilon_{\mathrm{ref}}$ 更准确地预测胜出样本的噪声，同时减弱对败出样本的噪声预测。偏好分数边际设为 0.1 时在 MeanInst 和 MeanClass 上取得最佳权衡（Table 3）。

### 关键因果机制

二维笔画 $\mathbf{J}_{xy}$ 作为结构条件的引入是 Stroke3D 的核心因果旋钮：它消除了从纯文本到骨架生成过程中的拓扑与姿态模糊性。消融实验（Figure 7）表明，带有 $\mathbf{J}_{xy}$ 条件的模型训练损失下降速度显著快于无此条件的模型，验证了结构指导对收敛的加速作用。

## 实验与关键发现

### 骨架生成：定量与定性评估

骨架生成是 Stroke3D 的核心可控环节。Table 1 在 MagicArticulate 测试集上报告了 Chamfer Distance（CD）的三项指标（CD‑J2J、CD‑J2B、CD‑B2B）对比。Stroke3D 在所有类别和所有指标上均取得最低误差：**CD‑J2J（All）为 0.048**，较 SKDream 的 0.111 降低 0.063；CD‑J2B（All）为 0.039，CD‑B2B（All）为 0.034。对比方法包括 RigNet（Xu et al., SIGGRAPH 2020）、SKDream（Xu et al., CVPR 2025 Highlight）、MagicArticulate（Song et al., CVPR 2025）和 UniRig（Zhang et al., SIGGRAPH 2025）。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_VgOWxor3LV/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of Chamfer Distance (CD) (§Section 4.3). CD scores are calculated over three metrics (CD-J2J, CD-J2B, CD-B2B) across three categories. The lowest and second-lowest scores are shown in bold and underlined, respectively*

定性结果（Figure 4）进一步表明，现有绑定方法依赖 3D 网格作为输入，而 Stroke3D 以 2D 投影骨架为条件，生成的骨架更忠实地贴合真值拓扑与姿态。在细粒度类别（Mythical、Toy、Weapon）上，Table 5 显示 Stroke3D 同样在 9 个 CD 指标中 8 项最低、1 项次低，证明其跨类别泛化能力。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_VgOWxor3LV/figures/016_Table_5.jpg]]
*Table 5: Quantitative comparison of Chamfer Distance (CD) (§Section4.3). CD scores are calculated over three metrics (CD-J2J, CD-J2B, CD-B2B) across five categories. The lowest and secondlowest scores are shown in bold and underlined, respectively*

笔画‑骨架对齐的定量评估（Table 6）采用 2D Chamfer Distance（CD₂D）度量投影骨架与输入笔画的几何一致性。Stroke3D 在所有类别和指标上均取得最低 CD₂D，验证了结构条件（Jxy）对骨架生成过程的强约束效果。

### 网格生成：SKA 评分与消融

网格生成质量通过 SKA Score 评估。Table 2 在 SKDream 评估集上对比了 SDEdit（Meng et al., ICLR 2022）、SKDream 以及逐步引入 TextuRig 数据集和 SKA‑DPO 偏好优化的消融版本。最终方案（+TextuRig & SKA‑DPO）的 **Mean Inst SKA 分数达 87.83**，较 SKDream 基线（80.43）提升约 7.4 分；**Mean Class SKA 分数达 84.36**，较基线（74.38）提升约 9.98 分。单独引入 TextuRig 已带来显著增益（Mean Inst 86.01，Mean Class 81.99），SKA‑DPO 在此基础上进一步将 Mean Inst 和 Mean Class 分别推高 1.82 和 2.37 分。

骨架条件的多视图生成定性对比（Figure 5）显示，Stroke3D 生成的视图质量更高，对输入骨架的几何忠实度明显优于基线。

### 消融实验

**结构条件 Jxy 的影响。** Figure 7 对比了有无 Jxy 条件时训练损失的收敛曲线。引入 Jxy 后，模型在粉红色和蓝色高亮区间内损失下降速度显著加快，验证了 2D 笔画结构指导对骨架生成收敛的加速作用。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_VgOWxor3LV/figures/011_Figure_7.jpg]]
*Figure 7: Ablation study on structural condition (§Section 4.3). The model converges faster with the structural condition. The pink and blue regions highlight intervals of rapid loss decrease*

**SKA‑DPO 偏好边际。** Table 3 消融了偏好分数边际（0.05、0.10、0.15、0.20）。边际为 0.1 时在 Mean Inst（87.83）和 Mean Class（84.36）上取得最佳权衡；过小的边际（0.05）导致 Mean Class 下降，过大的边际（0.20）则使 Mean Inst 退化。

**骨架生成训练数据消融。** Table 4 对比了四种数据配置：SkDiff‑Small（小规模数据）、SkDiff‑Raw（未对齐）、SkDiff‑NoTag（无文本标签）和 SkDiff‑Full（完整数据，含旋转对齐与文本标签）。SkDiff‑Full 在所有类别和 CD 指标上均取得最低误差，表明数据规模、旋转对齐和文本标注三者对骨架生成质量均有正向贡献。

**输入鲁棒性。** Figure 9 展示了随机丢弃部分关节时 CD 分数的变化曲线。模型在少量关节缺失的情况下仍能保持较低的 CD 分数，表明其对不完整笔画输入具有较强鲁棒性。

### 动画稳定性与应用鲁棒性

绑定后的动画稳定性通过自动蒙皮工具将网格绑定到生成骨架后进行验证。Figure 8 的定性演示表明，Stroke3D 生成的骨骼‑网格对在动画过程中保持了一致的运动学特性，未出现网格撕裂或关节脱离等退化现象。

在真实用户笔画场景下，Figure 11 展示了 Canvas Tool 的生成结果，验证了三项关键鲁棒性：
1. **噪声鲁棒性**：即使笔画存在抖动或扰动，几何保真度仍得以保持；
2. **视角无关性**：支持任意相机视角的生成；
3. **罕见概念泛化**：成功将训练中未见的“Samurai”和“Turtle”等分布外概念提升为可绑定的 3D 模型。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_VgOWxor3LV/figures/018_Figure_11.jpg]]
*Figure 11: Qualitative evaluation of generation robustness using our Canvas Tool. We present results generated from real-world 2D strokes to validate practical usability. The results demonstrate that Stroke3D is (1) robust to input noise, preserving geometric fidelity even with perturbed or jittery strokes; (2) view-invariant, supporting generation from arbitrary camera angles; and (3) generalizable to rare concepts, successfully lifting complex, out-of-distribution subjects (e.g., ’Samurai’, ’Turtle’) into rigged 3D models*

### 失败模式与局限性

尽管 Stroke3D 在多数指标上取得了最优结果，但分析揭示了以下瓶颈：

- **姿态多样性不足**：训练数据覆盖的姿态空间有限，导致罕见类别（如武士、乌龟）的生成结果存在不稳定性（Figure 11 虽展示成功案例，但作者承认该问题普遍存在）。
- **视角模糊性**：当 2D 笔画存在侧视图导致的关节重叠时，生成质量下降。Table 6 中部分类别的 CD₂D 指标虽有改善，但未完全解决该问题。
- **数据瓶颈**：训练数据集的规模和类别覆盖度是最主要的性能约束。作者明确承认可能存在类别分布偏见，但未量化其影响。
- **两阶段解耦**：当前框架尚未实现端到端的文本到绑定网格生成，骨架生成与网格合成仍为独立阶段。

### 关键图表索引

| 图表 | 核心结论 |
|------|----------|
| Table 1 | 骨架生成 CD 指标全面最优（CD‑J2J All 0.048） |
| Table 2 | 网格生成 SKA 评分最优（Mean Inst 87.83，+7.4 vs SKDream） |
| Figure 7 | Jxy 结构条件显著加速训练收敛 |
| Table 3 | SKA‑DPO 边际 0.1 取得最佳 Mean Inst/Class 权衡 |
| Figure 11 | 真实笔画场景下具备噪声鲁棒性、视角无关性和罕见概念泛化能力 |
| Figure 9 | 对不完整关节输入保持低 CD，验证输入鲁棒性 |

## 定位与知识库关联

### 1. 任务定位与核心差异

Stroke3D 解决的是一个“从非专业用户输入到可动画3D资产”的生成问题，其输入是2D笔画和文本描述，输出是带骨骼绑定（rigging）的3D网格。这与现有工作的核心差异在于**控制模态**和**生成粒度**。

现有骨架生成或绑定方法大致分为两类：
- **基于3D网格输入的方法**，如 **RigNet**（Xu et al., SIGGRAPH 2020），需要完整的3D网格作为输入来预测骨架，不面向非专业用户。
- **基于文本或自回归生成的方法**，如 **SKDream**（Xu et al., CVPR 2025 Highlight）、**MagicArticulate**（Song et al., CVPR 2025）和 **UniRig**（Zhang et al., SIGGRAPH 2025）。这些方法从文本描述直接生成骨架，但文本对空间拓扑和姿态的描述存在固有模糊性——同一文本可对应多种合理的骨架结构，这是该路线的核心瓶颈。

Stroke3D 的定位是**引入2D笔画作为结构条件（Jxy）**，在文本引导的基础上提供了显式的拓扑和姿态约束，从而消除了文本到骨架的结构模糊性。这一设计将用户控制从“语义描述”推进到“空间图解”，同时保持了非专业用户的可操作性。

### 2. 方法谱系中的技术继承与改进

Stroke3D 是一个两阶段框架，每一阶段都有明确的技术继承关系和针对性改进。

**骨架生成阶段**建立在图神经网络和扩散模型的交叉点上。其图变分自编码器（Sk-VAE）采用了 **GCN**（Kipf & Welling, ICLR 2017）和 **TransformerConv**（Shi et al., 2020）处理图结构数据，将骨架图的关节坐标和边拓扑编码到连续隐空间。在此基础上，**Skeletal Graph DiT（Sk-DiT）**沿用了 **DiT**（Peebles & Xie, ICCV 2023）的扩散变压器架构设计，但将标准自注意力层替换为TransformerConv以适应图结构输入。这一技术路线与SKDream等基于扩散的骨架生成方法同源，但关键区别在于条件机制：Sk-DiT以2D笔画坐标Jxy和边拓扑E作为显式条件注入去噪过程，而非仅依赖文本嵌入。

**网格生成阶段**直接以 **SKDream** 作为基础模型进行微调，但引入了两个关键改进槽位：
- **训练数据增强（TextuRig）**：原SKDream数据集存在纹理缺失和骨骼标注不完整的问题（如Figure 6所示，部分鸟类的骨架标注质量低甚至不完整）。TextuRig通过纹理筛选和视觉语言模型（VLM）重述，构建了更高质量的训练样本。
- **偏好优化（SKA-DPO）**：在监督微调之后，引入基于骨架-网格对齐分数（SKA Score）的偏好优化策略。其优化目标沿用了 **Diffusion-DPO** 的范式，但以SKA分数作为奖励信号来构建偏好对，鼓励模型在几何保真度上向高对齐样本倾斜。消融实验（Table 3）表明，偏好分数边际设为0.1时在实例级和类别级SKA分数上取得最佳权衡。

### 3. 与基线方法的定量关系

在骨架生成任务上，Stroke3D在Chamfer Distance的所有三个指标（CD-J2J、CD-J2B、CD-B2B）上均取得最低误差（Table 1）。以全类别CD-J2J为例，Stroke3D达到0.048，显著优于SKDream（0.111）、RigNet（0.150）、MagicArticulate（0.128）和UniRig（0.098）。这一优势在细粒度类别（Table 5：Mythical、Toy、Weapon）上同样保持，验证了2D笔画条件在跨类别泛化中的有效性。

在网格生成任务上，结合TextuRig和SKA-DPO后，Stroke3D的Mean Inst SKA分数达到87.83，比SKDream基线（80.43）提升了约7.4分；Mean Class SKA分数达到84.36，提升了约10分（Table 2）。与基于扩散模型编辑的 **SDEdit**（Meng et al., ICLR 2022）相比，优势更为显著。

### 4. 适用边界与已知局限

Stroke3D的有效性受以下边界条件约束：

- **数据覆盖瓶颈**：模型性能直接受限于训练数据的规模和姿态多样性。这是作者明确指出的最主要瓶颈。罕见概念（如“Samurai”、“Turtle”）虽能泛化（Figure 11），但生成不稳定，说明模型对分布外概念的鲁棒性有限。
- **笔画模糊性敏感**：当2D笔画存在视角模糊性（如侧视图导致关节重叠）时，生成质量下降。模型虽对输入噪声有一定鲁棒性（Figure 9展示了部分关节随机丢弃时仍保持较低CD分数），但对系统性歧义的应对能力不足。
- **两阶段框架的局限性**：当前为骨架生成和网格生成分离的两阶段管线，尚未实现端到端的文本到绑定网格生成。这意味着两阶段的误差可能累积，且用户无法在网格阶段直接修正骨架错误。
- **类别分布偏见**：作者承认训练数据可能存在类别分布偏见，但未进行具体评估或量化。这是一个需要后续验证的潜在公平性问题。

### 5. 开放问题与后续方向

从论文的局限性和分析中可提炼出以下开放问题：

- **数据规模扩展**：如何扩大数据集规模并引入更多样化的骨架姿态以解决数据瓶颈？作者提及可能利用更大规模的Articulation-XL数据集，但具体方案尚未探索。
- **端到端生成**：能否开发端到端网络直接从文本和笔画生成绑定网格，减少两阶段间的信息损失和误差累积？
- **视角鲁棒性**：如何处理笔画的视角模糊性并提高对侧视图等困难情况的鲁棒性？这可能需要在条件编码中显式建模相机参数或引入多视图一致性约束。
- **控制粒度细化**：当前2D笔画仅约束骨架拓扑和关节位置，未来是否可扩展到对网格形状、纹理或蒙皮权重的直接控制？

### 6. 知识库定位总结

Stroke3D 在3D资产生成领域占据了“**用户友好型可控生成**”这一生态位。它不追求从零开始的完全自动生成（如纯文本到3D的方法），也不假设用户具备3D建模专业知识（如需要完整网格输入的绑定方法），而是在两者之间开辟了一条以2D笔画为桥梁的中间路线。其技术贡献——图VAE与扩散变压器的结合、结构条件注入机制、以及基于对齐分数的偏好优化——为后续研究提供了可复用的模块和明确的改进方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Stroke3D_Lifting_2D_strokes_into_rigged_3D_model_via_latent_diffusion_models.pdf]]
