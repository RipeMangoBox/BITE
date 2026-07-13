---
title: "Cloning Deterministic Worlds: The Critical Role of Latent Geometry in Long-Horizon World Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Cloning_Deterministic_Worlds_The_Critical_Role_of_Latent_Geometry_in_Long_Horizon_World_Models.pdf
project_link: null
code_link: "https://github.com/XiaFire/Clone_Deterministic_Environment"
aliases:
- GRWMG
- CDWCRLGLHWM
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将时间对比学习作为几何正则化项加入世界模型的自动编码器训练，可重塑潜在空间，使其对齐环境的物理状态流形。
primary_logic: 高质量的潜在表示几何结构对于世界模型的稳定长时序预测至关重要，对比约束可以为潜在空间提供强有力的归纳偏置，从而显著提升滚动预测的保真度。
claims:
- 当动力学模型直接使用环境的真实物理状态时，可以实现近乎完美的长时序预测，说明表示是当前的主要瓶颈。
- 神谕模型（oracle）实现了近零帧级MSE，而标准VAE世界模型的误差快速累积，表明动力学模型本身并非限制因素。
- 加入时间对比正则化后，GRWM 显著缩小了与神谕模型的性能差距，并在多个环境和动力学模型上持续优于基线。
- Maze 9×9-DET (DF) 上 SSIM = 0.8516
---

# Cloning Deterministic Worlds: The Critical Role of Latent Geometry in Long-Horizon World Models

> [!tip] 核心洞察
> 高质量的潜在表示几何结构对于世界模型的稳定长时序预测至关重要，对比约束可以为潜在空间提供强有力的归纳偏置，从而显著提升滚动预测的保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 克隆确定性世界：潜在几何结构在长时序世界模型中的关键作用 |
| 英文题名 | Cloning Deterministic Worlds: The Critical Role of Latent Geometry in Long-Horizon World Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.26782) · [Code](https://github.com/XiaFire/Clone_Deterministic_Environment) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | Geometrically-Regularized World Models (GRWM) |
| Dataset | Maze 9×9-DET, Atari Asterix, Atari Breakout |

> [!tip] 效果简介
> - Maze 9×9-DET (DF) 上，SSIM 0.8516 vs 0.8448 (+0.0068)；rFID 2.8729 vs 4.4345 (-1.5616)。
> - Maze 9×9-DET (VD) 上，SSIM 0.7537 vs 0.5979 (+0.1558)；rFID 7.2813 vs 18.1453 (-10.8640)。
> - Maze 9×9-DET (SD) 上，SSIM 0.8369 vs 0.8367 (+0.0002)。

## 概要

### 问题背景

世界模型（World Models）旨在学习环境的内部表征，并以此进行未来状态的预测。然而，现有方法在长时序（long-horizon）预测中普遍面临保真度急剧下降的问题。本文的核心发现是：**当前世界模型的主要瓶颈并非动力学模型本身，而是潜在表示空间的几何结构**。当动力学模型直接使用环境的真实物理状态时，可以实现近乎完美的长时序预测，这表明表示学习阶段的质量决定了世界模型的预测上限。

### 核心贡献

本文提出了**几何正则化世界模型（Geometrically-Regularized World Models, GRWM）**，其核心思想是将时间对比学习作为几何正则化项引入世界模型的自动编码器训练中。具体而言，GRWM 在标准 VAE 的重建损失与 KL 散度之外，额外施加了两个几何约束：**时间缓慢损失（Temporal Slowness Loss）** 和 **潜在均匀性损失（Latent Uniformity Loss）**，以重塑潜在空间，使其更好地对齐环境的物理状态流形。GRWM 是一个轻量级的即插即用模块，可无缝集成到标准自动编码器中。

### 方法谱系与知识库定位

GRWM 位于世界模型、表示学习与对比学习的交叉点。与标准 VAE 世界模型（VAE-WM）相比，GRWM 在训练目标函数中增加了对比几何正则化，从而改变了潜在空间的组织方式。该方法可与多种先进的潜变量动力学模型结合使用，包括 Diffusion Forcing (DF)、Video Diffusion (VD) 和 Standard Diffusion (SD)，在不改变动力学模型架构的前提下系统性地提升长时序预测保真度。

### 主要发现

1. **表示瓶颈验证**：神谕模型（oracle，使用真实物理状态）实现了近零帧级 MSE，而标准 VAE 世界模型的误差快速累积，证实表示质量是主要瓶颈（Figure 1）。
2. **性能提升**：GRWM 在多个确定性环境（Maze 3×3-DET、Maze 9×9-DET、MC-DET）和多种动力学模型上均显著优于基线，大幅缩小了与神谕模型的性能差距（Figure 3, Table 2）。
3. **定性改善**：GRWM 在长时序滚动预测中能保持空间一致性，避免基线方法常见的“瞬移”或生成坍缩现象（Figure 4, Figure 5, Figure 6）。
4. **潜在空间结构**：聚类分析表明，GRWM 学习到的潜在空间与环境的真实状态流形具有更强的结构对齐性（Figure 7），潜在探测实验也定量证实了其表示对真实状态的预测能力更强（Table 1）。
5. **泛化性**：在 Atari 游戏环境（Asterix、Breakout）上的补充实验进一步验证了 GRWM 的有效性（Table 3）。

### 局限性与开放问题

当前 GRWM 主要针对确定性环境设计，尚未验证在部分可观察、随机或高度真实感环境中的有效性。此外，与神谕模型相比，学习到的表示仍有明显差距，表明现有几何正则化尚不足以实现近乎完美的长期预测。未来的方向包括：将几何正则化扩展到更复杂的环境、设计更强的表示学习方法以进一步缩小与神谕模型的差距，以及探索时间对比约束与其他动力学模型的结合潜力。

### 世界模型与长时序预测的挑战

世界模型（World Models）旨在学习环境的内部动力学，使智能体能够在“想象”中预测未来的观测序列。这类模型在基于模型的强化学习、规划与决策中扮演着核心角色。一个理想的世界模型应当能够在长时序范围内保持高保真度的滚动预测（rollout），即从初始状态出发，仅依赖自身生成的观测逐步推演未来数百甚至数千步的演化轨迹。

然而，现实中的世界模型普遍面临一个严峻问题：**预测误差随时间步呈指数级累积**，导致长时序生成的画面迅速偏离真实环境，出现模糊、失真甚至“瞬移”到语义不一致区域的现象。这一瓶颈严重制约了世界模型在需要长期推理的任务中的实用性。

### 现有方法的缺口：动力学模型与表示学习的失衡

近年来，世界模型的动力学建模能力取得了显著进步。以 **Diffusion Forcing (DF)**、**Video Diffusion (VD)** 和 **Standard Diffusion (SD)** 为代表的先进潜变量动力学模型，在视频预测和序列生成任务中展现了强大的时序建模能力。然而，即便搭载了这些最先进的动力学模型，现有世界模型在长时序滚动预测中仍然无法维持可接受的保真度。

这一现象引出了一个根本性问题：**长时序预测的瓶颈究竟在于动力学模型本身，还是在于潜在表示空间的质量？**

### 核心瓶颈的揭示：表示空间几何结构

本文通过一个关键诊断实验给出了明确答案。在一个简单的确定性 3D 导航环境中，作者构建了一个“神谕模型”（oracle model）：该模型直接使用环境的真实底层物理状态（ground-truth states）作为动力学模型的输入，而非从像素观测中学习潜在表示。结果显示，神谕模型实现了**近乎零的逐帧均方误差**（frame-wise MSE），在长时序预测中几乎没有误差累积（参见 Figure 1 左图）。

与之形成鲜明对比的是，标准的基于 VAE 的世界模型（VAE-WM）在相同环境下，预测误差随步数迅速攀升，在数十步后即严重偏离真实轨迹。这一对比强有力地表明：**当动力学模型获得高质量的物理状态表示时，它完全有能力进行精确的长时序推演；当前世界模型保真度的主要瓶颈在于潜在表示空间的几何结构，而非动力学模型本身。**

进一步分析发现，标准 VAE 学习到的潜在空间呈现出**杂乱无章的结构**：语义相近的物理状态在潜在空间中可能相距甚远，而语义迥异的状态却可能被错误地聚集在一起（参见 Figure 1 右上图）。这种几何失序导致动力学模型在潜在空间中推演时，极易偏离环境的真实状态流形，从而引发不可逆的误差累积。

### 本文动机：以几何正则化重塑潜在空间

基于上述诊断，本文提出一个核心洞察：**高质量的潜在表示几何结构对于世界模型的稳定长时序预测至关重要**。如果能够重塑潜在空间，使其几何结构对齐环境的物理状态流形——即相邻时间步的潜在表示彼此靠近，不同轨迹的表示均匀分布——那么动力学模型在潜在空间中的推演将更有可能停留在真实状态流形上，从而显著提升滚动预测的保真度。

为实现这一目标，本文引入了**时间对比学习**（temporal contrastive learning）作为几何正则化手段。时间对比学习天然鼓励时间上相近的样本在表示空间中彼此靠近，而时间上远离的样本相互推开，这与世界模型对理想潜在空间的需求高度契合。本文提出的 **Geometrically-Regularized World Models (GRWM)** 将这一思想实现为一个轻量级的即插即用模块，可无缝集成到标准自动编码器中，通过几何正则化项重塑潜在空间，从而系统性解锁现有先进动力学模型的长时序预测能力。

## 核心方法与创新机理

### 1. 瓶颈重定义：从动力学模型到潜在几何结构

本工作的首要创新在于对长时序世界模型性能瓶颈的重新诊断。传统研究普遍将世界模型滚动预测的误差累积归因于动力学模型的容量或训练不足。本文通过一个关键对照实验颠覆了这一认知：当动力学模型直接接收环境的真实物理状态（ground-truth states）作为输入时，可以实现近乎零误差的长时序预测（Figure 1 左，神谕模型表现为黑色虚线，逐帧MSE接近零）；而架构完全相同的动力学模型在标准VAE学习到的潜在表示上运行时，误差则迅速发散（Figure 1 左，蓝色虚线）。

这一对比揭示了两条核心结论：（1）在该确定性环境中，高保真度的长时序克隆在技术上是可行的；（2）当前的主要限制并非动力学模型本身，而是其所依赖的潜在表示空间的质量。这一发现将研究焦点从动力学模型的改进转移到了表示空间的几何结构上，为后续方法设计提供了全新的因果旋钮。

### 2. 核心方法：时间对比学习作为几何正则化

基于上述诊断，本文提出 **Geometrically-Regularized World Models (GRWM)**，其核心创新在于将时间对比学习原则引入世界模型的自动编码器训练，作为重塑潜在空间几何结构的正则化手段。

#### 2.1 关键变更槽位

GRWM 相对于标准 VAE 世界模型（VAE-WM）的核心变更体现在训练目标函数上：

| 组件 | VAE-WM（基线） | GRWM（本文） |
|------|----------------|--------------|
| 训练目标 | 仅包含重建损失 $\mathcal{L}_{\mathrm{recon}}$ 和 KL 散度 $\beta \mathcal{L}_{\mathrm{KL}}$ | 额外添加**时间缓慢损失** $\lambda_{\mathrm{slow}} \mathcal{L}_{\mathrm{slow}}$ 和**潜在均匀性损失** $\lambda_{\mathrm{uniform}} \mathcal{L}_{\mathrm{uniform}}$ |

完整训练目标为：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{recon}} + \beta \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{slow}} \mathcal{L}_{\mathrm{slow}} + \lambda_{\mathrm{uniform}} \mathcal{L}_{\mathrm{uniform}}$$

#### 2.2 时间缓慢损失：强制局部连续性

时间缓慢损失的设计动机源于一个基本观察：在物理世界中，相邻时刻的状态通常连续变化，其潜在表示应彼此靠近。该损失作用于投影头输出的单位超球面嵌入 $\mathbf{p}'$ 上：

$$\mathcal{L}_{\mathrm{slow}} = \mathbb{E}_{b \sim \mathcal{D}} \left[ \mathbb{E}_{(\mathbf{p}_i', \mathbf{p}_j') \sim \mathcal{P}_b' \times \mathcal{P}_b'} \left[ \| \mathbf{p}_i' - \mathbf{p}_j' \|_2 \right] \right]$$

该损失鼓励同一轨迹上下文窗口内的所有帧对在超球面上彼此靠近，从而强制潜在表示随时间缓慢、连续地变化。这一约束为潜在空间注入了时序平滑性的归纳偏置，有效抑制了表示在相邻帧之间的不连续跳变。

#### 2.3 潜在均匀性损失：防止表示坍缩

单纯施加时间缓慢损失可能导致所有表示坍缩到同一点。为保持表示的多样性和区分度，GRWM 引入了潜在均匀性损失：

$$\mathcal{L}_{\mathrm{uniform}} = \log \mathbb{E}_{(\mathbf{p}_i', \mathbf{p}_j') \sim \mathcal{P}_{\mathrm{neg}}} \left[ e^{-2 \| \mathbf{p}_i' - \mathbf{p}_j' \|_2^2} \right]$$

该损失通过最大化不同轨迹嵌入之间的间距，促使嵌入均匀分布在超球面上。两种损失形成互补的几何约束：时间缓慢损失在局部尺度上强制连续性，均匀性损失在全局尺度上维护结构的展开性。

### 3. 即插即用的轻量化设计

GRWM 的另一个重要创新在于其架构设计理念：它是一个轻量级的几何正则化模块，而非一个全新的世界模型架构。具体而言，GRWM 在标准自动编码器的基础上仅增加了两个组件：

- **投影头**：一个线性层后接 L2 归一化，将编码器输出的潜在表示 $z_t$ 映射到单位超球面上的嵌入 $\mathbf{p}'$，专门用于计算对比损失。
- **几何正则化损失**：即上述的时间缓慢损失和潜在均匀性损失。

编码器（2D CNN + 因果Transformer）和解码器的架构保持与基线一致。这种设计使得 GRWM 可以无缝集成到现有的潜变量动力学模型中——实验表明，无论是 Diffusion Forcing (DF)、Video Diffusion (VD) 还是 Standard Diffusion (SD)，集成 GRWM 后均能获得一致的性能提升（Figure 3），验证了其作为即插即用组件的通用性。

### 4. 与现有工作的本质区别

GRWM 的核心创新并非时间对比学习本身（该原理在自监督表示学习中已有广泛研究），而在于**将其重新定位为世界模型潜在空间的几何正则化器**。这一视角转换带来了方法论上的关键区别：

- 传统世界模型依赖重建损失和 KL 散度来约束潜在空间，但这些目标无法显式地塑造潜在空间的几何结构，导致学习到的表示在物理状态流形上呈现无组织的散乱分布（Figure 1 右上，Figure 7 上行）。
- GRWM 通过对比约束显式地要求潜在空间对齐环境的物理状态流形，使得空间上相邻的帧在潜在空间中也被组织在一起，形成空间连贯的聚类结构（Figure 1 右下，Figure 7 下行）。

潜在探测实验（Table 1）定量验证了这一效果：在三个数据集上，GRWM 学习到的表示对真实物理状态的回归 MSE 均显著低于 VAE-WM（例如 MC-DET 上 GRWM 为 0.081，VAE-WM 为 0.137），表明其潜在表示与底层物理状态的结构一致性更强。

GRWM 的核心设计理念是将**时间对比学习作为几何正则化项**，无缝集成到标准世界模型的自动编码器训练中，从而重塑潜在空间以对齐环境的物理状态流形。该方法并非提出全新的动力学模型，而是作为一个**轻量级、即插即用的几何正则化模块**，可作用于各类潜变量动力学模型之上。

### 系统流水线

GRWM 的整体架构由三个核心模块串联构成，形成“观测编码 → 表示正则化 → 观测重建”的端到端训练闭环：

1. **因果编码器（Causal Encoder）**：接收长度为 $k$ 的历史观测序列 $(o_{t-k}, \ldots, o_t)$，首通过 2D CNN 提取逐帧视觉特征，再由因果 Transformer 沿时间维度聚合上下文信息，输出包含时间上下文的潜在表示 $z_t$：
   $$z_t = E(o_{t-k}, \ldots, o_t)$$
   因果注意力机制确保 $z_t$ 仅依赖当前及过去帧，杜绝未来信息泄露，使编码器可直接用于滚动预测。

2. **投影头（Projection Head）**：将潜在表示 $z_t$ 经线性层映射后施加 L2 归一化，投影至单位超球面上的嵌入向量 $\mathbf{p}'$。该嵌入空间专用于计算对比损失，使得几何正则化在一个归一化、有界的流形上进行，避免表示尺度漂移。

3. **解码器（Decoder）**：从潜在表示 $z_t$ 重建当前观测 $\hat{o}_t$：
   $$\hat{o}_t = D(z_t)$$
   解码器与编码器共享相同的潜在表示，确保正则化后的几何结构直接服务于重建任务。

### 训练目标

总损失函数在标准 VAE 目标（重建损失 $\mathcal{L}_{\mathrm{recon}}$ 与 KL 散度 $\mathcal{L}_{\mathrm{KL}}$）之上，额外引入两项几何正则化损失，由超参数 $\lambda_{\mathrm{slow}}$ 和 $\lambda_{\mathrm{uniform}}$ 控制权重：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{recon}} + \beta \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{slow}} \mathcal{L}_{\mathrm{slow}} + \lambda_{\mathrm{uniform}} \mathcal{L}_{\mathrm{uniform}}$$

- **时间缓慢损失 $\mathcal{L}_{\mathrm{slow}}$**：强制同一轨迹上下文窗口内的所有帧对在超球面上彼此靠近，使潜在表示随时间缓慢连续变化，反映物理状态的平滑过渡特性：
  $$\mathcal{L}_{\mathrm{slow}} = \mathbb{E}_{b \sim \mathcal{D}} \left[ \mathbb{E}_{(\mathbf{p}_i', \mathbf{p}_j') \sim \mathcal{P}_b' \times \mathcal{P}_b'} \left[ \| \mathbf{p}_i' - \mathbf{p}_j' \|_2 \right] \right]$$

- **潜在均匀性损失 $\mathcal{L}_{\mathrm{uniform}}$**：通过最大化不同轨迹嵌入之间的间距，促使嵌入均匀分布在超球面上，防止表示坍缩到平凡解：
  $$\mathcal{L}_{\mathrm{uniform}} = \log \mathbb{E}_{(\mathbf{p}_i', \mathbf{p}_j') \sim \mathcal{P}_{\mathrm{neg}}} \left[ e^{-2 \| \mathbf{p}_i' - \mathbf{p}_j' \|_2^2} \right]$$

### 与动力学模型的解耦

GRWM 的几何正则化仅作用于自动编码器的表示学习阶段，与下游动力学模型（如 Diffusion Forcing、Video Diffusion、Standard Diffusion）完全解耦。训练完成后，编码器-解码器权重冻结，动力学模型在正则化后的潜在空间中独立训练与推理。这种模块化设计使 GRWM 可作为“插件”与任意潜变量动力学模型组合，无需修改后者架构。

### 输入输出规范

- **输入**：长度为 $k$ 的观测帧序列（原始像素），编码器以滑动窗口方式逐帧处理。
- **输出**：在训练阶段，输出重建帧 $\hat{o}_t$ 及用于对比损失的归一化嵌入 $\mathbf{p}'$；在滚动预测阶段，仅使用潜在表示 $z_t$ 作为动力学模型的输入与输出，解码器将预测的潜在状态还原为观测帧。
- **评估**：在像素空间计算预测帧与真实帧之间的逐帧均方误差 $\text{MSE}(t) = \| o_t - \hat{o}_t \|_2^2$，衡量滚动预测的累积误差。

### 5.1 因果编码器-解码器架构

GRWM 的世界模型基于一个标准自编码器框架，其核心由三个模块构成：

**因果编码器** 采用 2D CNN 与因果 Transformer 的级联结构。给定长度为 $k$ 的历史观测窗口，编码器首先通过 CNN 提取每帧的空间特征，随后由因果 Transformer 沿时间轴聚合上下文信息，确保当前时刻的潜在表示 $z_t$ 仅依赖于过去及当前的观测：

$$z_t = E(o_{t-k}, \ldots, o_t)$$

这一因果约束保证了潜在表示在时序上的因果一致性，为后续的几何正则化提供了结构基础。

**投影头** 由线性层与 L2 归一化组成，将编码器输出的潜在表示 $z_t$ 映射到单位超球面上的嵌入 $\mathbf{p}'$。该映射是计算对比损失的关键环节——所有几何正则化均在超球面上进行，而非直接在原始潜在空间中操作。

**解码器** 从潜在表示 $z_t$ 重建当前观测 $\hat{o}_t$：

$$\hat{o}_t = D(z_t)$$

重建质量由标准重建损失 $\mathcal{L}_{\mathrm{recon}}$ 约束，在 VAE 框架下还包含 KL 散度项 $\beta \mathcal{L}_{\mathrm{KL}}$。

### 5.2 几何正则化损失

GRWM 的核心创新在于将时间对比学习原则转化为两项几何正则化损失，直接作用于投影头输出的超球面嵌入。这两项损失与重建损失联合优化，重塑潜在空间的几何结构。

**时间缓慢损失（Temporal Slowness Loss）** 强制同一轨迹窗口内的所有帧对在超球面上彼此靠近：

$$\mathcal{L}_{\mathrm{slow}} = \mathbb{E}_{b \sim \mathcal{D}} \left[ \mathbb{E}_{(\mathbf{p}_i', \mathbf{p}_j') \sim \mathcal{P}_b' \times \mathcal{P}_b'} \left[ \| \mathbf{p}_i' - \mathbf{p}_j' \|_2 \right] \right]$$

其中 $\mathcal{P}_b'$ 表示从批次 $b$ 中同一轨迹采样的归一化嵌入集合。该损失直接最小化帧对之间的 L2 距离，鼓励潜在表示随时间缓慢连续变化，从而反映物理状态在时间上的平滑演化特性。

**潜在均匀性损失（Latent Uniformity Loss）** 通过最大化不同轨迹嵌入之间的间距，防止表示坍缩到超球面的局部区域：

$$\mathcal{L}_{\mathrm{uniform}} = \log \mathbb{E}_{(\mathbf{p}_i', \mathbf{p}_j') \sim \mathcal{P}_{\mathrm{neg}}} \left[ e^{-2 \| \mathbf{p}_i' - \mathbf{p}_j' \|_2^2} \right]$$

其中 $\mathcal{P}_{\mathrm{neg}}$ 表示从不同轨迹采样的负样本对集合。该损失采用径向基函数形式的斥力项，促使嵌入均匀覆盖超球面，确保潜在空间具有足够的表达能力来区分不同的物理状态。

**总训练目标** 将上述几何正则化项与标准自编码器损失联合优化：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{recon}} + \beta \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{slow}} \mathcal{L}_{\mathrm{slow}} + \lambda_{\mathrm{uniform}} \mathcal{L}_{\mathrm{uniform}}$$

其中 $\lambda_{\mathrm{slow}}$ 和 $\lambda_{\mathrm{uniform}}$ 为控制几何正则化强度的超参数。两项正则化损失共同作用：$\mathcal{L}_{\mathrm{slow}}$ 沿时间轴拉近相邻帧，形成连续的状态流形；$\mathcal{L}_{\mathrm{uniform}}$ 在全局尺度上推开不同轨迹，防止表示空间的局部坍缩。这种“局部吸引、全局排斥”的机制为潜在空间提供了强有力的几何归纳偏置。

### 5.3 逐帧评估指标

为量化世界模型的滚动预测保真度，本文采用像素空间的逐帧均方误差作为主要评估指标：

$$\text{MSE}(t) = \| o_t - \hat{o}_t \|_2^2$$

该指标逐时间步计算预测观测与真实观测之间的 L2 距离，能够精确刻画误差随预测时长的累积行为。在瓶颈诊断实验中，该指标直接揭示了表示质量与动力学模型能力之间的不对称性：当动力学模型使用真实物理状态时，$\text{MSE}(t)$ 在长时序上保持近零水平，而标准 VAE 世界模型的误差则随 $t$ 快速发散。

## 实验与关键发现

### 核心瓶颈验证：表示质量决定世界模型保真度

论文首先通过一个精巧的对比实验，确立了全文的核心论点：**潜在表示空间的几何结构，而非动力学模型本身，是长时序世界模型保真度的主要瓶颈**。

如 **Figure 1（左）** 所示，研究者在一个简单的确定性三维导航环境中，比较了两种模型的逐帧均方误差（Frame-wise MSE）：

$$
\text{MSE}(t) = \| o_t - \hat{o}_t \|_2^2
$$

其中，**神谕模型（Oracle）** 直接使用环境的真实物理状态作为动力学模型的输入，而 **VAE-WM** 则使用标准变分自编码器学习到的潜在表示。两者的动力学模型在架构上完全相同，唯一区别在于输入的潜在状态来源。实验结果显示，神谕模型实现了近乎零的逐帧误差，而 VAE-WM 的误差随时间步长迅速累积。这一鲜明对比直接揭示：**高保真度的长时序克隆在技术上是可行的，当前的主要限制并非来自动力学模型，而是来自它所操作的表示空间**。

进一步的可视化分析（**Figure 1 右**）表明，VAE-WM 的潜在表示在空间中呈现散乱无序的分布，而 GRWM 学习到的潜在空间则与环境的物理状态流形高度对齐，呈现出清晰的结构化组织。这为后续的几何正则化方法提供了直观的动机。

### 滚动预测性能：跨环境与跨动力学模型的定量评估

论文在三个确定性环境——Maze 3×3-DET、Maze 9×9-DET 和 Minecraft-DET（MC-DET）——上进行了系统的定量评估。如 **Figure 3** 所示，GRWM 在全部三个数据集上均显著缩小了与神谕模型的性能差距。

![[assets/figures/papers/paper_list_l2453_https_arxiv_org_abs_2510_26782/figures/003_Figure_3.jpg]]
*Figure 3: Rollout Performance. Frame-wise MSE between predicted and ground-truth trajectories on (a) M3x3-DET, (b) M9x9-DET, and (c) MC-DET datasets. The oracle model (black dotted line), which operates on the true underlying states, establishes a lower bound on error. For all three dynamics models—Diffusion Forcing (DF), Video Diffusion (VD), and Standard Diffusion (SD)—our GRWM (solid lines) consistently outperforms baselines (dashed lines), demonstrating significantly lower error accumulation over 63 steps and substantially closing the performance gap to the oracle*

具体而言，**Figure 3(a)** 展示了 Maze 3×3-DET 上的结果。神谕模型（黑色虚线）建立了误差下界，而 GRWM（实线）在三种先进的潜变量动力学模型——**Diffusion Forcing (DF)**、**Video Diffusion (VD)** 和 **Standard Diffusion (SD)**——上均持续优于对应的 VAE-WM 基线（虚线），展现出显著更低的误差累积速率。**Figure 3(b)** 和 **Figure 3(c)** 分别在更大规模的 Maze 9×9-DET 和视觉复杂度更高的 MC-DET 环境中验证了这一趋势，表明 GRWM 的几何正则化策略具有良好的跨环境泛化能力。

**Table 2**（补充材料）提供了 Maze 9×9-DET 上的感知质量指标补充。在 SSIM 指标上，GRWM 在 DF 动力学模型下达到 0.8516（基线 0.8448），在 VD 模型下提升尤为显著，从 0.5979 提升至 0.7537（+0.1558）。在 rFID 指标上，GRWM 同样展现出大幅改善：DF 模型下从 4.4345 降至 2.8729，VD 模型下从 18.1453 降至 7.2813。这些结果一致表明，几何正则化不仅降低了像素级误差，还显著提升了生成帧的感知质量。

### 定性分析：中长时序与超长时序的视觉保真度

**Figure 4** 展示了 Maze 9×9-DET 环境中中等长度滚动预测的定性对比。在第 100 帧和第 400 帧附近，GRWM 始终与真实观测保持高度相似，而基线 VAE-WM 则在粉色墙壁附近陷入困境，出现了“瞬移”现象——在视觉相似但空间位置不同的区域之间错误跳跃。这一失败模式直接印证了潜在空间几何结构紊乱导致的灾难性后果：当表示无法有效区分视觉相似但物理状态相异的场景时，动力学模型无法维持正确的轨迹。

在视觉复杂度更高的 MC-DET 环境（**Figure 5**）中，基线 VAE-WM 无法建模复杂的相机运动轨迹，在第 60 帧附近出现了明显的物体渲染错误（将石墙渲染为树木），而 GRWM 成功跟踪了复杂的运动模式，在整个序列中保持了与真实观测一致的高保真度生成。

![[assets/figures/papers/paper_list_l2453_https_arxiv_org_abs_2510_26782/figures/004_Figure_5.jpg]]
*Figure 5: Qualitative comparison of medium-horizon rollouts in MC-DET. We visualize rollouts from a baseline VAE-based world model (VAE-WM, middle) and our method (GRWM, bottom) against the ground truth (top). The baseline VAE-WM fails to model the complex camera trajectory, diverging significantly and rendering incorrect objects (e.g., trees instead of the stone wall at frame 60). Our method (GRWM) successfully tracks the complex motion and maintains high-fidelity generation consistent with the ground truth throughout the sequence*

**Figure 6** 进一步将评估推向极端——在 Maze 9×9-CE 数据集上进行了长达 10,000 步的超长时序滚动预测。基线 VAE-WM 频繁陷入生成相同颜色状态的困境，无法有效探索环境。相比之下，GRWM 产生了连贯且多样化的轨迹，成功探索了不同区域，同时保持了长期的时间一致性和结构一致性。这一结果充分证明了潜在空间几何结构对超长时序稳定性的关键支撑作用。

### 潜在空间结构分析：探测与聚类

**Table 1** 通过潜在探测（Latent Probing）实验量化了表示质量。研究者训练一个 MLP 探针，从冻结的潜在表示回归真实物理状态。GRWM 在所有三个数据集上均取得了显著更低的回归 MSE：Maze 3×3-DET 上为 0.031（VAE-WM 为 0.082），Maze 9×9-DET 上为 0.058（VAE-WM 为 0.106），MC-DET 上为 0.081（VAE-WM 为 0.137）。这表明 GRWM 的潜在表示编码了更丰富的物理状态信息，为动力学模型提供了更可靠的预测基础。

**Figure 7** 通过 K-means 聚类（k=20）直观展示了潜在空间的结构差异。每个点对应一帧，按其真实物理坐标（x, y）定位，颜色表示其被分配的聚类标签。VAE-WM（上行）的聚类呈现散乱、嘈杂的分布，空间上相距甚远的帧被错误地归入同一聚类。GRWM（下行）则展现出清晰、空间连贯的聚类结构，聚类边界与环境的物理布局高度吻合。这一可视化直接证实了时间对比正则化能够重塑潜在空间，使其与环境的真实状态流形对齐。

### Atari 环境的泛化验证

**Table 3**（补充材料）报告了在 Atari 游戏环境上的补充实验结果。在 Asterix 环境中，GRWM 将 PSNR 从 28.57 提升至 29.04，SSIM 从 0.9479 提升至 0.9518。在 Breakout 环境中，提升更为显著：PSNR 从 34.23 提升至 37.76（+3.53），SSIM 从 0.9848 提升至 0.9872。这些结果表明，尽管 GRWM 的核心设计针对确定性导航环境，其几何正则化策略在视觉风格迥异的 Atari 游戏场景中同样有效。

### 消融研究

补充材料（Section E）的消融研究验证了 GRWM 各核心组件的重要性。时间缓慢损失 $\mathcal{L}_{\mathrm{slow}}$ 和潜在均匀性损失 $\mathcal{L}_{\mathrm{uniform}}$ 均对最终性能有实质贡献，投影头（将潜在表示映射到单位超球面）也是方法有效性的关键设计。消融实验的具体数值需要查阅补充材料以获取精确数据，但现有证据（置信度 0.8）一致表明这些组件共同构成了完整的几何正则化方案。

### 失败模式与局限性

尽管 GRWM 取得了显著进展，论文坦诚地指出了若干局限性。首先，**当前方法主要针对确定性环境设计**，尚未在部分可观察、随机或高度真实感环境中验证有效性。其次，**GRWM 的生成结果中仍存在细微视觉伪影**，无法完美恢复细粒度场景细节。如 Figure 4 和 Figure 5 所示，虽然整体结构保真度大幅提升，但在纹理和边缘等细节层面仍有改进空间。第三，**与使用真实物理状态的神谕模型相比，学习到的表示仍有明显差距**，表明当前的几何正则化策略尚不足以实现近乎完美的长期预测。最后，**动力学模型本身可能仍存在局限性**，但本工作的实验设计重点突出了表示瓶颈，未全面探索动力学模型与表示学习的协同改进空间。

![[assets/figures/papers/paper_list_l2453_https_arxiv_org_abs_2510_26782/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison of medium-horizon rollouts in M9x9-DET. We visualize consecutive frames around frame 100 and frame 400. Our method (GRWM) maintains high similarity to the ground truth throughout, while the baseline VAE-WM gets trapped near the pink wall, indicating that VAE-WM tends to “teleport” between visually similar but distinct locations*

![[assets/figures/papers/paper_list_l2453_https_arxiv_org_abs_2510_26782/figures/007_Figure_7.jpg]]
*Figure 7: Visualization of latent space structure through clustering analysis. We perform k-means clustering (k = 20) on the latent representations of frames. Each point in the plots corresponds to a frame, positioned according to its true (x, y) coordinates in the environment. The (x, y) coordinates are normalized and lie within [−1, 1]. Points are colored based on their assigned latent cluster ID. The top row (VAE-WM) shows scattered, noisy clusters, indicating that spatially distant frames are incorrectly grouped together. The bottom row (GRWM) shows well-defined, spatially coherent clusters, demonstrating that our learned latent space is structurally aligned with the environment’s true state mani...*

![[assets/figures/papers/paper_list_l2453_https_arxiv_org_abs_2510_26782/figures/008_Table_1.jpg]]
*Table 1: Latent probing analysis. GRWM consistently learns representations that are more predictive of the true underlying states. We report regression MSE of an MLP probe on a held-out set (lower is better)*

![[assets/figures/papers/paper_list_l2453_https_arxiv_org_abs_2510_26782/figures/005_Figure_6.jpg]]
*Figure 6: Qualitative comparison of ultra long-horizon rollouts on the Maze 9x9-CE dataset. Frames are sampled every 1000 steps from a 10,000-step rollout. The baseline VAE-WM frequently gets stuck generating the same color states, failing to explore the environment effectively. In contrast, GRWM produces a coherent and diverse trajectory, successfully exploring different regions while preserving long-term temporal and structural consistency*

## 定位与知识库关联

### 世界模型中的表示瓶颈：从动力学建模到潜在几何结构

当前世界模型的研究重心长期集中在动力学模型的架构设计与训练范式上，包括基于RNN的状态空间模型、Transformer时序预测器、扩散模型驱动的潜变量动力学（如 **Diffusion Forcing**、**Video Diffusion**、**Standard Diffusion**）等。这些方法在中等时长的预测任务上取得了显著进展，但在长时序滚动预测中普遍面临保真度快速衰减的问题。本工作通过一个关键的诊断实验揭示了被忽视的瓶颈：**当动力学模型直接使用环境的真实物理状态时，可以实现近乎完美的长时序预测（近零帧级MSE），而使用标准VAE学习表示的同一动力学模型则误差快速累积**（Figure 1 left）。这一发现将问题的根源从动力学模型本身转移到了潜在表示空间的几何结构上。

### GRWM 的方法定位：时间对比学习作为几何正则化

GRWM（Geometrically-Regularized World Models）的核心贡献在于**将时间对比学习重新定位为世界模型自动编码器的几何正则化器**，而非单纯的表征学习目标。其方法论谱系可追溯至两条线索：

- **时间对比学习**：借鉴了时间缓慢性先验（temporal slowness prior）和对比表征学习的思想，通过强制同一轨迹窗口内的帧嵌入在单位超球面上彼此靠近（$\mathcal{L}_{\mathrm{slow}}$），同时最大化不同轨迹嵌入之间的均匀分布（$\mathcal{L}_{\mathrm{uniform}}$），为潜在空间注入物理状态流形应有的几何归纳偏置。
- **即插即用的模块化设计**：GRWM 以轻量级正则化模块的形式嵌入标准自动编码器训练流程，与具体的动力学模型架构解耦。实验表明，该方法在 **Diffusion Forcing**、**Video Diffusion** 和 **Standard Diffusion** 三种先进的潜变量动力学模型上均能一致提升滚动预测性能（Figure 3），验证了其作为通用表示增强组件的有效性。

### 与基线方法的性能边界

在 Maze 9×9-DET 环境上的感知指标评估（Table 2）揭示了 GRWM 在不同动力学后端下的增益模式：

- **Diffusion Forcing + GRWM**：SSIM 从 0.8448 提升至 0.8516（+0.0068），rFID 从 4.4345 降至 2.8729（-1.5616），在所有配置中取得了最优的绝对性能。
- **Video Diffusion + GRWM**：SSIM 从 0.5979 提升至 0.7537（+0.1558），rFID 从 18.1453 降至 7.2813（-10.8640），相对增益最为显著，表明 Video Diffusion 对表示质量的敏感度最高。
- **Standard Diffusion + GRWM**：SSIM 从 0.8367 微升至 0.8369（+0.0002），rFID 从 6.4686 降至 4.5200（-1.9486），在重建精度接近饱和的情况下仍实现了感知质量的明显改善。

在 Atari 环境的补充实验（Table 3）中，GRWM 在 Asterix 和 Breakout 上分别实现了 PSNR +0.47 和 +3.53 的提升，进一步验证了该方法在视觉复杂场景下的迁移能力。

### 潜在空间几何的结构性证据

GRWM 的有效性根植于其对潜在空间几何的重塑。**潜在探测分析**（Table 1）表明，GRWM 学习到的表示对真实物理状态的回归 MSE 在三个环境中均显著低于 VAE-WM（M3×3-DET: 0.031 vs 0.082；M9×9-DET: 0.058 vs 0.106；MC-DET: 0.081 vs 0.137），说明几何正则化使潜在编码保留了更丰富的状态信息。**聚类可视化**（Figure 7）进一步揭示了结构差异：VAE-WM 的潜在聚类在物理空间中呈散乱噪声分布，空间上相距甚远的帧被错误地归入同一聚类；而 GRWM 的聚类在物理坐标上形成空间连贯的簇，表明其潜在空间与环境的真实状态流形实现了结构对齐。

### 适用边界与已知局限

GRWM 的当前设计存在以下明确的适用边界：

1. **确定性环境的假设**：本工作主要针对完全可观察的确定性环境（Maze、Minecraft-DET）进行验证。在部分可观察、随机动态或高度真实感环境中的有效性尚未得到实验支撑，这是一个需要后续工作验证的开放问题。
2. **与神谕模型的性能差距**：尽管 GRWM 显著缩小了与使用真实物理状态的神谕模型之间的差距，但学习到的表示仍存在明显不足（Figure 3 中各环境中 GRWM 曲线与黑色虚线的距离），表明当前的几何正则化强度尚不足以实现近乎完美的长期预测保真度。
3. **细粒度视觉伪影**：在定性结果中（Figure 4、Figure 5），GRWM 的生成结果仍存在细微的视觉伪影，无法完美恢复细粒度场景细节（如 MC-DET 中的纹理一致性）。
4. **动力学模型本身的局限性未充分探索**：本工作的实验设计聚焦于隔离表示瓶颈，因此未系统研究动力学模型架构的改进空间。GRWM 与 Transformer、图神经网络等其他动力学后端的组合效果仍待探索。

### 开放问题与后续方向

- **跨域泛化**：如何将几何正则化的思想扩展到部分可观察环境（需要处理信念状态）、随机环境（需要建模不确定性）以及真实感视觉环境（需要处理高维复杂纹理）中？
- **更强的表示约束**：能否设计更强大的表示学习方法（如引入因果结构约束或物理先验），进一步缩小与神谕模型的性能差距？
- **动力学模型协同设计**：时间对比约束与其他动力学模型（如 Transformer 预测器、图神经网络状态空间模型）结合时，能否产生超越当前扩散模型基线的世界模型？
- **在线与持续学习场景**：在在线强化学习或持续环境变化的情境下，如何有效度量和动态维护潜在空间的几何结构？

## 原文 PDF

![[paperPDFs/CVPR_2026/Cloning_Deterministic_Worlds_The_Critical_Role_of_Latent_Geometry_in_Long_Horizon_World_Models.pdf]]
