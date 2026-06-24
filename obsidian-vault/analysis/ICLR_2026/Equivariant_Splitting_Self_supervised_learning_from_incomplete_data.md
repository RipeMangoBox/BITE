---
title: "Equivariant Splitting: Self-supervised learning from incomplete data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Equivariant_Splitting_Self_supervised_learning_from_incomplete_data.pdf
openreview_forum_id: upMIVpe467
aliases:
- ESE
- ESSSLFID
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将重建网络设计为满足新定义的等变重建器（f(y, A T_g) = T_g^{-1} f(y, A)），从而将等价分裂损失简化为普通分裂损失，同时利用变换不变性假设和测量分裂，保证全局极小点为MMSE估计器并消除显式变换开销。"
primary_logic: "通过定义适用于逆问题的重建网络等变性，等价分裂损失在等变网络下退化为无变换开销的普通分裂损失，且可证明在满秩条件下恢复MMSE最优估计。"
claims:
- "在无噪声且Q_{A_1}满秩时，分裂方法给出与监督方法相同的MMSE最优重建。"
- "若重建网络是等变重建器，则ES损失等价于普通分裂损失，消除变换计算。"
- "在图像修复、MRI和CT上，ES均显著优于EI等自监督基线，并接近监督水平。"
- "等变架构与分裂损失存在协同效应，使用等变网络可进一步提升性能。"
---

# Equivariant Splitting: Self-supervised learning from incomplete data

> [!tip] 核心洞察
> 通过定义适用于逆问题的重建网络等变性，等价分裂损失在等变网络下退化为无变换开销的普通分裂损失，且可证明在满秩条件下恢复MMSE最优估计。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 等变分裂：从不完整数据中进行自监督学习 |
| 英文题名 | Equivariant Splitting: Self-supervised learning from incomplete data |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=upMIVpe467); [GitHub](https://github.com/vsechaud/Equivariant-Splitting) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Equivariant Splitting (ES) |
| Dataset | Compressive Sensing (MNIST, 28×28, various m), Image Inpainting (DIV2K 128×128, ~70% missing), MRI (FastMRI, 320×320, ×8 accel., 40 dB SNR), Sparse-View CT (50 views, 50 dB SNR) |

> [!tip] 效果简介
> - Compressive Sensing (MNIST, 28×28, various m) 上，PSNR 为 close to supervised (see Figure 1 curve)，对比 EI significantly lower at high compression，变化 ES matches supervised; EI gap widens with compression。
> - Image Inpainting (DIV2K 128×128, ~70% missing) 上，PSNR / SSIM 为 27.45 ± 2.86 / 0.8737 ± 0.0461，对比 EI: 25.89 ± 2.65 / 0.8332 ± 0.0521，变化 +1.56 PSNR。
> - MRI (FastMRI, 320×320, ×8 accel., 40 dB SNR) 上，PSNR / SSIM 为 28.54 ± 2.75 / 0.7933 ± 0.0614，对比 EI: 27.88 ± 2.64 / 0.7750 ± 0.0604，变化 +0.66 PSNR。

## 概述

从不完整数据中学习重建是计算成像的核心难题。当前自监督方法面临一个根本性瓶颈：在仅有一个秩缺失前向算子的条件下，等变成像（Equivariant Imaging, EI）等现有方案计算开销大、可能不收敛到最小均方误差（MMSE）最优估计，而分裂方法又依赖多算子支持，难以直接用于单算子场景。

本文提出**等变分裂（Equivariant Splitting, ES）**，一种新的自监督逆问题学习方法。其核心思路是将重建网络设计为满足新定义的**等变重建器** $f(y, A T_g) = T_g^{-1} f(y, A)$，从而将等价分裂损失退化为普通分裂损失——既消除了显式变换的计算开销，又可在满秩条件下证明全局极小点即为 MMSE 估计器。这一设计将图像分布的变换不变性假设与测量分裂机制有机结合，实现了理论保证与计算效率的统一。

实验覆盖压缩感知、图像修复、MRI 重建和稀疏视角 CT 四个任务，ES 在所有任务上均显著优于 EI 等自监督基线，并接近全监督水平：修复任务 PSNR 提升 1.56 dB（27.45 vs 25.89），CT 任务提升 4.01 dB（32.62 vs 28.61），MRI 任务提升 0.66 dB（28.54 vs 27.88）。消融实验进一步证实，等变架构与分裂损失之间存在协同效应，且 ES 的训练效率接近监督学习，每个 epoch 耗时仅为 EI 的 1/4 到 1/3。

该方法的关键约束在于要求前向算子不与所选变换群等变，且推理时需对多个随机分裂求平均以近似加权 MMSE 估计。当噪声分布未知或图像分布严格违反不变性假设时，性能会有所退化，但这些限制为后续研究指明了方向。

## 背景与动机

### 逆问题中的不完全数据挑战

成像逆问题的核心是从不完整或退化的测量中恢复真实图像。前向模型可表述为：

$$\pmb{y} = \pmb{A} \pmb{x} + \pmb{\varepsilon}$$

其中 $\pmb{y}$ 为测量值，$\pmb{A}$ 为前向算子（如稀疏采样矩阵、Radon变换、傅里叶欠采样），$\pmb{x}$ 为真实图像，$\pmb{\varepsilon}$ 为噪声。当 $\pmb{A}$ 为单秩缺失算子时，测量空间存在零空间——即某些图像成分在测量中完全不可见，这使得从 $\pmb{y}$ 到 $\pmb{x}$ 的逆映射本质上是病态的。

监督学习方法通过大量配对数据 $(\pmb{x}, \pmb{y})$ 学习映射 $f(\pmb{y}, \pmb{A})$，最小化均方误差：

$$\mathcal{L}_{\mathrm{SUP}}(x, y, A, f) = \| f(y, A) - x \|^2$$

然而，在许多实际场景（如医学成像）中，获取高质量的真实图像 $\pmb{x}$ 代价高昂甚至不可行，这促使研究者转向自监督学习范式。

### 现有自监督方法的瓶颈

当前针对单秩缺失前向算子的自监督方法主要面临三类瓶颈：

**测量一致性方法的失效。** 基于测量一致性的方法（如MC/SURE）仅约束 $f(\pmb{y}, \pmb{A})$ 通过 $\pmb{A}$ 后与 $\pmb{y}$ 一致，但无法约束零空间内的成分。在MRI和CT等应用中，这类方法无法恢复缺失频率或缺失角度信息，重建结果严重退化。

**等变成像（EI）的计算与收敛局限。** EI方法通过引入等变正则项来约束零空间：

$$\mathscr{L}_{\mathrm{EI}}(y, A, f) = \| A f(y, A) - y \|^2 + \lambda \mathbb{E}_g \{ \| T_g f(y, A) - f(A T_g f(y, A), A) \|^2 \}$$

该损失利用图像分布对变换群 $\mathcal{G}$ 的不变性假设——$p(T_g x) = p(x), \forall g \in \mathcal{G}$——来提供零空间监督。然而，EI存在两个关键缺陷：**第一**，每个训练迭代需要2-3次网络前向传播以计算变换一致性项，计算开销显著；**第二**，EI不能保证收敛到最小均方误差（MMSE）最优估计器，在高压缩比下性能差距尤为明显。

**分裂方法的多算子依赖。** 测量分裂损失通过将测量和算子随机分割为两部分来构造自监督信号：

$$\mathcal{L}_{\mathrm{SPLIT}}(y, A, f) = \mathbb{E}_{y_1, A_1 \mid y, A} \{ \| A f(y_1, A_1) - y \|^2 \}$$

该方法在理论上可恢复MMSE最优估计（当分割后的子算子 $\pmb{Q}_{A_1}$ 满秩时），但其有效性依赖于**多个不同前向算子**的训练数据。在仅有单一前向算子的场景下，分裂方法无法直接应用——这是限制其实际部署的核心瓶颈。

### 本文的核心动机

上述瓶颈指向一个明确的研究缺口：**如何在单秩缺失前向算子的条件下，设计一种既具有MMSE最优性理论保证、又避免显式变换计算开销的自监督学习方法？**

本文的动机正是桥接这一缺口。核心思路是将等变成像中的变换不变性假设与分裂方法的测量分割机制相融合，但关键在于**改变等变性的实施方式**——不再通过额外的损失项来施加等变约束，而是将等变性直接嵌入重建网络的架构设计中。这需要重新定义逆问题背景下重建网络的等变性，并设计满足该性质的网络结构。若成功，则等变分裂损失可在理论上退化为无变换开销的普通分裂损失，同时保留MMSE最优性保证，实现计算效率与重建质量的双重提升。

## 核心创新

等变成像（Equivariant Imaging, EI）将变换不变性假设引入自监督逆问题学习，但其实现存在两个结构性瓶颈：**训练开销大**（每步需2–3次网络前向以显式计算等变正则项）且**无最优性保证**（EI损失函数的全局极小点未必对应MMSE估计器）。另一方面，测量分裂方法虽可恢复MMSE最优解，但依赖多算子场景，无法直接用于单秩缺失前向算子的情形。

Equivariant Splitting (ES) 的核心创新在于**将等变性从损失函数层面迁移到网络架构层面**，从而同时解决上述两个瓶颈。具体而言，ES 引入了三个关键设计：

**1. 等变重建器（Equivariant Reconstructor）的重新定义**

传统等变性定义要求网络满足 $f(T_g y, A) = T_g f(y, A)$，即对测量空间的变换等变。ES 重新定义了逆问题场景下的等变性：

$$f(\pmb{y}, \pmb{A} \pmb{T_g}) = \pmb{T_g^{-1}} f(\pmb{y}, \pmb{A})$$

即重建网络需对**前向算子**的变换等变，而非对测量的变换等变。这一定义使得等变性与测量分裂机制自然兼容：当输入算子从 $A$ 变为 $A T_g$ 时，网络输出应恰好是原输出的逆变换。该定义可通过平移等变 UNet（Chaman & Dokmanic, 2021b）或 Reynolds 组平均（式18）实现，无需修改训练损失。

**2. 等变分裂损失的退化性质**

ES 损失定义为对变换群求期望的分裂损失：

$$\mathcal{L}_{\mathrm{ES}}(y, A, f) \triangleq \mathbb{E}_g \{ \mathcal{L}_{\mathrm{SPLIT}}(y, A T_g, f) \}$$

**定理3**证明：若 $f$ 是等变重建器，则 ES 损失等价于普通分裂损失：

$$\mathcal{L}_{\mathrm{ES}}(y, A, f) = \mathcal{L}_{\mathrm{SPLIT}}(y, A, f)$$

这意味着 ES 在训练时**完全消除了显式的变换计算开销**——等变性由架构内建保证，损失函数仅需计算分裂损失。与 EI 相比，ES 每 epoch 训练时间缩短 2–4 倍（修复任务：12 s vs 58 s；MRI：19 s vs 75 s），效率接近监督学习。

**3. 全局最优性保证**

**定理1** 证明：在无噪声且分裂子矩阵 $Q_{A_1}$ 满秩的条件下，分裂损失的全局极小点即为 MMSE 最优估计器 $f^*(y_1, A_1) = \mathbb{E}_{x|y_1, A_1}\{x\}$。这一保证是 EI 所不具备的——EI 的等变正则项仅作为软约束，无法确保收敛到 MMSE 解。ES 通过将等变性硬编码到架构中，使分裂损失的理论保证得以完整保留。

**与 EI 的关键差异总结**

| 维度 | EI | ES |
|------|-----|-----|
| 等变性实现 | 损失函数中的显式正则项 | 网络架构内建 |
| 训练开销 | 每步 2–3 次前向 | 每步 1 次前向 |
| 最优性保证 | 无 | 满秩条件下恢复 MMSE |
| 变换计算 | 训练时显式计算 $T_g$ | 训练时零变换开销 |

实证上，等变架构与分裂损失之间存在**协同效应**：使用等变架构训练的分裂方法在 PSNR、SSIM 和等变度量上均优于非等变架构（Table 3），验证了理论设计在实际中的有效性。

## 整体框架

Equivariant Splitting (ES) 的核心思想是将测量分裂（measurement splitting）与变换不变性假设相结合，构建一个无需配对标定的自监督逆问题求解框架。其整体 pipeline 由训练与推理两个阶段构成，二者共享同一重建网络，但数据流和损失计算方式不同。

### 训练阶段

训练阶段的目标是最小化 ES 损失，该损失在等变重建器条件下等价于普通的测量分裂损失。具体流程如下：

1. **测量分裂**：对于每个训练样本，随机生成一个分裂掩码 $M$，将完整测量 $y$ 和对应的前向算子 $A$ 沿测量维度拆分为两部分：
   - 输入部分：$y_1 = M y$，$A_1 = M A$
   - 目标部分：完整的原始测量 $y$（作为预测目标）
   
2. **投影/反投影**：将分裂后的测量 $y_1$ 通过前向算子的伴随或伪逆映射回图像空间，作为重建网络的输入。这一步构成 artifact removal 重建器（式16）的前端。

3. **等变重建器**：网络 $f(y_1, A_1)$ 接收投影后的图像特征和算子信息，输出重建图像 $\hat{x}$。重建器需满足等变性定义：
   $$f(y, A T_g) = T_g^{-1} f(y, A)$$
   这意味着对前向算子施加变换 $T_g$ 后，重建结果应通过逆变换恢复。等变性通过以下方式实现：
   - **平移等变**：使用平移等变 UNet 作为去噪骨干（Chaman & Dokmanic, 2021b）
   - **旋转/反射等变**：通过 Reynolds 平均将非等变去噪器强制等变化：
     $$\phi(x) = \frac{1}{|\mathcal{G}|} \sum_{g \in \mathcal{G}} T_g^{-1} \psi(T_g x)$$
     或对整体重建函数做组平均（式18）

4. **损失计算**：ES 损失定义为对变换群求期望的分裂损失：
   $$\mathcal{L}_{\mathrm{ES}}(y, A, f) = \mathbb{E}_g \{ \mathcal{L}_{\mathrm{SPLIT}}(y, A T_g, f) \}$$
   其中普通分裂损失为：
   $$\mathcal{L}_{\mathrm{SPLIT}}(y, A, f) = \mathbb{E}_{y_1, A_1 \mid y, A} \{ \| A f(y_1, A_1) - y \|^2 \}$$
   关键定理（Theorem 3）保证：当 $f$ 是等变重建器时，ES 损失等价于普通分裂损失，即 $\mathcal{L}_{\mathrm{ES}} = \mathcal{L}_{\mathrm{SPLIT}}$。这意味着**显式的变换计算被消除**，训练时无需对每个变换 $g$ 做多次网络前向。

5. **最优性保证**：在无噪声且分裂后的部分前向算子 $Q_{A_1}$ 满秩的条件下，Theorem 1 证明分裂方法的全局极小点即为 MMSE 最优估计器：$f^*(y_1, A_1) = \mathbb{E}_{x|y_1, A_1}\{x\}$，与监督学习的理论最优解一致。

### 推理阶段

推理时不再计算损失，而是通过多次随机分裂聚合来近似加权 MMSE 估计（Proposition 1）：

1. 对同一组测量 $(y, A)$，执行 $J$ 次随机分裂（默认 $J=10$），每次生成不同的 $(y_1^{(j)}, A_1^{(j)})$。
2. 对每次分裂独立运行重建网络，得到 $\hat{x}_j = f(y_1^{(j)}, A_1^{(j)})$。
3. 对所有重建结果取平均：$\hat{x} = \frac{1}{J} \sum_j \hat{x}_j$。

这种多分裂聚合策略在理论上近似了对不同分裂方式的期望，提升了重建的稳定性和质量。

### 模块关系总结

整个框架的核心模块及其依赖关系如下：

| 模块 | 角色 | 关键约束 |
|------|------|----------|
| 随机分裂掩码 $M$ | 将测量/算子拆分为输入和目标 | 需保证 $Q_{A_1}$ 满秩（Theorem 1 前提） |
| 投影（伴随/伪逆） | 测量域→图像域映射 | 无特殊约束 |
| 等变重建器 $f$ | 从分裂测量重建图像 | 必须满足 $f(y, A T_g) = T_g^{-1} f(y, A)$ |
| 变换群 $\mathcal{G}$ | 提供不变性先验 | 前向算子 $A$ 不得与所选变换等变（Corollary 1） |
| 多分裂聚合 | 推理时平均多个分裂结果 | $J$ 越大越接近理论加权估计 |

### 与 EI 的关键差异

与 Equivariant Imaging (EI) 相比，ES 在框架设计上有两个根本性改进：

- **等变性实现方式**：EI 通过损失函数中的显式正则项 $\lambda \mathbb{E}_g \{ \| T_g f(y, A) - f(A T_g f(y, A), A) \|^2 \}$ 来促进等变性，每次迭代需要 2-3 次网络前向；ES 将等变性直接编码进网络架构，消除了显式变换开销。
- **最优性保证**：EI 不保证收敛到 MMSE 估计器；ES 在满秩条件下有严格的 MMSE 最优性证明（Theorem 1）。

### 适用条件与限制

框架的有效性依赖于以下关键假设：

1. **分布不变性**（Assumption 1）：真实图像分布 $p(x)$ 对变换群 $\mathcal{G}$ 不变，即 $p(T_g x) = p(x)$。
2. **算子非等变性**（Corollary 1）：前向算子 $A$ 不得与所选变换群等变。若违反此条件（如均匀间隔的 push-broom 掩码），ES 无法学到零空间之外的信息，性能会大幅下降（Table 7 中均匀掩码 ES 降至 21.94 PSNR vs 随机掩码 23.04 PSNR）。
3. **满秩条件**：Theorem 1 要求分裂后的部分算子 $Q_{A_1}$ 满秩；当条件数很大时实际恢复质量可能下降，需进一步验证。

整个 pipeline 的伪代码详见 Algorithm 1（训练）和 Algorithm 2（推理），具体架构细节（artifact removal、unrolled MoDL、Reynolds 平均）在 Appendix A.1 中展开。

## 核心模块与公式推导

### 逆问题前向模型

ES 方法建立在标准线性逆问题模型之上：

$$ \pmb{y} = \pmb{A} \pmb{x} + \pmb{\varepsilon} \tag{1} $$

其中 $\pmb{y} \in \mathbb{R}^m$ 为测量值，$\pmb{A} \in \mathbb{R}^{m \times n}$ 为前向算子（$m \leq n$），$\pmb{x} \in \mathbb{R}^n$ 为真实图像，$\pmb{\varepsilon}$ 为加性噪声。当 $m < n$ 时，问题为不适定逆问题，$\pmb{A}$ 存在非平凡零空间，仅靠测量一致性无法唯一确定重建结果。

### 核心假设：图像分布的不变性

ES 的理论基础是真实图像分布对某一变换群 $\mathcal{G}$ 的不变性：

$$ p(T_g x) = p(x), \quad \forall g \in \mathcal{G}, \forall x \in \mathbb{R}^n \tag{5} $$

其中 $\{T_g\}_{g \in \mathcal{G}}$ 是一组酉变换（如平移、旋转、翻转）。该假设是等变成像（EI）和等变分裂（ES）共同的前提，为从单秩缺失算子中学习零空间信息提供了约束。

### 测量分裂损失

分裂方法的核心思想是将测量和算子随机分为两部分，训练网络从一部分预测全部测量：

$$ \mathcal{L}_{\mathrm{SPLIT}}(y, A, f) = \mathbb{E}_{y_1, A_1 \mid y, A} \left\{ \| A f(y_1, A_1) - y \|^2 \right\} \tag{3} $$

其中 $y_1 = M y$，$A_1 = M A$，$M \in \mathbb{R}^{m_1 \times m}$ 为随机分裂掩码。该损失不依赖真实图像 $x$，仅需测量数据即可训练。**定理 1** 证明：在无噪声且 $Q_{A_1}$（$A_1$ 的行空间投影）满秩的条件下，分裂方法的全局极小点给出与监督学习相同的 MMSE 最优估计，即 $f^*(y_1, A_1) = \mathbb{E}_{x|y_1, A_1}\{x\}$。

### 等变分裂损失

ES 将分裂损失与变换不变性结合，对变换后的前向算子求期望：

$$ \mathcal{L}_{\mathrm{ES}}(y, A, f) \triangleq \mathbb{E}_g \left\{ \mathcal{L}_{\mathrm{SPLIT}}(y, A T_g, f) \right\} \tag{7} $$

直观上，ES 通过变换 $T_g$ 扰动前向算子 $A$，使网络在不同"视角"下学习重建，从而隐式地利用不变性约束零空间。

### 等变重建器：消除显式变换开销的关键

ES 的核心创新在于将等变性直接嵌入网络架构，而非作为损失项。**定义 1** 给出了适用于逆问题的等变重建器：

$$ f(\pmb{y}, \pmb{A} \pmb{T_g}) = \pmb{T_g^{-1}} f(\pmb{y}, \pmb{A}) \tag{15} $$

该定义表明：若前向算子经 $T_g$ 变换，重建结果应等价于先重建再逆变换。这与标准图像等变性不同——此处变换作用于算子而非图像。

**定理 3** 证明：若 $f$ 是等变重建器，则 ES 损失退化为普通分裂损失：

$$ \mathcal{L}_{\mathrm{ES}}(y, A, f) = \mathcal{L}_{\mathrm{SPLIT}}(y, A, f) \tag{21} $$

这一等价性消除了 ES 损失中对变换的显式期望计算，使训练效率接近监督学习（修复任务中 ES 每 epoch 约 12 秒，EI 约 58 秒）。

### 等变架构构建

论文提供两种构建等变重建器的途径：

**1. 平移等变 UNet 去噪器**：在 artifact removal 架构中，投影步骤后接平移等变 UNet，使整体重建器满足平移等变性。

**2. Reynolds 平均**：对任意非等变重建函数 $r(y, A)$，通过有限群上的平均强制等变性：

$$ f(\pmb{y}, \pmb{A}) = \frac{1}{|\mathcal{G}|} \sum_{g \in \mathcal{G}} \pmb{T}_g \, r(\pmb{y}, \pmb{A} \pmb{T}_g) \tag{18} $$

同理，对非等变去噪器 $\psi$ 也可用 Reynolds 平均获得等变版本，用于 MRI 和 CT 中的旋转/翻转群。

### 噪声场景扩展

对于含噪测量，ES 损失扩展为：

$$ \mathcal{L}_{\mathrm{ES}}^{\mathrm{noisy}}(y, A, f) = \mathbb{E}_{g, y_1, A_1 \mid y, A T_g} \left\{ \| A T_g f(y_1, A_1) - y \|^2 \right\} $$

当噪声分布已知时，可进一步引入噪声自适应加权。若噪声分布未知，ES 仍可在无噪声假设下运行，实验表明在低 SNR 下仍优于同等条件下的 EI 变体。

### 推理时的多分裂聚合

推理阶段，ES 对多个随机分裂（$J=10$）的重建结果取平均，以近似加权 MMSE 估计：

$$ \hat{x} = \frac{1}{J} \sum_{j=1}^{J} f(y_1^{(j)}, A_1^{(j)}) $$

该过程与训练时分裂策略一致，不引入额外模型或变换计算。

## 实验与分析

### 瓶颈验证：ES 在多个逆问题任务上一致优于自监督基线

ES 的核心主张——将等变性内化于架构从而消除显式变换开销、并借助分裂损失恢复 MMSE 最优估计——在压缩感知、图像修复、MRI 和稀疏 CT 四个不同任务上得到了一致验证。

**压缩感知**（Figure 1）：在 MNIST 28×28 压缩感知任务中，ES 的 PSNR 曲线在全压缩率范围（50%–90%）内紧贴监督学习基线，而 EI 基线的性能差距随压缩率增加而急剧扩大。这表明 ES 的分裂机制在高压缩下仍能有效利用测量中的零空间信息，而 EI 的等变正则项无法弥补这一信息缺口。


![[assets/figures/papers/iclr26_0009_upMIVpe467_Equivariant_Splitting_Self-supervised_learning_f/figures/001_Figure_1.jpg]]
*Figure 1: Compressive sensing results. ES (ours) performs similarly as the supervised baseline, unlike EI (baseline) whose performance gap widens with higher compression levels*

**图像修复**（Table 1, Figure 2）：在 DIV2K 128×128 图像修复（约 70% 缺失像素）上，ES 达到 PSNR 27.45 ± 2.86 dB、SSIM 0.8737 ± 0.0461，分别比 EI 的 25.89 ± 2.65 dB 和 0.8332 ± 0.0521 提升 +1.56 dB 和 +0.04。定性重建（Figure 2）中，EI 输出明显模糊，而 ES 在感知上更接近监督基线。值得注意的是，ES 的等变度量 EQUIV 也达到 27.46 dB，显著高于 EI 的 25.90 dB，说明等变架构与分裂损失的协同效应不仅提升重建质量，也强化了网络的等变一致性。


![[assets/figures/papers/iclr26_0009_upMIVpe467_Equivariant_Splitting_Self-supervised_learning_f/figures/007_Table_1.jpg]]
*Table 1: Inpainting results. ES (ours) performs better than EI (baseline), both in terms of reconstruction quality (PSNR, SSIM) and measured equivariance (EQUIV), while performing competitively against the supervised baseline. In bold, the best self-supervised metrics ( $\mathrm { a v g } \pm \mathrm { s t . d . }$ )

**医学成像**（Table 2, Figure 3）：在 FastMRI 膝关节 MRI（×8 加速，40 dB SNR）和稀疏 CT（50 视角，50 dB SNR）两个任务上，ES 均大幅领先所有自监督基线。MRI 上 ES 的 PSNR 为 28.54 ± 2.75 dB，比 EI（27.88 ± 2.64 dB）高 +0.66 dB，比 SURE（24.45 dB）和 IDFT（23.62 dB）的优势更为显著。CT 上 ES 达到 32.62 ± 2.16 dB，比 EI 的 28.61 ± 1.28 dB 提升 +4.01 dB，接近监督学习的 33.99 ± 2.48 dB。定性结果（Figure 3）显示，EI 重建存在明显的点状伪影，而 ES 输出更干净。


![[assets/figures/papers/iclr26_0009_upMIVpe467_Equivariant_Splitting_Self-supervised_learning_f/figures/014_Table_2.jpg]]
*Table 2: Medical imaging results. ES (ours) performs better than EI, SURE and MC (baselines), while performing almost as well as the supervised baseline in reconstruction quality (PSNR, SSIM) and measured equivariance (EQUIV). In bold, the best self-supervised metrics ( $\mathrm { a v g } \pm \mathrm { s t . d . }$ )

**噪声主导场景**（Table 5, Table 6）：在 MRI ×6 加速、10 dB SNR 的强噪声条件下，ES 仍保持 27.39 ± 2.44 dB，优于 EI 的 26.02 ± 1.65 dB（+1.37 dB），验证了方法对噪声的鲁棒性。


![[assets/figures/papers/iclr26_0009_upMIVpe467_Equivariant_Splitting_Self-supervised_learning_f/figures/022_Table_6.jpg]]
*Table 6: Extended results on the impact of equivariant architectures. Adds to Table 3 the results for EI with a non-equivariant architecture for the inpainting task, results for the noise-dominated MRI task. In bold, the best self-supervised metrics. Values: avg ± st.d*

### 关键消融：等变架构与分裂损失的协同效应

Table 3 和 Table 6 系统消融了等变架构的作用。在图像修复和 MRI 任务上，使用等变架构（平移等变 UNet 或旋转/翻转 Reynold 平均）的分裂训练始终比非等变架构获得更高的 PSNR、SSIM 和 EQUIV。例如，修复任务中等变架构的分裂损失 PSNR 为 27.45 dB，非等变架构为 27.20 dB；MRI（×8）中等变架构达 28.54 dB，非等变架构为 28.36 dB。这一协同效应直接验证了 Theorem 3 的理论预期：等变重建器使 ES 损失退化为普通分裂损失，消除了变换带来的额外方差。


![[assets/figures/papers/iclr26_0009_upMIVpe467_Equivariant_Splitting_Self-supervised_learning_f/figures/015_Table_3.jpg]]
*Table 3: Impact of using equivariant architectures. In accordance with the theoretical results described in Section 4, there is a synergy between the splitting loss and equivariant architectures resulting in higher performance. Non-equivariant models have surprisingly high equivariance measures (EQUIV) which might explain their high performance when using the splitting loss. Eq. arch. denotes whether the architecture is equivariant. In bold, the best self-supervised metrics (avg ± st.d.)*

Figure 8 的训练过程演化曲线进一步表明，分裂方法的优势与架构选择无关——无论是否使用等变架构，分裂损失训练的模型在训练全程始终优于对应的 EI 变体，且收敛速度更快。


![[assets/figures/papers/iclr26_0009_upMIVpe467_Equivariant_Splitting_Self-supervised_learning_f/figures/030_Figure_8.jpg]]
*Figure 8: Performance evolution during training for inpainting. Splitting methods perform better than EI independent of the network architecture*

### 失败模式与边界条件

**算子-变换等变性的破坏**（Table 7, Corollary 1）：当所选变换群使前向算子近似等变时，ES 性能急剧退化。在推扫式掩码修复实验中，均匀间隔掩码（近似平移等变）下 ES 的 PSNR 降至 21.94 dB，远低于随机掩码的 23.04 dB。这实证验证了 Corollary 1 的警告：若 $A T_g \approx T_g A$，变换无法向零空间注入新信息，ES 退化为无效。

**未知噪声分布的退化**（Table 8）：当噪声分布未知、采用无噪声假设的 ES 变体时，性能出现明显下降。修复任务中 PSNR 从 27.45 dB 降至 26.08 dB（-1.37 dB），噪声主导 MRI（×6, 10 dB）中从 27.39 dB 降至 24.80 dB（-2.59 dB）。尽管如此，ES 的未知噪声变体在所有场景下仍优于同等条件下的 EI 变体，表明分裂机制本身对噪声模型失配具有一定容忍度。

**推理时的多分裂平均开销**：ES 在推理时需对 J=10 个随机分裂求平均以近似加权 MMSE 估计，这引入了额外的计算成本。但 Table 10 显示，ES 的训练效率远优于 EI——修复任务上 ES 每 epoch 仅需 12 秒（EI 需 58 秒），MRI 上 ES 需 19 秒（EI 需 75 秒），训练总时长优势约为 2–4 倍。

### 重要图表结论摘要

- **Figure 1**：ES 在全压缩率范围匹配监督性能，EI 在高压缩下显著退化。
- **Table 1 & Figure 2**：ES 在修复任务上 PSNR +1.56 dB，定性上更清晰、模糊更少。
- **Table 2 & Figure 3**：ES 在 MRI 和 CT 上分别领先 EI +0.66 dB 和 +4.01 dB，EI 存在明显伪影。
- **Table 3 & Table 6**：等变架构与分裂损失存在正向协同，等变架构持续提升 PSNR/SSIM/EQUIV。
- **Table 7**：均匀掩码（近似等变）使 ES 失效，验证 Corollary 1 的边界条件。
- **Figure 8**：分裂方法在训练全程优于 EI，与架构选择无关。
- **Table 8**：未知噪声下 ES 仍优于 EI，但绝对性能下降，需注意噪声建模假设。

## 方法谱系与知识库定位

### 与现有自监督逆问题方法的关系

ES 的方法学根植于两条独立的自监督学习线路：**测量分裂** 与 **等变成像**，并将二者在单秩缺失前向算子的约束下统一。

**测量分裂方法** 依赖多个独立或可拆分的测量算子来构造训练信号。其核心损失为

$$\mathcal{L}_{\mathrm{SPLIT}}(y, A, f) = \mathbb{E}_{y_1, A_1 \mid y, A} \{ \| A f(y_1, A_1) - y \|^2 \},$$

即从部分测量 $y_1$ 和对应子算子 $A_1$ 重建后，用完整算子 $A$ 投影回完整测量 $y$ 并计算一致性。该方法在 $Q_{A_1}$ 满秩时可由 Theorem 1 保证全局极小点恢复 MMSE 最优估计，但其直接应用要求存在多个不同的前向算子，在单算子场景下无法直接工作。

**等变成像** 则利用图像分布对变换群 $G$ 的不变性假设 $p(T_g x) = p(x)$ 来约束零空间，损失函数为

$$\mathscr{L}_{\mathrm{EI}}(y, A, f) = \| A f(y, A) - y \|^2 + \lambda \mathbb{E}_g \{ \| T_g f(y, A) - f(A T_g f(y, A), A) \|^2 \}.$$

该损失包含测量一致性项和等变正则项，每步迭代需 2–3 次网络前向传播以计算变换下的等变惩罚。EI 可在单算子条件下工作，但不保证收敛到 MMSE 估计器，且在高压缩比下性能退化显著。

**ES 的整合逻辑** 是将 EI 中的变换不变性假设“注入”分裂框架，通过重新定义逆问题中的网络等变性来消除显式变换开销。具体而言，ES 损失定义为对变换求期望的分裂损失：

$$\mathcal{L}_{\mathrm{ES}}(y, A, f) \triangleq \mathbb{E}_g \{ \mathcal{L}_{\mathrm{SPLIT}}(y, A T_g, f) \}.$$

当重建网络满足等变重建器条件 $f(y, A T_g) = T_g^{-1} f(y, A)$ 时，Theorem 3 证明 ES 损失退化为普通分裂损失 $\mathcal{L}_{\mathrm{ES}} = \mathcal{L}_{\mathrm{SPLIT}}$，从而继承分裂方法在满秩条件下的 MMSE 最优性保证，同时消除 EI 中显式变换计算带来的额外开销。

**与测量一致性方法的对比**：MC/SURE 类方法仅依赖测量域一致性，在算子零空间内完全无约束，因此在 MRI 欠采样等任务中严重失效（Table 2 中 SURE 的 PSNR 仅为 24.45 dB，远低于 ES 的 28.54 dB）。ES 通过变换不变性假设有效约束了零空间，克服了这一根本缺陷。

### 适用边界与必要条件

ES 的有效性依赖三个关键前提，违反任一项均可能导致性能退化或方法失效：

1. **算子非等变性**：Corollary 1 要求所选变换群 $G$ 不与前向算子 $A$ 等变，即 $A T_g \neq T_g A$。若该条件不满足，变换后的算子 $A T_g$ 不引入新的测量信息，ES 退化为无零空间约束的普通分裂方法。Table 7 的推扫式掩码修复实验提供了实证：均匀间隔掩码（近似等变）下 ES 的 PSNR 从随机掩码的 23.04 dB 骤降至 21.94 dB，验证了算子不等变性的必要性。

2. **图像分布的不变性假设**：Assumption 1 要求 $p(T_g x) = p(x)$。该假设在自然图像中近似成立（平移不变性），在医学图像中虽非严格成立但近似有效——Table 2 中 MRI 和 CT 结果证明了这一点。然而，极端违反该假设时（如具有强方向性偏好的特定解剖结构），ES 的理论保证可能松动。

3. **子算子满秩条件**：Theorem 1 的 MMSE 最优性要求 $Q_{A_1}$（由分裂得到的子算子相关矩阵）满秩。当条件数很大时，实际恢复质量如何仍是一个开放问题，当前工作未提供该场景下的系统分析。

### 已知局限

1. **架构约束**：等变架构需要预先设计——平移等变 UNet 或通过 Reynolds 平均实现旋转/翻转等变。这限制了网络架构的灵活性，尤其在需要适配新型变换群时。

2. **噪声分布未知时的退化**：当测量噪声分布未知时，无噪声假设的 ES 变体性能会下降。Table 8 显示，在低 SNR 条件下（MRI ×6 加速，10 dB SNR），ES（未知噪声）的 PSNR 为 27.39 dB，虽仍优于 EI 的 26.02 dB，但绝对性能明显低于已知噪声分布的场景。

3. **推理计算开销**：推理时需对多个随机分裂（$J=10$）求平均以近似 Proposition 1 中的加权 MMSE 估计，带来 $J$ 倍的前向传播开销。虽然训练效率接近监督学习（Table 10：修复任务 ES 12 s/epoch vs EI 58 s/epoch），推理阶段的多次分裂平均仍是实际部署中的考虑因素。

4. **变换群的选择依赖**：Table 4 提供了根据算子等变性选择变换的决策表，但该选择目前依赖人工判断。对于复杂或非标准的前向算子，如何自动确定合适的变换群仍无系统方案。

### 开放问题

1. **近似不满秩条件下的行为**：当 $Q_{A_1}$ 条件数很大时，分裂方法的实际恢复质量尚未被系统研究。是否需要引入正则化手段来稳定训练，是一个具有实践价值的问题。

2. **连续变换群与非群变换的推广**：当前框架基于有限群，能否扩展到连续群（如任意角度旋转）或非群变换（如弹性变形），并设计相应的等变架构，是理论层面的自然延伸。

3. **真实采集场景的适应性**：真实 MRI 采集中存在生理运动、多线圈灵敏度差异等因素，会破坏严格的等变假设。ES 能否通过架构调整（如运动补偿模块）或数据增强来适应这些场景，尚待验证。

4. **非线性前向模型与复杂噪声的扩展**：当前理论和实验均基于线性前向模型和加性高斯噪声。扩展到非线性模型（如相位检索）或其他噪声分布（泊松噪声、Rician 噪声）并保持理论保证，是一个重要方向。

5. **极低测量率下的性能边界**：在极端欠采样条件下，能否结合生成先验或扩散模型进一步提升性能，同时维持 ES 的自监督特性，值得探索。Figure 1 的压缩感知曲线显示 ES 在极低测量率下仍接近监督水平，但该结论的泛化边界尚不明确。

## 原文 PDF

![[paperPDFs/ICLR_2026/Equivariant_Splitting_Self_supervised_learning_from_incomplete_data.pdf]]
