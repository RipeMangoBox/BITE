---
title: "MDM: Human Motion Diffusion Model"
type: paper
paper_level: A
venue: ICLR
year: 2023
pdf_ref: paperPDFs/ICLR_2023/MDM_Human_Motion_Diffusion_Model.pdf
aliases:
- MDMM
- MDM
tags:
- ICLR_2023
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "将扩散模型预测目标从噪声改为原始信号，从而可以直接应用几何损失（位置、速度、脚接触）来约束运动生成。"
primary_logic: "通过在扩散生成过程中预测干净样本而非噪声，并结合运动学几何损失（位置、速度、脚接触），MDM在保持轻量级的同时，能生成高质量、高多样性且可控的人体运动，实现多任务（文本/动作/无约束）的统一框架。"
claims:
- "MDM在文本到运动任务中，在HumanML3D和KIT基准上实现了最先进的FID、多样性和多模态性。"
- "在用户研究中，42.3%的情况下评估者偏好MDM生成的运动超过真实运动。"
- "MDM在动作到运动基准HumanAct12和UESTC上优于现有最先进方法。"
- "预测信号而非噪声使得应用几何损失成为可能，这些损失对运动质量至关重要。"
---

# MDM: Human Motion Diffusion Model

> [!tip] 核心洞察
> 通过在扩散生成过程中预测干净样本而非噪声，并结合运动学几何损失（位置、速度、脚接触），MDM在保持轻量级的同时，能生成高质量、高多样性且可控的人体运动，实现多任务（文本/动作/无约束）的统一框架。

| 字段 | 内容 |
|------|------|
| 中文题名 | MDM：人体运动扩散模型 |
| 英文题名 | MDM: Human Motion Diffusion Model |
| 会议/期刊 | ICLR 2023 |
| Links | [paper](https://arxiv.org/abs/2209.14916) · [GitHub](https://github.com/GuyTevet/motion-diffusion-model); [Project](https://guytevet.github.io/mdm-page/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | Motion Diffusion Model (MDM) |
| Dataset | HumanML3D, KIT, HumanAct12 |

> [!tip] 效果简介
> - HumanML3D 上，FID 为 0.544 (Table 1, transformer encoder)，对比 T2M (previous SOTA)，变化 显著降低（更好）。
> - KIT 上，FID 为 见表2中的SOTA结果，对比 其他竞争方法，变化 达到最佳。
> - HumanAct12 上，FID_train 为 0.100，对比 前任最佳（INR等），变化 显著更优。

## 概述

人体运动生成面临一个核心瓶颈：现有方法要么生成质量低、表现力受限（如基于VAE的方法假设正态分布），要么使用扩散模型时计算资源消耗大且难以有效控制生成质量。MDM（Human Motion Diffusion Model）通过一个关键洞察解决了这一问题——将扩散模型的预测目标从噪声改为原始干净信号，从而可以直接施加几何损失（位置、速度、脚接触）来约束运动生成。

在方法定位上，MDM属于**基于扩散的轻量级生成框架**，采用Transformer编码器骨干网络替代传统的U-Net，结合无分类器引导（classifier-free guidance）实现文本、动作等多条件统一控制。与需要外部分类器或分离模型的方案不同，MDM通过预测信号本身，使几何约束自然地融入扩散训练过程，在保持模型轻量的同时显著提升运动质量。

实验结果表明，MDM在多个基准上实现了全面领先：

- **文本到运动**：在HumanML3D和KIT数据集上达到最先进的FID、多样性和多模态性（Table 1, Table 2），用户研究中42.3%的情况下评估者偏好MDM生成的运动超过真实运动（Figure 4a）。
- **动作到运动**：在HumanAct12和UESTC基准上显著优于现有方法，FID和准确率均取得最佳（Table 3, Table 4）。
- **统一框架**：同一模型架构支持无约束生成、文本条件、动作条件及运动编辑（时间插值、身体部位编辑）等多任务，无需为每种条件设计独立模型。

MDM的训练仅需单块NVIDIA RTX 2080 Ti约三天，推理时约1分钟生成一个样本，在资源效率和生成质量之间取得了实用平衡。其核心贡献在于证明了“预测信号+几何损失”的范式能够有效替代传统扩散模型中的噪声预测，为可控运动生成开辟了新路径。

## 背景与动机

### 人体运动生成的核心挑战

人体运动生成是计算机视觉与图形学中长期存在的难题，其本质上是一个高度非确定性的映射问题：一段文本描述（如“一个人向前走并挥手”）可以对应无数种合理的运动序列，反之亦然。这种“多对多”的特性要求生成模型不仅要输出高质量、物理上合理的运动，还必须能够捕捉真实运动分布的丰富多样性。

然而，现有方法在这两个维度上始终难以兼得。基于变分自编码器（VAE）的方法，如 **T2M**（Guo et al., CVPR 2022）和 **TEMOS**（Petrovich et al., ECCV 2022），虽然推理速度快，但其核心假设——将运动分布建模为正态分布——本质上限制了模型的表现力，导致生成的运动趋于平均化、多样性不足。另一方面，扩散模型在图像生成领域已展现出强大的分布建模能力，但将其直接移植到运动生成时面临两个关键障碍：**（1）资源消耗巨大**，标准扩散模型通常需要庞大的 U-Net 骨干网络和上千步迭代；**（2）控制机制缺失**，传统扩散模型预测噪声而非干净信号，使得施加运动学约束（如关节位置准确性、脚部接触、速度平滑性）变得困难，而这些约束对生成物理上可信的人体运动至关重要。

### 现有方法的结构性缺口

具体而言，该领域存在以下结构性缺口：

1. **质量与多样性的权衡**：VAE 类方法受限于隐空间的正态假设，生成质量有限；而现有扩散模型虽能提升多样性，却因架构笨重和缺乏几何约束而难以保证运动质量。
2. **多任务统一框架的缺失**：文本到运动、动作到运动、无约束生成等任务通常需要分别设计专用模型，缺乏一个轻量且统一的框架来同时支持多种条件模态。
3. **可控编辑能力的匮乏**：大多数方法仅支持从零生成，无法对已有运动序列进行时间插值或特定身体部位的语义编辑。

### 本文动机

针对上述缺口，本文提出 **Motion Diffusion Model (MDM)**，核心动机在于：**通过重新设计扩散模型的预测目标和训练约束，在保持轻量级架构的同时，实现高质量、高多样性且可控的人体运动生成**。

具体而言，MDM 做出两个关键决策：
- **预测目标从噪声转向干净样本 $\hat{x}_0$**：这使得在训练过程中可以直接施加显式的几何损失函数（位置损失 $\mathcal{L}_{\text{pos}}$、速度损失 $\mathcal{L}_{\text{vel}}$、脚接触损失 $\mathcal{L}_{\text{foot}}$），从而将运动学的物理先验注入扩散过程。
- **采用轻量级 Transformer 编码器骨干**：相比图像扩散模型中常用的 U-Net，Transformer 更适配人体运动这种时序非空间数据，且参数效率更高（单块 RTX 2080 Ti 训练约 3 天）。

通过这一设计，MDM 旨在以一个统一框架覆盖文本到运动、动作到运动和无约束生成三大任务，并原生支持基于扩散修复的运动编辑，弥合现有方法在质量、多样性与可控性之间的鸿沟。

## 核心创新

MDM的核心创新在于对扩散模型生成范式的两个关键改造，使其能够以轻量级架构生成高质量、可控的人体运动。

### 1. 预测目标从噪声转向干净样本

标准扩散模型在每一步去噪过程中预测噪声分量 $\epsilon$，而MDM直接预测干净样本 $\hat{x}_0$（见公式 (2)）。这一转变并非简单的形式变化，而是解锁了在扩散框架内直接施加运动学约束的可能性——因为模型输出是可直接解读的运动表示，而非抽象的噪声残差。

**预测目标的因果链路**：
- 预测 $\hat{x}_0$ → 输出端暴露为原始运动表示 → 可以计算位置、速度等几何量 → 施加显式运动学损失
- 若预测噪声 $\epsilon$，则无法在训练过程中对生成的“运动”施加有物理含义的约束

### 2. 显式几何损失约束运动质量

基于上述设计，MDM引入了三类几何损失函数，直接约束生成运动的物理合理性：

| 损失函数 | 公式 | 作用机制 |
|---------|------|---------|
| 位置损失 $\mathcal{L}_{\mathrm{pos}}$ | 公式 (3) | 通过前向运动学（FK）计算关节点位置，约束预测运动与真实运动在三维空间中的位置一致性 |
| 速度损失 $\mathcal{L}_{\mathrm{vel}}$ | 公式 (5) | 约束相邻帧间关节速度的一致性，保证运动的时间平滑性 |
| 脚接触损失 $\mathcal{L}_{\mathrm{foot}}$ | 公式 (4) | 利用二进制接触掩码 $f_i$，在脚部着地时约束其速度趋近于零，有效减少脚部滑动伪影 |

这三类损失以加权形式与简单损失 $\mathcal{L}_{\mathrm{simple}}$ 结合（公式 (6)），形成总训练目标。消融实验表明，几何损失对运动质量的提升至关重要（见 Table 1 中 backbone 对比的间接证据）。

### 3. Transformer编码器骨干网络

MDM采用纯Transformer编码器架构作为生成网络 $G$，而非图像扩散模型中常用的U-Net。这一设计选择基于运动数据的时间序列特性：运动本质上是时序的、非空间的，Transformer的自注意力机制天然适合建模帧间长程依赖。实验表明，Transformer编码器在HumanML3D基准上的FID达到0.544，优于U-Net和GRU等替代方案（Table 1 backbone comparison）。

### 4. 无分类器引导的统一条件机制

MDM通过无分类器引导（classifier-free guidance）实现多条件统一生成。训练时以10%的概率随机丢弃条件 $c$ 设为 $\emptyset$，采样时通过引导尺度 $s$ 在条件和无条件预测之间插值（公式 (7)）：

$$G_s(x_t, t, c) = G(x_t, t, \emptyset) + s \cdot (G(x_t, t, c) - G(x_t, t, \emptyset))$$

这一机制使同一模型能够无缝支持文本到运动（以CLIP嵌入为条件）、动作到运动（以学习的类别嵌入为条件）以及无约束生成。引导尺度 $s=2.5$ 在保真度与多样性之间达到最优平衡（Figure 4(b)）。

### 5. 扩散修复实现运动编辑

通过固定部分运动序列并让模型在扩散过程中迭代生成其余部分，MDM天然支持两种编辑模式：
- **时间插值**：固定首尾25%的帧，生成中间50%的过渡运动
- **身体部位编辑**：固定不需要编辑的关节，仅生成目标部位的关节运动

这一能力无需额外训练，直接复用预训练模型的去噪过程（Figure 3）。

## 整体框架

MDM（Motion Diffusion Model）是一个基于扩散的生成框架，旨在统一处理文本到运动、动作到运动以及无约束运动生成等多类任务。其整体设计围绕一个核心洞察展开：**将扩散模型的预测目标从噪声 ε 改为干净信号 x̂₀**，从而使得在训练过程中可以直接施加几何运动学约束，在保持轻量级架构的同时显著提升生成质量。

### 模块组成与数据流

MDM 的 pipeline 由五个关键模块构成，其数据流如图 2（左）所示：

1. **条件编码器（Text Encoder）**  
   对于文本条件任务，MDM 采用冻结的 **CLIP-ViT-B/32** 将文本提示编码为条件嵌入 c。对于动作标签等其他条件，则使用可学习的类别嵌入。该嵌入将作为生成过程的控制信号。

2. **扩散过程（Diffusion Process）**  
   遵循标准马尔可夫前向加噪过程，逐步向原始运动序列 $x_0^{1:N}$ 添加高斯噪声，得到含噪序列 $x_t^{1:N}$：
   $$q(x_t^{1:N} | x_{t-1}^{1:N}) = \mathcal{N}(\sqrt{\alpha_t} x_{t-1}^{1:N}, (1-\alpha_t)I)$$
   其中 $N$ 为序列长度，$t$ 为扩散时间步。

3. **Transformer 编码器骨干网络**  
   这是 MDM 的核心生成模块，采用纯 **Transformer encoder-only** 架构。输入为含噪运动序列 $x_t^{1:N}$、时间步 $t$ 和条件嵌入 $c$，三者被投影后拼接为输入 token。与图像扩散模型中常用的 U-Net 不同，该设计更适配运动数据的时序性、非空间特性，且参数量更轻量。

4. **干净样本预测与几何损失**  
   模型直接预测干净样本 $\hat{x}_0 = G(x_t, t, c)$，而非预测噪声。训练目标由简单损失和三个几何损失加权组成：
   - **简单损失** $\mathcal{L}_{\mathrm{simple}} = E_{x_0, t} [\|x_0 - G(x_t, t, c)\|_2^2]$：约束预测样本与真实样本的全局一致性。
   - **位置损失** $\mathcal{L}_{\mathrm{pos}}$：通过前向运动学（FK）计算关节点位置，约束预测运动与真实运动在三维空间中的位置一致性。
   - **速度损失** $\mathcal{L}_{\mathrm{vel}}$：约束相邻帧间关节速度的一致性，保证运动平滑。
   - **脚接触损失** $\mathcal{L}_{\mathrm{foot}}$：利用二进制接触掩码 $f_i$，约束着地脚部的速度趋近于零，减少滑动伪影。

   总损失函数为：
   $$\mathcal{L} = \mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{foot}} \mathcal{L}_{\mathrm{foot}}$$

5. **无分类器引导采样（Classifier-Free Guidance）**  
   训练时以 10% 的概率随机将条件 $c$ 置为空 $\emptyset$，使模型同时学习条件生成和无条件生成。采样时通过引导尺度 $s$ 在两者之间插值：
   $$G_s(x_t, t, c) = G(x_t, t, \emptyset) + s \cdot (G(x_t, t, c) - G(x_t, t, \emptyset))$$
   调节 $s$ 可在保真度与多样性之间取得平衡（实验表明 $s=2.5$ 为最佳折中点）。

### 推理流程

如图 2（右）所示，采样从纯噪声 $x_T$ 开始，在每一步 $t$ 中，模型预测干净样本 $\hat{x}_0$，再通过扩散过程将其回退到 $x_{t-1}$，迭代 $T$ 步后得到最终生成的运动序列。

### 运动编辑能力

框架通过**扩散修复（diffusion inpainting）** 机制自然支持运动编辑：
- **时间插值**：固定序列首尾各 25% 的帧，让模型生成中间 50% 的过渡运动。
- **身体部位编辑**：固定不需编辑的关节，仅让模型重新生成目标部位的运动，实现语义级局部编辑（如仅改变上半身动作）。

### 关键设计选择与替代方案

| 设计槽位 | 基线做法 | MDM 选择 | 证据锚点 |
|---------|---------|---------|---------|
| 扩散骨干网络 | U-Net（图像扩散常用） | Transformer encoder-only | Section 3, Figure 2 |
| 预测目标 | 噪声 ε | 干净样本 $\hat{x}_0$ | Equation (2) |
| 几何约束 | 无或隐式 | 显式位置/速度/脚接触损失 | Equations (3)-(5) |
| 条件机制 | 分类器引导或分离模型 | 无分类器引导 + CLIP 嵌入 | Equation (7) |
| 运动编辑 | 不支持或有限 | 扩散修复（时间+空间） | Section 5.1 |

![[assets/figures/papers/paper_list_l9_MDM_Human_Motion_Diffusion_Model/figures/002_Figure_2.jpg]]
*Figure 2: (Left) Motion Diffusion Model (MDM) overview. The model is fed a motion sequence $\boldsymbol { x } _ { t } ^ { 1 : N }$ of length N in a noising step t, as well as t itself and a conditioning code c. c, a CLIP (Radford et al., 2021) based textual embedding in this case, is first randomly masked for classifier-free learning and then projected together with t into the input token $z _ { t k }$ . In each sampling step, the transformerencoder predicts the final clean motion $\hat { x } _ { 0 } ^ { 1 : N }$ . (Right) Sampling MDM. Given a condition c, we sample random noise $x _ { T }$ at the dimensions of the desired motion, then iterate from T to 1. At each step t, MDM predicts the clean sample ${ \ha$...

消融实验证实，Transformer 编码器骨干在不同架构变体中表现一致且优于 U-Net 和 GRU 替代方案（Table 1），验证了该设计选择的合理性。

### 补充图表

![[assets/figures/papers/paper_list_l9_MDM_Human_Motion_Diffusion_Model/figures/001_Figure_1.jpg]]
*Figure 1: Our Motion Diffusion Model (MDM) reflects the many-to-many nature of text-to-motion mapping by generating diverse motions given a text prompt. Our custom architecture and geometric losses help yielding high-quality motion. Darker color indicates later frames in the sequence*

## 核心模块与公式推导

MDM 的核心设计围绕一个轻量级 Transformer 编码器骨干网络展开，其关键创新在于将扩散模型的预测目标从噪声改为干净样本，从而使得显式几何损失可以直接作用于生成过程。整体架构由五个协同模块构成。

### 扩散过程与预测目标转换

MDM 沿用标准马尔可夫扩散过程，逐步向运动序列添加高斯噪声：

$$q(x_t^{1:N} | x_{t-1}^{1:N}) = \mathcal{N}(\sqrt{\alpha_t} x_{t-1}^{1:N}, (1-\alpha_t)I) \quad \text{(Equation 1)}$$

其中 $x_t^{1:N}$ 表示长度为 $N$ 的运动序列在第 $t$ 步加噪后的状态，$\alpha_t$ 为噪声调度参数。

与传统扩散模型预测噪声 $\epsilon$ 不同，MDM 直接预测干净样本 $\hat{x}_0$。训练时采用简单均方误差损失：

$$\mathcal{L}_{\mathrm{simple}} = E_{x_0 \sim q(x_0|c), t \sim [1,T]} [\|x_0 - G(x_t, t, c)\|_2^2] \quad \text{(Equation 2)}$$

其中 $G$ 为 Transformer 编码器生成网络，$c$ 为条件嵌入（如 CLIP 文本嵌入），$T$ 为扩散总步数。这一预测目标的转换是 MDM 能够应用几何损失的根本原因——预测 $\hat{x}_0$ 后可直接计算其在运动学空间中的物理合理性，而预测噪声则无法实现这一点。

### 几何损失函数

为提升生成运动的物理合理性，MDM 引入了三个几何损失函数，均作用于预测的干净样本 $\hat{x}_0$ 上。

**位置损失** 通过前向运动学（FK）将关节旋转映射为三维关节点位置，约束预测位置与真实位置的差异：

$$\mathcal{L}_{\mathrm{pos}} = \frac{1}{N} \sum_{i=1}^N \|FK(x_0^i) - FK(\hat{x}_0^i)\|_2^2 \quad \text{(Equation 3)}$$

**脚接触损失** 针对运动生成中常见的脚部滑动问题，利用二进制接触掩码 $f_i$ 约束着地脚的速度为零：

$$\mathcal{L}_{\mathrm{foot}} = \frac{1}{N-1} \sum_{i=1}^{N-1} \|(FK(\hat{x}_0^{i+1}) - FK(\hat{x}_0^i)) \cdot f_i\|_2^2 \quad \text{(Equation 4)}$$

其中 $f_i$ 在脚与地面接触时为 1，否则为 0，迫使接触帧间关节点位移趋近于零。

**速度损失** 约束相邻帧间关节速度的一致性：

$$\mathcal{L}_{\mathrm{vel}} = \frac{1}{N-1} \sum_{i=1}^{N-1} \|(x_0^{i+1} - x_0^i) - (\hat{x}_0^{i+1} - \hat{x}_0^i)\|_2^2 \quad \text{(Equation 5)}$$

总训练损失为上述各项的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{foot}} \mathcal{L}_{\mathrm{foot}} \quad \text{(Equation 6)}$$

其中 $\lambda_{\mathrm{pos}}$、$\lambda_{\mathrm{vel}}$、$\lambda_{\mathrm{foot}}$ 为各几何损失的权重超参数。

### 无分类器引导采样

MDM 采用无分类器引导（classifier-free guidance）机制实现条件控制。训练时以 10% 的概率随机将条件 $c$ 置为空 $\emptyset$，使模型同时学习条件生成和无条件生成。采样时通过尺度 $s$ 在条件预测与无条件预测之间插值：

$$G_s(x_t, t, c) = G(x_t, t, \emptyset) + s \cdot (G(x_t, t, c) - G(x_t, t, \emptyset)) \quad \text{(Equation 7)}$$

当 $s=1$ 时退化为标准条件生成；$s>1$ 时增强条件信号的引导强度，在保真度与多样性之间取得平衡。消融实验表明 $s=2.5$ 为最优平衡点（Figure 4b）。

### 扩散修复编辑

MDM 通过扩散修复（diffusion inpainting）实现运动编辑，无需额外训练。其核心机制是在去噪过程的每一步中，将已知部分（如运动首尾帧或特定身体部位关节）替换为真实值，仅对未知区域执行去噪更新。具体而言：

- **时间插值**：固定序列前 25% 和后 25% 的帧，生成中间 50% 的过渡运动。
- **身体部位编辑**：固定不需要编辑的关节，仅对目标部位关节进行生成，同时可接受文本条件引导。

这一机制使得同一模型能够同时支持文本到运动、动作到运动、无约束生成以及运动编辑等多任务场景，体现了统一框架的设计优势。

## 实验与分析

### 文本到运动生成

MDM在文本到运动任务上进行了全面评估，使用了**HumanML3D**和**KIT**两个主流基准，并严格遵循T2M（Guo et al., CVPR 2022）的评估协议：所有指标均运行20次以计算95%置信区间（MultiModality运行5次）。评估指标包括FID（衡量生成质量）、R-Precision（衡量文本-运动匹配精度）、Diversity（衡量生成多样性）和MultiModality（衡量多模态生成能力）。

在**HumanML3D**基准上（Table 1），MDM以Transformer编码器为骨干网络取得了FID **0.544**，显著优于此前的最佳方法T2M（基于VAE）和其他竞争方法（JL2P、Text2Gesture、TEMOS等）。在Diversity和MultiModality指标上，MDM同样达到最优，证明其不仅能生成高质量运动，还能覆盖文本提示的多种合理运动解释。值得注意的是，Table 1还对比了不同骨干网络（U-Net、GRU）的性能，Transformer编码器在所有指标上均表现一致且优越，且保持了轻量级特性。

![[assets/figures/papers/paper_list_l9_MDM_Human_Motion_Diffusion_Model/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on the HumanML3D test set. All methods use the real motion length from the ground truth. $\cdot _ { }$ , means results are better if the metric is closer to the real distribution. We run all the evaluation 20 times (except MultiModality runs 5 times) and ± indicates the 95% confidence interval. Bold indicates best result*

在**KIT**基准上（Table 2），MDM延续了领先趋势，在FID等关键指标上达到最佳。KIT数据集规模较小、运动类型更集中，MDM在此场景下仍展现出强大的泛化能力。

![[assets/figures/papers/paper_list_l9_MDM_Human_Motion_Diffusion_Model/figures/005_Table_2.jpg]]
*Table 2: Quantitative results on the KIT test set*

### 用户研究

为进一步验证生成运动的感知质量，作者在KIT测试集上进行了用户研究（Figure 4a）。评估者被要求在两段运动中选择更符合文本描述的一项，对比对象包括真实运动（Ground Truth）和其他生成模型。结果显示，MDM在**42.3%**的情况下被偏好超过真实运动，接近50%的随机基线水平，这表明MDM生成的运动在主观感知上已逼近真实数据。与其他生成模型相比，MDM在大多数对比中获得了更高的偏好率。

### 动作到运动生成

MDM在动作到运动任务上同样展现出强大的性能。该任务以离散动作类别为条件生成对应运动，评估使用了**HumanAct12**和**UESTC**两个基准。

在**HumanAct12**上（Table 3），MDM在四项指标中的三项取得最优：**FID_train达到0.100**，**Accuracy达到0.990**，Multimodality为2.520。相比此前的最佳方法（如ACTOR、INR），MDM在生成质量和动作识别准确率上均有显著提升。Accuracy接近完美（0.990），说明生成的运动与给定动作类别高度一致。

![[assets/figures/papers/paper_list_l9_MDM_Human_Motion_Diffusion_Model/figures/008_Table_3.jpg]]
*Table 3: Evaluation of action-to-motion on the HumanAct12 dataset. Our model leads the board in three out of four metrics. Ground-truth evaluation results are slightly different for each of the works, due to implementation differences, such as python package versions. It is important to assess the diversity and multimodality of each model using its own ground-truth results, as they are measured by their distance from GT. We show the GT metrics measured by our model and by the leading compared work, INR (Cervantes et al., 2022). Bold indicates best result, underline indicates second best, ± indicates 95% confidence interval, → indicates that closer to real is better*

在**UESTC**上（Table 4），MDM的优势更为明显：**FID_test为12.81**，Accuracy为0.950，Multimodality为14.26，与第二名方法之间存在明显差距。UESTC数据集包含更复杂的动作序列，MDM在此场景下的领先证明了其对复杂运动模式的建模能力。

![[assets/figures/papers/paper_list_l9_MDM_Human_Motion_Diffusion_Model/figures/009_Table_4.jpg]]
*Table 4: Evaluation of action-to-motion on the UESTC dataset. The performance improvement with our model shows a clear gap from state-of-the-art. Bold indicates best result, underline indicates second best, ± indicates 95% confidence interval, → indicates that closer to real is better*

### 无约束运动生成

在无约束运动合成任务中（Table 5），MDM与专门为此设计的**MoDi**（Raab et al., arXiv 2022）进行了对比。在HumanAct12数据集上，MDM取得了FID **31.92**，接近但略逊于MoDi。这一结果说明，尽管MDM并非为无约束生成专门优化，其统一的扩散框架仍能产生合理的运动序列，展现了方法的通用性。

![[assets/figures/papers/paper_list_l9_MDM_Human_Motion_Diffusion_Model/figures/010_Figure_3.jpg]]
*Figure 3: model to generate the rest. In particular, we experiment with editing the upper body joints only. In figure 3 we show that in both cases, using the method described in Section 3 generates smooth motions that adhere both to the fixed part of the motion and the condition (if one was given). Table 5: Evaluation of unconstrained synthesis on the HumanAct12 dataset. We test MDM in the challenging unconstrained setting, and compare with MoDi (Raab et al., 2022), a work that was specially designed for such setting. We demonstrate that in addition to being able to support any condition, we can achieve plausible results in the unconstrained setting. Bold indicates best result*

### 消融实验

**无分类器引导尺度**：Figure 4b展示了在HumanML3D上引导尺度 $s$ 对FID和R-Precision的影响。结果表明，$s=2.5$ 附近存在保真度与多样性的最佳平衡点——过小的 $s$ 导致生成质量下降（FID升高），过大的 $s$ 则损害多样性（R-Precision降低）。这一发现为实际部署提供了明确的参数选择指导。

**骨干网络对比**：Table 1中包含了对Transformer编码器、U-Net和GRU三种骨干网络的消融对比。Transformer在所有指标上均优于其他架构，验证了自注意力机制对时序运动数据建模的适配性。

### 运动编辑能力

MDM通过扩散修复（diffusion inpainting）实现了两种运动编辑模式（Figure 3）：
- **时间插值**：固定运动序列的前25%和后25%，让模型生成中间50%的过渡帧。该过程可附加文本条件以控制过渡风格。
- **身体部位编辑**：固定不需要修改的关节（如下半身），仅让模型根据新文本提示重新生成目标部位（如上身）。Figure 3展示了上半身编辑的示例，生成的过渡运动平滑且同时满足固定部分和文本条件的约束。

### 失败模式与局限性

尽管MDM在多个基准上取得了领先结果，仍存在以下局限：

1. **推理速度**：生成单个样本需要约1000次前向传播（约1分钟），对实时应用（如交互式游戏、VR）仍显不足。这是扩散模型固有的采样效率问题。
2. **无约束生成**：在无约束设置下，MDM的性能未超越专门设计的MoDi，说明通用框架在特定场景下仍有优化空间。
3. **几何损失的适用范围**：在文本到运动任务中，由于HumanML3D的数据表示已包含必要的运动学信息，几何损失未被使用。这限制了该方法在更广泛文本到运动场景中的直接迁移，需要适当的运动学表示支持。

### 公平性说明

所有文本到运动评估遵循T2M（Guo et al., CVPR 2022）的协议，包括使用真实运动长度、20次运行计算置信区间等标准化流程。训练资源统一为单块NVIDIA GeForce RTX 2080 Ti，约3天完成训练，保证了方法间硬件公平性。用户研究在KIT测试集上进行，通过随机化对比和多名评估者确保了主观评估的可靠性。

## 方法谱系与知识库定位

### 1. 方法沿革与基线关系

MDM 出现在人体运动生成从自编码器范式向扩散模型范式过渡的关键节点。此前的主流方法可大致分为两条技术路线：

**自编码器路线**以 VAE 及其变体为核心，代表性工作包括：
- **JL2P** (Ahuja & Morency, 3DV 2019)：基于自编码器的文本到运动框架，较早探索语言与运动的联合嵌入。
- **Text2Gesture** (Bhattacharya et al., VR 2021)：面向手势生成的文本条件模型。
- **T2M** (Guo et al., CVPR 2022)：基于 VAE 的文本到运动方法，在 HumanML3D 和 KIT 基准上曾达到 SOTA，是 MDM 在文本到运动任务上的主要对比对象。
- **TEMOS** (Petrovich et al., ECCV 2022)：同样基于 VAE，同时支持文本和动作条件。
- **ACTOR** (Petrovich et al., ICCV 2021)：面向动作到运动的 Transformer VAE 模型，是 HumanAct12 和 UESTC 基准上的重要基线。

这些 VAE 类方法的共同瓶颈在于：假设潜在空间服从正态分布，限制了生成运动的多样性和表现力；同时缺乏显式的运动学约束，生成质量难以保证。

**扩散模型路线**在 MDM 之前已有初步探索，但存在两个突出问题：
- 沿用图像扩散模型的 U-Net 骨干网络，未针对人体运动的时序、非空间特性进行适配。
- 预测目标为噪声 ε，使得无法直接施加几何约束（因为损失定义在噪声空间而非运动信号空间）。

MDM 的核心突破在于**将预测目标从噪声改为干净样本** $\hat{x}_0$（Equation 2），这一改动看似简单，却产生了连锁效应：使得位置损失 $\mathcal{L}_{\text{pos}}$、速度损失 $\mathcal{L}_{\text{vel}}$ 和脚接触损失 $\mathcal{L}_{\text{foot}}$ 可以直接作用于预测信号（Equations 3-5），从而在训练过程中显式约束运动学合理性。同时，MDM 采用 **Transformer encoder-only** 架构替代 U-Net，更贴合运动数据的时序特性，且参数量更轻量（单块 RTX 2080 Ti 训练约 3 天）。

在条件机制上，MDM 采用**无分类器引导**（classifier-free guidance），通过 CLIP-ViT-B/32 编码文本条件，训练时以 10% 概率随机丢弃条件，采样时在条件与无条件预测间插值（Equation 7）。这一设计使单一模型能够统一支持文本到运动、动作到运动和无约束生成三种任务，无需为每种条件训练独立模型。

### 2. 适用边界与局限

**推理效率瓶颈**：MDM 生成单个样本需要约 1000 次前向传播（约 1 分钟），难以满足实时交互需求。这是扩散模型固有的采样步数问题，论文未采用 DDIM 等加速采样策略，留下了明显的优化空间。

**无约束生成并非最优**：在 HumanAct12 无约束运动合成设置下，MDM 的 FID 为 31.92，接近但略逊于专门为此设计的 **MoDi** (Raab et al., arXiv 2022)（Table 5）。这表明 MDM 的“统一框架”优势在极端无约束场景下存在性能折衷。

**几何损失的适用范围受限**：文本到运动任务（HumanML3D、KIT）中，论文并未使用几何损失，原因是数据表示已包含必要信息。这意味着几何损失对数据格式有依赖，在更通用的文本到运动场景中直接应用可能存在障碍。

**编辑能力的边界**：扩散修复（diffusion inpainting）支持时间插值和身体部位编辑（Figure 3），但编辑质量依赖于已知部分的固定比例（如时间插值需固定首尾各 25%），极端稀疏条件下的编辑效果未经验证。

### 3. 开放问题

1. **精细控制与物理仿真融合**：MDM 的几何损失提供了粗粒度的运动学约束，但能否进一步融入物理仿真约束（如接触力、动力学平衡）或风格迁移机制，以实现更精细的运动控制？

2. **高效采样策略**：能否通过 DDIM 等确定性采样方法将推理步数从 1000 步压缩至数十步，在保持生成质量的前提下将推理时间降至秒级？

3. **几何损失的泛化**：几何损失能否通过适当的运动表示变换（如将关节角度转换为关节点位置）拓展到更广泛的文本到运动场景中，使所有条件生成任务都受益于运动学约束？

4. **多模态条件统一生成**：MDM 已展示文本和动作类别的单条件生成能力，能否将框架扩展至多模态条件（如文本+音频、文本+场景上下文）的统一生成，进一步拓宽应用场景？

## 原文 PDF

![[paperPDFs/ICLR_2023/MDM_Human_Motion_Diffusion_Model.pdf]]
