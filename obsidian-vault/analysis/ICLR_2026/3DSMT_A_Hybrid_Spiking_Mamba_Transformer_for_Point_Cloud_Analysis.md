---
title: "3DSMT: A Hybrid Spiking Mamba-Transformer for Point Cloud Analysis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/3DSMT_A_Hybrid_Spiking_Mamba_Transformer_for_Point_Cloud_Analysis.pdf
aliases:
- 3HSMT
- 3HSMTPCA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/classification_and_understanding
core_operator: "在SNN框架内引入混合架构：使用Spiking Local Offset Attention（SLOA）进行局部几何特征提取，同时使用Spiking Mamba Block（SMB）进行线性复杂度的全局特征融合。"
primary_logic: "通过将脉冲神经网络的稀疏事件驱动特性与Mamba的线性复杂度全局建模能力以及Transformer的局部注意力机制相结合，可以在保持极低能耗的同时，显著提升SNN在点云分析任务上的精度，达到甚至超越多数ANN方法。"
claims:
- "3DSMT在ModelNet40上达到95.2% OA（带投票），在ScanObjectNN三个变体上分别达到92.0%、92.1%、90.6% OA，均为SNN方法中的最优结果。"
- "3DSMT的FLOPs仅为1.3 G，能耗为4.3 mJ，远低于所有ANN对比方法（如PointNeXt 16.6 mJ, PTv2 78.7 mJ）。"
- "在ShapeNetPart部件分割任务上，3DSMT达到85.1% Ins.mIoU，为SNN方法最高。"
- "消融实验表明，混合架构（SLOA + SMB）相比单独使用SLOA或SMB，在ModelNet40上OA提升超过2个百分点。"
---

# 3DSMT: A Hybrid Spiking Mamba-Transformer for Point Cloud Analysis

> [!tip] 核心洞察
> 通过将脉冲神经网络的稀疏事件驱动特性与Mamba的线性复杂度全局建模能力以及Transformer的局部注意力机制相结合，可以在保持极低能耗的同时，显著提升SNN在点云分析任务上的精度，达到甚至超越多数ANN方法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 3DSMT：一种用于点云分析的混合脉冲曼巴-Transformer模型 |
| 英文题名 | 3DSMT: A Hybrid Spiking Mamba-Transformer for Point Cloud Analysis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KkoS6y0pHP); [GitHub](https://github.com/zzm666-ui/3DSMT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/classification_and_understanding |
| Method | 3DSMT (Hybrid Spiking Mamba-Transformer) |
| Dataset | ModelNet40, ScanObjectNN PB_T50_RS, ScanObjectNN OBJ_BG, ScanObjectNN OBJ_ONLY |

> [!tip] 效果简介
> - ModelNet40 上，OA (%) 为 95.2，对比 92.3 (SPM)，变化 +2.9。
> - ScanObjectNN PB_T50_RS 上，OA (%) 为 92.0，对比 84.2 (SPM)，变化 +7.8。
> - ScanObjectNN OBJ_BG 上，OA (%) 为 92.1，对比 90.2 (SPM)，变化 +1.9。

## 概述

3DSMT（Hybrid Spiking Mamba-Transformer）针对现有基于人工神经网络（ANN）的点云分析方法计算复杂度高（O(N²)）、能耗大，以及脉冲神经网络（SNN）方法精度与ANN差距显著、缺乏有效局部-全局特征融合机制的核心瓶颈，提出了一种混合脉冲架构。其核心思路是将脉冲神经网络的稀疏事件驱动特性与Mamba的线性复杂度全局建模能力、Transformer的局部注意力机制相结合：通过Spiking Local Offset Attention（SLOA）进行细粒度局部几何特征提取，利用Spiking Mamba Block（SMB）实现线性复杂度的全局特征融合。

该方法在多个基准上取得了SNN方法的最优结果：在ModelNet40上达到95.2% OA（带投票），在ScanObjectNN的三个变体上分别达到92.0%、92.1%、90.6% OA，在ShapeNetPart部件分割上达到85.1% Ins.mIoU。同时，3DSMT的推理能耗仅为4.3 mJ，远低于PointNeXt（16.6 mJ）和PTv2（78.7 mJ）等ANN方法。消融实验验证了混合架构的有效性：单独使用SLOA或SMB时OA分别为92.5%和92.8%，而两者结合可提升至94.7%。该工作的主要局限在于：与最优ANN方法（如PTv3）仍有精度差距（如SemanticKITTI Test mIoU: 71.3% vs 75.5%），且首个卷积层和最终全连接层仍需MAC操作，无法完全在纯脉冲硬件上运行。

## 背景与动机

点云分析是3D视觉的核心任务，其根本瓶颈在于：现有基于人工神经网络（ANN）的方法（如Point Transformer、PointMamba）虽然精度高，但计算复杂度高（Transformer自注意力为O(N²)），能耗大，难以部署在资源受限的边缘设备上。另一方面，现有的脉冲神经网络（SNN）点云方法虽然继承了SNN的稀疏事件驱动特性和极低能耗优势，但其精度与ANN方法差距显著，且缺乏有效的局部-全局特征融合机制。

现有方法的因果瓶颈在于：SNN点云模型的设计大多直接移植ANN的架构，未能充分利用SNN的脉冲计算特性来设计高效的局部几何特征提取和全局上下文融合模块。具体表现为：局部特征提取依赖标准MLP或全局自注意力，前者缺乏细粒度几何结构感知，后者计算复杂度过高；全局特征融合则缺乏线性复杂度的替代方案。

本文的核心洞察是：将SNN的稀疏事件驱动特性与Mamba的线性复杂度全局建模能力、以及Transformer的局部注意力机制有机结合，可以在保持极低能耗的同时，显著提升SNN在点云分析任务上的精度，达到甚至超越多数ANN方法。具体而言，论文提出了3DSMT（Hybrid Spiking Mamba-Transformer），其关键设计包括：（1）**Spiking Local Offset Attention (SLOA)**：通过脉冲序列实现局部K近邻注意力（O(N×K²)，K为常数），避免softmax和MAC运算，以事件驱动方式捕获细粒度局部几何特征；（2）**Spiking Mamba Block (SMB)**：基于双向状态空间模型（SSM），以线性复杂度O(N)实现全局特征融合，并使用非因果Conv1D消除时序伪影；（3）**Spiking Position Encoding (SPE)**：通过交替堆叠SN层和MLP层，实现脉冲形式的时空特征编码。整个模型使用Integrate-and-Fire (IF)神经元直接训练（代理梯度），避免ANN-SNN转换的额外时间开销。

消融实验（Table 7）验证了混合架构的必要性：在ModelNet40上，单独使用SLOA的OA为92.5%，单独使用SMB为92.8%，而混合架构（SLOA + SMB）达到94.7%，提升超过2个百分点。这一结果直接证明了局部注意力与全局Mamba在SNN框架下的互补性。

## 核心创新

3DSMT的核心创新在于**在SNN框架内首次引入混合架构**，通过替换标准Transformer自注意力和ANN激活函数两个关键槽位，解决了现有SNN点云方法精度低、缺乏有效局部-全局特征融合机制的根本瓶颈。

**关键槽位变更：**

1.  **局部特征提取模块**：从标准Transformer自注意力（复杂度O(N²)）或PointNet++的MLP，替换为**Spiking Local Offset Attention (SLOA)**。SLOA利用K-Norm和K-Pool进行局部特征传播与聚合（K为常数，复杂度O(N×K²)），通过脉冲序列实现逻辑AND和累加操作替代softmax和MAC运算，从而在保持稀疏事件驱动特性的同时捕获细粒度局部几何结构。消融实验（Table 7）证实，SLOA的引入使ModelNet40 OA从92.8%（仅SMB）提升至94.7%（混合架构），提升超过2个百分点。

2.  **全局特征融合模块**：从标准Transformer自注意力（O(N²)），替换为**Spiking Mamba Block (SMB)**。SMB基于双向状态空间模型（SSM），核心复杂度为O(N)，通过非因果Conv1D消除时序伪影，并利用动态脉冲门控机制进行特征选择。这使得全局建模从二次复杂度降为线性，同时保持低能耗。Table 7显示，SMB单独使用时ModelNet40 OA为92.8%，与SLOA组合后达到94.7%。

3.  **位置编码**：从标准正弦/可学习连续位置编码，替换为**Spiking Position Encoding (SPE)**。SPE通过交替堆叠SN层和MLP层，生成脉冲形式的时空特征编码，与整个脉冲计算流兼容。

4.  **神经元类型与训练方式**：从ANN的连续激活函数（如ReLU）或部分SNN的ANN-SNN转换，统一使用**Integrate-and-Fire (IF)神经元**进行直接训练（代理梯度）。Table 13显示，IF神经元在ModelNet40上OA为94.7%，优于LIF神经元的94.2%，且避免了ANN-SNN转换的额外时间开销。

**核心洞察与因果机制**：3DSMT的精度提升来源于**脉冲稀疏计算与混合架构的协同**。SLOA通过局部K近邻注意力以脉冲形式提取几何细节（避免全局softmax的MAC开销），SMB则利用SSM的线性复杂度进行全局上下文融合。两者通过残差连接和LayerNorm整合在Spiking Hybrid Block中。这种设计使得SNN在ModelNet40上达到95.2% OA（带投票），在ScanObjectNN三个变体上分别达到92.0%、92.1%、90.6% OA，均为SNN方法中的最优结果（Table 1）。同时，能耗仅为4.3 mJ，远低于所有ANN对比方法（如PointNeXt 16.6 mJ, PTv2 78.7 mJ）。**精度-能耗帕累托前沿的突破**是3DSMT的核心贡献：它首次证明SNN点云方法可以在精度上超越多数ANN基线（如PointNet++、Point Transformer），同时保持数量级的能效优势。

## 整体框架

![[assets/figures/papers/iclr26_0001_KkoS6y0pHP_3DSMT_A_Hybrid_Spiking_Mamba-Transformer_for_Poi/figures/001_Figure_1.jpg]]
*Figure 1: 3DSMT overview. The model comprises a Spiking Patch Embedding (SPE) module, a sequence of Spiking Hybrid Blocks (SHBs), and a task-specific head. The output of the (i-1)-th SHB serves as the input to the i-th SHB. (a) The SPE module first maps low-dimensional point coordinates into a high-dimensional feature space, which serves as the input to the first SHB. (b) Each SHB integrates a Spiking Local Offset Attention (SLOA) block, a Spiking Mamba Block (SMB), and a Spiking Position Encoding (SPE) module to capture local and global features*

3DSMT的整体架构遵循“局部-全局”混合脉冲处理范式，其核心设计动机是：在保持SNN低能耗优势的同时，通过线性复杂度全局建模弥补纯局部SNN方法在点云分析上的精度损失。架构由三个主要阶段组成：Spiking Patch Embedding (SPE)、多层Spiking Hybrid Block (SHB)堆叠、以及任务特定的预测头（分类或分割头）。

**输入-输出流**：原始点云（N×3坐标）首先进入SPE模块。SPE通过最远点采样（FPS）和K近邻（KNN）将点云组织为L个局部patch，每个patch包含k个点。随后，SPE通过交替的MLP和脉冲神经元（SN）层将低维坐标映射到高维脉冲特征空间。其核心操作如公式(1-3)所示：先由MLP和SN层提取初步语义信息U，再通过MaxPool聚合局部上下文G，最后将U与G拼接后经MLP和SN层输出U'。该过程同时完成了维度提升和脉冲化，为后续SHB提供脉冲形式的token序列。

**SHB模块**是3DSMT的核心计算单元。每个SHB内部集成了三个子模块：Spiking Local Offset Attention (SLOA)、Spiking Mamba Block (SMB)和Spiking Position Encoding (SPE)。SHB的输入如公式(4)所示：由[CLS]令牌与L个patch特征拼接后加上位置编码S_pos构成。每个SHB层按序执行两个步骤（公式5-6）：首先应用SLOA（含残差连接和LayerNorm），然后应用SMB（同样含残差连接和LayerNorm）。第i个SHB的输出直接作为第i+1个SHB的输入，形成深度级联。模型默认堆叠12个SHB（Table 15消融显示12层达到最佳OA 94.7%）。

**SLOA模块**负责局部几何特征提取。其设计规避了标准Transformer的全局自注意力（O(N²)），转而采用K近邻局部注意力。SLOA首先通过K-Norm和K-Pool进行局部特征传播与聚合，然后计算脉冲形式的Q、K、V注意力矩阵（A = Q·Kᵀ·V），并通过逻辑AND和累加操作实现，避免了softmax和MAC运算。最终输出S₃通过计算注意力特征与输入特征的偏移量（S₂ - SN(A)）并经MLP和SN处理后与输入残差相加得到。

**SMB模块**负责全局特征融合。它基于双向状态空间模型（SSM），实现了O(N)线性复杂度的全局建模。SMB包含SSM分支和Gate分支，通过非因果Conv1D消除时序伪影，并采用动态脉冲门控机制进行特征选择。输入特征Z首先经SN层转换为二进制脉冲序列Z₁，最终输出经SN层和线性层得到Z₃。

**位置编码（SPE）**：通过交替堆叠SN层和MLP层，以脉冲形式编码点云的空间结构信息。该编码在每个SHB层内被加入（如公式5中的O^{i-1} + S_pos），确保位置信息在深度网络中持续传递。

**预测头**：分类任务中，堆叠线性层将[CLS]令牌映射到类别预测；分割任务中，结合第4、8、12层SHB的输出特征进行逐点部件概率输出。

**能耗模型**：3DSMT的总能耗由两部分组成——首个卷积层和全连接层的MAC操作能耗（E_MAC × (FLOPs_Conv¹ + FLOPs_FC)），以及所有脉冲层的AC操作能耗（E_AC × ΣSOPsˡ）。其中SOPsˡ = f_r × T × FLOPs(l)，即脉冲发放率、时间步长和该层FLOPs的乘积。这种设计使得大部分计算通过稀疏脉冲的AC操作完成，显著降低了能耗。据Table 1和Table 18数据，3DSMT的FLOPs为1.3 G，能耗为4.3 mJ，而去除脉冲的版本FLOPs为7.9 G，能耗为36.3 mJ，验证了脉冲架构的效率优势。

**与基线的对比**：3DSMT对比了多种基线方法，包括ANN基线（PointNet++、Point Transformer、PointMamba）和SNN基线（Spike PointNet、SPT、SPM）。核心改进在于将标准Transformer的O(N²)全局注意力替换为SLOA的局部注意力（O(N×K²)，K为常数）和SMB的全局SSM（O(N)），在保持线性复杂度的同时实现了局部-全局特征的有效融合。

## 核心模块与公式推导

3DSMT的核心架构围绕**Spiking Hybrid Block (SHB)** 展开，通过交替使用局部和全局特征提取模块，在脉冲神经网络框架下实现高效的点云分析。其关键设计包括：Spiking Patch Embedding (SPE) 用于将原始点云转换为脉冲令牌序列；Spiking Local Offset Attention (SLOA) 用于捕获细粒度局部几何结构；Spiking Mamba Block (SMB) 用于以线性复杂度融合全局上下文；以及 Spiking Position Encoding (SPE) 提供脉冲形式的位置信息。

**Spiking Patch Embedding (SPE)** 模块首先通过最远点采样 (FPS) 和 K近邻 (KNN) 构建局部patch。对于每个patch，SPE通过交替的MLP和脉冲神经元 (SN) 层提取深层语义信息，并利用MaxPool聚合局部上下文，增强令牌表示的判别力。其过程可形式化为：
$$U = \mathbf{MLP}(\operatorname{SN}(\mathbf{MLP}(E))), \quad G = \mathbf{MaxPool}(U), \quad U^{\prime} = \mathbf{MLP}(\operatorname{SN}(\operatorname{Concat}(U, G)))$$
其中，$E$ 为输入patch特征，$U$ 为初步学习的深层语义，$G$ 为局部上下文，$U'$ 为最终输出的patch令牌。

**Spiking Hybrid Block (SHB)** 的初始输入为：
$$\mathcal{O}^{0} = [X_{cls}; F_p(x_p^1); \cdots; F_p(x_p^L)] + S_{pos}$$
其中，$X_{cls}$ 为可学习的[CLS]令牌，$F_p(x_p^i)$ 为第 $i$ 个patch的特征，$S_{pos}$ 为脉冲位置编码。每个SHB层依次应用SLOA和SMB，并包含残差连接和层归一化 (LayerNorm)：
$$O^{i^{\prime}} = \mathrm{SLOA}(\mathrm{LN}(O^{i-1} + S_{pos})) + O^{i-1}, \quad O^{i} = \mathbf{SMB}(\mathbf{LN}(O^{i^{\prime}})) + O^{i^{\prime}}$$

**Spiking Local Offset Attention (SLOA)** 模块是局部特征提取的核心。它首先通过K-Norm和K-Pool对每个令牌的K近邻进行特征传播与聚合，然后计算脉冲形式的偏移注意力。注意力计算利用脉冲Q、K、V的二进制特性，通过逻辑AND和累加操作实现，避免了标准Transformer中的softmax和浮点乘法-累加 (MAC) 运算：
$$A = Q \cdot K^{T} \cdot V$$
SLOA的输出通过计算注意力特征与输入特征的偏移量来增强局部几何表示：
$$S_{3} = \mathbf{MLP}(\mathbf{SN}(S_{2} - \mathbf{SN}(A))) + S_{2}$$
其中，$S_2$ 为经过K-Norm和K-Pool后的特征。SLOA通过三层严格对称的操作设计（K-Norm、K-Pool、偏移注意力）确保置换不变性。

**Spiking Mamba Block (SMB)** 负责线性复杂度的全局特征融合。它由一个SSM分支和一个脉冲门控 (Gate) 分支组成。输入特征 $Z$ 首先通过脉冲神经元层转换为二进制脉冲序列：
$$Z_{1} = \mathbf{SN}(Z)$$
随后，SSM分支通过双向非因果Conv1D对脉冲序列进行建模，消除时序伪影，实现线性复杂度 $O(N)$。脉冲门控分支动态选择重要特征。SMB的最终输出为：
$$Z_{3} = \mathbf{Lin}(\mathbf{SN}(Z_{2}))$$
其中，$Z_2$ 为经SSM和门控融合后的特征，$\mathbf{Lin}$ 为线性层。

**Spiking Position Encoding (SPE)** 模块通过交替堆叠SN层和MLP层，为序列提供脉冲形式的空间位置编码。其输入为点坐标 $p = (x, y, z) \in \mathbb{R}^3$，输出为与令牌特征同维度的脉冲编码 $S_{pos}$。

**脉冲神经元模型**：3DSMT采用Integrate-and-Fire (IF) 神经元。其膜电位更新、脉冲触发和重置机制如下：
$$u_t = V_{t-1} + I_t, \quad S_t = \Theta(u_t - V_{th}), \quad V_t = u_t (1 - S_t) + V_{reset} S_t$$
其中，$V_{t-1}$ 为上一时刻膜电位，$I_t$ 为输入电流，$V_{th}$ 为阈值，$\Theta(\cdot)$ 为阶跃函数，$S_t$ 为脉冲输出。当膜电位超过阈值时发放脉冲，随后膜电位重置。训练采用代理梯度 (surrogate gradient) 方法进行直接训练，避免ANN-SNN转换。

**能耗计算**：3DSMT的能耗由两部分组成：首个卷积层和全连接层的MAC操作能耗，以及所有脉冲层的累加 (AC) 操作能耗。脉冲层的突触操作数 (SOPs) 计算为：
$$\mathrm{SOPs}^{l} = f_{r} \times T \times \mathrm{FLOPs}(l)$$
其中，$f_r$ 为脉冲发放率，$T$ 为时间步长，$\mathrm{FLOPs}(l)$ 为第 $l$ 层的浮点操作数。总能耗为：
$$E_{\mathrm{3DSMT}} = E_{\mathrm{MAC}} \times (\mathrm{FLOPs}_{\mathrm{Conv}}^{1} + \mathrm{FLOPs}_{\mathrm{FC}}) + E_{\mathrm{AC}} \times \left(\sum_{l=1}^{L} \mathrm{SOPs}^{l}\right)$$
其中，$E_{\mathrm{MAC}} = 4.6 \text{ pJ}$，$E_{\mathrm{AC}} = 0.9 \text{ pJ}$。这种设计使得3DSMT在保持高精度的同时，能耗远低于所有ANN对比方法（如PointNeXt 16.6 mJ, PTv2 78.7 mJ）。

## 实验与分析

### 主要分类与分割结果

3DSMT在多个点云分析基准上取得了SNN方法中的最优结果。

**形状分类。** 在ModelNet40数据集上，3DSMT不使用投票策略时达到94.7% OA，使用投票策略后进一步提升至95.2% OA（Table 1）。这一结果显著优于现有的SNN方法，如SPM（92.3% OA）和SPT（91.9% OA），且与主流ANN方法（如PointNeXt 94.0% OA）相比也具有竞争力。在更具挑战性的ScanObjectNN数据集上，3DSMT在三个变体（OBJ_BG、OBJ_ONLY、PB_T50_RS）上分别达到92.1%、90.6%和92.0% OA（Table 1），均为SNN方法中的最高值。值得注意的是，在PB_T50_RS变体上，3DSMT相比SPM（84.2% OA）提升了7.8个百分点，表明混合架构在处理真实世界噪声点云时具有显著优势。

![[assets/figures/papers/iclr26_0001_KkoS6y0pHP_3DSMT_A_Hybrid_Spiking_Mamba-Transformer_for_Poi/figures/002_Table_1.jpg]]
*Table 1: Classification results on ModelNet40 and ScanObjectNN. ‘-’ denotes that the model did not provide results, The units of OA, Energy and FLOPs are percentage (%), millijoule (mJ) and Gigabyte (G), respectively. ‘w/o vot’ denotes the method without voting strategy, while ‘w vot’ indicates testing with voting strategy applied. Among the SNN-based methods, the best results are presented in bold, and the second-best results are underlined*

**小样本分类。** 在ModelNet40的小样本分类任务中（Table 2），3DSMT在5-way 10-shot和5-way 20-shot设置下分别达到92.8%和96.2% OA，在10-way 10-shot和10-way 20-shot设置下分别达到87.2%和92.1% OA。这些结果证明了模型在数据稀缺条件下的泛化能力。

![[assets/figures/papers/iclr26_0001_KkoS6y0pHP_3DSMT_A_Hybrid_Spiking_Mamba-Transformer_for_Poi/figures/003_Table_2.jpg]]
*Table 2: Few-shot Classification results on ModelNet40*

**部件分割。** 在ShapeNetPart数据集上（Table 3），3DSMT达到85.1% Ins.mIoU和82.7% Cat.mIoU，为SNN方法中的最高结果。可视化结果（Figure 4, Figure 7）显示预测与真实标注高度一致。

![[assets/figures/papers/iclr26_0001_KkoS6y0pHP_3DSMT_A_Hybrid_Spiking_Mamba-Transformer_for_Poi/figures/004_Table_3.jpg]]
*Table 3: The Part Segmentation results on ShapeNetPart*

**室内/室外场景分割。** 在S3DIS数据集Area 5上（Table 4），3DSMT达到70.2% mIoU。在SemanticKITTI数据集上（Table 5），3DSMT达到68.1% Val mIoU和71.3% Test mIoU，优于E-3DSNN（63.2% Val mIoU, 69.4% Test mIoU）。但与最优ANN方法PTv3（75.5% Test mIoU）相比仍存在差距。

![[assets/figures/papers/iclr26_0001_KkoS6y0pHP_3DSMT_A_Hybrid_Spiking_Mamba-Transformer_for_Poi/figures/005_Table_4.jpg]]
*Table 4: Semantic Segmentation Results on S3DIS Dataset. The unit of energy consumption is mJ*

![[assets/figures/papers/iclr26_0001_KkoS6y0pHP_3DSMT_A_Hybrid_Spiking_Mamba-Transformer_for_Poi/figures/006_Table_5.jpg]]
*Table 5: Scene Segmentation on Semantic KITTI. We compare our SNN-based methods 3DSMT with ANN-based methods and SNN-based methods on SemanticKITTI Behley et al. (2019), with the metric being mIoU (Val/Test). As shown in the table5, 3DSMT outperforms E-3DSNN among SNN, achieving 68.1% (Val mIoU) and 71.3% (Test mIoU), which are 4.9 and 1.9 percentage points higher respectively. While ANN method PTv3 reaches the highest Test mIoU (75.5%), 3DSMT as a point cloud SNN shows competitive performance. Table 5: Scene segmentation results on Semantic KITTI Dataset*

### 能耗与效率分析

3DSMT的核心优势在于极低的计算能耗。在ModelNet40上（Table 1），3DSMT的FLOPs仅为1.3 G，能耗为4.3 mJ，远低于所有ANN对比方法（如PointNeXt 16.6 mJ, PTv2 78.7 mJ）。这一优势来源于脉冲神经网络的稀疏事件驱动特性：脉冲层仅需累加（AC）操作（0.9 pJ），而非脉冲层的乘积累加（MAC）操作（4.6 pJ）。消融实验（Table 18）进一步证实了脉冲架构的效率优势：3DSMT（脉冲版本）在ModelNet40上OA为94.7%，FLOPs为1.3 G，能耗为4.3 mJ；而去除脉冲的ANN版本OA为94.9%（仅提升0.2个百分点），但FLOPs激增至7.9 G，能耗增至36.3 mJ（提升约8.4倍）。

在延迟和内存方面（Table 6），3DSMT的训练延迟为298ms，训练内存为10.1G，推理延迟为142ms，推理内存为4.6G，均为对比方法中最低。

### 消融实验与架构分析

**混合架构有效性。** 消融实验（Table 7）验证了混合架构设计的必要性。在ModelNet40上，单独使用SLOA（无全局融合）的OA为92.5%，单独使用SMB（无局部注意力）的OA为92.8%，而完整混合架构（SLOA + SMB）的OA为94.7%，提升超过2个百分点。在ScanObjectNN三个变体上，完整架构同样一致优于单独模块。

**SLOA关键参数。** SLOA中的K近邻数量（Table 8）和Token数量L（Table 9）对性能有直接影响。K=4时在ModelNet40上达到最佳OA 94.7%和mAcc 91.8%；Token数量L=128时达到最佳性能。这反映了局部感受野大小和序列长度之间的权衡。

**双向SSM策略。** 双向SSM策略（L-SSM + C-SSM）（Table 11）在ModelNet40上OA为94.7%，优于单向策略，表明双向建模对点云全局特征融合至关重要。

**SNN超参数。** 最佳SNN超参数为TimeStep=3, Threshold=1.0（Figure 2）。IF神经元（Table 13）在ModelNet40上OA为94.7%，优于LIF神经元的94.2%，说明简单的IF模型在此架构中已足够有效。TS数据增强（Table 12）在ModelNet40上OA为94.7%，优于R数据增强的94.2%。

**模型深度。** 12个SHB堆叠（Table 15）在ModelNet40上达到最高OA 94.7%，继续增加层数不再带来收益。

### 线性复杂度验证

3DSMT的线性复杂度来源于两个关键设计（I CLAIM OF LINEAR COMPLEXITY FOR 3DSMT）：（1）SLOA使用局部K近邻注意力，复杂度为O(N×K²)，其中K为常数（实验中K=4），避免了标准Transformer的O(N²)全局自注意力；（2）SMB基于SSM核心，复杂度为O(N)。实际测量结果（Table 1）显示3DSMT的FLOPs仅为1.3 G，远低于PTv2的67.9 G，验证了线性复杂度的实际效果。

### 特征可视化与失效模式

t-SNE可视化（Figure 6）显示，3DSMT在不同数据集上学到的特征分布存在差异：ModelNet40上特征点分布较为扩散且存在部分类间重叠，而ScanObjectNN的OBJ_BG和OBJ_ONLY变体上特征聚类更清晰、类间边界更明确。这一差异与分类性能一致：模型在ScanObjectNN上相对SPM的提升更大（+7.8%在PB_T50_RS上），说明混合架构对噪声数据的特征判别能力增强更显著。

脉冲发放率可视化（Figure 3）显示，SLOA中的Q、K、V以及SMB中的M_init、M_end均保持适中的脉冲发放率，表明模型在稀疏计算和特征表达能力之间取得了平衡。

### 局限性

当前SNN方法在点云分析上的精度与最优ANN方法（如PTv3）仍存在一定差距（例如SemanticKITTI Test mIoU: 3DSMT 71.3% vs PTv3 75.5%）。此外，3DSMT的首个卷积层和最终全连接层仍需MAC操作，无法完全在纯脉冲硬件上高效运行。目前尚无结合激光扫描与事件驱动机制从源头生成3D点云脉冲的方法，限制了3DSMT在纯神经形态硬件上的端到端部署。模型在目标检测和场景理解等更复杂的点云任务上的性能尚未验证。

## 方法谱系与知识库定位

### 基线方法与核心改进

3DSMT定位于脉冲神经网络（SNN）框架下的点云分析，其核心动机是解决现有方法在计算效率与精度之间的权衡困境。该方法的直接基线可分为两个谱系：一是基于ANN的点云分析方法，包括PointNet++（基于MLP）、Point Transformer（基于Transformer自注意力，复杂度$O(N^2)$）和PointMamba（基于Mamba的状态空间模型，复杂度$O(N)$）；二是已有的SNN点云方法，包括Spike PointNet、SPT（SNN-Transformer混合）和SPM（Spike Mamba基线）。

3DSMT的核心因果机制在于**在SNN框架内引入混合架构**，替换了两个关键模块：局部特征提取从标准Transformer自注意力（$O(N^2)$，含softmax和MAC运算）替换为**Spiking Local Offset Attention (SLOA)**，通过K-Norm和K-Pool进行局部K近邻注意力（复杂度$O(N \times K^2)$，$K$为常数），利用脉冲序列的逻辑AND和累加操作替代MAC运算；全局特征融合从标准Transformer自注意力替换为**Spiking Mamba Block (SMB)**，基于双向状态空间模型（SSM）实现$O(N)$复杂度，并使用非因果Conv1D消除时序伪影和动态脉冲门控机制。此外，位置编码从连续值的正弦/可学习编码替换为**Spiking Position Encoding (SPE)**，通过交替堆叠SN层和MLP层实现脉冲形式的时空特征编码；神经元类型统一使用Integrate-and-Fire (IF)神经元并通过代理梯度直接训练，避免了ANN-SNN转换的额外时间开销。

### 适用边界与条件

3DSMT的线性复杂度优势依赖于两个关键设计约束：SLOA的局部性（$K=4$为最优值，Token数量$L=128$为最优配置）和SMB的SSM核心。当点云规模增大时，SLOA的$O(N \times K^2)$和SMB的$O(N)$复杂度使得模型在理论上可扩展（消融实验Table 16验证了点云规模对性能的影响）。模型在12个SHB堆叠时达到最优精度（ModelNet40 OA 94.7%），表明深度增加仍有收益但边际递减。

在数据特性方面，3DSMT在干净合成数据（ModelNet40 OA 95.2%带投票）和真实扫描数据（ScanObjectNN PB_T50_RS OA 92.0%）上均表现优异，但在更具挑战性的真实场景（SemanticKITTI Test mIoU 71.3%）中与最优ANN方法（PTv3 75.5%）仍有差距。小样本学习实验（Table 2）表明模型在数据稀缺场景下具有竞争力（5-way 10-shot OA 92.8%）。

### 局限与开放问题

**精度-效率权衡的剩余缺口**：当前SNN点云方法的精度与最优ANN方法（如PTv3）在复杂场景分割任务上仍存在显著差距（SemanticKITTI Test mIoU: 71.3% vs 75.5%）。消融实验（Table 18）显示，去除脉冲架构后OA提升至94.9%（vs 94.7%），但FLOPs从1.3G激增至7.9G，能耗从4.3mJ升至36.3mJ——这揭示了当前SNN在精度上仍存在的微小幅损失，但换来了约8.4倍的能耗降低。

**混合架构的硬件部署瓶颈**：3DSMT的首个卷积层和最终全连接层仍需MAC操作，无法完全在纯脉冲硬件上高效运行。此外，目前尚无结合激光扫描与事件驱动机制从源头生成3D点云脉冲的方法，限制了模型在纯神经形态硬件上的端到端部署。在神经形态硬件上设计处理3D点云的RC电路需要额外的工程努力。

**任务覆盖的局限性**：模型在目标检测和场景理解等更复杂的点云任务上的性能尚未验证。消融实验也仅对比了IF和LIF两种神经元类型，其他脉冲神经元模型（如AdEx）的影响未知。模型扩展到更大规模点云或更高分辨率时的行为也需进一步研究。

**证据强度评估**：上述局限和开放问题均直接来源于论文的limitations和open questions部分（置信度1.0），但精度差距的具体数值（PTv3 75.5%）需要手动验证是否来自同一实验设置。能耗比较基于标准假设（MAC 4.6 pJ, AC 0.9 pJ，参考Horowitz 2014），该假设在SNN领域被广泛采用但存在简化。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/3DSMT_A_Hybrid_Spiking_Mamba_Transformer_for_Point_Cloud_Analysis.pdf

![[paperPDFs/ICLR_2026/3DSMT_A_Hybrid_Spiking_Mamba_Transformer_for_Point_Cloud_Analysis.pdf]]
