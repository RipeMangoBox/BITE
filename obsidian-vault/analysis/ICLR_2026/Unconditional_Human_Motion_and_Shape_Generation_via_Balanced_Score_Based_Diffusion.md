---
title: Unconditional Human Motion and Shape Generation via Balanced Score Based Diffusion
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Unconditional_Human_Motion_and_Shape_Generation_via_Balanced_Score_Based_Diffusion.pdf
project_link: null
code_link: null
aliases:
- BSBD
- UHMSGBSBD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 结构保持的特征归一化（旋转保持正交性，平移保持各向同性）和理论驱动的梯度平衡损失加权（逐组不确定性加权和维度补偿）
primary_logic: 通过对SMPL参数进行结构保持的归一化，并根据梯度分析设计自适应损失权重，可以在不使用辅助损失和冗余特征的条件下，使分数基扩散模型高效生成高质量的人体运动与形状，并兼容概率流ODE进行采样与似然估计。
claims:
- 将输入特征归一化从简单的均值/标准差改为结构保持归一化，FID从6.23大幅降至3.32，同时多样化、足滑和肢体长度一致性均改善。
- 引入针对梯度平衡的损失加权（4.4节和4.5节）以及特征组维度处理（4.6节），累计将FID降至2.40，并显著减少脚滑动至20.43%和肢体长度标准差至0.02 mm。
- 最终SMPL模型在HumanML3D测试集上取得FID 1.81，与SOTA方法MLD（1.17）和MDM（3.58）相当或更优，同时直接生成形状，避免后处理。
- 梯度可视化显示，经过重新平衡后，各特征组和不同时间步的梯度分布更均匀。
---

# Unconditional Human Motion and Shape Generation via Balanced Score Based Diffusion

> [!tip] 核心洞察
> 通过对SMPL参数进行结构保持的归一化，并根据梯度分析设计自适应损失权重，可以在不使用辅助损失和冗余特征的条件下，使分数基扩散模型高效生成高质量的人体运动与形状，并兼容概率流ODE进行采样与似然估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于平衡得分扩散的无条件人体运动与形状生成 |
| 英文题名 | Unconditional Human Motion and Shape Generation via Balanced Score Based Diffusion |
| 会议/期刊 | ICLR 2026 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Balanced Score-Based Diffusion |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D (test set) 上，FID↓ 1.81 (OursSMPL) vs 3.58 (MDM) (-1.77)；Diversity↑ 8.73 (OursSMPL) vs 8.14 (MDM) (+0.59)；Foot skating (%)↓ 16.31 (OursSMPL) vs 8.58 (MDM) (+7.73)。

## 概要

无条件人体运动与形状生成的核心瓶颈在于：表示人体姿态、朝向、平移和形状的SMPL参数构成一个异构特征空间，各组分的统计特性差异显著。标准扩散模型在训练时，不同特征组和不同时间步的梯度动态严重失衡，导致生成质量受限。现有方法往往依赖辅助损失或冗余特征来缓解这一问题，但缺乏对扩散训练动态本身的系统性分析。

本文提出**Balanced Score-Based Diffusion**，核心思路是通过**结构保持的特征归一化**与**理论驱动的梯度平衡损失加权**，直接在分数基扩散框架内解决上述失衡问题，无需任何辅助损失或额外特征。具体而言，该方法对旋转向量施加正交性保持的归一化，对平移施加各向同性归一化，并基于梯度分析为每个特征组和每个扩散时间步自适应学习损失权重，同时通过维度补偿均衡高低维特征组的贡献。这一最小化设计使模型能够高效匹配人体运动分布，并天然兼容概率流ODE（PF-ODE）进行快速采样与似然估计。

实验表明，该方法的累积消融效果显著：在HumanML3D验证集上，结构保持归一化将FID从6.23降至3.32（Table 1）；引入梯度平衡加权后进一步降至2.65；逐组不确定性加权和维度处理后达到2.40，同时脚滑动率降至20.43%、肢体长度标准差降至0.02 mm。最终模型在HumanML3D测试集上取得FID 1.81，与SOTA方法**MLD**（Chen et al., CVPR 2023, FID 1.17）和**MDM**（Tevet et al., ICCV 2023, FID 3.58）可比或更优，且直接生成形状参数，避免了后处理步骤（Table 2）。采样仅需31次神经网络评估（NFE），在单张RTX 3090上平均耗时约1.7秒。

该方法在方法谱系中定位于**分数基扩散模型**的轻量化改进分支：它继承EDM/EDM2的连续时间扩散框架与预条件网络设计，但通过输入空间的结构化重整和损失空间的自适应均衡，将人体运动生成的训练稳定性与样本质量提升至与专用运动扩散模型相当的水平。其知识贡献在于揭示并量化了异构参数空间对扩散训练的干扰机制，并提供了一套可复用的归一化与加权方案，为后续条件生成和多模态扩展奠定了基础。

**局限与待验证点**：基于SMPL参数的模型脚滑动率（16.31%）仍高于使用3D关节坐标的MDM（8.58%），可能需要额外运动学约束；生成网格偶现自相交伪影（训练数据中亦存在）；楼梯行走场景下高度保持不稳定。这些问题指向物理约束与后处理优化的潜在改进方向。

### 问题背景

人体运动生成是计算机视觉与图形学中的核心任务之一，其目标是从噪声或条件信号中合成自然、多样的人体运动序列。主流方法通常依赖参数化人体模型（如SMPL）来表示姿态与形状，并将运动建模为高维参数序列的分布学习问题。近年来，扩散模型在该领域取得了显著进展，但现有工作普遍面临一个深层瓶颈：**异构特征空间的统计特性失配**。

具体而言，一个典型的SMPL运动帧包含四类特征组——关节旋转、全局朝向、全局平移和体型参数——它们在物理意义、数值范围和维度上截然不同。标准扩散模型的训练目标是对所有特征施加统一的L2去噪损失，这隐含地假设各维度对损失的贡献是均质的。然而，当特征组的梯度动态在训练过程中严重失衡时，模型会倾向于拟合高幅值或高维度的特征组，导致生成质量下降、脚滑动加剧或肢体长度不一致等问题。

### 现有方法缺口

当前主流的人体运动扩散模型通常采用以下策略来应对上述挑战，但各自存在不足：

- **辅助损失与冗余表示**：如 **MDM**（Tevet et al., ICCV 2023）使用3D关节坐标作为运动表示，并依赖脚部接触损失等辅助项来抑制脚滑动。这类方法虽然有效，但引入了额外的超参数调优负担，且3D关节坐标无法直接生成体型参数，需要后处理步骤。
- **隐空间扩散**：如 **MLD**（Chen et al., CVPR 2023）将运动编码到隐空间后再进行扩散，虽然提升了效率，但其性能依赖于预训练的特征提取器（如HumanML3D的运动编码器），并非完全无条件生成。
- **经验性损失加权**：部分工作采用EDM2的连续不确定性加权来平衡不同时间步的损失，但该方法未考虑**特征组间**的梯度差异，导致高维特征组（如关节旋转）在训练中占据主导地位。

一个关键观察是：**简单地使用均值/标准差进行Z分数归一化（如HumanML3D启发的方式）并不能真正解决梯度失衡问题**。这是因为旋转矩阵的正交性、全局平移的各向同性等几何结构在普通归一化中被破坏，使得不同特征组的期望幅值仍不一致，训练信号依然偏向某些特征组。

### 本文动机

本文的核心动机在于：**能否在不引入辅助损失、不依赖冗余特征表示的前提下，仅通过结构保持的特征归一化和理论驱动的梯度平衡策略，使分数基扩散模型高效生成高质量的人体运动与形状？**

这一动机源于以下洞察：
1. **结构保持归一化**：旋转向量应保持其期望幅值为1（通过乘以√3实现），全局平移应使用所有坐标的Z分数以保持各向同性，而体型参数则可逐元素标准化。这种归一化尊重了各特征组的几何本质。
2. **梯度平衡损失加权**：通过分析去噪损失对不同特征组和时间步的梯度贡献，可以推导出自适应的逐组损失权重，使训练过程中的梯度动态趋于均匀，从而避免任何单一特征组主导优化。
3. **概率流ODE兼容性**：平衡后的分数基模型天然兼容概率流ODE，支持高效采样（如31次函数评估）和精确似然估计，为生成质量评估提供了额外维度。

最终目标是构建一个**最小化、自洽的无条件人体运动与形状生成框架**，其性能可与依赖大量工程技巧的SOTA方法相媲美，同时保持方法的简洁性和理论可解释性。

## 核心方法与创新机理

本工作提出 **Balanced Score-Based Diffusion**，在不引入辅助损失、冗余特征或后处理步骤的条件下，通过两个关键创新使分数基扩散模型能够高效生成高质量的无条件人体运动与形状：

1.  **结构保持的特征归一化（Structure-Preserving Feature Normalization）**
    针对 SMPL 参数中异构特征组（姿态旋转、全局朝向、全局平移、形状系数）的统计特性差异，设计了保持各自几何结构的标准化策略。具体而言：
    *   **旋转向量**（姿态与全局朝向）：乘以 $\sqrt{3}$ 使其期望幅值为 1，保持正交性约束。
    *   **全局平移**：对所有坐标统一计算 Z 分数，避免各向异性缩放扭曲 3D 空间。
    *   **形状参数**：采用逐元素 Z 分数归一化。
    该归一化替代了受 HumanML3D 启发的简单均值/标准差缩放，使各特征组在训练初期即具有统一的尺度与结构完整性。

2.  **理论驱动的梯度平衡损失加权（Gradient-Balanced Loss Weighting）**
    针对标准扩散模型训练中不同特征组与不同时间步之间梯度动态不平衡的问题，提出了一套自适应损失加权机制：
    *   **逐时间步不确定性加权**：引入可学习的 MLP $u_\psi(t)$ 逼近各时间步的梯度幅度，并按 $\frac{\sqrt{\lambda(t)}}{\sqrt{e^{u_\psi(t)}}}$ 缩放去噪损失，确保所有时间步对参数更新的贡献均衡。
    *   **逐特征组不确定性加权**：将 $u_\psi$ 扩展为每组独立的 $u_\psi^k(t)$（$k \in \{J, \Phi, \tau, \beta\}$），分别学习各组的梯度动态，实现组间梯度平衡。
    *   **维度补偿串联权重**：针对特征组维度差异（姿态 126 维 vs. 形状 10 维），设计幅度保持的串联权重 $w^k = \sqrt{\frac{N^J+N^\Phi+N^\tau+N^\beta}{4}} / \sqrt{N^k}$，在输入拼接与损失计算中均衡各组贡献，防止高维组主导训练。

上述两个创新形成因果链条：**结构保持归一化**为模型提供了几何一致的输入空间，而**梯度平衡加权**则确保了该空间中各分量被公平地学习。消融实验（Table 1）验证了这一因果机制：仅将输入归一化改为结构保持，FID 即从 6.23 大幅降至 3.32；在此基础上依次引入梯度均衡、逐组不确定性与维度补偿，FID 进一步降至 2.40，同时脚滑动率降至 20.43%、肢体长度标准差降至 0.02 mm。最终模型在 HumanML3D 测试集上取得 FID 1.81，与需依赖辅助特征的 SOTA 方法 **MLD**（Chen et al., CVPR 2023, FID 1.17）和 **MDM**（Tevet et al., ICCV 2023, FID 3.58）相当或更优，且直接输出 SMPL 参数与形状，无需后处理。

**与 baseline 的核心差异**在于：baseline 沿用 EDM2 的连续不确定性加权 $\mathcal{L}_{EDM2}$ 与简单 Z 分数归一化，仅关注时间步维度的损失平衡，忽略了特征空间内部的异构性与维度差异。本方法通过**结构保持归一化**与**多维梯度均衡**两个 changed slots，将平衡性从单一时间维度扩展至特征组维度，从而在最小化模型复杂度的前提下显著提升生成质量。

本文提出一种基于分数基扩散模型的无条件人体运动与形状生成方法，其核心在于不依赖辅助损失或冗余特征，仅通过**结构保持的特征归一化**与**理论驱动的梯度平衡损失加权**，即可在标准SMPL参数空间上实现高质量生成。整体pipeline由以下模块串联构成：

1. **SMPL运动表示**：将每帧人体姿态编码为SMPL参数的拼接向量 $\mathbf{x}(0)_i = [J_i \quad \Phi_i \quad \tau_i \quad \beta]^T$，包含21个关节的6D旋转 $J_i$、全局朝向6D $\Phi_i$、全局平移3D $\tau_i$ 以及形状参数10D $\beta$（Equation 9）。这一表示直接输出可驱动SMPL-H网格的参数，无需后处理。

2. **结构保持的特征归一化**：针对异构特征空间的统计特性差异，对旋转分量施加 $\sqrt{3}$ 缩放以保持正交性并使期望幅值为1；对全局平移采用所有坐标的Z分数归一化以保持各向同性；形状参数则逐元素Z分数标准化（Section 4.3）。该步骤是后续梯度均衡的基础。

3. **方差爆炸连续扩散前向过程与预条件**：采用 $\mathbf{x}(t) = \mathbf{x}(0) + t\epsilon$ 的连续时间扩散过程（Equation 1），并通过预条件模块 $c_{skip}, c_{out}, c_{in}, c_{noise}$ 对网络输入输出进行标准化，使 $F_\theta$ 的输入输出保持单位方差（Equation 5）。

4. **EDM2 U-Net骨干网络**：使用1D卷积操作的EDM2架构作为去噪预测器 $F_\theta$，支持变长序列处理（Section A.2）。网络接收噪声数据 $\mathbf{x}(t)$ 和时间步 $t$，输出对原始数据的预测 $D_\theta$。

5. **梯度平衡损失加权模块**：引入可学习的MLP $u_\psi(t)$ 来估计不同时间步的梯度幅度，并按 $\sqrt{\lambda(t)} / \sqrt{e^{u_\psi(t)}}$ 缩放去噪损失（Equation 16）；进一步为每个特征组 $k \in \{J, \Phi, \tau, \beta\}$ 单独学习 $u_\psi^k(t)$，并引入维度补偿权重 $w^k = \sqrt{(N^J+N^\Phi+N^\tau+N^\beta)/4} / \sqrt{N^k}$，最终形成逐组平衡的训练目标（Equation 20）。

6. **ODE采样**：训练完成后，使用Heun二阶ODE求解器沿概率流ODE进行采样，仅需31次函数评估（NFE）即可从噪声生成运动序列，并支持PF-ODE似然估计与往返误差评估（Section 5.2）。

**数据流**：原始SMPL参数序列 → 结构保持归一化 → 加噪前向扩散 → EDM2 U-Net去噪预测 → 梯度平衡损失反向传播（含 $u_\psi$ 联合优化）→ 训练收敛后通过ODE求解器采样 → 直接输出SMPL参数并提取网格。

该框架的关键因果机制在于：通过结构保持归一化消除特征组间的统计偏差，再通过梯度分析驱动的自适应损失权重使各特征组在不同时间步的梯度动态趋于均衡，从而让扩散模型能够高效匹配人体运动分布。消融实验（Table 1）验证了这一机制的有效性——仅改进归一化即可将FID从6.23降至3.32，叠加梯度平衡策略后进一步降至2.40。

### 3.1 运动表示与预处理模块

**SMPL运动帧表示** 将人体运动序列建模为帧级SMPL参数的串联。第 $i$ 帧的原始特征向量定义为：

$$\mathbf{x}(0)_i = \left[ J_i \quad \Phi_i \quad \tau_i \quad \beta \right]^T$$

其中各特征组的维度与语义为：
- $J_i \in \mathbb{R}^{N^J}$（$N^J = 21 \times 6$）：21个关节的6D旋转表示，描述身体姿态；
- $\Phi_i \in \mathbb{R}^{N^\Phi}$（$N^\Phi = 6$）：全局朝向的6D旋转表示；
- $\tau_i \in \mathbb{R}^{N^\tau}$（$N^\tau = 3$）：全局平移的3D坐标；
- $\beta \in \mathbb{R}^{N^\beta}$（$N^\beta = 10$）：SMPL形状参数，所有帧共享。

这一最小化表示直接生成SMPL参数，避免了后处理步骤。

### 3.2 扩散框架与预条件模块

**前向扩散过程** 采用方差爆炸（Variance Exploding）的连续时间扩散：

$$\mathbf{x}(t) = \mathbf{x}(0) + t \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

对应的概率流ODE（PF-ODE）为：

$$d\mathbf{x}(t) = -t \nabla_{\mathbf{x}(t)} \log p(\mathbf{x}(t), t)$$

**网络预条件** 为稳定训练，对网络输入输出进行标准化缩放：

$$D_{\theta}(\mathbf{x}(t), t) = c_{skip}(t) \mathbf{x}(t) + c_{out}(t) F_{\theta}(c_{in}(t) \mathbf{x}(t), c_{noise}(t))$$

其中 $F_{\theta}$ 为1D操作的EDM2 U-Net骨干网络，$c_{skip}$、$c_{out}$、$c_{in}$、$c_{noise}$ 为基于单位方差要求导出的标量系数，确保网络输入输出具有适当的尺度。

### 3.3 结构保持的特征归一化模块

**核心问题**：异构特征组（旋转、平移、形状）的统计特性不同，简单的Z分数归一化会破坏几何结构，导致训练不稳定。

**解决方案**：对各类特征分别进行结构保持的标准化，使期望幅值 $\mathcal{M}[\mathbf{a}] = \sqrt{\frac{1}{N^a} \sum_{i=1}^{N^a} \mathbb{E}[a_i^2]}$ 为1：

- **旋转向量**（关节角 $J$ 和全局朝向 $\Phi$）：乘以 $\sqrt{3}$ 使期望幅值为1，保持正交性；
- **全局平移 $\tau$**：对所有坐标维度统一计算Z分数（均值/标准差），避免偏斜3D空间；
- **形状参数 $\beta$**：逐元素Z分数标准化。

消融实验（Table 1）表明，仅此归一化改进即可将FID从6.23降至3.32。

### 3.4 梯度均衡的损失加权模块

**理论驱动**：标准EDM损失 $\mathcal{L}_{EDM}(\theta) = \mathbb{E} \left[ \lambda(t) \| D_{\theta}(\mathbf{x}(t), t) - \mathbf{x}(0) \|_2^2 \right]$ 在不同时间步的梯度动态不平衡。通过分析梯度幅度与预期损失的关系，推导出自适应加权方案。

**不确定性权重学习**：引入可学习的MLP $u_{\psi}(t)$，通过最小化以下目标来估计最优权重：

$$e^{u_{\psi}^*(t)} = \mathbb{E}\left[ \frac{\lambda(t)}{N L} \| D_{\theta}(\hat{\mathbf{x}}(t), t) - \hat{\mathbf{x}}(0) \|_2^2 \right]$$

修改后的去噪损失为：

$$\mathcal{L}(\theta) = \mathbb{E}\left[ \frac{\sqrt{\lambda(t)}}{N L \oslash (\sqrt{e^{u_{\psi}(t)}})} \| D_{\theta}(\hat{\mathbf{x}}(t), t) - \hat{\mathbf{x}}(0) \|_2^2 \right]$$

其中 $\oslash$ 表示逐元素除法。该加权使梯度幅度与 $c_{out}(t) / \sqrt{\mathbb{E}[\|D_{\theta} - \mathbf{x}(0)\|_2^2]}$ 成比例，实现不同时间步的梯度均衡。Table 1显示此改进将FID进一步降至2.65。

### 3.5 逐特征组均衡模块

**维度补偿权重**：不同特征组的维度差异（$N^J=126, N^\Phi=6, N^\tau=3, N^\beta=10$）会导致高维组主导训练。通过幅度保持的串联权重进行补偿：

$$w^k = \sqrt{\frac{N^J + N^\Phi + N^\tau + N^\beta}{4}} \frac{1}{\sqrt{N^k}}$$

该权重同时应用于输入特征缩放和损失计算。

**逐组不确定性学习**：为每个特征组 $k \in \{J, \Phi, \tau, \beta\}$ 独立学习不确定性函数 $u_{\psi^k}^k(t)$，最终训练目标为：

$$\mathcal{L}_{\mathrm{final}}(\theta) = \sum_{k \in \{J, \Phi, \tau, \beta\}} \mathbb{E}\left[ \frac{\sqrt{\lambda(t)} w^k}{N L \oslash (\sqrt{e^{u_{\psi^k}^k(t)}})} \| D_{\theta}^k(\hat{\mathbf{x}}_w(t), t) - \hat{\mathbf{x}}^k(0) \|_2^2 \right]$$

梯度可视化（Figure 2）证实，经过逐组均衡后，各特征组在不同时间步的梯度分布趋于均匀。Table 1的累积结果显示，逐组不确定性加权将FID降至2.48，加入维度处理后最终达到2.40，同时脚滑动降至20.43%、肢体长度标准差降至0.02 mm。

![[assets/figures/papers/paper_list_l1908_Unconditional_Human_Motion_and_Shape_Generation_via_Balanced_Score_Based/figures/003_Figure_2.jpg]]
*Figure 2: Average L2 norms of gradients with respect to*

## 实验与关键发现

### 核心瓶颈验证：梯度不平衡是性能劣化的根源

本文的核心假设是：SMPL参数空间中不同特征组（姿态、朝向、平移、形状）的统计特性差异，会导致扩散模型训练过程中梯度动态严重不平衡。Figure 2 通过PyTorch autograd直接测量了各特征组梯度随扩散时间步的分布，提供了决定性证据。

在基线模型（使用标准Z分数归一化）中，梯度幅度在不同时间步之间呈现剧烈波动，且不同特征组的梯度量级差异显著。经过本文提出的结构保持归一化和逐组不确定性加权后，梯度分布趋于均匀——各特征组在所有时间步上的梯度幅度被拉平至相近水平。这一可视化直接印证了方法设计的因果机制：**通过平衡梯度，模型能够更有效地学习所有特征组的联合分布，而非被高维或大方差组主导**。

### 消融实验：逐项改进的累积效应

Table 1 以累积方式报告了各方法模块的贡献，所有实验均在验证集上计算FID。消融链条清晰地展示了从基线到最终模型的性能跃迁路径：

![[assets/figures/papers/paper_list_l1908_Unconditional_Human_Motion_and_Shape_Generation_via_Balanced_Score_Based/figures/002_Table_1.jpg]]
*Table 1: Collection of results from each ablation performed in Section 4. Ablations and results are cumulative, meaning a section’s experiment also includes changes from all previous sections. Each of our proposed additions improve the model. FID is calculated on the validation set*

| 消融阶段（累积） | FID↓ | 多样性↑ | 足滑动率(%)↓ | 肢体长度σ(mm)↓ |
|---|---|---|---|---|
| 基线（Z分数归一化） | 6.23 | — | — | — |
| + 结构保持归一化（4.3节） | 3.32 | — | — | — |
| + 梯度均衡损失加权（4.4节） | 2.65 | — | — | — |
| + 逐组不确定性加权（4.5节） | 2.48 | — | — | — |
| + 特征组维度处理（4.6节） | 2.40 | — | 20.43 | 0.02 |

**结构保持归一化**是贡献最大的单项改进：将FID从6.23降至3.32（降幅46.7%）。这表明简单的均值/标准差归一化严重扭曲了旋转和平移的几何结构，导致扩散模型难以匹配真实运动分布。旋转向量乘以√3使其期望幅值为1，全局平移采用所有坐标的联合Z分数，这些设计保持了SE(3)变换的底层几何性质。

**梯度均衡损失加权**（4.4节）将FID进一步降至2.65。该方法通过学习一个MLP $u_\psi(t)$ 来估计不同时间步的梯度幅度，并在损失中按 $1/\sqrt{e^{u_\psi(t)}}$ 进行缩放，使得所有时间步对参数更新的贡献趋于一致。

**逐组不确定性加权**（4.5节）将FID推至2.48。将 $u_\psi$ 扩展为四个独立的 $u_\psi^k(t)$（分别对应姿态、朝向、平移、形状），允许模型自适应地调节各特征组的损失权重，而非使用全局标量。

**特征组维度处理**（4.6节）使FID达到2.40，同时足滑动率降至20.43%、肢体长度标准差降至0.02 mm。通过权重 $w^k = \sqrt{(N^J+N^\Phi+N^\tau+N^\beta)/4} / \sqrt{N^k}$ 对输入和损失进行缩放，消除了高维组（如126维姿态）对低维组（如3维平移）的支配效应。

### 主结果：与SOTA方法的定量对比

Table 2 报告了在HumanML3D测试集上与两个代表性扩散模型的全面比较。所有模型使用相同的训练/验证/测试划分，评估帧数192，采样5000个序列并取三次运行的最佳值。

![[assets/figures/papers/paper_list_l1908_Unconditional_Human_Motion_and_Shape_Generation_via_Balanced_Score_Based/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison between our final models and two other generative human motion diffusion models. FID is calculated on the test set. Best in each column is bold, second best is underlined. The Real row depicts metrics calculated on training data*

| 模型 | FID↓ | 多样性↑ | 足滑动率(%)↓ | 肢体长度σ(mm)↓ |
|---|---|---|---|---|
| Real（训练数据） | 0.02 | 8.69 | 9.18 | 0.00 |
| MDM (Tevet et al., ICCV 2023) | 3.58 | 8.14 | **8.58** | 3.73 |
| MLD (Chen et al., CVPR 2023) | **1.17** | **9.37** | — | — |
| OursSMPL | 1.81 | 8.73 | 16.31 | **0.02** |
| OursRootRel | 3.18 | 8.76 | 7.97 | 1.74 |

**OursSMPL** 在FID上（1.81）显著优于MDM（3.58），与MLD（1.17）处于同一量级。但需注意公平性差异：MLD使用HumanML3D的文本特征作为条件输入，而本文方法为无条件生成，且直接输出SMPL参数（包含形状），无需后处理步骤。

**肢体长度一致性**是OursSMPL的突出优势：0.02 mm的标准差远优于MDM的3.73 mm，甚至优于训练数据的理论下界（0.00 mm仅因SMPL模板本身无变化）。这归因于形状参数β的直接生成，避免了从关节位置反推骨骼长度时引入的误差。

**足滑动**是主要短板：OursSMPL的16.31%高于MDM的8.58%。原因在于MDM使用3D关节坐标表示，天然对足部位置施加更强的约束；而SMPL参数空间缺乏显式的运动学约束。OursRootRel通过转换为根相对坐标，将足滑动降至7.97%，验证了表示选择对该指标的关键影响。

### 失败模式与局限性

尽管整体质量与SOTA相当，本文方法存在三类已知失败模式：

1. **足滑动**：如主结果所示，SMPL参数化模型的足滑动率（16.31%）仍高于基于关节坐标的方法。这源于旋转参数的小误差会沿运动链累积放大至末端效应器位置。

2. **网格自相交**：渲染网格中偶尔出现身体部件穿透，这一伪影也存在于训练数据中，表明模型忠实地学习了数据分布中的缺陷，而非方法本身引入。

3. **高度漂移**：在楼梯行走场景中，角色上升后有时无法保持高度，可能因缺乏全局位置的历史一致性约束。

### PF-ODE评估：采样效率与似然估计

Figure 3 展示了概率流ODE框架下的系统评估。在归一化特征空间中的往返误差随反向NFE增加而单调下降，31次函数评估即可达到较低的往返误差水平。负对数似然（NLL）在未归一化特征空间中随NFE增加而收敛，验证了模型作为连续归一化流的有效性。这些结果表明，本文的平衡策略不仅提升了生成质量，还保持了扩散模型在概率推理方面的理论优势——这是许多针对人体运动定制的扩散方法所不具备的特性。

![[assets/figures/papers/paper_list_l1908_Unconditional_Human_Motion_and_Shape_Generation_via_Balanced_Score_Based/figures/005_Figure_3.jpg]]
*Figure 3: PF-ODE evaluation on the full-length test motions. (a) NLL in unormalized feature space vs. NFE. (b) Round-trip error in normalized feature space vs. backwards NFE. (c) Round trip error in normalized feature space vs. backwards*

### 公平性说明

所有对比实验遵循严格公平性协议：MDM使用作者公布的代码和默认超参数进行无条件重训练；所有模型采用相同的训练/验证/测试划分（10626/665/1997）；FID和多样性计算遵循HumanML3D官方协议；足滑动和肢体长度标准差作为补充质量指标；三次运行取最佳值，变化幅度≤3%。

![[assets/figures/papers/paper_list_l1908_Unconditional_Human_Motion_and_Shape_Generation_via_Balanced_Score_Based/figures/001_Figure_1.jpg]]
*Figure 1: Unconditionally generated samples from our final model. SMPL parameters are generated directly and the mesh is extracted with the SMPL-H model. Generated with 31 NFE. Darker color indicates later frames in the sequence. See supplementary videos for more qualitative results*

![[assets/figures/papers/paper_list_l1908_Unconditional_Human_Motion_and_Shape_Generation_via_Balanced_Score_Based/figures/006_Table_3.jpg]]
*Table 3: Hyperparameters used for all versions of our model*

## 定位与知识库关联

### 1. 与基线方法的关系

本工作属于基于扩散模型的无条件人体运动生成方向，其直接参照系为连续时间分数基扩散框架。在基础架构上，方法沿用了 **EDM**（Karras et al., NeurIPS 2022）的方差爆炸前向过程与预条件策略，并采用 **EDM2**（Karras et al., 2024）的1D U-Net骨干网络作为去噪函数 $F_\theta$。这一选择使模型天然兼容概率流ODE（PF-ODE），支持高效采样和似然估计。

与现有运动生成扩散模型的根本差异在于**问题定位的层次**。主流方法如 **MDM**（Tevet et al., ICCV 2023）和 **MLD**（Chen et al., CVPR 2023）将性能瓶颈归因于表示能力或生成范式，分别采用Transformer扩散架构和潜空间扩散来提升质量。本文则从更底层的优化动力学出发，指出核心瓶颈在于**异构特征空间（姿态旋转、全局朝向、平移、形状）的统计特性差异**，导致扩散训练过程中不同特征组和不同时间步的梯度动态严重失衡。这一诊断将问题从“模型设计”下移至“损失景观的几何特性”，构成了方法论的独特贡献。

在具体技术手段上，本文与基线的关键分叉点包括：

- **输入归一化策略**：基线采用受HumanML3D启发的Z分数归一化（逐元素均值，各特征组标准差的均值），忽视了旋转矩阵的正交性和平移空间的各向同性。本文提出结构保持归一化——旋转向量乘以 $\sqrt{3}$ 使期望幅值为1，平移采用全局坐标Z分数，形状参数逐元素标准化。这一改动使FID从6.23骤降至3.32（Table 1），揭示了特征空间几何结构对扩散训练的决定性影响。

- **损失加权机制**：基线使用EDM2的连续不确定性加权 $\mathcal{L}_{\text{EDM2}}$（Equation 8），仅平衡不同时间步的损失尺度。本文通过梯度分析（Section 4.4）发现，最优逐时间步权重应使梯度幅值正比于 $c_{out}(t)$ 而反比于预期L2损失的平方根，由此引入可学习的 $u_\psi(t)$ 来逼近这一理论最优加权（Equation 16）。进一步，将加权细化为逐特征组的 $u_\psi^k(t)$（Section 4.5），并引入维度补偿权重 $w^k = \sqrt{N_{\text{total}}/4} / \sqrt{N^k}$（Equation 18）以消除高维组（如126维关节角）对低维组（如3维平移）的支配效应。这一系列操作累计将FID降至2.40，脚滑动降至20.43%（Table 1）。

- **表示空间选择**：MDM使用3D关节坐标作为生成目标，天然有利于约束脚滑动（8.58%），但需后处理拟合SMPL参数。本文直接生成SMPL参数（关节6D旋转、全局朝向、平移、形状），避免后处理，但脚滑动（16.31%）相对较高，构成了表示空间选择的固有权衡。

### 2. 适用边界

本方法的核心假设与适用范围如下：

- **表示空间约束**：方法深度耦合于SMPL参数化人体模型。关节角采用6D连续旋转表示，依赖旋转矩阵的正交归一化假设。若迁移至其他骨架拓扑或关节表示（如四元数、轴角），需重新推导结构保持归一化策略。

- **无条件生成场景**：当前训练和评估均基于无条件设定，未引入文本、动作标签或场景上下文。方法的核心组件（特征归一化、梯度均衡）是任务无关的优化技术，理论上可迁移至条件生成，但需验证条件信号引入后梯度动态是否保持平衡。

- **数据分布假设**：特征归一化依赖训练集统计量（均值和标准差），且 $u_\psi$ 网络在训练集上学习时间步与特征组的权重映射。在分布外运动（如极端姿态、非人形运动）上的泛化性未经检验。

- **计算资源边界**：方法采用EDM2骨干网络，训练需600 epoch，采样使用Heun二阶ODE求解器（31 NFE）。在资源受限场景（如移动端部署、实时应用）中，31 NFE的采样成本可能构成瓶颈，需进一步探索蒸馏或更少步数的采样策略。

### 3. 局限与开放问题

**已识别的局限**（来自论文自身分析）：

1. **脚滑动问题**：尽管通过梯度均衡将脚滑动从基准的较高水平降至16.31%，仍显著高于使用3D关节坐标的MDM（8.58%）。这表明仅靠损失加权无法完全补偿SMPL表示在运动学约束表达上的固有不足。论文明确指出可能需要额外的运动学约束。

2. **自相交伪影**：渲染网格中偶尔出现肢体自相交，且该伪影也存在于训练数据中，暗示问题部分源于数据质量而非生成模型本身。

3. **楼梯运动高度漂移**：生成的楼梯行走序列在上升后有时无法保持高度，表明模型对长程物理一致性（重力、地面接触）的建模存在不足。

**开放研究问题**：

1. **脚滑动的根治方案**：能否在不引入3D关节坐标或辅助损失的前提下，通过在SMPL空间施加足部速度约束或接触一致性正则化来进一步降低脚滑动？这涉及表示空间选择与物理合理性之间的深层权衡。

2. **条件生成的迁移性**：梯度均衡策略是否能在文本到运动、动作到运动等条件场景中保持有效性？条件信号的引入可能改变各特征组的梯度动态，需重新验证 $u_\psi^k(t)$ 的学习行为。

3. **物理一致性的后处理**：自相交和高度漂移是否可通过物理模拟（如MuJoCo、SMPLify的接触约束）在后处理阶段纠正？这涉及生成质量与物理合理性的分解——是否应将物理约束显式嵌入生成过程而非依赖后处理？

4. **权重学习机制的充分性**：$u_\psi$ 是一个小型MLP，其容量是否足以捕捉时间步与特征组之间复杂的交互效应？在更长的运动序列或更多特征组场景下，是否需要更结构化的权重预测器（如注意力机制）？

5. **小样本与少轮次的鲁棒性**：当前消融实验基于600 epoch的充分训练。在小批量（如batch size < 32）或更少训练轮次下，$u_\psi$ 的估计方差增大，平衡策略是否仍能稳定收敛？这关系到方法在计算资源受限场景中的实用性。

6. **与其他生成范式的结合**：梯度均衡思想是否可推广至其他生成框架（如流匹配、一致性模型）？其核心在于识别并补偿损失景观中的各向异性，这一原理可能具有跨范式的适用性。

## 原文 PDF

![[paperPDFs/ICLR_2026/Unconditional_Human_Motion_and_Shape_Generation_via_Balanced_Score_Based_Diffusion.pdf]]
