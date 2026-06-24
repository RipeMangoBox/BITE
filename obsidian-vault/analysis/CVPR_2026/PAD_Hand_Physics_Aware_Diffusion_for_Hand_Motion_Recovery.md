---
title: "PAD-Hand: Physics-Aware Diffusion for Hand Motion Recovery"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PAD_Hand_Physics_Aware_Diffusion_for_Hand_Motion_Recovery.pdf
project_link: null
code_link: null
aliases:
- PAD-Hand
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将欧拉-拉格朗日动力学残差作为虚拟观测量，以概率方式集成到条件扩散模型的目标中。
primary_logic: 利用扩散模型的生成能力，通过虚拟观测变量将物理先验融入轨迹分布，并通过最后一层拉普拉斯近似为每个关节和帧提供可解释的物理一致性方差。
claims:
- 在DexYCB上，PA-MPJPE从4.88 mm降至4.63 mm (5.1%)，ACCEL从6.70降至3.34 mm/frame²（50.1%），表明物理感知精调同时提升精度和物理合理性。
- 动态方差直方图显示高方差区间对应较大的平均欧拉-拉格朗日残差，验证了方差估计与物理违规的一致性。
- 概率物理集成（Ours）在各项指标上优于确定性惩罚变体，且残差R(q)更低。
- 添加欧拉-拉格朗日残差损失显著降低PA-MPJPE、MPJPE和ACCEL。
---

# PAD-Hand: Physics-Aware Diffusion for Hand Motion Recovery

> [!tip] 核心洞察
> 利用扩散模型的生成能力，通过虚拟观测变量将物理先验融入轨迹分布，并通过最后一层拉普拉斯近似为每个关节和帧提供可解释的物理一致性方差。

| 字段 | 内容 |
|------|------|
| 中文题名 | PAD-Hand：物理感知扩散模型用于手部运动恢复 |
| 英文题名 | PAD-Hand: Physics-Aware Diffusion for Hand Motion Recovery |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.26068) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PAD-Hand |
| Dataset | DexYCB, HO3D |

> [!tip] 效果简介
> - DexYCB 上，PA-MPJPE (mm) 4.63 vs 4.88 (WiLoR) (-0.25 (5.1%))；MPJPE (mm) 10.56 vs 12.75 (WiLoR) (-2.19 (17.2%))；ACCEL (mm/frame^2) 3.34 vs 6.70 (WiLoR) (-3.36 (50.1%))。
> - HO3D 上，PA-MPJPE (mm) 7.43 vs 7.50 (WiLoR) (-0.07 (0.9%))；ACCEL (mm/frame^2) 2.71 vs 4.98 (WiLoR) (-2.27 (45.6%))。

## 概述

从单目图像或视频中恢复三维手部运动是构建自然交互系统的关键步骤。现有方法——无论是逐帧图像姿态估计器（如 **WiLoR**、**HaMeR**、**HandOccNet**），还是引入时序建模的视频方法（如 **VIBE**、**TCMR**、**Deformer**）——都难以保证输出运动在物理上的合理性。一个根本瓶颈在于：这些方法无法量化物理一致性，而确定性物理约束（如直接惩罚动力学残差）会强制将残差归零，忽略了估计本身的不确定性以及模型误差的存在。

**PAD-Hand** 针对这一瓶颈提出了一个概率物理感知框架。其核心思路是：将手部运动的欧拉-拉格朗日（Euler-Lagrange, EL）动力学残差视为“虚拟观测量”，以概率方式集成到条件扩散模型的训练目标中，而非作为硬约束。这一设计使得模型既能利用扩散模型的生成能力来融合物理先验，又能通过最后一层拉普拉斯近似（Last-Layer Laplace Approximation, LLLA）为每个关节和每一帧输出可解释的物理一致性方差。

在方法谱系上，PAD-Hand 位于“扩散模型运动精调”这一新兴范式，区别于 **DIP** 等纯数据驱动的扩散精调方法。其关键改动槽位包括：（1）将物理集成方式从无/确定性残差惩罚改为概率虚拟观测；（2）在损失函数中显式加入 EL 残差项 $\mathcal{L}_{EL}$；（3）引入 LLLA 方差预测头与反向扩散方差传播算法，输出关节级和网格级的动态不确定性。

实验表明，PAD-Hand 在 DexYCB 和 HO3D 两个标准数据集上同时提升了重建精度和物理合理性。在 DexYCB 上，相对于图像基线 WiLoR，PA-MPJPE 从 4.88 mm 降至 4.63 mm（5.1%），而衡量运动平滑度的 ACCEL 从 6.70 降至 3.34 mm/frame²（50.1%），说明物理感知精调不仅没有牺牲精度，反而带来了显著增益。消融实验进一步证实：概率物理集成优于确定性惩罚变体，且模型的动态方差高值区间与较大的 EL 残差一致，验证了方差估计确实能够指示物理违规。

## 背景与动机

### 问题背景

从单目图像或视频中恢复三维手部运动是计算机视觉与图形学的核心挑战，在AR/VR、人机交互和机器人遥操作等领域具有广泛应用。手部具有高度关节化、自遮挡严重、运动快速等特点，使得从二维观测推断三维姿态和运动本质上是一个病态问题。

近年来，基于图像的手部姿态估计方法取得了显著进展，代表性工作包括**WiLoR**、**HaMeR**和**HandOccNet**等。这些方法能够从单帧图像中估计出较为准确的手部姿态参数（通常基于MANO参数化模型）。在此基础上，视频运动恢复方法（如**VIBE**、**TCMR**、**Deformer**）通过引入时序建模，进一步提升了运动序列的平滑性和一致性。扩散模型也被引入运动精调任务，例如**DIP**利用扩散过程的生成能力对初始估计进行优化。

### 现有方法的瓶颈

尽管上述方法在运动精度和平滑性上取得了提升，但存在一个根本性缺陷：**现有方法无法量化物理一致性**。

具体而言，当前方法普遍采用确定性物理约束，将运动学或动力学残差强制归零，以此作为优化目标。这种做法隐含了两个不合理的假设：

1. **忽略估计不确定性**：确定性约束假定物理模型是完美无缺的，且观测数据完全可靠。然而，在实际场景中，图像姿态估计器的输出本身包含噪声和不确定性，物理模型（如惯性参数的近似）也存在误差。
2. **忽略模型误差**：将残差强制归零意味着物理模型被视为绝对真理，但手部动力学建模中，惯性参数通常基于统计近似，接触力（如手-物体交互）往往被忽略，这些模型误差在确定性框架下无法被表达和处理。

这一瓶颈导致现有方法在物理合理性方面缺乏保障，也无法为下游任务提供关于估计可靠性的信息。

### 核心动机与解决思路

本文的核心动机是**将物理约束从确定性惩罚转变为概率集成**，使模型能够同时优化运动精度和物理合理性，并提供可解释的不确定性估计。

实现这一目标的因果调控变量是：**将欧拉-拉格朗日动力学残差作为虚拟观测量**。具体而言，本文不要求动力学残差严格为零，而是将其视为从一个分布中抽取的虚拟观测，并将该分布的似然函数集成到条件扩散模型的训练目标中。这一设计使得：

- 模型可以在数据驱动损失和物理一致性损失之间取得自适应平衡；
- 通过最后一层拉普拉斯近似（LLLA），模型能够为每个关节和每一帧输出物理一致性的方差估计；
- 方差信息可以反向传播，指示哪些时刻和关节的运动估计不可靠，为后续决策提供依据。

利用扩散模型的生成能力，PAD-Hand将物理先验以概率方式融入轨迹分布，在提升运动恢复精度的同时，显著改善了物理合理性（如加速度一致性），并首次实现了手部运动恢复中物理一致性的可量化不确定性建模。

## 核心创新

PAD-Hand 的核心创新在于将**手部运动的物理先验以概率方式融入条件扩散模型**，并同步输出**可解释的动态不确定性估计**，从而在提升运动恢复精度的同时量化物理一致性。与现有工作的关键差异体现在以下五个“changed slots”上。

### 物理集成方式：从确定性惩罚到概率虚拟观测

现有方法要么完全忽略物理约束，要么将其作为确定性残差惩罚项直接加入损失函数。这种做法隐含假设模型估计是精确的，强行将残差归零会忽略估计不确定性和模型误差。PAD-Hand 改变了这一范式：**将欧拉-拉格朗日动力学残差视为虚拟观测量**，假定其服从零均值高斯分布，并将该分布的负对数似然集成到扩散模型的训练目标中（Equation 10）。这使得模型不必将残差强制归零，而是学习在物理约束与数据拟合之间取得最优平衡。消融实验证实，概率物理集成在各项指标上均优于确定性惩罚变体，且欧拉-拉格朗日残差 $R(q)$ 更低（Table 4, Table 9）。

### 损失函数：从单一数据损失到数据-物理联合损失

基线扩散模型仅使用数据驱动损失 $\mathcal{L}_{data}$ 监督去噪过程。PAD-Hand 将其扩展为联合损失：

$$\mathcal{L}_{total} = \lambda_1 \mathcal{L}_{data} + \lambda_2 \mathcal{L}_{EL}$$

其中 $\mathcal{L}_{EL}$ 是虚拟观测变量的负对数似然损失（Equation 11）。这一设计的关键在于：$\mathcal{L}_{data}$ 保证运动估计与图像观测的一致性，而 $\mathcal{L}_{EL}$ 注入手部动力学先验，约束运动轨迹的物理合理性。消融实验表明，添加欧拉-拉格朗日残差损失使得 PA-MPJPE、MPJPE 和 ACCEL 均有统计显著改善（Table 3），且数据驱动损失与物理损失联合使用达到最佳性能（Table 5）。

### 不确定性估计：从无到最后一层拉普拉斯近似

现有视频运动恢复方法均为确定性输出，无法量化估计的可靠性。PAD-Hand 引入**最后一层拉普拉斯近似（LLLA）**，在训练完成后对骨干网络的最后一层进行后验推断，为每个关节和每一帧输出独立的预测方差（Section 3.4, Equation 12）。这一方差直接反映了模型对该帧该关节估计的不确定性。定性结果（Figure 1, Figure 4）显示，高方差区域与图像姿态估计器产生剧烈抖动的帧高度吻合，表明方差能够有效指示估计不可靠的位置。

### 方差传播：从单步方差到递归全轨迹方差

LLLA 仅提供单步去噪预测的方差。PAD-Hand 进一步设计了**反向扩散过程中的方差递归传播算法**（Algorithm 1），从纯噪声步骤 $N$ 的狄拉克分布出发，逐步传播方差直至初始步骤 $0$，得到最终运动估计的完整方差 $\mathrm{Var}(x_{1:T}^0)$（Equation 14）。基于此，还可通过雅可比近似推导出动力学残差的方差 $\mathrm{Var}(\mathcal{F}_{1:T})$（Equation 17），从而量化物理违规的程度。动态方差直方图分析（Figure 5）验证了高方差区间与较大的平均欧拉-拉格朗日残差一致，表明方差估计与物理违规之间存在强对齐关系。

### 扩散模型输入：从合成噪声到图像姿态估计器预测

传统扩散模型从纯高斯噪声开始去噪生成。PAD-Hand 将**图像姿态估计器（如 WiLoR）的逐帧预测作为扩散模型的输入条件** $y_{1:T}$，并设计前向过程将干净运动逐步偏移至这些初始估计（Section 3.2）。这一设计使得扩散模型的任务从“从零生成”转变为“从粗糙估计精调”，显著降低了学习难度，同时保留了扩散模型的多模态生成能力以修正初始估计中的时序不一致和物理违规。

## 整体框架

PAD-Hand 的整体流程以**单帧图像姿态估计器**为起点，通过**条件扩散模型**对初始运动序列进行精调，并在精调过程中引入**欧拉-拉格朗日动力学残差作为虚拟观测量**，最终输出物理一致的手部运动轨迹及其逐帧、逐关节的**动态方差估计**。

### 输入与预处理

给定一段长度为 $T$ 的图像序列 $\mathcal{T}_{1:T}$，首先由现成的图像姿态估计器（如 **WiLoR**、**HaMeR** 或 **HandOccNet**）逐帧预测 MANO 手部模型的姿态参数 $\theta_{1:T}$ 和形状参数 $\beta_{1:T}$。为消除形状在时序上的不一致性，PAD-Hand 对序列内的形状参数取均值，得到固定的平均形状 $\beta_{avg} = \frac{1}{T} \sum_{i=1}^{T} \beta_i$，后续所有网格重建均基于该固定形状进行。图像姿态估计器的预测值 $y_{1:T}$ 作为条件信号输入扩散模型，构成整个框架的“数据锚点”。

### 条件扩散主干网络

扩散模型的核心是一个基于 **Transformer 编码器-解码器**架构的主干网络 $f_\phi$（Figure 3）。在扩散步 $n$，当前含噪运动序列 $x_{1:T}^n$ 与图像估计 $y_{1:T}$ 分别通过 MANO 层转换为网格，再由 **MeshCNN** 提取空间特征；扩散步 $n$ 则经 MLP 编码为嵌入向量。Transformer 编码器-解码器融合上述特征，输出精调后的干净运动预测 $\hat{x}_{1:T}$。

扩散过程采用**有偏正向转移分布**，将干净运动逐步拉向图像估计值，而非标准高斯噪声。反向过程则通过重参数化均值 $\mu_\phi$ 进行去噪，其形式为 $A_n x_{1:T}^n + B_n f_\phi(x_{1:T}^n, y_{1:T}, n)$，其中 $A_n$ 和 $B_n$ 由噪声调度决定。

### 物理先验的集成方式

PAD-Hand 的关键创新在于**将物理约束从确定性惩罚转化为概率虚拟观测**。具体而言，对每一帧计算欧拉-拉格朗日动力学残差：

$$Z_t = \mathsf{M}_t \ddot{\mathsf{q}}_t + \mathsf{C}_t + \mathsf{g}_t - \hat{\mathcal{F}}_t$$

其中 $\mathsf{M}_t$、$\mathsf{C}_t$、$\mathsf{g}_t$ 分别为广义质量矩阵、科里奥利力项和重力项，$\hat{\mathcal{F}}_t$ 为近似外力。该残差被建模为来自零均值高斯分布的虚拟观测量，其负对数似然构成物理损失 $\mathcal{L}_{EL}$。

总训练目标为数据驱动损失与物理损失的加权和：

$$\mathcal{L}_{total} = \lambda_1 \mathcal{L}_{data} + \lambda_2 \mathcal{L}_{EL}$$

其中 $\mathcal{L}_{data} = \mathbb{E}_{n \sim [1,N]} || x_{1:T} - f_{\phi}(x_{1:T}^n, y_{1:T}, n) ||^2$ 监督主干网络预测干净运动。

### 方差估计与传播

PAD-Hand 通过**最后一层拉普拉斯近似（LLLA）**为预测头赋予贝叶斯性质，输出逐关节、逐帧的预测方差 $\mathrm{Var}(\hat{x}_{1:T})$。在推理阶段，**方差传播算法**（Algorithm 1）从扩散步 $N$ 的狄拉克分布出发，递归传播每一步的方差：

$$\mathrm{Var}(x_{1:T}^{n-1}) = A_n^2 \mathrm{Var}(x_{1:T}^n) + B_n^2 \mathrm{Var}(\hat{x}_{1:T}) + \Sigma_n^2 + 2 A_n B_n \mathrm{Cov}(x_{1:T}^n, \hat{x}_{1:T})$$

最终得到初始运动 $x_{1:T}^0$ 的完整方差估计。此外，通过雅可比矩阵 $J_{\mathcal{F}_{1:T}}$ 可将运动方差近似映射为动力学残差的力方差：

$$\mathrm{Var}(\mathcal{F}_{1:T}) \approx J_{\mathcal{F}_{1:T}} \mathrm{Var}(x_{1:T}^0) J_{\mathcal{F}_{1:T}}^{\top}$$

该方差信息可指示哪些帧或关节的运动估计不可靠，为下游应用提供可解释的不确定性度量。

### 模块间数据流总结

整个 pipeline 的数据流可概括为：图像序列 → 图像姿态估计器 → 初始姿态与平均形状 → 条件扩散主干网络（融合 MeshCNN 空间特征与扩散步嵌入）→ 精调运动预测 + LLLA 方差 → 欧拉-拉格朗日残差计算 → 联合损失反向传播 → 方差传播算法输出最终运动及其不确定性。物理残差模块仅在训练时作为虚拟观测损失参与优化，推理时无需额外计算动力学方程，保持了推理效率。

### 补充图表

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/002_Figure_2.jpg]]
*Figure 2: Overview of PAD-Hand. A sequence of images*

## 核心模块与公式推导

PAD-Hand 围绕“将物理先验以概率方式注入扩散模型”这一核心思想，构建了四个紧密协作的关键模块：欧拉-拉格朗日动力学残差计算、条件扩散主干网络、虚拟观测损失函数、以及基于最后一层拉普拉斯近似（LLLA）的方差估计与传播。

### 欧拉-拉格朗日动力学残差

手部运动被建模为铰接刚体系统，其广义坐标定义为 $\mathsf{q} = \{\mathsf{R}, \mathsf{t}, \theta\}$，分别对应全局旋转、平移和关节角。系统动力学遵循欧拉-拉格朗日方程：

$$\mathsf{M}(\mathsf{q}; \mathsf{m}, \mathsf{I}) \ddot{\mathsf{q}} + \mathsf{C}(\mathsf{q}, \dot{\mathsf{q}}; \mathsf{m}, \mathsf{I}) + \mathsf{g}(\mathsf{q}; \mathsf{m}) = \mathcal{F}$$

其中 $\mathsf{M}$ 为广义质量矩阵，$\mathsf{C}$ 为科里奥利力与离心力项，$\mathsf{g}$ 为重力项，$\mathcal{F}$ 为广义外力。该方程将运动轨迹与物理定律建立了确定性映射。

对于任意给定的运动估计，定义每帧的**动力学残差**为：

$$Z_t = \mathsf{M}_t \ddot{\mathsf{q}}_t + \mathsf{C}_t + \mathsf{g}_t - \hat{\mathcal{F}}_t$$

该残差量化了运动轨迹偏离物理定律的程度。现有方法通常将其作为确定性惩罚项强制归零，但这一做法忽略了估计不确定性和模型误差——当初始姿态估计存在噪声时，硬约束反而可能引入额外偏差。

### 条件扩散主干网络

主干网络采用 Transformer 编码器-解码器架构（4 层编码器、4 层解码器、8 注意力头、嵌入维度 512）。其输入为当前扩散步 $n$ 下的噪声运动 $x_{1:T}^n$ 和图像姿态估计器的预测 $y_{1:T}$。两者分别通过 MeshCNN 提取空间网格特征，扩散步 $n$ 则通过 MLP 编码为嵌入向量。Transformer 融合这些特征后，由 LLLA 头输出精炼后的干净运动 $\hat{x}_{1:T}$ 及其逐关节、逐帧的预测方差。

反向扩散过程中，条件均值由主干网络 $f_\phi$ 参数化：

$$\mu_{\phi}(x_{1:T}^n, y_{1:T}, n) = A_n x_{1:T}^n + B_n f_{\phi}(x_{1:T}^n, y_{1:T}, n)$$

训练时，数据驱动损失为干净运动的重建误差：

$$\mathcal{L}_{data} = \mathbb{E}_{n \sim [1,N]} || x_{1:T} - f_{\phi}(x_{1:T}^n, y_{1:T}, n) ||^2$$

### 虚拟观测损失：物理先验的概率集成

区别于确定性残差惩罚，PAD-Hand 将动力学残差 $Z_{1:T}$ 视为**虚拟观测量**，假设其服从零均值高斯分布。由此构造负对数似然损失：

$$\mathcal{L}_{EL} = \mathbb{E}_{n \sim [1,N]} \frac{1}{2\sigma_n} || Z_{1:T}(x_{1:T}^0) ||^2$$

其中 $\sigma_n$ 为扩散步相关的噪声尺度。最终训练目标为数据损失与物理损失的加权组合：

$$\mathcal{L}_{total} = \lambda_1 \mathcal{L}_{data} + \lambda_2 \mathcal{L}_{EL}$$

这一设计的核心优势在于：扩散模型在生成过程中天然具有去噪能力，概率形式的物理约束允许模型在数据保真度与物理一致性之间自适应权衡，而非强制满足可能不精确的动力学方程。

### 方差估计与传播

推理阶段采用**最后一层拉普拉斯近似（LLLA）** 作为后验推断步骤，将主干网络最后一层线性化以获得预测方差。LLLA 头输出高斯后验预测分布：

$$p(\hat{x}_{1:T} | x_{1:T}^n, n, \mathcal{D}) \approx \mathcal{N}(f_\phi(x_{1:T}^n, y_{1:T}, n), \mathrm{diag}(\gamma_\phi^2(x_{1:T}^n, y_{1:T}, n)))$$

在反向扩散过程中，方差从初始的 Dirac delta 分布开始递归传播：

$$\mathrm{Var}(x_{1:T}^{n-1}) = A_n^2 \mathrm{Var}(x_{1:T}^n) + B_n^2 \mathrm{Var}(\hat{x}_{1:T}) + \Sigma_n^2 + 2 A_n B_n \mathrm{Cov}(x_{1:T}^n, \hat{x}_{1:T})$$

最终获得初始运动 $x_{1:T}^0$ 的逐关节、逐帧方差。进一步，通过雅可比矩阵 $J_{\mathcal{F}_{1:T}}$ 将运动方差传播至动力学残差空间，得到力方差近似：

$$\mathrm{Var}(\mathcal{F}_{1:T}) \approx J_{\mathcal{F}_{1:T}} \mathrm{Var}(x_{1:T}^0) J_{\mathcal{F}_{1:T}}^{\top}$$

该方差估计为每个关节和每帧提供了可解释的物理一致性度量——高方差区域指示模型对运动估计的不确定性较大，通常对应物理违规严重的区域。

### 补充图表

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/003_Figure_3.jpg]]
*Figure 3: Backbone architecture. At diffusion step n, the current pose sequence*

## 实验与分析

### 主实验结果

PAD-Hand 在两个广泛使用的手部姿态基准 DexYCB 和 HO3D 上进行了评估，以 PA-MPJPE、MPJPE 和 ACCEL 作为核心指标，同时评估运动精度和物理合理性。

**DexYCB 数据集。** 如 Table 1 所示，以 WiLoR 作为图像姿态估计器初始化时，PAD-Hand 将 PA-MPJPE 从 4.88 mm 降至 **4.63 mm**（相对提升 5.1%），MPJPE 从 12.75 mm 降至 **10.56 mm**（17.2%），而衡量运动平滑度的 ACCEL 则从 6.70 大幅降至 **3.34 mm/frame²**（50.1%）。这一结果表明，物理感知精调在提升重建精度的同时，显著增强了运动轨迹的物理合理性。与其他视频运动恢复方法（如 VIBE、TCMR、Deformer）及扩散精调方法 DIP 相比，PAD-Hand 在所有指标上均取得最优或接近最优的结果。

**HO3D 数据集。** 在 HO3D 上（Table 2），PAD-Hand 将 PA-MPJPE 从 7.50 mm 降至 **7.43 mm**（0.9%），ACCEL 从 4.98 降至 **2.71 mm/frame²**（45.6%）。PA-MPJPE 的提升幅度小于 DexYCB，但 ACCEL 的大幅下降表明物理感知损失在跨数据集上一致地改善了运动平滑度。HO3D 上 PA-MPJPE 增益较小的原因可能在于该数据集的初始估计质量更高或场景复杂度不同，但论文未对此展开详细分析。

**跨基线泛化性。** Table 6 展示了以 HaMeR 和 HandOccNet 作为不同图像姿态估计器时的结果。PAD-Hand 在这些不同质量的初始化上均能稳定提升性能，表明物理感知精调框架不依赖于特定的前端估计器。

**定性分析。** Figure 4（DexYCB）和 Figure 6（HO3D）展示了三个代表性序列的精调效果。在原始图像估计出现明显抖动的帧（红色框标注区域），PAD-Hand 输出的轨迹更加平滑且符合运动学规律。同时，方差图（joint-level 和 mesh-level）在这些抖动帧上呈现高值，直观地验证了模型的不确定性与运动估计不可靠区域的一致性。

### 消融实验

**欧拉-拉格朗日残差损失的有效性。** Table 3 对比了仅使用数据驱动损失与加入欧拉-拉格朗日残差损失（L_EL）的效果。添加 L_EL 后，PA-MPJPE、MPJPE 和 ACCEL 均获得统计显著的改善，证实动力学残差的虚拟观测建模是有效的物理先验注入方式。

**概率物理集成 vs. 确定性惩罚。** Table 4 和 Table 9 比较了三种物理集成策略：(1) 无物理损失；(2) 确定性残差惩罚（将残差直接作为 L2 损失项）；(3) 本文的概率虚拟观测方法。结果显示，概率集成在所有指标上均优于确定性惩罚，且欧拉-拉格朗日残差 R(q) 更低。这一消融直接支撑了核心主张：将物理残差视为分布而非硬约束，能更好地处理模型误差和估计不确定性。

**数据驱动损失的贡献。** Table 5 消融了数据驱动损失分量（L_g 和 L_r）的作用。结果表明，数据驱动损失与物理损失联合使用获得最佳性能，单独使用任一损失均会导致性能下降。这验证了两类损失在训练中的互补性。

**数据效率。** Table 8 展示了在不同训练数据比例下 L_EL 的效果。加入物理损失后，即使在数据稀缺条件下（如仅使用 25% 训练数据），模型仍能保持较好的性能，表明物理先验提供了有效的归纳偏置，降低了对大规模标注数据的依赖。

**未见数据集的泛化性。** Table 7 报告了在具有挑战性的 TACO 数据集（S1 测试分割）上的泛化结果。PAD-Hand 在该未见数据集上仍优于基线，且 L_EL 的加入增强了泛化能力，进一步验证了物理感知建模的鲁棒性。

**对腐败初始化的鲁棒性。** 附录 C.2 的实验表明，即使对初始姿态估计施加 80% 的高斯噪声（PA-MPJPE 恶化至 24.27 mm），PAD-Hand 仍能将其恢复至 6.53 mm，展示了扩散模型结合物理先验对严重初始误差的强鲁棒性。

### 方差估计的物理一致性验证

Figure 5 展示了动态方差的直方图分布，其中每个柱的颜色编码了该方差区间内的平均欧拉-拉格朗日残差（蓝色低，红色高）。结果显示，高方差区间与较大的动力学残差高度一致，即模型在物理违规严重的区域分配了更高的不确定性。这一对齐验证了 LLLA 方差估计的可解释性——方差不仅是模型的不确定性度量，更直接指示了物理一致性违规的程度。

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/008_Figure_5.jpg]]
*Figure 5: Distribution of dynamic variances for PAD-Hand. Bar color encodes the mean Euler–Lagrange residual within each variance bin (blue is low, red is high). Higher variance bins coincide with larger residuals, indicating that the model’s uncertainty aligns with physics violations*

### 失败模式与局限分析

尽管 PAD-Hand 在主实验中表现优异，但存在以下可识别的失败模式：

1. **物理模型近似误差。** 欧拉-拉格朗日动力学使用近似惯性参数且未显式建模接触力，在手-物体交互场景中可能不够精确。当前框架缺乏对物体几何和接触约束的建模，导致在精细操作场景中物理残差可能无法完全反映真实的动力学违规。

2. **对初始估计质量的依赖。** 方法依赖于现成的图像姿态估计器作为初始化。当初始估计质量极差时（如严重遮挡或极端姿态），性能会下降。虽然扩散模型具有一定的鲁棒性（如 80% 噪声实验所示），但极端情况下的恢复能力仍有上限。

3. **推理计算成本。** 方差估计需要蒙特卡洛采样（Algorithm 1），增加了推理阶段的计算开销。论文未报告具体的推理时间对比，这一点的实际影响需要结合部署场景手动验证。

4. **方差解释的局限性。** 当前方差估计仅针对动力学残差建模，未能直接传递到手部姿态本身的不确定性解释。这意味着用户可以看到哪些帧/关节存在物理违规，但无法直接获得姿态估计的置信区间。

5. **HO3D 评估的不完整性。** 由于 HO3D 测试集的姿态参数未公开，无法在该数据集上评估完整的物理残差 R(q)，限制了物理一致性验证的全面性。

6. **评估场景的覆盖范围。** 实验仅在 DexYCB、HO3D 和 TACO 三个数据集上进行，未见大规模野外视频（如 in-the-wild YouTube 视频）的测试。在复杂背景、动态光照和多样手-物交互场景下的泛化性仍需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/004_Table_1.jpg]]
*Table 1: Comparison to SOTAs on DexYCB. “*” denotes results obtained from official models; others are from original papers*

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/005_Table_2.jpg]]
*Table 2: Comparison to SOTAs on HO3D. “*” denotes results from official models; others are from original papers. “P” and “D” denote probabilistic and deterministic models, respectively*

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/007_Table_4.jpg]]
*Table 4: Ablation on physics integration on DexYCB*

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/009_Table_3.jpg]]
*Table 3: Effectiveness of residual loss on DexYCB*

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/010_Table_5.jpg]]
*Table 5: Effectiveness of data-driven losses*

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/011_Table_7.jpg]]
*Table 7: Generalization to unseen TACO [37]. S1 testing split is used for evaluation*

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/014_Table_9.jpg]]
*Table 9: Ablation on physics integration on DexYCB. † denotes that values are scaled by*

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/001_Figure_1.jpg]]
*Figure 1: Refined motion estimates by PAD-Hand with dynamic variance. Top: Image-based estimates (left) are refined by our model (PAD-Hand) (right) to enforce temporal and physics consistency. Bottom: Joint-level (left) and mesh-level (right) variance maps concentrate on frames/regions where the image-based motion estimate is unreliable (highlighted in red), aligning high variance with poor motion estimates. The color bar shows normalized variance (low to high)*

![[assets/figures/papers/paper_list_l998_https_arxiv_org_abs_2603_26068/figures/006_Figure_4.jpg]]
*Figure 4: Refined motion estimates by PAD-Hand with dynamic variance on DexYCB. We visualize three representative sequences (I–III). In each block, row (a) compares the original image-based motion estimates to the trajectories refined by PAD-Hand, while row (b) shows the corresponding variance estimations in terms of joint-level and mesh-level dynamic variance. The red boxes highlight frames where the image-based estimates exhibit strong jitter*

## 方法谱系与知识库定位

### 1. 问题定位：从确定性恢复走向概率物理推理

从单张图像或视频恢复手部运动的主流方法（**WiLoR**、**HaMeR**、**HandOccNet** 等图像姿态估计器，以及 **VIBE**、**TCMR**、**Deformer** 等视频运动恢复方法）虽然取得了显著的姿态精度提升，但存在一个共同瓶颈：**缺乏对物理一致性的可量化度量**。这些方法要么完全忽略物理约束，要么将动力学残差作为确定性惩罚项强制归零——这种做法隐含地假设模型估计完美无噪声，忽略了图像观测的不确定性和手部动力学模型本身的近似误差。

PAD-Hand 的核心推进在于**将欧拉-拉格朗日动力学残差从“硬约束”重新定义为“虚拟观测量”**，并以概率方式集成到条件扩散模型的训练目标中。这一转变使得模型能够：1）在数据驱动损失与物理先验之间进行软权衡；2）通过最后一层拉普拉斯近似（LLLA）为每个关节和每帧提供可解释的物理一致性方差估计。

### 2. 与扩散模型运动精调方法的关系

在扩散模型用于运动精调的方法谱系中，**DIP**（Diffusion-based Inverse Problem solver）是一个直接相关的基线。DIP 将运动恢复视为逆问题，利用扩散先验进行后处理精调，但其目标函数仅包含数据驱动项，缺乏物理感知能力。PAD-Hand 在以下关键维度上区别于 DIP：

| 维度 | DIP | PAD-Hand |
|------|-----|----------|
| 物理约束 | 无 | EL 残差作为虚拟观测损失 |
| 不确定性估计 | 无 | LLLA + 反向传播方差 |
| 扩散输入 | 合成噪声 | 图像姿态估计器预测值 |
| 方差传播 | 无 | 递归传播至最终运动与力方差 |

实验证据（Table 10、Table 11）表明，PAD-Hand 在 DexYCB 和 HO3D 上均优于 DIP，且 EL 残差 $R(q)$ 更低，验证了物理感知扩散目标的增益并非来自更强的数据拟合，而是来自物理合理性的提升。

### 3. 与简单平滑后处理的本质区别

一个自然的质疑是：PAD-Hand 的 ACCEL 指标大幅下降（DexYCB 上 50.1%）是否仅来自时序平滑效应？**SmoothFilter** 基线的对比（Table 1）给出了否定答案——简单平滑虽然能降低加速度，但会牺牲姿态精度（PA-MPJPE 升高）。PAD-Hand 则在降低 ACCEL 的同时**提升**了 PA-MPJPE（4.88→4.63 mm），表明物理感知精调实现了精度与平滑性的帕累托改进，而非简单的精度-平滑折衷。

### 4. 方法适用边界

PAD-Hand 的适用性受以下因素制约：

**（1）对初始姿态估计质量的依赖。** 方法以现成图像姿态估计器（如 WiLoR）的输出作为扩散模型的训练输入和条件信号。当初始估计质量极差时（如严重遮挡、极端视角），物理残差提供的约束可能不足以完全纠正姿态误差。消融实验（Section C.2）显示模型对 80% 高斯噪声腐败具有鲁棒性，但该实验仅针对合成噪声，真实场景中的系统性估计偏差可能更难修复。

**（2）物理模型的近似性。** 欧拉-拉格朗日动力学使用近似惯性参数（质量 $m$、惯量 $I$），且未显式建模接触力 $\mathcal{F}$——在公式中 $\hat{\mathcal{F}}_t$ 仅作为残差中的估计项出现。这意味着在手-物体交互场景中，接触力的缺失可能导致物理残差本身不准确，从而削弱虚拟观测损失的约束效力。

**（3）方差估计的计算代价。** LLLA 后验预测和方差传播算法（Algorithm 1）需要蒙特卡洛采样，增加了推理计算成本。这对于实时应用场景可能构成障碍。

**（4）数据集的局限性。** 实验仅在 DexYCB 和 HO3D 两个受控数据集上进行，虽然 TACO 数据集上的泛化实验（Table 7）显示了正向迁移，但未见大规模野外视频测试。此外，HO3D 测试集未公开姿态参数，导致完整物理残差 $R(q)$ 无法在该数据集上评估。

### 5. 开放问题与未来方向

**（1）物体几何与接触信息的融合。** 当前方法仅建模手部自身的动力学，未利用被操作物体的几何和物理属性。将物体信息纳入 EL 动力学框架，有望处理精细的手-物体交互场景（如工具使用、灵巧操作）。

**（2）方差估计的扩展与标定。** 当前方差估计仅针对动力学残差，未直接传递到手部姿态本身的不确定性解释。能否将 LLLA 方差与姿态误差建立标定关系（如期望校准误差），使其成为可信的置信度度量？此外，方差信息能否用于主动学习（选择高不确定性帧进行人工标注）或在线自适应系统？

**（3）极端数据稀缺条件下的物理先验有效性。** Table 8 的数据效率实验表明 $\mathcal{L}_{EL}$ 在小数据场景下仍有增益，但当训练数据极度稀缺或姿态分布严重偏离训练集时，虚拟观测先验是否仍能提供有效约束？这需要更系统的分布外测试。

**（4）与概率人体运动模型的统一。** PAD-Hand 的概率物理集成框架原则上可推广至全身人体运动恢复（如 SMPL 模型）。将 EL 动力学扩展至全身运动链，并与现有概率人体模型（如 HuMoR）融合，是一个自然且有价值的延伸方向。

---

**知识库定位总结：** PAD-Hand 属于**物理感知的概率运动精调方法**，其核心创新在于通过虚拟观测变量将物理先验融入扩散模型的概率框架，并首次为手部运动恢复提供了可解释的逐关节动态方差估计。方法在姿态精度和平滑性上均超越现有图像/视频基线和扩散精调基线（DIP），但物理模型的近似性和对初始估计的依赖构成了当前适用边界。

## 原文 PDF

![[paperPDFs/CVPR_2026/PAD_Hand_Physics_Aware_Diffusion_for_Hand_Motion_Recovery.pdf]]