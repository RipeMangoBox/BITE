---
title: "SyncDiff: Synchronized Motion Diffusion for Multi-Body Human-Object Interaction Synthesis"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Interaction_Synthesis.pdf
aliases:
- SyncDiff
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在对齐分数的引导下，将多体运动建模为动态图模型，并在训练中增加对齐损失，在推理中实施显式同步步骤以融合样本分数与对齐分数，直接约束个体运动与相对运动的一致性。
primary_logic: 通过频率分解明确建模高频语义成分，并将多体同步形式化为图模型上的最大似然采样问题，联合优化数据样本分数与对齐分数，可在统一的扩散框架下显著提升任意数量身体的交互质量。
claims:
- 同步机制（对齐分数+显式同步）大幅改善接触一致性，消除异步与穿透。
- 频率分解确保高频语义不被低频运动淹没，提升动作识别准确率。
- 在五个多体交互数据集上全面超越现有最先进方法，动作识别准确率平均提升超过15%。
- TACO 上 CSIoU (%, ↑) = 73.00
---

# SyncDiff: Synchronized Motion Diffusion for Multi-Body Human-Object Interaction Synthesis

> [!tip] 核心洞察
> 通过频率分解明确建模高频语义成分，并将多体同步形式化为图模型上的最大似然采样问题，联合优化数据样本分数与对齐分数，可在统一的扩散框架下显著提升任意数量身体的交互质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | SyncDiff：面向多体人-物交互的同步运动扩散模型 |
| 英文题名 | SyncDiff: Synchronized Motion Diffusion for Multi-Body Human-Object Interaction Synthesis |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://syncdiff.github.io/) · [paper](https://arxiv.org/abs/2412.20104) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SyncDiff |
| Dataset | TACO, CORE4D, BEHAVE, OAKINK2 |

> [!tip] 效果简介
> - TACO 上，CSIoU (%, ↑) 73.00 vs DiffH2O: 62.29 (+10.71)；RA (%, ↑) 73.28 vs DiffH2O: 61.40 (+11.88)。
> - CORE4D 上，CRR (%, ↑) 6.15 vs CG-HOI: 3.67 (+2.48)。
> - BEHAVE 上，CRR (%, ↑) 10.29 vs OMOMO: 7.88 (+2.41)。

## 概述

多体人‑物交互（HOI）合成——同时生成任意数量的人体、手部与刚性物体的运动——是具身智能与数字人领域的基础难题。现有方法大多面向特定身体数量（如单手‑单物体或单人‑单物体），难以在高频微小运动与复杂高阶关系上保持精确同步，普遍存在穿透、接触丢失或语义缺失等问题。

SyncDiff 的核心思路是：**将对齐分数与显式同步步骤引入统一的扩散框架，将多体同步形式化为动态图模型上的最大似然采样问题**。具体而言，该方法将运动按频率分解为低频（dc）与高频（ac）分量，确保握手、拧盖等高频语义成分不被低频运动淹没；训练时引入对齐损失，约束个体运动与相对运动的一致性；推理时每隔若干步执行显式同步，融合样本分数与对齐分数以最大化总体似然。这一设计使得 SyncDiff 能够以单一模型适配从手‑物到多人‑多物的各类交互场景，而无需预定义物体轨迹或交互关键帧。

在五个多体交互数据集（TACO、GRAB、CORE4D、BEHAVE、OAKINK2）上，SyncDiff 全面超越现有最先进方法：**语义动作识别准确率平均提升超过 15%，接触质量指标（如 CSIoU）提升 10–21 个百分点**。消融实验进一步证实，频率分解、对齐损失与显式同步步骤三者缺一不可——移除任一组件均会导致接触一致性或语义准确率的显著退化。

SyncDiff 的方法定位可概括为：**以频率感知的运动表示和对齐驱动的同步机制为核心改造点，在扩散模型框架内实现可扩展的多体交互生成**。其局限性主要体现在对铰接物体的关节约束建模不足、显式同步的计算开销随身体数量二次增长，以及对纯多人交互场景的通用性受限。

## 背景与动机

多体交互运动合成是计算机视觉与图形学中的核心问题，其目标是为任意数量的手、人体和刚体物体生成自然且语义合理的协同运动序列。这类合成在具身智能、机器人操作、虚拟现实和动画制作等场景中具有广泛的应用前景。然而，现有方法在应对多体交互时暴露出一个根本性瓶颈：**难以为任意数量的身体合成精确同步的交互运动，尤其在高频微小运动和复杂高阶关系上，容易产生穿透、接触丢失或语义缺失**。

具体而言，当前多体运动生成方法主要存在以下结构性缺口：

1. **同步机制缺失**：以 **MACS**（手物交互，单物体多手）、**DiffH2O**（双手单物体）、**CG-HOI**（多人单物体）和 **OMOMO**（单人单物体）为代表的现有工作，或完全缺乏显式同步机制，或仅依赖隐式共现建模。这使得生成的个体运动之间缺乏一致性约束，导致物体间穿透、接触丢失或异步动作等典型失败模式（参见 Figure 4、Figure 8）。

2. **高频语义被淹没**：现有方法仅使用时域轨迹作为运动表示，未对不同频率成分进行差异化处理。这导致高频周期性微小运动（如搅拌时铲子的旋转、拧瓶盖时的螺旋趋势）容易被低频大范围运动所淹没，而这些高频成分恰恰是识别动作类型和判断交互质量的关键语义载体。

3. **多体建模缺乏统一框架**：不同任务（手物交互、人物交互、多物体操作）各自采用独立的模型架构和表示方式，缺乏一个能够统一处理任意数量身体交互的通用框架。这限制了方法的可扩展性和跨场景迁移能力。

针对上述缺口，**SyncDiff** 提出了一种统一的同步运动扩散框架。其核心动机在于：将多体同步形式化为动态图模型上的最大似然采样问题，通过在对齐分数的引导下联合优化数据样本分数与对齐分数，在统一的扩散框架内实现任意数量身体的精确同步交互。该方法从两个层面切入问题——在训练阶段引入对齐分数及对齐损失以显式约束个体运动与相对运动的一致性，在推理阶段实施图式显式同步步骤以融合样本分数与对齐分数。同时，通过频率分解将运动信号分离为低频（dc）和高频（ac）分量，确保高频语义成分不被低频运动所掩盖。

这一设计使得 SyncDiff 在五个多体交互数据集（TACO、GRAB、CORE4D、BEHAVE、OAKINK2）上全面超越现有最先进方法，动作识别准确率平均提升超过 15%，接触质量指标（CSIoU、CSR）亦有显著增益。

## 核心创新

SyncDiff 的核心创新在于将多体交互运动生成重新定义为**动态图模型上的同步采样问题**，并通过两个互补的机制——训练时的**对齐分数与对齐损失**、推理时的**显式同步步骤**——从根本上解决现有方法中个体运动与相对运动不一致导致的穿透、接触丢失和语义缺失。与依赖隐式共现或完全无同步机制的基线方法（如 DiffH2O、CG-HOI、MACS 等）相比，SyncDiff 的关键改进体现在以下三个维度。

### 1. 频域运动分解：保护高频语义不被淹没

现有方法仅在时域建模运动轨迹，导致细微的高频周期性运动（如拧瓶盖时的螺旋旋转、锅铲在锅底的往复刮擦）容易被大幅度的低频身体运动所掩盖。SyncDiff 引入**频率分解机制**（Section 3.3），利用快速傅里叶变换将每条运动序列显式拆分为低频（dc）和高频（ac）分量：

$$x_{\mathrm{dc}, u} = \sum_{l=-3}^{2} a_l \cos(u \phi_l) + b_l \sin(u \phi_l), \quad x_{\mathrm{ac}, u} = \sum_{l \in [-L, -4] \cup [3, L-1]} a_l \cos(u \phi_l) + b_l \sin(u \phi_l)$$

其中 L=16 为截止频率上界。这一设计使模型在扩散去噪过程中能够独立处理不同频率成分，确保高频语义分量不被低频运动“平均化”而丢失。消融实验证实，移除频率分解后，语义指标 FID 和动作识别准确率（RA）显著下降，且定性结果显示物体间的有效相对运动几乎消失（Figure 10）——锅铲仅在盘子表面小范围停滞，无法完成功能性操作。

### 2. 对齐分数与对齐损失：训练中显式约束同步关系

基线方法在训练时仅使用标准的扩散重建损失，缺乏对多体间相对运动一致性的直接监督。SyncDiff 在训练过程中**推导并引入对齐分数**，并通过对齐损失 $\mathcal{L}_{\mathrm{align}}$ 显式约束预测的相对运动与由个体运动计算出的相对运动之间的一致性：

$$\mathcal{L}_{\mathrm{align}} = \sum_{j_1, j_2 \in [1, m], j_1 \neq j_2} \| \hat{x}_{o_{j_2} \to o_{j_1}} - \mathrm{rel}(\hat{x}_{o_{j_1}}, \hat{x}_{o_{j_2}}) \|_2^2 + \sum_{i \in [1, n], j \in [1, m]} \| \hat{x}_{h_i \to o_j} - \mathrm{rel}(\hat{x}_{o_j}, \hat{x}_{h_i}) \|_2^2$$

该损失覆盖所有物体-物体对和人体/手-物体对，迫使模型在生成个体运动的同时保持相对运动在几何上自洽。最终的综合损失函数将 dc 损失、ac 损失、对齐损失与四元数归一化损失加权组合：

$$\mathcal{L} = \lambda_{\mathrm{dc}} \mathcal{L}_{\mathrm{dc}} + \lambda_{\mathrm{ac}} \mathcal{L}_{\mathrm{ac}} + \lambda_{\mathrm{align}} \mathcal{L}_{\mathrm{align}} + \lambda_{\mathrm{norm}} \mathcal{L}_{\mathrm{norm}}$$

消融实验表明，移除 $\mathcal{L}_{\mathrm{align}}$ 后接触指标 CSIoU 和 CSR 出现明显下降（Table 1, 3, 5），验证了对齐损失对维持接触一致性的关键作用。

### 3. 显式同步推理：图模型上的最大似然采样

这是 SyncDiff 最具区分度的创新。现有方法在推理过程中对多体运动独立去噪，缺乏跨身体的协调机制。SyncDiff 将多体系统建模为**动态图模型**，在推理时每隔 s 步（实践中 s=50, T=1000）执行一次**显式同步操作**，通过融合样本分数与对齐分数来最大化整体似然。以刚性物体为例，同步更新公式为：

$$\hat{x}_{o_j}' = \frac{\frac{2}{m-1} \sigma^2 \overline{\lambda}}{1+2\sigma^2 \overline{\lambda}} \sum_{j'\neq j} \mathrm{comb}(\hat{x}_{o_{j'}}, \hat{x}_{o_j o_{j'}}) + \frac{1}{1+2\sigma^2 \overline{\lambda}} \hat{\mu}_{o_j} + \sigma' \epsilon$$

该公式将每个物体的运动更新为其自身预测均值 $\hat{\mu}_{o_j}$ 与其他物体运动通过相对关系组合结果的加权融合，在数学上等价于图模型的最大似然推断。移除显式同步步骤后，接触指标和动作识别率均显著降低（Table 1, 3, 5），证明了这一机制对消除异步和穿透不可或缺。

### 方法谱系与知识库定位

SyncDiff 处于**多体人-物交互运动生成**与**扩散模型可控生成**的交叉点。与以下代表性基线相比，其差异化优势明确：

- **DiffH2O**（双手-单物体，无同步机制）：SyncDiff 在 TACO 数据集上 CSIoU 提升 +10.71%，RA 提升 +11.88%；在 GRAB 未见被试者划分上 CSIoU 提升 +16.32%（Table 1, 2）。
- **CG-HOI**（多人-单物体，依赖隐式共现）：SyncDiff 在 CORE4D 数据集上 CRR 从 3.67% 提升至 6.15%（Table 3）。
- **MACS**（单物体-多手，无同步）：SyncDiff 在 OAKINK2 数据集上 CSIoU 从 51.22% 提升至 72.14%，提升幅度达 +20.92%（Table 5）。
- **OMOMO**（单人-单物体）：SyncDiff 在 BEHAVE 数据集上 CRR 从 7.88% 提升至 10.29%（Table 4）。

SyncDiff 的同步机制使其能够统一处理**任意数量**的手、人体和刚体，而上述基线方法均针对固定的身体数量组合设计，泛化能力受限。这一统一性源于将同步问题形式化为图模型上的概率推断，而非针对特定交互模式的手工规则。

### 局限与待验证边界

尽管创新显著，以下局限需在解读时注意：
- 显式同步步骤的时间复杂度随身体数量**二次增长**，在大量交互场景下计算开销较高。
- 当前方法**不保证物理真实性**，微小误差可能在真实机器人任务中导致失败——这一边界尚未在物理仿真环境中验证。
- 相对运动表示**局限于刚体坐标系**，不适用于纯多人交互合成——论文明确承认了这一通用性限制。

## 整体框架

SyncDiff 构建了一个统一的单阶段扩散框架，用于合成任意数量手、人体与刚体之间的同步多体交互运动。其核心思想是将多体运动建模为**动态图模型上的最大似然采样问题**，并在训练与推理两个阶段分别引入同步机制，从而在保持生成多样性的同时，强制个体运动与相对运动的一致性。

### 输入与输出

**输入**由两部分组成：
- **动作与物体类别条件**：通过预训练的 CLIP 模型提取动作标签与物体类别标签的语义特征。
- **物体几何条件**：利用基点点集（Basis Point Set, BPS）编码器提取物体几何形状的结构特征。

**输出**为一段同步化的多体运动序列，包含：
- 每个刚体物体的 6-DoF 刚体变换轨迹（3-DoF 平移 + 6-DoF 旋转，以四元数表示）。
- 每个人体/手的 SMPL-X 或 MANO 关节旋转轨迹。
- 所有物体-物体间、人体-物体间的相对运动表示。

最终，通过网格重建模块从关节位置优化恢复 MANO/SMPL-X 网格，用于渲染与定量评估。

### 整体 Pipeline

SyncDiff 的完整流程由以下五个核心模块串联构成：

#### 1. 运动表示构建

对于包含 $m$ 个刚体物体和 $n$ 个人体/手的场景，首先计算所有个体运动（物体刚体变换 $\{x_{o_j}\}$、人体/手关节旋转 $\{x_{h_i}\}$）以及所有成对相对运动（物体-物体相对变换 $\{x_{o_{j_2} \to o_{j_1}}\}$、人体/手-物体相对变换 $\{x_{h_i \to o_j}\}$）。随后，将所有这些表示**拼接为一个高阶运动表征 $x$**，作为扩散模型的统一操作对象。

#### 2. 频率分解

对拼接后的运动表征 $x$ 执行快速傅里叶变换（FFT），将信号分解为频率分量：

$$x_{u \in [0, N-1]} = \sum_{l=0}^{N-1} a_l \cos(u \phi_l) + b_l \sin(u \phi_l)$$

随后按截止频率上界 $L=16$ 将信号切分为两部分：
- **低频（DC）分量** $x_{\mathrm{dc}}$：包含 $l \in [-3, 2]$ 的频率成分，捕捉运动的整体趋势与慢变模式。
- **高频（AC）分量** $x_{\mathrm{ac}}$：包含 $l \in [-L, -4] \cup [3, L-1]$ 的频率成分，显式表征周期性微小运动（如拧瓶盖的螺旋趋势、锅铲在锅面的往复滑动），这些高频语义成分对动作类型识别至关重要。

#### 3. Transformer 去噪骨干

采用**潜在扩散（Latent Diffusion）**范式，以 Transformer 作为去噪网络骨干。在每个去噪时间步，网络以带噪运动表征、扩散时间步 $t$、CLIP 语义特征和 BPS 几何特征为条件，预测噪声并逐步恢复干净的运动信号。该骨干同时对 DC 和 AC 分量进行去噪。

#### 4. 对齐损失模块

在训练阶段，SyncDiff 引入**对齐损失** $\mathcal{L}_{\mathrm{align}}$，显式约束预测的相对运动与由个体运动导出的相对运动之间的一致性：

$$\mathcal{L}_{\mathrm{align}} = \sum_{j_1, j_2} \| \hat{x}_{o_{j_2} \to o_{j_1}} - \mathrm{rel}(\hat{x}_{o_{j_1}}, \hat{x}_{o_{j_2}}) \|_2^2 + \sum_{i, j} \| \hat{x}_{h_i \to o_j} - \mathrm{rel}(\hat{x}_{o_j}, \hat{x}_{h_i}) \|_2^2$$

该损失与 DC 重建损失 $\mathcal{L}_{\mathrm{dc}}$、AC 重建损失 $\mathcal{L}_{\mathrm{ac}}$、四元数归一化损失 $\mathcal{L}_{\mathrm{norm}}$ 加权组合，形成总损失函数：

$$\mathcal{L} = \lambda_{\mathrm{dc}} \mathcal{L}_{\mathrm{dc}} + \lambda_{\mathrm{ac}} \mathcal{L}_{\mathrm{ac}} + \lambda_{\mathrm{align}} \mathcal{L}_{\mathrm{align}} + \lambda_{\mathrm{norm}} \mathcal{L}_{\mathrm{norm}}$$

#### 5. 显式同步推理

在推理阶段，SyncDiff 每隔 $s$ 步（实践中取 $s=50$，总去噪步数 $T=1000$）执行一次**显式同步操作**。该步骤将多体运动建模为图模型，同时利用扩散模型的**样本分数**（由去噪骨干预测的均值 $\hat{\mu}$）和**对齐分数**（由相对运动一致性导出），通过最大似然推断融合两者信息，更新所有个体的运动状态。对于刚体物体，同步更新公式为：

$$\hat{x}_{o_j}' = \frac{\frac{2}{m-1} \sigma^2 \overline{\lambda}}{1+2\sigma^2 \overline{\lambda}} \sum_{j'\neq j} \mathrm{comb}(\hat{x}_{o_{j'}}, \hat{x}_{o_j o_{j'}}) + \frac{1}{1+2\sigma^2 \overline{\lambda}} \hat{\mu}_{o_j} + \sigma' \epsilon$$

在两次同步步骤之间，仍使用标准扩散去噪步骤 $\hat{x}_{t-1} = \hat{\mu}(\hat{x}_t, t) + \sigma_t \epsilon$ 进行逐步去噪。同步化后的运动表征 $\hat{x}'$ 继续参与后续去噪迭代。

### 模块间关系

频率分解与对齐损失/显式同步构成了 SyncDiff 的两条互补线索：**频率分解**确保高频语义成分不被低频运动淹没，**同步机制**则通过训练中的对齐损失和推理中的显式同步步骤，强制多体运动在几何与语义层面保持一致。两者共同作用，使得 SyncDiff 能够有效消除穿透、接触丢失和异步等现有多体生成方法的典型失败模式。

### 补充图表

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SyncDiff. The light blue boxes show the inference process with explicit synchronization steps performed every s step. For denoising steps irrelevant to explicit synchronization (those marked as*

## 核心模块与公式推导

SyncDiff 的核心架构由四个关键模块构成，它们协同工作以解决多体交互运动生成中的同步与语义保留问题。

### 运动表示与频率分解

SyncDiff 将多体运动统一表示为一个高阶向量 $\mathbf{x}$，该向量由所有个体的运动（如人体/手的关节旋转与平移）以及所有物体-物体、人体/手-物体之间的相对运动拼接而成。这一表示无需预定义物体运动轨迹或交互关键帧，释放了对先验引导的依赖。

为了显式保留高频语义成分（如精细的周期性接触动作），模型对序列中的每个运动通道独立执行快速傅里叶变换（FFT）。给定长度为 $N$ 的运动序列 $x_u$，其频域分解为：

$$x_{u \in [0, N-1]} = \sum_{l=0}^{N-1} a_l \cos(u \phi_l) + b_l \sin(u \phi_l)$$

随后，将频率分量划分为低频（dc）与高频（ac）两部分，以截止频率上界 $L=16$ 为界：

$$x_{\mathrm{dc}, u} = \sum_{l=-3}^{2} a_l \cos(u \phi_l) + b_l \sin(u \phi_l)$$

$$x_{\mathrm{ac}, u} = \sum_{l \in [-L, -4] \cup [3, L-1]} a_l \cos(u \phi_l) + b_l \sin(u \phi_l)$$

低频分量捕获运动的整体趋势，而高频分量则编码精细的振动与接触语义，确保后者不会在扩散去噪过程中被低频运动所淹没。

### Transformer 去噪骨干

模型采用基于 Transformer 的潜在扩散范式（latent diffusion）对上述分解后的运动进行联合去噪。条件信号包括：从预训练 CLIP 提取的动作与物体类别文本特征，以及通过基点点集（BPS）编码的物体几何特征。该骨干网络同时对个体运动与相对运动进行预测，为后续的同步约束提供原始样本分数。

### 对齐损失与训练约束

为在训练阶段显式注入多体同步先验，SyncDiff 引入了对齐损失 $\mathcal{L}_{\mathrm{align}}$。该损失计算所有物体-物体对和人体/手-物体对之间，预测的相对运动 $\hat{x}_{o_{j_2} \to o_{j_1}}$ 与由个体运动导出的相对运动之间的 L2 误差：

$$\mathcal{L}_{\mathrm{align}} = \sum_{j_1, j_2 \in [1, m], j_1 \neq j_2} \| \hat{x}_{o_{j_2} \to o_{j_1}} - \mathrm{rel}(\hat{x}_{o_{j_1}}, \hat{x}_{o_{j_2}}) \|_2^2 + \sum_{i \in [1, n], j \in [1, m]} \| \hat{x}_{h_i \to o_j} - \mathrm{rel}(\hat{x}_{o_j}, \hat{x}_{h_i}) \|_2^2$$

最终的综合损失函数为各分量的加权组合：

$$\mathcal{L} = \lambda_{\mathrm{dc}} \mathcal{L}_{\mathrm{dc}} + \lambda_{\mathrm{ac}} \mathcal{L}_{\mathrm{ac}} + \lambda_{\mathrm{align}} \mathcal{L}_{\mathrm{align}} + \lambda_{\mathrm{norm}} \mathcal{L}_{\mathrm{norm}}$$

其中 $\mathcal{L}_{\mathrm{dc}}$ 与 $\mathcal{L}_{\mathrm{ac}}$ 分别为低频与高频分量的重建损失，$\mathcal{L}_{\mathrm{norm}}$ 为四元数归一化损失，以确保旋转表示的合法性。

### 显式同步推理

在推理阶段，SyncDiff 将多体交互建模为一个动态图模型，并执行最大似然同步采样。标准扩散去噪步骤为：

$$\hat{x}_{t-1} = \hat{\mu}(\hat{x}_t, t) + \sigma_t \epsilon \quad (\epsilon \sim \mathcal{N}(0, I))$$

在实际推理中，模型每隔 $s$ 步（$s=50$，总去噪步数 $T=1000$）执行一次显式同步操作。以刚性物体为例，其运动更新融合了来自其他物体的相对运动信息与自身预测均值，从而强制个体运动与相对运动之间的一致性。更新后的同步运动 $\hat{x}'$ 被重新注入去噪循环，用于后续的逐步去噪。这一机制等价于在动态图模型上最大化联合似然，从数学上保证了多体运动的全局同步性。

## 实验与分析

### 总体表现：多数据集全面领先

SyncDiff 在五个涵盖手‑物、人‑物、多物体交互的数据集上进行了系统评估，所有主实验结果均指向同一结论：**同步机制与频率分解共同带来了接触一致性与语义准确率的显著跃升**。表 1‑5 给出了各数据集的核心指标，这里提炼关键瓶颈与因果证据。

在双物体‑双手交互数据集 **TACO** 上，SyncDiff 的接触交并比 **CSIoU** 达到 73.00%，动作识别准确率 **RA** 达到 73.28%，分别超出最强基线 DiffH2O 逾 10 个百分点（Table 1）。这一差距的根源在于 DiffH2O 等基线缺乏显式同步约束，导致手与物体、物体与物体之间频繁出现穿透或接触丢失（Figure 4 定性展示）。SyncDiff 通过**对齐损失**在训练中强制预测相对运动与由个体运动导出的相对运动一致，并在推理中每隔 50 步执行**显式同步**，将多体运动更新形式化为图模型上的最大似然采样，从而从根本上抑制了异步与穿透。

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/005_Table_1.jpg]]
*Table 1: Results on TACO [48] dataset. The best in each column is highlighted in bold*

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results from TACO [48] dataset. Invalid action indicates the poses cannot complete the operation effectively*

在 **GRAB** 抓取后阶段，SyncDiff 在未见主体（Unseen Subject）划分下 CSIoU 达 44.92%，较 DiffH2O 提升 16.32 个百分点（Table 2）。该场景的难点在于物体已被抓取，手‑物相对运动幅度极小，基线方法容易丢失高频微动。SyncDiff 的**频率分解**将运动显式拆分为低频（dc）与高频（ac）分量，确保细微的周期性接触调整不被大尺度身体运动淹没——这是因果调节变量的直接证据。

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/009_Table_2.jpg]]
*Table 2: Comparison on GRAB [81] dataset for the post-grasping phase. Following DiffH2O [13], we conduct experiments on the phase where the object has been grasped. Each column highlights the best method in red, with the second best highlighted in blue. Results of IMoS [24] and*

在多人物体交互数据集 **CORE4D** 和 **BEHAVE** 上，SyncDiff 的接触保持率 **CRR** 分别达到 6.15% 和 10.29%，均显著优于 CG‑HOI 和 OMOMO（Table 3, 4）。值得注意的是，这两个数据集的 CRR 绝对值整体偏低，反映出多人‑多物体长序列交互中保持持续接触本身就是开放性难题。SyncDiff 的优势在于其同步机制可**动态建模任意数量身体之间的相对关系**，而基线方法通常只考虑单人或双手与单物体的交互，面对多人协作场景时缺乏跨身体约束，产生不合理的抓取姿态（Figure 8）。

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/012_Table_3.jpg]]
*Table 3: Results on CORE4D [109] dataset. The best in each column is highlighted in bold*

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative results from BEHAVE [2] dataset. Baseline methods suffer from unreasonable grasp poses due to unsynchronized synthesis of body transformations*

在 **OAKINK2** 数据集上，SyncDiff 的 CSIoU 达 72.14%，超出 MACS 达 20.92 个百分点（Table 5）。该数据集要求瓶盖与瓶身的精确对齐与螺旋拧紧动作（Figure 6），属于高频语义密集型任务。MACS 等基线仅建模时域轨迹，无法捕捉旋转相位等高频成分，而 SyncDiff 的频域显式建模直接针对这一瓶颈，使语义识别准确率平均超越现有最先进方法 **15% 以上**。

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/013_Table_5.jpg]]
*Table 5: Results on OAKINK2 [108] dataset. The best in each column is highlighted in bold*

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative results from OAKINK2 [108] dataset. The task requires precise contact between objects, where the bottle cap needs to align perfectly with the bottle, and there needs to be a tendency for it to be twisted down in a clockwise spiral. while our method mitigates these issues*

### 消融实验：三个关键设计的因果验证

消融实验从三个维度拆解了 SyncDiff 的贡献：

1. **频率分解的移除**：当去掉频率分解模块、直接对原始时域运动进行扩散时，TACO 数据集上的语义指标 FID 和 RA 显著下降（Table 11），同时高频分量重建误差增大（Table 10）。定性结果（Figure 10）显示，移除分解后，锅铲在盘子表面的周期性相对运动退化为局部小范围停滞，丧失了“翻炒”这一高频语义。这直接验证了核心洞察：**高频成分是动作类别识别的关键载体，低频统一建模会使其被淹没**。

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/015_Figure_10.jpg]]
*Figure 10: Qualitative results from TACO [48] dataset. Periodic relative motions are required between two objects. The color changes from deep to light, representing time passage. After removing the decomposition mechanism, the spatula tends to get stuck in a small area on the plate’s surface, without effective relative movements*

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/021_Table_11.jpg]]
*Table 11: Semantic quality of ablation studies on TACO [48] dataset. The best in each column is highlighted in bold*

2. **对齐损失 L_align 的移除**：在 TACO、CORE4D、OAKINK2 三个数据集上，移除对齐损失后 CSIoU 和 CSR 等接触指标均出现明显下降（Table 1, 3, 5）。对齐损失是训练阶段唯一的同步约束信号，其缺失意味着模型仅依赖隐式共现学习相对运动，无法保证个体运动与相对运动的几何一致性，穿透与接触丢失随之增加。

3. **显式同步步骤的移除**：即使保留了训练时的对齐损失，若推理时不执行显式同步，接触指标与动作识别率同样降低（Table 1, 3, 5）。这表明训练阶段的对齐分数必须在推理时被主动利用——显式同步步骤相当于在采样过程中持续注入图模型的结构先验，将个体去噪均值与相邻身体的运动信息融合，从而最大化总体似然。

此外，同步间隔 $s$ 的调节实验（Table 7）表明，$s=50$ 在推理速度与语义准确率之间取得了良好平衡：过大的 $s$ 使同步频率不足，接触质量下降；过小的 $s$ 则增加计算开销而收益递减。

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/017_Table_7.jpg]]
*Table 7: Results for different s on TACO Split 1*

### 关键定性发现与失败模式

定性可视化揭示了基线方法的典型失败模式，这些模式恰好对应 SyncDiff 设计所针对的瓶颈：

- **穿透与接触丢失**（Figure 3, 4, 7）：基线方法在双手‑物体或多人物体场景中频繁出现手穿入物体或脱离接触的现象，根本原因在于缺乏跨身体同步约束。SyncDiff 的显式同步步骤在推理时持续校正个体运动，使手与物体、物体与物体之间保持合理的相对位姿。
- **不合理抓取姿态**（Figure 8）：在 BEHAVE 数据集上，OMOMO 等基线因未同步身体变换与手部运动，产生违反物理常识的抓取姿态。SyncDiff 通过图模型联合推理所有身体的运动，避免了此类不一致。
- **高频语义丢失**（Figure 10）：移除频率分解后，周期性相对运动退化为静止或随机抖动，证明频域建模对于保留“搅拌”“拧紧”等功能性动作语义是不可或缺的。

### 评估公平性说明

RA 指标使用的动作分类器在 train/val/test 全集合上训练，可能对生成模型产生偏向。作者通过用户研究（Figure 9）验证了相对排名的合理性，但指出**缺乏基于轨迹的动作识别基础模型**是当前领域的共性问题，RA 的跨方法可比性需结合接触指标综合判断。

### 推理效率与局限性

推理时间方面（Table 8, 9），显式同步步骤的时间复杂度随身体数量二次增长。在 200 帧人‑物交互序列上，SyncDiff 的推理时间高于无同步的基线，这是同步机制的计算代价。作者已将铰接物体拆分为刚体部分处理，但未利用内在关节约束，这限制了在需要精确关节运动（如工具操作）场景中的物理真实性。此外，相对运动表示局限于刚体坐标系，不适用于纯多人交互合成，通用性受限。

### 补充图表

![[assets/figures/papers/paper_list_l1776_SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Inter/figures/011_Table_4.jpg]]
*Table 4: Results on BEHAVE [2] dataset. The best in each column is highlighted in bold*

## 方法谱系与知识库定位

### 1. 方法脉络与关键差异

SyncDiff 针对的核心瓶颈是：现有多体运动生成方法在合成任意数量身体（手、人体、刚体）的交互时，难以保证精确的时空同步，尤其在高频微小运动和复杂高阶关系上，容易产生穿透、接触丢失或语义缺失。SyncDiff 的因果调节变量在于：将对齐分数（alignment scores）引入训练，并在推理中通过动态图模型上的显式同步步骤，联合优化数据样本分数与对齐分数，从而直接约束个体运动与相对运动的一致性。

在方法谱系上，SyncDiff 与以下基线形成明确对比：

- **MACS**（手物交互基线，单物体多手）：仅依赖隐式共现，缺乏显式同步机制，在 OAKINK2 数据集上接触指标 CSIoU 仅为 51.22%，SyncDiff 提升至 72.14%（+20.92 个百分点）。
- **DiffH2O**（手物交互基线，双手单物体）：同样缺少同步机制，在 TACO 数据集上 CSIoU 为 62.29%、动作识别率 RA 为 61.40%，SyncDiff 分别达到 73.00% 和 73.28%。
- **CG-HOI**（人物交互基线，多人单物体）：在 CORE4D 数据集上接触鲁棒率 CRR 为 3.67%，SyncDiff 提升至 6.15%。
- **OMOMO**（人物交互基线，单人单物体）：在 BEHAVE 数据集上 CRR 为 7.88%，SyncDiff 达到 10.29%。
- **IMoS**（手物交互基线，抓取后阶段）：在 GRAB 数据集上参与抓取后阶段比较，SyncDiff 在未见主体划分上 CSIoU 达 44.92%，远超 DiffH2O 的 28.60%。

从技术栈角度看，SyncDiff 在三个关键槽位上做出了改变：

| 槽位 | 基线做法 | SyncDiff 做法 |
|------|----------|---------------|
| 运动表示 | 仅使用时域轨迹 | 频率分解：显式建模低频（dc）和高频（ac）分量，在频域保留高频语义成分 |
| 同步机制 | 依赖隐式共现或无同步 | 训练时引入对齐分数及对齐损失；推理时按图模型执行显式同步，最大化总体似然 |
| 损失函数 | 标准扩散重建损失 | 叠加 DC 损失、AC 损失、对齐损失与四元数归一化损失（Eq. 4） |

频率分解的引入确保了高频语义成分（如周期性微小运动）不被低频运动淹没，这对动作类型的识别至关重要。消融实验证实，移除频率分解后语义指标 FID 和 RA 显著下降，且重建的高频分量误差增大（Table 10, Table 11）。移除对齐损失则导致接触指标 CSIoU、CSR 明显下降（Table 1, Table 3, Table 5），移除显式同步步骤同样使接触指标和动作识别率降低，证明同步步骤的必要性。

### 2. 适用边界与局限

SyncDiff 的适用边界由以下因素界定：

**（1）铰接物体的关节感知建模缺失。** SyncDiff 直接将铰接物体拆分为刚体部分进行建模，未利用内在关节约束。这意味着对于需要关节运动一致性的场景（如剪刀开合、工具箱打开），模型无法保证物理上合理的关节运动，可能产生不自然的物体变形。

**（2）显式同步的计算复杂度随身体数量二次增长。** 同步步骤需要对所有物体-物体对和人体/手-物体对进行更新，当交互身体数量较大时，计算开销显著增加。当前设置中同步间隔 s=50 在推理速度与语义准确率之间取得了平衡（Table 7），但在实时应用或大规模场景中仍可能成为瓶颈。

**（3）不保证物理真实性。** 尽管同步机制大幅改善了接触一致性和穿透问题，但模型输出的运动并不经过物理仿真验证，微小误差在真实机器人任务中可能导致操作失败。这限制了 SyncDiff 在需要严格物理约束的下游任务（如机器人抓取执行）中的直接应用。

**（4）相对运动表示局限于刚体坐标系。** SyncDiff 的相对运动表示依赖于刚体坐标系变换，这使得框架天然适用于人-物和手-物交互，但对于纯多人交互场景（如双人舞蹈、多人运动配合），缺乏合适的相对运动表示，通用性受限。

### 3. 开放问题

基于 SyncDiff 的方法定位和已知局限，以下开放问题值得进一步探索：

- **铰接物体约束整合**：如何将铰接物体的关节约束整合到多体似然建模中？可能的路径包括在运动表示中引入关节角度参数化，或在同步步骤中加入关节一致性约束项。

- **同步关系的稀疏化与效率提升**：能否利用人体先验或学习策略过滤非必要的同步关系，以降低显式同步的计算开销？例如，仅在接触可能性高的物体对之间执行同步，或通过图稀疏化策略减少同步更新的边数。

- **功能性操作常识的学习**：在缺少 affordance 数据的场景下，如何使模型学习到功能性操作常识？当前模型依赖动作标签和物体类别特征，但对于需要理解物体功能 affordance 的复杂操作（如拧瓶盖需要旋转趋势），模型可能缺乏足够的语义理解。

- **更通用的相对运动表示**：针对纯多人交互，如何设计不依赖刚体坐标系的相对运动表示？可能的方案包括基于骨骼拓扑的相对旋转表示，或基于注意力机制的隐式关系建模。

- **动作识别评估的公平性改进**：当前 RA 指标使用的分类器在 train/val/test 全集合上训练，可能偏向生成模型。作者通过用户研究验证了相对排名的合理性，但缺乏基于轨迹的动作识别基础模型仍是领域共性问题。开发此类基础模型将改善评估的公平性和泛化性。

- **实时应用扩展**：SyncDiff 能否通过模型蒸馏或更高效的同步策略（如减少总去噪步数 T、优化同步间隔 s）扩展至实时应用？当前 T=1000、s=50 的设置离实时推理仍有距离，需要进一步的速度-质量权衡研究。

## 原文 PDF

![[paperPDFs/ICCV_2025/SyncDiff_Synchronized_Motion_Diffusion_for_Multi_Body_Human_Object_Interaction_Synthesis.pdf]]