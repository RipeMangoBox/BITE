---
title: "GenZI: Zero-Shot 3D Human-Scene Interaction Generation"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/GenZI_Zero_Shot_3D_Human_Scene_Interaction_Generation.pdf
project_link: null
code_link: null
aliases:
- GenZI
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 从大型视觉-语言模型（VLMs）中蒸馏出丰富的2D人-场景组合先验知识，以替代对3D交互数据的依赖。
primary_logic: VLM在2D图像中能够生成合理的交互假设；通过鲁棒的多视图3D提升，可将这些2D假设转化为3D空间中符合场景上下文的交互，从而完全绕过对3D交互训练数据的需求。
claims:
- GenZI是首个零样本3D人-场景交互生成方法，无需任何3D交互数据训练。
- 动态掩码机制能够自动生成补绘区域，无需人工标注。
- 用户研究显示，GenZI的生成质量显著优于对比方法，选择偏好率超过87%。
- 消融实验证明，动态掩码（DM）、视图一致性（VC）和迭代细化（IR）三个模块对最终合成质量均有重要贡献。
---

# GenZI: Zero-Shot 3D Human-Scene Interaction Generation

> [!tip] 核心洞察
> VLM在2D图像中能够生成合理的交互假设；通过鲁棒的多视图3D提升，可将这些2D假设转化为3D空间中符合场景上下文的交互，从而完全绕过对3D交互训练数据的需求。

| 字段 | 内容 |
|------|------|
| 中文题名 | GenZI：零样本三维人-场景交互生成 |
| 英文题名 | GenZI: Zero-Shot 3D Human-Scene Interaction Generation |
| 会议/期刊 | CVPR 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | GenZI |
| Dataset | Sketchfab数据集 |

> [!tip] 效果简介
> - Sketchfab数据集 上，用户偏好率（二选一） >87% vs 对比所有基线，具体数值见图4 (显著领先)；平均真实感评分（1-5） 3.6 vs 所有基线得分较低，详见图4 (最高)；CLIP（语义一致性） 0.2710 vs COINS、Hassan et al.、Ours-SV，具体值见表1 (最佳)。

## 概要

在三维场景中生成逼真的人-场景交互是虚拟现实、具身智能等领域的核心需求。然而，这一任务长期受困于一个根本瓶颈：现有方法依赖大规模、多样化的3D人-场景交互数据进行监督学习，而此类数据的采集与标注极其困难且昂贵，严重限制了方法的泛化能力。**COINS**（Zhao et al., ECCV 2022）等代表性工作虽然取得了进展，但仍被束缚于封闭的交互类别集合和室内场景假设，难以拓展到开放场景。

GenZI 针对这一瓶颈提出了一个范式转换式的解决方案：**从大型视觉-语言模型（VLMs）中蒸馏丰富的2D人-场景组合先验知识，完全替代对3D交互训练数据的依赖**。其核心洞察在于，VLM在2D图像中已经习得了合理的人-场景交互语义空间——例如，它能“理解”一个人应当在椅子附近“坐下”而非“漂浮”在半空。GenZI通过鲁棒的多视图3D提升，将这些2D假设转化为3D空间中符合场景上下文的交互，从而首次实现了零样本3D人-场景交互生成，无需任何3D交互数据训练。

方法上，GenZI构建了三个关键创新模块构成的技术管线：首先，**动态掩码补绘**利用扩散模型的交叉注意力图自动生成补绘区域，无需人工标注即可在多视角渲染图像中合成2D人-场景组合；其次，**鲁棒3D提升**通过同时优化姿态参数与视图一致性权重，自适应聚焦于一致视图，解决了多视图2D假设可能相互矛盾的问题；最后，**迭代细化**以当前生成的3D人体剪影作为更精确的掩码，重新进行补绘与提升，逐步提高人-场景的空间一致性。

实验验证了该方法的有效性。在Sketchfab数据集上的用户研究表明，参与者对GenZI生成结果的偏好率超过87%，平均真实感评分达3.6/5，显著优于所有对比基线。消融实验进一步证实，动态掩码、视图一致性和迭代细化三个模块对最终合成质量均有重要贡献——去除任一模块都会导致人体漂浮、穿模或语义一致性下降等典型失效模式。

GenZI的局限性同样值得关注。其生成能力受限于潜在扩散模型的补绘能力上限，难以处理复杂的2D人-场景组合，且扩散模型的迭代推理过程导致速度较慢。此外，方法依赖第三方2D姿态估计器的精度，并需要手动指定交互的大致位置点，尚不能处理需要自由空间推理的复杂交互。这些限制为未来的改进指明了方向。



三维人-场景交互生成（3D Human-Scene Interaction Generation）旨在将虚拟人体自然地置入给定的三维环境中，使其与场景物体产生合理、语义一致的交互。这一任务在虚拟现实、游戏开发、影视制作和具身人工智能等领域具有广泛的应用前景。然而，现有方法面临一个根本性的瓶颈：**对大规模、多样化的3D人-场景交互数据的严重依赖**。

具体而言，以 **COINS**（Zhao et al., ECCV 2022）为代表的组合式合成方法和以 **Hassan et al.**（Hassan et al., ICCV 2019）为代表的场景约束姿态估计方法，均需要在类似PROX这样的3D交互数据集上进行监督训练。这类数据的采集和标注过程极其困难且昂贵——它要求同时捕获高质量的三维场景几何、精确的人体运动以及两者之间的细粒度接触关系。由此带来的后果是，现有方法的泛化能力受到严重制约：当面对训练集中未曾出现的场景类型、物体几何或交互动作时，合成质量往往急剧下降（Figure 5）。

这一困境的核心矛盾在于：**3D交互数据的稀缺性**与**真实世界场景的无限多样性**之间的鸿沟。如果能绕过对3D交互训练数据的直接需求，转而从更易获取的信号源中提取交互先验，就有可能从根本上打破这一瓶颈。

GenZI的动机正源于此。其核心洞察是：大型视觉-语言模型（VLMs）在海量互联网图文数据上预训练后，已经习得了丰富的2D人-场景组合语义空间——它们能够“想象”出一个合理的人体在给定场景图像中应如何出现。如果能将这些2D交互假设鲁棒地提升到3D空间，就可以完全绕过对3D交互训练数据的需求，实现**零样本**（zero-shot）的三维人-场景交互生成。正如论文所述，GenZI是首个无需任何3D交互数据训练的零样本方法（Abstract）。



## 核心方法与创新机理

GenZI 的核心创新在于**完全绕过了对 3D 人-场景交互训练数据的依赖**，转而从大型视觉-语言模型中蒸馏出丰富的 2D 交互先验知识，并通过鲁棒的多视图 3D 提升将其转化为与场景上下文一致的 3D 交互。这一范式转变通过三个关键的 changed slots 得以实现。

### 从 3D 监督到 2D 先验蒸馏：训练数据需求的根本性改变

现有方法（如 **COINS** (Zhao et al., ECCV 2022) 和 **Hassan et al.** (ICCV 2019)）需要大规模、多样化的 3D 人-场景交互数据（如 PROX 数据集）进行监督学习，而此类数据的采集和标注极其困难且昂贵，严重限制了方法的泛化能力。

GenZI 将这一依赖彻底消除：**训练数据需求从“需要大量 3D 交互数据”变为“零样本，无需任何 3D 交互数据”**。其因果机制在于，大型视觉-语言模型在 2D 图像中已经学会了丰富的人-场景组合语义空间，能够生成合理的交互假设。GenZI 通过在多视图渲染图像上进行潜在扩散补绘，将这些 2D 假设蒸馏出来，再通过鲁棒优化提升到 3D，从而完全绕过了对 3D 交互训练数据的需求。这一设计使得方法对任意类型的 3D 场景具有天然的泛化能力。

### 动态掩码机制：补绘掩码生成方式的自动化

传统补绘方法通常需要手动指定掩码区域或使用固定随机掩码，这不仅依赖人工标注，也难以适应多样化的场景几何和交互需求。

GenZI 将**补绘掩码生成从“手动指定”变为“基于扩散模型交叉注意力图的全自动动态掩码”**。具体而言，该方法利用潜在扩散模型去噪过程中生成的交叉注意力图，自动定位文本提示所对应的感兴趣区域，并在去噪过程中动态更新掩码。这一机制使得 2D 人-场景组合的合成无需任何人工干预，同时掩码能够自适应地调整到合理的补绘位置，为后续的多视图 3D 提升提供了高质量的 2D 假设。

### 鲁棒多视图 3D 提升：从平均约束到自适应视图一致性

单视图方法（如 Hassan et al.）仅能利用单一视角的姿态信息进行 3D 拟合，而简单的多视图平均约束则可能被不一致的 2D 假设所污染，导致姿态平均化、表现力下降。

GenZI 将**多视图 3D 提升策略从“单视图拟合或平均多视图约束”变为“同时优化姿态参数和视图一致性权重的鲁棒优化”**。其核心是引入视图选择权重 $w^i$，在姿态拟合能量函数中自适应地聚焦于与 3D 姿态最一致的 2D 假设视图：

$$\xi_{\mathrm{PF}} = \frac{\sum_i w^i \sum_j \mathbf{c}_j^i \rho(\Pi(\hat{\mathbf{J}})_j^i - \mathbf{J}_j^i)}{\sum_i w^i}$$

其中 $\rho$ 为 Geman-McClure 鲁棒核函数，$\mathbf{c}_j^i$ 为关节置信度。配合视图选择正则化 $\mathcal{E}_{\mathrm{VS}} = \max(\tau - \sum_i w^i, 0)$ 鼓励至少选择 $\tau$ 个视图，该优化策略能够有效抑制不一致视图的干扰，同时保持足够的多视图约束来生成表现力强的 3D 姿态。

### 迭代细化：从开放补绘到剪影引导的闭环优化

GenZI 进一步引入迭代细化策略，将初步生成的 3D 人体剪影作为更精确的掩码，重新输入潜在扩散补绘，形成“2D 补绘 → 3D 提升 → 剪影引导再补绘”的闭环。这一机制替代了初始的动态掩码，提供了与当前 3D 姿态高度一致的补绘区域，逐步提高 2D 假设与 3D 结果之间的一致性。

消融实验（Table 2 和 Figure 6）证实，动态掩码（DM）、视图一致性（VC）和迭代细化（IR）三个模块对最终合成质量均有重要贡献：去除 DM 会导致语义一致性下降，人体与场景脱节；去除 VC 会导致姿态平均化；去除 IR 则会导致人体穿模。三者协同作用，使得 GenZI 在无需任何 3D 交互训练数据的前提下，实现了优于监督基线的生成质量。



GenZI 的整体流水线遵循“蒸馏–提升–细化”的三阶段范式，其核心思路是将大型视觉语言模型（VLM）在 2D 空间中习得的丰富交互先验，通过鲁棒的多视图几何一致性约束，提升为 3D 空间中符合场景上下文的参数化人体。

**输入与输出。** 流水线接收三类输入：任意三维场景 $S$、描述期望交互的简短文本提示 $\Gamma$，以及场景中交互发生的大致位置点 $\mathbf{p} \in \mathbb{R}^3$。输出为 SMPL-X 参数化的人体模型 $(\mathbf{R}, \mathbf{t}, \Theta, \Phi)$，分别对应全局朝向、全局平移、VPoser 隐空间中的身体姿态以及身体形状混合系数（Section 3.1）。

**第一阶段：多视图 2D 交互假设生成。** 系统首先在位置 $\mathbf{p}$ 周围随机采样 $k = 16$ 个虚拟相机，相机分布于半球面上并经过 $\mathbf{p}$ 的可见性过滤，渲染得到 $k$ 幅场景 RGB 图像（Section 3.2）。随后，利用潜在扩散模型对每幅渲染图像执行文本条件补绘，生成与提示 $\Gamma$ 相符的 2D 人体。此过程的核心创新在于**动态掩码机制**：无需人工指定补绘区域，而是从扩散模型的交叉注意力图 $\mathbf{A} \in \mathbb{R}^{hw \times n}$ 中自动提取与文本实体（如“person”）相关的空间激活区域，并在去噪过程中自适应更新掩码，使补绘人体自然融入场景上下文（Figure 3）。

**第二阶段：鲁棒多视图 3D 提升。** 对补绘后的 $k$ 幅图像，使用 AlphaPose 估计 2D 关节位置 $\mathbf{J}^i$ 及置信度 $\mathbf{c}^i$。然后通过最小化总能量函数 $\mathcal{E}_{\mathrm{total}}$ 来优化 SMPL-X 参数，该函数由六项加权组成（Formula 1）：

$$
\mathcal{E}_{\mathrm{total}} = \lambda_{\mathrm{PF}} \mathcal{E}_{\mathrm{PF}} + \lambda_{\mathrm{VS}} \mathcal{E}_{\mathrm{VS}} + \lambda_{\mathrm{BP}} \mathcal{E}_{\mathrm{BP}} + \lambda_{\mathrm{BS}} \mathcal{E}_{\mathrm{BS}} + \lambda_{\mathrm{SC}} \mathcal{E}_{\mathrm{SP}}
$$

其中，$\mathcal{E}_{\mathrm{PF}}$ 为鲁棒姿态拟合项，它引入视图一致性权重 $w^i$ 和 Geman-McClure 鲁棒核 $\rho$，使得优化过程能自适应聚焦于多视图间最一致的 2D 假设，抑制不一致视图的干扰（Formula 2）。$\mathcal{E}_{\mathrm{VS}}$ 则通过 $\max(\tau - \sum_i w^i, 0)$ 鼓励至少选择 $\tau$ 个视图，防止权重退化（Formula 3）。其余项分别为 VPoser 身体姿态先验 $\mathcal{E}_{\mathrm{BP}}$、形状马氏距离先验 $\mathcal{E}_{\mathrm{BS}}$，以及基于 SDF 的场景穿透约束 $\mathcal{E}_{\mathrm{SC}}$（Formula 4–6）。这一鲁棒优化策略是 GenZI 区别于简单平均多视图约束的核心差异点。

**第三阶段：迭代细化。** 将初步优化得到的 3D 人体渲染为各视角下的剪影，以此作为比动态掩码更精确、更一致的补绘掩码，重新执行潜在扩散补绘和 3D 提升。此迭代过程（Section 3.4）逐步消除初始阶段可能存在的 2D-3D 不一致，有效缓解人体与场景的穿模问题。消融实验证实，去除迭代细化（IR）后合成质量显著下降，人体会出现穿透场景物体的现象（Table 2, Figure 6）。

**与已有范式的根本差异。** 传统方法（如 **COINS** [Zhao et al., ECCV 2022] 和 **Hassan et al.** [ICCV 2019]）依赖大规模 3D 人-场景交互数据（如 PROX 数据集）进行监督学习，其泛化能力受限于训练数据的规模和多样性。GenZI 通过从 VLM 蒸馏 2D 组合先验，完全绕过了对 3D 交互训练数据的需求，实现了零样本生成。这一范式转变使得系统能够处理任意类型的 3D 场景和开放词汇的文本描述，而不再受限于封闭的交互类别集合。

### 补充图表

![[assets/figures/papers/paper_list_l1714_GenZI_Zero_Shot_3D_Human_Scene_Interaction_Generation/figures/001_Figure_1.jpg]]
*Figure 1: Given an arbitrary 3D scene, GenZI can synthesize virtual humans interacting with the 3D environment at specified locations from a brief text description. Our approach does not require any 3D human-scene interaction training data or 3D learning. By distilling interaction priors from powerful 2D vision-language models, we optimize for 3D human-scene interaction synthesis in a flexible fashion, with simple language-based control and high generality to various types of scene environments*

![[assets/figures/papers/paper_list_l1714_GenZI_Zero_Shot_3D_Human_Scene_Interaction_Generation/figures/002_Figure_2.jpg]]
*Figure 2: GenZI distills information from vision-language model for 3D human-scene interaction. We first leverage large vision-language models to synthesize possible 2D humans interactions with the 3D scene S by employing latent diffusion inpainting [34] on multiple rendered views of the environment at location p using our dynamic masking scheme to automatically estimate inpainting masks. We then lift these 2D hypotheses to 3D in a robust optimization for a 3D parametric body model B (SMPL-X [29]) that is most consistent with detected 2D poses in the inpainted 2D hypotheses. This produces a semantically consistent interaction that respects the scene context, without requiring any 3D human-scene inter...*



GenZI 的生成流程由四个核心模块串联而成，形成“2D 先验蒸馏 → 3D 鲁棒提升 → 迭代细化”的闭环。

**多视角场景渲染**：给定交互中心点 $\mathbf{p} \in \mathbb{R}^3$，在半球面上随机采样 $k=16$ 个虚拟相机，并过滤掉 $\mathbf{p}$ 被遮挡的视角，渲染对应的场景 RGB 图像。该模块为后续 2D 补绘提供多视角的场景上下文。

**动态掩码补绘**：这是 GenZI 从 VLM 中蒸馏交互先验的关键环节。传统补绘需要手动指定掩码区域，而 GenZI 利用潜在扩散模型在去噪过程中生成的交叉注意力图 $\mathbf{A} \in \mathbb{R}^{hw \times n}$（其中 $h$、$w$ 为特征图空间维度，$n$ 为文本提示的 token 数），自动定位与交互文本相关的图像区域，动态生成补绘掩码 $\mathbf{M}$。形式上，扩散模型执行 $\varOmega(\mathbf{z}_t, \mathbf{M}, \mathbf{I}, T, t)$，从带噪潜变量 $\mathbf{z}_t$ 出发，在时间步 $t$ 依据掩码 $\mathbf{M}$、场景图像 $\mathbf{I}$ 和文本提示 $T$ 进行去噪补绘。该方案完全免除了人工标注掩码的需求，使系统能够自动适应不同场景和交互类型。

**2D 姿态估计**：对补绘后的多视图图像，使用 AlphaPose 提取 2D 关节位置 $\mathbf{J}^i$ 及对应的置信度分数 $\mathbf{c}^i$，为后续 3D 提升提供观测约束。

**鲁棒 3D 提升**：将多视图 2D 姿态假设提升为 SMPL-X 参数化人体 $(\mathbf{R}, \mathbf{t}, \Theta, \Phi)$，其中 $\mathbf{R}$ 为全局朝向，$\mathbf{t}$ 为全局平移，$\Theta$ 为 VPoser 隐空间中的身体姿态参数，$\Phi$ 为身体形状混合系数。优化目标为以下总能量函数的最小化：

$$
\mathcal{E}_{\mathrm{total}} = \lambda_{\mathrm{PF}} \mathcal{E}_{\mathrm{PF}} + \lambda_{\mathrm{VS}} \mathcal{E}_{\mathrm{VS}} + \lambda_{\mathrm{BP}} \mathcal{E}_{\mathrm{BP}} + \lambda_{\mathrm{BS}} \mathcal{E}_{\mathrm{BS}} + \lambda_{\mathrm{SC}} \mathcal{E}_{\mathrm{SC}} + \lambda_{\mathrm{SP}} \mathcal{E}_{\mathrm{SP}}
$$

各能量项含义如下：

- **姿态拟合能量** $\mathcal{E}_{\mathrm{PF}}$：核心数据项。引入视图一致性权重 $w^i$ 和 Geman-McClure 鲁棒核函数 $\rho$，将 3D 关节投影与 2D 检测关节的加权误差最小化：

$$
\xi_{\mathrm{PF}} = \frac{\sum_i w^i \sum_j \mathbf{c}_j^i \rho(\Pi(\hat{\mathbf{J}})_j^i - \mathbf{J}_j^i)}{\sum_i w^i}
$$

其中 $\Pi(\hat{\mathbf{J}})_j^i$ 为 3D 关节 $\hat{\mathbf{J}}$ 在第 $i$ 个视图的投影，$\mathbf{J}_j^i$ 和 $\mathbf{c}_j^i$ 分别为该视图中第 $j$ 个关节的 2D 检测位置与置信度。视图权重 $w^i$ 由优化器自动学习，使系统自适应聚焦于 2D 假设一致的视图，抑制不一致视图的干扰。

- **视图选择正则化** $\mathcal{E}_{\mathrm{VS}}$：鼓励优化器至少选择 $\tau$ 个有效视图，避免退化为单视图解：

$$
\mathcal{E}_{\mathrm{VS}} = \max(\tau - \sum_i w^i, 0)
$$

- **身体姿态先验** $\mathcal{E}_{\mathrm{BP}}$：结合 VPoser 隐空间的正则化与关节角度约束，防止生成不自然的姿态：

$$
\mathcal{E}_{\mathrm{BP}} = \|\Theta\|^2 + \mathcal{E}_{\mathrm{JA}}(\hat{\Theta})
$$

- **身体形状先验** $\mathcal{E}_{\mathrm{BS}}$：通过马氏距离约束形状参数保持在合理范围内：

$$
\mathcal{E}_{\mathrm{BS}} = \|\Phi\|^2
$$

- **场景穿透约束** $\mathcal{E}_{\mathrm{SC}}$：利用场景的 SDF 函数 $\varPsi(\mathbf{v})$ 避免人体顶点 $\mathbf{v} \in \mathbf{V}$ 穿入场景物体。当所有顶点均在场景外部时，惩罚最小 SDF 值；否则，惩罚所有穿入顶点的 SDF 绝对值之和：

$$
\mathcal{E}_{\mathrm{SC}} = \begin{cases} \min_{\mathbf{v} \in \mathbf{V}} \varPsi(\mathbf{v}), & \varPsi(\mathbf{v}) > 0 \ \forall \mathbf{v} \in \mathbf{V} \\ \sum_{\mathbf{v} \in \mathbf{V}} |\min(\varPsi(\mathbf{v}), 0)|, & \text{otherwise} \end{cases}
$$

- **自穿透约束** $\mathcal{E}_{\mathrm{SP}}$：防止人体各部位之间的相互穿透，具体形式原文未展开，但其作用是标准的人体网格自交惩罚项。

**迭代细化**：初始 3D 提升结果仍可能存在视图不一致或穿模问题。GenZI 以当前生成的人体剪影作为新的补绘掩码 $\mathbf{M}$，替代动态掩码，重新执行潜在扩散补绘和 3D 提升。这一闭环迭代使得 2D 补绘与 3D 优化相互促进，逐步提升交互的语义合理性与空间一致性。消融实验证实，去除该模块会导致人体穿模，合成质量显著下降（Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l1714_GenZI_Zero_Shot_3D_Human_Scene_Interaction_Generation/figures/003_Figure_3.jpg]]
*Figure 3: Human inpainting with dynamic masking. Top: Given a scene image and a text prompt, a human is inpainted into the image without a mask specifying the inpainting region for latent diffusion. Bottom: The masks generated by our dynamic masking scheme based on cross-attention maps at different diffusion time steps adaptively shift to find the region of interest*



## 实验与关键发现

### 零样本生成能力与实验设置

为验证GenZI的零样本3D人-场景交互生成能力，作者构建了基于Sketchfab数据集的评估基准。该基准包含8个大规模、多样化的3D场景（涵盖室内外环境），并设计了38种交互动作提示。这一设置的核心挑战在于：GenZI在训练阶段从未接触任何3D人-场景交互数据，其全部先验知识均从大型视觉-语言模型（VLM）的2D补绘中蒸馏而来。实验对比了三类基线方法：**COINS**（Zhao et al., ECCV 2022）——一种依赖语义标签控制的组合式交互合成方法；**Hassan et al.**（ICCV 2019）——基于场景约束的单视图3D姿态估计方法；以及GenZI的单视图消融版本**Ours-Single View**。评估指标涵盖语义一致性（CLIP分数）、生成多样性（多样性熵）、非碰撞分数和接触分数四个维度。

### 主观评估：用户偏好显著领先

用户研究从两个维度展开：二选一偏好测试（binary study）和1-5分真实感评分（unary study）。在二选一测试中，参与者被要求从GenZI与某个基线的生成结果中选择更真实、更符合语义的交互。结果表明，**GenZI的选择偏好率超过87%**（Figure 4），在所有对比中均取得压倒性优势。在真实感评分中，GenZI获得**3.6的平均分**，为所有方法中最高。这一主观优势的根源在于两个机制级联：动态掩码补绘确保了2D人体与场景的语义适配，而鲁棒多视图3D提升则避免了单视图方法常见的姿态-场景割裂。

![[assets/figures/papers/paper_list_l1714_GenZI_Zero_Shot_3D_Human_Scene_Interaction_Generation/figures/004_Figure_4.jpg]]
*Figure 4: User study of 3D human-scene interaction synthesis on the Sketchfab dataset, where participants show a strong preference for the generations by our approach, in comparison with all baselines, COINS [51], Hassan et al. [10], and Ours-Single View*

### 客观指标：语义一致性与物理合理性兼顾

Table 1汇总了定量对比结果。GenZI在语义一致性（CLIP分数0.2710）、多样性熵和非碰撞分数三项指标上均取得最佳。值得注意的是，接触分数与基线持平，这并非劣势——由于GenZI无需3D交互数据训练，其接触行为完全由VLM先验驱动，持平本身证明了蒸馏策略的有效性。单视图方法（Hassan et al.和Ours-SV）虽在多样性熵上表现较高，但这是以牺牲语义合理性为代价的：缺乏多视图约束导致姿态估计随机性增大，生成结果与场景脱节（Figure 5定性结果佐证了这一点）。COINS因依赖封闭的⟨动作，物体⟩标签集，在面对训练分布外的场景物体（如曲面桥面、异形椅子）时合成质量显著退化。

### 消融实验：三个模块的因果贡献

Table 2和Figure 6系统拆解了动态掩码（DM）、视图一致性（VC）和迭代细化（IR）三个模块的因果效应。去除动态掩码后，语义一致性下降最为显著——补绘区域无法自动适配场景几何，导致生成的人体与场景语义脱节，出现“漂浮”现象（Figure 6中人物悬浮于吧台椅上方）。去除视图一致性权重后，3D姿态趋于多视图的平均化，丧失了表现力，因为优化器无法自适应地聚焦于一致视图而被迫折中。去除迭代细化后，穿模问题凸显：初始生成的人体剪影不够精确，缺乏第二轮补绘的修正，导致身体网格穿透场景物体（Figure 6中人物穿入吧台椅）。三个模块的消融结果共同验证了管线设计的必要性：DM负责2D语义适配，VC保证3D一致性，IR消除物理穿透。

### 失败模式与局限性

尽管GenZI在零样本设定下表现优异，其性能上限受制于两个外部组件。第一，**潜在扩散模型的补绘能力边界**：对于超出VLM训练分布的复杂人-场景组合（如非典型姿态或罕见物体交互），2D补绘可能产生不合理的假象，进而污染3D提升结果。第二，**2D姿态估计器的精度瓶颈**：GenZI依赖AlphaPose提取多视图2D关节，当补绘图像存在严重遮挡或模糊时，姿态估计误差会通过鲁棒优化的权重机制传播，导致3D姿态扭曲。此外，当前方法需要手动指定交互的大致位置点p，无法处理需要自由空间推理的交互场景。扩散模型的迭代推理也限制了实时应用的可能性。

### 补充图表

![[assets/figures/papers/paper_list_l1714_GenZI_Zero_Shot_3D_Human_Scene_Interaction_Generation/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons on the Sketchfab dataset. Our approach achieves the best semantic consistency, diversity entropy, and non-collision scores, with the contact score on par. Note that single view methods Hassan et al. [10] and Ours-SV tend to produce increased diversity at the cost of semantic plausibility*

![[assets/figures/papers/paper_list_l1714_GenZI_Zero_Shot_3D_Human_Scene_Interaction_Generation/figures/007_Table_2.jpg]]
*Table 2: Ablation study on the Sketchfab dataset. The semantic consistency of 3D interaction generations degrades without dynamic masking (DM), view consistency (VC), or iterative refinement (IR), compared to our full approach*

![[assets/figures/papers/paper_list_l1714_GenZI_Zero_Shot_3D_Human_Scene_Interaction_Generation/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of our method ablations on Sketchfab dataset for the input text: “sitting on a bar stool”. Without dynamic masking (DM) or view consistency (VC), the person floats above the middle stool. Without iterative refinement (IR), the person penetrates the stool. Our full approach results in a more realistic synthesis*

![[assets/figures/papers/paper_list_l1714_GenZI_Zero_Shot_3D_Human_Scene_Interaction_Generation/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative results on the Sketchfab dataset. Our GenZI synthesizes more realistic 3D human-scene interactions and generalizes better across diverse scene types, compared to the baselines COINS [51], Hassan et al. [10], and Ours-Single View. For COINS, we show the used ⟨action, object⟩ labels from its closed set of indoor interactions; its closed setting can lead to degraded results from out-ofdistribution object classes (e.g., curved bridge deck as the floor, chair at a different height or shape than those in the training set)*



## 定位与知识库关联

### 核心定位：零样本3D人-场景交互生成

GenZI 的核心贡献在于开辟了一条完全绕过3D交互数据依赖的技术路径。在3D人-场景交互生成领域，传统方法普遍受制于一个根本瓶颈：大规模、多样化的3D交互数据采集和标注极其困难且昂贵，这严重限制了模型的泛化能力。GenZI 的因果操纵变量是从大型视觉-语言模型（VLMs）中蒸馏出丰富的2D人-场景组合先验知识，以替代对3D交互数据的依赖。其核心洞察在于：VLM在2D图像中能够生成合理的交互假设；通过鲁棒的多视图3D提升，可将这些2D假设转化为3D空间中符合场景上下文的交互，从而完全绕过对3D交互训练数据的需求。

### 与基线方法的对比关系

GenZI 与现有工作的对比揭示了其方法论上的根本差异：

**COINS**（Zhao et al., ECCV 2022）代表了基于语义控制的组合式人-场景交互合成路线。该方法依赖预定义的⟨动作，物体⟩标签集合来指导生成，其封闭的交互类别设定在面对分布外物体类别时会产生退化结果——例如将弯曲的桥面识别为地板，或将非标准高度的椅子误判。GenZI 以开放式的文本提示替代了封闭标签集，从根本上解除了这一限制。

**Hassan et al.**（Hassan et al., ICCV 2019）采用场景约束进行3D人体姿态估计，但其方法本质上是单视图的，依赖单张图像中的场景几何信息来约束姿态。GenZI 的多视图鲁棒优化策略与之形成鲜明对比：通过同时优化姿态参数和视图一致性权重，GenZI 能够自适应地聚焦于一致的视图，而非平均化多视图约束。

**Ours-Single View** 是 GenZI 的单视图消融版本，其存在本身即揭示了多视图策略的关键价值。单视图方法倾向于产生更高的多样性，但这是以牺牲语义合理性为代价的——这一权衡在 Table 1 的定量结果中得到了明确体现。

### 方法谱系中的关键创新槽位

从方法设计的维度审视，GenZI 在三个关键槽位上实现了范式转换：

**训练数据需求**：从需要大量3D人-场景交互数据（如PROX数据集）进行监督训练，转变为零样本——无需任何3D交互数据，仅通过VLM蒸馏先验。这一转变的证据锚点明确：论文摘要中明确提出“Our approach does not require any 3D human-scene interaction training data or 3D learning”。

**补绘掩码生成**：从手动指定或使用固定随机掩码，转变为基于扩散模型交叉注意力图的全自动动态掩码。这一机制在去噪过程中自适应地更新掩码区域，使VLM能够在无需人工标注的情况下自动找到合理的2D人体补绘位置。

**多视图3D提升策略**：从单视图姿态拟合或平均多视图约束，转变为鲁棒优化——同时优化姿态参数和视图一致性权重，自适应聚焦于一致视图。这一策略通过引入视图选择正则化项 $\mathcal{E}_{\mathrm{VS}} = \max(\tau - \sum_i w^i, 0)$ 和鲁棒核函数 $\rho$ 来实现，有效处理了多视图2D假设不一致的问题。

### 适用边界与局限

GenZI 的适用边界由其技术架构的内在约束所定义：

**VLM能力的上限约束**：本方法受限于潜在扩散模型的补绘能力，难以想象复杂的2D人-场景组合。当文本提示描述的交互超出VLM在2D图像中见过的模式范围时，补绘质量会显著下降。此外，扩散模型的迭代性质导致推理速度较慢，限制了实时应用场景。

**2D姿态估计的精度依赖**：GenZI 依赖第三方2D姿态估计器（AlphaPose）的精度，估计误差可能通过3D提升过程传播并放大。这一依赖关系构成了一个信息瓶颈：2D姿态估计的质量直接决定了3D优化的上限。

**交互位置的手动指定**：需要手动指定交互的大致位置点 $\mathbf{p}$，这限制了方法处理需要自由空间推理的复杂交互的能力。当交互涉及大范围的空间移动或需要理解场景功能区域时，单一位置点不足以提供充分的约束。

### 开放问题

当前研究留下了若干值得探索的方向：

**动态掩码的鲁棒性边界**：动态掩码方案在处理严重遮挡或复杂场景几何时的表现尚不明确。当场景中存在多个可能的交互区域时，交叉注意力机制的选择行为需要更深入的分析。

**推理效率的优化空间**：如何降低扩散模型的推理延迟，实现实时或近实时应用，是一个具有实际价值的方向。可能的路径包括模型蒸馏、渐进式去噪或替代性的生成架构。

**VLM能力演进的红利**：未来更强大的VLM能否进一步提升补绘质量和交互多样性，这既是开放问题，也是该方法框架的潜在优势——GenZI 的零样本特性使其能够直接受益于底层VLM的进步，而无需重新训练。

**多视图不一致的处理瓶颈**：当多视图2D假设高度不一致时，鲁棒优化的性能瓶颈在哪里？视图选择权重机制在极端情况下的行为需要更系统的表征。

**扩展维度**：该方法能否扩展到多人交互或动态场景？当前框架假设单个静态人体与静态场景的交互，多人交互引入了人体间约束，动态场景则需要时序一致性建模。



## 原文 PDF

![[paperPDFs/CVPR_2024/GenZI_Zero_Shot_3D_Human_Scene_Interaction_Generation.pdf]]
