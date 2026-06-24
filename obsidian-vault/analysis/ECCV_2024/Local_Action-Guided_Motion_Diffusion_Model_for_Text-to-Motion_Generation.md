---
title: Local Action-Guided Motion Diffusion Model for Text-to-Motion Generation
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Local_Action_Guided_Motion_Diffusion_Model_for_Text_to_Motion_Generation.pdf
project_link: "https://jpthu17.github.io/GuidedMotion-project/"
code_link: "https://github.com/qrzou/locomotion"
aliases:
- LAGMDMTMG
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 每个局部动作的引导权重 λ（由图形注意力网络学习并可手动调整），通过改变权重值可以连续地控制局部动作对全局运动的影响程度。
primary_logic: 将全局运动生成分解为局部动作的先验采样和层次化引导扩散：利用语义图将全局描述解构为多个局部动作，并通过能量函数和图形注意力网络在扩散过程中的动作级别施加局部动作的条件引导，实现了从局部到全局的可控生成，降低了生成复杂性，提高了运动的多样性和可控性。
claims:
- 在HumanML3D数据集上，GuidedMotion的FID达到0.057，相比基线MLD的0.473显著降低，表明生成质量大幅提升。
- 在复杂动作子集上，GuidedMotion在大部分指标上优于其他方法，证明了局部动作引导在复杂运动生成中的有效性。
- 消融研究表明，加入局部动作引导后，FID从0.473降至0.057，R-Precision Top-3从0.772提升至0.788。
- HumanML3D 上 FID = 0.057
---

# Local Action-Guided Motion Diffusion Model for Text-to-Motion Generation

> [!tip] 核心洞察
> 将全局运动生成分解为局部动作的先验采样和层次化引导扩散：利用语义图将全局描述解构为多个局部动作，并通过能量函数和图形注意力网络在扩散过程中的动作级别施加局部动作的条件引导，实现了从局部到全局的可控生成，降低了生成复杂性，提高了运动的多样性和可控性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于局部动作引导的运动扩散模型用于文本到运动生成 |
| 英文题名 | Local Action-Guided Motion Diffusion Model for Text-to-Motion Generation |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2407.10528) · [Project](https://jpthu17.github.io/GuidedMotion-project/) · [Code](https://github.com/qrzou/locomotion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GuidedMotion |
| Dataset | HumanML3D, KIT, Complex Motion Subset |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.057 vs 0.473 (MLD) (-0.416)；R-Precision Top-1 0.503 vs 0.481 (MLD) (+0.022)。
> - KIT 上，FID 0.213 vs 0.404 (MLD) (-0.191)；R-Precision Top-1 0.430 vs 0.390 (MLD) (+0.040)。
> - Complex Motion Subset (HumanML3D) 上，FID 0.144 vs 0.441 (MLD, estimated from context) (-0.297)。

## 概述

**问题瓶颈**：现有文本到运动生成方法（如MLD、MDM、T2M-GPT）主要关注直接合成全局运动，忽略了运动序列中普遍存在的多个局部动作的细粒度生成与控制。如图5所示，大多数运动包含2个以上的局部动作，但现有方法缺乏对局部动作的显式建模，导致在合成复杂运动时生成结果与用户意图存在偏差，运动多样性和可控性受限。

**核心洞察**：将全局运动生成分解为局部动作的先验采样和层次化引导扩散。利用语义图将全局描述解构为多个局部动作，并通过能量函数和图形注意力网络在扩散过程中施加动作级别的局部动作条件引导，实现从局部到全局的可控生成，降低生成复杂性，提升运动多样性与可控性。

**方法定位**：GuidedMotion以**MLD**（Chen et al., CVPR 2023）为基础扩散模型，在四个关键维度上进行了改进：(1) 条件信号从单一的全局文本描述扩展为全局文本 + 多个局部动作参考；(2) 扩散过程从单层扩展为运动级、动作级、细节级三层层次扩散；(3) 引入基于能量函数的局部动作梯度引导机制，由图形注意力网络自动估计每个局部动作的引导权重λ；(4) 通过语义图解析和MLD自动采样生成局部动作参考，无需人工标注。

**因果机制**：每个局部动作的引导权重λ由图形注意力网络学习并可手动调整。改变λ值可以连续控制局部动作对全局运动的影响程度（见图7），这是实现细粒度可控生成的关键控制变量。

**主要结果**（决定性证据）：
- 在HumanML3D数据集上，GuidedMotion的FID达到**0.057**，相比基础模型MLD的0.473降低**0.416**，R-Precision Top-1从0.481提升至**0.503**（Table 1）。
- 在KIT数据集上，FID从MLD的0.404降至**0.213**，R-Precision Top-1从0.390提升至**0.430**（Table 2）。
- 在包含至少3个局部动作且长度≥150帧的复杂运动子集上，GuidedMotion在大部分指标上优于其他方法，FID为**0.144**（Table 3）。
- 消融研究证实：移除局部动作引导后FID从0.057升高至0.473，R-Precision Top-3从0.788下降至0.772，验证了局部动作引导的核心作用（Table 4）。

**局限与待验证问题**：生成运动受限于数据集最大长度，无法建模超出该长度的连续动作序列；方法在潜在空间扩散，难以进行低级编辑（如修改单个关节位置）；扩散模型的固有随机性可能导致偶尔不良的生成结果。这些限制需要在后续研究中进一步验证和改进。

## 背景与动机

### 文本到运动生成的核心瓶颈

文本到运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，扩散模型在该领域取得了显著进展，代表性工作包括 **MDM**（Tevet et al., ICLR 2023）、**MLD**（Chen et al., CVPR 2023）、**T2M-GPT**（Zhang et al., CVPR 2023）、**MotionDiffuse**（Zhang et al., TPAMI 2024）和 **ReMoDiffuse**（Zhang et al., ICCV 2023）等。

然而，现有方法存在一个根本性瓶颈：它们主要关注直接合成全局运动，忽略了对局部动作的生成和精确控制。真实的人体运动通常由多个局部动作组合而成——例如“一个人先走几步，然后弯腰捡起东西，再转身离开”包含了行走、弯腰、转身等多个局部动作。图5的统计分布也证实，运动序列通常包含多个局部动作，而非单一动作。当合成此类复杂运动时，缺乏局部动作层面的细粒度引导会导致生成结果与用户意图存在偏差，生成的运动可能在局部动作的语义准确性、时序连贯性或组合多样性上表现不佳。

### 现有方法的缺口

具体而言，现有方法的条件信号仅使用全局文本描述，扩散过程为单层结构，且无显式的局部引导机制。这种“从全局到全局”的生成范式面临两个关键困难：

1. **生成复杂性高**：模型需要一次性从文本描述中推断出所有局部动作及其时序关系，随着动作数量增加，生成难度急剧上升。
2. **可控性不足**：用户无法对特定局部动作施加偏好或调整，生成结果的多样性完全依赖于扩散模型的随机性，缺乏细粒度的操控手段。

### 本文动机与核心思路

针对上述缺口，本文提出 **GuidedMotion**，核心洞察是将全局运动生成分解为局部动作的先验采样和层次化引导扩散。具体而言，方法利用语义图将全局描述解构为多个局部动作，并通过能量函数和图注意力网络在扩散过程中施加动作级别的局部动作条件引导，实现从局部到全局的可控生成。这一设计降低了生成复杂性，同时赋予用户对每个局部动作的引导权重进行连续调节的能力，从而提高了运动的多样性和可控性。

## 核心创新

### 问题瓶颈：全局生成缺乏局部动作的细粒度控制

现有文本到运动生成方法（如 **MLD** (Chen et al., CVPR 2023)、**MDM** (Tevet et al., ICLR 2023)、**T2M-GPT** (Zhang et al., CVPR 2023)）主要关注从全局文本描述直接合成完整运动序列，忽略了运动内在的层次结构——一个复杂运动通常由多个局部动作组合而成（Figure 5 显示多数运动包含多个局部动作）。这种“一步到位”的生成范式导致两个关键缺陷：

1. **缺乏细粒度引导**：模型仅以全局文本为条件，无法对构成运动的各个局部动作施加独立控制，生成结果容易偏离用户的精确意图。
2. **复杂运动合成质量下降**：当运动包含多个动作且序列较长时，全局生成难以协调各动作之间的时序关系和语义一致性，导致动作退化或语义错位（Figure 4 的定性对比印证了这一点）。

### 核心洞察：从局部到全局的层次化可控生成

GuidedMotion 的核心创新在于**将全局运动生成分解为局部动作的先验采样与层次化引导扩散**。其关键思路是：利用语义图将全局描述解构为多个局部动作节点及其关系边，然后以这些局部动作作为细粒度控制信号，在扩散生成过程中逐层次地引导运动合成——从运动级（motion level）到动作级（action level）再到细节级（specific level），实现从粗到精的可控生成。

### 方法层面的关键改变（Changed Slots）

相对于以 MLD 为代表的基线方法，GuidedMotion 在四个核心维度上引入了实质性改变：

**1. 条件信号：从单一全局文本到“全局文本 + 多局部动作参考”**

基线方法仅使用全局文本描述 $c$ 作为条件信号。GuidedMotion 通过语义图解析器（Semantic Graph Parser）将原始运动描述自动解构为多个局部动作描述，并利用预训练的 MLD 模型为每个局部动作生成参考运动片段（Local Action Sampler）。这些参考局部动作作为附加条件信号 $c^k$（$k=1,\dots,K$）注入扩散过程，为全局运动合成提供了显式的局部语义锚点。

**2. 引导机制：从无条件生成到基于能量函数的局部动作梯度引导**

基线扩散模型的反向过程仅依赖无条件得分 $\nabla_{z_t} \log p(z_t)$ 和全局文本条件得分。GuidedMotion 引入了基于能量函数的多项引导机制，将条件得分分解为：

$$\nabla_{z_t} \log p(z_t | c) = \nabla_{z_t} \log p(z_t) + \sum_{k=1}^K \nabla_{z_t} \log p(c^k | z_t)$$

其中每个局部动作条件 $c^k$ 对应一个能量函数 $\mathcal{E}(c^k, z_t)$，其梯度 $\nabla_{z_t} \mathcal{E}(c^k, z_t)$ 在反向过程中作为修正项，引导生成运动与参考局部动作对齐。最终的反向步骤为：

$$z_{t-1} = \tilde{z}_{t-1} - \sum_{k=1}^K \lambda_t^k \nabla_{z_t} \mathcal{E}(c^k, z_t)$$

其中 $\lambda_t^k$ 是每个局部动作的引导权重。

**3. 引导权重的自适应估计：图注意力网络替代固定权重**

引导权重 $\lambda_t^k$ 并非手工设定，而是由**图注意力网络（GAT）** 从语义图中自动学习。具体而言，语义图中的节点嵌入 $\mathbf{v}_i$ 经过线性变换和拼接后输入注意力模块：

$$\tilde{\mathbf{h}}_{ij} = [\mathbf{W}\mathbf{v}_i, \mathbf{W}\mathbf{v}_j]$$

注意力系数结合了共享变换 $\mathbf{M}$ 和关系特定变换 $\mathbf{M}_r$（根据边类型 $\mathbf{R}_{ij}$）：

$$e_{ij} = \sigma(\mathbf{M}^{\top} \tilde{\mathbf{h}}_{ij}) + \sigma(\mathbf{R}_{ij} \mathbf{M}_r^{\top} \tilde{\mathbf{h}}_{ij})$$

归一化后的注意力系数 $\tilde{e}^k$ 经缩放因子 $\rho_t$ 调整后直接作为引导权重 $\lambda_t^k = \rho_t \tilde{e}^k$。这一设计的**因果调节旋钮**在于：用户可以在推理时手动调整各局部动作的 $\lambda$ 值，连续地控制每个动作对全局运动的影响程度（Figure 7 展示了调整 $\lambda$ 的可视化效果），实现了从自动学习到手动微调的灵活可控。

**4. 扩散过程层次：从单层到三层层次化扩散**

基线方法在单一层次上进行扩散去噪。GuidedMotion 将扩散过程拆分为三个语义层次，每个层次对应一个独立的 Transformer 去噪网络：

- **运动级（Motion Level）**：捕获整体运动轨迹，以运动级语义节点 $\mathcal{V}^m$ 为条件，训练损失为 $\mathcal{L}_M = \mathbb{E}[\| \epsilon^m - \phi_m(z^m, t^m, \mathcal{V}^m) \|_2^2]$。
- **动作级（Action Level）**：以运动级输出 $z^m$ 和动作级节点 $\mathcal{V}^a$ 为条件，训练损失为 $\mathcal{L}_A = \mathbb{E}[\| \epsilon^a - \phi_a(z^a, t^a, [\mathcal{V}^m, \mathcal{V}^a, z^m]) \|_2^2]$。**局部动作引导仅施加于此层次**，以保证生成稳定性。
- **细节级（Specific Level）**：以动作级输出 $z^a$ 和所有层次节点 $[\mathcal{V}^m, \mathcal{V}^a, \mathcal{V}^s]$ 为条件，训练损失为 $\mathcal{L}_S = \mathbb{E}[\| \epsilon^s - \phi_s(z^s, t^s, [\mathcal{V}^m, \mathcal{V}^a, \mathcal{V}^s, z^a]) \|_2^2]$。

三个层次级联训练，总损失为 $\mathcal{L} = \mathcal{L}_M + \mathcal{L}_A + \mathcal{L}_S$。消融实验（Table 4）证实，从运动级到细节级的递进生成带来性能的逐步提升。

### 创新有效性的决定性证据

消融研究（Table 4）提供了最直接的因果证据：当移除局部动作引导后，FID 从 **0.057 急剧升高至 0.473**（与 MLD 基线持平），R-Precision Top-3 从 **0.788 降至 0.772**。这一对比清晰表明，局部动作引导是性能提升的核心驱动力，而非层次化架构或 VAE 的附带效果。在复杂动作子集（≥3 个局部动作，≥150 帧）上的实验（Table 3）进一步验证了该方法在协调多动作、长序列运动合成中的独特优势。

## 整体框架

GuidedMotion 的整体框架围绕一个核心思想展开：将全局运动生成分解为局部动作的先验采样与层次化条件扩散，从而实现对复杂运动的细粒度可控合成。图2展示了该框架的完整数据流。

**输入与语义解析。** 系统接收一段描述完整运动的自然语言文本（例如“一个人先向前走，然后蹲下捡起东西”）。首先通过**语义图解析器（Semantic Graph Parser）** 将该描述解构为一张有向语义图。图中的节点分为三个语义层级——运动（motion）、动作（action）和细节（specific），边则编码了节点间的语义关系类型（见 Table A）。这一解析步骤将全局描述显式地分解为多个局部动作及其上下文关联，为后续的层次化处理提供了结构化条件。

**局部动作参考生成。** 语义图中每个动作节点对应一个局部动作描述。**局部动作采样器（Local Action Sampler）** 使用一个预训练的文本到运动模型 **MLD**（Chen et al., CVPR 2023），根据这些局部动作描述独立生成参考局部动作序列。这些参考动作作为附加条件信号，在后续的全局运动生成中提供细粒度引导。值得注意的是，局部动作可以预生成，因此不会计入推理时间开销（见 Table B）。

**层次化运动扩散。** 全局运动的合成在潜在空间中进行，由一个**运动变分自编码器（Motion VAE）** 将运动序列压缩到三个语义层级的潜在表示：运动级 $z^m$、动作级 $z^a$ 和细节级 $z^s$。对应的**层次化扩散去噪器（Hierarchical Diffusion Denoiser）** 由三个 Transformer 网络组成，分别负责这三个层级的去噪预测。扩散过程从运动级开始，逐步细化到动作级和细节级，形成由粗到精的生成管线：
- 运动级模型以运动节点的图嵌入为条件，预测噪声 $\epsilon^m$，生成运动的全局轮廓。
- 动作级模型以运动级输出 $z^m$ 以及运动、动作节点的嵌入为条件，预测噪声 $\epsilon^a$。
- 细节级模型以动作级输出 $z^a$ 以及全部三个层级的节点嵌入为条件，预测噪声 $\epsilon^s$。

三个层级的训练目标分别由公式 (10)–(12) 给出，总损失为三者之和 $\mathcal{L} = \mathcal{L}_M + \mathcal{L}_A + \mathcal{L}_S$。

**局部动作能量引导。** 框架的关键创新在于动作级扩散过程中注入的**基于能量的局部动作引导（Energy-based Local Action Guidance）**。在动作级去噪的每一步，系统计算当前生成的动作潜在表示与各参考局部动作之间的能量函数梯度，并将其作为修正项加入反向扩散过程（公式 (5)）。每个局部动作的引导强度由一个可学习的权重 $\lambda_t^k$ 控制。

**图注意力权重估计。** 引导权重 $\lambda_t^k$ 并非固定，而是由**图注意力权重估计器（Graph Attention Weight Estimator）** 动态计算。该模块使用图注意力网络（GAT），以语义图中动作节点与运动节点的嵌入拼接作为输入（公式 (6)），通过结合共享变换矩阵 $\boldsymbol{M}$ 和关系特定变换矩阵 $\boldsymbol{M}_r$ 计算注意力系数 $e_{ij}$（公式 (7)），最终由注意力系数和缩放因子 $\rho_t$ 确定每个局部动作的引导权重（公式 (8)）。这一机制使得模型能够根据语义上下文自适应地平衡不同局部动作对全局运动的影响程度。

**输出与可控性。** 细节级扩散的最终输出经 Motion VAE 解码器重建为完整的运动序列。用户可以通过手动调整各局部动作的引导权重 $\lambda$，连续地控制某个局部动作在最终运动中的表现强度（见 Figure 7），实现了从局部到全局的可控运动生成。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework of GuidedMotion for controllable text-tomotion generation. We propose to employ reference local actions as control signals in the global motion generation process. To automatically obtain these local actions, we deconstruct the original motion description into multiple local action descriptions and utilize a text-to-motion model to generate these local actions*

## 核心模块与公式推导

GuidedMotion 的核心设计是将全局运动生成分解为局部动作引导的层次化扩散过程。方法包含三个关键模块：**基于语义图的局部动作采样**、**基于能量函数的局部动作引导**，以及**层次化运动扩散架构**。

### 局部动作采样与语义图构建

给定全局运动描述，系统首先通过语义图解析器将描述解构为多层语义图（运动级、动作级、细节级节点及边关系，详见 Table A）。随后，利用预训练的 **MLD** 模型（Chen et al., CVPR 2023）根据每个局部动作描述独立生成参考局部动作序列。这些参考动作作为后续全局生成的条件信号，为扩散过程提供细粒度引导。

### 基于能量函数的局部动作引导

条件扩散模型的反向过程可表述为：

$$z_{t-1} = (1 + \frac{1}{2} \beta_t) z_t + \beta_t \nabla_{z_t} \log p(z_t | c) + \sqrt{\beta_t} \epsilon \quad \text{(Eq. 1)}$$

利用贝叶斯分解，条件得分可拆分为无条件得分与修正梯度之和：

$$\nabla_{z_t} \log p(z_t | c) = \nabla_{z_t} \log p(z_t) + \nabla_{z_t} \log p(c | z_t) \quad \text{(Eq. 2)}$$

修正梯度通过能量函数 $\mathcal{E}(c, z_t)$ 的梯度近似：$\nabla_{z_t} \log p(c | z_t) \propto -\nabla_{z_t} \mathcal{E}(c, z_t)$。对于多个局部动作 $c^k$，反向过程扩展为多引导项形式：

$$z_{t-1} = \tilde{z}_{t-1} - \sum_{k=1}^K \lambda_t^k \nabla_{z_t} \mathcal{E}(c^k, z_t) \quad \text{(Eq. 5)}$$

其中 $\lambda_t^k$ 是每个局部动作的引导权重，由**图注意力权重估计器**动态计算。该模块将语义图中的节点嵌入 $\mathbf{v}_i$ 经变换后拼接为边输入：

$$\tilde{\mathbf{h}}_{ij} = [\mathbf{h}_i, \mathbf{h}_j] = [\mathbf{W}\mathbf{v}_i, \mathbf{W}\mathbf{v}_j] \quad \text{(Eq. 6)}$$

注意力系数结合共享变换 $\mathbf{M}$ 和关系特定变换 $\mathbf{M}_r$：

$$e_{ij} = \sigma(\mathbf{M}^{\top} \tilde{\mathbf{h}}_{ij}) + \sigma(\mathbf{R}_{ij} \mathbf{M}_r^{\top} \tilde{\mathbf{h}}_{ij}) \quad \text{(Eq. 7)}$$

最终引导权重由归一化注意力系数与缩放因子 $\rho_t$ 确定：

$$\lambda_t^k = \rho_t \tilde{e}^k \quad \text{(Eq. 8)}$$

节点嵌入通过注意力聚合与跳跃连接更新：

$$\mathcal{V}_i = \sigma' \big( \sum_{j \in \mathbb{N}_i} \tilde{e}_{ij} \mathbf{h}_j \big) + \mathbf{v}_i \quad \text{(Eq. 9)}$$

这一机制使得每个局部动作的引导强度可根据语义上下文自适应调节，用户也可手动调整 $\lambda$ 实现精细控制（见 Figure 7）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/012_Figure_7.jpg]]
*Figure 7: The proposed GuidedMotion controls the generation process of motion diffusion models. Our method provides flexibility in adjusting the guiding weight λ of each local action, enabling fine-grained control over global motion*

### 层次化运动扩散架构

运动变分自编码器将运动序列编码至三个语义层次的潜在空间：运动级（token 数 $Q^m=2$）、动作级（$Q^a=4$）、细节级（$Q^s=8$），潜在维度 $D'=256$。对应的三个 Transformer 去噪网络以级联方式工作，训练目标分别为：

运动级损失：
$$\mathcal{L}_M = \mathbb{E}_{z,\epsilon,t} \Big[ \| \epsilon^m - \phi_m(z^m, t^m, \mathcal{V}^m) \|_2^2 \Big] \quad \text{(Eq. 10)}$$

动作级损失（以运动级输出为条件）：
$$\mathcal{L}_A = \mathbb{E}_{z,\epsilon,t} \Big[ \| \epsilon^a - \phi_a(z^a, t^a, [\mathcal{V}^m, \mathcal{V}^a, z^m]) \|_2^2 \Big] \quad \text{(Eq. 11)}$$

细节级损失（以动作级输出为条件）：
$$\mathcal{L}_S = \mathbb{E}_{z,\epsilon,t} \Big[ \| \epsilon^s - \phi_s(z^s, t^s, [\mathcal{V}^m, \mathcal{V}^a, \mathcal{V}^s, z^a]) \|_2^2 \Big] \quad \text{(Eq. 12)}$$

总训练目标为三者之和 $\mathcal{L} = \mathcal{L}_M + \mathcal{L}_A + \mathcal{L}_S$。局部动作引导仅在动作级施加，以保证生成稳定性（见 Figure 3）。消融实验表明，从运动级到细节级逐步细化能持续提升生成质量，细节级 VAE 在 HumanML3D 上的重建 FID 低至 0.019（Table C）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/003_Figure_3.jpg]]
*Figure 3: The model architecture of the hierarchical motion diffusion model. Utilizing the semantic graph as input, the hierarchical diffusion model dissects the textto-motion diffusion process into three semantic levels, which correspond to capturing the overall motion, local actions, and action specifics. To enhance generation stability, we exclusively implement local action guidance at the action level*

## 实验与分析

### 主实验结果

GuidedMotion在两个标准人体运动生成基准上均取得了最优性能，尤其在生成质量（FID）上实现了跨越式提升。

在HumanML3D测试集上（Table 1），GuidedMotion的FID达到**0.057**，相比基础扩散模型MLD的0.473降低了**87.9%**，在所有对比方法中排名第一。R-Precision Top-1为0.503，优于MLD的0.481，表明生成运动与文本描述的对齐程度更高。其他指标如MultiModal Distance（3.016）和Diversity（9.410）同样具有竞争力。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/005_Table_1.jpg]]
*Table 1: Comparisons to current state-of-the-art methods on the HumanML3D test set. “↑” denotes that higher is better. “↓” denotes that lower is better. “→” denotes that results are better if the metric is closer to the real motion. We repeat all the evaluations 20 times and report the average with a 95% confidence interval. Bold and underlined indicate the best and second-best results, respectively*

在KIT测试集上（Table 2），GuidedMotion同样保持领先：FID为**0.213**（MLD为0.404），R-Precision Top-1为0.430（MLD为0.390），验证了方法的跨数据集泛化能力。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/006_Table_2.jpg]]
*Table 2: Comparisons to other methods on the KIT test set. We repeat all the evaluations 20 times and report the average with a 95% confidence interval. Bold and underlined indicate the best and second-best results, respectively*

值得注意的是，GuidedMotion在FID上的优势远大于R-Precision等语义对齐指标。这一现象与方法的因果机制一致：局部动作引导的核心作用是约束生成运动的细粒度结构，使其更接近真实运动分布（从而大幅降低FID），而非仅改善全局语义匹配。

### 复杂运动子集评估

为验证局部动作引导在复杂运动生成中的有效性，论文从HumanML3D测试集中筛选出包含至少3个局部动作且长度≥150帧的样本构成复杂运动子集（Table 3）。在该子集上，GuidedMotion在FID、R-Precision等大部分指标上优于所有对比方法。这一结果直接支撑了核心主张：当运动包含多个局部动作时，层次化局部引导能有效降低合成难度，避免全局方法在长序列、多动作场景下的语义退化和运动失真。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/007_Table_3.jpg]]
*Table 3: Comparisons to other methods on the complex motion subset. We filter the HumanML3D test set containing at least 3 local actions and 150 frames or more in length as a new test set to verify the ability to generate complex motions*

### 消融研究

消融实验（Table 4）揭示了各组件的贡献层级：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/008_Table_4.jpg]]
*Table 4: Ablation study of each part on the HumanML3D test set*

**局部动作引导的核心作用。** 移除局部动作引导后，FID从0.057急剧上升至0.473，R-Precision Top-3从0.788降至0.772。这表明局部动作引导是性能提升的决定性因素——没有它，模型退化为标准全局扩散模型。

**层次化扩散的递进增益。** 从运动级（motion level）到动作级（action level）再到细节级（specific level），生成性能逐步提升。细节级别在R-Precision Top-3和FID上均达到最佳，验证了三个语义层次的递进建模能逐级细化运动细节，而非冗余堆叠。

**VAE token大小的重建能力。** 附录Table C显示，增加VAE的token大小（$Q^m=2 \to Q^a=4 \to Q^s=8$）能持续增强重建能力，细节级VAE在HumanML3D上的重建FID低至0.019。这为扩散模型提供了高质量潜在空间，是生成质量的基础保障。

### 推理效率分析

推理时间评估（Table B）表明，GuidedMotion采用DDIM采样（$T^m=T^a=T^s=50$）时，单样本推理时间与MLD基本持平。这是因为局部动作可预先生成，推理阶段仅需在动作级扩散过程中施加基于能量函数的梯度引导，额外计算开销可忽略。Table 6进一步验证了扩散步数配置对性能的影响，50步为最优平衡点。

### 失败模式与局限性

尽管整体性能优异，GuidedMotion存在以下约束：

1. **序列长度限制。** 生成运动受限于数据集中最大长度，无法建模超出该长度的连续动作序列。这是数据驱动的固有瓶颈，而非方法设计缺陷。
2. **低级编辑能力缺失。** 方法在潜在空间中进行扩散，适合高级运动编辑（如替换局部动作），但难以进行低级编辑（如修改单个关节位置）。这是潜在空间建模的固有权衡。
3. **扩散随机性。** 扩散模型的固有随机性可能导致偶尔不良的生成结果。论文未提供失败案例的定量统计，该点需手动验证。
4. **VAE性能依赖。** 方法的生成质量受限于预训练运动VAE的重建能力。当VAE对特定运动模式重建不足时，会向下游扩散模型传播误差。
5. **推理速度上限。** 尽管额外开销可忽略，推理速度仍受现有扩散模型框架限制，未突破扩散采样的根本效率瓶颈。

### 引导权重的可控性

Figure 7展示了调整引导权重$\lambda$的可视化效果：通过改变每个局部动作的引导权重，用户可以连续控制该动作对全局运动的影响程度。这一机制使GuidedMotion不仅是一个生成模型，更是一个可控编辑工具——用户可自由组合偏好的局部动作，生成符合心理意象的运动序列（Figure 1）。引导权重由图形注意力网络自动估计，同时支持手动调整，兼顾了自动化与灵活性。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/001_Figure_1.jpg]]
*Figure 1: Generating motion with diverse local actions. Different local actions correspond to distinct user preferences. Our method empowers users to combine preferred local actions freely, generating motions that align with their mental imagery. Furthermore, the combination of varied local actions enhances the motion diversity*

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparisons. The darker colors indicate the later in time. The motions generated by our method closely align with the descriptions, outperforming others that exhibit degraded motions or improper semantics*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative comparison of different hierarchical levels. The output at the higher level (e.g., specific level) contains more action details*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/010_Figure_5.jpg]]
*Figure 5: The distribution of the number of local actions in each motion. Motions typically consist of multiple local actions rather than just one local action*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_10528/figures/009_Table_6.jpg]]
*Table 6: Effect of diffusion steps on the HumanML3D test set. We use DDIM in practice and set*

## 方法谱系与知识库定位

**GuidedMotion** 的核心贡献在于将文本到运动生成从“全局描述→全局运动”的单层映射，重构为“全局描述→局部动作引导→层次化运动扩散”的多阶段可控生成范式。该方法的方法论定位、与基线工作的关系及适用边界如下。

### 与基线方法的关系

GuidedMotion 直接建立在 **MLD**（Chen et al., CVPR 2023）的潜在扩散框架之上，将其作为局部动作采样的基础模型和全局运动生成的基线。与 MLD 仅使用全局文本描述作为条件信号不同，GuidedMotion 引入了**多个参考局部动作作为附加条件信号**，将扩散过程的引导机制从无显式局部引导升级为**基于能量函数的局部动作梯度引导**。这一改变使得条件信号从单一全局文本扩展为“全局文本 + 局部动作参考”的组合，从而实现了对生成过程的细粒度控制。

与其他主流方法的差异更为显著。**MDM**（Tevet et al., ICLR 2023）和 **MotionDiffuse**（Zhang et al., TPAMI 2024）均采用单层扩散架构，直接在原始运动空间或潜在空间中进行去噪，缺乏对运动语义层次的显式建模。**T2M-GPT**（Zhang et al., CVPR 2023）则采用自回归生成范式，同样未对局部动作进行单独的条件引导。**ReMoDiffuse**（Zhang et al., ICCV 2023）虽然引入了检索增强机制，但其检索对象是全局运动片段，而非语义解构后的局部动作。GuidedMotion 的独特之处在于：通过语义图解析将全局描述解构为多个局部动作，并在扩散过程中以动作级别施加条件引导，从而降低了复杂运动的生成难度。

### 核心因果机制

GuidedMotion 的性能提升可归因于三个相互耦合的机制：

1. **局部动作先验采样**：语义图解析器（Semantic Graph Parser）将运动描述解析为运动、动作、细节三层节点及关系边，随后局部动作采样器利用 MLD 根据各局部动作描述生成参考动作。这为扩散过程提供了结构化的先验信息，将“从零生成复杂运动”转化为“在局部动作参考下协调全局运动”。

2. **层次化条件扩散**：运动 VAE 将运动序列编码到三个语义层次（运动级、动作级、细节级），对应不同粒度的运动表示。三个 Transformer 去噪网络分别在各层次进行去噪预测，其中动作级模型以运动级输出为条件（Eq. 11），细节级模型以动作级输出为条件（Eq. 12）。消融实验（Table 4）证实，从运动级到细节级，生成性能逐步提升，细节级别的 FID 和 R-Precision 均达到最优。

3. **可调节的局部动作引导权重**：图注意力网络（GAT）通过学习节点间的关系嵌入，自动估计每个局部动作的引导权重 $\lambda_t^k$（Eq. 8）。该权重可在推理时手动调整，实现对不同局部动作影响程度的连续控制（Fig. 7）。这是该方法的核心因果旋钮——改变 $\lambda$ 值即可调节局部动作对全局运动的约束强度。

### 适用边界与局限

**适用场景**：该方法特别适合需要生成包含多个局部动作的复杂运动序列（如“先走向椅子，然后坐下，最后挥手”），且用户希望对各局部动作进行独立控制的场景。在 HumanML3D 的复杂动作子集（至少 3 个局部动作、150 帧以上）上，GuidedMotion 的 FID 为 0.144，显著优于其他方法（Table 3），验证了其在复杂运动生成中的优势。

**已知局限**（需手动验证具体边界值）：
- **序列长度受限**：生成运动受限于数据集中运动片段的最大长度，无法建模超出该长度的连续动作序列。
- **低级编辑能力不足**：方法在潜在空间中进行扩散，适合高级运动编辑（如调整动作风格、替换局部动作），但难以进行低级编辑（如修改单个关节位置）。
- **VAE 瓶颈**：运动合成能力受限于预训练运动 VAE 的重建质量。当 VAE 对某些运动类型的重建能力不足时，会直接影响生成质量（Table C 显示细节级 VAE 在 HumanML3D 上的 FID 为 0.019，但该性能可能因运动类型而异）。
- **扩散随机性**：扩散模型的固有随机性可能导致偶尔的不良生成结果，目前缺乏有效的缓解机制。
- **推理速度**：尽管局部动作可预生成（不计入推理时间），但扩散去噪过程本身仍受现有扩散模型推理速度的限制（Table B 报告了不同扩散步数下的时间成本）。

### 开放问题

1. **时间一致性连续运动建模**：如何突破数据集片段长度限制，生成时间上一致的长序列连续运动？
2. **潜在空间低级编辑**：如何在保持潜在空间扩散优势的同时，实现对单个关节位置等低级属性的精确编辑？
3. **生成稳定性提升**：如何缓解扩散模型随机性带来的不良结果，例如通过后处理筛选或改进采样策略？
4. **更高效的运动潜在空间**：如何设计更紧凑且重建质量更高的运动潜在表示，以减轻 VAE 瓶颈对生成质量的影响？

## 原文 PDF

![[paperPDFs/ECCV_2024/Local_Action_Guided_Motion_Diffusion_Model_for_Text_to_Motion_Generation.pdf]]