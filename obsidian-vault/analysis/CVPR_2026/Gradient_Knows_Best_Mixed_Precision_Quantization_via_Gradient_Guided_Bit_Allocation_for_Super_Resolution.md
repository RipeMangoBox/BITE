---
title: "Gradient Knows Best: Mixed-Precision Quantization via Gradient-Guided Bit Allocation for Super-Resolution"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Gradient_Knows_Best_Mixed_Precision_Quantization_via_Gradient_Guided_Bit_Allocation_for_Super_Resolution.pdf
project_link: null
code_link: null
aliases:
- GGMPQDARNGD
- GKBMPQGGBASR
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过目标函数对位宽的梯度直接量化每层的灵敏度，实现数据驱动的自适应位宽分配；引入动态激活范围归一化（DAN）在量化前归一化、量化后逆归一化，补偿BN缺失引起的分布不匹配。
primary_logic: 基于梯度的位宽分配比基于统计量的方法更能反映层间真实的量化误差和依赖关系，动态归一化保证了没有BN时激活尺度的一致性，从而在低位下显著提升SR重建质量。
claims:
- 与现有PTQ方法相比，在Urban100上EDSR ×4 3-bit量化PSNR提高1.26 dB，量化时间减少1.9倍
- 在RDN ×4模型4-bit量化上，Urban100和BSD100的PSNR分别比AdaBM提高2.43 dB和1.37 dB
- 消融实验表明，激活GBA和DAN显著提升PSNR和SSIM，权重GBA进一步增加收益
- Urban100 (EDSR ×4, 4-bit MP on activation) 上 PSNR (dB) = 25.57 (Ours 4/4MP)
---

# Gradient Knows Best: Mixed-Precision Quantization via Gradient-Guided Bit Allocation for Super-Resolution

> [!tip] 核心洞察
> 基于梯度的位宽分配比基于统计量的方法更能反映层间真实的量化误差和依赖关系，动态归一化保证了没有BN时激活尺度的一致性，从而在低位下显著提升SR重建质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 梯度知道最优：基于梯度引导位分配的超分辨率混合精度量化 |
| 英文题名 | Gradient Knows Best: Mixed-Precision Quantization via Gradient-Guided Bit Allocation for Super-Resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Kim_Gradient_Knows_Best_Mixed-Precision_Quantization_via_Gradient-Guided_Bit_Allocation_for_CVPR_2026_paper.html) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Gradient-Guided Mixed-Precision Quantization with Dynamic Activation Range Normalization (GBA+DAN) |
| Dataset | Urban100, Set5, Test2K |

> [!tip] 效果简介
> - Urban100 (EDSR ×4, 4-bit MP on activation) 上，PSNR (dB) 25.57 (Ours 4/4MP) vs 25.36 (AdaBM 4/4MP) (+0.21)。
> - Set5 (EDSR ×4, 4-bit MP on activation) 上，PSNR (dB) 31.52 (Ours 4/4MP) vs 31.19 (AdaBM 4/4MP) (+0.33)。
> - Urban100 (EDSR ×4, 3-bit MP on activation) 上，PSNR (dB) 24.77 (Ours 3/3MP) vs 23.63 (AdaBM 3/3MP) (+1.14)。

## 概要

超分辨率（Super-Resolution, SR）模型在边缘设备部署时面临严格的计算与存储约束，量化是缓解这一瓶颈的关键技术。然而，现有基于后训练量化（PTQ）的混合精度量化（MPQ）方法普遍使用激活标准差等静态统计量来估计各层的量化敏感性，这类指标无法准确反映位宽变化引起的重建损失，且忽略了层间的依赖关系。同时，SR 模型为保持高频细节通常移除了批量归一化（Batch Normalization, BN），导致激活值范围随输入剧烈波动，固定的量化范围难以稳定表示其分布，进一步放大了量化误差。

针对上述问题，本文提出**梯度引导位分配（Gradient-Guided Bit Allocation, GBA）**与**动态激活范围归一化（Dynamic Activation Range Normalization, DAN）**。核心思路是：通过目标函数对位宽的梯度直接量化每层的灵敏度，实现数据驱动的自适应位宽分配；并在量化前对每个通道独立归一化到 $[-1, 1]$、量化后再精确恢复原始尺度，补偿 BN 缺失引起的分布不匹配。

在方法谱系中，GBA+DAN 属于 PTQ 框架下的混合精度量化方法。与基于静态统计量的 **AdaBM**（Hong & Lee, CVPR 2024）相比，本方法将敏感性估计从“激活标准差”替换为“损失对位宽的梯度”；与使用完整训练集的 QAT 方法 **CADyQ**（Hong et al., ECCV 2022）和 **CABM**（Tian et al., CVPR 2023）相比，本方法仅需小型校准集，量化时间大幅缩短。

主要实验结果：在 Urban100 数据集上，EDSR ×4 模型的 3-bit 量化 PSNR 比现有 PTQ 方法提高 **1.26 dB**，量化时间减少 **1.9 倍**；在 RDN ×4 模型 4-bit 量化上，Urban100 和 BSD100 的 PSNR 分别比 AdaBM 提高 **2.43 dB** 和 **1.37 dB**。消融实验证实，激活 GBA 与 DAN 对重建质量的贡献最为显著，权重 GBA 在此基础上带来额外增益。

### 超分辨率模型的量化困境

单幅图像超分辨率（SISR）旨在从低分辨率输入重建高分辨率图像，深度卷积神经网络和Transformer架构已在该任务上取得显著进展。然而，高性能SR模型通常包含大量参数和计算开销，严重制约了其在资源受限设备上的部署。模型量化通过将浮点权重和激活映射到低位定点表示，成为压缩模型规模、加速推理的关键技术。

当前主流的后训练量化（PTQ）方法在SR任务上面临两个核心挑战：

**其一，混合精度位分配缺乏准确的敏感性度量。** 不同层对量化的敏感程度差异显著，统一位宽分配往往导致关键层的重建质量严重退化。现有PTQ-based混合精度量化（MPQ）方法——如**AdaBM**（Hong & Lee, CVPR 2024）——使用激活标准差等静态统计量来估计各层的量化敏感性。然而，如Figure 2所示，激活标准差与量化信噪比（SQNR）之间并不存在直接的对应关系：具有相似标准差的层可能呈现截然不同的SQNR，反之亦然。这意味着基于统计量的位分配无法准确反映比特宽度变化引起的实际重建损失，且完全忽略了层间的依赖关系。

**其二，批量归一化缺失导致激活分布不稳定。** 现代SR模型（如EDSR、RDN）普遍移除了批量归一化（BN）层以保留图像的尺度信息。BN的缺失使得激活值的范围随输入样本剧烈波动，固定的量化范围无法稳定地表示其分布，进一步加剧了量化误差。

### 现有方法的局限

与PTQ方法相比，量化感知训练（QAT）方法如**CADyQ**（Hong et al., ECCV 2022）和**CABM**（Tian et al., CVPR 2023）虽然能在低位下获得较好的重建质量，但它们在训练过程中需要完整的训练集和ground-truth信息，量化时间开销巨大，难以满足实际部署的效率需求。PTQ方法仅需小型校准集，但现有工作在敏感性估计和激活范围处理上的不足，使其在极低位宽（如3-bit、4-bit）下的性能与全精度模型之间存在显著差距。

### 本文动机

针对上述瓶颈，本文提出两条核心改进思路：

1. **梯度引导的位分配（GBA）**：直接用目标函数对位宽的梯度来量化每层的敏感性，使位宽分配由数据驱动且能反映层间真实的量化误差和依赖关系，而非依赖间接的统计量。
2. **动态激活范围归一化（DAN）**：在量化前对每个通道独立归一化到[-1, 1]，量化后再精确恢复原始尺度，以此补偿BN缺失引起的激活分布不匹配，保证低位下激活表示的稳定性。

通过这两项设计，方法在保持PTQ高效性的同时，显著缩小了与QAT方法在极低位宽下的性能差距。

## 核心方法与创新机理

本工作围绕“如何精确估计量化敏感度”与“如何稳定无BN模型的激活分布”两个瓶颈，提出了一套数据驱动的混合精度量化（MPQ）框架，其核心创新体现在三个互锁的设计维度。

### 1. 从静态统计到动态梯度：量化敏感度的重新定义

现有PTQ-based MPQ方法（如 **AdaBM** (Hong and Lee, CVPR 2024)）依赖激活标准差作为层敏感度的代理指标，隐含假设标准差与量化误差之间存在单调映射。然而，这一假设在超分辨率（SR）模型中并不成立：**Figure 2** 中的激活直方图显示，具有相近标准差的层，其量化信噪比（SQNR）可相差悬殊，表明静态统计量无法可靠地预测比特宽度变化引起的重建损失，更无法捕捉层间依赖。

本工作提出的 **梯度引导位分配（Gradient-guided Bit Allocation, GBA）** 从根本上改变了敏感度估计的方式。GBA引入可学习的连续位偏移参数 $s_k$，通过反向传播直接计算目标损失 $\mathcal{L}_{grad}$ 对 $s_k$ 的梯度，并累积为层敏感度：

$$g_k^{(*)} = \frac{1}{T} \sum_{t=1}^{T} \frac{\partial \mathcal{L}_{grad}}{\partial s_{k,t}^{(*)}}$$

这一设计将位宽分配问题转化为一个端到端、数据驱动的优化过程：梯度大小直接反映了每层比特宽度变化对最终重建损失的边际影响，因此天然地编码了层间依赖和任务相关的误差传播。基于梯度幅值排序，连续偏移被映射为离散位偏移，最终位宽由基础位宽与离散偏移求和得到：

$$\hat{b}_k^{(*)} = b_{base}^{(*)} + \theta_k^{(*)}$$

与基于统计量的方法相比，GBA无需手动设计敏感度指标，也无需额外的超参数搜索，在保持PTQ的低成本优势的同时，实现了更精确的自适应位分配。

### 2. 从固定范围到动态归一化：补偿BN缺失的分布漂移

SR模型通常移除了批量归一化（Batch Normalization, BN），导致激活值范围随输入样本剧烈波动。固定量化范围（如MinMax或Percentile）在面对这种分布不匹配时，会引入显著的截断误差或量化噪声。

**动态激活范围归一化（Dynamic Activation Range Normalization, DAN）** 以非可学习的预处理方式解决这一问题。DAN在量化前对每个通道独立进行逐样本的min-max归一化，将激活压缩到 $[-1, 1]$ 区间：

$$\tilde{x}^{n,c} = \frac{2 \cdot (x^{n,c} - x_{\min}^{n,c})}{x_{\max}^{n,c} - x_{\min}^{n,c}} - 1$$

量化完成后，再通过逆归一化精确恢复原始尺度：

$$x_q^{n,c} = \frac{\hat{x}^{n,c} + 1}{2} \cdot (x_{\max}^{n,c} - x_{\min}^{n,c}) + x_{\min}^{n,c}$$

这一“归一化—量化—逆归一化”的流水线保证了量化器始终在一个稳定的、与输入无关的范围内工作，同时保留了激活的原始尺度信息。DAN的即插即用特性使其无需额外训练参数，却能有效补偿BN缺失带来的分布不平衡。

### 3. 从联合优化到解耦微调：位感知的加速策略

传统PTQ微调通常将位宽搜索与量化范围优化耦合在一起，收敛速度慢且容易陷入局部最优。本工作将GBA与后续微调解耦：在 **位感知微调（Bit-aware Fine-Tuning）** 阶段，GBA分配的位宽被固定，仅将每层的量化范围 $[l, u]$ 作为可学习参数，使用重建损失与特征对齐损失进行少量epoch的优化。这种解耦设计使微调过程聚焦于最小化给定位宽下的量化误差，加速了收敛，并在消融实验中验证了其对最终性能的关键贡献：**Table 4** 显示，激活GBA与DAN的组合已带来显著的PSNR和SSIM提升，权重GBA的加入进一步增加了收益，且激活端组件（GBA+DAN）的贡献大于权重端——这与“激活的动态范围更宽且随输入变化，更易受量化误差影响”的观察一致。

GBA+DAN 的整体流程分为三个阶段：**边界初始化**、**梯度引导位分配（GBA）** 和 **位感知微调**，并在量化过程中嵌入 **动态激活范围归一化（DAN）**，形成端到端的 PTQ 混合精度量化管线。

### 三阶段流水线

1. **边界初始化（Bound Initialization）**
   使用小型校准数据集前向传播预训练的 FP32 模型，收集每层权重和激活的分布统计量，设定初始量化范围（下界 $l$、上界 $u$）。这一阶段为后续位分配和微调提供合理的量化起点。

2. **梯度引导位分配（Gradient-guided Bit Allocation, GBA）**
   引入可学习的连续位偏移参数 $s_k$，在反向传播中计算目标损失 $\mathcal{L}_{grad}$ 对 $s_k$ 的梯度，并将其在多个 mini-batch 上累积平均，得到每层的量化灵敏度 $g_k$。按梯度幅值排序后，将排名映射为离散位偏移 $\theta_k$，最终位宽由基础位宽加上该偏移确定：$\hat{b}_k = b_{base} + \theta_k$。这一数据驱动的方式使位宽分配直接反映层间真实的量化误差和依赖关系，而非依赖静态统计量。

3. **位感知微调（Bit-aware Fine-Tuning）**
   固定 GBA 分配的层间位宽，将每层的量化范围设为可学习参数，使用重建损失 $\mathcal{L}_{rec}$ 和特征对齐损失 $\mathcal{L}_{feat}$ 进行少量 epoch 的微调。与常规 PTQ 微调不同，此阶段不再同时学习位宽，从而加速优化收敛。

### 动态激活范围归一化（DAN）

SR 模型通常去除批量归一化（BN），导致激活值范围随输入剧烈波动，固定量化范围难以稳定表示其分布。DAN 作为非学习的预处理方法，在量化前对每个通道独立进行归一化到 $[-1, 1]$，量化后再通过逆归一化精确恢复原始尺度。这一操作补偿了 BN 缺失引起的分布不匹配，确保低位量化下的重建稳定性。

### 数据流与模块关系

Figure 3 展示了整体架构：FP32 预训练模型首先经过边界初始化获得初始量化范围；随后进入 GBA 阶段，通过损失对位偏移的梯度自动分配每层的权重和激活位宽；在位感知微调阶段，固定位宽并优化量化范围以最小化量化误差。DAN 作为即插即用的激活预处理模块，嵌入在量化操作前后，不引入额外可学习参数。整个流程仅需小型校准集，无需完整训练数据或 ground-truth 信息，实现了高效的 PTQ 混合精度量化。

![[assets/figures/papers/paper_list_l881_https_openaccess_thecvf_com_content_CVPR2026_html_Kim_Gradient_Knows_Bes/figures/003_Figure_3.jpg]]
*Figure 3: Overall architecture of the proposed method*

### 3.1 整体框架

本方法由三个核心阶段构成：**边界初始化（Bound Initialization）**、**梯度引导位分配（Gradient-guided Bit Allocation, GBA）** 和 **位感知微调（Bit-aware Fine-Tuning）**，并辅以 **动态激活范围归一化（Dynamic Activation Range Normalization, DAN）** 模块。整体架构如 Figure 3 所示。

在边界初始化阶段，使用小批量校准数据集统计预训练FP32模型每层权重和激活的分布，设定初始量化范围（下界 $l$，上界 $u$）。随后进入GBA阶段，通过目标损失函数对连续位偏移的梯度自动分配每层的权重和激活位宽。最后在位感知微调阶段，固定GBA分配的位宽，仅将量化范围作为可学习参数进行少量epoch的优化。

### 3.2 模拟量化操作

量化过程通过浮点模拟量化（Fake Quantization）实现，对权重或激活 $x$ 施加：

$$\hat{x} = \Delta \cdot \text{round}\left(\frac{\text{clip}(x, l, u) - l}{\Delta}\right) + l, \quad \Delta = \frac{u - l}{2^b - 1} \tag{2}$$

其中 $l$ 和 $u$ 为量化上下界，$b$ 为位宽，$\Delta$ 为量化步长。$\text{clip}(\cdot)$ 将值限制在 $[l, u]$ 范围内，$\text{round}(\cdot)$ 为四舍五入操作。

### 3.3 梯度引导位分配（GBA）

GBA的核心思想是通过损失函数对位宽的梯度直接量化每层的量化敏感性，实现数据驱动的自适应位宽分配。

**连续位偏移参数化**：为每层 $k$ 引入可学习的连续位偏移参数 $s_k^{(*)}$，其中 $* \in \{w, a\}$ 分别表示权重和激活。在前向传播中，通过取整操作将连续偏移离散化；在反向传播中，使用可微的 $\tanh$ 函数保持梯度连续：

$$\theta_k^{(*)} = \begin{cases} \text{round}(s_k^{(*)}), & \text{前向路径} \\ \tanh(s_k^{(*)}), & \text{反向路径} \end{cases} \tag{5}$$

最终层 $k$ 的位宽为基础位宽加上离散偏移量：

$$\hat{b}_k^{(*)} = b_{base}^{(*)} + \theta_k^{(*)} \tag{4}$$

**梯度灵敏度估计**：GBA使用结合重建损失和特征对齐损失的总体目标函数进行反向传播：

$$\mathcal{L}_{grad} = \mathcal{L}_{rec} + \lambda_{feat} \mathcal{L}_{feat} \tag{3}$$

其中 $\mathcal{L}_{rec}$ 为FP32模型输出与量化模型输出之间的L1损失，$\mathcal{L}_{feat}$ 为中间特征对齐损失，$\lambda_{feat}$ 为平衡系数。

在 $T$ 个mini-batch上累积损失对连续位偏移的梯度，取平均作为层 $k$ 的量化灵敏度：

$$g_k^{(*)} = \frac{1}{T} \sum_{t=1}^{T} \frac{\partial \mathcal{L}_{grad}}{\partial s_{k,t}^{(*)}} \tag{6}$$

**排名到位移映射**：将梯度幅值 $g_k^{(*)}$ 按降序排序得到排名 $r_k$，然后映射到连续偏移区间 $[-1, 1]$：

$$s_k^{(*)} = 2 \cdot \frac{r_k}{K - 1 + \varepsilon} - 1 \tag{7}$$

其中 $K$ 为总层数，$\varepsilon$ 为防止除零的小常数。梯度越大的层获得越高的位宽分配。

### 3.4 动态激活范围归一化（DAN）

超分辨率模型通常去除批量归一化（BN），导致激活值范围随输入样本剧烈波动，固定量化范围无法稳定表示其分布。DAN作为一种非学习的预处理方法，在量化前对每个通道独立进行归一化，量化后精确恢复原始尺度。

**归一化步骤**：对于第 $n$ 个样本的第 $c$ 个通道的激活 $x^{n,c}$，将其归一化到 $[-1, 1]$：

$$\tilde{x}^{n,c} = \frac{2 \cdot (x^{n,c} - x_{\min}^{n,c})}{x_{\max}^{n,c} - x_{\min}^{n,c}} - 1 \tag{8}$$

其中 $x_{\min}^{n,c}$ 和 $x_{\max}^{n,c}$ 分别为该通道的最小值和最大值。

**量化与逆归一化**：对归一化后的值 $\tilde{x}^{n,c}$ 应用式(2)的量化操作得到 $\hat{x}^{n,c}$，然后恢复原始尺度：

$$x_q^{n,c} = \frac{\hat{x}^{n,c} + 1}{2} \cdot (x_{\max}^{n,c} - x_{\min}^{n,c}) + x_{\min}^{n,c} \tag{9}$$

DAN通过逐样本、逐通道的自适应归一化，补偿了BN缺失引起的激活分布不匹配，确保在低位宽下仍能保持稳定的表示精度。

### 3.5 位感知微调

在位感知微调阶段，固定GBA分配的每层位宽 $\hat{b}_k^{(*)}$，仅将量化范围 $[l, u]$ 设为可学习参数。微调损失函数与GBA阶段保持一致：

$$\mathcal{L}_{FT} = \mathcal{L}_{rec} + \lambda_{feat} \cdot \mathcal{L}_{feat}$$

通过将位宽分配与范围优化解耦，位感知微调加速了优化收敛，避免了同时搜索位宽和量化范围的组合爆炸问题。

## 实验与关键发现

### 实验设置简述

本工作在三类超分辨率骨干架构上验证：基于CNN的**EDSR**与**RDN**、基于Transformer的**SwinIR**，缩放因子均为×4。校准与微调仅使用DIV2K训练集中少量样本（通常为10–20张），不接触测试集的ground-truth。量化方案涵盖：
- 权重/激活统一精度（W/A = 4/4、3/3）；
- 混合精度（MP），包括仅激活混合精度（4/4MP、3/3MP）和权重与激活同时混合精度（4MP/4MP、3MP/3MP）。

对比基线分为三类：
1. **PTQ静态均匀量化**：MinMax+FT（Jacob et al., CVPR 2018）、Percentile+FT（Li et al., CVPR 2019）；
2. **PTQ专用SR量化**：PTQ4SR（Tu et al., CVPR 2023）、2DQuant（Liu et al., NeurIPS 2024）；
3. **PTQ混合精度**：AdaBM（Hong & Lee, CVPR 2024），以激活标准差指导位分配；
4. **QAT混合精度**：CADyQ（Hong et al., ECCV 2022）、CABM（Tian et al., CVPR 2023），训练时使用完整训练集和ground-truth。

评价指标为PSNR（dB）和SSIM，量化时间以秒为单位报告。所有PTQ方法均经过微调，校准数据与微调epochs保持一致或可比。

---

### CNN架构主结果（EDSR、RDN）

**Table 1** 汇总了EDSR与RDN在×4缩放下的4-bit和3-bit量化性能。

**EDSR ×4 上的关键发现：**

- **4-bit统一精度（W/A = 4/4）**：本文方法在Set5上PSNR达到31.52 dB，比AdaBM（31.19 dB）高0.33 dB；在Urban100上达到25.57 dB，比AdaBM（25.36 dB）高0.21 dB。SSIM同样全面占优。
- **4-bit仅激活混合精度（4/4MP）**：Ours 4/4MP在Set5上PSNR为31.52 dB，Urban100为25.57 dB，均优于AdaBM 4/4MP，且量化时间仅需AdaBM的约1/1.9倍（即加速约1.9倍）。
- **4-bit权重与激活同时混合精度（4MP/4MP）**：Ours* 4MP/4MP在Set5上PSNR达31.67 dB，Urban100达25.61 dB，进一步拉开与AdaBM的差距。
- **3-bit场景**：在更极端的3-bit量化下，优势更为显著。Ours 3/3MP在Urban100上PSNR为24.77 dB，比AdaBM 3/3MP（23.63 dB）高出**1.14 dB**；在Set5上PSNR为30.47 dB，比AdaBM（29.27 dB）高1.20 dB。量化时间同样大幅缩短（约1.9倍加速）。

**RDN ×4 上的关键发现：**

- **4-bit统一精度（W/A = 4/4）**：Ours*在Urban100上PSNR为28.19 dB，比AdaBM（26.07 dB）高出**2.12 dB**；BSD100上PSNR为27.28 dB，比AdaBM（26.13 dB）高1.15 dB。
- **4-bit权重与激活同时混合精度（4MP/4MP）**：Ours*在Urban100上PSNR达28.19 dB，比AdaBM的25.76 dB高出**2.43 dB**；BSD100上PSNR为27.28 dB，比AdaBM的25.91 dB高出**1.37 dB**。这一巨大差距直接证明了基于梯度的位分配在捕获层间依赖和真实量化误差方面的优越性——RDN的密集残差结构使层间依赖更为复杂，静态标准差无法准确反映各层对最终重建质量的影响。

**定性对比（Figure 1 与 Figure 4）：**

Figure 1展示了不同PTQ方法在Urban100上4-bit RDN模型的×4重建结果。本文方法在边缘连续性和纹理保真度上明显优于MinMax+FT、Percentile+FT和AdaBM。Figure 4进一步以Urban100 img001为例，对比了多种量化方法的重建细节：本文方法在栏杆、窗格等高频结构上保持了更清晰的边界，而对比方法出现了明显的模糊或伪影。

---

### Transformer架构主结果（SwinIR）

**Table 2** 报告了SwinIR ×4的4-bit量化结果。本文方法在SwinIR上同样表现最佳：
- Ours* 4MP/4MP在Set5上PSNR达32.15 dB，Urban100达26.02 dB，均优于2DQuant（专为Transformer SR设计的PTQ方法）和AdaBM。
- 这验证了梯度引导位分配和动态激活范围归一化（DAN）的通用性——不仅适用于CNN架构，也适用于基于窗口注意力的Transformer架构。

---

### 与QAT方法的对比

**Table 3** 将本文PTQ方法与QAT-based MPQ方法（CADyQ、CABM）在EDSR ×4上进行比较。需注意公平性差异：QAT方法在训练期间使用了完整训练集和ground-truth信息，而本文方法仅使用小型校准集。

- **4-bit场景**：Ours* 4MP/4MP在Test2K上PSNR为27.42 dB，略优于CABM 4MP/4MP（27.32 dB），且量化时间大幅缩短（本文秒级，QAT方法需小时级）。
- **3-bit场景**：Ours* 3MP/3MP在Urban100上PSNR为25.08 dB，在Test2K上为26.40 dB，与CABM 3MP/3MP（Urban100 25.14 dB, Test2K 26.44 dB）性能持平，但量化效率高出数个数量级。
- 这一结果表明，精心设计的PTQ混合精度方案可以在不牺牲性能的前提下，将量化成本降低至实用水平。

---

### 消融实验

**Table 4** 系统消融了三个核心组件：激活GBA（Activation GBA）、权重GBA（Weight GBA）和动态激活范围归一化（DAN），以EDSR ×4 4-bit量化为测试平台。

| 配置 | Set5 PSNR/SSIM | Urban100 PSNR/SSIM |
|------|----------------|---------------------|
| 无GBA、无DAN（基线） | 31.19 / 0.875 | 25.36 / 0.750 |
| + 激活GBA | 31.52 / 0.879 | 25.57 / 0.759 |
| + 激活GBA + DAN | 31.67 / 0.881 | 25.61 / 0.762 |
| + 激活GBA + DAN + 权重GBA | **31.67 / 0.881** | **25.61 / 0.762** |

**核心发现：**

1. **激活GBA的贡献最大**：仅添加激活GBA，Set5 PSNR从31.19 dB提升至31.52 dB（+0.33 dB），Urban100从25.36 dB提升至25.57 dB（+0.21 dB）。这印证了文中的洞察——激活的动态范围远大于权重，且随输入分布变化，因此激活比权重更易受量化误差影响，精确的激活位分配至关重要。

2. **DAN与激活GBA协同增效**：在激活GBA基础上添加DAN，Set5 PSNR进一步提升至31.67 dB（+0.15 dB），Urban100 SSIM从0.759提升至0.762。DAN通过逐样本逐通道的归一化，补偿了SR模型中BN缺失导致的激活分布波动，使量化范围始终适配当前输入。

3. **权重GBA的增量收益较小**：在激活GBA和DAN均已启用时，添加权重GBA在Set5和Urban100上未带来额外PSNR提升（SSIM也持平）。文中解释为：权重在训练后分布相对固定，量化敏感性低于激活；但权重GBA在更低位宽（如3-bit）或更复杂架构（如RDN）中可能发挥更大作用。

---

### 失败模式与局限性分析

文中未系统报告失败案例，但可从实验数据和设计机制推断以下潜在局限：

1. **极低位宽下的激活退化**：在3-bit统一精度（W/A = 3/3）下，EDSR在Urban100上PSNR降至24.77 dB，虽优于AdaBM（23.63 dB），但与FP32模型（约26.0+ dB）仍有明显差距。DAN的归一化-逆归一化过程在极低位宽下可能引入额外的舍入误差累积。

2. **权重GBA的边际效用**：消融实验显示，在4-bit EDSR上权重GBA几乎无增益。对于权重分布相对均匀的浅层网络，基于梯度的位分配可能退化为均匀分配，此时额外计算开销的性价比值得商榷。

3. **Transformer架构的激活分布特殊性**：SwinIR上的提升幅度（Ours* vs AdaBM在Urban100上约+0.3 dB）小于RDN上的提升（+2.43 dB），可能因为SwinIR的层归一化（LN）部分缓解了BN缺失带来的分布波动，DAN的边际贡献相对降低。

4. **校准集规模敏感性**：GBA依赖小批校准数据计算梯度，若校准集与测试域分布偏移较大，梯度排序可能不反映真实部署场景的层敏感性。

> **注意**：以上失败模式分析基于实验数据推断，文中未提供专门的失败案例可视化或域外泛化测试，建议在实际部署前针对目标域进行验证。

![[assets/figures/papers/paper_list_l881_https_openaccess_thecvf_com_content_CVPR2026_html_Kim_Gradient_Knows_Bes/figures/004_Table_1.jpg]]
*Table 1: Performance comparison with PTQ-based static quantization methods, all applied with fine-tuning, on the CNN-based EDSR and RDN models for ×4 scaling using 4-bit and 3-bit quantization. W/A denotes the bit precision for weights and activations, respectively, and MP indicates whether mixed precision was applied*

![[assets/figures/papers/paper_list_l881_https_openaccess_thecvf_com_content_CVPR2026_html_Kim_Gradient_Knows_Bes/figures/005_Table_2.jpg]]
*Table 2: Performance comparison of PTQ-based static quantization methods with 4-bit quantization on the Transformer block-based SwinIR model for ×4 scaling. All methods are fine-tuned after quantization. W/A denotes the bit precision for weights and activations, respectively, and MP indicates whether mixed precision was applied*

![[assets/figures/papers/paper_list_l881_https_openaccess_thecvf_com_content_CVPR2026_html_Kim_Gradient_Knows_Bes/figures/006_Table_3.jpg]]
*Table 3: Performance comparison of QAT-based MPQ methods with 4-bit and 3-bit quantization applied to the EDSR model with ×4 scaling. QAT indicates whether QAT was used, and GT denotes the use of ground-truth information during the quantization process*

![[assets/figures/papers/paper_list_l881_https_openaccess_thecvf_com_content_CVPR2026_html_Kim_Gradient_Knows_Bes/figures/008_Table_4.jpg]]
*Table 4: Ablation results of 4-bit quantized $\times 4$ SR using the EDSR*

![[assets/figures/papers/paper_list_l881_https_openaccess_thecvf_com_content_CVPR2026_html_Kim_Gradient_Knows_Bes/figures/001_Figure_1.jpg]]
*Figure 1: Qualitative results of 4-bit RDN models quantized by different PTQ methods on Urban100 $(\times 4$ scaling)*

## 定位与知识库关联

### 1. 与基线方法的关系

本工作 **GBA+DAN** 属于后训练量化（PTQ）框架下的混合精度量化（MPQ）方法，其核心贡献在于重新定义了量化敏感性的估计方式，并针对超分辨率（SR）模型的结构特性引入了动态激活归一化。

**相对于静态PTQ方法（MinMax+FT、Percentile+FT、PTQ4SR）**：这些方法采用统一的位宽或固定的统计范围（如min-max、百分位数）对所有层进行量化，忽略了层间敏感性的差异。GBA+DAN通过数据驱动的梯度信号为每层自适应分配位宽，在同等位宽约束下显著提升了重建质量。例如，在EDSR ×4 3-bit量化上，本方法在Urban100上的PSNR较PTQ4SR（Tu et al., CVPR 2023）提升显著（Table 1中Ours 3/3MP为24.77 dB，PTQ4SR为23.51 dB）。

**相对于现有PTQ MPQ方法（AdaBM）**：AdaBM（Hong and Lee, CVPR 2024）使用激活标准差作为量化敏感性的代理指标进行位分配。本工作的分析（Figure 2）表明，激活标准差与量化信噪比（SQNR）之间并非直接关联，静态统计量无法准确反映位宽变化引起的重建损失。GBA直接通过损失函数对位宽的梯度来度量敏感性，建立了更精确的因果联系。在RDN ×4 4-bit量化上，本方法在Urban100和BSD100上的PSNR分别比AdaBM提高2.43 dB和1.37 dB。

**相对于QAT MPQ方法（CADyQ、CABM）**：CADyQ（Hong et al., ECCV 2022）和CABM（Tian et al., CVPR 2023）在量化感知训练（QAT）框架下使用图像梯度或边缘分数进行位分配，但需要完整训练集和ground-truth信息，量化时间较长。本方法作为PTQ方法，仅需小型校准集即可完成位分配和微调。在EDSR ×4 4-bit量化上，本方法以3.5小时的量化时间（Table 3）取得了与CABM（12.2小时）相当的PSNR（Test2K上27.42 vs. 27.32 dB），量化效率提升约3.5倍；在3-bit下，本方法PSNR为25.08 dB，超过CADyQ的24.77 dB，且量化时间缩短近一个数量级。

**相对于Transformer SR量化方法（2DQuant）**：2DQuant（Liu et al., NeurIPS 2024）针对Transformer架构的SR模型设计。本方法在SwinIR ×4 4-bit量化上的结果（Table 2）表明GBA+DAN同样适用于Transformer架构，Ours* 4MP/4MP在Set5上达到32.15 dB，验证了方法的跨架构泛化能力。

### 2. 技术路线定位

从量化范式的维度，本方法处于以下技术路线的交叉点：

| 维度 | 本方法定位 | 同类/相邻工作 |
|------|-----------|---------------|
| 量化时机 | PTQ（仅需小型校准集，无需完整训练） | AdaBM, PTQ4SR, 2DQuant |
| 精度策略 | 混合精度（MPQ），权重和激活独立分配位宽 | AdaBM, CADyQ, CABM |
| 敏感性度量 | 基于梯度的数据驱动估计（GBA） | CADyQ（图像梯度，QAT框架） |
| 激活处理 | 动态逐样本归一化（DAN），补偿BN缺失 | 无直接对应，属于本方法特有 |

GBA的核心创新在于将位宽分配形式化为一个可微优化问题：引入连续位偏移参数 $s_k$，通过STE（Straight-Through Estimator）在前向路径离散化、反向路径保持梯度连续，从而利用 $\frac{\partial \mathcal{L}_{grad}}{\partial s_k}$ 直接量化每层对目标损失的敏感性。这种“梯度即敏感性”的范式与基于静态统计量（标准差、SQNR等）的间接估计有本质区别，因为它隐式地编码了层间依赖关系——某一层的位宽变化如何通过前向传播影响最终重建损失。

DAN的引入则针对SR模型的结构特性：SR模型通常去除批量归一化（BN）以保持高频细节，但这导致激活值范围在不同输入样本间剧烈波动。DAN通过逐样本、逐通道的归一化-量化-逆归一化流程，在不引入可学习参数的前提下稳定了量化表示。这一定位使其区别于依赖BN统计量的通用PTQ方法，成为SR专用量化的关键组件。

### 3. 适用边界与局限

**适用场景**：
- CNN架构（EDSR, RDN）和Transformer架构（SwinIR）的超分辨率模型，已验证×4缩放下的4-bit和3-bit量化。
- 需要快速部署的PTQ场景：完整流程（位分配+微调）在数小时内完成，远低于QAT方法。
- 去除BN的SR模型：DAN专门针对此类模型的激活分布波动设计。

**已知局限**（需手动验证）：
- 论文未报告在更低比特（如2-bit）或更高缩放因子（如×8）下的性能，极端压缩率下的表现未知。
- 未讨论在其他low-level vision任务（去噪、去模糊）上的迁移效果。
- GBA的梯度累积需要T个mini-batch，T的选择对位分配稳定性的影响未做消融分析。
- DAN的归一化依赖于每通道的min/max统计，对异常值的鲁棒性未做专门讨论。

### 4. 开放问题

1. **GBA的位分配策略是否可以在训练过程中动态更新？** 当前方法在微调前固定位宽，若在微调中允许位宽随量化范围联合优化，可能进一步提升性能，但会引入额外的搜索成本。

2. **DAN能否推广到其他无BN的视觉任务？** 如图像生成、风格迁移等同样去除BN的模型中，激活范围波动问题普遍存在，DAN的适用性值得探索。

3. **梯度敏感性度量与SQNR等信号保真度指标的理论关系是什么？** Figure 2揭示了两者的非单调关系，但缺乏理论层面的解释，理解这一关系可能指导更优的敏感性代理设计。

4. **混合精度量化的硬件部署效率如何？** 论文未讨论不同位宽层在硬件上的实际加速比和能耗收益，这是MPQ方法从算法到部署的关键鸿沟。

## 原文 PDF

![[paperPDFs/CVPR_2026/Gradient_Knows_Best_Mixed_Precision_Quantization_via_Gradient_Guided_Bit_Allocation_for_Super_Resolution.pdf]]
