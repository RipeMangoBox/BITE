---
title: "GENIE: Higher-Order Denoising Diffusion Solvers"
type: paper
paper_level: A
venue: NeurIPS
year: 2022
pdf_ref: paperPDFs/NEURIPS_2022/GENIE_Higher_Order_Denoising_Diffusion_Solvers.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/GENIE/
aliases:
- GHODDS
- GENIE
tags:
- NEURIPS_2022
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "ODE求解过程中的高阶梯度项（尤其是Jacobian-向量积），通过引入这些项可以显著提高单步精度，从而允许更大的求解步长。"
primary_logic: "利用自动微分从预训练的一阶得分网络中提取二阶Jacobian-向量积，并将其蒸馏到一个轻量级预测头部，可以在几乎不增加计算成本的情况下实现二阶Taylor方法（GENIE）求解生成ODE，大幅减少所需函数评估次数（NFE）而保持或提高生成质量。"
claims:
- "GENIE在CIFAR-10上仅需10步NFE即达到FID 5.28，显著优于DDIM的11.6"
- "GENIE比DDIM具有更小的局部截断误差（LTE）和全局截断误差（GTE）"
- "混合网络参数化和权重函数对性能至关重要，消融显示去除后FID显著变差"
- "CIFAR-10 (unconditional) 上 FID = 6.27 (NFE=10, with AFS and denoising)"
---

# GENIE: Higher-Order Denoising Diffusion Solvers

> [!tip] 核心洞察
> 利用自动微分从预训练的一阶得分网络中提取二阶Jacobian-向量积，并将其蒸馏到一个轻量级预测头部，可以在几乎不增加计算成本的情况下实现二阶Taylor方法（GENIE）求解生成ODE，大幅减少所需函数评估次数（NFE）而保持或提高生成质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GENIE：高阶去噪扩散求解器 |
| 英文题名 | GENIE: Higher-Order Denoising Diffusion Solvers |
| 会议/期刊 | NeurIPS 2022 |
| Links | [paper](https://arxiv.org/abs/2210.05475) · [Project](https://nv-tlabs.github.io/GENIE) · [Project](https://research.nvidia.com/labs/toronto-ai/GENIE/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GENIE (Higher-Order Denoising Diffusion Solver) |
| Dataset | CIFAR-10 (unconditional), ImageNet 64x64 (conditional), LSUN Bedrooms (unconditional), LSUN Church-Outdoor (unconditional) |

> [!tip] 效果简介
> - CIFAR-10 (unconditional) 上，FID 为 6.27 (NFE=10, with AFS and denoising)，对比 11.2 (DDIM, NFE=10, with AFS and denoising)，变化 4.93。
> - ImageNet 64x64 (conditional) 上，FID 为 7.41 (NFE=10, with AFS and denoising)，对比 10.7 (DDIM, NFE=10, with AFS and denoising)，变化 3.29。
> - LSUN Bedrooms (unconditional) 上，FID 为 9.29 (NFE=10, with AFS and denoising)，对比 12.5 (DDIM, NFE=10, with AFS and denoising)，变化 3.21。

## 概要

扩散模型在高维数据上的概率流常微分方程（ODE）求解面临一个核心瓶颈：一阶求解器（如DDIM）无法捕捉ODE的局部曲率，导致截断误差大，必须采用大量小步长才能保证生成质量。GENIE（Higher-Order Denoising Diffusion Solver）针对这一问题，提出了一种二阶截断泰勒方法（TTM），通过引入高阶梯度项（尤其是Jacobian-向量积，JVP）来显著提高单步精度，从而在几乎不增加计算成本的情况下大幅减少所需函数评估次数（NFE）。

该方法的核心洞察在于：利用自动微分从预训练的一阶得分网络中提取二阶JVP，并将其蒸馏到一个轻量级预测头部，使二阶Taylor更新步骤的计算开销极小（CIFAR-10模型仅增加约1.5%）。实验表明，GENIE在多个基准上以更少的NFE显著超越了一阶求解器：在CIFAR-10上仅需10步NFE即达到FID 5.28（DDIM为11.6），在ImageNet 64×64和LSUN Bedrooms/Church-Outdoor上同样保持一致的FID优势。消融实验证实，混合网络参数化和权重函数对性能至关重要，去除后FID显著变差。

GENIE的局限性在于仅探索了二阶方法，三阶TTM在少步数时反而不如二阶；此外，它仍运行在生成ODE框架内，无法像蒸馏方法那样实现单步生成。尽管如此，GENIE为扩散模型的快速采样提供了一条高效的高阶求解路径，其轻量级设计使其易于集成到现有预训练模型中。



扩散模型已成为高维连续数据生成建模的核心范式，其生成过程通常被形式化为一个逆向随机微分方程（SDE）或与之等价的概率流常微分方程（Probability Flow ODE）。在实际部署中，概率流ODE因其确定性采样特性而备受青睐，然而，**该ODE在高维数据下的高效求解构成了根本性瓶颈**。

现有的一阶求解器，如 **DDIM**（Song et al., ICLR 2021）所采用的Euler方法，在求解该ODE时需要大量小步长才能保证生成质量。其根本原因在于：一阶方法仅利用ODE向量场的当前值进行线性外推，**无法捕捉向量场的局部曲率**，导致每一步的截断误差随步长增大而急剧累积。如 Figure 1 所示，一阶方法在曲率显著的区域会偏离真实ODE轨迹，迫使采样过程必须采用保守的小步长策略，从而大幅增加了函数评估次数（NFE）和推理延迟。

针对这一效率瓶颈，现有加速采样研究主要沿着两条路径展开：一是基于线性多步法（如 **S-PNDM** 和 **F-PNDM**，Liu et al., ICLR 2022）的二阶求解器，它们通过利用历史步骤信息来提升精度，但本质上仍是对一阶梯度场的插值近似，并未显式建模ODE的高阶导数；二是知识蒸馏方法（如渐进蒸馏），通过将多步采样过程压缩为单步模型来绕过ODE求解，但这类方法改变了模型本身，失去了与预训练得分模型的即插即用兼容性。

**本文的核心动机在于填补这一方法学空白**：能否在不改变预训练一阶得分网络的前提下，显式引入ODE的高阶导数信息，从而构造一个真正意义上的高阶求解器，在更少的NFE下实现更精确的生成轨迹？这一思路面临的关键挑战在于——高阶导数（尤其是Jacobian-向量积，JVP）的计算成本在深度神经网络中通常极为高昂。

GENIE的突破性洞察在于：**利用自动微分从预训练的一阶得分网络中提取二阶JVP，并将其蒸馏到一个轻量级预测头部**，从而在几乎不增加推理计算成本的情况下，实现二阶截断泰勒方法（TTM）对生成ODE的求解。这一设计使得GENIE能够以二阶精度捕捉ODE的局部曲率，允许显著更大的求解步长，同时保持对任意预训练扩散模型的即插即用兼容性。



## 核心方法与创新机理

GENIE的核心创新在于将**二阶截断泰勒方法（Truncated Taylor Method, TTM）**引入扩散模型的概率流ODE求解，并通过**梯度蒸馏**以极低计算开销获取所需的高阶导数项，从而在显著减少函数评估次数（NFE）的同时保持或提升生成质量。

### 创新一：从一阶到二阶的求解范式跃迁

现有快速采样器（如**DDIM**，Song et al., ICLR 2021）本质上是基于一阶Euler方法的ODE求解器，其更新仅依赖当前点的梯度方向，无法捕捉ODE的局部曲率，导致截断误差随步长增大而急剧累积。GENIE将求解器阶数从一阶提升至二阶，其更新公式为：

$$\bar{\mathbf{x}}_{t_{n+1}} = \bar{\mathbf{x}}_{t_n} + h_n \epsilon_{\theta}(\mathbf{x}_{t_n}, t_n) + \frac{1}{2} h_n^2 \frac{d\epsilon_{\theta}}{d\gamma_t}\big|_{\mathbf{x}_{t_n}, t_n}$$

新增的二阶项 $\frac{1}{2} h_n^2 d_{\gamma_t}\epsilon_{\theta}$ 显式建模了得分场沿ODE轨迹的局部曲率，使得单步外推更精确，从而允许更大的求解步长。实验证据表明，在相同NFE下，GENIE的局部截断误差（LTE）和全局截断误差（GTE）均显著低于DDIM（Figure 14, Figure 15），这直接解释了其生成质量的提升。

### 创新二：基于自动微分的梯度蒸馏机制

二阶TTM的关键瓶颈在于如何高效获取高阶导数 $d_{\gamma_t}\epsilon_{\theta}$。该全导数可分解为两个Jacobian-向量积（JVP）和一个时间导数项：

$$d_{\gamma_t}\epsilon_{\theta} = \frac{1}{\sqrt{\gamma_t^2+1}} \frac{\partial \epsilon_{\theta}}{\partial \mathbf{x}_t}\epsilon_{\theta} - \frac{\gamma_t}{1+\gamma_t^2} \frac{\partial \epsilon_{\theta}}{\partial \mathbf{x}_t}\mathbf{x}_t + \frac{\partial \epsilon_{\theta}}{\partial t}\frac{dt}{d\gamma_t}$$

GENIE的解决方案是**梯度蒸馏**：利用自动微分从预训练的一阶得分网络 $\epsilon_{\theta}$ 中精确计算上述JVP作为监督信号，然后将其蒸馏到一个轻量级预测头部 $k_{\psi}$ 中。该预测头部以 $\epsilon_{\theta}$ 的中间特征为输入，通过混合网络参数化输出三个子网络的加权组合来近似 $d_{\gamma_t}\epsilon_{\theta}$：

$$k_{\psi} = -\frac{1}{\gamma_t}k_{\psi}^{(1)} + \frac{\gamma_t}{1+\gamma_t^2}k_{\psi}^{(2)} + \frac{1}{\gamma_t(1+\gamma_t^2)}k_{\psi}^{(3)}$$

这一设计的核心优势在于：推理时无需执行昂贵的自动微分，仅通过一次前向传播即可同时获得一阶得分 $\epsilon_{\theta}$ 和高阶导数 $k_{\psi}$，额外计算开销极低（CIFAR-10模型上约1.5%）。

### 创新三：混合参数化与加权蒸馏损失

消融实验揭示了两个关键设计选择对性能的决定性作用：

1. **混合网络参数化**：将JVP分解为三个独立输出通道并按时间相关系数组合，去除该设计后FID显著上升（CIFAR-10, NFE=5时从13.9升至14.7，Table 2）。
2. **权重函数 $g_d(t) = \gamma_t^2$**：在蒸馏损失中对不同时间步施加差异化权重，去除后性能大幅下降（NFE=5时FID从13.9升至14.8，NFE=15时退化更明显，Table 2）。

这些消融结果表明，高阶导数在不同噪声水平下的尺度差异巨大，混合参数化和时间感知权重对于稳定蒸馏过程、使预测头部准确学习JVP至关重要。

### 与相关工作的本质区别

与基于线性多步法的二阶求解器（如**S-PNDM**、**F-PNDM**，Liu et al., ICLR 2022）不同，GENIE直接使用高阶得分信息（蒸馏后的JVP）进行生成建模，而非通过有限差分或其他近似方式间接利用历史梯度信息。在相同低NFE设置下，GENIE始终提供更低的FID（Figure 5），验证了显式高阶导数建模相对于隐式多步方法的优势。



GENIE 是一个基于二阶截断泰勒方法（Truncated Taylor Method, TTM）的扩散模型快速采样框架。其核心思路是将扩散模型的标准概率流 ODE（DDIM ODE）从一阶 Euler 求解提升为二阶求解，从而在更大的步长下保持高精度生成，大幅减少所需的函数评估次数（NFE）。

### Pipeline 总览

整个框架由三个核心模块串联构成，形成“预训练—蒸馏—采样”的清晰流水线：

1. **一阶得分网络 ε_θ**：一个预训练的去噪扩散模型，接收带噪数据 x_t 和时间 t，输出噪声预测 ε_θ(x_t, t)。该网络同时提供中间层特征，供下游模块复用。
2. **预测头部 k_ψ**：一个轻量级的神经网络输出头，直接附加在 ε_θ 的最后一个特征层之上（见 Figure 4）。它以 ε_θ 的中间特征为输入，输出对高阶梯度项 d_{γ_t} ε_θ 的近似。该模块通过梯度蒸馏（Gradient Distillation）训练：利用自动微分从 ε_θ 中计算出精确的 Jacobian-向量积（JVP）作为目标，最小化加权 L2 损失来训练 k_ψ。
3. **二阶 Taylor 更新步骤**：在采样阶段，GENIE 使用当前的噪声预测 ε_θ(x_t, t) 和预测头部 k_ψ 输出的高阶导数近似，执行二阶 Taylor 更新方程（Eq. 9），从 x_{t_n} 一步推进到 x_{t_{n+1}}。

### 数据流与模块关系

在推理时，数据流如下：

**输入** → **ε_θ 前向传播** → **特征共享** → **k_ψ 预测高阶导数** → **二阶 Taylor 更新** → **输出**

具体而言：
- 当前状态 x_t 和时间 t 输入 ε_θ，得到噪声预测 ε_θ(x_t, t) 和中间特征。
- 中间特征被送入预测头部 k_ψ，输出三个子网络预测值 k_ψ^{(1)}, k_ψ^{(2)}, k_ψ^{(3)}，通过混合参数化公式（Eq. 14）组合为高阶导数 d_{γ_t} ε_θ 的近似：

$$k_{\psi} = -\frac{1}{\gamma_t}k_{\psi}^{(1)} + \frac{\gamma_t}{1+\gamma_t^2}k_{\psi}^{(2)} + \frac{1}{\gamma_t(1+\gamma_t^2)}k_{\psi}^{(3)}$$

- 最后，将 ε_θ 和 k_ψ 的输出代入二阶 TTM 更新公式，完成一步采样：

$$\bar{\mathbf{x}}_{t_{n+1}} = \bar{\mathbf{x}}_{t_n} + h_n \epsilon_{\theta}(\mathbf{x}_{t_n}, t_n) + \frac{1}{2} h_n^2 \frac{d\epsilon_{\theta}}{d\gamma_t}\big|_{\mathbf{x}_{t_n}, t_n}$$

### 关键设计要点

**高阶导数的获取**是 GENIE 区别于其他快速采样器的核心。d_{γ_t} ε_θ 的全导数可分解为两个 Jacobian-向量积项和一个时间导数项（Eq. 12）：

$$d_{\gamma_t}\epsilon_{\theta} = \frac{1}{\sqrt{\gamma_t^2+1}} \frac{\partial \epsilon_{\theta}}{\partial \mathbf{x}_t}\epsilon_{\theta} - \frac{\gamma_t}{1+\gamma_t^2} \frac{\partial \epsilon_{\theta}}{\partial \mathbf{x}_t}\mathbf{x}_t + \frac{\partial \epsilon_{\theta}}{\partial t}\frac{dt}{d\gamma_t}$$

这些项通过自动微分从 ε_θ 中精确计算，然后蒸馏到 k_ψ 中。这种设计使得 GENIE 在推理时无需执行昂贵的二阶自动微分，仅需一次额外的轻量级前向传播（开销在 CIFAR-10 上约 1.5%），即可获得二阶精度。

**与一阶方法的本质区别**：DDIM（Song et al., ICLR 2021）等一阶求解器仅使用 ε_θ 的当前值进行线性外推，无法捕捉 ODE 梯度场的局部曲率。GENIE 通过引入高阶梯度项，使单步更新能够适应梯度场的变化方向（见 Figure 1 的示意对比），从而在相同步长下显著降低局部截断误差（LTE）和全局截断误差（GTE）（见 Figure 14、Figure 15 的定量验证）。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/001_Figure_1.jpg]]
*Figure 1: Our novel Higher-Order Denoising Diffusion Solver (GENIE) relies on the second truncated Taylor method (TTM) to simulate a (re-parametrized) Probability Flow ODE for sampling from denoising diffusion models. The second TTM captures the local curvature of the ODE’s gradient field and enables more accurate extrapolation and larger step sizes than the first TTM (Euler’s method), which previous methods such as DDIM [58] utilize*



### 一阶基座：DDIM 概率流 ODE 的重参数化

GENIE 的求解对象是 DDIM 所对应的概率流 ODE。论文将 DDIM 的生成过程重参数化为一个关于虚拟时间变量 $\gamma_t$ 的简洁形式：

$$d \bar{\mathbf{x}}_t = \epsilon_{\theta}(\mathbf{x}_t, t) \, d\gamma_t$$

其中 $\epsilon_{\theta}$ 是预训练的一阶去噪网络，$\gamma_t = \alpha_t / \sigma_t$ 是信噪比相关的单调函数。这一重参数化将原本复杂的扩散 ODE 转化为一个形式上极为简单的常微分方程，为后续引入高阶 Taylor 方法提供了干净的数学结构（见 Eq. (6)）。

### 核心更新步：二阶截断 Taylor 方法

GENIE 的核心思想是将二阶截断 Taylor 方法（Second Truncated Taylor Method, TTM）应用于上述 DDIM ODE。通用的 $p$ 阶 TTM 格式为：

$$\mathbf{y}_{t_{n+1}} = \mathbf{y}_{t_n} + h_n \frac{d\mathbf{y}}{dt}\Big|_{(\mathbf{y}_{t_n}, t_n)} + \cdots + \frac{1}{p!} h_n^p \frac{d^p\mathbf{y}}{dt^p}\Big|_{(\mathbf{y}_{t_n}, t_n)}$$

将其应用于 DDIM ODE（即取 $p=2$），得到 GENIE 的采样迭代公式：

$$\bar{\mathbf{x}}_{t_{n+1}} = \bar{\mathbf{x}}_{t_n} + h_n \epsilon_{\theta}(\mathbf{x}_{t_n}, t_n) + \frac{1}{2} h_n^2 \frac{d\epsilon_{\theta}}{d\gamma_t}\Big|_{\mathbf{x}_{t_n}, t_n}$$

其中 $h_n = \gamma_{t_{n+1}} - \gamma_{t_n}$ 为步长。与一阶 Euler 方法（DDIM）相比，GENIE 增加了二阶项 $\frac{1}{2} h_n^2 \, d_{\gamma_t}\epsilon_{\theta}$，该二阶项能够捕捉 ODE 梯度场的局部曲率，从而允许更大的求解步长并显著降低截断误差（见 Eq. (9)）。

### 高阶导数的来源：Jacobian-向量积分解

二阶 TTM 的关键在于计算全导数 $d_{\gamma_t}\epsilon_{\theta}$。通过链式法则，该全导数可分解为三个分量：

$$d_{\gamma_t}\epsilon_{\theta} = \frac{1}{\sqrt{\gamma_t^2+1}} \frac{\partial \epsilon_{\theta}}{\partial \mathbf{x}_t} \epsilon_{\theta} - \frac{\gamma_t}{1+\gamma_t^2} \frac{\partial \epsilon_{\theta}}{\partial \mathbf{x}_t} \mathbf{x}_t + \frac{\partial \epsilon_{\theta}}{\partial t} \frac{dt}{d\gamma_t}$$

其中前两项为 Jacobian-向量积（JVP），第三项为时间偏导数。这里的 Jacobian $\partial \epsilon_{\theta} / \partial \mathbf{x}_t$ 与二阶得分函数直接相关：

$$\frac{\partial \epsilon_{\theta}(\mathbf{x}_t, t)}{\partial \mathbf{x}_t} = -\sigma_t \frac{\partial \mathbf{s}_{\theta}(\mathbf{x}_t, t)}{\partial \mathbf{x}_t} \approx -\sigma_t \nabla_{\mathbf{x}_t}^{\top} \nabla_{\mathbf{x}_t} \log p_t(\mathbf{x}_t)$$

因此，GENIE 本质上是利用了预训练一阶得分网络所隐含的二阶得分信息（见 Eq. (12) 及 Section 3.1）。

### 蒸馏模块：轻量级预测头部 $k_{\psi}$

直接通过自动微分在每次采样步计算上述 JVP 会带来显著的计算开销。GENIE 的解决方案是将这些高阶导数蒸馏到一个轻量级预测头部 $k_{\psi}$ 中。该头部附加在预训练得分网络 $\epsilon_{\theta}$ 的最后一个特征层之上，共享大部分主干网络参数，仅新增少量绿色专属层（见 Figure 4）。

为稳定训练并适应不同时间步的数值尺度，$k_{\psi}$ 采用混合网络参数化（mixed network parameterization），将输出分解为三个子网络的加权组合：

$$k_{\psi} = -\frac{1}{\gamma_t} k_{\psi}^{(1)} + \frac{\gamma_t}{1+\gamma_t^2} k_{\psi}^{(2)} + \frac{1}{\gamma_t(1+\gamma_t^2)} k_{\psi}^{(3)}$$

这三个子通道 $k_{\psi}^{(1)}, k_{\psi}^{(2)}, k_{\psi}^{(3)}$ 分别对应 JVP 分解中的不同分量。蒸馏训练的目标函数为加权 L2 损失：

$$\min_{\psi} \mathbb{E}_{t, \mathbf{x}_0, \epsilon} \left[ g_d(t) \left\| k_{\psi}(\mathbf{x}_t, t) - d_{\gamma_t} \epsilon_{\theta}(\mathbf{x}_t, t) \right\|_2^2 \right]$$

其中 $g_d(t) = \gamma_t^2$ 是权重函数，用于平衡不同时间步的损失尺度。消融实验表明，混合参数化和权重函数对最终性能至关重要：去除混合参数化后，CIFAR-10 上 NFE=5 时的 FID 从 13.9 升至 14.7；去除权重函数后，FID 进一步升至 14.8（见 Table 2）。

### 管线模块总结

GENIE 的完整采样管线由三个模块串联构成：

1. **一阶得分网络 $\epsilon_{\theta}$**：预训练的去噪模型，提供去噪预测和中间特征。
2. **预测头部 $k_{\psi}$**：以 $\epsilon_{\theta}$ 的中间特征为输入，输出高阶导数 $d_{\gamma_t}\epsilon_{\theta}$ 的近似值。训练时通过自动微分计算目标 JVP 进行蒸馏，推理时直接前向传播，额外计算开销极小（CIFAR-10 模型不到 2%）。
3. **二阶 Taylor 更新步**：将 $\epsilon_{\theta}$ 的输出和 $k_{\psi}$ 的预测代入 GENIE 迭代公式，完成一步采样更新。

需要注意的是，$k_{\psi}$ 的训练需要在全精度下进行，因为混合精度下计算 $\partial \epsilon_{\theta} / \partial t$ 时会出现数值不稳定（NaN），这是该方法的一个实际工程限制。



## 实验与关键发现

### 核心定量结果

GENIE 在多个标准图像生成基准上以极低的函数评估次数（NFE）实现了显著优于一阶求解器 DDIM 的 FID 指标。在 CIFAR-10 无条件生成任务中，GENIE 仅需 10 步 NFE 即可达到 FID 5.28，而 DDIM 在相同步数下 FID 为 11.6（Table 1）。在启用 Analytical First Step（AFS）和去噪步骤的扩展配置下，GENIE 在 10 步 NFE 时取得 FID 6.27，DDIM 为 11.2，差距达 4.93（Table 8）。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/025_Table_8.jpg]]
*Table 8: Unconditional CIFAR-10 generative performance (measured in FID). Methods above the middle line use the same score model checkpoint; methods below all use different ones. (†): numbers are taken from literature. This table is an extension of Tab. 1*

在更大规模数据集上，GENIE 同样保持一致的领先优势：
- **ImageNet 64×64**（条件生成）：GENIE 在 10 步 NFE 下 FID 为 7.41，DDIM 为 10.7，差距 3.29（Table 9）。
- **LSUN Bedrooms**（无条件）：GENIE 在 10 步 NFE 下 FID 为 9.29，DDIM 为 12.5，差距 3.21（Table 10）。
- **LSUN Church-Outdoor**（无条件）：GENIE 在 10 步 NFE 下 FID 为 10.5，DDIM 为 12.8，差距 2.3（Table 11）。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/026_Table_9.jpg]]
*Table 9: Conditional ImageNet generative performance (measured in FID)*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/027_Table_10.jpg]]
*Table 10: Unconditional LSUN Bedrooms generative performance (measured in FID). Methods above the middle line use the same score model checkpoint; Learned Sampler uses a different one. (†): numbers are taken from literature*

与二阶线性多步法求解器 S-PNDM 和 F-PNDM（Liu et al., ICLR 2022）相比，GENIE 在相同低 NFE 设置下始终提供更低的 FID（Figure 5）。所有比较均使用同一预训练得分模型检查点，确保公平性。

### 误差分析：截断误差的定量证据

GENIE 的性能优势根源于其更低的局部截断误差（LTE）和全局截断误差（GTE）。在 LSUN Church-Outdoor 数据集上，以 DDIM 1000 步 NFE 的生成结果作为近似真实值进行测量：

- **局部截断误差**（Figure 15）：在三个代表性时间点 $t \in \{0.1, 0.2, 0.5\}$ 上，GENIE 的单步 L2 距离均显著小于 DDIM。这表明二阶 Taylor 方法确实捕捉到了 ODE 的局部曲率，使单步外推更加精确。
- **全局截断误差**（Figure 14）：GENIE 在 Inception 特征空间中的 L2 距离明显低于 DDIM、S-PNDM 和 F-PNDM 等快速采样器。全局误差的降低直接对应了生成样本质量的提升。

在玩具 2D 数据集上的定性实验（Figure 2）进一步验证了这一机制：DDIM 在 25 步求解后仍然采样到模态之间的低密度区域，而 GENIE 的样本仅呈现轻微噪声，更接近真实分布。

### 消融实验：关键设计选择

CIFAR-10 上的消融实验（Table 2）揭示了 GENIE 中两个关键设计组件的重要性：

1. **混合网络参数化**：移除混合参数化（即 $k_\psi$ 的三个子网络加权组合，Eq. (14)）后，在 NFE=5 时 FID 从 13.9 升至 14.7。混合参数化通过将高阶梯度分解为三个独立通道，稳定了蒸馏训练并适应不同时间步的数值特性。

2. **权重函数 $g_d(t) = \gamma_t^2$**：移除该权重函数后，NFE=5 时 FID 从 13.9 升至 14.8，而在 NFE=15 时性能下降更为显著。权重函数的作用在于平衡不同时间步的蒸馏损失，使得预测头部能够在整个扩散时间范围内准确学习 JVP。

### 计算开销与公平性

GENIE 的额外预测头部 $k_\psi$ 引入了少量计算开销：在 CIFAR-10 模型上约为 1.5%（Sec. 5）。论文在比较 NFE 时未计入该开销，但已明确标注并考虑了这一因素。预测头部的蒸馏训练需要约 5 万次迭代（Table 5），且由于自动微分计算 $\partial \epsilon_\theta / \partial t$ 时混合精度下出现数值不稳定（NaN），训练不得不在全精度下进行，这可能影响训练速度和内存占用。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/018_Table_5.jpg]]
*Table 5: Model hyperparameters and training details for the prediction heads*

AFS 和去噪步骤作为超参数被统一应用于所有比较方法，选择各自最佳配置进行报告，保证了实验对比的公平性。

### 局限性：高阶方法的边界

尽管二阶 Taylor 方法在多数场景下表现优异，论文也揭示了高阶方法的边界：

- 在 CIFAR-10 上尝试三阶 TTM 时，少步数设置下性能反而不如二阶方法。这表明更高阶导数难以被准确学习，或者优化过程本身成为瓶颈。
- GENIE 仍然运行在生成 ODE 框架内，无法像基于蒸馏的方法（如 Progressive Distillation）那样实现单步或极少步数生成。
- 预测头部的额外训练增加了流程复杂度，且需要全精度训练以避免数值不稳定。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/010_Figure_7.jpg]]
*Figure 7: Classifier-free guidance for the ImageNet classes Pembroke Welsh Corgi (263) and Streetcar (829)*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/008_Table.jpg]]

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/012_Table.jpg]]

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/013_Table.jpg]]

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/017_Table_4.jpg]]
*Table 4: Model hyperparameters and training details. The CIFAR-10 model is taken from Song et al. [57]; all other models are trained by ourselves*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/021_Table_6.jpg]]
*Table 6: Unconditional CIFAR-10 generative performance, measured in Recall (higher values are better). All methods use the same score model checkpoint*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2210_05475/figures/022_Table_7.jpg]]
*Table 7: Unconditional CIFAR-10 generative performance (measured in FID) using our GENIE and DDIM [58] with different striding schedules using exponents $\rho \in \{$ 1 . 5 , 2 . 0 , 2 . 5 $\}$



## 定位与知识库关联

### 与基线方法的关系

GENIE 的核心定位是将扩散模型的生成过程显式地视为一个**常微分方程（ODE）的数值求解问题**，并首次将**二阶截断泰勒方法（Truncated Taylor Method, TTM）**引入该领域。这与现有工作形成了清晰的方法谱系。

**一阶求解器基线**：GENIE 直接对标的是基于一阶 Euler 方法的 **DDIM**（Song et al., ICLR 2021）。DDIM 将生成过程重参数化为一个概率流 ODE，但其求解仅利用当前点的梯度（即一阶得分函数 $\epsilon_\theta$），本质上是一阶 TTM。这导致其在较大步长时无法捕捉 ODE 的局部曲率，产生显著的截断误差。GENIE 通过引入二阶梯度项 $d_{\gamma_t}\epsilon_\theta$，在理论上将局部截断误差从 $\mathcal{O}(h^2)$ 降至 $\mathcal{O}(h^3)$，从而允许更大的求解步长。这一理论优势在实验中得到了直接验证：在 CIFAR-10 上，GENIE 仅需 10 步 NFE 即达到 FID 5.28，而 DDIM 为 11.6（Table 1 及扩展 Table 8）。Figure 15 的局部截断误差（LTE）分析和 Figure 14 的全局截断误差（GTE）分析进一步从数值分析角度证实了 GENIE 在每个单步和整个轨迹上的误差均显著低于 DDIM。

**多步法与通用 ODE 求解器基线**：GENIE 也与基于线性多步法的求解器进行了比较，包括 **S-PNDM** 和 **F-PNDM**（Liu et al., ICLR 2022）。这些方法通过组合历史梯度信息来提高精度，属于多步法范畴，而 GENIE 是单步法（仅依赖当前点的高阶导数）。在 Figure 5 的 FID-NFE 曲线对比中，GENIE 在低 NFE 设置下始终提供更优的样本质量，表明单步高阶信息比多步历史信息在少步数场景下更为有效。此外，论文还将 GENIE 与通用自适应步长 Runge-Kutta 方法（RK4(5)）和随机求解器 Euler-Maruyama 进行了对比，进一步确立了专用二阶求解器在扩散模型生成任务上的优势。

**与蒸馏方法的区别**：GENIE 的方法谱系与基于蒸馏的加速方法（如 Progressive Distillation）有本质区别。蒸馏方法通过将多步采样过程压缩到极少的步骤中，改变的是模型本身；而 GENIE 保持预训练的一阶得分网络 $\epsilon_\theta$ 不变，仅在其上添加一个轻量级预测头部 $k_\psi$ 来近似高阶导数，改变的是求解器的阶数。这使得 GENIE 可以即插即用地应用于任何预训练扩散模型，而不需要重新训练整个采样管线。但这也意味着 GENIE 无法像蒸馏方法那样实现单步或极少步数生成，其有效步数通常仍在 5-15 NFE 范围内。

### 适用边界与关键假设

GENIE 的有效性建立在以下关键假设和技术边界之上：

1. **ODE 框架的固有限制**：GENIE 完全在确定性概率流 ODE 框架内运行，不涉及随机微分方程（SDE）的随机项。这意味着它继承了 ODE 采样的特性：样本多样性可能不如 SDE 求解器，但轨迹更稳定、可复现。论文中明确将 Euler-Maruyama 列为基线 SDE 求解器，但 GENIE 本身并未将高阶导数引入随机采样过程。

2. **二阶精度的收益上限**：论文仅研究了二阶 TTM。在 CIFAR-10 上的初步实验表明，三阶 TTM 在少步数时反而不如二阶方法。这一现象暗示，更高阶导数的学习难度和数值不稳定性可能抵消理论精度增益，二阶可能是在当前模型容量和训练范式下的一个“甜点”。该问题被论文列为开放问题，需要进一步研究。

3. **梯度蒸馏的数值代价**：高阶导数 $d_{\gamma_t}\epsilon_\theta$ 的计算依赖自动微分（AD）对一阶得分网络求取 Jacobian-向量积（JVP）。论文明确指出，在混合精度训练下，计算 $\partial\epsilon_\theta/\partial t$ 时会出现数值不稳定（产生 NaN），因此蒸馏训练不得不在全精度下进行。这增加了训练时的内存和计算开销，尽管推理时预测头部 $k_\psi$ 的额外开销很小（CIFAR-10 模型约 1.5%）。

4. **预测头部的泛化能力**：$k_\psi$ 被设计为 $\epsilon_\theta$ 最后一层特征上的轻量级附加输出头，其学习目标是通过加权 L2 损失拟合从教师网络（$\epsilon_\theta$ 本身）通过 AD 计算出的 JVP 真值。这意味着 $k_\psi$ 的精度受限于教师网络的质量和蒸馏过程的充分性。论文报告的蒸馏训练仅需约 5 万次迭代，但这一开销是否可忽略取决于具体应用场景。

### 局限与开放问题

论文明确承认了以下局限性，并提出了相应的开放研究方向：

**已确认的局限**：
- **更高阶方法的收益不明确**：二阶以上 TTM 的有效性尚未得到系统验证，CIFAR-10 上的初步三阶实验结果为负面。
- **额外训练负担**：尽管预测头部 $k_\psi$ 轻量，但仍需额外的蒸馏训练阶段，增加了方法部署的复杂度。
- **数值稳定性问题**：自动微分在混合精度下的不稳定性迫使训练在全精度下进行，可能限制其在资源受限环境中的应用。
- **无法实现极低步数生成**：与基于蒸馏的方法相比，GENIE 仍需要 5-15 步 NFE，无法实现单步或两步生成。

**论文提出的开放问题**：
- **与渐进蒸馏的融合**：能否将 GENIE 的预测头部集成到渐进蒸馏流程中，以减少蒸馏所需的阶段数，同时提升最终模型的少步生成质量？
- **无 AD 的高阶学习目标**：能否开发不依赖自动微分的高阶得分匹配目标，直接学习 JVP，从而避免蒸馏过程中的 AD 计算开销和数值不稳定问题？
- **高阶导数在 SDE 中的引入**：GENIE 目前基于确定性 ODE，如何将高阶导数引入随机采样（SDE）框架，以同时获得更好的覆盖度和样本质量？
- **高阶方法的根本瓶颈**：三阶及以上 TTM 无法提供一致收益的原因是什么？是模型难以准确学习高阶导数（容量瓶颈），还是优化过程本身的不稳定性（优化瓶颈）？这需要从数值分析和学习理论两个角度进行深入研究。



## 原文 PDF

![[paperPDFs/NEURIPS_2022/GENIE_Higher_Order_Denoising_Diffusion_Solvers.pdf]]
