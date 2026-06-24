---
title: "U^2Flow: Uncertainty-Aware Unsupervised Optical Flow Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/U_2Flow_Uncertainty_Aware_Unsupervised_Optical_Flow_Estimation.pdf
project_link: null
code_link: "https://github.com/sunzunyi/U2FLOW"
aliases:
- U2
- U2UAUOFE
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 利用数据增强下的预测不一致性构建自监督不确定性信号（Laplace似然），并将预测的不确定性解耦引入网络，用于自适应流精炼和损失调制。
primary_logic: 通过强制模型在多种增强下保持预测一致性，暴露其低置信区域，由此产生的逐像素不确定性可作为一种内在反馈，指导网络动态抑制不可靠的特征和训练信号，实现无监督下光流与不确定性的联合优化。
claims:
- U2Flow 是首个循环无监督框架，联合估计光流和逐像素不确定性，达到最先进性能。
- 基于增强一致性的解耦不确定性学习策略提供了稳定的自监督信号。
- 预测的不确定性被有效用于引导流精炼和调制区域平滑损失。
- U2Flow 在 KITTI-2015 上 Fl-all 达到 6.13%，显著优于 UPFlow (9.38%)。
---

# U^2Flow: Uncertainty-Aware Unsupervised Optical Flow Estimation

> [!tip] 核心洞察
> 通过强制模型在多种增强下保持预测一致性，暴露其低置信区域，由此产生的逐像素不确定性可作为一种内在反馈，指导网络动态抑制不可靠的特征和训练信号，实现无监督下光流与不确定性的联合优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | U^2Flow: 不确定性感知的无监督光流估计 |
| 英文题名 | U^2Flow: Uncertainty-Aware Unsupervised Optical Flow Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Sun_U2Flow_Uncertainty-Aware_Unsupervised_Optical_Flow_Estimation_CVPR_2026_paper.html) · [Code](https://github.com/sunzunyi/U2FLOW) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | U^2Flow |
| Dataset | KITTI 2015, Sintel, Sintel Clean test |

> [!tip] 效果简介
> - KITTI 2015 上，Fl-all (%) 6.13 vs UPFlow 9.38 (-3.25)。
> - Sintel (final+clean) 上，AUSE / CC 0.11 / 0.66。
> - Sintel Clean test 上，EPE 2.83。

## 概述

无监督光流估计的核心瓶颈在于缺乏可靠的不确定性信号：即便模型能输出逐像素预测，也难以判断“哪里不可信”，更无法利用这一信息反向提升光流精度与鲁棒性。U²Flow 针对这一缺口，提出首个循环无监督框架，**联合估计光流与逐像素不确定性**，并将预测的不确定性解耦引入网络，用于自适应流精炼和损失调制。

其核心洞察是：**通过强制模型在多种数据增强下保持预测一致性，暴露其低置信区域**，由此产生的逐像素不确定性可作为一种内在反馈，指导网络动态抑制不可靠的特征和训练信号，实现无监督下光流与不确定性的联合优化。具体而言，U²Flow 从增强一致性中导出 Laplace 似然的自监督不确定性目标，并将该目标与主流损失解耦训练，避免梯度干扰；同时，预测的不确定性被用于缩放流特征以精炼残差，以及生成可靠性掩码来调制同应性平滑损失。

实验表明，U²Flow 在 KITTI-2015 上达到 Fl-all **6.13%**，显著优于此前无监督方法 UPFlow（9.38%），并在 Sintel 基准上取得最先进的无监督性能。消融实验确认：解耦训练策略、不确定性感知精炼模块和不确定性引导的双向融合对性能提升至关重要；但也揭示出同应性平滑损失仅在 KITTI 等刚性场景有效，在 Sintel 上反而损害精度，构成方法泛化性的一个已知限制。

## 背景与动机

光流估计是计算机视觉中的基础任务，旨在恢复连续视频帧之间逐像素的密集运动场。近年来，基于深度学习的监督方法取得了显著进展，但其对大规模稠密真值标注的依赖严重制约了在真实场景中的可扩展性。无监督光流估计通过光度一致性等自监督信号绕开了标注瓶颈，因而成为极具吸引力的替代方案。

然而，无监督范式面临一个关键的结构性缺陷：**缺乏可靠的不确定性估计手段**。在监督学习中，模型可通过与真值的残差自然导出预测置信度；但在无监督设定下，光度误差本身受光照变化、遮挡、纹理缺失等因素污染，无法直接作为不确定性的代理。更棘手的是，即便通过某些启发式方法获得了不确定性估计，**如何将其有效集成以提升光流精度和鲁棒性**仍是一个开放问题——现有方法大多将不确定性视为独立的后处理产物，而非嵌入估计循环的驱动信号。

这一缺口在真实世界应用中尤为突出。自动驾驶和机器人导航等安全关键系统不仅需要准确的光流，还必须知道“哪里不可靠”，以便下游模块做出风险感知决策。现有无监督方法（如 **UPFlow**，Luo et al., CVPR 2021）仅输出点估计，无法提供这种能力。同时，基于循环架构的先进方法（如 **RAFT**，Teed and Deng, ECCV 2020；**SMURF**，Stone et al., CVPR 2021）虽然在精度上不断突破，但其迭代精炼过程并未显式建模预测的不确定性，导致网络在遮挡边界、运动不连续处仍会产生高误差却无预警的输出。

本文的动机正源于此：**能否让无监督光流模型在估计运动的同时，自省地感知其预测的不可靠性，并利用这种感知反向优化估计过程？** 核心洞察在于，通过对同一输入施加多种数据增强并强制预测一致性，模型在不同增强下的输出差异天然暴露了其低置信区域——这是一种无需真值的、内在的不确定性信号。将该信号解耦引入循环更新机制，可同时实现两个目标：为每个像素提供可解释的不确定性估计，以及利用该不确定性动态调制特征精炼和损失函数，从而在无监督条件下实现光流与不确定性的联合优化。

基于上述动机，本文提出 **U²Flow**——首个循环无监督框架，联合估计光流和逐像素不确定性，并将预测的不确定性作为内在反馈，贯穿流精炼、平滑损失调制和双向融合等多个环节，最终在 KITTI 和 Sintel 等主流基准上取得无监督方法的最先进性能。

## 核心创新

U²Flow 的核心创新在于将**不确定性估计**从无监督光流训练中的附属产物提升为**内在驱动信号**，通过三个耦合的机制形成闭环：自监督不确定性生成 → 不确定性感知流精炼 → 不确定性引导的损失调制。这一设计使得网络能够在无真实标签的条件下，同时优化光流预测和逐像素置信度，并将置信度反哺给流估计本身。

### 1. 解耦的不确定性自监督信号

无监督光流缺乏直接的不确定性真值，U²Flow 的关键突破在于利用**数据增强下的预测不一致性**构建监督信号。具体而言，对同一输入施加不同增强（如色彩抖动、空间变换），模型会产生略有差异的光流预测；这些差异的分布被建模为 Laplace 分布，并通过极大似然估计（MLE）目标训练不确定性头部：

$$\tilde{\ell}_{\mathrm{unc}}^{(k)}(p) = \sqrt{2} \exp(-\frac{1}{2}\pmb{\alpha}^{(k)}(p)) \hat{D}^{(k)}(\pmb{p}) + \frac{1}{2}\pmb{\alpha}^{(k)}(p)$$

其中 $\pmb{\alpha}^{(k)} = \log(\pmb{\sigma}_{12}^{2(k)})$ 为对数方差预测，$\hat{D}^{(k)}$ 为不同增强下流预测的绝对差异。该损失在数值上稳定，且**解耦于主流损失**——通过阻断梯度传播（stop-gradient），防止不确定性学习干扰光流主任务。

这一策略的因果逻辑是：**迫使模型在多种增强下保持预测一致性，暴露其低置信区域**。消融实验（Table 3）证实，仅添加不确定性头部而不解耦训练会导致性能下降，验证了解耦设计的必要性。

### 2. 不确定性感知的流精炼模块

传统循环光流架构（如 **RAFT**，Teed and Deng, ECCV 2020）直接从隐藏状态预测流残差，未考虑不同空间位置的置信度差异。U²Flow 将预测的不确定性显式注入精炼过程：

1. 不确定性头部从 GRU 隐藏状态 $\mathbf{h}^{(k)}$ 解码对数方差 $\pmb{\alpha}^{(k)}$；
2. 通过 sigmoid 变换生成可靠性图 $\mathbf{s}^{(k)} = \phi(-\pmb{\alpha}^{(k)})$；
3. 用该可靠性图逐像素缩放流特征 $\tilde{\mathbf{f}}^{(k)} = \mathbf{f}^{(k)} \odot \mathbf{s}^{(k)*}$（阻断梯度）；
4. 将原始特征、缩放特征和不确定性图拼接后，由卷积层预测流残差 $\Delta\mathbf{F}_{12}^{(k)}$。

这一设计的直觉是：**高不确定性区域的特征被抑制，网络被引导依赖更可靠的线索进行精炼**。消融实验（Table 4）表明，该模块在所有基准上优于无精炼和标准精炼（无不确定性引导），验证了不确定性信息对精炼的增益。

### 3. 不确定性引导的损失调制与双向融合

U²Flow 将不确定性进一步用于两个下游环节：

- **同应性平滑损失的可靠性掩码**：传统方法使用遮挡掩码排除不可靠像素，但遮挡并不等价于高误差。U²Flow 采用不确定性阈值 $\tau_{hg}$ 筛选高置信像素参与同应性估计和损失计算（Figure 3 显示不确定性掩码比遮挡掩码更准确地指示流误差区域）。需注意，该损失假设平面刚体运动，在 Sintel 等复杂场景下反而降低性能，消融实验（Table 3）明确建议在 Sintel 上禁用此损失。

- **不确定性引导的双向流融合**：利用前向/后向不确定性生成融合掩码 $\mathbf{M}_{\mathrm{fused}}$，自适应地融合原始前向流与后向流导出的预测。消融实验（Table 5）显示该策略在 Sintel 和 KITTI 上均优于基于遮挡的融合和无融合，尤其提升了非遮挡区域精度。

### 创新总结

相较于仅估计光流的无监督方法（如 **UPFlow**，Luo et al., CVPR 2021），U²Flow 的三个 changed slots 构成递进关系：**解耦的自监督不确定性**提供可靠信号源，**不确定性感知精炼**将该信号注入流估计核心，**不确定性引导的融合与损失调制**在输出和后处理阶段进一步利用该信号。这一“估计—反馈—调制”的闭环是无监督光流中不确定性从副产品升级为核心组件的首次系统实践。

## 整体框架

U²Flow 的整体架构继承自 **RAFT**（Teed & Deng, ECCV 2020）的循环迭代范式，并在此基础上引入了三个核心创新模块：不确定性估计头、不确定性感知的精炼模块，以及不确定性引导的双向流融合模块。图 2 给出了完整的架构概览。

**输入与特征提取。** 给定连续两帧 RGB 图像 $\mathbf{I}_1, \mathbf{I}_2 \in \mathbb{R}^{H \times W \times 3}$，首先通过共享的特征编码器提取逐像素特征，并构建全对相关体积（4D correlation volume）$C$。遵循 **SMURF**（Stone et al., CVPR 2021）的设计，所有批归一化层被替换为实例归一化，以增强无监督训练的稳定性。

**循环更新与不确定性估计。** 在每次迭代 $k$ 中，GRU 更新块从相关体积中检索特征，并结合当前光流估计输出隐藏状态 $\mathbf{h}^{(k)}$。该隐藏状态同时馈入两个分支：
1. **流特征解码器** $\mathcal{C}_{\mathrm{flow}}$ 产生中间流特征 $\mathbf{f}^{(k)}$；
2. **不确定性估计头** $\mathcal{C}_{\mathrm{unc}}$ 预测对数方差 $\boldsymbol{\alpha}^{(k)} = \log(\boldsymbol{\sigma}_{12}^{2(k)})$，保证数值稳定性。

**不确定性感知精炼。** 不确定性并非仅作为输出副产品，而是被反向注入流估计过程。具体地，对数方差经 sigmoid 变换得到可靠性图 $\mathbf{s}^{(k)} = \phi(-\boldsymbol{\alpha}^{(k)})$，用于逐像素缩放流特征：$\tilde{\mathbf{f}}^{(k)} = \mathbf{f}^{(k)} \odot \mathbf{s}^{(k)*}$（$*$ 表示阻断梯度传播）。随后，原始流特征、缩放后的流特征与不确定性图拼接，经卷积层预测流残差 $\Delta\mathbf{F}_{12}^{(k)}$，实现不确定性引导的自适应精炼。

**损失监督与解耦设计。** 总损失 $\ell_{\mathrm{Total}}$ 由同应性平滑损失和逐迭代损失加权求和构成，后者包含光度损失、平滑损失、增强正则化损失（源自 **ARFlow**, Liu et al., CVPR 2020）、语义损失（源自 **UnSAMFlow**, Yuan et al., CVPR 2024）以及不确定性 MLE 损失。关键设计在于：不确定性监督信号通过数据增强一致性自监督产生，且不确定性损失与主流损失解耦——梯度不通过 $\mathbf{s}^{(k)*}$ 回传至流特征，避免不确定性学习干扰光流优化。

**后处理融合。** 在推理阶段，利用前向与后向不确定性分别生成二值可靠性掩码 $\mathbf{M}_{\mathrm{f}} = \mathbb{1}(\boldsymbol{\sigma}_{t \to t+1}^{2} < \theta)$ 和 $\mathbf{M}_{\mathrm{b}}$，自适应融合原始前向流与后向流导出的预测，以轻量后处理方式获得多帧收益，无需大规模重训练。

### 补充图表

![[assets/figures/papers/paper_list_l2113_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_U2Flow_Uncertainty/figures/002_Figure_2.jpg]]
*Figure 2: Overview of U2Flow architecture. (a) The overall recurrent structure follows RAFT [47]. (b) The uncertainty-aware refinement module and the uncertainty estimation head respectively predict optical flow and per-pixel uncertainty in the recurrent update block*

## 核心模块与公式推导

### 特征提取与相关体构建

U²Flow 继承 **RAFT**（Teed and Deng, ECCV 2020）的循环架构，输入两帧连续 RGB 图像 $\mathbf{I}_1, \mathbf{I}_2 \in \mathbb{R}^{H \times W \times 3}$，通过特征编码器提取逐像素特征，并计算全对余弦相似度构建 4D 相关体积 $\mathbf{C}$。遵循 **SMURF**（Stone et al., CVPR 2021）的设计，将所有批归一化层替换为实例归一化以增强无监督训练的稳定性。

### 循环更新块与不确定性估计头

循环更新块（GRU）以相关体积查找结果和当前光流估计为输入，迭代输出隐藏状态 $\mathbf{h}^{(k)}$，其中 $k$ 为迭代步。在此基础上，U²Flow 引入两个关键模块：

**不确定性估计头** 从隐藏状态解码对数方差，以保证数值稳定：

$$\pmb{\alpha}^{(k)} = \log(\pmb{\sigma}_{12}^{2(k)}) \quad \text{(Eq. 2)}$$

其中 $\mathcal{C}_{\mathrm{unc}}$ 为两层卷积解码器。对负对数方差施加 sigmoid 得到可靠性指示图：

$$\mathbf{s}^{(k)} = \phi(-\pmb{\alpha}^{(k)}) \quad \text{(Eq. 3)}$$

**不确定性感知精炼模块** 利用可靠性图调制流特征。首先通过 $\mathcal{C}_{\mathrm{flow}}$ 从隐藏状态解码中间流特征 $\mathbf{f}^{(k)}$，随后进行梯度阻断的逐像素缩放：

$$\tilde{\mathbf{f}}^{(k)} = \mathbf{f}^{(k)} \odot \mathbf{s}^{(k)*} \quad \text{(Eq. 4)}$$

其中 $(\cdot)^{*}$ 表示停止梯度传播，阻断不确定性梯度对主流特征的反向影响。流残差由缩放特征、原始特征与不确定性图拼接后预测：

$$\Delta\mathbf{F}_{12}^{(k)} = \mathcal{C}'_{\mathrm{flow}}(\mathrm{concat}(\mathbf{f}^{(k)}, \tilde{\mathbf{f}}^{(k)}, \alpha^{(k)*})) \quad \text{(Eq. 5)}$$

最终光流更新为 $\mathbf{F}_{12}^{(k)} = \mathbf{F}_{12}^{(k-1)} + \Delta\mathbf{F}_{12}^{(k)}$。

### 自监督不确定性学习

在无真值条件下，U²Flow 通过 **增强一致性** 原理生成不确定性监督信号。核心思想：对输入施加数据增强后，模型在低置信区域的预测一致性会下降，这种不一致性可作为不确定性的自监督目标。

具体地，对原始帧和增强帧分别估计光流 $\hat{\mathbf{F}}_{12}^{(k)}$ 与 $\hat{\mathbf{F}}_{12}^{\prime(k)}$，以二者的差异 $\hat{D}^{(k)}(\pmb{p})$ 作为目标误差，采用 Laplace 分布假设下的负对数似然（NLL）作为不确定性损失。为数值稳定，最终形式为：

$$\tilde{\ell}_{\mathrm{unc}}^{(k)}(p) = \sqrt{2} \exp\left(-\frac{1}{2}\pmb{\alpha}^{(k)}(p)\right) \hat{D}^{(k)}(\pmb{p}) + \frac{1}{2}\pmb{\alpha}^{(k)}(p) \quad \text{(Eq. 9)}$$

该损失 **解耦** 于主流损失，即 $\alpha^{(k)}$ 的梯度不通过 $\hat{D}^{(k)}$ 反传至光流预测分支，避免不确定性学习干扰光流优化。消融实验证实，仅添加不确定性头而无解耦训练会导致性能下降。

### 不确定性增强的同应性平滑损失

传统同应性平滑损失使用遮挡掩码排除不可靠像素。U²Flow 引入 **不确定性掩码** 替代：仅当预测方差低于阈值 $\tau_{\mathrm{hg}}$ 时，像素参与同应性估计与损失计算：

$$\ell_{\mathrm{hg}} = \frac{1}{H' \times W'} \sum_{p} \|\mathbf{F}_{ij}(\pmb{p}) - \mathbf{F}_{ij}^{\mathrm{H}}(\pmb{p})\|_1 \quad \text{(Eq. 7)}$$

其中 $\mathbf{F}_{ij}^{\mathrm{H}}$ 为通过 RANSAC 拟合的同应性精炼流。不确定性掩码相比遮挡掩码能更精确地指示高误差区域（见 Figure 3），为刚体运动场景提供更可靠的平滑约束。但该损失假设平面刚体运动，仅在 KITTI 上有效，在 Sintel 复杂场景下反而损害性能。

![[assets/figures/papers/paper_list_l2113_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_U2Flow_Uncertainty/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of different masks for indicating flow errors. The masks are visualized as translucent green overlays on the optical flow error maps, where correct estimations are shown in blue, incorrect ones in red, and black pixels denote regions without ground truth. As shown in (c), some high-error regions remain unmasked, while certain low-error regions are incorrectly masked. In contrast, our method (d) accurately identifies high-error regions, providing more reliable cues for subsequent homography smoothness (Sec. 3.3), flow fusion (Sec. 3.4), and other downstream tasks*

### 不确定性引导的双向流融合

后处理阶段，U²Flow 利用前向不确定性 $\pmb{\sigma}_{t \to t+1}^{2}$ 与后向不确定性 $\pmb{\sigma}_{t \to t-1}^{2}$ 生成二值可靠性掩码：

$$\mathbf{M}_{\mathrm{f}} = \mathbb{1}(\pmb{\sigma}_{t \to t+1}^{2} < \theta), \quad \mathbf{M}_{\mathrm{b}} = \mathbb{1}(\pmb{\sigma}_{t \to t-1}^{2} < \theta)$$

融合掩码 $\mathbf{M}_{\mathrm{fused}} = \mathbf{M}_{\mathrm{f}} \cup \mathbf{M}_{\mathrm{b}}$ 标识至少一个方向高置信的像素，自适应融合原始前向流与由后向流导出的预测流。该模块作为轻量后处理，无需大规模重训练即可获得多帧方法的收益。

### 总损失函数

$$\ell_{\mathrm{Total}} = \lambda_{\mathrm{hg}} \ell_{\mathrm{hg}} + \sum_{k=1}^{K} \zeta^{K-k} \left( \ell_{\mathrm{ph}}^{(k)} + \lambda_{\mathrm{sm}} \ell_{\mathrm{sm}}^{(k)} + \lambda_{\mathrm{ar}} \ell_{\mathrm{ar}}^{(k)} + \lambda_{\mathrm{sem}} \ell_{\mathrm{sem}}^{(k)} + \lambda_{\mathrm{unc}} \ell_{\mathrm{unc}}^{(k)} \right) \quad \text{(Eq. 11)}$$

其中 $\ell_{\mathrm{ph}}$ 为光度损失，$\ell_{\mathrm{sm}}$ 为边缘感知平滑损失，$\ell_{\mathrm{ar}}$ 为增强正则化损失（继承自 **ARFlow**, Liu et al., CVPR 2020），$\ell_{\mathrm{sem}}$ 为语义增强损失（继承自 **UnSAMFlow**, Yuan et al., CVPR 2024），$\zeta^{K-k}$ 为指数衰减因子，赋予后期迭代更高权重。

### 补充图表

![[assets/figures/papers/paper_list_l2113_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_U2Flow_Uncertainty/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between previous optical flow estimation methods and our approach. (Left) Previous methods estimate only optical flow. (Right) Our proposed U2Flow framework jointly estimates optical flow and its uncertainty, and further leverages the predicted uncertainty to refine the flow estimation*

## 实验与分析

### 主要结果

U²Flow 在 Sintel 和 KITTI 两大公开基准上进行了系统评估，与监督和无监督方法进行全面对比（Table 1）。在 KITTI 2015 测试集上，U²Flow 取得 **Fl-all 6.13%**，显著优于此前无监督方法 UPFlow 的 9.38%（降幅达 3.25 个百分点）；启用双向流融合模块（+FF）后，Fl-all 进一步降至 **6.00%**。在 Sintel Clean 测试集上，U²Flow 的 EPE 为 2.83，Final 测试集为 4.16，均处于无监督方法的最优水平。

![[assets/figures/papers/paper_list_l2113_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_U2Flow_Uncertainty/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on Sintel and KITTI online benchmarks. Metrics evaluated at “all” (all pixels), “noc” (non-occlusions). MF denotes methods trained using multi-frame data. † denotes models with semantic inputs. “+FF” denotes our bidirectional flow fusion module. Missing entries (–) denote unreported results. Parentheses indicate that training and testing are conducted on the same dataset*

值得注意的是，U²Flow 在 KITTI 上的优势尤为突出，这与其训练策略密切相关：KITTI 训练额外引入了同应性平滑损失和语义增强，而 Sintel 训练未启用这两项。这种数据集特化的训练配置意味着 KITTI 上的性能增益不能完全迁移至 Sintel 场景，需审慎解读跨数据集的公平性。

在不确定性估计质量上，U²Flow 在 Sintel 训练集上取得 **AUSE 0.11 / CC 0.66** 的优异结果（Table 2），稀疏化曲线（Figure 4）表明其不确定性估计与真实误差高度一致，能够有效识别不可靠的流预测区域。

![[assets/figures/papers/paper_list_l2113_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_U2Flow_Uncertainty/figures/005_Table_2.jpg]]
*Table 2: Comparison of uncertainty estimation performance on the Sintel (final, clean) and KITTI (2012, 2015) training sets*

![[assets/figures/papers/paper_list_l2113_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_U2Flow_Uncertainty/figures/006_Figure_4.jpg]]
*Figure 4: Sparsification curves for uncertainty evaluation. Lower AUSE (shown in parentheses) is better*

### 消融实验

消融研究围绕五个关键组件展开（Table 3）：

![[assets/figures/papers/paper_list_l2113_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_U2Flow_Uncertainty/figures/008_Table_3.jpg]]
*Table 3: Ablation study on key components. We evaluate the impact of Uncertainty Estimation (UE), Decoupling of flow and uncertainty learning (Dec.), Flow Refinement (FR), uncertaintyenhanced*

**不确定性估计与解耦训练**：仅添加不确定性估计头（UE）而不解耦训练，反而导致性能下降；引入解耦策略（Dec.）后，不确定性监督信号通过梯度阻断与主流损失隔离，光流精度和不确定性质量均获显著提升。这一现象揭示了无监督不确定性学习中梯度冲突的关键瓶颈——不确定性头若与流预测共享梯度，会干扰主任务优化。

**不确定性感知流精炼**：Table 4 对比了无精炼、标准精炼（不含不确定性）和不确定性感知精炼三种方案。不确定性感知精炼在所有基准上均取得最低 EPE，验证了利用预测不确定性动态缩放流特征、抑制不可靠区域对残差预测贡献的有效性。

**不确定性引导双向融合**：Table 5 显示，基于不确定性的融合掩码优于传统遮挡掩码融合和无融合方案，尤其在非遮挡区域的精度提升显著。这得益于不确定性掩码能更准确地指示高误差区域（Figure 3），避免了遮挡掩码在低误差区误掩、高误差区漏掩的问题。

**同应性平滑损失**：该损失在 KITTI 上带来显著增益，但在 Sintel 上略微损害性能。消融实验明确指出，Sintel 训练中应禁用该损失。其根本原因在于同应性平滑假设平面刚体运动，KITTI 场景以刚性运动为主，而 Sintel 包含大量非刚性形变和复杂运动，该假设不再成立。

### 泛化能力

Table 6 展示了交叉数据集泛化实验：在 Sintel 上训练、直接在 KITTI 上测试，以及反向设置。U²Flow 在跨数据集场景下仍保持较强的泛化能力，但性能下降幅度表明域差异（合成 vs. 真实、刚性 vs. 非刚性运动）仍是无监督光流泛化的核心挑战。

![[assets/figures/papers/paper_list_l2113_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_U2Flow_Uncertainty/figures/010_Table_6.jpg]]
*Table 6: Generalization ability. Training on one dataset and testing directly on the other dataset*

### 失败模式与局限性

定性结果（Figure 5）显示，U²Flow 在运动边界和细结构区域（如 Sintel 的洞穴场景中人物肢体的快速运动）仍存在明显误差。这些区域往往同时具有高不确定性和高流误差，表明当前不确定性估计对极端运动模糊和非高斯噪声的捕获能力有限。

![[assets/figures/papers/paper_list_l2113_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_U2Flow_Uncertainty/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results on the KITTI test set (sample frames #5 and #9) and the Sintel (final pass) test set (samples: ambush 3, frame 23; cave 3, frame 16), compared with SMURF [41]. Additional examples can be found on the official benchmark website*

同应性平滑损失的场景依赖性构成了方法通用性的主要限制。此外，不确定性监督依赖于预定义的数据增强范围，可能无法覆盖真实世界中的非高斯误差源（如运动模糊、极端光照变化），导致分布外场景下不确定性估计欠佳。

### 补充图表

![[assets/figures/papers/paper_list_l2113_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_U2Flow_Uncertainty/figures/009_Table_4.jpg]]
*Table 4: Ablation study on the flow refinement module*

![[assets/figures/papers/paper_list_l2113_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_U2Flow_Uncertainty/figures/011_Table_5.jpg]]
*Table 5: Ablation study on the bidirectional flow fusion module*

## 方法谱系与知识库定位

### 1. 与基线工作的关系

U²Flow 的核心架构继承自 **RAFT**（Teed and Deng, ECCV 2020），保留了其全对相关体积构建与基于 GRU 的循环更新机制。在此基础上，方法沿两条技术路线进行改造：无监督训练稳定性与不确定性感知的流精炼。

在无监督训练方面，U²Flow 直接采纳了 **SMURF**（Stone et al., CVPR 2021）以实例归一化替代批归一化的策略以增强无监督训练的稳定性，并集成了 **ARFlow**（Liu et al., CVPR 2020）的数据增强正则化流损失。此外，方法借鉴了 **UnSAMFlow**（Yuan et al., CVPR 2024）的语义增强与基于区域平滑的损失函数设计，将其纳入总损失框架。与这些工作不同，U²Flow 的核心增量在于首次将不确定性估计解耦引入循环更新过程，并利用不确定性信号对所有损失项和精炼模块进行动态调制。

在无监督光流性能对比中，U²Flow 直接对标 **UPFlow**（Luo et al., CVPR 2021）。在 KITTI-2015 基准上，U²Flow 的 Fl-all 达到 6.13%，显著优于 UPFlow 的 9.38%（Δ = −3.25%）。这一差距的核心驱动力并非架构的根本性变革，而是不确定性引导的自适应精炼与损失调制机制——消融实验表明，仅添加不确定性头而无解耦训练策略，反而会导致性能下降，印证了“如何集成不确定性”比“是否估计不确定性”更为关键。

### 2. 适用边界与关键假设

U²Flow 的性能优势建立在若干隐含假设之上，理解这些假设是判断其适用性的前提：

**（1）数据增强范围的完备性假设。** 不确定性监督信号完全来源于预定义数据增强下的预测不一致性（Laplace 似然 MLE 损失）。这意味着模型只能学习到增强变换所覆盖的误差模式。对于超出增强范围的现实扰动——如严重的非高斯运动模糊、极端光照变化或大气畸变——不确定性估计的可靠性缺乏理论保证。这一局限在交叉数据集泛化实验中可能被部分暴露，但原文未对此类分布外场景进行专项测试。

**（2）平面刚体运动假设（同应性平滑损失）。** 同应性平滑损失 $\ell_{\mathrm{hg}}$ 假设场景运动可由单应性矩阵近似描述，这在 KITTI（以车载刚性运动为主）上带来了显著提升，但在 Sintel（包含复杂非刚性运动）上反而略微损害性能。消融实验明确指出，在 Sintel 上应禁用该损失。这一发现揭示了方法的场景依赖性：当运动模式偏离平面刚体假设时，不确定性增强的同应性损失会错误地惩罚正确的非刚性流，反而引入噪声。

**（3）双向流一致性假设。** 不确定性引导的双向融合模块依赖前向/后向流的一致性来生成融合掩码。在遮挡边界或纹理稀疏区域，双向流本身可能同时不可靠，此时融合掩码的可靠性依赖于不确定性估计的准确度，形成循环依赖。

### 3. 局限与开放问题

**已确认的局限：**

- **场景通用性受限。** 同应性平滑损失仅在刚体运动主导的场景（KITTI）有效，在 Sintel 等复杂场景下反而降低性能，限制了方法作为通用无监督光流框架的适用范围。
- **不确定性监督的覆盖盲区。** 依赖预定义数据增强的自监督信号无法完全覆盖真实世界的非高斯误差源，在分布外场景下不确定性估计可能欠佳。
- **计算效率未系统评估。** 方法在 RAFT 基础上增加了不确定性估计头、精炼模块和双向融合后处理，但原文未报告推理延迟或参数量对比，其计算开销与精度增益的权衡尚不明确。

**开放问题：**

- **更全面的不确定性建模。** 当前 Laplace 似然假设误差服从拉普拉斯分布，未来需探索能够捕获更复杂误差结构（如异方差、多模态）的不确定性建模方式，以覆盖运动模糊、大气畸变等非高斯误差源。
- **向多帧与高分辨率的扩展。** 不确定性引导的融合模块已展示了利用多帧信息的潜力，但如何将联合估计框架系统性地扩展到多帧光流和更高分辨率，同时保持计算效率，仍是一个开放问题。
- **跨任务泛化能力。** 当前不确定性引导的组件——特征缩放、损失调制、融合掩码——是否可泛化到其他密集预测任务（如立体匹配、场景流），值得进一步验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/U_2Flow_Uncertainty_Aware_Unsupervised_Optical_Flow_Estimation.pdf]]
