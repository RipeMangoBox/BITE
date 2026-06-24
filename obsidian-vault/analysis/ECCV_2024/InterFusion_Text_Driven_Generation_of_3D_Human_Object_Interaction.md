---
title: "InterFusion: Text-Driven Generation of 3D Human-Object Interaction"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction.pdf
aliases:
- InterFusion
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 从文本描述中估计3D人体姿态作为几何先验，简化了人体生成，并为物体生成提供空间约束，从而使人体和物体可以解耦生成并全局联合优化。
primary_logic: 将HOI生成分解为两阶段：先利用大规模合成图像和CLIP构建文本-姿态码本，检索并筛选出锚定姿态；随后在该姿态引导下，通过局部（人体NeRF、物体NeRF）分离优化和全局（交互场景）联合优化，结合SDS损失和几何约束，实现连贯且高精度的3D人-物交互场景生成。
claims:
- InterFusion在CLIP得分和GPT-4V选择率上大幅领先所有基线方法，证明其生成的3D场景与文本描述更一致、物理交互更合理。
- 去除交互SDS损失（SDS-I）后GPT-4V选择率从77.05%暴跌至1.64%，说明交互语义引导是生成正确交互的关键。
- 去除物体几何约束后，生成极不稳定，物体容易退化并穿透人体，定量选择和定性视觉均显著劣化。
- 定制61类文本提示（13种交互类型） 上 CLIP score = 0.3308 (Ours-HC)
---

# InterFusion: Text-Driven Generation of 3D Human-Object Interaction

> [!tip] 核心洞察
> 将HOI生成分解为两阶段：先利用大规模合成图像和CLIP构建文本-姿态码本，检索并筛选出锚定姿态；随后在该姿态引导下，通过局部（人体NeRF、物体NeRF）分离优化和全局（交互场景）联合优化，结合SDS损失和几何约束，实现连贯且高精度的3D人-物交互场景生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterFusion: 文本驱动的3D人-物交互生成 |
| 英文题名 | InterFusion: Text-Driven Generation of 3D Human-Object Interaction |
| 会议/期刊 | ECCV 2024 |
| Links | [Project](https://sisidai.github.io/InterFusion/) · [Code](https://github.com/deep-floyd/IF) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | InterFusion |
| Dataset | 定制61类文本提示（13种交互类型） |

> [!tip] 效果简介
> - 定制61类文本提示（13种交互类型） 上，CLIP score 0.3308 (Ours-HC) vs 0.3027 (DreamFusion), 0.3179 (Magic3D), 0.2761 (TextMesh), 0.3203 (Ours-OC) (+0.0281 对比最强基线 (Ours-OC))。
> - 同上 上，GPT-4V select (%) 65.57 (Ours-HC) vs 8.20 (DreamFusion), 11.48 (Magic3D), 1.64 (TextMesh), 13.11 (Ours-OC) (+52.46 对比最强基线 (Ours-OC))；CLIP R-Precision (%) 83.6 (Ours) vs 77.0 (MVDream), 68.8 (DreamFusion), 73.8 (Magic3D), 47.5 (TextMesh), 67.2 (Prol... (+6.6 对比最强基线 (MVDream))；FID_CLIP (越低越好) 63.7 (Ours) vs 65.5 (MVDream), 68.4 (DreamFusion), 70.0 (Magic3D), 69.8 (TextMesh), 64.8 (Prol... (-1.8 对比最强基线 (MVDream))。

## 概述

**核心问题**：文本驱动的3D人-物交互（HOI）生成面临双重瓶颈——（1）缺乏成对的文本-交互训练数据，导致多概念（人体、物体、交互语义）联合生成时出现语义混淆；（2）现有扩散模型难以同时建模多个具有复杂空间关系的概念，直接应用文本到3D方法（如DreamFusion、Magic3D）会产生几何残缺、交互错误或物体穿透等严重问题。

**核心思路**：InterFusion将HOI生成分解为两阶段——先利用大规模合成图像与CLIP构建文本-姿态码本，检索并筛选出与交互描述匹配的**锚定3D人体姿态**作为几何先验；随后在该姿态引导下，将人体与物体解耦为独立的NeRF（H-NeRF与O-NeRF），分别进行分数蒸馏采样（SDS）优化，再通过全局交互SDS损失与几何约束进行联合调整，最终生成连贯且高精度的3D交互场景。

**方法定位**：InterFusion属于**文本到3D生成**与**神经辐射场（NeRF）优化**的交叉方法，区别于DreamFusion（Poole et al. 2022）、Magic3D（Lin et al. 2023）、TextMesh（Tsalicoglou et al. 2023）、MVDream（Shi et al. 2024）和ProlificDreamer（Wang et al., NeurIPS 2024）等从零生成或物体中心生成的基线，其关键创新在于引入**文本估计的人体姿态作为显式几何锚点**，并采用**解耦-联合优化策略**。

**主要结果**：在涵盖13种交互类型的61类文本提示基准上，InterFusion的CLIP得分达到0.3308，显著优于最强基线Ours-OC的0.3203；GPT-4V选择率高达65.57%，远超基线最高值13.11%（Table 1）。消融实验证实，移除交互SDS损失后GPT-4V选择率从77.05%暴跌至1.64%，移除物体几何约束后降至16.39%，验证了交互语义引导与空间约束的关键作用（Table 2）。

## 背景与动机

### 问题背景

文本驱动的3D内容生成近年来取得了显著进展。以DreamFusion为代表的分数蒸馏采样（Score Distillation Sampling, SDS）方法，通过利用预训练的2D扩散模型作为先验，实现了从任意文本描述生成3D物体或场景。然而，这些方法主要聚焦于单一物体或简单场景的生成，当面对需要同时生成多个具有复杂空间关系的概念时，其表现急剧下降。

人-物交互（Human-Object Interaction, HOI）场景正是这类复杂生成任务的典型代表。一个完整的HOI场景需要同时生成人体和物体，且两者之间必须存在语义合理、物理正确的空间关系——例如“一个人坐在椅子上”要求人体臀部与椅面接触，“一个人骑自行车”要求双手握把、双脚踩踏。这种多概念、强约束的生成需求，对现有文本到3D方法构成了根本性挑战。

### 现有方法缺口

直接应用通用文本到3D方法生成HOI场景存在两个核心瓶颈：

**（1）训练数据匮乏导致多概念生成混乱。** 现有文本到3D方法依赖的扩散模型主要在单一物体的图文对数据上训练，缺乏成对的文本-交互场景训练数据。当文本提示同时包含人体风格、物体风格和交互类型时，扩散模型难以正确解耦和组合这些语义概念，常常导致人体与物体在语义或几何上混淆。

**（2）扩散模型难以同时建模复杂空间关系。** 即使扩散模型能够理解文本中的多个概念，其从零开始同时生成人体和物体并建立精确的相对位置关系仍然极其困难。由于缺乏显式的空间约束，生成结果容易出现人体与物体分离、物体退化消失、或两者相互穿透等问题。

### 本文动机

针对上述瓶颈，本文提出一个核心洞察：**从文本描述中估计3D人体姿态作为几何先验，可以有效地将复杂的HOI生成问题解耦。** 人体姿态不仅直接决定了交互的类型和空间布局，还为物体的位置和方向提供了天然的锚定约束。通过先确定“人如何与物交互”的姿态骨架，再分别生成人体外观和物体几何，可以显著降低生成难度，避免多概念混淆。

基于这一洞察，本文设计了一个两阶段框架InterFusion：第一阶段从文本中检索并筛选出锚定姿态（anchor pose），第二阶段在该姿态的几何约束下，通过分离优化人体模型和物体模型，并结合全局交互语义引导，实现连贯且高精度的3D人-物交互场景生成。

## 核心创新

InterFusion 的核心创新在于将“文本→3D人-物交互”这一耦合难题，通过**人体姿态先验的注入**与**生成过程的解耦-联合优化**两条主线加以解决。相较于现有 text-to-3D 方法直接对整个场景进行联合生成，InterFusion 的关键变化体现在两个 **changed slots** 上。

### 1. 几何先验类型：从“无先验”到“锚定人体姿态”

现有零样本文本到3D方法（如 **DreamFusion**、**Magic3D**、**TextMesh** 等）在生成人-物交互场景时，缺乏对交互空间结构的显式建模，导致人体与物体在空间关系上出现语义混淆和几何穿透。InterFusion 用一个从文本中**估计的3D人体姿态**作为锚定几何先验，从根本上改变了这一局面。

该先验的获取并非依赖稀缺的真实文本-3D交互数据，而是通过一个**文本-姿态码本检索机制**实现：首先在大规模合成HOI图像上提取CLIP姿态嵌入，经K-Means聚类构建包含2,048个姿态原型的码本；然后对输入交互文本 $T^I$ 的CLIP嵌入与码本中姿态嵌入进行余弦相似度检索，取Top-k候选并通过CLIP分数筛选出最优锚定姿态（见 Eq. (2)）。这一设计巧妙绕过了成对训练数据匮乏的瓶颈，使人体生成从一开始就具备合理的空间占位，为后续物体生成提供了明确的几何约束。

消融实验中的 **Ours-OC** 基线（用物体几何先验替代人体姿态先验）从反面验证了这一创新的必要性：在相同文本提示下，Ours-OC 生成的场景在多视角下出现人体与物体的空间关系错误（见 Figure 7），GPT-4V 选择率仅为 13.11%，而本文的 Ours-HC 达到 65.57%（Table 1），差距达 52.46 个百分点。

### 2. 生成优化策略：从“单一联合生成”到“解耦-联合优化”

传统 text-to-3D 方法使用单一 NeRF 同时生成人体和物体，SDS 损失在语义和几何层面产生严重混淆。InterFusion 将生成过程**解耦为 H-NeRF（人体）和 O-NeRF（物体）两个独立模型**，分别进行 SDS 优化，再通过全局交互 SDS 损失和几何约束进行联合调整。

具体而言，这一策略包含三个关键机制：

- **分离的语义引导**：H-NeRF 接受人体风格文本 $y^H$ 和头部增强文本 $y^{H,h}$ 的双分支 SDS 引导（Eq. 3），O-NeRF 则同时由交互场景文本 $y^I$ 和物体风格文本 $y^O$ 引导（Eq. 5），使各自专注于自身语义区域。
- **锚定姿态的几何约束**：H-NeRF 受锚定姿态的占位约束，确保人体密度分布在姿态锚点内部（Eq. 4）；O-NeRF 则受穿透惩罚，防止物体进入人体占位区域（Eq. 7）。
- **梯度截断的联合优化**：在通过 alpha 合成渲染完整交互场景（Eq. 6）并施加交互 SDS 损失时，**截断流向人体的梯度**，避免交互损失过度驱动人体变形，从而维持解耦优化的平衡。

消融实验揭示了各机制的贡献强度：移除交互 SDS 损失（$L_{SDS}^I$）后，GPT-4V 选择率从 77.05% 暴跌至 1.64%（Table 2），证明交互语义引导是生成正确交互的**决定性因素**；移除物体几何约束（$L_{geo}^O$）后，选择率降至 16.39%，且物体在原点退化或穿透人体的现象频繁出现（Figure 5b）；移除物体独立 SDS 损失（$L_{SDS}^O$）后选择率仅余 4.92%，表明物体独立优化对完整交互场景同样不可或缺。

### 创新本质

InterFusion 的创新本质上是一个**“先验注入→解耦生成→联合约束”**的因果链条：锚定姿态作为几何先验（causal knob）解决了多概念空间关系建模的瓶颈（real bottleneck），使人体和物体可以安全地分离优化；而交互 SDS 损失和几何约束则确保了解耦后的两个模型在语义和空间上重新对齐，最终产出连贯的3D人-物交互场景。

## 整体框架

InterFusion 将文本驱动的 3D 人-物交互（HOI）生成分解为**两个阶段**：锚定姿态生成（Anchor Pose Generation）和姿态引导的 HOI 优化（Pose-Guided HOI Generation）。这一分解的核心动机在于，直接文本到 3D 方法在 HOI 任务上效果不佳，根源是（1）缺乏成对的文本-交互训练数据，导致多概念生成混乱；（2）扩散模型难以同时建模多个具有复杂空间关系的概念。InterFusion 通过从文本描述中估计 3D 人体姿态作为几何先验，简化了人体生成，并为物体生成提供空间约束，从而使人体和物体可以解耦生成并全局联合优化。

**输入与输出**。框架的输入是一个文本三元组：

$$
T = \{ T^H, T^O, \dot{T}^I \}
$$

分别指定期望的人体风格、物体风格和交互类型。输出为 3D 场景表示：

$$
\psi = \{ \psi^H, \psi^O \}
$$

包含人体模型和物体模型。

**第一阶段：锚定姿态生成**。该阶段利用大规模合成 HOI 图像数据集，通过 CLIP 嵌入和 K-Means 聚类（2,048 个质心）构建文本-姿态码本。对于给定的交互文本 $\dot{T}^I$，通过 CLIP 文本嵌入与码本中姿态嵌入的余弦相似度检索前 k 个最匹配的 3D 姿态：

$$
\{\theta_k^T\}^I = \mathrm{TOP}_k \left( f_{text}(T^I), \theta_E \right)
$$

随后从候选姿态中筛选出最终锚定姿态，作为第二阶段的几何先验。

**第二阶段：姿态引导的 HOI 优化**。该阶段以锚定姿态为约束，将 HOI 场景解耦为两个独立的 NeRF 模型——H-NeRF（人体）和 O-NeRF（物体）——分别进行优化，并通过全局交互场景联合调整。具体包含以下模块：

1. **人体模型优化（H-NeRF）**：以锚定姿态为几何约束，通过人体风格文本的 SDS 损失及头部区域增强，优化人体 NeRF 的密度和颜色。
2. **物体模型优化（O-NeRF）**：依据交互类型和物体风格文本的 SDS 损失，并施加锚定姿态占位惩罚，优化物体 NeRF，防止与人体穿透。
3. **相机追踪（Camera Tracing）**：根据占用概率自动调整相机姿态，聚焦场景或物体的中心区域，提升细节捕获。
4. **全局联合优化**：通过 alpha 合成将 H-NeRF 和 O-NeRF 渲染为完整交互场景，利用交互文本的 SDS 梯度同时更新两个模型，并截断流向人体的梯度以平衡优化。

总损失函数为：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{SDS}}^H + \lambda_1 \mathcal{L}_{\mathrm{SDS}}^O + \mathcal{L}_{\mathrm{geo}}^H + \lambda_2 \mathcal{L}_{\mathrm{geo}}^O + \lambda_3 L_{\mathrm{reg}}
$$

其中 $\mathcal{L}_{\mathrm{SDS}}^H$ 和 $\mathcal{L}_{\mathrm{SDS}}^O$ 分别为人体和物体的 SDS 损失，$\mathcal{L}_{\mathrm{geo}}^H$ 和 $\mathcal{L}_{\mathrm{geo}}^O$ 为几何约束损失，$L_{\mathrm{reg}}$ 为正则项，权重 $\lambda_1, \lambda_2, \lambda_3$ 采用退火策略动态调整。

**与基线方法的关键差异**。InterFusion 与现有文本到 3D 方法（如 DreamFusion、Magic3D、TextMesh、MVDream、ProlificDreamer）的核心区别在于：这些基线方法通常使用单一 NeRF 联合生成人体和物体，缺乏显式几何先验，导致语义和几何混淆；而 InterFusion 通过“文本→3D 姿态→解耦生成”的路径，将人体姿态作为锚定几何先验，实现了人体和物体的分离优化与全局协调。消融基线 Ours-OC（用物体几何先验替代人体姿态先验）的显著性能下降（GPT-4V 选择率从 65.57% 降至 13.11%，Table 1）进一步验证了人体姿态先验的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l1762_InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction/figures/002_Figure_2.jpg]]
*Figure 2: InterFusion is a two-stage framework that transforms textual descriptions into detailed 3D human-object interactions, initially synthesizing anchor poses (upper left) and then optimizing the human model (upper right) and object model (bottom) with constraints from estimated pose and textual prompts*

## 核心模块与公式推导

InterFusion 的核心架构围绕“解耦生成、姿态锚定、联合优化”三条主线展开，其关键模块与数学表述如下。

### 3.1 锚定姿态生成模块

该模块旨在从文本交互描述中估计一个可靠的 3D 人体姿态作为几何先验。其核心是一个基于 CLIP 嵌入的文本-姿态码本检索系统。

首先，利用大规模合成 HOI 图像数据集，提取每张图像的 CLIP 视觉嵌入，并对图像中对应的 3D 人体姿态参数进行编码。随后，通过 K-Means 聚类构建包含 2,048 个质心的姿态码本，每个质心代表一类典型交互姿态。

给定输入文本中的交互描述 $T^I$，通过 CLIP 文本编码器 $f_{text}$ 提取其嵌入，并与码本中所有姿态的视觉嵌入计算余弦相似度，检索出最匹配的前 $k$ 个姿态：

$$
\{\theta_{k}^{T}\}^{I} = \mathrm{TOP}_{k} \left( f_{text}(T^{I}), \theta_{E} \right) \tag{2}
$$

其中 $\theta_{E}$ 为码本中姿态的嵌入集合。检索出的姿态候选随后通过 CLIP 分数进一步筛选，最终选定一个锚定姿态 $\theta_{anchor}$，作为后续解耦优化阶段的空间约束。

### 3.2 人体模型优化模块 (H-NeRF)

人体模型 $\psi^{H}$ 采用 NeRF 表示，其优化以锚定姿态为几何约束，并通过分数蒸馏采样 (SDS) 损失从文本描述中汲取外观信息。

**SDS 损失**：人体 SDS 损失由两部分组成——全身渲染分支和头部增强渲染分支，以同时优化整体风格与面部细节：

$$
\nabla_{\psi^{H}} \mathcal{L}_{\mathrm{SDS}} = \mathbb{E}_{t,\epsilon} \left[ w(t) (\hat{\epsilon}_{\phi}(x_t^{H}; y^{H}, t) - \epsilon) \frac{\partial x^{H}}{\partial \psi^{H}} \right] + \mathbb{E}_{t,\epsilon} \left[ w(t) (\hat{\epsilon}_{\phi}(x_t^{H,h}; y^{H,h}, t) - \epsilon) \frac{\partial x^{H,h}}{\partial \psi^{H}} \right] \tag{3}
$$

其中 $x^{H}$ 为全身渲染图，$x^{H,h}$ 为头部区域渲染图，$y^{H}$ 和 $y^{H,h}$ 分别为对应的人体风格文本提示和头部增强提示，$\hat{\epsilon}_{\phi}$ 为预训练扩散模型的预测噪声，$w(t)$ 为时间步权重。

**几何约束损失**：为确保生成的人体形态与锚定姿态一致，引入基于 COAP (Continuous Occupancy for Articulated Bodies) 的几何约束。COAP 以 SMPL 姿态参数 $\theta$ 和形状参数 $\beta$ 为输入，输出任意 3D 点的占用概率 $f(p)$。几何损失定义为：

$$
\mathcal{L}_{\mathrm{geo}}^{H} = \mathrm{CE}_{p_i \in \mathbb{P}_{\mathrm{in}}} (\alpha_i, f(p_i)) + \mathrm{CE}_{p_j \in \mathbb{P}_{\mathrm{out}}} (\alpha_j, f(p_j)) (1 - e^{-\frac{d}{2\eta^{2}}}) \tag{4}
$$

其中 $\mathbb{P}_{\mathrm{in}}$ 为锚定姿态内部的采样点集，$\mathbb{P}_{\mathrm{out}}$ 为外部采样点集，$\alpha_i$ 为 H-NeRF 在点 $p_i$ 处的预测占用率，$d$ 为外部点到锚定表面的距离，$\eta$ 为衰减系数。该损失强制内部点被占用、外部点随距离增大而占用概率衰减。

### 3.3 物体模型优化模块 (O-NeRF)

物体模型 $\psi^{O}$ 同样以 NeRF 表示，其优化需同时满足物体风格描述和交互语义，并防止与人体模型发生空间穿透。

**SDS 损失**：物体 SDS 损失由交互场景渲染和物体单独渲染两个视角共同引导：

$$
\nabla_{\psi^{O}} \mathcal{L}_{\mathrm{SDS}} = \mathbb{E}_{t,\epsilon} \left[ w(t) (\hat{\epsilon}_{\phi}(x_t^{I}; y^{I}, t) - \epsilon) \frac{\partial x^{I}}{\partial \psi^{O}} \right] + \mathbb{E}_{t,\epsilon} \left[ w(t) (\hat{\epsilon}_{\phi}(x_t^{O}; y^{O}, t) - \epsilon) \frac{\partial x^{O}}{\partial \psi^{O}} \right] \tag{5}
$$

其中 $x^{I}$ 为人-物交互场景渲染图，$x^{O}$ 为物体单独渲染图，$y^{I}$ 和 $y^{O}$ 分别为交互文本描述和物体风格描述。

**几何约束损失**：为防止物体侵入人体占据的空间，对锚定姿态内部点施加排斥约束：

$$
\mathcal{L}_{\mathrm{geo}}^{O} = \mathrm{CE}_{p_i \in \mathbb{P}_{\mathrm{in}}} (\alpha_i, 1 - f(p_i)) \tag{7}
$$

该损失强制锚定姿态内部点在 O-NeRF 中的占用率 $\alpha_i$ 趋近于零，确保物体不穿透人体。

### 3.4 全局联合优化与 Alpha 合成渲染

为生成连贯的交互场景，通过 Alpha 合成将 H-NeRF 和 O-NeRF 的渲染结果融合为单一交互图像 $x^{I}$：

$$
x^{I} = \sum_i w_i^{I} c_i^{I}, \quad w_i^{I} = \alpha_i^{I} \prod_{j=1}^{i-1} (1 - \alpha_j^{I}), \quad c_i^{I} = \frac{\alpha_i^{H}}{\alpha_i^{H} + \alpha_i^{O}} c_i^{H} + \frac{\alpha_i^{O}}{\alpha_i^{H} + \alpha_i^{O}} c_i^{O} \tag{6}
$$

其中 $\alpha_i^{H}$、$c_i^{H}$ 和 $\alpha_i^{O}$、$c_i^{O}$ 分别为人体和物体 NeRF 在采样点 $i$ 处的密度和颜色，$\alpha_i^{I} = \alpha_i^{H} + \alpha_i^{O}$ 为合成密度。交互场景的 SDS 梯度同时流向两个 NeRF，但流向人体模型的梯度被截断，以维持优化平衡。

### 3.5 总损失函数

最终优化目标为各损失项的加权组合，权重采用退火策略动态调整：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{SDS}}^{H} + \lambda_{1} \mathcal{L}_{\mathrm{SDS}}^{O} + \mathcal{L}_{\mathrm{geo}}^{H} + \lambda_{2} \mathcal{L}_{\mathrm{geo}}^{O} + \lambda_{3} L_{\mathrm{reg}} \tag{8}
$$

其中 $\mathcal{L}_{\mathrm{SDS}}^{H}$ 和 $\mathcal{L}_{\mathrm{SDS}}^{O}$ 分别为人体和物体的 SDS 损失，$\mathcal{L}_{\mathrm{geo}}^{H}$ 和 $\mathcal{L}_{\mathrm{geo}}^{O}$ 为对应的几何约束损失，$L_{\mathrm{reg}}$ 为正则化项（如密度正则），$\lambda_{1}$、$\lambda_{2}$、$\lambda_{3}$ 为动态权重系数。

## 实验与分析

### 核心性能与基线对比

InterFusion 在自定义的 61 类文本提示基准（涵盖 13 种交互类型）上进行了系统评估。该基准由 ChatGPT 生成，确保交互类别均匀分布，避免评估偏向特定类型。所有基线方法均基于 threestudio 框架实现，采用相同的多分辨率哈希网格表示和 DeepFloyd 扩散模型引导，保证公平比较。

**Table 1** 报告了 CLIP score 和 GPT-4V 选择率两项核心指标。InterFusion（Ours-HC）在 CLIP score 上达到 0.3308，超越最强基线 Ours-OC（0.3203）约 0.0281，远超 DreamFusion（0.3027）、Magic3D（0.3179）和 TextMesh（0.2761）。在 GPT-4V 选择率上，InterFusion 以 65.57% 的压倒性优势领先，而最强基线 Ours-OC 仅为 13.11%，DreamFusion 和 Magic3D 分别只有 8.20% 和 11.48%，TextMesh 更是低至 1.64%。这一巨大差距表明，CLIP score 虽然能反映语义一致性，但对几何完整性和物理交互正确性的敏感度不足——GPT-4V 作为半自动评判，能更精准地捕捉生成场景中的人-物空间关系是否合理。

**Table 3** 进一步引入了 MVDream 和 **ProlificDreamer**（Wang et al., NeurIPS 2024）等更强基线，并补充了 CLIP R-Precision 和 FID_CLIP 指标。InterFusion 的 R-Precision 达到 83.6%，比 MVDream（77.0%）高出 6.6 个百分点；FID_CLIP 降至 63.7，优于 MVDream 的 65.5 和 ProlificDreamer 的 64.8。这些结果一致表明，解耦生成策略和锚定姿态先验在保持语义保真度的同时，显著提升了生成质量。

**Figure 4** 的定性对比揭示了基线方法的典型失败模式：DreamFusion 和 Magic3D 常产生人体与物体的语义混淆（如人体部位融入物体几何），TextMesh 则因隐式 SDF 表示的限制，难以生成完整的交互场景。相比之下，InterFusion 能稳定生成人体与物体空间关系正确、纹理细节丰富的 3D 场景。

### 消融实验：损失项的作用机制

**Table 2** 和 **Figure 5** 通过系统消融揭示了各损失项的关键贡献。

**交互 SDS 损失（SDS-I）** 的移除导致性能崩溃：GPT-4V 选择率从 77.05% 暴跌至 1.64%，CLIP score 也从 0.3308 降至 0.2959。这表明，仅靠人体和物体的独立优化无法建立正确的交互语义——模型需要从交互场景的联合渲染中获取空间-语义联合引导，才能将人体和物体“对齐”到合理的相对位置。

**物体 SDS 损失（SDS-O）** 的移除使 GPT-4V 选择率降至 4.92%。这说明物体独立优化分支对完整交互生成必不可少：若仅依赖交互场景的 SDS 梯度，物体生成容易退化为人体几何的附属物，丧失独立的语义完整性。

**物体几何约束（L_geo^O）** 的消融结果尤为关键：GPT-4V 选择率降至 16.39%，**Figure 5b** 显示物体容易在原点附近退化或直接穿透人体。该约束通过交叉熵损失强制物体 NeRF 不占用锚定姿态内部的采样点，本质上是将人体占位信息作为物体生成的“禁区”先验。缺少这一约束时，SDS 梯度缺乏足够的空间排斥力来阻止穿透，导致物理交互错误。

### 失败模式与局限性

尽管 InterFusion 在整体指标上表现优异，但存在以下已知局限：

1. **局部接触区域精度不足**：手部等精细交互部位仍可能出现穿透现象。框架缺乏专门的手部/接触区域优化模块，仅依赖全局几何约束难以完全解决局部穿透问题。
2. **静态场景限制**：当前生成结果为静态 3D 场景，无法表示交互过程的动作序列，限制了在动态 HOI 理解任务中的应用。
3. **预训练模型依赖**：生成质量受限于底层视觉语言模型（VLM）的能力边界，对复杂或罕见交互描述的泛化能力有待验证。

这些失败模式指向了明确的研究方向：引入手部精细化模块、扩展至 4D 动态生成、以及利用大语言模型自动拆解复杂交互文本以生成更精细的时空约束。

### 补充图表

![[assets/figures/papers/paper_list_l1762_InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation of CLIP score and GPT-4V select*

![[assets/figures/papers/paper_list_l1762_InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction/figures/007_Table_2.jpg]]
*Table 2: Quantitative results of ablation studies*

![[assets/figures/papers/paper_list_l1762_InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison results with baselines. InterFuion generates more stable and higher-quality results and is more consistent with input interaction descriptions*

![[assets/figures/papers/paper_list_l1762_InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction/figures/009_Figure_7.jpg]]
*Figure 7: Comparison between the object-centric baseline (Ours-OC) and InterFusion (Ours-HC) across multiple views, given the text prompt "a man with a full beard wearing a flannel shirt riding a bike" (top) and "a man in a rugby jersey and cotton shorts playing the guitar" (bottom)*

![[assets/figures/papers/paper_list_l1762_InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction/figures/010_Table_3.jpg]]
*Table 3: Quantitative comparisons of more baselines and metrics*

![[assets/figures/papers/paper_list_l1762_InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction/figures/012_Figure_9.jpg]]
*Figure 9: Visual ablations across multiple views for loss terms during the pose-guided generation process, given the text prompt "a man wearing a red baseball cap playing the guitar" (top) and "a person in a paisley print shirt and corduroy pants sitting on a chair" (bottom)*

![[assets/figures/papers/paper_list_l1762_InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction/figures/003_Figure_3.jpg]]
*Figure 3: More results generated by InterFusion. Diverse integration poses are supported. Numerous human and object styles are also supported*

![[assets/figures/papers/paper_list_l1762_InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction/figures/008_Figure_6.jpg]]
*Figure 6: Additional qualitative comparison results with baseline methods*

![[assets/figures/papers/paper_list_l1762_InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction/figures/011_Figure_8.jpg]]
*Figure 8: Comparisons with recent avatar generation methods, given the text prompt "a man with blond hair wearing a brown leather jacket"*

![[assets/figures/papers/paper_list_l1762_InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction/figures/013_Figure_10.jpg]]
*Figure 10: InterFuison provides a flexible way for controllable editing of human-object interactions, enabling geometry and texture manipulations for either humans or objects through simple adjustments in the corresponding text prompts*


## 方法谱系与知识库定位

### 1. 核心瓶颈与突破路径

文本驱动的3D人-物交互（HOI）生成面临双重挑战：**（1）数据稀缺**——缺乏成对的文本-交互3D数据，导致直接生成时人体、物体和交互语义严重混淆；**（2）空间建模困难**——扩散模型难以同时建模多个具有复杂空间关系的概念。InterFusion的核心突破在于将HOI生成分解为**锚定姿态估计**与**姿态引导的分离优化**两阶段：先从大规模合成图像中构建文本-姿态码本，检索出几何锚点；再以该姿态为约束，解耦人体NeRF和物体NeRF的生成，通过局部SDS优化与全局联合调整实现连贯的交互场景。

### 2. 与基线方法的关系

#### 2.1 相对于通用text-to-3D方法的改进

InterFusion直接对比了DreamFusion、Magic3D、TextMesh、MVDream和ProlificDreamer（Wang et al., NeurIPS 2024）等通用text-to-3D方法。这些基线均采用单一NeRF或SDF表示联合生成整个场景，缺乏对HOI任务中多概念空间关系的显式建模。实验表明（Table 1, Table 3），通用方法在HOI任务上存在两类典型失败模式：

- **语义混淆**：如“a man riding a bike”提示下，DreamFusion和Magic3D生成的人体与自行车融为一体，无法区分独立实体（Figure 4）。
- **交互缺失**：TextMesh和ProlificDreamer常忽略交互动作本身，仅生成孤立的人体或物体。

InterFusion通过引入人体姿态先验和解耦优化策略，在CLIP score上达到0.3308（对比最强基线MVDream的0.3203），GPT-4V选择率65.57%（对比最强基线Ours-OC的13.11%），证明几何先验对HOI生成的决定性作用。

#### 2.2 消融基线Ours-OC的启示

Ours-OC是用物体几何先验替代人体姿态先验的消融基线。其GPT-4V选择率仅13.11%，远低于Ours-HC的65.57%（Table 1）。多视角对比（Figure 7）显示，物体中心策略无法为人体生成提供有效空间约束，导致人体姿态与交互描述严重偏离。这验证了**人体姿态作为锚定几何先验的不可替代性**——人体是交互动作的主动执行者，其空间配置直接定义了交互的语义和物理约束。

#### 2.3 与人体化身生成方法的关系

InterFusion与近期人体化身生成方法（如Figure 8所示对比）共享SDS优化范式，但关键区别在于：化身方法仅关注人体本身的生成质量，而InterFusion将人体置于交互上下文中，通过交互SDS损失和物体几何约束确保人-物空间关系的正确性。消融实验（Table 2）表明，移除交互SDS损失后GPT-4V选择率从77.05%暴跌至1.64%，证明交互语义引导是区分HOI生成与单纯人体生成的核心机制。

### 3. 适用边界与局限

#### 3.1 技术依赖边界

InterFusion的性能受限于预训练视觉语言模型的能力上限。其锚定姿态检索依赖CLIP的文本-图像对齐质量，SDS优化依赖DeepFloyd扩散模型的生成先验。论文明确指出，随着基础模型的进步，框架效果会直接提升——这意味着当前方法的**上限由外部模型决定，而非框架本身**。

#### 3.2 局部交互精度不足

尽管全局交互结构合理，但局部接触区域（尤其是手部）仍存在穿透现象。框架缺乏专门的手部/接触区域精细化模块，这是导致局部交互不准确的结构性原因。Figure 5b的消融可视化显示，移除物体几何约束后穿透问题急剧恶化，说明现有约束只能提供粗粒度的空间占位控制。

#### 3.3 静态场景限制

当前方法仅生成静态3D场景，无法表示交互过程的动作序列。这限制了其在需要动态运动理解的应用场景（如动作识别数据增强、物理模拟）中的使用。框架的两阶段设计在理论上可扩展至时间维度，但需要解决时序一致性和运动先验的引入问题。

### 4. 开放问题

1. **精细化接触建模**：如何在框架中加入专门的手部/接触区域优化模块，解决局部穿透问题？可能的路径包括引入手部参数化模型（如MANO）或接触场预测网络。

2. **动态HOI生成**：如何将静态HOI生成框架扩展至4D（3D+时间），实现文本驱动的动态人-物交互序列生成？这需要解决时序SDS优化、运动先验构建和跨帧一致性约束等挑战。

3. **复杂交互的自动拆解**：如何利用大语言模型自动解析复杂交互文本（如“a person picks up a cup, drinks, and puts it down”），生成分阶段的时空约束？这涉及高层任务规划与底层几何生成的深度耦合。

4. **多物体交互场景**：当前框架仅支持单人-单物交互，扩展到多物体或多人的交互场景需要解决更复杂的空间关系建模和遮挡处理问题。

## 原文 PDF

![[paperPDFs/ECCV_2024/InterFusion_Text_Driven_Generation_of_3D_Human_Object_Interaction.pdf]]