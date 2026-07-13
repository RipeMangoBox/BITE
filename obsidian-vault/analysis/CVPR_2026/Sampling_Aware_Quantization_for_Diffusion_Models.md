---
title: Sampling-Aware Quantization for Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Sampling_Aware_Quantization_for_Diffusion_Models.pdf
project_link: null
code_link: "https://github.com/TaylorJocelyn/Sampling-aware-Quantization"
aliases:
- SAQSPSQ
- SAQDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 混合阶轨迹对齐（Mixed-Order Trajectory Alignment）策略，通过约束低阶与高阶采样方向的一致性，线性化概率流。
primary_logic: 量化造成的方向偏差通过高阶项累积，将确定性概率流ODE转变为发散性SDE；对齐不同阶数的采样轨迹可以迫使量化误差与离散化误差同阶，从而抑制累积。
claims:
- 量化网络引起的误差序列在积分中累积，形成主导项。
- 混合阶轨迹对齐通过匹配一阶和二阶方向估计，线性化采样路径。
- 消融实验表明MOTA模块能显著降低FID和sFID。
- LSUN-Churches 256×256 上 FID = SA-PTQ (W8A8)
---

# Sampling-Aware Quantization for Diffusion Models

> [!tip] 核心洞察
> 量化造成的方向偏差通过高阶项累积，将确定性概率流ODE转变为发散性SDE；对齐不同阶数的采样轨迹可以迫使量化误差与离散化误差同阶，从而抑制累积。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向扩散模型的采样感知量化 |
| 英文题名 | Sampling-Aware Quantization for Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.02242) · [Code](https://github.com/TaylorJocelyn/Sampling-aware-Quantization) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | Sampling-Aware Quantization (SA-PTQ and SA-QLoRA) |
| Dataset | LSUN-Churches 256×256, LSUN-Bedroom 256×256, ImageNet 256×256 |

> [!tip] 效果简介
> - LSUN-Churches 256×256 上，FID SA-PTQ (W8A8) vs PTQD (W8A8) (-1.22)；FID SA-QLoRA (W4A4) vs EfficientDM (W4A4) (-5.53)。
> - LSUN-Bedroom 256×256 上，FID SA-PTQ (W8A8) vs PTQD (W8A8) (-0.48)；sFID SA-QLoRA (W4A4) vs EfficientDM (W4A4) (-4.44)。
> - ImageNet 256×256 (20 steps) 上，FID SA-QLoRA vs FP32 (接近全精度)。

## 概要

扩散模型在图像生成任务上表现卓越，但其巨大的计算开销严重制约了实际部署效率。通过量化压缩网络权重与激活值是加速推理的常见手段，然而现有量化方法在扩散模型上普遍失效——根本瓶颈在于：**量化噪声会干扰高阶采样器的方向估计，导致快速采样轨迹发生系统性偏离，误差在积分过程中持续累积并最终主导总误差**。

针对这一瓶颈，本文提出**采样感知量化（Sampling-Aware Quantization）**策略，核心思路是通过**混合阶轨迹对齐（Mixed-Order Trajectory Alignment）**约束低阶与高阶采样方向的一致性，从而线性化概率流、将量化累积误差压制至与离散化截断误差同阶。在此基础上，作者将该策略分别适配到训练后量化与QLoRA微调范式，形成**SA-PTQ**与**SA-QLoRA**两种变体。

实验覆盖类别条件生成（ImageNet 256×256）、无条件生成（LSUN-Bedroom/Churches 256×256）以及文本引导生成（MS-COCO 512×512）等多种场景。在稀疏步快速采样设定下，SA-PTQ在W8A8配置下相较PTQD将FID降低0.5–1.2，SA-QLoRA在W4A4配置下相较EfficientDM将FID降低约5.5。消融实验进一步证实混合阶轨迹对齐模块对FID与sFID均有显著增益。整体而言，该方法在保持快速采样收敛特性的同时，显著缩小了量化模型与全精度模型之间的生成质量差距。

扩散模型已在图像生成领域取得显著进展，但其推理过程需要反复执行去噪网络的前向传播，计算开销极大。为降低部署成本，网络量化成为自然选择——将浮点权重与激活值映射为低位宽定点表示，从而压缩模型体积并加速推理。

然而，直接对扩散模型应用标准量化方案会导致生成质量严重退化。这一退化在**稀疏步数快速采样**场景下尤为突出：当采样步数从数百步缩减至20步甚至更少时，量化模型的FID指标急剧上升，与全精度模型的差距被显著放大。现有量化方法（如PTQ4DM、Q-Diffusion、PTQD、EfficientDM）主要关注单步重建误差的最小化，却忽视了量化噪声在**多步采样轨迹中的累积效应**。

本文通过分析快速采样的数学原理，揭示了这一累积效应的根本机制。扩散模型的反向采样可统一描述为概率流常微分方程（ODE）的数值积分，而高阶快速采样器（如DPM-Solver-2）通过对噪声估计网络进行高阶泰勒展开来逼近采样方向。当量化引入的误差序列沿积分路径累积后，会形成一个与步长成正比的主导项，其量级为 $\mathcal{O}(\delta \cdot e^{-\lambda_s} \cdot (\lambda_t - \lambda_s))$，其中 $\delta$ 表征量化误差幅度。该累积项与离散化截断误差 $\mathcal{O}((\lambda_t - \lambda_s)^{k+1})$ 共同构成总误差上界。在稀疏步数采样下，步长 $(\lambda_t - \lambda_s)$ 增大，量化累积误差迅速膨胀，成为总误差的主导来源。

从几何角度看，量化造成的方向偏差通过高阶项的反复迭代，将原本确定性的概率流ODE转变为具有发散特性的随机微分方程（SDE），导致采样轨迹偏离真实数据分布。图2直观展示了这一过程：一阶采样器仅在区间起点进行一次方向估计，而二阶采样器通过中间步骤细化方向；量化误差使这些中间步骤的方向估计发生漂移，最终污染整个区间的采样方向。

上述分析表明，**现有量化方法的根本缺口在于缺乏对采样过程的感知**——它们在校准和优化阶段仅考虑单点重建精度，未能约束量化模型在不同阶数采样轨迹下的行为一致性。这促使本文提出**采样感知量化**框架，其核心动机是通过对齐低阶与高阶采样方向，线性化概率流，从而将量化累积误差压制至与离散化误差同阶的水平。

## 核心方法与创新机理

本文的核心创新在于首次从**采样加速原理**的角度审视扩散模型量化问题，揭示了量化误差对高阶快速采样器的破坏性机制，并据此提出了**采样感知量化（Sampling-Aware Quantization）**框架。该框架包含两个具体变体：面向后训练量化的**SA-PTQ**和面向参数高效微调的**SA-QLoRA**。

### 瓶颈洞察：量化噪声如何破坏快速采样

扩散模型的快速采样（如DPM-Solver）依赖于对噪声估计网络进行**高阶泰勒展开**，通过在采样区间内引入中间节点来精细化方向估计（Figure 2b）。然而，量化网络引入的噪声 $\Delta \epsilon_{\theta}$ 会沿积分路径累积，形成一个**量化累积误差项**：

$$\Delta_{quant} = \sum_{n=0}^{k-1} \Delta \epsilon_{\theta}^{(n)}(\mathbf{x}_{\lambda_s}, \lambda_s) \int_{\lambda_s}^{\lambda_t} e^{-\lambda} \cdot \frac{(\lambda - \lambda_s)^n}{n!} \mathrm{d}\lambda$$

该误差项与离散化截断误差共同构成总误差上界：

$$\mathcal{L}_{\Delta} = \mathcal{O}(\delta \cdot e^{-\lambda_s} \cdot (\lambda_t - \lambda_s)) + \mathcal{O}((\lambda_t - \lambda_s)^{k+1})$$

其中 $\delta$ 直接控制量化累积误差。分析表明，**量化累积误差主导了总误差**，使得原本确定性的概率流ODE变为发散性SDE，严重破坏快速采样的收敛性（Figure 2c）。这一发现解释了为何现有量化方法在稀疏步数采样下性能急剧退化。

### 核心机制：混合阶轨迹对齐（Mixed-Order Trajectory Alignment）

为解决上述问题，本文提出**混合阶轨迹对齐（MOTA）**策略。其核心思想是：通过约束量化网络的一阶采样方向与全精度网络的高阶采样方向在中间节点处保持一致，**线性化概率流轨迹**（Figure 2d），从而使量化误差与离散化误差保持同阶，抑制累积效应。

具体而言，MOTA的优化目标为：

$$\arg\min_{s,z} \mathbb{E}_{(\mathbf{x}_t,t)\sim\mathcal{D}, (\mathbf{x}_s,s)\sim\mathcal{S}} \| \hat{\epsilon}_{\theta}(\mathbf{x}_{\lambda_s}, \lambda_s) - \epsilon_{\theta}(\mathbf{x}_{\lambda_t}, \lambda_t) \|^2$$

与传统量化方法仅在同一输入下对齐全精度与量化输出不同，MOTA**跨时间步对齐不同阶数的方向估计**，从根本上修正了量化引入的方向偏差。

### 关键Changed Slots：与传统量化方法的本质差异

相较于PTQ4DM、Q-Diffusion、PTQD、EfficientDM等基线方法，本文在三个关键维度上进行了系统性改造：

| 改造维度 | 基线方法 | 本文方法 | 机制作用 |
|---------|---------|---------|---------|
| **校准数据采集** | 标准图像分布采样 | 双阶轨迹采样（一阶和二阶采样点） | 使校准数据覆盖高阶采样器实际访问的中间状态分布 |
| **重建损失** | 全精度与量化模块在同一输入下的MSE | 全精度一阶点输出与量化二阶点输出的MSE | 强制模块在跨阶条件下保持输出一致性 |
| **训练损失** | 量化与全精度噪声预测的MSE+余弦相似度 | 额外加入混合阶轨迹对齐损失 $\mathcal{L}_{MOTA}$ | 直接约束量化模型的高阶方向估计与全精度对齐 |

在SA-QLoRA中，总损失进一步整合了方向约束 $\mathcal{L}_{COS}$ 和轨迹对齐损失 $\mathcal{L}_{MOTA}$：

$$\arg\min_{w,s,z} \mathcal{L}_{COS} + \mathcal{L}_{MOTA}$$

消融实验（Table 4）证实了各模块的独立贡献：MOTA模块相较于基线BRECQ降低FID 4.1、sFID 3.83；额外加入方向对齐约束 $\mathcal{L}_{COS}$ 后，FID再降0.95、sFID降0.31，验证了混合阶对齐与方向约束的协同效应。

本文提出的**采样感知量化（Sampling-Aware Quantization）**框架，其核心设计动机源于一个关键观察：量化噪声对高阶采样器的方向估计产生干扰，导致快速采样轨迹偏离，误差在高阶项中持续累积，最终使确定性概率流ODE退化为发散性SDE。为应对这一瓶颈，框架通过**混合阶轨迹对齐（Mixed-Order Trajectory Alignment, MOTA）**策略，约束低阶与高阶采样方向的一致性，从而线性化概率流，迫使量化误差与离散化误差保持同阶，抑制误差累积。

基于这一核心策略，框架衍生出两种适配不同部署场景的变体：

- **SA-PTQ**：面向训练后量化（Post-Training Quantization）场景，无需反向传播训练，通过双阶轨迹校准实现模块级重建。
- **SA-QLoRA**：面向低比特微调场景，将MOTA与QLoRA结合，引入方向约束损失进行联合优化。

两种变体共享统一的采样感知设计理念，但在校准数据构造、损失函数和优化流程上存在差异，下文分别阐述。

### SA-PTQ 流程

SA-PTQ 的工作流程如 Figure 3a 所示，包含两个核心阶段：

**1. 双阶轨迹采样（Dual-order Trajectory Sampling）**

传统PTQ方法在校准时通常从标准图像分布中采样，而SA-PTQ改为从**采样轨迹**中采集校准数据。具体而言，对于每个采样步，同时记录一阶采样点 $\mathbf{x}_{t_j}$ 和二阶采样点 $\mathbf{x}_{s_j}$（见 Algorithm 1: DPM-Solver-2），构成双阶轨迹样本对 $(t_j, s_j)$。这种采样方式使校准数据天然携带采样器在不同阶数下的方向信息。

**2. 混合阶轨迹对齐校准（Mixed-Order Trajectory Alignment Calibration）**

在模块级重建阶段，对于待量化的模块 $\hat{f}_i(\cdot)$，SA-PTQ不再使用传统MSE（即全精度与量化模块在同一输入下的输出差异），而是采用跨阶对齐目标：将全精度模块在一阶点 $\mathbf{x}_{t_j}$ 的输出，与量化模块在对应二阶点 $\mathbf{x}_{s_j}$ 的输出进行对齐。其重建损失为：

$$\arg\min_{\alpha} \mathbb{E}_{(t_j, s_j)} \| f_i(\mathbf{x}_{t_j}, t_j, cond) - \hat{f}_i(\mathbf{x}_{s_j}, s_j, cond) \|^2$$

其中 $\alpha$ 为量化参数。这一设计迫使量化模块在二阶采样点的输出，逼近全精度模块在一阶采样点的输出，从而隐式地实现了混合阶轨迹对齐。

### SA-QLoRA 流程

SA-QLoRA 在 QLoRA 的基础上引入采样感知约束，工作流程如 Figure 3b 所示。在每一步采样后，LoRA 权重 $W_{LoRA}$ 和量化参数 $s, z$ 被迭代更新。其训练目标由两项损失联合构成：

**方向约束损失 $\mathcal{L}_{COS}$**：强制量化模型与全精度模型的噪声预测方向一致：

$$\mathcal{L}_{COS} = 1 - \frac{\langle \epsilon_{\theta}(\mathbf{x}_{t_i}, t_i), \hat{\epsilon}_{\theta}(\mathbf{x}_{s_i}, s_i) \rangle}{\| \epsilon_{\theta}(\mathbf{x}_{t_i}, t_i) \| \| \hat{\epsilon}_{\theta}(\mathbf{x}_{t_i}, t_i) \|}$$

**轨迹对齐损失 $\mathcal{L}_{MOTA}$**：直接对齐量化二阶点输出与全精度一阶点输出：

$$\mathcal{L}_{MOTA} = \mathbb{E}_{(t_i, s_i)} \| \hat{\epsilon}_{\theta}(\mathbf{x}_{s_i}, s_i) - \epsilon_{\theta}(\mathbf{x}_{t_i}, t_i) \|^2$$

SA-QLoRA 的总优化目标为两者的联合：

$$\arg\min_{w,s,z} \mathcal{L}_{COS} + \mathcal{L}_{MOTA}$$

### 框架统一性

两种变体的共同本质在于：**将量化校准/训练的数据分布从“图像空间”迁移到“采样轨迹空间”**，并通过混合阶对齐约束，使量化模型在快速采样场景下的方向估计偏差得到显式控制。消融实验（Table 4）证实，MOTA模块相较于基线BRECQ可降低FID 4.1、sFID 3.83；额外加入方向对齐约束 $\mathcal{L}_{COS}$ 后，FID再降0.95，sFID降0.31，验证了各模块的独立贡献。

### 量化误差的累积机制

扩散模型的反向采样依赖于对噪声估计网络 $\epsilon_{\theta}$ 的高阶泰勒展开来近似采样方向。当网络被量化后，量化噪声 $\Delta\epsilon_{\theta}$ 会通过积分累积，形成主导性的误差项。

量化后的数值积分可表示为：

$$
\mathbf{x}_t = \frac{\alpha_t}{\alpha_s} \mathbf{x}_s - \alpha_t \sum_{n=0}^{k-1} \hat{\epsilon}_{\theta}^{(n)}(\mathbf{x}_{\lambda_s}, \lambda_s) \int_{\lambda_s}^{\lambda_t} e^{-\lambda} \cdot \frac{(\lambda - \lambda_s)^n}{n!} \mathrm{d}\lambda + \mathcal{O}((\lambda_t - \lambda_s)^{k+1})
$$

其中 $\hat{\epsilon}_{\theta} = \epsilon_{\theta} + \Delta\epsilon_{\theta}$。由此导出的量化累积误差项为：

$$
\Delta_{quant} = \sum_{n=0}^{k-1} \Delta\epsilon_{\theta}^{(n)}(\mathbf{x}_{\lambda_s}, \lambda_s) \int_{\lambda_s}^{\lambda_t} e^{-\lambda} \cdot \frac{(\lambda - \lambda_s)^n}{n!} \mathrm{d}\lambda
$$

总误差上界由量化累积误差与离散化截断误差共同构成：

$$
\mathcal{L}_{\Delta} = \mathcal{O}(\delta \cdot e^{-\lambda_s} \cdot (\lambda_t - \lambda_s)) + \mathcal{O}((\lambda_t - \lambda_s)^{k+1})
$$

其中 $\delta$ 为量化噪声幅值。**分析表明，量化累积误差（第一项）直接受 $\delta$ 控制，成为总误差的主导项**，严重破坏 ODE 采样的快速收敛性。这意味着量化不仅引入逐点扰动，更通过高阶项在积分过程中将确定性概率流 ODE 转变为发散性 SDE 行为（Fig. 2c）。

### 混合阶轨迹对齐（Mixed-Order Trajectory Alignment）

核心思路：**约束量化网络的一阶采样方向与全精度网络的高阶采样方向对齐**，使量化误差与离散化误差同阶，从而抑制累积。

对于二阶采样器（如 DPM-Solver-2），采样过程包含中间节点 $s_i$ 和终点 $t_i$。传统量化目标仅对齐同一输入下的全精度与量化输出：

$$
\arg\min_{s,z} \mathbb{E}_{(\mathbf{x}_t,t)\sim\mathcal{D}} \| \epsilon_{\theta}(\mathbf{x}_t,t) - \hat{\epsilon}_{\theta}(\mathbf{x}_t,t) \|^2
$$

而混合阶轨迹对齐将目标改为：

$$
\arg\min_{s,z} \mathbb{E}_{(\mathbf{x}_t,t)\sim\mathcal{D}, (\mathbf{x}_s,s)\sim\mathcal{S}} \| \hat{\epsilon}_{\theta}(\mathbf{x}_{\lambda_s}, \lambda_s) - \epsilon_{\theta}(\mathbf{x}_{\lambda_t}, \lambda_t) \|^2
$$

**即用量化网络在一阶采样点 $\mathbf{x}_s$ 的输出，去匹配全精度网络在二阶采样点 $\mathbf{x}_t$ 的输出**。这一对齐迫使量化后的概率流轨迹线性化（Fig. 2d），使量化误差不再通过高阶项放大。

### SA-PTQ：双阶轨迹校准

SA-PTQ 将混合阶对齐思想嵌入模块级重建流程（Fig. 3a），包含两个关键组件：

**双阶轨迹采样**：从二阶采样器（DPM-Solver-2）的轨迹中同时采集一阶点 $(t_j, \mathbf{x}_{t_j})$ 和二阶点 $(s_j, \mathbf{x}_{s_j})$ 作为校准数据。

**混合阶轨迹对齐校准**：对每个待量化模块 $f_i$，最小化全精度模块在一阶点的输出与量化模块在二阶点的输出之间的 MSE：

$$
\arg\min_{\alpha} \mathbb{E}_{(t_j, s_j)} \| f_i(\mathbf{x}_{t_j}, t_j, cond) - \hat{f}_i(\mathbf{x}_{s_j}, s_j, cond) \|^2
$$

### SA-QLoRA：方向约束与轨迹对齐联合优化

SA-QLoRA 在 QLoRA 微调框架中引入两个损失项（Fig. 3b）：

**方向约束损失 $\mathcal{L}_{COS}$**：强制量化网络与全精度网络的噪声预测方向一致：

$$
\mathcal{L}_{COS} = 1 - \frac{\langle \epsilon_{\theta}(\mathbf{x}_{t_i}, t_i), \hat{\epsilon}_{\theta}(\mathbf{x}_{s_i}, s_i) \rangle}{\| \epsilon_{\theta}(\mathbf{x}_{t_i}, t_i) \| \| \hat{\epsilon}_{\theta}(\mathbf{x}_{t_i}, t_i) \|}
$$

**轨迹对齐损失 $\mathcal{L}_{MOTA}$**：直接对齐量化一阶输出与全精度高阶输出：

$$
\mathcal{L}_{MOTA} = \mathbb{E}_{(t_i, s_i)} \| \hat{\epsilon}_{\theta}(\mathbf{x}_{s_i}, s_i) - \epsilon_{\theta}(\mathbf{x}_{t_i}, t_i) \|^2
$$

SA-QLoRA 的总优化目标为：

$$
\arg\min_{w,s,z} \mathcal{L}_{COS} + \mathcal{L}_{MOTA}
$$

其中 $w$ 为 LoRA 权重，$s$、$z$ 为量化参数。

### 模块关系总结

| 模块 | 功能 | 作用阶段 |
|------|------|----------|
| 双阶轨迹采样 | 生成一阶和二阶采样点对 | 校准数据准备 |
| 混合阶轨迹对齐校准 | 指导模块重建以对齐不同阶输出 | SA-PTQ 重建 |
| $\mathcal{L}_{MOTA}$ | 混合阶轨迹对齐损失 | SA-QLoRA 训练 |
| $\mathcal{L}_{COS}$ | 余弦相似度方向约束 | SA-QLoRA 训练 |

消融实验（Table 4）验证了 MOTA 模块的有效性：相比基础 BRECQ 重建，MOTA 使 FID 降低 4.1、sFID 降低 3.83；额外加入 $\mathcal{L}_{COS}$ 后 FID 再降 0.95。

## 实验与关键发现

### 瓶颈验证：量化误差如何破坏快速采样

量化扩散模型的根本瓶颈并非简单的逐层输出失真，而是**量化噪声通过高阶采样器的方向估计机制发生系统性累积**。在确定性概率流ODE（Eqn. 4）的快速采样中，高阶求解器（如DPM-Solver-2）会在一个采样区间内进行多次中间方向估计以逼近真实轨迹。量化网络引入的噪声 $\Delta \epsilon_{\theta}$ 使这些中间估计发生偏移，导致误差在积分过程中逐项累积，形成主导项：

$$\Delta_{quant} = \sum_{n=0}^{k-1} \Delta \epsilon_{\theta}^{(n)}(\mathbf{x}_{\lambda_s}, \lambda_s) \int_{\lambda_s}^{\lambda_t} e^{-\lambda} \cdot \frac{(\lambda - \lambda_s)^n}{n!} \mathrm{d}\lambda$$

总误差上界 $\mathcal{L}_{\Delta} = \mathcal{O}(\delta \cdot e^{-\lambda_s} \cdot (\lambda_t - \lambda_s)) + \mathcal{O}((\lambda_t - \lambda_s)^{k+1})$ 表明，量化累积误差（第一项）直接受量化噪声幅度 $\delta$ 控制，其量级远大于离散化截断误差（第二项），成为快速采样质量下降的主因。从轨迹角度看，量化使得原本确定性的概率流ODE退化为发散性的随机行为（图2c），中间采样点发生位置偏移，最终方向估计偏离真实路径。

### 主实验结果

#### 类别条件生成（ImageNet 256×256）

Table 1 展示了 LDM-4 在 20 步 DPM-Solver-2 采样下的类别条件生成性能。在 W8A8 设定下，SA-PTQ 的 FID 与全精度模型差距极小，显著优于 PTQ4DM、Q-Diffusion、PTQD 等基线。在更具挑战性的 W4A4 低比特场景，SA-QLoRA 的 FID 接近全精度水平，而 EfficientDM 等同位宽方法则出现明显退化。Figure 6 和 Figure 7 的可视化对比进一步证实：SA-QLoRA 在 W8A8 和 W4A4 下均能保持与全精度高度一致的生成质量，基线方法则出现纹理模糊或结构失真。

![[assets/figures/papers/paper_list_l928_https_arxiv_org_abs_2505_02242/figures/011_Figure_6.jpg]]
*Figure 6: Comparison of generative performance on the ImageNet 256×256 dataset with 20-step sampling among the full-precision LDM4 and its W8A8 quantized counterparts using PTQ4DM, Q-diffusion, PTQD, EfficientDM, and our proposed SA-LoRA. (Revised version of the main figure in the main text, supplemented with the names of the applied quantization algorithms.)*

![[assets/figures/papers/paper_list_l928_https_arxiv_org_abs_2505_02242/figures/012_Figure_7.jpg]]
*Figure 7: Comparison of generative performance on the ImageNet 256×256 dataset with 20-step sampling among the full-precision LDM4 and its W4A4 quantized counterparts using PTQ4DM, Q-diffusion, PTQD, EfficientDM, and our proposed SA-LoRA. (Revised version of the main figure in the main text, supplemented with the names of the applied quantization algorithms.)*

#### 无条件生成（LSUN-Bedroom 和 LSUN-Church）

在 LSUN-Bedroom 256×256 上（Table 2），SA-PTQ（W8A8）的 FID 较 PTQD 降低 0.48；SA-QLoRA（W4A4）的 sFID 较 EfficientDM 大幅降低 4.44。在 LSUN-Church 256×256 上（Table 5），SA-PTQ（W8A8）FID 较 PTQD 降低 1.22；SA-QLoRA（W4A4）FID 较 EfficientDM 降低 5.53，优势更为显著。Figure 8 和 Figure 11 的样本对比显示，SA-QLoRA 在 W4A8 下生成的教堂和卧室图像与全精度 LDM-8/LDM-4 几乎无法区分。

![[assets/figures/papers/paper_list_l928_https_arxiv_org_abs_2505_02242/figures/005_Table_2.jpg]]
*Table 2: Performance comparisons of unconditional image generation on LSUN-Bedroom 256 × 256*

![[assets/figures/papers/paper_list_l928_https_arxiv_org_abs_2505_02242/figures/009_Table_5.jpg]]
*Table 5: Performance comparisons of unconditional image generation on LSUN-Church*

![[assets/figures/papers/paper_list_l928_https_arxiv_org_abs_2505_02242/figures/013_Figure_8.jpg]]
*Figure 8: Comparison of generative performance between the full-precision LDM8 and its W4A8 quantized counterpart, utilizing our proposed SA-QLoRA, on the LSUN-Church 256×256 dataset under 50-step sampling*

#### 文本引导生成（MS-COCO 512×512）

Table 3 的结果表明，SA-QLoRA 在文本引导的 512×512 高分辨率生成任务上同样有效。Figure 12 展示了具体生成案例（如“戴帽子的小狗”和“躺在绿草地上的柯基”），量化模型准确保留了文本语义和视觉细节。

### 消融实验：混合阶轨迹对齐的关键作用

Table 4 的消融实验直接验证了 MOTA 模块和方向约束 $\mathcal{L}_{COS}$ 的贡献。以 BRECQ（仅使用标准 MSE 重建）为基线：

![[assets/figures/papers/paper_list_l928_https_arxiv_org_abs_2505_02242/figures/007_Table_4.jpg]]
*Table 4: Ablation study of the sampling-aware quantization components using LDM-4 (scale = 1.5, step = 20) on the ImageNet 256 × 256*

- **加入 MOTA 模块**：FID 降低 4.1，sFID 降低 3.83。这表明仅通过混合阶轨迹对齐校准就能大幅抑制量化累积误差。
- **进一步加入方向对齐约束 $\mathcal{L}_{COS}$**：FID 再降 0.95，sFID 再降 0.31。余弦相似度损失强制量化模型的方向估计与全精度模型保持一致，进一步线性化概率流（图2d），使快速采样轨迹更稳定。

### 方法谱系与知识库定位

本工作针对**扩散模型后训练量化（PTQ）与参数高效微调量化（QLoRA）**场景，与现有方法的关键差异体现在三个维度：

1. **校准数据采集**：传统方法（PTQ4DM、Q-Diffusion、PTQD）从标准图像分布采样校准数据；本方法采用**双阶轨迹采样**，同时采集一阶和二阶采样点，使校准数据覆盖高阶求解器的实际运行轨迹。
2. **重建损失**：基线方法使用全精度与量化模块在**同一输入**下的 MSE；SA-PTQ 使用全精度一阶点输出与量化二阶点输出的 MSE（Eqn. 15），实现跨阶轨迹对齐。
3. **训练损失**：SA-QLoRA 在标准量化-全精度噪声预测 MSE + 余弦相似度损失基础上，额外加入**混合阶轨迹对齐损失 $\mathcal{L}_{MOTA}$**（Eqn. 19），将轨迹对齐从校准阶段延伸到微调阶段。

与 EfficientDM 等低比特量化方法相比，SA-QLoRA 不依赖复杂的混合精度分配或逐层敏感度分析，而是通过采样原理层面的误差控制实现更优的低比特性能。

### 局限性

论文未明确讨论方法在以下场景的表现：极端低比特（如 W2A2）、非 DPM-Solver 系列的其他高阶求解器兼容性、以及更大规模模型（如 SDXL）上的扩展性。这些方面需要进一步验证。

## 定位与知识库关联

### 问题定位：量化误差与采样动力学的失配

本文的核心洞察在于揭示了一个此前被忽视的瓶颈：**量化噪声并非均匀地损害扩散模型，而是通过高阶采样器的方向估计机制产生累积性偏差**。具体而言，量化网络引入的误差序列在数值积分中形成主导项，将原本确定性的概率流ODE转变为发散性SDE，导致快速采样轨迹偏离（见Eqn. (9)–(10)）。这一发现将扩散模型量化的研究焦点从“逐层重建精度”转向了“采样动力学稳定性”。

### 与基线方法的关系

**PTQ4DM** 和 **Q-Diffusion** 代表了扩散模型后训练量化的早期尝试，其核心策略是沿用在图像分类中成熟的逐层重建或校准集对齐方法，未考虑采样过程中误差的时序累积特性。**PTQD** 则进一步引入了量化误差的显式修正，但其修正目标仍局限于单步噪声预测的MSE，缺乏对高阶采样器方向估计偏差的约束。

本文提出的 **采样感知量化（Sampling-Aware Quantization）** 在三个关键环节实现了突破：

1. **校准数据采集**：从标准图像分布采样转向**双阶轨迹采样**（一阶和二阶采样点），使校准数据分布与高阶采样器的实际运行轨迹匹配（Sec 4.2）。
2. **重建损失定义**：将损失从“全精度与量化模块在同一输入下的MSE”重构为“全精度一阶点输出与量化二阶点输出的MSE”，直接对齐不同阶数的方向估计（Eqn. (15)）。
3. **训练损失扩展**：在量化与全精度噪声预测的MSE+余弦相似度基础上，额外加入**混合阶轨迹对齐损失 $\mathcal{L}_{MOTA}$**，约束低阶与高阶采样方向的一致性（Eqn. (19)–(20)）。

在低比特场景下，**EfficientDM** 作为W4A4量化的代表性基线，其性能在LSUN-Churches上被SA-QLoRA以FID降低5.53的幅度显著超越（Table 5），验证了采样感知策略在极限量化下的有效性。

### 方法谱系中的位置

从技术谱系来看，本文的方法处于**量化感知训练（QAT）** 与**扩散模型采样加速**的交叉地带。其核心贡献——混合阶轨迹对齐（Mixed-Order Trajectory Alignment）——本质上是一种**线性化概率流的约束策略**，通过强制量化误差与离散化误差同阶来抑制累积。这一思路与扩散模型加速采样中“高阶展开”和“轨迹线性化”的理论框架一脉相承，但将其首次应用于量化误差的建模与控制。

SA-PTQ和SA-QLoRA分别覆盖了PTQ和QLoRA两种主流量化范式，形成了从轻量级校准到微调优化的完整方案。这种双轨设计使其适用于不同的部署约束：SA-PTQ无需训练数据，适合快速部署；SA-QLoRA则通过LoRA微调进一步补偿量化损失，在W4A4等极限位宽下保持生成质量。

### 适用边界与局限

**适用边界**：
- 方法的核心假设是采样器采用高阶数值积分（如DPM-Solver-2），其有效性在稀疏步数（如20步）快速采样场景下最为显著。当采样步数足够多、离散化误差本身已很小时，量化累积误差的相对贡献降低，方法的增益可能减弱。
- 实验覆盖了类别条件生成（ImageNet 256×256）、无条件生成（LSUN-Bedroom/Churches）和文本引导生成（MS-COCO 512×512）三类任务，表明方法对条件类型不敏感。

**需验证的局限**：
- 论文未提供在极端低步数（如5–10步）下的性能数据，此时离散化误差与量化误差的交互可能更为复杂。
- 对于非DPM-Solver系列的其他高阶采样器（如UniPC、DEIS），混合阶对齐策略的通用性需要进一步验证。
- 在更大规模模型（如SDXL、Stable Diffusion 3）上的可扩展性未经验证，尽管QLoRA的框架本身支持参数高效微调。

### 开放问题

1. **误差界的紧致性**：Eqn. (10) 给出的误差上界 $\mathcal{L}_{\Delta} = \mathcal{O}(\delta \cdot e^{-\lambda_s} \cdot (\lambda_t - \lambda_s)) + \mathcal{O}((\lambda_t - \lambda_s)^{k+1})$ 揭示了量化误差与离散化误差的加性关系，但两项之间的耦合效应（如量化误差是否会影响高阶项的截断误差）未被深入分析。

2. **采样器阶数与对齐策略的适配**：当前方法以二阶采样器（DPM-Solver-2）为对齐目标，对于三阶或更高阶采样器，是否需要对齐更多中间节点？对齐策略的扩展代价与收益尚不明确。

3. **时间步依赖的量化敏感性**：扩散模型在不同时间步对量化的敏感性可能存在差异（如噪声水平高时容错性更强），是否可以通过时间步自适应的量化位宽分配进一步提升效率，是一个值得探索的方向。

4. **与其他压缩技术的协同**：混合阶轨迹对齐的框架是否可以推广到剪枝、蒸馏等其他压缩范式，形成统一的“采样感知压缩”理论，尚待研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Sampling_Aware_Quantization_for_Diffusion_Models.pdf]]
