---
title: Motion In Betweening for Densely Interacting Characters
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/Motion_In_Betweening_for_Densely_Interacting_Characters.pdf
project_link: null
code_link: null
aliases:
- CSB
- MBDIC
tags:
- SIGGRAPH_ASIA_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过跨空间表示显式解耦个体运动与交互条件，并利用周期性对抗学习与运动细化器维护长期交互一致性与运动质量。
primary_logic: 将交互生成分解为个体相对关键姿势的插值和基于对方根空间的交互调制；用成对关节距离动态的周期性编码驱动对抗训练，迫使生成器保持长期交互模式；在推理时用简单的自编码器细化潜分布，阻止误差漂移。
claims:
- 跨空间中间插值将问题分解为个体中间插值和交互建模两个阶段。
- 使用成对关节距离（PJD）的周期性自编码器捕获交互周期性，并通过对抗训练维持长期交互质量。
- 运动细化器校正自回归生成的分布漂移，防止姿势误差累积，使FID从0.696降至0.282。
- 用户研究中，本方法得分与真实运动相近，显著超越所有基线。
---

# Motion In Betweening for Densely Interacting Characters

> [!tip] 核心洞察
> 将交互生成分解为个体相对关键姿势的插值和基于对方根空间的交互调制；用成对关节距离动态的周期性编码驱动对抗训练，迫使生成器保持长期交互模式；在推理时用简单的自编码器细化潜分布，阻止误差漂移。

| 字段 | 内容 |
|------|------|
| 中文题名 | 密集交互角色的运动中间插值 |
| 英文题名 | Motion In Betweening for Densely Interacting Characters |
| 会议/期刊 | SIGGRAPH ASIA 2025 |
| Links |  [paper](https://dl.acm.org/doi/10.1145/3757377.3763950)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Cross-Space In-Betweening |
| Dataset | Boxing |

> [!tip] 效果简介
> - Boxing 上，FID (100 frames) 0.282 vs 0.696 (w/o Motion Refiner) (-0.414)；Interaction quality (discriminator accuracy at 40 frames) 0.914 vs 优于所有基线（具体数值未提供） (N/A)；L2P (30 frames) 0.192 vs N/A（与Phase Betweener等比较，数值未提供） (N/A)。

## 概要

密集交互双角色的运动中间插值面临一个核心瓶颈：系统必须同时满足空间‑时间对齐、关键姿势到达和泛化性三重严格约束，导致解空间严重受限。当自回归生成长序列时，姿势误差会快速累积，严重破坏交互质量。本文提出 **Cross‑Space In‑Betweening**，将交互生成分解为两个阶段——个体相对关键姿势的插值与基于对方根空间的交互调制——从而显式解耦个体运动与交互条件。在此基础上，方法引入成对关节距离动态的周期性编码，驱动对抗训练以维持长期交互模式，并在推理时使用运动细化器校正潜分布，阻止误差漂移。

实验表明，在 Boxing 数据集上，运动细化器使 FID 从 0.696 降至 0.282；用户研究中，本方法得分与真实运动相当，显著超越所有基线方法。该方法为密集交互角色的长期运动合成提供了一条有效的解耦‑调制‑校正路径，但其周期性编码策略主要适用于拳击、舞蹈等具有明显重复模式的交互，如何扩展至非周期性或高度非对称交互仍是开放问题。

### 问题背景

在计算机动画和交互式角色控制中，**运动中间插值**（motion in-betweening）是一项核心任务：给定稀疏的关键姿势（keypose），自动生成连接这些关键姿势的平滑过渡运动。这一技术在游戏开发、电影制作和虚拟现实等领域具有广泛的应用价值，能够显著降低动画师逐帧制作的工作量。

然而，当场景中涉及**两个密集交互的角色**时——例如拳击、舞蹈或格斗——中间插值的难度急剧上升。与单角色场景不同，双角色交互运动需要同时满足三个严格约束：

1. **空间对齐**：两个角色的肢体位置必须在每一帧保持合理的相对关系，避免穿透或不自然的接触。
2. **时间对齐**：交互动作的节奏和相位必须协调，例如出拳与格挡的时机需精确匹配。
3. **关键姿势到达**：生成的运动必须在指定时间点准确到达预设的关键姿势。

这三个约束叠加在一起，导致解空间严重受限。在长序列生成过程中，微小的姿势误差会通过自回归预测逐步累积，最终破坏交互质量，表现为角色间穿透、动作失真或关键姿势偏离。

### 现有方法缺口

现有的运动中间插值方法主要针对**单角色**场景设计，难以直接迁移到密集交互场景。具体而言，存在以下几个关键缺口：

**缺口一：缺乏对不同坐标空间的显式建模。** 现有双角色生成方法通常将双方的运动数据简单拼接后送入网络，或使用交叉注意力机制混合特征。这种方式将两个角色的运动隐式地耦合在一起，忽略了它们各自处于不同的局部坐标空间这一事实。当一方角色的运动需要根据另一方的姿态进行调整时，网络不得不同时学习个体运动规律和交互条件，导致学习负担过重、泛化能力不足。

**缺口二：缺乏长期交互质量的保障机制。** 标准自回归训练仅优化短时预测误差，缺乏对长期生成行为的约束。在双角色场景中，这意味着即使单步预测准确，误差也会在数十帧后累积到足以破坏交互模式的程度。例如，**Cross-Interaction Attention** 基线方法就表现出严重的姿势误差累积问题，而 **CondMDI** 虽然基于扩散模型，但在关键姿势对齐方面仍有不足。

**缺口三：交互周期性未被有效利用。** 拳击、舞蹈等密集交互运动具有显著的周期性特征——成对关节之间的距离变化遵循可预测的节奏模式。现有方法未将这种周期性作为显式约束引入训练，导致生成的运动在长时间跨度上逐渐偏离真实的交互节奏，角色可能滑向关键姿势而缺乏实质性的交互动作。

### 本文动机

针对上述缺口，本文提出 **Cross-Space In-Betweening** 方法，核心动机如下：

**动机一：将交互生成分解为个体运动与交互条件两个子问题。** 与其让网络同时学习“如何运动”和“如何交互”，不如先为每个角色独立生成朝向关键姿势的过渡运动，再基于另一方的空间信息进行调制。这种分解使每个子任务更加聚焦，降低了学习难度。

**动机二：利用交互的周期性特征维持长期质量。** 密集交互中的成对关节距离动态具有内在的周期性模式。通过显式建模这种周期性并将其作为对抗训练的监督信号，可以迫使生成器在长时间跨度上保持一致的交互行为，从根本上抑制误差累积。

**动机三：在推理阶段引入轻量级校正机制。** 即使训练阶段引入了长期约束，自回归推理时的分布漂移仍然不可完全避免。通过在推理时使用一个简单的运动细化器对生成片段的潜分布进行校正，可以以极小的计算开销阻止误差漂移，使FID指标从0.696大幅改善至0.282。

## 核心方法与创新机理

本工作针对**密集交互双角色运动中间插值**这一高约束生成任务，提出了 **Cross-Space In-Betweening** 框架。其核心创新可归结为两个关键“changed slots”，分别解决了交互条件注入方式和长期生成质量维持机制的根本缺陷。

### 创新一：跨空间交互条件注入

**Baseline 缺陷**：现有双角色生成方法通常将双方运动直接拼接（如 **Phase Betweener** 的扩展）或使用交叉注意力混合特征（如 **Cross-Interaction Attention**）。这类策略忽视了不同角色坐标空间分布的差异，导致交互条件与个体运动特征在几何上未对齐，难以精确建模角色间的空间关系。

**Proposed 方案**：本方法将双角色中间插值显式分解为“个体相对关键姿势的插值”和“基于对方根空间的交互调制”两个阶段。
- **第一阶段**（个体中间插值）：将输入运动通过离散余弦变换（DCT）映射到频域，利用1D卷积和图卷积网络（GCN）构成的编码器 $Enc$，预测单个角色相对关键姿势的空间偏移 $\hat{M}^{t+l} = Enc(DCT(M^{t}))$。这一步仅关注个体运动学约束，不涉及交互。
- **第二阶段**（交互建模）：将第一阶段预测结果通过空间变换 $\mathcal{T}$ 映射到**另一角色的根空间**，获得角色间相对姿态表示 $\hat{M}_{\mathrm{rel}}^{t+l} = \mathcal{T}(\hat{M}^{t+l})$。随后，从该相对表示中通过变分采样得到潜变量 $z$，由 FiLM 层产生仿射参数 $(\gamma, \beta)$，对关键姿势空间中的个体运动特征进行缩放和平移调制：$\hat{M}_{\mathrm{mod}}^{t+l} = \hat{M}^{t+l} \cdot \gamma + \beta$。最终通过解码器和逆DCT重建出考虑交互的完整运动。

这一设计的核心洞察在于：**交互条件不应在原始坐标空间中混合，而应通过显式的空间变换将一方运动“投影”到另一方的参考系中**，使FiLM调制能够感知角色间的相对位置、朝向和距离，从而在保持个体运动质量的同时精确注入交互约束。消融实验证实，去除跨空间和FiLM调制后，重建性能下降约20%，且出现严重的穿透和不真实交互（Fig. 9）。

### 创新二：双层次长期质量维持机制

**Baseline 缺陷**：标准自回归生成方法在长序列预测时，缺乏专门的长期校正机制。单步误差会在迭代中累积，导致姿势漂移、关节变形和交互模式崩溃。这在密集交互场景中尤为致命——两个角色的误差会相互放大。

**Proposed 方案**：引入两个互补模块，分别在交互层和单角色层稳定长期生成。

**1. 交互周期性判别器（交互层）**
密集交互（如拳击、舞蹈）具有显著的周期性模式。本方法提取角色间所有关节对的成对关节距离（Pairwise Joint Distance, PJD）逐帧变化量：
$$d^{t} = \{ \| x_{i}^{t} - y_{j}^{t} \|_{2}^{2} - \| x_{i}^{t-1} - y_{j}^{t-1} \|_{2}^{2} \mid i, j \in J \}$$
将长度为 $N$ 的PJD动态序列 $\mathcal{D}^{t}$ 输入周期性自编码器（PAE），编码为正弦参数化的相位/频率/振幅/偏置表示 $\boldsymbol{h}^{t} = PAE(\mathcal{D}^{t})$。在此基础上，引入对抗判别器对长预测片段（$N=30$帧）进行真伪分类，迫使生成器维持周期一致的交互模式。消融实验表明，去除该模块后角色会滑向关键姿势而缺乏真实交互运动（Fig. 14）。

**2. 运动细化器（单角色层）**
为解决自回归生成中的分布漂移问题，在推理阶段引入一个轻量级的自编码器+GCN结构作为运动细化器。其训练目标为最小化细化输出与真值的均方误差：
$$\mathcal{L}_{\mathrm{refine}} = \frac{1}{P} \sum^{P} (M_{\mathrm{refine}}^{t+l} - M_{\mathrm{gt}}^{t+l})^{2}$$
在推理时，细化器对生成的运动片段进行潜分布校正，阻止误差在自回归循环中累积。定量消融显示，去除运动细化器导致长序列FID从 **0.282 恶化至 0.696**（Table 1），并出现手部关节变形（Fig. 13）。

### 创新总结

| 创新维度 | Baseline 做法 | 本方法 | 效果 |
|---------|-------------|--------|------|
| 交互条件注入 | 特征拼接/交叉注意力混合 | 跨空间变换 + FiLM调制 | 重建性能提升约20%，消除穿透 |
| 长期质量维持 | 无专门校正 | 周期性对抗判别器 + 运动细化器 | FID降低0.414，交互判别器准确率达0.914 |

这两个创新协同运作：跨空间表示解耦了个体运动与交互条件，使生成器能专注于各自子问题；双层次长期维持机制则分别在交互模式一致性和个体运动质量两个层面阻止误差累积，共同支撑了用户研究中与真实运动得分相当的生成质量（Fig. 8）。

本文提出 **Cross-Space In-Betweening**，一种面向密集交互双角色的运动中间插值框架。其核心设计理念是将复杂的双角色交互生成问题**分解为两个阶段**：个体中间插值（Individual In-Betweening）与交互建模（Interaction Modeling），并通过跨空间表示实现二者的有效耦合。

### 问题定义

系统以自回归方式运行：给定长度为 $T=20$ 帧的双角色观测序列 $M^{t:t+T}$，预测未来 $l=10$ 帧的运动 $M^{t+l} = f(M^t)$。每个角色运动帧 $m$ 包含根位移、根旋转及关节旋转。关键挑战在于，生成的运动必须同时满足三个严格约束——到达指定的关键姿势、维持角色间的空间交互关系、以及保证长期运动质量。

### Pipeline 总览

框架整体结构如 **Fig. 2** 所示，由以下模块串联构成：

![[assets/figures/papers/paper_list_l1810_Motion_In_Betweening_for_Densely_Interacting_Characters/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our framework. The system first generates an initial prediction for individual character which minimizes the distance to keypose. Then, it extracts relative pose representations as conditions to refine the initial prediction and generates interactive motions. Pairwise joint distances and the outcomes of main network are fed into an interaction discriminator and a motion refiner to model interaction periodicity and to reduce pose error, respectively*

**1. 个体中间插值（Individual In-Betweening）**
首先将输入运动序列 $M^t$ 经离散余弦变换（DCT）映射到频域，再通过 1D 卷积与图卷积网络（GCN）组成的编码器 $Enc$，预测单个角色相对于关键姿势的空间偏移：
$$\hat{M}^{t+l} = Enc(DCT(M^{t}))$$
此阶段仅关注个体运动学，不考虑交互约束。

**2. 相对空间变换与交互调制**
将初步预测 $\hat{M}^{t+l}$ 通过空间变换 $\mathcal{T}$ 映射到另一角色的根空间，获得相对姿态表示 $\hat{M}_{\mathrm{rel}}^{t+l}$。随后，从该相对特征中通过变分采样提取潜变量 $z$，利用 FiLM（Feature-wise Linear Modulation）产生缩放参数 $\gamma$ 和偏移参数 $\beta$，对个体运动特征进行调制：
$$\hat{M}_{\mathrm{mod}}^{t+l} = \hat{M}^{t+l} \cdot \gamma + \beta$$
调制后的特征经解码器 $Dec$ 和逆 DCT（IDCT）重建为最终交互运动帧 $M^{t+l}$。这一跨空间设计显式解耦了个体运动与交互条件，使模型能在关键姿势空间中建模个体运动，同时在根空间中注入交互信息。

**3. 长期质量维持机制**
自回归生成中误差会快速累积，因此框架引入两个专门模块来稳定长期输出：

- **交互周期性建模（Interaction Periodicity Model）**：从生成运动中提取成对关节距离（Pairwise Joint Distance, PJD）的动态序列 $\mathcal{D}^t$，通过周期性自编码器（PAE）编码为正弦参数化的相位特征 $\boldsymbol{h}^t$。一个独立的判别器以 $N=30$ 帧的长片段为输入进行对抗训练，迫使生成器维持周期一致的交互模式（**Fig. 3**）。

- **运动细化器（Motion Refiner）**：由自编码器与 GCN 构成，在推理时对 Cross-Space In-betweening 输出的运动片段进行分布校正 $M_{\mathrm{refine}}^{t+l} = Refiner(M^{t+l})$，防止生成分布漂移导致的姿势误差累积。

### 训练与推理流程

训练时，主网络以 3 步自回归预测的 MSE 损失与 KL 正则化联合优化：
$$\mathcal{L}_{\mathrm{inbetween}} = \lambda_{\mathrm{mse}} \mathcal{L}_{\mathrm{mse}} + \lambda_{\mathrm{kl}} \mathcal{L}_{\mathrm{kl}}$$
同时，交互周期性判别器以对抗损失 $\mathcal{L}_{\mathrm{adv}}$ 独立训练，运动细化器以 $\mathcal{L}_{\mathrm{refine}}$ 单独训练。推理时，主网络自回归生成运动片段，运动细化器实时校正输出分布，单步推理耗时约 125 ms / 10 帧。

这一模块化设计使得框架能够在不显著增加复杂度的前提下，同时满足关键姿势到达、交互空间一致性和长期运动质量三大约束。

### 4.1 跨空间中间插值（Cross-Space In-betweening）

本方法将双角色中间插值问题分解为两个阶段：**个体中间插值**和**交互建模**。这种分解策略的核心动机在于，密集交互场景下的解空间受到空间-时间对齐、关键姿势到达和泛化能力三重严格约束，直接对双方运动联合建模极易导致姿势误差快速累积。

#### 4.1.1 个体中间插值

首先对每个角色独立预测其中间运动。给定输入运动序列 $M^t$，将其变换到频域后通过编码器预测未来 $l=10$ 帧的运动偏移：

$$\hat{M}^{t+l} = \text{Enc}(\text{DCT}(M^t))$$

其中 DCT 为离散余弦变换，编码器由 1D 卷积层和图卷积网络（GCN）级联组成。该阶段输出的是角色在关键姿势空间中的相对偏移表示，尚未考虑对手角色的影响。

#### 4.1.2 交互建模

交互建模的关键创新在于**跨空间条件注入**：将一方角色的初步预测变换到另一方的根空间，获得角色间的相对姿态信息，再通过特征线性调制（FiLM）将交互条件注入个体运动特征。

首先通过空间变换 $\mathcal{T}$ 将初步预测转换到对方根空间：

$$\hat{M}_{\text{rel}}^{t+l} = \mathcal{T}(\hat{M}^{t+l})$$

随后从相对表示中通过变分采样提取潜变量 $z$，并由 FiLM 层产生缩放参数 $\gamma$ 和偏移参数 $\beta$：

$$z = \mu(\hat{M}_{\text{rel}}^{t+l}) + \epsilon \cdot \sigma(\hat{M}_{\text{rel}}^{t+l}), \quad \gamma, \beta = \text{FiLM}(z)$$

最后对个体运动特征进行调制并重建为最终交互运动帧：

$$\hat{M}_{\text{mod}}^{t+l} = \hat{M}^{t+l} \cdot \gamma + \beta$$

$$M^{t+l} = \text{IDCT}(\text{Dec}(\hat{M}_{\text{mod}}^{t+l}))$$

这种设计的优势在于：个体运动在关键姿势空间中保持稳定表示，而交互条件通过对方根空间的相对几何关系显式编码，避免了两者特征的直接拼接或交叉注意力带来的分布失配问题。

#### 4.1.3 中间插值损失函数

训练时采用 $P=3$ 步自回归预测的均方误差：

$$\mathcal{L}_{\text{mse}} = \frac{1}{P} \sum^{P} (M^{t+l} - M_{\text{gt}}^{t+l})^{2}$$

配合变分自编码器的 KL 正则化项：

$$\mathcal{L}_{\text{kl}} = -0.5 \cdot \left(1 + \sigma - \mu^{2} - e^{\sigma}\right)$$

整体中间插值损失为两者的加权组合：

$$\mathcal{L}_{\text{inbetween}} = \lambda_{\text{mse}} \mathcal{L}_{\text{mse}} + \lambda_{\text{kl}} \mathcal{L}_{\text{kl}}$$

---

### 4.2 长期质量维持机制

标准自回归训练在长序列生成时面临严重的分布漂移问题。本方法引入两个互补模块分别在交互层和单角色层稳定长期生成质量。

#### 4.2.1 交互周期性建模

针对拳击、舞蹈等具有明显重复模式的交互，从生成运动中提取**成对关节距离（Pairwise Joint Distance, PJD）** 的动态变化：

$$d^{t} = \{ \| x_{i}^{t} - y_{j}^{t} \|_{2}^{2} - \| x_{i}^{t-1} - y_{j}^{t-1} \|_{2}^{2} \mid i, j \in J \}$$

其中 $x_i^t$ 和 $y_j^t$ 分别为两个角色在时刻 $t$ 的第 $i$ 和第 $j$ 个关节位置，$J$ 为关节集合。将长度为 $N$ 的 PJD 序列记为 $\mathcal{D}^{t} \in \mathbb{R}^{J \times N}$。

周期性自编码器（Periodic Autoencoder, PAE）将 PJD 动态编码为参数化的正弦表示：

$$\boldsymbol{h}^{t} = \text{PAE}(\mathcal{D}^{t}) = \boldsymbol{a}^{t} \sin(2\pi (\boldsymbol{f}^{t} + \boldsymbol{\phi}^{t})) + \boldsymbol{b}^{t}$$

其中 $\boldsymbol{a}^{t}$、$\boldsymbol{f}^{t}$、$\boldsymbol{\phi}^{t}$、$\boldsymbol{b}^{t}$ 分别为振幅、频率、相位和偏置参数。通过对抗训练，判别器学习区分真实交互的周期性模式与生成运动中的伪周期模式，迫使生成器维持长期交互一致性：

$$\mathcal{L}_{\text{adv}} = \mathbb{E}_{M_{\text{gt}}^{t+l:t+l+N} \sim \mathcal{M}} [\log D(M_{\text{gt}}^{t+l:t+l+N})] + \mathbb{E}_{M^{t:t+N} \sim \rho_{G}} [\log (1 - D(G(M^{t:t+N})))]$$

#### 4.2.2 运动细化器

运动细化器在推理时对 Cross-Space In-betweening 生成的漂移分布进行校正。该模块由自编码器和 GCN 组成，对生成的运动片段进行空间-时间特征提取与重建：

$$M_{\text{refine}}^{t+l} = \text{Refiner}(M^{t+l})$$

训练损失为细化输出与真值的均方误差：

$$\mathcal{L}_{\text{refine}} = \frac{1}{P} \sum^{P} (M_{\text{refine}}^{t+l} - M_{\text{gt}}^{t+l})^{2}$$

消融实验表明，去除运动细化器后长序列 FID 从 0.282 恶化至 0.696，并出现手部关节变形（Fig. 13），验证了该模块对阻止误差累积的关键作用。

## 实验与关键发现

### 主结果

我们首先在Boxing数据集上评估重建质量与交互质量。如表1所示，完整方法在30帧重建指标L2P上达到**0.192**，在40帧交互判别器准确率上达到**0.914**。相比之下，去除运动细化器的版本FID从0.282恶化至0.696，表明长期误差累积是密集交互生成的核心瓶颈。

在用户研究中（Fig. 8），本方法的评分分布与真实运动（Ground Truth）高度接近，且显著超越所有基线方法。与**CondMDI**的定性对比（Fig. 6）显示，本方法在关键姿势对齐方面表现更优；与引入交叉注意力的双角色生成基线**Cross-Interaction Attention**相比（Fig. 5），后者出现严重的姿势误差累积，而本方法保持了长期运动一致性。

![[assets/figures/papers/paper_list_l1810_Motion_In_Betweening_for_Densely_Interacting_Characters/figures/009_Figure_8.jpg]]
*Figure 8: User study results presented as a box plot of ratings across different methods. Our method achieves scores comparable to the ground truth and surpasses all baseline approaches*

![[assets/figures/papers/paper_list_l1810_Motion_In_Betweening_for_Densely_Interacting_Characters/figures/005_Figure_5.jpg]]
*Figure 5: alitative results compared with baseline methods. Cross-Interaction A ention exhibits severe pose error accumulation issue*

![[assets/figures/papers/paper_list_l1810_Motion_In_Betweening_for_Densely_Interacting_Characters/figures/006_Figure_6.jpg]]
*Figure 6: Keypose alignment performance compared with CondMDI*

跨数据集泛化方面，在ReMoCap和InterHuman数据集上的定性结果（Fig. 4, Fig. 11, Fig. 12）展示了平滑、无缝的转折运动，验证了方法的泛化能力。推理效率上，每10帧预测耗时约**125 ms**，具备实时交互的潜力。

![[assets/figures/papers/paper_list_l1810_Motion_In_Betweening_for_Densely_Interacting_Characters/figures/004_Figure_4.jpg]]
*Figure 4: alitative results on ReMoCap and InterHuman dataset. Our method produces smooth and seamless turning motions (light blue and pink) in between keyposes (blue and red)*

### 消融实验

消融实验围绕三个核心模块展开：

1. **运动细化器（Motion Refiner）**：去除该模块后，长序列FID从0.282急剧恶化至0.696（Table 1消融行），且定性结果（Fig. 13）显示若干秒后角色手部关节出现明显变形。这证实了自回归生成中分布漂移是导致姿势误差累积的直接原因，而运动细化器通过潜变量校正有效阻止了这一漂移。

![[assets/figures/papers/paper_list_l1810_Motion_In_Betweening_for_Densely_Interacting_Characters/figures/014_Figure_13.jpg]]
*Figure 13: alitative results without the Motion Refiner. The blue character exhibits hand joint deformation a er a few seconds of prediction*

2. **交互建模（跨空间变换 + FiLM调制）**：去除交互建模后，重建性能下降约**20%**（Section 5.5）。定性结果（Fig. 9）显示角色之间出现严重穿透和不真实交互，说明跨空间相对表示和FiLM条件调制是产生物理合理交互的关键。

![[assets/figures/papers/paper_list_l1810_Motion_In_Betweening_for_Densely_Interacting_Characters/figures/010_Figure_9.jpg]]
*Figure 9: alitative comparison on interaction modeling. On the right, both characters exhibit significant penetration and unrealistic interactions*

3. **交互周期性建模（周期性自编码器 + 对抗判别器）**：去除对抗判别器后，角色运动滑向关键姿势而缺乏真实交互行为（Fig. 14），表明成对关节距离动态的周期性编码和对抗训练对于维持长期交互模式至关重要。

![[assets/figures/papers/paper_list_l1810_Motion_In_Betweening_for_Densely_Interacting_Characters/figures/015_Figure_14.jpg]]
*Figure 14: alitative results without modeling interaction periodicity. The blue character is sliding to its keypose without interactive movement*

### 失败模式与局限性

尽管方法在Boxing等周期性交互任务上表现优异，仍存在以下失败模式与局限：

- **长期误差累积**：在极端长序列生成中，即使有运动细化器，仍可能出现骨骼变形（Fig. 15），说明当前校正机制无法完全消除误差漂移。
- **非周期性交互**：周期性编码策略主要适用于拳击、舞蹈等具有明显重复模式的交互，不易扩展到杂技、随机打斗等非周期性场景。
- **离线优化缺失**：系统不支持对已生成序列进行离线精细调整以实现更好的关键姿势对齐。
- **时间控制缺失**：当前框架不支持中间插值的时间调节（如过渡快慢），因为这会显著增加建模复杂度。

![[assets/figures/papers/paper_list_l1810_Motion_In_Betweening_for_Densely_Interacting_Characters/figures/016_Figure_15.jpg]]
*Figure 15: Examples of deformed bones caused by long-term error accumulation*

### 重要图表结论

- **Table 1**：完整方法在重建质量（L2P=0.192）、交互质量（判别器准确率=0.914）和FID（0.282）上全面领先，消融实验验证了运动细化器和交互建模的必要性。
- **Fig. 8**：用户研究箱线图显示本方法评分与真实值相当，统计上显著优于所有基线，提供了最强的主观质量证据。
- **Fig. 13/14**：消融可视化分别揭示了去除运动细化器导致的手部变形和去除交互周期性导致的滑移现象，为因果机制提供了直观证据。
- **Fig. 5**：与Cross-Interaction Attention的对比直接暴露了简单注意力机制在长序列生成中的严重误差累积问题，反衬出跨空间解耦设计的优势。

![[assets/figures/papers/paper_list_l1810_Motion_In_Betweening_for_Densely_Interacting_Characters/figures/007_Table_1.jpg]]
*Table 1: antitative results compared with previous methods and ablated versions. All comparison methods and ablated networks are trained on Boxing dataset only*

## 定位与知识库关联

### 问题定位：密集交互中间插值的核心瓶颈

双角色密集交互（如拳击、舞蹈、摔跤）的中间插值任务面临一个三维约束困境：生成的运动必须同时满足（1）精确的关键姿势到达（空间约束），（2）角色间持续、真实的交互关系（交互约束），以及（3）长序列自回归生成中的误差不累积（时间约束）。这三个约束的联合作用使解空间严重受限——传统单角色中间插值方法（如相位驱动的运动匹配）直接扩展到双角色时，缺乏对交互空间的显式建模，导致角色间出现穿透、滑步或交互模式崩溃；而简单的双角色拼接或交叉注意力方案（如 **Cross-Interaction Attention** 基线）则因特征空间未对齐，在长序列生成中姿势误差快速累积，最终产生骨骼变形和不真实交互。

### 核心因果机制：跨空间解耦与周期性对抗维持

本方法 **Cross-Space In-Betweening** 的核心创新在于将上述三维约束分解为两个可控阶段，并引入两个专门的长期质量维持机制：

**1. 个体-交互解耦（跨空间中间插值）**

第一阶段，系统将每个角色的运动表示为相对于其关键姿势的空间偏移量，通过 DCT 频域编码和 GCN 编码器独立预测个体中间插值 $\hat{M}^{t+l} = Enc(DCT(M^{t}))$。这解决了“关键姿势到达”约束。

第二阶段，将初步预测变换到另一角色的根空间，获得相对姿态表示 $\hat{M}_{\mathrm{rel}}^{t+l} = \mathcal{T}(\hat{M}^{t+l})$，然后通过 FiLM（Feature-wise Linear Modulation）从该相对表示中变分采样潜变量 $z$，产生缩放和偏移参数 $(\gamma, \beta)$ 调制个体运动特征。这一设计的关键在于：**交互条件不是在原始运动空间直接混合，而是在关键姿势偏移空间中注入**，使角色既能保持自身运动结构，又能响应对方的相对位置和姿态。

**2. 长期交互质量的双重保障**

自回归生成的核心风险是分布漂移——每步预测的微小误差在迭代中放大，最终使生成的运动偏离真实交互分布。本方法从两个层面进行对抗：

- **交互周期性判别器**：提取成对关节距离（PJD）的动态序列 $\mathcal{D}^{t} = (d^{t}, d^{t+1}, \ldots, d^{t+N})$，用周期性自编码器（PAE）将其编码为正弦参数化的相位/频率表示 $\boldsymbol{h}^{t} = \boldsymbol{a}^{t} \sin(2\pi (\boldsymbol{f}^{t} + \boldsymbol{\phi}^{t})) + \boldsymbol{b}^{t}$，然后通过对抗训练迫使生成器在长片段（N=30帧）上维持周期一致的交互模式。这直接针对拳击、舞蹈等具有重复节奏的密集交互场景。
  
- **运动细化器（Motion Refiner）**：一个轻量自编码器+GCN结构，在推理时对生成的运动片段进行分布校正 $M_{\mathrm{refine}}^{t+l} = Refiner(M^{t+l})$，阻止误差漂移。消融实验显示，去除该模块导致 FID 从 0.282 恶化至 0.696（Table 1），并在数秒内出现手部关节变形（Fig. 13）。

### 与现有方法的差异定位

| 方法 | 交互建模策略 | 长期质量维持 | 关键局限 |
|------|-------------|-------------|---------|
| **Phase Betweener (combined)** | 单角色相位方法直接扩展，无显式交互建模 | 标准自回归训练，无专门校正 | 无法处理角色间空间关系，交互质量差 |
| **Cross-Interaction Attention** | 交叉注意力混合双角色特征 | 无长期校正机制 | 特征空间未对齐，误差严重累积（Fig. 5） |
| **CondMDI** | 条件运动扩散模型 | 扩散模型本身具有长期稳定性 | 关键姿势对齐能力弱于本方法（Fig. 6） |
| **Cross-Space In-Betweening (Ours)** | 跨空间解耦：个体偏移预测 + 根空间 FiLM 调制 | 周期性对抗判别器 + 运动细化器双重保障 | 依赖交互周期性假设，非周期性场景受限 |

### 适用边界与局限性

**已验证的适用场景：**
- 拳击（Boxing 数据集）：FID=0.282，交互判别器准确率 0.914，用户研究得分与真实运动相当（Fig. 8）
- 舞蹈类密集交互（ReMoCap、InterHuman 数据集）：产生平滑的转身过渡运动（Fig. 4, 11, 12）

**明确局限性：**
1. **周期性依赖**：PJD 周期性编码策略主要适用于拳击、舞蹈等具有明显重复模式的交互。论文明确指出该方法不易扩展到非周期性交互（如杂技、随机打斗）。
2. **无时间控制**：当前系统不支持中间插值的时间调节（in-between timing condition），用户无法指定过渡的快慢节奏。
3. **离线精调缺失**：不支持对已生成序列进行离线精细调整以实现更好的关键姿势对齐。
4. **双角色限制**：框架设计针对两个角色的密集交互，未扩展到多角色（≥3）场景。

### 开放问题与后续方向

1. **非周期性交互扩展**：如何将方法推广到非周期性或高度非对称的交互（如杂技、随机打斗）？可能需要将 PJD 动态的周期性先验替换为更通用的交互模式编码器。

2. **时间控制融入**：是否能在不显著增加复杂度的前提下融入时间控制条件，让用户指定过渡的快慢？这涉及在 FiLM 调制或潜变量中引入时间维度的条件信号。

3. **多角色泛化**：如何将跨空间解耦框架推广到多于两个角色的密集交互场景？根空间变换的数量将随角色数平方增长，需要设计可扩展的相对表示方案。

4. **与扩散模型结合**：周期性判别器能否与扩散模型等更灵活的生成框架结合？扩散模型本身具有较好的长期稳定性，但推理速度较慢（本方法推理仅需 125ms/10帧），结合两者的优势可能进一步提升长时间稳定性和多样性。

5. **评估体系的独立性**：论文使用独立训练的判别器评估交互质量（Section 5.4），这一做法避免了评估偏差，但判别器本身的能力上限会影响评估的可靠性。如何建立更客观的密集交互质量评估标准仍是一个开放问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/Motion_In_Betweening_for_Densely_Interacting_Characters.pdf]]
