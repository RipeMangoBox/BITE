---
title: "ThemeStation: Generating Theme-aware 3D Assets From Few Exemplars"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/ThemeStation_Generating_Theme_aware_3D_Assets_From_Few_Exemplars.pdf
project_link: null
code_link: "https://github.com/3DTopia/ThemeStation"
aliases:
- ThemeStation
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 双分数蒸馏（DSD）中概念先验与参考先验在不同噪声级别上的解耦应用：高噪声用于概念布局与颜色，低噪声用于细节纹理与几何。
primary_logic: 预训练文本到图像扩散模型的反向扩散过程具有从粗到细的噪声级别动态，这与概念先验（全局布局/颜色）和参考先验（高频细节）的功能天然吻合，因此通过在不同去噪时间步施加不同先验可有效避免损失冲突。
claims:
- 消融实验（Table 3）表明，完整模型（+Ref. DSD）在语义一致性（CLIP 0.890）、视觉质量（5.848）和几何质量（5.616）上均优于仅概念先验的基线，验证了DSD与参考先验的必要性。
- 用户研究（Figure 4）显示，在30名用户参与的900次成对比较中，所有偏好均显著偏向ThemeStation（p<0.05），证明了其生成的3D资产在质量与多样性上优于七种前沿方法。
- 噪声级别反转消融（Figure 7）表明，将概念先验用于低噪声、参考先验用于高噪声会导致显著性能下降，证实了从粗到细动态与先验功能的一致性。
- Ablation Study (Table 3) 上 CLIP similarity ↑ = 0.890 (+Ref. DSD)
---

# ThemeStation: Generating Theme-aware 3D Assets From Few Exemplars

> [!tip] 核心洞察
> 预训练文本到图像扩散模型的反向扩散过程具有从粗到细的噪声级别动态，这与概念先验（全局布局/颜色）和参考先验（高频细节）的功能天然吻合，因此通过在不同去噪时间步施加不同先验可有效避免损失冲突。

| 字段 | 内容 |
|------|------|
| 中文题名 | ThemeStation：基于少量示例的主题感知三维资产生成 |
| 英文题名 | ThemeStation: Generating Theme-aware 3D Assets From Few Exemplars |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://3dthemestation.github.io/) · [Code](https://github.com/3DTopia/ThemeStation) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | ThemeStation |
| Dataset | Ablation Study, User Study |

> [!tip] 效果简介
> - Ablation Study (Table 3) 上，CLIP similarity ↑ 0.890 (+Ref. DSD) vs 0.877 (Baseline concept prior only) (+0.013)；Visual Quality ↑ 5.848 (+Ref. DSD) vs 5.639 (Baseline) (+0.209)。
> - User Study (Figure 4) 上，User preference all pairwise comparisons significantly favor ThemeStation (p<0.05) vs seven compared methods (significant)。

## 概要

现有基于示例的三维生成方法仅能对输入模型进行简单的尺寸调整或重组，无法理解示例的语义与风格，导致生成结果缺乏主题一致性与内容多样性。本文提出**ThemeStation**，一个主题感知的三维到三维生成框架，仅需少量三维示例即可生成主题统一且形态多样的三维资产。该方法采用两阶段生成范式：首阶段通过微调预训练文本到图像扩散模型生成主题一致的概念图像；次阶段提出**双分数蒸馏（Dual Score Distillation, DSD）**，利用扩散模型从粗到细的去噪动态，在高噪声级别施加概念先验以控制全局布局与颜色，在低噪声级别施加参考先验以恢复纹理与几何细节，从而有效解耦两种先验并缓解损失冲突。实验表明，完整模型在语义一致性（CLIP 0.890）、视觉质量（5.848）和几何质量（5.616）上均优于仅概念先验的基线；用户研究中30名参与者的900次成对比较均显著偏向ThemeStation（p<0.05），验证了其在生成质量与多样性上超越七种前沿方法的优势。该方法定位于基于扩散先验的三维生成与风格化建模的交叉点，为小样本主题感知三维资产生成提供了新的技术路径。

## 核心方法与创新机理

ThemeStation 的核心目标是从极少量的三维示例（甚至仅一个）出发，生成一批主题一致但形态多样的新三维资产。现有基于示例的三维生成方法（如 **SinGAN3D** (Wu and Zheng, 2022)、**VP-SinGAN** (Wu et al., 2023)）仅能对输入模型进行简单的尺寸调整、重复或重组，无法理解示例的语义与风格，导致生成结果缺乏主题一致性和内容多样性。这一瓶颈的根源在于：这些方法缺乏对示例“主题”的语义级理解，也没有机制将示例的视觉细节可控地迁移到新生成的结构中。

ThemeStation 通过两个关键设计突破这一瓶颈：(1) 两阶段生成流程，模拟人工三维建模“先绘制概念图、再逐步建模”的工作流；(2) **双分数蒸馏（Dual Score Distillation, DSD）**，利用预训练扩散模型的从粗到细去噪动态，在不同噪声级别上解耦应用概念先验与参考先验，从而避免损失冲突。

### 两阶段生成流程

ThemeStation 的生成流程包含四个顺序模块，分为两个阶段：

**第一阶段：主题驱动的概念图像生成。** 给定少量三维示例，首先将其渲染为多视角图像，然后在这些渲染图像上微调一个预训练的文本到图像（T2I）扩散模型。微调后的模型（称为主题驱动扩散模型）能够生成与输入示例主题一致但形态多样的二维概念图像。这一阶段的关键在于微调迭代次数的选择：200次迭代在概念图像的多样性与质量之间取得最佳平衡（LPIPS多样性0.617，LAION美学评分6.355）；超过300次迭代会导致过拟合，多样性大幅下降（LPIPS降至0.403以下）。

**第二阶段：参考信息引导的三维资产建模。** 这一阶段包含三个步骤：
1. **初始三维模型提取**：使用现成的 image-to-3D 方法（如 Wonder3D (Long et al., 2023)）将第一阶段生成的概念图像提升为神经隐式 SDF 初始模型。
2. **双分数蒸馏优化**：通过 DSD 损失，在不同噪声级别上联合概念先验和参考先验，逐步将初始粗糙模型优化为高质量纹理网格。这是方法的核心创新，下文将详细展开。
3. **网格精细化**：将 SDF 转换为 DMTet 表示（192网格，512分辨率），在优化循环中直接优化纹理网格。

### 双分数蒸馏（DSD）：核心创新机理

DSD 的核心洞察来自对预训练扩散模型去噪动态的深入理解：扩散模型的反向扩散过程具有从粗到细的噪声级别动态——高噪声级别（大 $t$）主要决定图像的全局布局和颜色分布，低噪声级别（小 $t$）则负责恢复高频细节和纹理。这一动态与两类先验的功能天然吻合：概念先验需要约束全局主题一致性（布局、颜色），参考先验需要注入精细的纹理和几何细节。

基于这一洞察，DSD 将两个先验分配到不同的噪声级别区间，构建联合优化目标：

**概念先验（Concept Prior）** 作用于高噪声级别 $t_h$。它通过在第一阶段概念图像和初始模型渲染视图上联合微调的扩散模型 $\phi_c$ 来施加约束，其梯度为：

$$\nabla_{\boldsymbol{\theta}}\mathcal{L}_{\mathrm{concept}}(\phi_c,t_h) = \mathbb{E}_{t_h,\epsilon}\left[\omega\left(\epsilon_{\phi_c}\left(x_{t_h};y,t_h\right)-\epsilon_{\mathrm{lora}}\right)\frac{\partial x}{\partial\boldsymbol{\theta}}\right]$$

其中 $\epsilon_{\phi_c}$ 是概念先验扩散模型的噪声预测，$\epsilon_{\mathrm{lora}}$ 是 LoRA 微调的变分分数蒸馏（VSD）模型的噪声预测，$y$ 是文本条件。该梯度在高噪声级别上驱动三维表示 $\boldsymbol{\theta}$ 向概念图像的全局布局和颜色分布靠拢。

**参考先验（Reference Prior）** 作用于低噪声级别 $t_l$。与以往仅使用颜色图像学习参考先验的方法不同，ThemeStation 同时使用渲染的颜色图像 $x$ 和法线贴图 $n$ 来学习参考先验扩散模型 $\phi_r$，以联合捕获纹理和几何细节。其梯度为：

$$\nabla_{\theta}\mathcal{L}_{\mathrm{ref}}(\phi_r,t_l) = \mathbb{E}_{t_l,\epsilon}[\omega(\epsilon_{\phi_r}(x_{t_l};y_x,t_l)-\epsilon_{\mathrm{lora}})\frac{\partial x}{\partial\theta}] + \mathbb{E}_{t_l,\epsilon}[\omega(\epsilon_{\phi_r}(n_{t_l};y_n,t_l)-\epsilon_{\mathrm{lora}})\frac{\partial x}{\partial\theta}]$$

其中 $y_x$ 和 $y_n$ 分别是颜色和法线的条件文本。两个期望项分别对应纹理细节和几何细节的约束。在低噪声级别上，参考先验恢复输入示例中的精细元素，使最终模型继承示例的视觉风格。

**DSD 损失** 将两个先验的梯度加权组合：

$$\nabla_{\theta}\mathcal{L}_{\mathrm{DSD}} = \alpha\nabla_{\theta}\mathcal{L}_{\mathrm{concept}}(\phi_c,t_h) + \beta\nabla_{\theta}\mathcal{L}_{\mathrm{ref}}(\phi_r,t_l)$$

其中 $\alpha$ 和 $\beta$ 是平衡权重。这一设计的关键在于：两个先验在不同的噪声区间独立作用，概念先验在高噪声级别塑造全局结构，参考先验在低噪声级别注入细节，从而避免了简单叠加两个先验时产生的损失冲突。

### Changed Slots：相对于基线的方法改进

ThemeStation 相对于现有方法有三个关键改进槽位：

**槽位一：生成流程从单阶段到两阶段。** 现有方法（如 DreamFusion、RealFusion）直接从文本或图像生成三维模型，缺乏对主题一致性的显式建模。ThemeStation 的两阶段流程将“主题理解”与“三维建模”解耦，第一阶段专注于生成主题一致的概念图像，第二阶段再将概念图像提升为三维模型并注入参考细节。

**槽位二：先验组合策略从简单相加到噪声级别解耦。** 直接将概念先验和参考先验相加（naive stacking）会导致严重的损失冲突，产生凹凸表面和模糊纹理（见图7(b)）。DSD 通过噪声级别分离有效缓解了这一冲突：概念先验仅在高噪声级别作用，参考先验仅在低噪声级别作用。消融实验证实，反转这一分配（概念先验用于低噪声、参考先验用于高噪声）会显著降低生成质量（见图7(d)），将参考先验扩展到所有噪声级别也无正面效果且质量下降（见图7(e)），证明了噪声级别分离的必要性。

**槽位三：参考先验从仅颜色到颜色+法线联合。** 同时使用渲染的颜色图像和法线贴图学习参考先验，使参考先验能够更全面地捕获纹理和几何细节，从而在三维优化中同时提升视觉质量和几何质量。

### 训练与推理路径

**第一阶段训练**：在输入示例的渲染图像上微调预训练 T2I 扩散模型，通常使用 200 次迭代，学习率等细节见附录。微调后的模型可在推理时通过不同随机种子生成多样化的概念图像。

**第二阶段优化**：这是一个基于优化的推理过程。从概念图像提取初始 SDF 模型后，通过 DSD 损失迭代更新三维表示参数。每次迭代中，从随机视角渲染颜色和法线图像，分别计算概念先验和参考先验的梯度，加权组合后更新 DMTet 网格参数。整个优化过程需要数小时，这是当前方法的主要效率瓶颈。

### 因果关系总结

ThemeStation 的创新机理可概括为一条因果链：两阶段流程将主题一致性与三维质量解耦 → DSD 利用扩散模型的从粗到细去噪动态，将概念先验（全局约束）和参考先验（细节注入）分配到不同噪声级别 → 噪声级别的分离避免了损失冲突 → 颜色+法线联合参考先验同时提升纹理和几何质量 → 最终生成主题一致、细节丰富、形态多样的三维资产。

![[assets/figures/papers/paper_list_l39_https_3dthemestation_github_io/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ThemeStation. Given just one or a few reference models, our approach can generate theme-consistent 3D models in two stages. In the first stage, we fine-tune a pre-trained text-to-image (T2I) diffusion model to form a customized theme-driven diffusion model that produces various concept images. In the second stage, we conduct reference-informed 3D asset modeling by progressively optimizing a rough initial model (omitted in this figure for brevity), which is obtained using an off-the-shelf image-to-3D method given the concept image, into a final 3D asset. We use a novel dual score distillation (DSD) loss for optimization, which applies concept prior and reference prior at differen...*

## 实验与关键发现

ThemeStation 的实验评估围绕两个核心目标展开：一是验证第二阶段参考信息引导的 3D 建模能力（与 image-to-3D 方法的对比），二是验证整体框架的主题一致性与生成多样性（与 3D 变体生成方法的对比）。此外，通过系统的消融实验和用户研究，论文对双分数蒸馏（DSD）的各个设计选择进行了因果验证。

### 主结果：与前沿方法的定量与定性对比

**Image-to-3D 对比（Table 1）**。将 ThemeStation 的第二阶段与五种前沿 image-to-3D 方法进行对比：DreamFusion（Poole et al., 2023）、RealFusion（Melas-Kyriazi et al., 2023）、Make-It-3D（Tang et al., 2023b）、Zero-1-to-3（Liu et al., 2023b）和 One-2-3-45（Liu et al., 2023a）。所有方法使用相同的概念图像作为输入。ThemeStation 在语义一致性（CLIP similarity ↑）上达到 0.890，显著优于最强基线 Make-It-3D 的 0.877。在 Contextual Distance ↓ 指标上，ThemeStation 取得 3.168，同样优于所有对比方法。定性结果（Figure 5）进一步揭示：DreamFusion 和 RealFusion 生成的结果缺乏精细纹理；Make-It-3D 的几何结构较为粗糙；Zero-1-to-3 和 One-2-3-45 虽能生成合理几何，但纹理质量明显逊色。ThemeStation 在正面和背面视图下均展现出更丰富的纹理细节和更准确的几何结构。这一优势源于参考先验对颜色渲染和法线贴图的联合利用——前者恢复纹理，后者约束几何。

**3D 变体生成对比（Table 2）**。将 ThemeStation 完整两阶段流程与 SinGAN3D（Wu and Zheng, 2022）、VP-SinGAN（Wu et al., 2023）以及 DreamBooth3D（Raj et al., 2023）进行对比。在 Visual Diversity ↑ 指标上，ThemeStation 达到 0.315，远超 SinGAN3D（0.124）和 VP-SinGAN（0.097），证明其能生成更丰富的主题内变体。在 3D 感知的 CLIP 一致性上，ThemeStation 亦保持领先。定性结果（Figure 6）显示：SinGAN3D 和 VP-SinGAN 仅能对输入模型进行简单的尺寸缩放或部件重组，无法理解主题语义；DreamBooth3D 虽能生成新模型，但纹理质量和几何精度不足。ThemeStation 则能生成与示例主题一致（如卡通风格、特定动物类别）但形态各异的高质量 3D 资产。

**用户研究（Figure 4）**。为获得更可靠的主观质量评估，论文招募 30 名用户进行 2AFC 成对比较，共计 900 次问答。ThemeStation 与七种方法在所有成对比较中均获得统计显著的偏好（p < 0.05，卡方检验），覆盖了视觉质量、几何质量和主题一致性三个维度。这一结果排除了单一自动指标可能存在的偏差，为方法的整体优势提供了强有力的人因证据。

### 消融实验：DSD 设计的因果验证

消融实验（Table 3 和 Figure 7）系统验证了参考先验、DSD 损失和噪声级别分配三个关键设计选择。

![[assets/figures/papers/paper_list_l39_https_3dthemestation_github_io/figures/009_Table_3.jpg]]
*Table 3: Quantitative results of the ablation study*

**参考先验与 DSD 的必要性（Figure 7a–c）**。基线模型仅使用概念先验（Baseline），其 CLIP 一致性为 0.877，视觉质量评分 5.639，几何质量评分 5.460。直接叠加概念先验和参考先验（+Ref. naive）反而导致性能下降：视觉质量降至 5.502，几何质量降至 5.360，并产生凹凸不平的表面和模糊纹理。这是因为两个先验的梯度方向在高维空间中相互冲突，简单相加使优化陷入不良局部极小。完整模型（+Ref. DSD）通过在不同噪声级别分别施加两个先验，将 CLIP 提升至 0.890，视觉质量提升至 5.848，几何质量提升至 5.616。这一对比直接证明了 DSD 机制在缓解损失冲突中的核心作用。

**噪声级别分配的关键性（Figure 7c–e）**。将概念先验用于低噪声级别、参考先验用于高噪声级别（Inverted noise levels）会导致生成质量显著下降（Figure 7d），验证了从粗到细的动态与先验功能的天然匹配：高噪声级别对应全局布局与颜色（概念先验），低噪声级别对应高频细节（参考先验）。进一步地，将参考先验扩展到所有噪声级别（Ref. dominated，Figure 7e）不仅无正面效果，反而使质量恶化，表明将两个先验限制在不同噪声区间是必要的——全噪声级别的参考先验会干扰概念先验对全局结构的引导。

**第一阶段微调迭代次数（Table 4）**。主题驱动扩散模型的微调迭代次数直接影响概念图像的多样性与质量平衡。200 次迭代时 LPIPS-diversity 为 0.617，LAION-aesthetic-score 为 6.355，取得最佳折衷。300 次迭代时多样性骤降至 0.403，400 次迭代时进一步降至 0.347 且美学评分跌至 5.941，表明模型过拟合到示例图像，丧失了生成多样化概念的能力。

### 失败模式与适用边界

论文明确展示了方法的局限性（Figure 8）：

1. **概念图像错误的不可纠正性**。当第一阶段生成的概念图像存在严重语义错误（如尾巴生长在身体前方），第二阶段的 DSD 优化无法纠正这类全局性概念错误，最终 3D 模型会继承这些缺陷。这是两阶段流程中信息单向流动（概念图像→3D 模型）的固有局限。
2. **规则几何的生成困难**。对于需要严格规则形状的物体（如由完美立方体构成的建筑），方法缺乏显式几何约束，难以生成规整的几何结构。这是因为扩散先验本质上是统计性的，无法保证精确的几何正则性。
3. **优化效率**。当前管线仍需数小时来优化初始模型为最终 3D 资产，这与其他基于优化的 3D 生成方法（如 DreamFusion 系列）处于同一量级，但限制了交互式应用场景。

### 评估的公平性保障

用户研究采用标准 2AFC 范式，所有偏好均通过卡方检验验证统计显著性（p < 0.05），避免了随机猜测的影响。自动指标（CLIP similarity、Contextual Distance、Visual Diversity）均使用公开预训练模型计算，确保可复现性。与 image-to-3D 方法的对比中，所有方法使用相同的概念图像作为输入，排除了输入差异的干扰。

![[assets/figures/papers/paper_list_l39_https_3dthemestation_github_io/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with image-to-3D methods*

![[assets/figures/papers/paper_list_l39_https_3dthemestation_github_io/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison with 3D variation methods*

![[assets/figures/papers/paper_list_l39_https_3dthemestation_github_io/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of the key ideas between image style transfer (top) and our dual score distillation (bottom). Images are from Gatys et al. [2016] (top) and Dibia [2022] (bottom)*

![[assets/figures/papers/paper_list_l39_https_3dthemestation_github_io/figures/004_Figure_4.jpg]]
*Figure 4: Results of the user study. We compare our method with seven baseline methods using 2AFC pairwise comparisons. All preferences are statistically significant (?? \< 0.05, chi-squared test)*

## 定位与知识库关联

ThemeStation 在 3D 资产生成领域占据了一个此前未被充分探索的位置：**主题感知的 3D-to-3D 生成**。已有工作要么是从单张图像重建 3D（image-to-3D），要么是从文本描述生成 3D（text-to-3D），要么是对单个 3D 模型做有限变体（3D variation）。ThemeStation 的核心定位差异在于：给定一个或少量 3D 示例，它能够理解这些示例共享的“主题”（语义概念、风格、结构特征），并生成一批既保持主题一致性又具有内容多样性的新 3D 资产。

### 改变的 Slot：从“单先验重建”到“解耦双先验主题生成”

相对已有方法的本质改变可以归纳为一个关键 slot 的切换：

| Slot | 已有方法 | ThemeStation |
|------|----------|--------------|
| **先验组合策略** | 单一先验（如仅用文本条件或仅用参考图像）或两个先验的简单叠加 | 双分数蒸馏（DSD）：概念先验作用于高噪声级别（控制全局布局与颜色），参考先验作用于低噪声级别（恢复细节纹理与几何），以从粗到细的方式联合优化 |

这一 slot 的改变直接回应了本领域的核心瓶颈：**现有基于示例的 3D 生成方法（如 SinGAN3D、VP-SinGAN）仅能对输入模型进行简单的尺寸调整、重复或重组，无法理解示例的语义与风格，导致生成的 3D 模型缺乏主题一致性和内容多样性**。ThemeStation 通过将预训练文本到图像扩散模型的从粗到细的反向扩散动态与两种先验的功能特性对齐，有效避免了损失冲突，实现了主题一致性与内容多样性的统一。

### 知识库挂载点

ThemeStation 可挂载到知识库的以下节点：

1. **3D 资产生成（3D Asset Generation）**  
   - 父节点：基于扩散先验的 3D 生成方法  
   - 子节点：主题感知 3D-to-3D 生成  
   - 与 DreamFusion (Poole et al., 2023)、RealFusion (Melas-Kyriazi et al., 2023)、Make-It-3D (Tang et al., 2023b) 等 image-to-3D 方法的关系：这些方法解决的是从单张 2D 图像到 3D 的“提升”问题，而 ThemeStation 的第二阶段可视为对这一类方法的增强——在标准 image-to-3D 流程中引入了参考先验引导的优化，显著提升了 3D 模型的纹理细节和几何质量（Table 1 中 CLIP 相似度达 0.890，优于所有 image-to-3D 基线）。

2. **扩散模型先验蒸馏（Score Distillation from Diffusion Models）**  
   - 父节点：Score Distillation Sampling (SDS) 及其变体  
   - 子节点：双分数蒸馏（Dual Score Distillation, DSD）  
   - DSD 是 SDS/VSD 在主题感知场景下的扩展。其核心创新在于**将两个扩散先验分配到不同的噪声级别**——概念先验在高噪声级别施加（$t_h$），参考先验在低噪声级别施加（$t_l$）。这一设计与图像风格迁移中“内容损失用于高层、风格损失用于低层”的思路异曲同工（Figure 3），但将其迁移到了 3D 生成的分数蒸馏范式中。

3. **主题驱动生成（Theme-Driven Generation）**  
   - 父节点：DreamBooth 等主题定制化生成方法  
   - 子节点：基于 3D 示例的主题驱动 T2I 扩散模型微调  
   - ThemeStation 第一阶段在 3D 示例的渲染图像上微调预训练 T2I 扩散模型，这与 DreamBooth3D (Raj et al., 2023) 有相似之处，但目标不同：DreamBooth3D 是从少量 2D 图像重建特定物体的 3D 模型，而 ThemeStation 旨在生成与示例共享主题但内容多样的新概念图像。

4. **3D 变体生成（3D Variation Generation）**  
   - 与 SinGAN3D (Wu and Zheng, 2022) 和 VP-SinGAN (Wu et al., 2023) 的关系：这些方法直接从单个 3D 模型生成变体，缺乏语义理解能力。ThemeStation 通过引入概念先验，在主题一致性和生成多样性上均显著超越它们（Table 2 中 Visual Diversity 达 0.315，用户研究中所有成对比较均显著偏向 ThemeStation，p<0.05）。

### 适用边界

ThemeStation 的适用边界由以下条件界定：

- **输入要求**：需要 1 个或少量 3D 示例（exemplars），示例需共享可识别的主题特征。若示例之间缺乏语义一致性，第一阶段微调可能无法形成有意义的主题概念。
- **初始化依赖**：两阶段流程受初始概念图像质量影响显著。若概念图像存在严重错误（如物体部件位置错乱），DSD 优化难以纠正这些结构性错误，最终 3D 模型会继承这些缺陷（Figure 8a）。
- **几何约束缺失**：对于规则几何形状（如完美立方体构成的建筑），方法缺乏显式几何约束，难以生成严格规整的结构（Figure 8b）。
- **计算成本**：当前管线需要数小时来优化初始模型为最终 3D 资产，与 DreamFusion 等基于优化的方法类似，不适用于实时场景。

### 后续启发与开放问题

ThemeStation 为以下研究方向提供了启发：

1. **效率提升**：能否通过更先进的扩散模型（如蒸馏模型）或神经渲染技术将优化时间从数小时缩短至分钟级？这是基于优化的 3D 生成方法的共性挑战。

2. **前馈式生成**：是否可以训练一个前馈式主题感知 3D-to-3D 生成模型，绕过迭代优化过程，同时避免不良初始化带来的级联错误？这需要构建大规模的主题-3D 配对数据集。

3. **错误自动检测与修正**：概念图像阶段出现严重错误时，如何在不依赖人工干预的情况下自动检测并修正？这可能涉及将 3D 结构先验（如对称性、物理合理性）引入第一阶段生成过程。

4. **多模态主题理解**：当前的主题概念主要通过视觉示例隐式定义。未来工作可将文本描述作为主题的补充约束，实现更精确的主题控制。

5. **DSD 范式的推广**：将两个先验分配到不同噪声级别的思路不仅适用于 3D 生成，也可推广到其他需要平衡全局一致性与局部细节的生成任务（如视频生成、场景编辑），值得进一步探索。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/ThemeStation_Generating_Theme_aware_3D_Assets_From_Few_Exemplars.pdf]]